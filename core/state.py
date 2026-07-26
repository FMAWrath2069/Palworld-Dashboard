import threading


class ServerState:

    def __init__(self, server_id):

        self.server_id = server_id

        self.lock = threading.RLock()

        self.data = {
            "basecampnum": 0,
            "bases": [],
            "players": [],
            "stats": {
                "base_pals": 0,
                "players": 0,
                "wild_npcs": 0,
                "bases": 0,
                "guilds": 0
            },
            "last_updated": None,
            "last_updated_unix": None
        }


server_states = {}


def get_server_state(server_id):

    if server_id not in server_states:

        server_states[server_id] = ServerState(
            server_id
        )

    return server_states[server_id]