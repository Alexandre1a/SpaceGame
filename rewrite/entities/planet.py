import random

import pygame


class Planet:
    def __init__(self, pos, radius, color, name=None):
        """
        pos    : pygame.Vector2 en coords monde
        radius : rayon en px “monde”
        color  : tuple RGB
        """
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.color = color
        self.showOverlay = False
        self.inRange = False
        self.name = name if name else self.generateName()

    def generateName(self):
        self.letters = [
            "ty",
            "no",
            "li",
            "ge",
            "goy",
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
            "slop",
            "ye",
            "xe",
            "cy",
            "ber",
        ]
        self.name = random.choice(self.letters).capitalize() + random.choice(
            self.letters
        )
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

    def collidesPoint(self, point, margin=0) -> bool:
        self.p = pygame.Vector2(point)
        self.r = self.radius + margin
        return (self.p - self.pos).length_squared() < (self.r * self.r)

    def to_dict(self):
        return {
            "pos": [self.pos.x, self.pos.y],
            "radius": self.radius,
            "color": list(self.color),
            "name": self.name,
            "showOverlay": bool(self.showOverlay),
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

    def renderOverlay(self, surface, font):
        if not self.showOverlay:
            return
        self.overlayRect = pygame.Rect(100, 100, 600, 400)
        pygame.draw.rect(surface, (30, 30, 60), self.overlayRect)
        pygame.draw.rect(surface, (200, 200, 255), self.overlayRect, 3)

        self.title = font.render(self.name, True, (255, 255, 255))
        surface.blit(self.title, (self.overlayRect.x + 20, self.overlayRect.y + 20))

        self.tips = font.render(" Press C to close ", True, (100, 100, 100))
        surface.blit(self.tips, (self.overlayRect.x + 400, self.overlayRect.y + 20))
        self.content = font.render(
            "Quêtes, Ressources, Boutique", True, (200, 200, 200)
        )
        surface.blit(self.content, (self.overlayRect.x + 20, self.overlayRect.y + 60))
