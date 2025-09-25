import pygame
from screens.base_screen import Screen
from entities.planet import Planet

class GameScreen(Screen):
    def __init__(self, game):
        self.game = game
        self.ship = None
        self.zoom = 1.0
        # sample planets or use game.planets
        self.planets = [
            Planet((400, -200), 150, (30,100,200)),
            Planet((-800, 500), 300, (200,150,50)),
        ]

    def load_ship(self, ship, reset=True):
        self.ship = ship
        if reset:  # Par défaut on remet à zéro
            self.ship.pos = pygame.Vector2(0, 0)

    def handle_event(self, event): pass

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.ship.update(dt, keys)
        # zoom controls
        if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            self.zoom = min(5.0, self.zoom + 1.5 * dt)
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self.zoom = max(0.001, self.zoom - 1.5 * dt)

    def render(self, surface):
        surface.fill((10,10,30))
        # camera centered
        half = pygame.Vector2(surface.get_size()) / 2
        cam = self.ship.pos - half / self.zoom
        # draw planets
        for planet in self.planets:
            planet.render(surface, cam, self.zoom)
        # draw ship
        self.ship.render(surface, cam, self.zoom)
        # debug info
        font = self.game.fonts['default']
        fps = font.render(f"FPS: {self.game.clock.get_fps():.1f}", True, (200,200,50))
        speed = font.render(f"Speed: {self.ship.vel.length():.1f}", True, (0,255,255))
        zoom = font.render(f"Zoom: {self.zoom:.2f}×", True, (200,200,200))
        shipInfo = font.render(f"Ship: {self.ship.name}", True, (200,100,30))
        surface.blit(fps,  (10,10))
        surface.blit(speed,(10,30))
        surface.blit(zoom, (10,50))
        surface.blit(shipInfo, (10, 70))
