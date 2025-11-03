import pygame
from screens.base_screen import Screen
from ui.button import Button

class PauseMenu(Screen):
    def __init__(self, game):
        self.game = game
        wf, hf = game.screen.get_size()
        font = game.fonts['default']

        self.buttons = [
            Button("Resume", (wf//2, hf//2 - 50), self.resume, font),
            Button("Save & Quit", (wf//2, hf//2), self.save_and_quit, font),
            Button("Main Menu", (wf//2, hf//2 + 50), game.go_to_menu, font),
            Button("Quit to Desktop", (wf//2, hf//2 + 100), game.quit, font),
        ]

    def resume(self):
        self.game.current_screen = self.game.game_screen

    def save_and_quit(self):
        self.game.save_game()
        self.game.go_to_menu()

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def render(self, surface):
        surface.fill((0, 0, 0))
        font = self.game.fonts['default']
        text = font.render("Pause", True, (255, 255, 255))
        surface.blit(text, (surface.get_width()//2 - 40, 100))
        for btn in self.buttons:
            btn.render(surface)
