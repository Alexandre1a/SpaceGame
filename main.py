#===========
#= Imports =
#===========
# Python
import sys
import pygame

# Custom modules
from ressources.ressources import loadFonts, loadImages
from gameplay.quest_manager import QuestManager
from entities.ship import KeyboardController, Ship
# Screens
from screens.game_screen import GameScreen
from screens.pause_menu import PauseMenu
from screens.settings_screen import SettingsScreen
from screens.ship_selection import ShipSelectionScreen
from screens.title_screen import TitleScreen
from screens.start_screen import StartOptions

# Utils
from utils.save_manager import loadSave, saveGame
from utils.settings_manager import loadSettings, saveSettings
from utils.phtonos import Phtonos


class Game:
    def __init__(self):
        """
        This is the "spine" of the game, it centralise all values required for other compoments
        """
        print("SpaceGame Copyright (C) 2026 Alexandre Delcamp--Enache, Pablo Perez\nThis program comes with ABSOLUTLY NO WARRANTY !\nThis is a free software, and you are welcome to redistribute it under certain condtions.\nSee the GNU/GPL License for more details")

        # Init Pygame
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.clock = pygame.time.Clock()

        # Load Settings
        self.settings = loadSettings()

        # Init the screen and sets some parameters
        self.screen = pygame.display.set_mode(self.settings["resolution"])

        # Sets the window title
        pygame.display.set_caption("SpaceGame")

        # Load assets
        self.images = loadImages()
        self.fonts = loadFonts()

        # Create available ships
        self.availableShips = [
            Ship(
                "TestShip",
                "Admin",
                "S",
                self.images["gladius"],
                accel=1250,
                maxSpeed=5000,
                drag=0,
                turnSpeed=300,
            ),
            Ship(
              "Origin",
              "Luxury",
              "A",
              self.images["origin"],
              accel=1115,
              maxSpeed=3000,
              drag=0,
              turnSpeed=150,
            ),
            Ship(
                "600i",
                "Luxury",
                "B",
                self.images["600i"],
                accel=1250,
                maxSpeed=2000,
                drag=0,
                turnSpeed=120,
            ),
        ]
        # Selects a placeholder ship if none is selected
        self.selectedShip = self.availableShips[1]

        # Create the controller for the player to use
        self.controller = KeyboardController()
        # Loads the save
        self.save = loadSave(self)
        # Load the saved money (uses save data)
        self.amount = 0
        if self.save != None:
          self.amount = self.save["money"]
        else:
          self.initPhtonos()
          self.phtonos.add(self, 100)


    @property
    def currentScreen(self):
        return self._currentScreen

    @currentScreen.setter
    def currentScreen(self, screen):
        self._currentScreen = screen
        screen.onEnter()

    #====================
    #= Screen switchers =
    #====================
    def displayStartOptions(self):
        self.currentScreen = self.startOptions

    def displayShipSelection(self):
        self.currentScreen = self.shipSelect

    def displaySettingsScreen(self):
        self.currentScreen = self.settingsScreen

    def displayMenu(self):
        self.currentScreen = self.titleScreen

    def saveGame(self):
        saveGame(self)

    def initScreens(self):
      """
      This function is made to (re)generate the correct screens,
      we pass the height, the width and the fonts to use
      """
      self.titleScreen = TitleScreen(
          self,
          self.getWidth(),
          self.getHeight(),
          self.getFonts()["default"],
          self.getFonts()["title"],
      )
      self.shipSelect = ShipSelectionScreen(
          self,
          self.getWidth(),
          self.getHeight(),
          self.getFonts()["default"],
          self.getFonts()["title"],
      )
      self.gameScreen = GameScreen(
          self,
          self.getWidth(),
          self.getHeight(),
          self.getFonts()["default"],
          self.controller,
      )
      self.settingsScreen = SettingsScreen(
          self,
          self.getWidth(),
          self.getHeight(),
          self.getFonts()["default"],
          self.getFonts()["title"],
          self.settings,
      )
      self.pauseScreen = PauseMenu(
          self,
          self.getWidth(),
          self.getHeight(),
          self.getFonts()["default"],
      )
      self.startOptions = StartOptions(
          self,
          self.getWidth(),
          self.getHeight(),
          self.getFonts()["default"],
      )

    def initPhtonos(self):
      self.phtonos = Phtonos()

    def initQuestManager(self):
      self.questManager = QuestManager(self)

    def getSaveData(self):
        self.save = loadSave(self)
        return self.save

    def quit(self):
        sys.exit()

    # ==================== GETTERS ====================
    def getWidth(self):
        return self.screen.get_width()

    def getHeight(self):
        return self.screen.get_height()

    def getFonts(self):
        return self.fonts

    def getAvailableShips(self):
        return self.availableShips

    def getMoney(self):
        return self.amount

    def getSelectedShip(self):
        return self.selectedShip

    def getSettings(self):
        return self.settings

    # ==================== SETTER ====================

    def setSelectedShip(self, ship):
        if ship in self.availableShips:
            self.selectedShip = ship
        else:
            return "Please set a correct ship"

    def run(self):
        self.initScreens()
        self.currentScreen = self.titleScreen
        while True:
            dt = self.clock.tick(self.settings["fps"]) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_p
                        and self.currentScreen == self.gameScreen
                    ):
                        # Toggle pause
                        self.currentScreen = self.pauseScreen
                self.currentScreen.handleEvent(event)

            self.currentScreen.update(dt)
            self.currentScreen.render(self.screen)
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
