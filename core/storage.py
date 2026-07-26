# core/storage.py
import json
import os
import shutil

from core.config import SERVER_DATA_DIR
from core.state import get_server_state


def get_server_data_path(server):

    server_id = server.get("id") or "default"

    path = os.path.join(SERVER_DATA_DIR, server_id)
    os.makedirs(path, exist_ok=True)

    return path


def delete_server_data(server):

    folder = get_server_data_path(server)

    if os.path.isdir(folder):
        shutil.rmtree(folder, ignore_errors=True)


def load_json_file(path, default):

    if not os.path.exists(path):
        return default

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as error:

        print(f"Failed loading {path}: {error}")

        return default


def save_json_file(path, data):

    temp_file = f"{path}.tmp"

    try:

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

        os.replace(temp_file, path)

    except Exception as error:

        print(f"Failed saving {path}: {error}")


def load_data(server):

    server_id = server.get("id", "default")

    state = get_server_state(server_id)

    folder = get_server_data_path(server)

    bases = load_json_file(os.path.join(folder, "bases.json"), [])
    players = load_json_file(os.path.join(folder, "players.json"), [])
    pals = load_json_file(os.path.join(folder, "pals.json"), [])
    stats = load_json_file(os.path.join(folder, "stats.json"), {})
    metadata = load_json_file(os.path.join(folder, "metadata.json"), {})

    with state.lock:

        state.data["bases"] = bases
        state.data["players"] = players
        state.data["pals"] = pals
        state.data["stats"] = stats
        state.data.update(metadata)


def save_data(server):

    server_id = server.get("id", "default")

    state = get_server_state(server_id)

    folder = get_server_data_path(server)

    with state.lock:

        bases = state.data.get("bases", [])
        players = state.data.get("players", [])
        pals = state.data.get("pals", [])
        stats = state.data.get("stats", {})
        metadata = {
            "basecampnum": state.data.get("basecampnum", 0),
            "last_updated": state.data.get("last_updated"),
            "last_updated_unix": state.data.get("last_updated_unix")
        }

    save_json_file(os.path.join(folder, "bases.json"), bases)
    save_json_file(os.path.join(folder, "players.json"), players)
    save_json_file(os.path.join(folder, "pals.json"), pals)
    save_json_file(os.path.join(folder, "stats.json"), stats)
    save_json_file(os.path.join(folder, "metadata.json"), metadata)


def read_server_file(server, filename, default):

    folder = get_server_data_path(server)

    filepath = os.path.join(folder, filename)

    return load_json_file(filepath, default)