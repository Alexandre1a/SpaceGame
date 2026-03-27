import pygame

from screens.base_screen import Screen
from ui.button import Button


class StartOptions(Screen):
    def __init__(self, game, width, height, font):
        self.game = game
        self.width = width
        self.height = height
        self.font = font
        self.data = game.getSaveData()

        self.buttons = [
            Button(
              "Nouvelle Partie",
              (self.width // 2, self.height // 2 - 50),
              self.newGame,
              font
            ),
            Button(
                "Charger la partie",
                (self.width // 2, self.height // 2),
                self.loadGame,
                font,
            ),
            Button(
                "Retour",
                (self.width // 2, self.height // 2 + 50),
                self.game.displayMenu,
                font,
            ),
        ]

    def onEnter(self):
        self.data = self.game.getSaveData()
        if self.data is not None:
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
        self.game.gameScreen.generatePlanets(count=1200, spread=80000, minDistance=300)
        self.game.initQuestManager()
        self.game.questManager.generateQuests()
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
        self.game.initQuestManager()
        if "quests" in self.data:
          self.game.questManager.fromDict(self.data["quests"])
        self.game.currentScreen = self.game.gameScreen

    def handleEvent(self, event):
        for btn in self.buttons:
            btn.handleEvent(event)

    def render(self, surface):
        surface.fill((0, 0, 0))
        self.text = self.font.render("Choisissez une option", True, (255, 255, 255))
        surface.blit(self.text, (surface.get_width() // 2 - 100, 100))
        for btn in self.buttons:
            btn.render(surface)
