"""
Écran des paramètres du jeu.
Permet de modifier la résolution, le framerate et le mode plein écran.
"""

import pygame

from screens.base_screen import Screen
from ui.button import Button
from utils.settings_manager import (
    AVAILABLE_FPS,
    AVAILABLE_RESOLUTIONS,
    DEFAULT_SETTINGS,
    resetSettings,
    saveSettings,
)


class SettingsScreen(Screen):
    """
    Écran de configuration des paramètres du jeu.
    Permet de modifier les options graphiques et de performance.
    """

    def __init__(self, game, width, height, font, titleFont, settings):
        """
        Initialise l'écran des paramètres.

        Args:
            game: Référence vers l'objet Game principal
        """
        self._game = game
        self.width = width
        self.height = height

        # Récupération de la police
        self._font = font
        self._titleFont = titleFont

        # Copie des paramètres actuels pour modification
        self._settings = settings

        # Index actuels dans les listes de valeurs possibles
        self._fpsIndex = AVAILABLE_FPS.index(self._settings["fps"])
        self._resIndex = AVAILABLE_RESOLUTIONS.index(
            tuple(self._settings["resolution"])
        )

        # Bouton pour appliquer et sortir
        self._applyButton = Button(
            "Appliquer et Quitter",
            (width // 2, height // 2 + 150),
            self._exitSettings,
            font,
        )

        # Bouton pour réinitialiser
        self._resetButton = Button(
            "Réinitialiser",
            (width // 2, height // 2 + 200),
            self._resetSettings,
            font,
        )

        self._font = font

    def _cycleFPS(self, direction):
        """
        Change le FPS en parcourant la liste circulaire.

        Args:
            direction: 1 pour augmenter, -1 pour diminuer
        """
        self._fpsIndex = (self._fpsIndex + direction) % len(AVAILABLE_FPS)
        self._settings["fps"] = AVAILABLE_FPS[self._fpsIndex]

    def _cycleResolution(self, direction):
        """
        Change la résolution en parcourant la liste circulaire.

        Args:
            direction: 1 pour augmenter, -1 pour diminuer
        """
        self._resIndex = (self._resIndex + direction) % len(AVAILABLE_RESOLUTIONS)
        self._settings["resolution"] = AVAILABLE_RESOLUTIONS[self._resIndex]

    def _toggleFullscreen(self):
        """Active ou désactive le mode plein écran"""
        self._settings["fullscreen"] = not self._settings["fullscreen"]

    def _resetSettings(self):
        """Réinitialise les paramètres aux valeurs par défaut"""
        self._settings = DEFAULT_SETTINGS.copy()
        self._fpsIndex = AVAILABLE_FPS.index(self._settings["fps"])
        self._resIndex = AVAILABLE_RESOLUTIONS.index(
            tuple(self._settings["resolution"])
        )
        print("[SettingsScreen] Paramètres réinitialisés")

    def _exitSettings(self):
        """Applique les paramètres et retourne au menu"""
        # Sauvegarder dans le fichier
        saveSettings(self._settings)
        # Applique la résolution
        self.screen = pygame.display.set_mode(self._game.settings["resolution"])
        self._game.initScreens()
        # Retourner au menu
        self._game.displayMenu()
        print("[SettingsScreen] Paramètres appliqués")

    def handleEvent(self, event):
        """
        Gère les événements de l'écran des paramètres.

        Args:
            event: Événement pygame à traiter
        """
        if event.type == pygame.KEYDOWN:
            # Navigation dans les paramètres avec les flèches
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
                # Retour sans sauvegarder
                self._game.displayMenu()

        # Gestion des boutons
        self._applyButton.handleEvent(event)
        self._resetButton.handleEvent(event)

    def update(self, dt):
        """
        Met à jour la logique de l'écran des paramètres.

        Args:
            dt: Delta time
        """
        # L'écran des paramètres est statique
        pass

    def render(self, surface):
        """
        Affiche l'écran des paramètres.

        Args:
            surface: Surface pygame sur laquelle dessiner
        """
        # Fond
        surface.fill((20, 20, 40))

        # Titre

        self._titleText = self._titleFont.render("PARAMÈTRES", True, (200, 200, 255))
        self._titleRect = self._titleText.get_rect(
            center=(surface.get_width() // 2, 80)
        )
        surface.blit(self._titleText, self._titleRect)

        # Position de départ pour les options
        self._centerX = surface.get_width() // 2
        self._startY = 200

        # === OPTION FPS ===
        self._fpsValue = str(self._settings["fps"])
        self._fpsText = self._font.render(
            f"FPS: {self._fpsValue}", True, (255, 255, 255)
        )
        self._fpsRect = self._fpsText.get_rect(center=(self._centerX, self._startY))
        surface.blit(self._fpsText, self._fpsRect)

        # Flèches pour FPS
        arrowText = self._font.render("◄    ►", True, (150, 150, 150))
        arrowRect = arrowText.get_rect(center=(self._centerX, self._startY + 30))
        surface.blit(arrowText, arrowRect)

        # === OPTION RÉSOLUTION ===
        width, height = self._settings["resolution"]
        resText = self._font.render(
            f"Résolution: {width}x{height}", True, (255, 255, 255)
        )
        resRect = resText.get_rect(center=(self._centerX, self._startY + 80))
        surface.blit(resText, resRect)

        # Flèches pour résolution
        arrowText2 = self._font.render("▲    ▼", True, (150, 150, 150))
        arrowRect2 = arrowText2.get_rect(center=(self._centerX, self._startY + 110))
        surface.blit(arrowText2, arrowRect2)

        # === OPTION PLEIN ÉCRAN ===
        fsStatus = "ON" if self._settings["fullscreen"] else "OFF"
        fsText = self._font.render(f"Plein écran: {fsStatus}", True, (255, 255, 255))
        fsRect = fsText.get_rect(center=(self._centerX, self._startY + 160))
        surface.blit(fsText, fsRect)

        # Touche pour basculer
        fsHintText = self._font.render(
            "(Appuyez sur F pour basculer)", True, (120, 120, 120)
        )
        fsHintRect = fsHintText.get_rect(center=(self._centerX, self._startY + 190))
        surface.blit(fsHintText, fsHintRect)

        # Boutons
        self._applyButton.render(surface)
        self._resetButton.render(surface)

        # Instructions
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
