import pygame

class Button:
    def __init__(self, text, center_pos, callback, font,
                 padding=(10, 5), idle_color=(200,200,200), hover_color=(255,255,255), text_color=(0,0,0)):
        self.text = text
        self.callback = callback
        self.font = font
        # Render text
        self.text_surf = self.font.render(self.text, True, text_color)
        # Calculate rect with padding
        w = self.text_surf.get_width() + padding[0]*2
        h = self.text_surf.get_height() + padding[1]*2
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = center_pos
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.padding = padding

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def render(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.idle_color
        pygame.draw.rect(surface, color, self.rect)
        # Blit text
        text_pos = (self.rect.x + self.padding[0], self.rect.y + self.padding[1])
        surface.blit(self.text_surf, text_pos)