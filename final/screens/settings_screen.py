import pygame
from screens.base_screen import Screen
from ui.button import Button

class SettingsScreen(Screen):
    def __init__(self,game):
        self.game = game
        wf, hf = game.screen.get_width(), game.screen.get_height()
        font = self.game.fonts['default']

        self.buttons = [
            Button("Exit",  (wf//2, hf//2 + 100), game.go_to_menu,             font),
        ]

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def render(self, surface):
        surface.fill((20, 20, 40))
        for btn in self.buttons:
            btn.render(surface)
