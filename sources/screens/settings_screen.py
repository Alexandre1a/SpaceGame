"""
Settings screen
Allows the user to modify game settings such as resolution, framerate , and fullscreen mode
"""

import pygame

from screens.base_screen import Screen
from ui.button import Button
from utils.settings_manager import (
    AVAILABLE_FPS,
    AVAILABLE_RESOLUTIONS,
    resetSettings,
    saveSettings,
)


class SettingsScreen(Screen):
    """
    Settings screen,
    Allow the modification of game settings such graphics and performance
    """

    def __init__(self, game, width, height, font, titleFont, settings):
        self._game = game
        self.width = width
        self.height = height

        self._font = font
        self._titleFont = titleFont

        self._settings = settings

        self._fpsIndex = AVAILABLE_FPS.index(self._settings["fps"])
        self._resIndex = AVAILABLE_RESOLUTIONS.index(
            tuple(self._settings["resolution"])
        )

        self._applyButton = Button(
            "Appliquer et Quitter",
            (width // 2, height // 2 + 150),
            self._exitSettings,
            font,
        )

        self._resetButton = Button(
            "Réinitialiser",
            (width // 2, height // 2 + 200),
            self._resetSettings,
            font,
        )

        self._font = font

    def _cycleFPS(self, direction):
        """
        Change the maximum framerate by cycling through the available options

        Args:
            direction: 1 to increase, -1 to decrease
        """
        self._fpsIndex = (self._fpsIndex + direction) % len(AVAILABLE_FPS)
        self._settings["fps"] = AVAILABLE_FPS[self._fpsIndex]

    def _cycleResolution(self, direction):
        """
        Change the resolution by cycling through the available options

        Args:
            direction: 1 to increase, -1 to decrease
        """
        self._resIndex = (self._resIndex + direction) % len(AVAILABLE_RESOLUTIONS)
        self._settings["resolution"] = AVAILABLE_RESOLUTIONS[self._resIndex]

    def _toggleFullscreen(self):
        """Enable or disable fullscreen mode (can be bugged)"""
        self._settings["fullscreen"] = not self._settings["fullscreen"]

    def _resetSettings(self):
        """Réinitialise les paramètres aux valeurs par défaut"""
        resetSettings()

    def _exitSettings(self):
        """Apply settings and return to the menu"""
        saveSettings(self._settings)
        self.screen = pygame.display.set_mode(self._game.settings["resolution"])
        self._game.initScreens()
        self._game.displayMenu()
        print("[SettingsScreen] Paramètres appliqués")

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._cycleFPS(-1)
            elif event.key == pygame.K_RIGHT:
                self._cycleFPS(1)
            elif event.key == pygame.K_DOWN:
                self._cycleResolution(-1)
            elif event.key == pygame.K_UP:
                self._cycleResolution(1)
            elif event.key == pygame.K_f:
                self._toggleFullscreen()
            elif event.key == pygame.K_ESCAPE:
                self._game.displayMenu()

        self._applyButton.handleEvent(event)
        self._resetButton.handleEvent(event)

    def update(self, dt):
      # Static screen
      pass

    def render(self, surface):
        surface.fill((20, 20, 40))

        self._titleText = self._titleFont.render("PARAMÈTRES", True, (200, 200, 255))
        self._titleRect = self._titleText.get_rect(
            center=(surface.get_width() // 2, 80)
        )
        surface.blit(self._titleText, self._titleRect)

        self._centerX = surface.get_width() // 2
        self._startY = 200

        self._fpsValue = str(self._settings["fps"])
        self._fpsText = self._font.render(
            f"FPS: {self._fpsValue}", True, (255, 255, 255)
        )
        self._fpsRect = self._fpsText.get_rect(center=(self._centerX, self._startY))
        surface.blit(self._fpsText, self._fpsRect)

        arrowText = self._font.render("◄    ►", True, (150, 150, 150)) # Might need custom fonts
        arrowRect = arrowText.get_rect(center=(self._centerX, self._startY + 30))
        surface.blit(arrowText, arrowRect)

        width, height = self._settings["resolution"]
        resText = self._font.render(
            f"Résolution: {width}x{height}", True, (255, 255, 255)
        )
        resRect = resText.get_rect(center=(self._centerX, self._startY + 80))
        surface.blit(resText, resRect)

        arrowText2 = self._font.render("▲    ▼", True, (150, 150, 150))
        arrowRect2 = arrowText2.get_rect(center=(self._centerX, self._startY + 110))
        surface.blit(arrowText2, arrowRect2)

        fsStatus = "ON" if self._settings["fullscreen"] else "OFF"
        fsText = self._font.render(f"Plein écran: {fsStatus}", True, (255, 255, 255))
        fsRect = fsText.get_rect(center=(self._centerX, self._startY + 160))
        surface.blit(fsText, fsRect)

        fsHintText = self._font.render(
            "(Appuyez sur F pour basculer)", True, (120, 120, 120)
        )
        fsHintRect = fsHintText.get_rect(center=(self._centerX, self._startY + 190))
        surface.blit(fsHintText, fsHintRect)

        self._applyButton.render(surface)
        self._resetButton.render(surface)

        instructions = [
            "Utilisez les flèches ← → pour changer le FPS",
            "Utilisez les flèches ↑ ↓ pour changer la résolution",
            "Appuyez sur F pour activer/désactiver le plein écran",
            "Échap pour annuler",
        ]

        self._yOffset = surface.get_height() - 120
        for instruction in instructions:
            instText = self._font.render(instruction, True, (100, 100, 100))
            instRect = instText.get_rect(center=(self._centerX, self._yOffset))
            surface.blit(instText, instRect)
            self._yOffset += 25
