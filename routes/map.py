# routes/map.py

import json

from flask import Blueprint, render_template, send_from_directory

from core.config import(MAP_DIR,config,)

map_bp = Blueprint("map", __name__)

 
@map_bp.route("/")
def index():
    map_bounds = [
        [config["map"]["min_y"],config["map"]["min_x"]],
        [config["map"]["max_y"],config["map"]["max_x"]]
    ]
 
    return render_template(
        "index.html",
        tile_url=config["map"]["tile_url"],
        map_bounds=json.dumps(map_bounds)
    )

 
@map_bp.route("/map/<path:path>")
def serve_map(path):
    return send_from_directory(MAP_DIR,path)
