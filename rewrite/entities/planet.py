import random

import pygame
from pygame.typing import RectLike

from ui.button import Button


# A dict to hold all types of planets
PLANET_TYPE = {
    "rocky": {
        "colors": [(180, 120, 80), (160, 100, 60), (200, 140, 90), (140, 90, 60)],
        "radiusRange": (30, 80),
    },
    "gasGiant": {
        "colors": [(200, 160, 100), (180, 120, 80), (220, 180, 130), (160, 100, 60)],
        "radiusRange": (100, 200),
    },
    "ice": {
        "colors": [(160, 180, 200), (140, 160, 180), (120, 140, 160), (100, 120, 140)],
        "radiusRange": (50, 100),
    },
}

class Planet:
    def __init__(self, pos, radius, color, name=None, planetType=None):
        """
        pos    : pygame.Vector2 en coords monde
        radius : rayon en px “monde”
        color  : tuple RGB
        """
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.color = color
        self.showOverlay = False
        self.availableQuests = []
        self.inRange = False
        self.name = name if name else self.generateName()
        self.planetType = planetType or "rocky"
        self.optionalText = ""
        self.buttons = []

    def generateName(self):
        self.letters = [
            "ty",
            "no",
            "li",
            "ge",
            "new",
            "ven",
            "tura",
            "ex",
            "treme",
            "dra",
            "cula",
            "zyr",
            "pha",
            "phyr",
            "mir",
            "bit",
            "ye",
            "xe",
            "cy",
            "ber",
        ]
        self.name = random.choice(self.letters).capitalize() + random.choice( self.letters )
        if random.random() < 0.4:
            self.name += f"-{random.randint(1, 99)}"
        return self.name

    def render(self, surface, cameraOffset, zoom):
        # transforme coords monde → écran
        self.screenPos = (self.pos - cameraOffset) * zoom
        self.screenRadius = int(self.radius * zoom)
        if self.screenRadius > 1:
            if self.inRange:
                self.haloRadius = self.screenRadius + 10
                self.haloColor = (255, 255, 120)
                pygame.draw.circle(
                    surface,
                    self.haloColor,
                    (int(self.screenPos.x), int(self.screenPos.y)),
                    self.haloRadius,
                    width=3,
                )
            pygame.draw.circle(
                surface,
                self.color,
                (int(self.screenPos.x), int(self.screenPos.y)),
                self.screenRadius,
            )

    def collidePoints(self, point, margin=0) -> bool:
        p = pygame.Vector2(point)
        r = self.radius + margin
        return (p - self.pos).length_squared() < (r * r)

    def to_dict(self):
        return {
            "pos": [self.pos.x, self.pos.y],
            "radius": self.radius,
            "color": list(self.color),
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data):
        # assure que pos est Vector2 et color est tuple
        pos = pygame.Vector2(data["pos"])
        radius = data["radius"]
        color = tuple(data["color"])
        name = data.get("name")
        p = cls(pos, radius, color, name=name)
        p.showOverlay = data.get("showOverlay", False)
        return p

    def to_save_data(self):
        return [(self.pos.x, self.pos.y), self.radius, self.color, self.name]

    @staticmethod
    def from_save_data(data):
        return Planet(data[0], data[1], data[2], data[3])

    def renderOverlay(self, surface, font, rect):
        if not self.showOverlay:
            return
        pygame.draw.rect(surface, (30, 30, 60), rect)
        pygame.draw.rect(surface, (200, 200, 255), rect, 3)

        self.title = font.render("Name: " + self.name, True, (255, 255, 255))
        surface.blit(self.title, (rect.x + 20, rect.y + 20))
        self.planetTypeText = font.render("Type: " + self.planetType, True, (255, 255, 255))
        surface.blit(self.planetTypeText, (rect.x + 20, rect.y + 40))
        surface.blit(font.render(self.optionalText, True, (255, 255, 255)), (rect.x + 20, rect.y + 60))
        self.tips = font.render(" Press C to close ", True, (100, 100, 100))
        surface.blit(self.tips, (rect.x + 400, rect.y + 20))
        if len(self.buttons) != 0:
          for btn in self.buttons:
            btn.render(surface)
        # Button("Accept Quest",(rect.x + 400, rect.y + 20), None, font).render(surface)
