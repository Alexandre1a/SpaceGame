"""
Écran titre du jeu.
Affiche le menu principal avec les options de jeu et l'argent du joueur.
"""

import pygame
from screens.base_screen import Screen
from ui.button import Button


class TitleScreen(Screen):
    """
    Écran titre affichant le menu principal du jeu.
    """

    def __init__(self, game):
        """
        Initialise l'écran titre.
        
        Args:
            game: Référence vers l'objet Game principal
        """
        self._game = game
        
        # Récupération des dimensions de l'écran
        screenWidth = game.getScreen().get_width()
        screenHeight = game.getScreen().get_height()
        
        # Récupération de la police par défaut
        font = game.getFonts()['default']
        titleFont = game.getFonts().get('title', font)

        # Position verticale de départ pour les boutons
        centerX = screenWidth // 2
        startY = screenHeight // 2 - 100

        # Création des boutons du menu
        self._buttons = [
            Button(
                "Nouvelle Partie",
                (centerX, startY),
                game.startGame,
                font
            ),
            Button(
                "Charger Partie",
                (centerX, startY + 60),
                game.loadGameFromFile,
                font
            ),
            Button(
                "Sélection Vaisseau",
                (centerX, startY + 120),
                game.openShipSelection,
                font
            ),
            Button(
                "Paramètres",
                (centerX, startY + 180),
                game.openSettings,
                font
            ),
            Button(
                "Quitter",
                (centerX, startY + 240),
                game.quit,
                font
            ),
        ]

        # Stockage des polices pour le rendu
        self._font = font
        self._titleFont = titleFont

    def handleEvent(self, event):
        """
        Gère les événements de l'écran titre.
        
        Args:
            event: Événement pygame à traiter
        """
        # Passer l'événement à tous les boutons
        for button in self._buttons:
            button.handleEvent(event)

    def update(self, dt):
        """
        Met à jour la logique de l'écran titre.
        
        Args:
            dt: Delta time (temps écoulé depuis la dernière frame)
        """
        # L'écran titre est statique, pas de mise à jour nécessaire
        pass

    def render(self, surface):
        """
        Effectue le rendu de l'écran titre.
        
        Args:
            surface: Surface pygame sur laquelle dessiner
        """
        # Fond de l'espace (bleu très sombre)
        surface.fill((5, 5, 20))

        # === TITRE DU JEU ===
        titleText = self._titleFont.render("SPACE GAME", True, (100, 200, 255))
        titleRect = titleText.get_rect(center=(surface.get_width() // 2, 80))
        surface.blit(titleText, titleRect)

        # === ARGENT DU JOUEUR ===
        money = self._game.getMoney()
        moneyText = self._font.render(
            f"Crédits disponibles : {money:,} ¢",
            True,
            (255, 215, 0)  # Couleur or
        )
        moneyRect = moneyText.get_rect(center=(surface.get_width() // 2, 150))
        
        # Fond semi-transparent pour le texte d'argent
        bgRect = moneyRect.inflate(20, 10)
        bgSurface = pygame.Surface(bgRect.size, pygame.SRCALPHA)
        bgSurface.fill((0, 0, 0, 128))  # Noir semi-transparent
        surface.blit(bgSurface, bgRect)
        surface.blit(moneyText, moneyRect)

        # === VAISSEAU SÉLECTIONNÉ ===
        selectedShip = self._game.getSelectedShip()
        if selectedShip:
            shipName = selectedShip.getName()
            brand = selectedShip.getBrand()
            shipInfoText = f"Vaisseau : {brand} {shipName}"
        else:
            shipInfoText = "Aucun vaisseau sélectionné"
        
        shipText = self._font.render(shipInfoText, True, (150, 150, 255))
        shipRect = shipText.get_rect(center=(surface.get_width() // 2, 200))
        surface.blit(shipText, shipRect)

        # === BOUTONS ===
        for button in self._buttons:
            button.render(surface)

        # === VERSION DU JEU ===
        versionText = self._font.render("v1.0.0", True, (80, 80, 80))
        versionRect = versionText.get_rect(bottomright=(surface.get_width() - 10, surface.get_height() - 10))
        surface.blit(versionText, versionRect)