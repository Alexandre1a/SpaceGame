import pygame
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

FONTS = {
    'default': ('Consolas', 18),
}
IMAGES = {
    'gladius': 'gladius.png',
    'eagle':  'ship_eagle.png',
}


def load_fonts():
    fonts = {}
    for key, (name, size) in FONTS.items():
        fonts[key] = pygame.font.SysFont(name, size)
    return fonts


def load_images():
    images = {}
    for key, fname in IMAGES.items():
        path = os.path.join(ASSET_DIR, fname)
        images[key] = pygame.image.load(path).convert_alpha()
    return images