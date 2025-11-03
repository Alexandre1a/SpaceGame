"""
Module pour les boutons d'interface utilisateur.
Gère l'affichage et les interactions avec les boutons cliquables.
"""

import pygame


class Button:
    """
    Bouton cliquable pour l'interface utilisateur.
    Change de couleur au survol et exécute une fonction callback au clic.
    """

    def __init__(self, text, centerPos, callback, font,
                 padding=(10, 5), idleColor=(200, 200, 200),
                 hoverColor=(255, 255, 255), textColor=(0, 0, 0)):
        """
        Initialise un bouton.
        
        Args:
            text: Texte affiché sur le bouton
            centerPos: Position du centre du bouton (tuple x, y)
            callback: Fonction à appeler lors du clic
            font: Police pygame pour le texte
            padding: Espacement autour du texte (tuple horizontal, vertical)
            idleColor: Couleur du bouton au repos
            hoverColor: Couleur du bouton au survol
            textColor: Couleur du texte
        """
        self._text = text
        self._callback = callback
        self._font = font
        self._padding = padding
        self._idleColor = idleColor
        self._hoverColor = hoverColor
        self._textColor = textColor

        # Rendu du texte
        self._textSurface = self._font.render(self._text, True, self._textColor)

        # Calcul du rectangle avec padding
        width = self._textSurface.get_width() + padding[0] * 2
        height = self._textSurface.get_height() + padding[1] * 2
        self._rect = pygame.Rect(0, 0, width, height)
        self._rect.center = centerPos

    # ==================== GETTERS ====================

    def getText(self):
        """Retourne le texte du bouton"""
        return self._text

    def getRect(self):
        """Retourne le rectangle du bouton"""
        return self._rect

    def getPosition(self):
        """Retourne la position du centre du bouton"""
        return self._rect.center

    # ==================== SETTERS ====================

    def setText(self, text):
        """
        Change le texte du bouton et recalcule sa taille.
        
        Args:
            text: Nouveau texte à afficher
        """
        self._text = text
        self._textSurface = self._font.render(self._text, True, self._textColor)
        
        # Recalculer la taille du bouton
        oldCenter = self._rect.center
        width = self._textSurface.get_width() + self._padding[0] * 2
        height = self._textSurface.get_height() + self._padding[1] * 2
        self._rect = pygame.Rect(0, 0, width, height)
        self._rect.center = oldCenter

    def setPosition(self, centerPos):
        """
        Change la position du bouton.
        
        Args:
            centerPos: Nouvelle position du centre (tuple x, y)
        """
        self._rect.center = centerPos

    def setCallback(self, callback):
        """
        Change la fonction callback du bouton.
        
        Args:
            callback: Nouvelle fonction à appeler au clic
        """
        self._callback = callback

    # ==================== GESTION DES ÉVÉNEMENTS ====================

    def handleEvent(self, event):
        """
        Gère les événements pour ce bouton.
        
        Args:
            event: Événement pygame à traiter
        """
        # Détection du clic gauche sur le bouton
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                self._onClick()

    def _onClick(self):
        """Méthode interne appelée lors du clic sur le bouton"""
        if self._callback:
            try:
                self._callback()
            except Exception as e:
                print(f"[Button] Erreur lors de l'exécution du callback : {e}")

    # ==================== RENDU ====================

    def render(self, surface):
        """
        Affiche le bouton à l'écran.
        
        Args:
            surface: Surface pygame sur laquelle dessiner
        """
        # Déterminer la couleur en fonction du survol
        mousePos = pygame.mouse.get_pos()
        isHovered = self._rect.collidepoint(mousePos)
        color = self._hoverColor if isHovered else self._idleColor

        # Dessiner le rectangle du bouton
        pygame.draw.rect(surface, color, self._rect)

        # Dessiner une bordure légèrement plus sombre
        borderColor = tuple(max(0, c - 50) for c in color)
        pygame.draw.rect(surface, borderColor, self._rect, 2)

        # Afficher le texte centré
        textPos = (
            self._rect.x + self._padding[0],
            self._rect.y + self._padding[1]
        )
        surface.blit(self._textSurface, textPos)

    def isHovered(self):
        """
        Vérifie si la souris survole le bouton.
        
        Returns:
            True si la souris est sur le bouton, False sinon
        """
        mousePos = pygame.mouse.get_pos()
        return self._rect.collidepoint(mousePos)