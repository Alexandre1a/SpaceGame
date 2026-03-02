import json
import math
import random
from collections import OrderedDict
from random import randbytes, randint

import pygame

from entities.planet import Planet
from entities.ship import AdvancedAIController, Ship
from screens.base_screen import Screen

class System: # Move elsewhere
    def __init__(self, center) -> None:
        self.center = center
        self.planets = []

class GameScreen(Screen):
    def __init__(self, game, width, height, font, playerController):
        super().__init__()
        self.game = game
        self.ship = game.selectedShip
        self.zoom = 1.0
        self.playerController = playerController
        self.font = font
        self.overlayOpen = False
        self.savedVel = pygame.Vector2(0,0) # To Stop
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
        self.systems = []

        self.overlayRect = pygame.Rect(
            int(width * 0.05), # 5% From left
            int(height * 0.15), # 15% From right
            int(width * 0.4), # 40% width
            int(height * 0.5), # 50 height
        )
        # Procedural generation paramameters
        # Planets options
        self.genAttempts = 1500
        self.planetNb = 7
        self.minRadius = 20
        self.maxRadius = 60
        self.minSpacing = 1500
        self.size = (-7500, 7500)
        self.usedNames = set()
        self.colorRange = (0, 256)
        # Systems options
        self.systemNb = 40
        self.systemSize = 150
        self.systemGap = 25000
        self.systemMaxPlanet = 7
        self.systemMinPlanet = 3



    # ===================== SHIP LOAD =====================
    def loadShip(self, ship, pos, vel, angle):
        self.ship = ship
        self.ship.pos = pygame.Vector2(pos)
        self.ship.vel = pygame.Vector2(vel)
        self.ship.angle = angle

    def loadPlanets(self, planets):
        self.planets = planets

    def generateSystems(self):
        print("[GameScreen] Generating systems...")
        systemList = []
        for i in range(self.systemNb):
            placed = False
            for j in range(self.systemSize):
                cx = randint(self.size[0], self.size[1])
                cy = randint(self.size[0], self.size[1])
                center = pygame.Vector2(cx, cy)

                ok = True
                for s in systemList:
                    if (center - s.center).length_squared() < self.systemGap**2:
                        ok = False
                        break

                if ok:
                    systemList.append(System(center))
                    placed = True
                    break

        self.systems = systemList
        print("[GameScreen] Generated systems !")

    def generatePlanets(self):
        print("[GameScreen] Generating planets...")
        for system in self.systems:
            planetList = []
            planetNb = randint(self.systemMinPlanet, self.systemMaxPlanet)
            for i in range(planetNb):
                for j in range(self.genAttempts):
                    dist = randint(4000, 16000) # Magic numbers to change
                    angle = randint(0, 360)

                    r = randint(self.minRadius, self.maxRadius)
                    x = system.center.x + math.cos(math.radians(angle)) * dist
                    y = system.center.y + math.sin(math.radians(angle)) * dist

                    pos = pygame.Vector2(x, y)


                    ok = True
                    for p in system.planets:
                        needed = p.radius + r + self.minSpacing
                        if (pos - p.pos).length_squared()  < needed**2:
                            ok = False
                            break
                    if ok:
                        color = (randint(0,255), randint(0,255), randint(0,255))
                        planet = Planet((x, y), r, color)
                        planetList.append(planet)


        self.planets = planetList # Change so it's in a loop to generate a single planet
        print("[Game] Generated planets", [p.name for p in self.planets], "\nat coordinates :\nx:\t", [p.pos.x for p in self.planets], "\ny:\t", [p.pos.y for p in self.planets])

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for planet in self.planets:
                    if getattr(planet, "inRange", False):
                        for p in self.planets:
                            p.showOverlay = False

                        planet.showOverlay = True
                        # Stop the player
                        self.savedVel = self.ship.vel.copy()
                        self.ship.vel = pygame.Vector2(0,0)
                        self.overlayOpen = True
            elif event.key == pygame.K_c:
                for p in self.planets:
                    p.showOverlay = False
                self.ship.vel = self.savedVel
                self.overlayOpen = False


    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            self.zoom = min(2, self.zoom + 1.5 * dt)
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self.zoom = max(0.5, self.zoom - 0.5 * dt)

        if self.overlayOpen:
            return # Early return

        for planet in self.planets:
            if planet.collidePoints(self.ship.pos, margin=10):
                planet.inRange = True
            else:
                planet.inRange = False
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
            planet.renderOverlay(surface, self.font, self.overlayRect)

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
        w, h = surface.get_size()
        mm_w, mm_h = 200, 120
        mm_x = w - mm_w - 10
        mm_y = h - mm_h - 10

        # Fond et bordure
        mm_rect = pygame.Rect(mm_x, mm_y, mm_w, mm_h)
        pygame.draw.rect(surface, (15, 15, 25), mm_rect)
        pygame.draw.rect(surface, (100, 100, 140), mm_rect, 2)

        # VIEW_RANGE définit combien d'unités "monde" sont visibles
        # de chaque côté du vaisseau sur la minimap.
        # Augmente cette valeur pour "zoomer out" la minimap.
        VIEW_RANGE = 3000

        # L'échelle convertit des unités monde en pixels minimap.
        # Ex: si VIEW_RANGE=3000 et mm_w=200, scale_x = 200/6000 ≈ 0.033 px/unité
        scale_x = mm_w / (2 * VIEW_RANGE)
        scale_y = mm_h / (2 * VIEW_RANGE)

        # Le centre de la minimap correspond toujours à la position du vaisseau.
        # On calcule le décalage depuis ce centre pour chaque objet.
        center_mm_x = mm_x + mm_w // 2
        center_mm_y = mm_y + mm_h // 2

        # Dessiner les planètes
        for p in self.planets:
            dx = p.pos.x - self.ship.pos.x
            dy = p.pos.y - self.ship.pos.y

            sx = int(center_mm_x + dx * scale_x)
            sy = int(center_mm_y + dy * scale_y)

            # On calcule le rayon en pixels sur la minimap
            r = max(2, int(p.radius * scale_x))

            # On "gonfle" le rectangle de la minimap par le rayon du cercle.
            # Ainsi, on ne rejette le cercle que quand même son bord est sorti.
            visible_rect = mm_rect.inflate(r * 2, r * 2)
            if not visible_rect.collidepoint(sx, sy):
                continue

            # Maintenant on dessine, mais pygame.draw.circle déborde naturellement
            # hors de la minimap si on ne fait rien. Il faut donc "clipper" la surface.
            # On dit à pygame de n'autoriser le dessin que dans la zone de la minimap.
            surface.set_clip(mm_rect)
            pygame.draw.circle(surface, p.color, (sx, sy), r)
            surface.set_clip(None)  # On relâche le clip pour le reste du rendu

            # Taille du point proportionnelle au rayon de la planète,
            # mais avec un minimum de 2px pour rester visible
            r = max(2, int(p.radius * scale_x))
            pygame.draw.circle(surface, p.color, (sx, sy), r)

            # Afficher le nom si la planète est proche
            if abs(dx) < VIEW_RANGE * 0.5 and abs(dy) < VIEW_RANGE * 0.5:
                label = self.font.render(p.name, True, (180, 180, 180))
                surface.blit(label, (sx + r + 2, sy - 6))

        # Le vaisseau joueur est toujours au centre de la minimap
        pygame.draw.circle(surface, (255, 255, 255), (center_mm_x, center_mm_y), 4)

        # Optionnel : un petit indicateur de direction du vaisseau
        rad = math.radians(self.ship.angle - 90)
        tip_x = int(center_mm_x + math.cos(rad) * 8)
        tip_y = int(center_mm_y + math.sin(rad) * 8)
        pygame.draw.line(surface, (255, 255, 100), (center_mm_x, center_mm_y), (tip_x, tip_y), 2)
