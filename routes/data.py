# routes/data.py

import json

from flask import Blueprint, jsonify, request

from core.config import SERVER_DATA_DIR
from core.state import get_server_state
from core.storage import read_server_file
from services.polling import data_age_seconds
from services.servers import get_server


data_bp = Blueprint("data", __name__)


@data_bp.route("/api/bases")
def get_bases():

    server_id = request.args.get("serverId", "default")

    server = get_server(server_id)

    if not server:
        return jsonify({
            "success": False,
            "error": "Server not found"
        }), 404

    return jsonify(
        read_server_file(
            server,
            SERVER_DATA_DIR,
            "bases.json",
            []
        )
    )


@data_bp.route("/api/players")
def get_players():

    server_id = request.args.get("serverId", "default")

    server = get_server(server_id)

    if not server:
        return jsonify({
            "success": False,
            "error": "Server not found"
        }), 404

    return jsonify(
        read_server_file(
            server,
            SERVER_DATA_DIR,
            "players.json",
            []
        )
    )


@data_bp.route("/api/stats")
def get_stats():

    server_id = request.args.get("serverId", "default")

    server = get_server(server_id)

    if not server:
        return jsonify({
            "success": False,
            "error": "Server not found"
        }), 404

    stats = read_server_file(
        server,
        SERVER_DATA_DIR,
        "stats.json",
        {}
    )

    metadata = read_server_file(
        server,
        SERVER_DATA_DIR,
        "metadata.json",
        {}
    )

    return jsonify({
        "stats": stats,
        **metadata
    })


@data_bp.route("/api/data")
def get_all_data():

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
            "basecampnum": data.get("basecampnum", 0),
            "stats": data.get("stats", {}),
            "last_updated": data.get("last_updated"),
            "last_updated_unix": data.get("last_updated_unix"),
            "data_age_seconds": data_age_seconds(server),
            "data_refresh_seconds": server["data_refresh_seconds"],
        }

    return jsonify(response)