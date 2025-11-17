"""
Module de gestion des ressources du jeu.
Charge et gère les polices, images, sons, etc.
"""

import os

import pygame

from entities.ship import Ship

# Répertoire contenant tous les assets du jeu
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")


# Définition des polices disponibles
FONTS = {
    "default": ("Consolas", 18),
    "title": ("Consolas", 32),
    "small": ("Consolas", 14),
}

# Définition des images à charger
IMAGES = {
    "gladius": "gladius.png",
    "aurora": "aurora.jpg",
    "origin": "Origin.png",
    "600i": "600i.png",
}


def loadFonts():
    """
    Charge toutes les polices définies dans FONTS.

    Returns:
        Dictionnaire {nom: objet pygame.font.Font}
    """
    fonts = {}
    for key, (name, size) in FONTS.items():
        try:
            fonts[key] = pygame.font.SysFont(name, size)
        except Exception as e:
            print(f"[Resources] Erreur lors du chargement de la police '{key}': {e}")
            # Fallback sur une police par défaut
            fonts[key] = pygame.font.Font(None, size)

    print(f"[Resources] {len(fonts)} polices chargées")
    return fonts


def loadImages():
    """
    Charge toutes les images définies dans IMAGES.

    Returns:
        Dictionnaire {nom: objet pygame.Surface}
    """
    success = 0
    images = {}
    for key, filename in IMAGES.items():
        path = os.path.join(ASSET_DIR, filename)
        try:
            images[key] = pygame.image.load(path).convert_alpha()
            print(f"[Resources] Image chargée : {key} ({filename})")
            success += 1
        except Exception as e:
            print(f"[Resources] Erreur lors du chargement de '{filename}': {e}")
            # Créer une image de remplacement (carré rouge)
            images[key] = createPlaceholderImage()

    print(f"[Resources] {success} images chargées")
    return images


def createPlaceholderImage(size=(64, 64), color=(255, 0, 255)):
    """
    Crée une image de remplacement pour les assets manquants.

    Args:
        size: Tuple (largeur, hauteur) de l'image
        color: Couleur RGB de l'image

    Returns:
        Surface pygame remplie de la couleur spécifiée
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface


def getAssetPath(filename):
    """
    Retourne le chemin complet d'un fichier asset.

    Args:
        filename: Nom du fichier dans le dossier assets

    Returns:
        Chemin complet vers le fichier
    """
    return os.path.join(ASSET_DIR, filename)
