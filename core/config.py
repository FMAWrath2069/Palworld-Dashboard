# core/config.py

import os

import yaml


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
SERVER_DATA_DIR = os.path.join(DATA_DIR, "servers")
MAP_DIR = os.path.join(BASE_DIR, "map")
STATIC_DIR = os.path.join(BASE_DIR, "static")

CONFIG_FILE = os.path.join(BASE_DIR, "config.yaml")

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SERVER_DATA_DIR, exist_ok=True)

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file) or {}

api_config = config.setdefault("api", {})
server_config = config.setdefault("server", {})
map_config = config.setdefault("map", {})