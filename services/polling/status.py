# services/polling/status.py

from dataclasses import dataclass, field
from datetime import datetime
import threading


@dataclass
class PollerStatus:

    server_id: str

    thread: threading.Thread | None = None
    stop_event: threading.Event = field(default_factory=threading.Event)

    running: bool = False
    connected: bool = False

    last_poll: datetime | None = None
    last_success: datetime | None = None
    last_error: str | None = None

    poll_count: int = 0
    failure_count: int = 0

    lock: threading.RLock = field(default_factory=threading.RLock)


_pollers = {}
_pollers_lock = threading.RLock()


def get_poller(server_id: str) -> PollerStatus:

    with _pollers_lock:

        poller = _pollers.get(server_id)

        if poller is None:
            poller = PollerStatus(server_id=server_id)
            _pollers[server_id] = poller

        return poller


def ensure_poller(server_id):
    
    from .worker import poll_worker

    poller = get_poller(server_id)

    with poller.lock:

        if poller.thread and poller.thread.is_alive():
            return

        poller.stop_event.clear()

        poller.thread = threading.Thread(
            target=poll_worker,
            args=(server_id,),
            daemon=True,
        )

        poller.thread.start()


def stop_poller(server_id):

    poller = get_poller(server_id)

    with poller.lock:

        if not poller.thread:
            return

        poller.stop_event.set()
        thread = poller.thread

    thread.join(timeout=10)

    with poller.lock:
        poller.thread = None
        poller.running = False
        poller.connected = False


def restart_poller(server_id):

    stop_poller(server_id)
    ensure_poller(server_id)


def remove_poller(server_id):

    stop_poller(server_id)

    with _pollers_lock:
        _pollers.pop(server_id, None)


def get_all_pollers():

    with _pollers_lock:
        return dict(_pollers)