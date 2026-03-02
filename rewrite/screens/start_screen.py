import pygame

from screens.base_screen import Screen
from ui.button import Button


class StartOptions(Screen):
    def __init__(self, game, width, height, font):
        """
        Initialise l'écran de séléction de mode

        Args:
            game: Référence vers l'objet Game principal
        """

        self.game = game
        self.width = width
        self.height = height
        self.font = self.game.fonts["default"]
        self.data = game.getSaveData()

        self.buttons = [
            Button(
                "New Game", (self.width // 2, self.height // 2 - 50), self.newGame, font
            ),
            Button(
                "Load Game",
                (self.width // 2, self.height // 2),
                self.loadGame,
                font,
            ),
            Button(
                "Back",
                (self.width // 2, self.height // 2 + 50),
                self.game.displayMenu,
                font,
            ),
        ]

    def onEnter(self):
        self.data = self.game.getSaveData()
        if self.data != None:
            saveExists = True
        else:
            saveExists = False

        self.buttons[1].setDisabled(not saveExists)

    def newGame(self):
        self.game.gameScreen.loadShip(
            self.game.selectedShip,
            pos=pygame.Vector2(0, 0),
            vel=pygame.Vector2(0, 0),
            angle=90,
        )
        self.game.gameScreen.generateSystems()
        self.game.gameScreen.generatePlanets()
        self.game.currentScreen = self.game.gameScreen

    def loadGame(self):
        self.data = self.game.getSaveData()
        self.game.gameScreen.loadShip(
            self.data["ship"],
            self.data["pos"],
            self.data["vel"],
            self.data["angle"],
        )

        self.game.gameScreen.loadPlanets(self.data["planets"])
        self.game.currentScreen = self.game.gameScreen

    def handleEvent(self, event):
        for btn in self.buttons:
            btn.handleEvent(event)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.text = self.font.render("Chose an option", True, (255, 255, 255))
        surface.blit(self.text, (surface.get_width() // 2 - 100, 100))
        for btn in self.buttons:
            btn.render(surface)
