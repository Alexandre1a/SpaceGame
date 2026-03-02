import gzip
import json
import os

import pygame

SAVE_FILE = "savegame.json.gz"


# utilitaires pour planets
def serialize_planet(p):
    return p.to_dict()


def deserialize_planet(d):
    return __import__("entities.planet", fromlist=["Planet"]).Planet.from_dict(d)


def saveGame(game):
    data = {
        "ship": game.selectedShip.name,
        "pos": [game.selectedShip.pos.x, game.selectedShip.pos.y],
        "vel": [game.selectedShip.vel.x, game.selectedShip.vel.y],
        "angle": game.selectedShip.angle,
        "zoom" : game.gameScreen.zoom,
        # Plannets
        "planets": [serialize_planet(p) for p in game.gameScreen.planets],
    }
    with gzip.open(SAVE_FILE, "wb") as f:
        f.write(json.dumps(data).encode("utf-8"))
    print("[SaveManager] Game saved (gzipped).")
    print("[SaveManager] Saved data:", data)


def loadSave(game):
    if not os.path.exists(SAVE_FILE):
        print("[SaveManager] Can't find savefile")
        return None
    with gzip.open(SAVE_FILE, "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    print("[SaveManager] Save file loaded successfully")
    # Ship
    data["ship"] = game.selectedShip = next(
        (ship for ship in game.availableShips if ship.name == data["ship"]), None
    )

    data["planets"] = [deserialize_planet(p) for p in data["planets"]]

    print("[SaveManger] Loaded data: ", data)
    return data