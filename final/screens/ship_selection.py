import pygame
from screens.base_screen import Screen
from ui.button import Button

class ShipSelectionScreen(Screen):
    def __init__(self, game):
        self.game = game
        wf, hf = game.screen.get_size()
        font = game.fonts['default']
        self.buttons = []
        for i, ship in enumerate(game.available_ships):
            # On passe la font à Button
            btn = Button(
                ship.name,
                (wf//2, 150 + i*60),
                lambda s=ship: self.select(s),
                font
            )
            self.buttons.append(btn)

    def select(self, ship):
        self.game.selected_ship = ship
        # Retour à l'écran titre après sélection
        self.game.current_screen = self.game.title_screen

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((20, 20, 40))
        for btn in self.buttons:
            btn.render(surface)