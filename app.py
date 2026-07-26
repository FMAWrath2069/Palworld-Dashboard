# app.py

from flask import Flask

from core.storage import load_data
from core.config import (
    TEMPLATE_DIR,
    STATIC_DIR,
    server_config,
)

from routes import (
    status_bp,
    data_bp,
    servers_bp,
    game_bp,
    map_bp,
    server_status_bp,
)

from services.polling import ensure_poller
from services.servers import servers


app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static",
)


for blueprint in (
    status_bp,
    data_bp,
    servers_bp,
    game_bp,
    map_bp,
    server_status_bp,
):
    app.register_blueprint(blueprint)


def main():

    if not servers:
        print("No servers configured")
    else:
        for server_id, server in servers.items():
            load_data(server)
            ensure_poller(server_id)

    app.run(
        host=server_config["host"],
        port=server_config["port"],
        debug=False,
    )


if __name__ == "__main__":
    main()