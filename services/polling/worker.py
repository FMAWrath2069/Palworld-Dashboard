from datetime import datetime, timezone
import time

from core.state import get_server_state
from core.storage import load_data

from services.api import get_metrics_base_count
from services.gamedata import fetch_full_data
from services.servers import get_server
from services.tunnel import get_tunnel
from services.server_status import (
    update_success,
    update_failure,
)

from .status import get_poller


def parse_timestamp(timestamp):
    if not timestamp:
        return None

    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def data_age_seconds(server):
    state = get_server_state(server["id"])

    with state.lock:
        updated = state.data.get("last_updated")

    updated = parse_timestamp(updated)

    if updated is None:
        return None

    return max(
        0,
        (datetime.now(timezone.utc) - updated).total_seconds()
    )


def data_is_expired(server):
    age = data_age_seconds(server)

    return (
        age is None or
        age >= server.get("data_refresh_seconds", 60)
    )


def poll_worker(server_id):

    poller = get_poller(server_id)
    state = get_server_state(server_id)

    last_count = -1

    with poller.lock:
        poller.running = True
        poller.connected = False
        poller.last_error = None

    while not poller.stop_event.is_set():

        server = get_server(server_id)

        if not server:
            if poller.stop_event.wait(5):
                break
            continue

        interval = server.get("poll_interval_seconds", 30)
        name = server.get("name", server_id)

        try:

            get_tunnel(server)

            with poller.lock:
                poller.connected = True

            load_data(server)

            with state.lock:
                if last_count == -1:
                    last_count = state.data.get("basecampnum", -1)

            expired = data_is_expired(server)
            current = get_metrics_base_count(server)

            if current != last_count or expired:

                if fetch_full_data(server):
                    with state.lock:
                        last_count = state.data.get("basecampnum", current)

            with poller.lock:
                poller.last_poll = datetime.now(timezone.utc)
                poller.last_success = poller.last_poll
                poller.poll_count += 1
                poller.failure_count = 0
                poller.last_error = None

            update_success(server_id)

        except Exception as e:

            with poller.lock:
                poller.connected = False
                poller.last_poll = datetime.now(timezone.utc)
                poller.failure_count += 1
                poller.last_error = str(e)

            update_failure(server_id, str(e))

            print(f"[ERROR] [{name}] {e}")

        if poller.stop_event.wait(interval):
            break

    with poller.lock:
        poller.running = False
        poller.connected = False