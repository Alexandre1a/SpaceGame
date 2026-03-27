import pygame

from screens.base_screen import Screen
from ui.button import Button


class ShipSelectionScreen(Screen):
    """
    Display available ships and their stats
    """
    def __init__(self, game, width, height, font, titleFont):
        self._game = game
        self.titleFont = titleFont

        self._font = font
        self._buttons = []
        self.availableShips = game.getAvailableShips()

        startY = 200
        spacing = 80

        for i, ship in enumerate(self.availableShips):
            displayName = f"{ship.getName()}"

            button = Button(
                displayName,
                (width // 2, startY + i * spacing),
                lambda s=ship: self._selectShip(s),
                self._font,
            )
            self._buttons.append(button)

        self._backButton = Button(
            "Retour", (width // 2, height - 80), game.displayMenu, self._font
        )

        self._selectedForPreview = None
    def _selectShip(self, ship):
        self._game.setSelectedShip(ship)
        print(f"[ShipSelection] Vaisseau sélectionné : {ship.getName()}")
        self._game.displayMenu()

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._game.displayMenu()
                return
        for button in self._buttons:
            button.handleEvent(event)

        self._backButton.handleEvent(event)

    def update(self, dt):
        availableShips = self._game.getAvailableShips()
        self._selectedForPreview = None

        for i, button in enumerate(self._buttons):
            if button.isHovered() and i < len(availableShips):
                self._selectedForPreview = availableShips[i]
                break

    def render(self, surface):
        surface.fill((15, 15, 35))

        titleFont = self.titleFont
        titleText = titleFont.render("SÉLECTION DE VAISSEAU", True, (150, 200, 255))
        titleRect = titleText.get_rect(center=(surface.get_width() // 2, 80))
        surface.blit(titleText, titleRect)

        for button in self._buttons:
            button.render(surface)

        self._backButton.render(surface)

        if self._selectedForPreview:
            self._renderShipPreview(surface, self._selectedForPreview)

        instructionText = self._font.render(
            "Cliquez sur un vaisseau pour le sélectionner | Échap pour retour",
            True,
            (120, 120, 120),
        )
        instructionRect = instructionText.get_rect(
            center=(surface.get_width() // 2, surface.get_height() - 30)
        )
        surface.blit(instructionText, instructionRect)

    def _renderShipPreview(self, surface, ship):
        previewX = surface.get_width() - 300
        previewY = 200

        previewRect = pygame.Rect(previewX - 10, previewY - 10, 280, 250)
        pygame.draw.rect(surface, (30, 30, 50), previewRect)
        pygame.draw.rect(surface, (100, 150, 200), previewRect, 2)

        nameText = self._font.render(
            f"{ship.getBrand()} {ship.getName()} Class {ship.getRank()}",
            True,
            (255, 255, 255),
        )
        surface.blit(nameText, (previewX, previewY))

        yOffset = previewY + 40
        stats = [
            f"Accélération: {ship.getAcceleration():.0f}",
            f"Vitesse max: {ship.getMaxSpeed():.0f}",
            f"Rotation: {ship.getTurnSpeed():.0f}°/s",
        ]

        for stat in stats:
            statText = self._font.render(stat, True, (200, 200, 200))
            surface.blit(statText, (previewX, yOffset))
            yOffset += 25

        spriteScaled = pygame.transform.scale(ship.getSprite(), (80, 80))
        surface.blit(spriteScaled, (previewX + 90, previewY + 140))
