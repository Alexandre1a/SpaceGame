import pygame

# import ctypes
from resources import load_fonts, load_images
from entities.ship import Ship
from screens.title_screen import TitleScreen
from screens.ship_selection import ShipSelectionScreen
from screens.game_screen import GameScreen
from screens.settings_screen import SettingsScreen
from screens.pause_menu import PauseMenu
from utils.settings_manager import load_settings, save_settings
from utils.save_manager import *

# ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Game:
    def __init__(self):
        # Initialise pygame
        pygame.init()
        # Charge les paramètres enregistrés
        self.settings = load_settings()

        # Crée une balance temporaire
        self.money = 0
        # Charge l'argent
        Save.loadMoney(self)
        # Utiliser les settings pour créer l'écran avec la bonne résolution
        # flags = pygame.FULLSCREEN if self.settings["fullscreen"] else 0
        self.screen = pygame.display.set_mode(self.settings["resolution"])
        # Défini le titre de la fenètre
        pygame.display.set_caption("My Space Game")
        self.clock = pygame.time.Clock()

        # Load assets
        self.images = load_images()
        self.fonts = load_fonts()

        # Define ships
        self.available_ships = [
            Ship(
                "TestShip",
                self.images["gladius"],
                accel=1250,
                max_speed=1500,
                drag=0,
                turn_speed=300,
                brand="Aegis",
            ),
        ]
        self.selected_ship = None

        # Screens
        self.title_screen = TitleScreen(self)
        self.ship_select = ShipSelectionScreen(self)
        self.game_screen = GameScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.pause_screen = PauseMenu(self)
        self.current_screen = self.title_screen

    def start_game(self):
        if not self.selected_ship:
            self.selected_ship = self.available_ships[0]

        # Création d'une instance du vaisseau séléctionné
        from entities.ship import Ship

        template = self.selected_ship
        fresh_ship = Ship(
            template.name,
            template.sprite,
            template.acceleration,
            template.max_speed,
            template.drag,
            template.turn_speed,
        )

        self.selected_ship = fresh_ship
        self.game_screen.load_ship(
            fresh_ship, reset=True
        )  # Si le reset est vrai, il remet la position à 0
        self.current_screen = self.game_screen

    def open_ship_selection(self):
        self.current_screen = self.ship_select

    def go_to_menu(self):
        self.current_screen = self.title_screen

    def pause(self):
        self.current_screen = self.pause_screen

    def open_settings(self):
        self.current_screen = self.settings_screen

    def save_game(self):
        if self.selected_ship:
            save_game(self.selected_ship)

    def load_game_from_file(self):
        ok = load_game(self)
        if ok:
            self.current_screen = self.game_screen

    def rebuild_screens(
        self,
    ):  # Permet de recréer les écrans (après changement de résolution par exemple)
        """Recrée tous les écrans pour s'adapter à la nouvelle résolution"""
        # Sauvegarder l'écran actuel
        current = self.current_screen

        # Recréer tous les écrans avec les nouvelles dimensions
        self.title_screen = TitleScreen(self)
        self.ship_select = ShipSelectionScreen(self)
        self.game_screen = GameScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.pause_screen = PauseMenu(self)

        # Restaurer le vaisseau dans game_screen si nécessaire
        if self.selected_ship:
            self.game_screen.load_ship(self.selected_ship, reset=False)

        # Remettre le bon écran actif
        if current == self.title_screen or isinstance(current, TitleScreen):
            self.current_screen = self.title_screen
        elif isinstance(current, ShipSelectionScreen):
            self.current_screen = self.ship_select
        elif isinstance(current, GameScreen):
            self.current_screen = self.game_screen
        elif isinstance(current, SettingsScreen):
            self.current_screen = self.settings_screen
        elif isinstance(current, PauseMenu):
            self.current_screen = self.pause_screen

    def quit(self):
        pygame.quit()
        exit()

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
            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
