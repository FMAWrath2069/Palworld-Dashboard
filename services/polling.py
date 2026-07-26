from datetime import datetime, timezone
import threading
import time

from core.state import get_server_state
from core.storage import load_data

from services.api import get_metrics_base_count
from services.gamedata import fetch_full_data
from services.servers import get_server
from services.tunnel import get_tunnel


_poll_threads = {}
_poll_lock = threading.Lock()


def ensure_poller(server_id):

    with _poll_lock:

        thread = _poll_threads.get(server_id)

        if thread and thread.is_alive():
            return

        thread = threading.Thread(
            target=poll_metrics,
            args=(server_id,),
            daemon=True,
        )

        thread.start()

        _poll_threads[server_id] = thread

        server = get_server(server_id)
        server_name = (
            server.get("name", server_id)
            if server
            else server_id
        )

        print(f"[{server_name}] Polling thread started")


def parse_timestamp(timestamp):
    if not timestamp:
        return None

    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def data_age_seconds(server):

    server_id = server.get("id", "default")

    state = get_server_state(server_id)

    with state.lock:
        updated_at = state.data.get("last_updated")

    updated_datetime = parse_timestamp(updated_at)

    if updated_datetime is None:
        return None

    age = (
        datetime.now(timezone.utc)
        - updated_datetime
    ).total_seconds()

    return max(0, age)


def data_is_expired(server):

    age = data_age_seconds(server)

    refresh_seconds = server.get(
        "data_refresh_seconds",
        60,
    )

    return (
        age is None
        or age >= refresh_seconds
    )


def poll_metrics(server_id):

    state = get_server_state(server_id)

    last_count = -1

    while True:

        server = get_server(server_id)

        if not server:
            time.sleep(5)
            continue

        server_name = server.get("name", server_id)

        poll_interval = server.get(
            "poll_interval_seconds",
            30,
        )

        try:

            get_tunnel(server)

            load_data(server)

            with state.lock:
                if last_count == -1:
                    last_count = state.data.get(
                        "basecampnum",
                        -1,
                    )

            expired = data_is_expired(server)

            current_count = get_metrics_base_count(server)

            count_changed = (
                current_count != last_count
            )

            if count_changed or expired:

                if count_changed:
                    print(
                        f"[{server_name}] "
                        f"basecampnum changed "
                        f"from {last_count} "
                        f"to {current_count}"
                    )

                if expired:
                    print(
                        f"[{server_name}] "
                        "Saved data is older "
                        "than the refresh interval."
                    )

                if fetch_full_data(server):
                    with state.lock:
                        last_count = state.data.get(
                            "basecampnum",
                            current_count,
                        )

            else:

                age = data_age_seconds(server)

                age_text = (
                    "unknown"
                    if age is None
                    else f"{int(age)} seconds"
                )

                print(
                    f"[{server_name}] "
                    "No refresh required: "
                    f"basecampnum={current_count}, "
                    f"data_age={age_text}"
                )

        except Exception as error:
            print(
                f"[ERROR] "
                f"[{server_name}] "
                f"Polling failed: {error}"
            )

        time.sleep(poll_interval)