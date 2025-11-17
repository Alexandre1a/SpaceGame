import json
import os

import pygame

SAVE_FILE = "savegame.json"


def saveGame(game):
    data = {
        "ship": game.selectedShip.name,
        "pos": [game.selectedShip.pos.x, game.selectedShip.pos.y],
        "vel": [game.selectedShip.vel.x, game.selectedShip.vel.y],
        "angle": game.selectedShip.angle,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def loadGame(game):
    if not os.path.exists(SAVE_FILE):
        print("[SaveManager] Can't file savefile")
        return False
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)
        print("[SaveManager] Save file loaded successfully")

    # Retrouver le modèle du vaisseau par nom
    game.selectedShip = next(
        (ship for ship in game.availableShips if ship.name == data["ship"]), None
    )
    if game.selectedShip is not None:
        print("Loaded ship", game.selectedShip)
        # Appliquer l'état sauvegardé
        game.gameScreen.loadShip(
            game.selectedShip,
            pygame.Vector2(data["pos"]),
            pygame.Vector2(data["vel"]),
            data["angle"],
        )
    return True
