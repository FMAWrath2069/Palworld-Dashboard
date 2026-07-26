# services/api.py

import requests
from flask import jsonify

from services.tunnel import get_connection


def get_api_headers(password=""):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    if password:
        headers["Authorization"] = f"Basic {password}"

    return headers


def api_call(url, password=""):

    headers = get_api_headers(password)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        raise RuntimeError(
            f"API call to {url} failed: {error}"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            f"API response from {url} was not valid JSON: {error}"
        ) from error


def game_server_url(path, server):
    host, port = get_connection(server)

    path = str(path).lstrip("/")

    return f"http://{host}:{port}/{path}"


def relay_game_request(
    method,
    path,
    payload,
    servers,
    servers_lock,
    password=""
):
    print("\n===== GAME PAYLOAD =====")
    print(payload)
    print("========================")
    server_id = payload.get("serverId") if payload else None

    with servers_lock:
        server = servers.get(server_id)

    if not server:
        return jsonify({
            "success": False,
            "error": "Unknown server"
        }), 400

    server_password = server.get("password", password)

    url = game_server_url(path, server)
    headers = get_api_headers(server_password)
    print(f"Sending {method} to {url}")
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=payload,
            timeout=30
        )

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        response_payload = None

        if "application/json" in content_type:
            try:
                response_payload = response.json()
            except ValueError:
                response_payload = None

        if not response.ok:
            return jsonify({
                "success": False,
                "error": response_payload or response.text,
                "status_code": response.status_code
            }), response.status_code

        if response_payload is not None:
            return jsonify(response_payload), response.status_code

        return jsonify({
            "success": True,
            "status_code": response.status_code,
            "response": response.text
        }), response.status_code

    except requests.RequestException as error:

        print(f"[API ERROR] {error}")

        return jsonify({
            "success": False,
            "error": "Unable to communicate with the game server."
        }), 502


def get_metrics_base_count(server, password=""):
    url = game_server_url(
        "v1/api/metrics",
        server
    )

    password = server.get("password", password)

    metrics = api_call(url, password)

    if not isinstance(metrics, dict):
        return 0

    try:
        return int(metrics.get("basecampnum", 0))
    except (TypeError, ValueError):
        return 0
