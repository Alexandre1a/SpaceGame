import os

import pygame

from entities.ship import Ship

# Directories containing all game assets
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
MUSIC_DIR = os.path.join(os.path.dirname(__file__), "music")


# All fonts available in the game
FONTS = {
    "default": ("Consolas", 18),
    "title": ("Consolas", 32),
    "small": ("Consolas", 14),
}

# All sprites available in the game
IMAGES = {
    "gladius": "gladius.png",
    "origin": "Origin.png",
    "600i": "600i.png",
}

# All music available in the game
MUSIC = {
  "menu": "menu.ogg",
  "main": "main.wav",
}


def loadFonts():
    """
    Loads all fonts defined in "FONTS"

    Returns:
        Dict {name: object pygame.font.Font}
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
    Loads all sprites defined in "IMAGES"

    Returns:
        Dict {name: object pygame.Surface}
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
            images[key] = createPlaceholderImage()

    print(f"[Resources] {success} images chargées")
    return images


def createPlaceholderImage(size=(64, 64), color=(255, 0, 255)):
    """
    Creates  a placeholder image for missing sprites

    Args:
        size: Tuple (witdh, height) of the image
        color: RGB color of the image

    Returns:
      A pygame surface filled with the specified color
    """
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface

def getMusicPath(filename):
  """
  Returns the full path of a music file.
  Args:
    filename: Name of the file in the assets folder

  Returns:
    The full path of the music file
  """
  return os.path.join(MUSIC_DIR, filename)

def getAssetPath(filename):
    """
    Returns the full path of an asset file

    Args:
        filename: Name of the file in the assets folder

    Returns:
        The full path of the file
    """
    return os.path.join(ASSET_DIR, filename)
