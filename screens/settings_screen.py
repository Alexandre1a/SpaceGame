import pygame

from screens.base_screen import Screen
from ui.button import Button
from utils.settings_manager import (
    AVAILABLE_FPS,
    AVAILABLE_RESOLUTIONS,
    load_settings,
    save_settings,
)


class SettingsScreen(Screen):
    def __init__(self, game):
        self.game = game
        wf, hf = game.screen.get_width(), game.screen.get_height()
        font = self.game.fonts["default"]

        # Charge les settings existants depuis self.game.settings
        # (au lieu de recharger depuis le fichier)
        self.settings = self.game.getSettings().copy()

        # Index actuels pour parcourir les listes
        self.fps_index = AVAILABLE_FPS.index(self.settings["fps"])
        self.res_index = AVAILABLE_RESOLUTIONS.index(tuple(self.settings["resolution"]))

        # Boutons - ils seront centrés selon la résolution actuelle
        self.buttons = [
            Button("Apply & Exit", (wf // 2, hf // 2 + 150), self.exit_settings, font),
        ]

    def cycle_fps(self, direction):
        """Change le FPS en parcourant la liste circulaire"""
        self.fps_index = (self.fps_index + direction) % len(AVAILABLE_FPS)
        self.settings["fps"] = AVAILABLE_FPS[self.fps_index]

    def cycle_res(self, direction):
        """Change la résolution en parcourant la liste circulaire"""
        self.res_index = (self.res_index + direction) % len(AVAILABLE_RESOLUTIONS)
        self.settings["resolution"] = AVAILABLE_RESOLUTIONS[self.res_index]

    def toggle_fullscreen(self):
        """Active/désactive le mode plein écran"""
        self.settings["fullscreen"] = not self.settings["fullscreen"]

    def exit_settings(self):
        """Sauvegarde et applique les changements"""
        # 1. Sauvegarder dans le fichier JSON
        save_settings(self.settings)

        # 2. Mettre à jour les settings dans l'objet Game
        self.game.settings = self.settings.copy()

        # 3. Appliquer les changements de résolution
        flags = pygame.FULLSCREEN if self.settings["fullscreen"] else 0
        self.game.screen = pygame.display.set_mode(self.settings["resolution"], flags)

        # 4. IMPORTANT : Recréer tous les écrans pour recalculer les positions
        self.game.rebuild_screens()

        # 5. Retourner au menu (le nouveau menu avec les bonnes positions)
        self.game.current_screen = self.game.title_screen

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.cycle_fps(-1)
            elif event.key == pygame.K_RIGHT:
                self.cycle_fps(1)
            elif event.key == pygame.K_DOWN:
                self.cycle_res(-1)
            elif event.key == pygame.K_UP:
                self.cycle_res(1)
            elif event.key == pygame.K_f:
                self.toggle_fullscreen()

        for btn in self.buttons:
            btn.handle_event(event)

    def render(self, surface):
        surface.fill((20, 20, 40))
        font = self.game.fonts["default"]

        # Titre - toujours centré grâce au calcul dynamique
        title = font.render("Settings", True, (200, 200, 255))
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 80))

        # Affichage FPS
        fps_text = (
            "Unlimited" if self.settings["fps"] == 0 else str(self.settings["fps"])
        )
        fps_label = font.render(f"FPS: {fps_text} (← →)", True, (255, 255, 255))
        surface.blit(
            fps_label, (surface.get_width() // 2 - fps_label.get_width() // 2, 200)
        )

        # Affichage résolution
        w, h = self.settings["resolution"]
        res_label = font.render(f"Resolution: {w}x{h} (↑ ↓)", True, (255, 255, 255))
        surface.blit(
            res_label, (surface.get_width() // 2 - res_label.get_width() // 2, 250)
        )

        # Affichage fullscreen
        fs_label = font.render(
            f"Fullscreen: {'ON' if self.settings['fullscreen'] else 'OFF'} (press F)",
            True,
            (255, 255, 255),
        )
        surface.blit(
            fs_label, (surface.get_width() // 2 - fs_label.get_width() // 2, 300)
        )

        # Boutons
        for btn in self.buttons:
            btn.render(surface)
