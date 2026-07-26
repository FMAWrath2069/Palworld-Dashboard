#constants.py
import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
SERVER_CONFIG_FILE = os.path.join(DATA_DIR, "servers.json")
SERVER_DATA_DIR = os.path.join(DATA_DIR, "servers")
MAP_DIR = os.path.join(BASE_DIR, "map")
STATIC_DIR = os.path.join(BASE_DIR, "static")
CONFIG_FILE = os.path.join(BASE_DIR, "config.yaml")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SERVER_DATA_DIR, exist_ok=True)

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file) or {}

api_config = config.setdefault("api", {})
server_config = config.setdefault("server", {})

API_METRICS = api_config.get("metrics_url", "")
API_GAMEDATA = api_config.get("gamedata_url", "")
PASSWORD = api_config.get("password", "")

POLL_INTERVAL = int(
    api_config.get("poll_interval_seconds", 30)
)

DATA_REFRESH_SECONDS = int(
    api_config.get("data_refresh_seconds", 60)
)

MAX_PAL_BASE_DISTANCE = api_config.get(
    "max_pal_base_distance",
    10000
)

if MAX_PAL_BASE_DISTANCE in ("", None, 0, "0"):
    MAX_PAL_BASE_DISTANCE = None
else:
    MAX_PAL_BASE_DISTANCE = float(MAX_PAL_BASE_DISTANCE)