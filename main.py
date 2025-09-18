import math
import random
import re

import pygame
pygame.init()

colors = [
    name for name in pygame.color.THECOLORS
    # avoid hard to see colors
    if re.search('(red|green|blue)', name)
]


def random_sprite(inside, min_size=(100,100), max_size=(200,200)):
    min_width, min_height = min_size
    max_width, max_height = max_size
    sprite = pygame.sprite.Sprite()
    size = (
        random.randint(min_width,max_width),
        random.randint(min_height,max_height)
    )
    position = (
        random.randint(0, inside.width - size[0]),
        random.randint(0, inside.height - size[1])
    )
    sprite.rect = pygame.Rect(position, size)
    color = random.choice(colors)
    sprite.image = pygame.Surface(sprite.rect.size)
    sprite.image.fill(color)
    return sprite

window = pygame.display.set_mode((800,)*2)
frame = window.get_rect()
camera = frame.copy()
space = frame.inflate(frame.width*2, frame.height*2)

sprites = [random_sprite(space) for _ in range(100)]
player = pygame.image.load("./assets/ships/aurora.jpg")
speed = 5
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
while running:
    elapsed = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player.rect.y -= speed
    if pressed[pygame.K_RIGHT]:
        player.rect.x += speed
    if pressed[pygame.K_DOWN]:
        player.rect.y += speed
    if pressed[pygame.K_LEFT]:
        player.rect.x -= speed
    camera.center = player.rect.center
    # draw
    window.fill((0,)*3)
    for sprite in sprites:
        window.blit(sprite.image, (sprite.rect.x - camera.x, sprite.rect.y - camera.y))
    pygame.display.flip()

pygame.quit()
