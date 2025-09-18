import pygame
import math
import sys

# -- Configuration de la fenêtre --
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Foule Calme avec Zoom et Planète")
clock = pygame.time.Clock()

# -- Chargement du sprite du vaisseau
ship_image = pygame.image.load("ship.png").convert_alpha()

# -- État du joueur
player_pos   = pygame.Vector2(0, 0)   # coordonnées dans le monde
player_vel   = pygame.Vector2(0, 0)
player_angle = 90                    # en degrés

# -- Paramètres de mouvement
ACCELERATION     = 400.0   # px/s²
BRAKE_ACCELERATION = 800.0  # px/s², à ajuster
MAX_SPEED        = 600.0   # px/s
DRAG_COEFFICIENT = 0
ANGULAR_SPEED    = 180.0   # deg/s

# -- Paramètres de zoom
zoom        = 0.5
ZOOM_SPEED  = 0.001           # change de zoom par seconde
MIN_ZOOM    = 0.01
MAX_ZOOM    = 3.0

# -- Planète statique dans le monde
planet_pos   = pygame.Vector2(400, -200)  # position fixe
planet_radius = 10000                    # rayon en px “monde”
planet_color  = (30, 100, 200)            # bleuâtre

# -- Boucle principale --
running = True
while running:
    dt = clock.tick(120) / 1000.0  # dt en secondes

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
        zoom += ZOOM_SPEED
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        zoom -= ZOOM_SPEED
    zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))

    # Accélération avant/back
    if keys[pygame.K_z]:
        rad = math.radians(player_angle)
        thrust = pygame.Vector2(math.cos(rad), -math.sin(rad))
        player_vel += thrust * ACCELERATION * dt
    if keys[pygame.K_x]:
        # 1) on ne freine que si on a déjà de la vitesse
        speed_sq = player_vel.length_squared()
        if speed_sq > 0.0:
            # 2) direction du frein = opposée à la vélocité
            vel_dir = player_vel.normalize()
            brake_dir = -vel_dir

            # 3) on stocke la vélocité avant freinage
            old_vel = player_vel.copy()

            # 4) on applique le freinage
            player_vel += brake_dir * (BRAKE_ACCELERATION * dt)

            # 5) si on a "inversé" la direction, on stoppe net
            if player_vel.dot(old_vel) < 0:
                player_vel = pygame.Vector2(0, 0)
        

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
    screen.fill((10, 10, 30))  # fond sombre

    # Calcul de l'offset caméra (centrée sur le joueur)
    half_screen = pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) / 2
    camera_offset = player_pos - (half_screen / zoom)

    # 1) Dessiner la planète
    screen_planet_pos = (planet_pos - camera_offset) * zoom
    pygame.draw.circle(
        screen,
        planet_color,
        (int(screen_planet_pos.x), int(screen_planet_pos.y)),
        int(planet_radius * zoom)
    )

    # 2) Dessiner le vaisseau
    screen_pos = (player_pos - camera_offset) * zoom
    rotated_ship = pygame.transform.rotozoom(ship_image, player_angle, zoom)
    ship_rect = rotated_ship.get_rect(center=screen_pos)
    screen.blit(rotated_ship, ship_rect)

    # 3) UI debug
    font = pygame.font.SysFont("Consolas", 18)
    fps_text  = font.render(f"FPS: {clock.get_fps():.1f}", True, (200,200,50))
    zoom_text = font.render(f"Zoom: {zoom:.2f}×", True, (200,200,200))
    speed_text = font.render(f"Speed: {player_vel.length():.1f}", True, (0, 255, 255))
    fps_rect   = fps_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 10, fps_rect.bottom + 5))
    zoom_rect = zoom_text.get_rect(topright=(SCREEN_WIDTH - 10, speed_rect.bottom + 5))
    
    screen.blit(fps_text,   fps_rect)
    screen.blit(speed_text, speed_rect)
    screen.blit(zoom_text, zoom_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()