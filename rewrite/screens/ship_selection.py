"""
Écran de sélection de vaisseau.
Permet au joueur de choisir son vaisseau parmi ceux disponibles.
"""

import pygame
from screens.base_screen import Screen
from ui.button import Button


class ShipSelectionScreen(Screen):
    """
    Écran permettant de sélectionner un vaisseau.
    Affiche la liste des vaisseaux disponibles avec leurs caractéristiques.
    """

    def __init__(self, game):
        """
        Initialise l'écran de sélection de vaisseau.
        
        Args:
            game: Référence vers l'objet Game principal
        """
        self._game = game
        
        # Récupération des dimensions de l'écran
        screenWidth = game.getScreen().get_width()
        screenHeight = game.getScreen().get_height()
        
        # Récupération des polices
        font = game.getFonts()['default']
        
        # Création des boutons pour chaque vaisseau disponible
        self._buttons = []
        availableShips = game.getAvailableShips()
        
        startY = 200
        spacing = 80
        
        for i, ship in enumerate(availableShips):
            # Nom affiché : Marque + Nom du vaisseau
            displayName = f"{ship.getBrand()} {ship.getName()}"
            
            button = Button(
                displayName,
                (screenWidth // 2, startY + i * spacing),
                lambda s=ship: self._selectShip(s),
                font
            )
            self._buttons.append(button)
        
        # Bouton retour
        self._backButton = Button(
            "Retour",
            (screenWidth // 2, screenHeight - 80),
            game.goToMenu,
            font
        )
        
        self._font = font
        self._selectedForPreview = None  # Vaisseau survolé pour l'aperçu

    def _selectShip(self, ship):
        """
        Sélectionne un vaisseau et retourne au menu principal.
        
        Args:
            ship: Le vaisseau sélectionné
        """
        self._game.setSelectedShip(ship)
        print(f"[ShipSelection] Vaisseau sélectionné : {ship.getBrand()} {ship.getName()}")
        self._game.goToMenu()

    def handleEvent(self, event):
        """
        Gère les événements de l'écran de sélection.
        
        Args:
            event: Événement pygame à traiter
        """
        # Touche Échap pour retourner au menu
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._game.goToMenu()
                return

        # Gestion des clics sur les boutons
        for button in self._buttons:
            button.handleEvent(event)
        
        self._backButton.handleEvent(event)

    def update(self, dt):
        """
        Met à jour la logique de l'écran de sélection.
        
        Args:
            dt: Delta time
        """
        # Détecter le vaisseau survolé pour l'aperçu
        availableShips = self._game.getAvailableShips()
        self._selectedForPreview = None
        
        for i, button in enumerate(self._buttons):
            if button.isHovered() and i < len(availableShips):
                self._selectedForPreview = availableShips[i]
                break

    def render(self, surface):
        """
        Affiche l'écran de sélection de vaisseau.
        
        Args:
            surface: Surface pygame sur laquelle dessiner
        """
        # Fond
        surface.fill((15, 15, 35))

        # Titre
        titleFont = self._game.getFonts().get('title', self._font)
        titleText = titleFont.render("SÉLECTION DE VAISSEAU", True, (150, 200, 255))
        titleRect = titleText.get_rect(center=(surface.get_width() // 2, 80))
        surface.blit(titleText, titleRect)

        # Boutons des vaisseaux
        for button in self._buttons:
            button.render(surface)

        # Bouton retour
        self._backButton.render(surface)

        # Aperçu du vaisseau survolé
        if self._selectedForPreview:
            self._renderShipPreview(surface, self._selectedForPreview)

        # Instructions
        instructionText = self._font.render(
            "Cliquez sur un vaisseau pour le sélectionner | Échap pour retour",
            True,
            (120, 120, 120)
        )
        instructionRect = instructionText.get_rect(
            center=(surface.get_width() // 2, surface.get_height() - 30)
        )
        surface.blit(instructionText, instructionRect)

    def _renderShipPreview(self, surface, ship):
        """
        Affiche un aperçu des caractéristiques du vaisseau.
        
        Args:
            surface: Surface sur laquelle dessiner
            ship: Vaisseau à afficher
        """
        # Zone d'aperçu sur le côté droit
        previewX = surface.get_width() - 300
        previewY = 200

        # Fond de l'aperçu
        previewRect = pygame.Rect(previewX - 10, previewY - 10, 280, 250)
        pygame.draw.rect(surface, (30, 30, 50), previewRect)
        pygame.draw.rect(surface, (100, 150, 200), previewRect, 2)

        # Nom du vaisseau
        nameText = self._font.render(
            f"{ship.getBrand()} {ship.getName()}",
            True,
            (255, 255, 255)
        )
        surface.blit(nameText, (previewX, previewY))

        # Caractéristiques
        yOffset = previewY + 40
        stats = [
            f"Accélération: {ship.getAcceleration():.0f}",
            f"Vitesse max: {ship.getMaxSpeed():.0f}",
            f"Traînée: {ship.getDrag():.3f}",
            f"Rotation: {ship.getTurnSpeed():.0f}°/s",
        ]

        for stat in stats:
            statText = self._font.render(stat, True, (200, 200, 200))
            surface.blit(statText, (previewX, yOffset))
            yOffset += 25

        # Sprite du vaisseau (réduit)
        spriteScaled = pygame.transform.scale(ship.getSprite(), (80, 80))
        surface.blit(spriteScaled, (previewX + 90, previewY + 140))