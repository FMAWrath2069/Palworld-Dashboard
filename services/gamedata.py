# gamedata.py

import math
import time
from datetime import datetime

from core.constants import (
    MAX_PAL_BASE_DISTANCE,
    SERVER_DATA_DIR,
)
from core.state import get_server_state
from services.api import (
    api_call,
    game_server_url,
)
from core.storage import save_data
from utils.time import utc_now_iso


def safe_number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def get_actor_location(actor):
    return {
        "x": safe_number(actor.get("LocationX"), 0),
        "y": safe_number(actor.get("LocationY"), 0),
        "z": safe_number(actor.get("LocationZ"), 0),
    }


def calculate_distance(location_a, location_b):
    delta_x = location_a["x"] - location_b["x"]
    delta_y = location_a["y"] - location_b["y"]
    delta_z = location_a["z"] - location_b["z"]

    return math.sqrt(
        delta_x ** 2 +
        delta_y ** 2 +
        delta_z ** 2
    )


def extract_placement_order(name):
    if not isinstance(name, str):
        return None

    name = name.strip()

    if name.endswith("(仮)"):
        name = name[:-3].strip()

    digits = []

    for character in reversed(name):
        if character.isdigit():
            digits.append(character)
        else:
            break

    if not digits:
        return None

    digits.reverse()

    try:
        return int("".join(digits))
    except ValueError:
        return None


def get_actor_id(actor, fallback):
    instance_id = actor.get("InstanceID")

    if instance_id not in (None, ""):
        return str(instance_id)

    return str(fallback)


def convert_coords(loc_x, loc_y):
    map_x = (loc_y - 158000) / 459
    map_y = (loc_x + 123888) / 459

    return map_x, map_y


def is_base_pal(actor):
    return (
        actor.get("Type") == "Character"
        and actor.get("UnitType") == "BaseCampPal"
    )


def is_player(actor):
    return (
        isinstance(actor, dict)
        and actor.get("Type") == "Character"
        and actor.get("UnitType") == "Player"
        and isinstance(actor.get("NickName"), str)
        and actor.get("NickName").strip() != ""
        and isinstance(actor.get("userid"), str)
        and actor.get("userid").strip() != ""
    )


def is_wild_npc(actor):
    if is_base_pal(actor):
        return False

    if is_player(actor):
        return False

    actor_type = str(actor.get("Type", "")).lower()
    unit_type = str(actor.get("UnitType", "")).lower()

    wild_values = {
        "npc",
        "wildnpc",
        "wild_npc",
        "wild",
    }

    return (
        actor_type in wild_values
        or unit_type in wild_values
    )


def convert_player(actor, index):
    return {
        "id": get_actor_id(actor, f"player-{index}"),
        "Type": "Character",
        "UnitType": "Player",
        "NickName": actor.get("NickName", ""),
        "userid": actor.get("userid", ""),
        "nickname": actor.get("NickName", ""),
        "ip": actor.get("ip", ""),
        "level": actor.get("level", 0),
        "HP": actor.get("HP", 0),
        "MaxHP": actor.get("MaxHP", 0),
        "GuildID": actor.get("GuildID", ""),
        "GuildName": actor.get("GuildName", ""),
        "Class": actor.get("Class", ""),
        "LocationX": actor.get("LocationX", 0),
        "LocationY": actor.get("LocationY", 0),
        "LocationZ": actor.get("LocationZ", 0),
        "IsActive": actor.get("IsActive", ""),
    }


def convert_pal(actor, index):
    location = get_actor_location(actor)

    return {
        "id": get_actor_id(actor, f"pal-{index}"),
        "nickname": actor.get("NickName", ""),
        "level": actor.get(
            "Level",
            actor.get("level", 0),
        ),
        "hp": actor.get("HP", 0),
        "max_hp": actor.get("MaxHP", 0),
        "class": actor.get("Class", ""),
        "ai_action": actor.get("AI_Action", ""),
        "guild_id": actor.get("GuildID", ""),
        "guild_name": actor.get("GuildName", ""),
        "location": location,
        "base_id": None,
        "base_distance": None,
    }


def convert_base(palbox, index):
    guild_id = str(palbox.get("GuildID", ""))

    name = palbox.get(
        "Name",
        "Unnamed Base",
    )

    placement_order = extract_placement_order(name)
    world_location = get_actor_location(palbox)

    map_x, map_y = convert_coords(
        world_location["x"],
        world_location["y"],
    )

    id_suffix = (
        placement_order
        if placement_order is not None
        else index
    )

    base_id = f"{guild_id}:{id_suffix}"

    return {
        "id": base_id,
        "name": name,
        "guild_name": palbox.get(
            "GuildName",
            "Unknown",
        ),
        "guild_id": guild_id,
        "class": palbox.get(
            "Class",
            "",
        ),
        "placement_order": placement_order,
        "base_number": None,
        "total_bases": None,
        "display_number": None,
        "map_x": round(map_x, 2),
        "map_y": round(map_y, 2),
        "x": round(map_x, 2),
        "y": round(map_y, 2),
        "world_location": world_location,
        "pals": [],
        "pal_count": 0,
    }


def assign_pals_to_bases(pals, bases):
    bases_by_guild = {}

    for base in bases:
        guild_id = base.get("guild_id", "")

        bases_by_guild.setdefault(
            guild_id,
            [],
        ).append(base)

    for pal in pals:
        guild_id = pal.get("guild_id", "")

        guild_bases = bases_by_guild.get(
            guild_id,
            [],
        )

        if not guild_bases:
            pal["base_id"] = None
            pal["base_distance"] = None
            continue

        if len(guild_bases) == 1:
            pal["base_id"] = guild_bases[0]["id"]
            pal["base_distance"] = None
            continue

        pal_location = pal.get(
            "location",
            {},
        )

        if not all(
            key in pal_location
            for key in ("x", "y", "z")
        ):
            pal["base_id"] = None
            pal["base_distance"] = None
            continue

        closest_base = None
        closest_distance = None

        for base in guild_bases:
            base_location = base.get(
                "world_location",
                {},
            )

            if not all(
                key in base_location
                for key in ("x", "y", "z")
            ):
                continue

            distance = calculate_distance(
                pal_location,
                base_location,
            )

            if (
                closest_distance is None
                or distance < closest_distance
            ):
                closest_base = base
                closest_distance = distance

        if closest_base is None:
            pal["base_id"] = None
            pal["base_distance"] = None
            continue

        if (
            MAX_PAL_BASE_DISTANCE is not None
            and closest_distance > MAX_PAL_BASE_DISTANCE
        ):
            pal["base_id"] = None
            pal["base_distance"] = round(
                closest_distance,
                2,
            )
            continue

        pal["base_id"] = closest_base["id"]
        pal["base_distance"] = round(
            closest_distance,
            2,
        )


def fetch_full_data(server):
    print(f"[{datetime.now()}] Fetching gamedata...")

    url = game_server_url(
        "v1/api/game-data",
        server,
    )

    password = server.get("password", "")

    gamedata = api_call(url,password)

    if not isinstance(gamedata, dict):
        print("[ERROR] Gamedata response is not an object.")
        return False

    actors = gamedata.get(
        "ActorData",
        [],
    )

    if not isinstance(actors, list):
        print("[ERROR] ActorData is not a list.")
        return False

    raw_palboxes = [
        actor
        for actor in actors
        if isinstance(actor, dict)
        and actor.get("Type") == "PalBox"
    ]

    raw_base_pals = [
        actor
        for actor in actors
        if isinstance(actor, dict)
        and is_base_pal(actor)
    ]

    raw_players = [
        actor
        for actor in actors
        if isinstance(actor, dict)
        and is_player(actor)
    ]

    raw_wild_npcs = [
        actor
        for actor in actors
        if isinstance(actor, dict)
        and is_wild_npc(actor)
    ]

    players_by_userid = {}

    for index, actor in enumerate(
        raw_players,
        start=1,
    ):
        player = convert_player(
            actor,
            index,
        )

        userid = player["userid"]

        if userid not in players_by_userid:
            players_by_userid[userid] = player

    players = list(players_by_userid.values())

    bases = [
        convert_base(
            palbox,
            index,
        )
        for index, palbox in enumerate(
            raw_palboxes,
            start=1,
        )
    ]

    bases.sort(
        key=lambda base: (
            base["guild_id"],
            (
                base["placement_order"]
                if base["placement_order"] is not None
                else float("inf")
            ),
            base["name"],
        )
    )

    bases_by_guild = {}

    for base in bases:
        bases_by_guild.setdefault(
            base["guild_id"],
            [],
        ).append(base)

    for guild_bases in bases_by_guild.values():
        total_guild_bases = len(guild_bases)

        for display_index, base in enumerate(
            guild_bases,
            start=1,
        ):
            base["base_number"] = display_index
            base["total_bases"] = total_guild_bases
            base["display_number"] = (
                f"{display_index}/{total_guild_bases}"
            )

    pals = [
        convert_pal(
            actor,
            index,
        )
        for index, actor in enumerate(
            raw_base_pals,
            start=1,
        )
    ]

    assign_pals_to_bases(
        pals,
        bases,
    )

    pals_by_base_id = {}

    for pal in pals:
        base_id = pal.get("base_id")

        if base_id:
            pals_by_base_id.setdefault(
                base_id,
                [],
            ).append(pal)

    for base in bases:
        base_pals = pals_by_base_id.get(
            base["id"],
            [],
        )

        base["pals"] = base_pals
        base["pal_count"] = len(base_pals)

    updated_at = utc_now_iso()
    updated_unix = time.time()

    stats = {
        "base_pals": sum(
            1
            for pal in pals
            if pal.get("base_id") is not None
        ),
        "players": len(players),
        "wild_npcs": len(raw_wild_npcs),
        "bases": len(bases),
        "guilds": len({
            base.get("guild_id")
            for base in bases
            if base.get("guild_id")
        }),
    }

    server_id = server.get(
        "id",
        "default",
    )

    state = get_server_state(
        server_id,
    )

    with state.lock:
        state.data["bases"] = bases
        state.data["players"] = players
        state.data["pals"] = pals
        state.data["basecampnum"] = len(bases)
        state.data["stats"] = stats
        state.data["last_updated"] = updated_at
        state.data["last_updated_unix"] = updated_unix

        save_data(server)

        print(
            f"Updated {stats['bases']} bases with "
            f"{stats['base_pals']} assigned base Pals, "
            f"{stats['players']} players, and "
            f"{stats['wild_npcs']} wild NPCs."
        )

        return True