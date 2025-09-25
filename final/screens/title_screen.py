import pygame
from screens.base_screen import Screen
from ui.button import Button

class TitleScreen(Screen):
    def __init__(self, game):
        self.game = game
        # On prend la surface de rendu depuis game.screen
        wf, hf = game.screen.get_width(), game.screen.get_height()
        # Obtenir les fonts
        font = self.game.fonts['default']

        # Création des trois boutons centrés
        self.buttons = [
            Button("New Game",  (wf//2, hf//2 - 50), game.start_game,       font),
            Button("Load Game", (wf//2, hf//2 - 100), game.load_game_from_file, font),
            Button("Ships", (wf//2, hf//2),      game.open_ship_selection, font),
            Button("Settings", (wf//2, hf//2 + 50), game.open_settings, font),
            Button("Exit",  (wf//2, hf//2 + 100), game.quit,             font),
        ]



    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def update(self, dt):
        pass

    def render(self, surface):
        # On utilise la surface passée ici pour le rendu
        surface.fill((0, 0, 30))
        # Création du texte
        font = self.game.fonts['default']
        # Déterminer le nom du vaisseau sélectionné
        if self.game.selected_ship:
            ship_name = self.game.selected_ship.name
        else:
            ship_name = "Gladius"
        text_surf = font.render(f"Vaisseau choisi : {ship_name}", True, (255, 255, 255))
        # Blit text
        text_pos = (50, 50)
        surface.blit(text_surf, text_pos)
        for btn in self.buttons:
            btn.render(surface)
