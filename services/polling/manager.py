from threading import Lock, Thread

from .status import (
    get_all_pollers,
    get_poller,
    remove_poller,
)
from .worker import poll_worker


_lock = Lock()


def ensure_poller(server_id):

    with _lock:

        poller = get_poller(server_id)

        if (
            poller.thread and
            poller.thread.is_alive()
        ):
            return

        poller.stop_event.clear()

        poller.thread = Thread(
            target=poll_worker,
            args=(server_id,),
            daemon=True,
            name=f"Poller-{server_id}",
        )

        poller.thread.start()


def stop_poller(server_id, timeout=5):

    with _lock:
        poller = get_poller(server_id)

        if not poller.thread:
            return

        poller.stop_event.set()

        thread = poller.thread

    thread.join(timeout)

    with poller.lock:
        poller.thread = None


def restart_poller(server_id):

    stop_poller(server_id)
    ensure_poller(server_id)


def stop_all_pollers():

    for server_id in list(get_all_pollers()):
        stop_poller(server_id)


def remove_stopped_poller(server_id):

    poller = get_poller(server_id)

    if (
        poller.thread is None or
        not poller.thread.is_alive()
    ):
        remove_poller(server_id)