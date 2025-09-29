import pygame

class Planet:
    def __init__(self, pos, radius, color):
        """
        pos    : pygame.Vector2 en coords monde
        radius : rayon en px “monde”
        color  : tuple RGB
        """
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.color = color

    def render(self, surface, camera_offset, zoom):
        # transforme coords monde → écran
        screen_pos = (self.pos - camera_offset) * zoom
        screen_radius = int(self.radius * zoom)
        if screen_radius > 1:
            pygame.draw.circle(
                surface,
                self.color,
                (int(screen_pos.x), int(screen_pos.y)),
                screen_radius
            )