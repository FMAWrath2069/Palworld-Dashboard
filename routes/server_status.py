# routes/server_status.py

from flask import Blueprint, jsonify

from services.server_status import get_all_status

server_status_bp = Blueprint("server_status", __name__)


@server_status_bp.route("/api/server-status", methods=["GET"])
def server_status():

    return jsonify(get_all_status())