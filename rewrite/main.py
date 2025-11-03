# Importe les dépendances requises
import pygame

# Importe les sous-modules personalisés
from ressources import loadFonts, loadImages
from entities.ship import Ship, KeyboardController
# Screens
from screens.title_screen import TitleScreen
from screens.ship_selection import ShipSelectionScreen
from screens.game_screen import GameScreen
from screens.settings_screen import SettingsScreen
from screens.pause_menu import PauseMenu
# Utilitaires
from utils.settings_manager import loadSettings, saveSettings
from utils.save_manager import loadSave



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
        #self.save = loadSave()
        #self.money = self.save["money"]

        # Charge les assets
        self.images = loadImages()
        self.fonts = loadFonts()

        # Charge les vaisseaux disponibles
        self.availableShips = [
            Ship(
                "TestShip",
                self.images["gladius"],
                accel=1250,
                maxSpeed=5000,
                drag=0,
                turnSpeed=300,
            ),
        ]
        # Prends un placeholder quand aucun vaisseau n'est choisi
        self.selectedShip = self.availableShips[0]

        # Initialise et crée les paramètres de l'écran
        self.screen = pygame.display.set_mode(self.settings["resolution"])

        # Défini le titre de la fenêtre
        pygame.display.set_caption("SpaceGame")
        # self.clock = pygame.time.Clock()

        # Crée le controller (Après le chargement de menu)
        controller = KeyboardController()

        self.current_screen = TitleScreen(self)


    def run(self):
        while True:
            dt = self.clock.tick(self.settings["fps"]) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_p
                        and self.current_screen == self.game_screen
                    ):
                        # Toggle pause
                        self.current_screen = self.pause_screen
            
            self.current_screen.handle_event(event)

        self.current_screen.update(dt)
        self.current_screen.render(self.screen)
        pygame.display.filp()




if __name__ == "__main__":
    Game().run()