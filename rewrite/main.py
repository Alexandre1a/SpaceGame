# Importe les dépendances requises
import sys

import pygame

# Importe les sous-modules personalisés
from ressources.ressources import loadFonts, loadImages

# Screens
from entities.ship import KeyboardController, Ship  # , ShipAI, SimpleAIController
from screens.game_screen import GameScreen
from screens.pause_menu import PauseMenu
from screens.settings_screen import SettingsScreen
from screens.ship_selection import ShipSelectionScreen
from screens.title_screen import TitleScreen

# Utilitaire
from utils.save_manager import loadGame, saveGame
from utils.settings_manager import loadSettings, saveSettings


class Game:
    def __init__(self):
        """
        Cette classe est la colone vertébrale du programe, elle aura toutes les valeurs requises par les autres composants
        Tout est en camelCase
        """
        # Initialise pygame
        pygame.init()
        self.clock = pygame.time.Clock()

        # Charge les paramètres et la sauvegarde
        self.settings = loadSettings()
        # self.save = loadSave()
        # self.money = self.save["money"]
        self.money = 100

        # Initialise et crée les paramètres de l'écran
        self.screen = pygame.display.set_mode(self.settings["resolution"])

        # Défini le titre de la fenêtre
        pygame.display.set_caption("SpaceGame")

        # Charge les assets
        self.images = loadImages()
        self.fonts = loadFonts()

        # Charge les vaisseaux disponibles
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
                "600i",
                "Origin",
                "B",
                self.images["600i"],
                accel=1250,
                maxSpeed=2000,
                drag=0,
                turnSpeed=120,
            ),
        ]
        # Prends un placeholder quand aucun vaisseau n'est choisi
        self.selectedShip = self.availableShips[0]

        # Crée le controller (Après le chargement de menu)
        self.controller = KeyboardController()

    # Fonction pour afficher les différents écrans
    def displayStartOptions(self):
        # Todo
        # self.currentScreen = self.StartOptions
        self.gameScreen.loadShip(
            self.selectedShip,
            pos=pygame.Vector2(0, 0),
            vel=pygame.Vector2(0, 0),
            angle=90,
        )
        # self.gameScreen.generatePlanets()
        self.currentScreen = self.gameScreen

    def displayShipSelection(self):
        self.currentScreen = self.shipSelect

    def displaySettingsScreen(self):
        self.currentScreen = self.settingsScreen

    def displayMenu(self):
        self.currentScreen = self.titleScreen

    def saveGame(self):
        saveGame(self)

    def initScreens(self):
        # Screens
        self.titleScreen = TitleScreen(
            self,
            self.screen.get_width(),
            self.screen.get_height(),
            self.fonts["default"],
        )
        self.shipSelect = ShipSelectionScreen(
            self,
            self.screen.get_width(),
            self.screen.get_height(),
            self.fonts["default"],
            self.fonts["title"],
        )
        self.gameScreen = GameScreen(
            self,
            self.screen.get_width(),
            self.screen.get_height(),
            self.fonts["default"],
            self.controller,
        )
        self.settingsScreen = SettingsScreen(
            self,
            self.screen.get_width(),
            self.screen.get_height(),
            self.fonts["default"],
            self.fonts["title"],
            self.settings,
        )
        self.pauseScreen = PauseMenu(
            self,
            self.screen.get_width(),
            self.screen.get_height(),
            self.fonts["default"],
        )

    def loadGame(self):
        loadGame(self)
        self.currentScreen = self.gameScreen

    def quit(self):
        sys.exit()

    # ==================== GETTERS ====================
    """ Inutile puisque on passe directement les valeurs dans la création des écrans
    def getWidth(self):
        return self.screen.get_width()

    def getHeight(self):
        return self.screen.get_height()

    def getFonts(self):
        return self.fonts
    """

    def getAvailableShips(self):
        return self.availableShips

    def getMoney(self):
        return self.money

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


def render_overlay(self, surface, font):
    if not self.show_overlay:
        return

    overlay_rect = pygame.Rect(100, 100, 600, 400)
    pygame.draw.rect(surface, (30, 30, 60), overlay_rect)
    pygame.draw.rect(surface, (200, 200, 255), overlay_rect, 3)

    title = font.render(self.name, True, (255, 255, 255))
    surface.blit(title, (overlay_rect.x + 20, overlay_rect.y + 20))
