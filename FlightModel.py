import pygame
import math
import sys

# -- Configuration de la fenêtre --
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Limited Sky")

# Horloge et delta
clock = pygame.time.Clock()
dt = 0

# Couleurs
background_color = "white"

# Police de debug
font = pygame.font.SysFont("Consolas", 20)

# -- Chargement du sprite du vaisseau (doit pointer vers votre fichier) --
ship_image = pygame.image.load("./assets/ships/Gladius_pixel.png").convert_alpha()

# -- État du joueur --
player_pos   = pygame.Vector2(0, 0)   # coordonnées dans le « monde »
player_vel   = pygame.Vector2(0, 0)
player_angle = 0.0                    # en degrés

# -- Paramètres de mouvement --
ACCELERATION     = 400.0   # px/s²
MAX_SPEED        = 600.0   # px/s
DRAG_COEFFICIENT = 1 # 0.5
ANGULAR_SPEED    = 180.0   # deg/s

# -- Paramètres de zoom --
zoom        = 1.5
ZOOM_SPEED  = 1.0           # change de zoom par seconde
MIN_ZOOM    = 0.001
MAX_ZOOM    = 3.0

# -- Boucle principale --
running = True
while running:
    dt = clock.tick(60) / 1000.0  # dt en secondes

    # ----- Gérer les événements -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- Input clavier -----
    keys = pygame.key.get_pressed()

    # Rotation du vaisseau
    if keys[pygame.K_q]:
        player_angle += ANGULAR_SPEED * dt
    if keys[pygame.K_d]:
        player_angle -= ANGULAR_SPEED * dt
    player_angle %= 360

    # Zoom / dézoom
    if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
        zoom += ZOOM_SPEED * dt
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        zoom -= ZOOM_SPEED * dt
    zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))

    # Accélération avant/back
    if keys[pygame.K_z]:
        rad = math.radians(player_angle)
        thrust = pygame.Vector2(math.cos(rad), -math.sin(rad))
        player_vel += thrust * ACCELERATION * dt
    if keys[pygame.K_s]:
        # marche arrière à demi-puissance
        rad = math.radians(player_angle)
        thrust = pygame.Vector2(-math.cos(rad), math.sin(rad))
        player_vel += thrust * (ACCELERATION * 0.5) * dt

    # Traînée proportionnelle à v²
    speed_sq = player_vel.length_squared()
    if speed_sq > 0:
        drag = -player_vel.normalize() * (DRAG_COEFFICIENT * speed_sq)
        player_vel += drag * dt

    # Limiter la vitesse
    if player_vel.length() > MAX_SPEED:
        player_vel.scale_to_length(MAX_SPEED)

    # Mise à jour de la position dans le monde
    player_pos += player_vel * dt

    # ----- Rendu -----
    screen.fill(background_color)

    # Calcul de l'offset caméra (centrée sur le joueur)
    half_screen = pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) / 2
    camera_offset = player_pos - (half_screen / zoom)

    # Position écran du joueur
    screen_pos = (player_pos - camera_offset) * zoom

    # Dessin du sprite zoomé et tourné
    rotated_ship = pygame.transform.rotozoom(ship_image, player_angle, zoom)
    ship_rect = rotated_ship.get_rect(center=screen_pos)
    screen.blit(rotated_ship, ship_rect)

    # Afficher quelques infos (FPS et zoom)
    fps = clock.get_fps()
    fps_text   = font.render(f"FPS: {fps:.1f}", True, (255, 255,   0))
    speed_text = font.render(f"Speed: {player_vel.length():.1f}", True, (0, 255, 255))
    zoom_text = font.render(f"Zoom: {zoom:.2f}×", True, (0, 255, 255))
    fps_rect   = fps_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 10, fps_rect.bottom + 5))
    zoom_rect = zoom_text.get_rect(topright=(SCREEN_WIDTH - 10, speed_rect.bottom + 5))
    screen.blit(fps_text,   fps_rect)
    screen.blit(speed_text, speed_rect)
    screen.blit(zoom_text, zoom_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
