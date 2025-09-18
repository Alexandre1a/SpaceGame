import pygame
from screens.base_screen import Screen
from ui.button import Button

class TitleScreen(Screen):
    def __init__(self, game):
        self.game = game
        # On prend la surface de rendu depuis game.screen
        wf, hf = game.screen.get_width(), game.screen.get_height()
        font = game.fonts['default']
        # Création des trois boutons centrés
        self.buttons = [
            Button("Play",  (wf//2, hf//2 - 50), game.start_game,       font),
            Button("Ships", (wf//2, hf//2),      game.open_ship_selection, font),
            Button("Exit",  (wf//2, hf//2 + 50), game.quit,             font),
        ]

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self, dt):
        pass

    def render(self, surface):
        # On utilise la surface passée ici pour le rendu
        surface.fill((0, 0, 30))
        for btn in self.buttons:
            btn.render(surface)