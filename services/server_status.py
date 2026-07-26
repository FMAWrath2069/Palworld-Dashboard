# services/server_status.py
from datetime import datetime, timezone
import threading


_status = {}
_lock = threading.RLock()


def _now():
    return datetime.now(timezone.utc).isoformat()


def set_status(server_id, status, message=None):
    with _lock:
        state = _status.setdefault(server_id, {})

        state["status"] = status
        state["message"] = message

        now = _now()

        state["last_seen"] = now

        if status == "online":
            state["last_success"] = now
        elif status in ("offline", "error"):
            state["last_failure"] = now


def update_success(server_id):
    with _lock:
        state = _status.setdefault(server_id, {})

        now = _now()

        if state.get("status") != "online":
            state["status"] = "online"

        state["message"] = None
        state["last_seen"] = now
        state["last_success"] = now


def update_failure(server_id, message=None):
    with _lock:
        state = _status.setdefault(server_id, {})

        state["status"] = "offline"
        state["message"] = message
        state["last_failure"] = _now()


def get_status(server_id):
    with _lock:
        return dict(
            _status.get(
                server_id,
                {
                    "status": "unknown",
                    "message": None,
                    "last_seen": None,
                    "last_success": None,
                    "last_failure": None,
                },
            )
        )


def get_all_status():
    with _lock:
        return {
            server_id: dict(value)
            for server_id, value in _status.items()
        }


def remove_status(server_id):
    with _lock:
        _status.pop(server_id, None)