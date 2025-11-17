import gzip
import json
import os

import pygame

SAVE_FILE = "savegame.json.gz"


# utilitaires pour planets
def serializePlanet(p):
    return p.to_dict()


def deserializePlanet(d):
    return __import__("entities.planet", fromlist=["Planet"]).Planet.from_dict(d)


def saveGame(game):
    data = {
        "ship": game.selectedShip.name,
        "pos": [game.selectedShip.pos.x, game.selectedShip.pos.y],
        "vel": [game.selectedShip.vel.x, game.selectedShip.vel.y],
        "angle": game.selectedShip.angle,
        # galaxy state
        "galaxy_seed": getattr(game, "galaxy_seed", None),
        "chunks": game.gameScreen.serializeLoadedChunks(),  # dict chunk_key -> [planets...]
        "player_zoom": game.gameScreen.zoom,
    }
    with gzip.open(SAVE_FILE, "wb") as f:
        f.write(json.dumps(data).encode("utf-8"))
    print("[SaveManager] Game saved (gzipped).")


def loadGame(game):
    if not os.path.exists(SAVE_FILE):
        print("[SaveManager] Can't find savefile")
        return False
    with gzip.open(SAVE_FILE, "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    print("[SaveManager] Save file loaded successfully")

    # restore galaxy seed if present
    if data.get("galaxy_seed") is not None:
        game.galaxy_seed = data["galaxy_seed"]

    # Ship
    game.selectedShip = next(
        (ship for ship in game.availableShips if ship.name == data["ship"]), None
    )
    if game.selectedShip:
        game.gameScreen.loadShip(
            game.selectedShip,
            pygame.Vector2(data["pos"]),
            pygame.Vector2(data["vel"]),
            data["angle"],
        )

    # Restore chunks/planets
    chunks = data.get("chunks", {})
    game.gameScreen.deserializeLoadedChunks(chunks)

    # restore zoom
    game.gameScreen.zoom = data.get("player_zoom", game.gameScreen.zoom)

    return True
