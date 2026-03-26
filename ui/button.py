
import pygame


class Button:
    def __init__(
        self,
        text,
        centerPos,
        callback,
        font,
        padding=(10, 5),
        idleColor=(200, 200, 200),
        hoverColor=(255, 255, 255),
        textColor=(0, 0, 0),
        disabledColor=(80, 80, 80),
    ):
        self._text = text
        self._callback = callback
        self._font = font
        self._padding = padding
        self._idleColor = idleColor
        self._hoverColor = hoverColor
        self._textColor = textColor
        self._disabled = False
        self._disabledColor = disabledColor

        self._textSurface = self._font.render(self._text, True, self._textColor)

        width = self._textSurface.get_width() + padding[0] * 2
        height = self._textSurface.get_height() + padding[1] * 2
        self._rect = pygame.Rect(0, 0, width, height)
        self._rect.center = centerPos

    #===========
    #= Getters =
    #===========

    def getText(self):
        return self._text

    def getRect(self):
        return self._rect

    def getPosition(self):
        return self._rect.center

    def getDisabled(self):
        return self._disabled

    #===========
    #= Setters =
    #===========

    def setText(self, text):
        self._text = text
        self._textSurface = self._font.render(self._text, True, self._textColor)

        # Update the size
        oldCenter = self._rect.center
        width = self._textSurface.get_width() + self._padding[0] * 2
        height = self._textSurface.get_height() + self._padding[1] * 2
        self._rect = pygame.Rect(0, 0, width, height)
        self._rect.center = oldCenter

    def setPosition(self, centerPos):
        self._rect.center = centerPos

    def setCallback(self, callback):
        self._callback = callback

    def setDisabled(self, state: bool):
        self._disabled = state

    def handleEvent(self, event):
        if self._disabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                self._onClick()

    def _onClick(self):
        if self._callback:
            try:
                self._callback()
                print(f"[Button] Exécution du callback : {self._callback}")
            except Exception as e:
                print(f"[Button] Erreur lors de l'exécution du callback : {e}")

    # ==================== RENDU ====================

    def render(self, surface):
        mousePos = pygame.mouse.get_pos()

        isHovered = self._rect.collidepoint(mousePos)

        if self._disabled:
            color = self._disabledColor
        else:
            color = self._hoverColor if isHovered else self._idleColor

        pygame.draw.rect(surface, color, self._rect)

        borderColor = tuple(max(0, c - 50) for c in color)
        pygame.draw.rect(surface, borderColor, self._rect, 2)

        textPos = (self._rect.x + self._padding[0], self._rect.y + self._padding[1])
        surface.blit(self._textSurface, textPos)

    def isHovered(self):
        mousePos = pygame.mouse.get_pos()
        return self._rect.collidepoint(mousePos)
