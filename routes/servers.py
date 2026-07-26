# /routes/servers.py
from flask import Blueprint, jsonify, request

from core.storage import (
    get_server_data_path,
    load_data,
    delete_server_data,
)

from services.polling import (
    restart_poller,
    stop_poller,
)

from services.servers import (
    get_server,
    get_server_list,
    set_server,
    delete_server,
)

from services.tunnel import stop_tunnel
from services.server_status import remove_status

servers_bp = Blueprint("servers", __name__)


@servers_bp.route("/api/servers", methods=["POST"])
def add_server():

    server = request.get_json() or {}

    server_id = server.get("id")

    if not server_id:
        return jsonify({
            "success": False,
            "error": "Missing server id"
        }), 400

    server = set_server(server)
    folder = get_server_data_path(server)

    load_data(server)

    # Always start with a fresh poller
    restart_poller(server_id)

    print(f"Created server storage: {folder}")

    return jsonify({
        "success": True,
        "server": server_id
    })


@servers_bp.route("/api/servers", methods=["GET"])
def get_servers_route():

    return jsonify(get_server_list())


@servers_bp.route("/api/servers/<server_id>", methods=["PUT"])
def update_server(server_id):

    updated_server = request.get_json() or {}

    existing_server = get_server(server_id)

    if not existing_server:
        return jsonify({
            "success": False,
            "error": "Server not found"
        }), 404

    updated_server["id"] = server_id

    if not updated_server.get("password"):
        updated_server["password"] = existing_server.get("password", "")

    for key in (
        "poll_interval_seconds",
        "data_refresh_seconds",
        "max_pal_base_distance",
        "use_ssh",
        "ssh_host",
        "ssh_port",
        "ssh_user",
        "ssh_key",
        "remote_host",
        "remote_port",
    ):
        if key not in updated_server:
            updated_server[key] = existing_server.get(key)

    server = set_server(updated_server)

    load_data(server)

    restart_poller(server_id)

    return jsonify({
        "success": True,
        "server": server
    })


@servers_bp.route("/api/servers/<server_id>", methods=["DELETE"])
def delete_server_route(server_id):

    if not get_server(server_id):
        return jsonify({
            "success": False,
            "error": "Server not found"
        }), 404

    stop_poller(server_id)
    stop_tunnel(server_id)
    remove_status(server_id)
    
    delete_server_data(get_server(server_id))
    delete_server(server_id)

    return jsonify({
        "success": True
    })