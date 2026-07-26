# services/servers.py

import json
import os
import threading

from core.storage import get_server_data_path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SERVER_CONFIG_FILE = os.path.join(DATA_DIR, "servers.json")

servers_lock = threading.RLock()

SERVER_DEFAULTS = {
    "poll_interval_seconds": 30,
    "data_refresh_seconds": 60,
    "max_pal_base_distance": None,

    # SSH Tunnel
    "use_ssh": False,
    "ssh_host": "",
    "ssh_port": 22,
    "ssh_user": "",
    "ssh_key": "",
    "remote_host": "127.0.0.1",
    "remote_port": 8212,
}


def apply_server_defaults(server):
    server = dict(server)

    for key, value in SERVER_DEFAULTS.items():
        server.setdefault(key, value)

    return server


def load_servers():
    if not os.path.exists(SERVER_CONFIG_FILE):
        return {}

    try:
        with open(
            SERVER_CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            loaded_servers = json.load(file)

        for server_id, server in loaded_servers.items():
            loaded_servers[server_id] = apply_server_defaults(server)

        return loaded_servers

    except Exception as error:
        print(f"[ERROR] Loading servers failed: {error}")
        return {}


servers = load_servers()


def save_servers():
    with servers_lock:
        with open(
            SERVER_CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                servers,
                file,
                indent=2
            )


def get_server(server_id):
    with servers_lock:
        return servers.get(server_id)


def get_servers():
    with servers_lock:
        return servers.copy()


def get_server_list():
    with servers_lock:
        return list(servers.values())


def set_server(server):
    server = apply_server_defaults(server)

    server_id = server["id"]

    with servers_lock:
        if server_id in servers:
            servers[server_id].clear()
            servers[server_id].update(server)
        else:
            servers[server_id] = server

        save_servers()

    return servers[server_id]


def delete_server(server_id):
    with servers_lock:
        if server_id not in servers:
            return False

        del servers[server_id]
        save_servers()

    return True


def save_server_log(server_id, filename, entry):
    server = get_server(server_id)

    if not server:
        return False

    folder = get_server_data_path(server)

    filepath = os.path.join(folder, filename)

    logs = []

    if os.path.exists(filepath):
        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:
            logs = json.load(file)

    logs.append(entry)

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            logs,
            file,
            indent=2
        )

    return True