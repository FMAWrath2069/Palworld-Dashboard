# routes/game.py

from flask import Blueprint, request

from services.api import relay_game_request
from services.servers import (
    servers,
    servers_lock,
)

game_bp = Blueprint("game", __name__)


@game_bp.route("/api/game/<path:game_path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def relay_game_api(game_path):

    payload = None

    if request.method in {"POST", "PUT", "PATCH"}:
        payload = request.get_json(silent=True)

    return relay_game_request(
        method=request.method,
        path=game_path,
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )


@game_bp.route("/api/kick", methods=["POST"])
def kick_player():

    payload = request.get_json(silent=True) or {}

    print("KICK PAYLOAD:", payload)

    return relay_game_request(
        method="POST",
        path="v1/api/kick",
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )


@game_bp.route("/api/ban", methods=["POST"])
def ban_player():

    payload = request.get_json(silent=True) or {}

    return relay_game_request(
        method="POST",
        path="v1/api/ban",
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )


@game_bp.route("/api/unban", methods=["POST"])
def unban_player():

    payload = request.get_json(silent=True) or {}

    return relay_game_request(
        method="POST",
        path="v1/api/unban",
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )


@game_bp.route("/api/announce", methods=["POST"])
def announce():

    payload = request.get_json(silent=True) or {}

    return relay_game_request(
        method="POST",
        path="v1/api/announce",
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )


@game_bp.route("/api/save-world", methods=["POST"])
def save_world():

    payload = request.get_json(silent=True) or {}

    return relay_game_request(
        method="POST",
        path="v1/api/save",
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )


@game_bp.route("/api/shutdown", methods=["POST"])
def shutdown_server():

    payload = request.get_json(silent=True) or {}

    return relay_game_request(
        method="POST",
        path="v1/api/shutdown",
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )


@game_bp.route("/api/emergency-stop", methods=["POST"])
def emergency_stop():

    payload = request.get_json(silent=True) or {}

    return relay_game_request(
        method="POST",
        path="v1/api/stop",
        payload=payload,
        servers=servers,
        servers_lock=servers_lock,
    )