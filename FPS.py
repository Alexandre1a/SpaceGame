import pygame
import time
pygame.init()

# Configuration de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Foule Calme")

# Horloge et delta time
clock = pygame.time.Clock()
dt = 0

# Police pour debug
font = pygame.font.SysFont("Consolas", 20)

# Position et vélocité du joueur
player_pos   = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
player_vel   = pygame.Vector2(0, 0)
acceleration = 400.0     # pixels/s²
max_speed    = 600.0     # pixels/s
friction     = 1      # coefficient de décélération (0.0–1.0)

running = True
while running:
    # --- Gestion des événements --------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouse = pygame.mouse.get_pressed(num_buttons=3)
        
    # --- Entrées clavier ---------------------------------
    keys = pygame.key.get_pressed()
    move = pygame.Vector2(0, 0)
    if keys[pygame.K_z]:
        move.y = -1
    if keys[pygame.K_s]:
        move.y = +1
    if keys[pygame.K_q]:
        move.x = -1
    if keys[pygame.K_d]:
        move.x = +1
    if keys[pygame.K_x]:
        print('ToDo : Deceleration')
    if keys[pygame.K_RETURN]:
        break
    # --- Entrée Souris ----------------------------------
    if mouse[0]:
        time.sleep(0.1)
        print("Something")
    # Si on bouge, appliquer l'accélération
    if move.length_squared() > 0:
        move = move.normalize()
        player_vel += move * acceleration * dt
        # Limiter la vitesse
        if player_vel.length() > max_speed:
            player_vel = player_vel.normalize() * max_speed
    else:
        # Sinon appliquer la friction
        player_vel *= friction

    # Mettre à jour la position
    player_pos += player_vel * dt

    # --- Rendu -------------------------------------------
    screen.fill("white")
    pygame.draw.circle(screen, "red", player_pos, 40)

    # Affichage debug : FPS et vitesse
    fps = clock.get_fps()
    fps_text   = font.render(f"FPS: {fps:.1f}", True, (255, 255,   0))
    speed_text = font.render(f"Speed: {player_vel.length():.1f}", True, (0, 255, 255))
    fps_rect   = fps_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 10, fps_rect.bottom + 5))
    screen.blit(fps_text,   fps_rect)
    screen.blit(speed_text, speed_rect)

    pygame.display.flip()

    # --- Tick ---------------------------------------------
    dt = clock.tick(300) / 1000.0  # limiter à 60 FPS, obtenir dt en secondes

pygame.quit()