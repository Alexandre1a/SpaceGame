import json, os

SAVE_FILE = "savegame.json"

def save_game(ship):
    data = {
        "ship": ship.name,
        "pos": [ship.pos.x, ship.pos.y],
        "vel": [ship.vel.x, ship.vel.y],
        "angle": ship.angle,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game(game):
    if not os.path.exists(SAVE_FILE):
        return False
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    # retrouver le modèle du vaisseau par nom
    template = None
    for ship in game.available_ships:
        if ship.name == data["ship"]:
            template = ship
            break

    if not template:
        return False

    # recréer un vaisseau neuf basé sur le modèle
    from entities.ship import Ship
    ship = Ship(
        template.name,
        template.sprite,
        template.acceleration,
        template.max_speed,
        template.drag,
        template.turn_speed,
    )

    # appliquer l’état sauvegardé
    ship.pos.xy = data["pos"]
    ship.vel.xy = data["vel"]
    ship.angle = data["angle"]

    # charger dans la partie
    game.selected_ship = ship
    game.game_screen.load_ship(ship, reset=False)
    return True
