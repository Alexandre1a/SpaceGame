import pygame
from resources import load_fonts, load_images
from entities.ship import Ship
from screens.title_screen import TitleScreen
from screens.ship_selection import ShipSelectionScreen
from screens.game_screen import GameScreen
from screens.settings_screen import SettingsScreen
from screens.pause_menu import PauseMenu
from utils.settings_manager import load_settings, save_settings
from utils.save_manager import save_game, load_game


class Game:
    def __init__(self):
        pygame.init()
        self.settings = load_settings()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("My Space Game")
        self.clock = pygame.time.Clock()

        # Load assets
        self.images = load_images()
        self.fonts = load_fonts()

        # Define ships
        self.available_ships = [
            Ship("Gladius", self.images['gladius'], accel=400, max_speed=225, drag=0, turn_speed=52),
            Ship("Aurora", self.images['aurora'], accel=400, max_speed=200, drag=0, turn_speed=500),
            Ship("400i", self.images['400i'], accel=250, max_speed=1225, drag=0, turn_speed=70),
            Ship("Interceptor", self.images['gladius'], accel=1250, max_speed=1500, drag=0, turn_speed=300),
        ]
        self.selected_ship = None

        # Screens
        self.title_screen = TitleScreen(self)
        self.ship_select  = ShipSelectionScreen(self)
        self.game_screen  = GameScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.pause_screen = PauseMenu(self)
        self.current_screen = self.title_screen

    def start_game(self):
        if not self.selected_ship:
            self.selected_ship = self.available_ships[0]

        # au lieu d'utiliser directement self.selected_ship, on recrée une instance
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
        self.game_screen.load_ship(fresh_ship, reset=True)  # reset=True = pos (0,0)
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

    def quit(self):
        pygame.quit()
        exit()

    def run(self):
        while True:
            dt = self.clock.tick(500) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p and self.current_screen == self.game_screen:
                        # Toggle pause
                        self.current_screen = self.pause_screen

                self.current_screen.handle_event(event)

            self.current_screen.update(dt)
            self.current_screen.render(self.screen)
            pygame.display.flip()

if __name__ == '__main__':
    Game().run()
