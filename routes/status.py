# routes/status.py

import json

from flask import Blueprint, jsonify, request

from core.state import get_server_state
from services.polling import data_age_seconds
from services.servers import get_server

status_bp = Blueprint("status", __name__)


@status_bp.route("/api/status")
def get_status():

    server_id = request.args.get("serverId", "default")

    server = get_server(server_id)

    if not server:
        return jsonify({
            "success": False,
            "error": "Server not found"
        }), 404

    state = get_server_state(server_id)

    with state.lock:

        data = state.data.copy()

        response = {
            "bases": json.loads(json.dumps(data.get("bases", []))),
            "players": json.loads(json.dumps(data.get("players", []))),
            "onlinePlayers": json.loads(json.dumps(data.get("players", []))),
            "stats": data.get("stats", {}),
            "statistics": data.get("stats", {}),
            "last_updated": data.get("last_updated"),
            "last_updated_unix": data.get("last_updated_unix"),
            "data_age_seconds": data_age_seconds(server),
            "data_refresh_seconds": server["data_refresh_seconds"],
        }

    return jsonify(response)