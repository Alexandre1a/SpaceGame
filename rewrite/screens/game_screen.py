import json
import math
import random
from collections import OrderedDict
from random import randint

import pygame

from entities.planet import Planet
from entities.ship import AdvancedAIController, Ship
from screens.base_screen import Screen

class GameScreen(Screen):
    def __init__(self, game, width, height, font, playerController):
        super().__init__()
        self.game = game
        self.ship = game.selectedShip
        self.zoom = 1.0
        self.playerController = playerController
        self.font = font
        enemy_ship = Ship(
            "Enemy1",
            "Alien",
            "S",
            sprite=self.game.images["600i"],
            accel=1000,
            maxSpeed=3000,
            drag=0,
            turnSpeed=180,
        )
        enemy_ship.pos = pygame.Vector2(500, 500)

        # Créer l’IA qui suit le joueur
        enemy_ai = AdvancedAIController(self.ship)

        # Stocker dans une liste d’ennemis
        self.enemies = [(enemy_ship, enemy_ai)]

        self.planets = []

        if len(self.planets):
            print("[Game] Generationg plannets...")
            self.planets = self.generatePlanets


    # ===================== SHIP LOAD =====================
    def loadShip(self, ship, pos, vel, angle):
        self.ship = ship
        self.ship.pos = pygame.Vector2(pos)
        self.ship.vel = pygame.Vector2(vel)
        self.ship.angle = angle

    def generatePlanets(self):
        # Generate placeholder plannet
        planetList = [
            Planet(
                pos=pygame.Vector2(0, 0),
                radius=100,
                color=(255, 0, 0)
            )
        ]

        self.planets = planetList # Change so it's in a loop to generate a single planet
        print("[Game] Generated planets", [p.name for p in self.planets], "\n at coordinates :\n x:\t", [p.pos.x for p in self.planets], "\ny:\t", [p.pos.y for p in self.planets])

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                print("[Game] Attempting to open overlay")
                for planet in self.planets:
                    if getattr(planet, "inRange", False):
                        # fermer les autres overlays
                        for p in self.planets:
                            p.show_overlay = False

                        # ouvrir celle-ci
                        planet.renderOverlay = True
            elif event.key == pygame.K_c:
                for p in self.planets:
                    p.show_overlay = False


    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            self.zoom = min(2, self.zoom + 1.5 * dt)
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self.zoom = max(0.5, self.zoom - 0.5 * dt)

        for planet in self.planets:
            if planet.collidePoints(self.ship.pos, margin=10):
                planet.inRange = True
            else:
                planet.inRange = False
        # update ship physics
        controls = (
            self.playerController.getControls()
            if hasattr(self.playerController, "getControls")
            else self.playerController.getControls(self.ship)
        )
        self.ship.update(dt, controls)
        # update enemies
        for enemy, ai in self.enemies:
            controls = ai.getControls(enemy, dt)
            enemy.update(dt, controls)


    # ===================== RENDER =====================
    def render(self, surface):
        surface.fill((10, 10, 30))
        # camera centered
        half = pygame.Vector2(surface.get_size()) / 2
        cam = self.ship.pos - half / self.zoom

        # draw planets
        for planet in self.planets:
            planet.render(surface, cam, self.zoom)

        # draw ship
        for enemy, _ in self.enemies:
            enemy.render(surface, cam, self.zoom)
        self.ship.render(surface, cam, self.zoom)

        for planet in self.planets:
            planet.renderOverlay(surface, self.font)

        # debug info
        fps = self.font.render(f"FPS: {self.game.clock.get_fps():.1f}", True, (200, 200, 50))
        speed = self.font.render(f"Speed: {self.ship.vel.length():.1f}", True, (0, 255, 255))
        zoom_txt = self.font.render(f"Zoom: {self.zoom:.2f}×", True, (200, 200, 200))
        shipInfo = self.font.render(f"Ship: {self.ship.name}", True, (200, 100, 30))
        shipPos = self.font.render(f"Pos: {self.ship.pos}", True, (200, 100, 30))
        surface.blit(fps, (10, 10))
        surface.blit(speed, (10, 30))
        surface.blit(zoom_txt, (10, 50))
        surface.blit(shipInfo, (10, 70))
        surface.blit(shipPos, (10, 90))

        # minimap (bottom-right)
        self.render_minimap(surface, cam, self.zoom)

    # ===================== MINIMAP =====================
    def render_minimap(self, surface, cam, zoom):
        # small minimap: shows planets in the local 3x3 chunk area
        w, h = surface.get_size()
        mm_w, mm_h = 200, 120
        mm_x, mm_y = w - mm_w - 10, h - mm_h - 10
        mm_rect = pygame.Rect(mm_x, mm_y, mm_w, mm_h)
        pygame.draw.rect(surface, (15, 15, 25), mm_rect)
        pygame.draw.rect(surface, (100, 100, 140), mm_rect, 2)

        # define minimap world extents: centered on ship ± VIEW (e.g., CHUNK_SIZE)
        left = self.ship.pos.x
        top = self.ship.pos.y
        scale_x = mm_w
        scale_y = mm_h

        # draw planets in the gathered area
        for p in self.planets:
            sx = mm_x + (p.pos.x - left) * scale_x
            sy = mm_y + (p.pos.y - top) * scale_y
            # clamp inside minimap
            if not (mm_x <= sx <= mm_x + mm_w and mm_y <= sy <= mm_y + mm_h):
                continue
            r = max(2, int(3 * (p.radius / 2000)))  # dot size by radius
            pygame.draw.circle(surface, p.color, (int(sx), int(sy)), r)

        # player dot
        px = mm_x + mm_w / 2
        py = mm_y + mm_h / 2
        pygame.draw.circle(surface, (255, 255, 255), (int(px), int(py)), 4)
