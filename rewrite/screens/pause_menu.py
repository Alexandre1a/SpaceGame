import pygame

from screens.base_screen import Screen
from ui.button import Button


class PauseMenu(Screen):
    def __init__(self, game, width, height, font):
        """
        Initialise l'écran de pause.

        Args:
            game: Référence vers l'objet Game principal
        """
        self.game = game
        self.width = width
        self.height = height
        self.font = self.game.fonts["default"]

        self.buttons = [
            Button(
                "Resume", (self.width // 2, self.height // 2 - 50), self.resume, font
            ),
            Button(
                "Save & Quit",
                (self.width // 2, self.height // 2),
                self.saveAndQuit,
                font,
            ),
            Button(
                "Main Menu",
                (self.width // 2, self.height // 2 + 50),
                game.displayMenu,
                font,
            ),
            Button(
                "Quit to Desktop",
                (self.width // 2, self.height // 2 + 100),
                game.quit,
                font,
            ),
        ]

    def resume(self):
        self.game.current_screen = self.game.gameScreen

    def saveAndQuit(self):
        self.game.saveGame()
        self.game.displayMenu()

    def handleEvent(self, event):
        for btn in self.buttons:
            btn.handleEvent(event)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.text = self.font.render("Pause", True, (255, 255, 255))
        surface.blit(self.text, (surface.get_width() // 2 - 40, 100))
        for btn in self.buttons:
            btn.render(surface)
