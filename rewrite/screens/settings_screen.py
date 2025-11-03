"""
Écran des paramètres du jeu.
Permet de modifier la résolution, le FPS et le mode plein écran.
"""

import pygame
from screens.base_screen import Screen
from ui.button import Button
from utils.settings_manager import (
    saveSettings,
    AVAILABLE_FPS,
    AVAILABLE_RESOLUTIONS
)


class SettingsScreen(Screen):
    """
    Écran de configuration des paramètres du jeu.
    Permet de modifier les options graphiques et de performance.
    """

    def __init__(self, game):
        """
        Initialise l'écran des paramètres.
        
        Args:
            game: Référence vers l'objet Game principal
        """
        self._game = game
        
        # Récupération des dimensions de l'écran
        screenWidth = game.getScreen().get_width()
        screenHeight = game.getScreen().get_height()
        
        # Récupération de la police
        font = game.getFonts()['default']

        # Copie des paramètres actuels pour modification
        self._settings = game.getSettings().copy()

        # Index actuels dans les listes de valeurs possibles
        self._fpsIndex = AVAILABLE_FPS.index(self._settings["fps"])
        self._resIndex = AVAILABLE_RESOLUTIONS.index(tuple(self._settings["resolution"]))

        # Bouton pour appliquer et sortir
        self._applyButton = Button(
            "Appliquer et Quitter",
            (screenWidth // 2, screenHeight // 2 + 150),
            self._exitSettings,
            font
        )

        # Bouton pour réinitialiser
        self._resetButton = Button(
            "Réinitialiser",
            (screenWidth // 2, screenHeight // 2 + 200),
            self._resetSettings,
            font
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
        from utils.settings_manager import DEFAULT_SETTINGS
        self._settings = DEFAULT_SETTINGS.copy()
        self._fpsIndex = AVAILABLE_FPS.index(self._settings["fps"])
        self._resIndex = AVAILABLE_RESOLUTIONS.index(tuple(self._settings["resolution"]))
        print("[SettingsScreen] Paramètres réinitialisés")

    def _exitSettings(self):
        """Applique les paramètres et retourne au menu"""
        # Sauvegarder dans le fichier
        saveSettings(self._settings)
        
        # Mettre à jour les paramètres dans l'objet Game
        oldResolution = self._game.getSettings()["resolution"]
        self._game._settings = self._settings.copy()
        
        # Appliquer les changements de résolution si nécessaire
        newResolution = self._settings["resolution"]
        if oldResolution != newResolution or self._settings["fullscreen"] != self._game.getSettings().get("fullscreen"):
            flags = pygame.FULLSCREEN if self._settings["fullscreen"] else 0
            self._game._screen = pygame.display.set_mode(newResolution, flags)
            
            # Reconstruire tous les écrans avec les nouvelles dimensions
            self._game.rebuildScreens()
        
        # Retourner au menu
        self._game.goToMenu()
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
                self._game.goToMenu()

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
        titleFont = self._game.getFonts().get('title', self._font)
        titleText = titleFont.render("PARAMÈTRES", True, (200, 200, 255))
        titleRect = titleText.get_rect(center=(surface.get_width() // 2, 80))
        surface.blit(titleText, titleRect)

        # Position de départ pour les options
        centerX = surface.get_width() // 2
        startY = 200

        # === OPTION FPS ===
        fpsValue = "Illimité" if self._settings["fps"] == 0 else str(self._settings["fps"])
        fpsText = self._font.render(
            f"FPS: {fpsValue}",
            True,
            (255, 255, 255)
        )
        fpsRect = fpsText.get_rect(center=(centerX, startY))
        surface.blit(fpsText, fpsRect)

        # Flèches pour FPS
        arrowText = self._font.render("◄    ►", True, (150, 150, 150))
        arrowRect = arrowText.get_rect(center=(centerX, startY + 30))
        surface.blit(arrowText, arrowRect)

        # === OPTION RÉSOLUTION ===
        width, height = self._settings["resolution"]
        resText = self._font.render(
            f"Résolution: {width}x{height}",
            True,
            (255, 255, 255)
        )
        resRect = resText.get_rect(center=(centerX, startY + 80))
        surface.blit(resText, resRect)

        # Flèches pour résolution
        arrowText2 = self._font.render("▲    ▼", True, (150, 150, 150))
        arrowRect2 = arrowText2.get_rect(center=(centerX, startY + 110))
        surface.blit(arrowText2, arrowRect2)

        # === OPTION PLEIN ÉCRAN ===
        fsStatus = "ON" if self._settings["fullscreen"] else "OFF"
        fsText = self._font.render(
            f"Plein écran: {fsStatus}",
            True,
            (255, 255, 255)
        )
        fsRect = fsText.get_rect(center=(centerX, startY + 160))
        surface.blit(fsText, fsRect)

        # Touche pour basculer
        fsHintText = self._font.render(
            "(Appuyez sur F pour basculer)",
            True,
            (120, 120, 120)
        )
        fsHintRect = fsHintText.get_rect(center=(centerX, startY + 190))
        surface.blit(fsHintText, fsHintRect)

        # Boutons
        self._applyButton.render(surface)
        self._resetButton.render(surface)

        # Instructions
        instructions = [
            "Utilisez les flèches ← → pour changer le FPS",
            "Utilisez les flèches ↑ ↓ pour changer la résolution",
            "Appuyez sur F pour activer/désactiver le plein écran",
            "Échap pour annuler"
        ]
        
        yOffset = surface.get_height() - 120
        for instruction in instructions:
            instText = self._font.render(instruction, True, (100, 100, 100))
            instRect = instText.get_rect(center=(centerX, yOffset))
            surface.blit(instText, instRect)
            yOffset += 25
