#===========
#= Imports =
#===========
# Python
import math
import pygame
import random

# Custom
from entities.planet import Planet, PLANET_TYPE
from entities.ship import Ship
from screens.base_screen import Screen
from ui.button import Button
from ressources.ressources import getMusicPath

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
        self.planets = []

        self.overlayRect = pygame.Rect(
            int(width * 0.05), # 5% From left
            int(height * 0.15), # 15% From right
            int(width * 0.4), # 40% width
            int(height * 0.5), # 50% height
        )

        self.buttons = [
          Button("Accept Quest", (self.overlayRect.x + 100, self.overlayRect.y + 120) , None, self.font),
          Button("Complete Quest", (self.overlayRect.x + 400, self.overlayRect.y + 120) , None, self.font)
        ]

    def onEnter(self):
      pygame.mixer.music.stop()
      pygame.mixer.music.load(getMusicPath("main.wav"))
      pygame.mixer.music.play(-1)

    #================
    #= Save Loading =
    #================

    def loadShip(self, ship, pos, vel, angle):
        self.ship = ship
        self.ship.pos = pygame.Vector2(pos)
        self.ship.vel = pygame.Vector2(vel)
        self.ship.angle = angle

    def loadPlanets(self, planets):
        self.planets = planets

    #==================
    #= Procedural Gen =
    #==================

    def generatePlanets(self, count=12, spread=8000, minDistance=300):
        ''''
        Generates planets based on the parameters
        count: overhall planet count
        spread: how much space they occupy
        minDistantce: the minimal distance form eachother
        '''
        print("[GameScreen] Generating planets...")
        planets = []

        for _ in range(count):
            planetType = random.choice(list(PLANET_TYPE.keys()))
            typeData = PLANET_TYPE[planetType]

            radius = random.randint(*typeData["radiusRange"])
            color = random.choice(typeData["colors"])

            placed = False
            attempts = 0
            currentMinDistance = minDistance

            while not placed:
                angle = random.uniform(0, 2 * math.pi)
                dist = random.uniform(spread * 0.1, spread)
                pos = pygame.Vector2(dist * math.cos(angle), dist * math.sin(angle))

                tooClose = any( (pos - p.pos).length() < currentMinDistance + radius + p.radius for p in planets )

                if not tooClose:
                    self.planets.append(Planet(pos, radius, color, planetType=planetType))
                    placed = True
                else:
                    attempts += 1
                    if attempts % 20 == 0:
                        currentMinDistance = max(50, currentMinDistance - 50)

        print(f"[Game] Generated {len(self.planets)} plannets")

    def handleEvent(self, event):
      for btn in self.buttons:
        btn.handleEvent(event)
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_e:
            # Overlay, to accept quest and complete them
              for planet in self.planets:
                  if getattr(planet, "inRange", False):
                      for p in self.planets:
                          p.showOverlay = False
                          p.optionalText = ""
                          p.buttons = []

                      planet.showOverlay = True
                      if self.game.questManager.checkPlanetIsGiver(planet):
                        planet.optionalText += " \nI have a quest !"
                        self.buttons[0].setCallback(lambda p=planet: self.game.questManager.acceptQuest(p))
                        planet.buttons.append(self.buttons[0])
                        planet.buttons[0].setDisabled(False)
                      if self.game.questManager.checkPlanetIsTarget(planet):
                        planet.optionalText += "            I am a target!"
                        self.buttons[1].setCallback(lambda p=planet: self.game.questManager.completeQuest(p))
                        planet.buttons.append(self.buttons[1])
                        planet.buttons[1].setDisabled(False)
                      # Stop the player
                      self.savedVel = self.ship.vel.copy()
                      self.ship.vel = pygame.Vector2(0,0)
                      self.overlayOpen = True
          elif event.key == pygame.K_c:
              for p in self.planets:
                  p.showOverlay = False
                  p.optionalText = ""
              self.ship.vel = self.savedVel
              self.overlayOpen = False


    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
            self.zoom = min(2, self.zoom + 1.5 * dt)
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            self.zoom = max(0.0001, self.zoom - 0.5 * dt)

        if self.overlayOpen:
            return

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

    #=============
    #= Rendering =
    #=============
    def render(self, surface):
        surface.fill((10, 10, 30))
        # Center the camera
        half = pygame.Vector2(surface.get_size()) / 2
        cam = self.ship.pos - half / self.zoom

        # Draw planets
        for planet in self.planets:
            planet.render(surface, cam, self.zoom)

        # Draw ship
        self.ship.render(surface, cam, self.zoom)

        for planet in self.planets:
            planet.renderOverlay(surface, self.font, self.overlayRect)

        # Debug info
        fps = self.font.render(f"FPS: {self.game.clock.get_fps():.1f}", True, (200, 200, 50))
        speed = self.font.render(f"Speed: {self.ship.vel.length():.1f}", True, (0, 255, 255))
        zoom_txt = self.font.render(f"Zoom: {self.zoom:.2f}×", True, (200, 200, 200))
        shipInfo = self.font.render(f"Ship: {self.ship.name}", True, (200, 100, 30))
        shipPos = self.font.render(f"Pos: {self.ship.pos}", True, (200, 100, 30))
        moneyInfo = self.font.render(f"Money: {self.game.getMoney()}", True, (200, 100, 30))
        questInfo = self.font.render(f"Current Quest: {self.game.questManager.getActiveQuest()}", True, (200, 100, 30))
        surface.blit(fps, (10, 10))
        surface.blit(speed, (10, 30))
        surface.blit(zoom_txt, (10, 50))
        surface.blit(shipInfo, (10, 70))
        surface.blit(shipPos, (10, 90))
        surface.blit(moneyInfo, (10, 110))
        surface.blit(questInfo, (10, 130))

        self.renderMinimap(surface, self.zoom)
        self.renderQuestRadar(surface)

    #=======================
    #=        Utils        =
    #= Minimap/Quest Radar =
    #=======================
    def renderMinimap(self, surface, zoom):
      """
      Renders a simple minimap
      surface: the pygame surface to draw to
      zoom: zoom level, used to scale the minimap
      """
      w, h = surface.get_size()
      mm_w, mm_h = 200, 120
      mm_x = w - mm_w - 10
      mm_y = h - mm_h - 10

      # Background and border
      mm_rect = pygame.Rect(mm_x, mm_y, mm_w, mm_h)
      pygame.draw.rect(surface, (15, 15, 25), mm_rect)
      pygame.draw.rect(surface, (100, 100, 140), mm_rect, 2)

      VIEW_RANGE = 3000/zoom

      # Convert from world coordinates to minimap coordinates
      scale_x = mm_w / (2 * VIEW_RANGE)
      scale_y = mm_h / (2 * VIEW_RANGE)

      # The center of the minmap si the ship pos
      # Compute the gap from the center for each object
      center_mm_x = mm_x + mm_w // 2
      center_mm_y = mm_y + mm_h // 2

      for p in self.planets:
          dx = p.pos.x - self.ship.pos.x
          dy = p.pos.y - self.ship.pos.y

          sx = int(center_mm_x + dx * scale_x)
          sy = int(center_mm_y + dy * scale_y)

          # Compute the radius on the minimap
          r = max(2, int(p.radius * scale_x))

          # Inflate the minimap rectangle to not display a planet that is out of bounds
          visible_rect = mm_rect.inflate(r * 2, r * 2)
          if not visible_rect.collidepoint(sx, sy):
              continue

          # Clip the planets to the surface,
          # This tells Pygame to draw only in the minimap zone
          surface.set_clip(mm_rect)
          pygame.draw.circle(surface, p.color, (sx, sy), r)
          surface.set_clip(None)

          # Size of the point in correlation with the planet's radius but with a safeguard of 2 pixels
          r = max(2, int(p.radius * scale_x))
          pygame.draw.circle(surface, p.color, (sx, sy), r)


          # Display the name of the planet if we are near
          if abs(dx) < VIEW_RANGE * 0.5 and abs(dy) < VIEW_RANGE * 0.5:
              label = self.font.render(p.name, True, (180, 180, 180))
              surface.blit(label, (sx + r + 2, sy - 6))

      # Player's ship is at the center of the minimap
      pygame.draw.circle(surface, (255, 255, 255), (center_mm_x, center_mm_y), 4)

      # A small direction indicator
      rad = math.radians(self.ship.angle - 90)
      tip_x = int(center_mm_x + math.cos(rad) * 8)
      tip_y = int(center_mm_y + math.sin(rad) * 8)
      pygame.draw.line(surface, (255, 255, 100), (center_mm_x, center_mm_y), (tip_x, tip_y), 2)

    def renderQuestRadar(self, surface):
      """
      Renders an arrow to the quest destination, the colour depends on the distance
      """

      quest = self.game.questManager.getActiveQuestPos()
      if quest is None:
        return
      radarX = surface.get_width() - 120
      radarY = surface.get_height() - 200

      direction = quest - self.ship.pos
      dist = direction.length()

      # Normalise direction
      direction = direction.normalize()

      angle = math.atan2(direction.y, direction.x)
      size = 25

      p1 = (radarX + math.cos(angle)*size,
            radarY + math.sin(angle)*size)
      p2 = (radarX + math.cos(angle+2.5)*size/2,
            radarY + math.sin(angle+2.5)*size/2)
      p3 = (radarX + math.cos(angle-2.5)*size/2,
            radarY + math.sin(angle-2.5)*size/2)

      ratio = max(0, min(1, dist / 50000))
      color = ( int(255*(1-ratio)), 0, int(255*ratio))

      pygame.draw.polygon(surface, color, [p1, p2, p3])
