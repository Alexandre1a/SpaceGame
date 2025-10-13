# Importe les dépendances requises
import pygame

# Importe les sous-modules personalisés
pass


class Game:
    def __init__(self):
        """
        Cette classe est la colone vertébrale du programe, elle aura toutes les valeurs requises par les autres composants
        Tout est en camelCase
        """
        # Initialise pygame
        pygame.init()
        # Charge les paramètres et la sauvegarde
        self.settings = loadSettings()
        self.save = loadSave()
        self.money = self.save["money"]

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
