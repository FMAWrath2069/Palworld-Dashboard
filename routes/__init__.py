# routes/__init__.py

from .status import status_bp
from .data import data_bp
from .servers import servers_bp
from .game import game_bp
from .map import map_bp
from .server_status import server_status_bp

__all__ = [
    "status_bp",
    "data_bp",
    "servers_bp",
    "game_bp",
    "map_bp",
    "server_status_bp",
]