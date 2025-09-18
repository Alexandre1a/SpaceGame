import pygame
from resources import load_fonts, load_images
from entities.ship import Ship
from screens.title_screen import TitleScreen
from screens.ship_selection import ShipSelectionScreen
from screens.game_screen import GameScreen

class Game:
    def __init__(self):
        pygame.init()
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
        ]
        self.selected_ship = None

        # Screens
        self.title_screen = TitleScreen(self)
        self.ship_select  = ShipSelectionScreen(self)
        self.game_screen  = GameScreen(self)
        self.current_screen = self.title_screen

    def start_game(self):
        if not self.selected_ship:
            self.selected_ship = self.available_ships[0]
        self.game_screen.load_ship(self.selected_ship)
        self.current_screen = self.game_screen

    def open_ship_selection(self):
        self.current_screen = self.ship_select

    def quit(self):
        pygame.quit()
        exit()

    def run(self):
        while True:
            dt = self.clock.tick(500) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                self.current_screen.handle_event(event)
            self.current_screen.update(dt)
            self.current_screen.render(self.screen)
            pygame.display.flip()

if __name__ == '__main__':
    Game().run()
