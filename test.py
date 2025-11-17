import math
import sys

import pygame


class ShipControls:
    def __init__(self):
        self.thrust = False
        self.brake = False
        self.turn_left = False
        self.turn_right = False


class KeyboardController:
    def get_controls(self):
        keys = pygame.key.get_pressed()
        controls = ShipControls()
        controls.thrust = keys[pygame.K_z] or keys[pygame.K_UP]
        controls.brake = keys[pygame.K_x] or keys[pygame.K_DOWN]
        controls.turn_left = keys[pygame.K_q] or keys[pygame.K_LEFT]
        controls.turn_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        return controls


class SimpleAIController:
    """
    Contrôleur IA basique qui poursuit une cible.
    """

    def __init__(self, target_pos):
        self.target_pos = target_pos

    def get_controls(self, ship):
        """
        Calcule les commandes pour diriger le vaisseau vers la cible.
        """
        controls = ShipControls()

        # Calculer la direction vers la cible
        to_target = self.target_pos - ship.pos

        # Si on est proche, on arrête
        if to_target.length() < 50:
            controls.brake = True
            return controls

        # Calculer l'angle vers la cible
        target_angle = math.degrees(math.atan2(to_target.y, to_target.x)) + 90
        target_angle %= 360

        # Calculer la différence d'angle
        angle_diff = (target_angle - ship.angle + 180) % 360 - 180

        # Tourner vers la cible
        if angle_diff < -5:
            controls.turn_left = True
        elif angle_diff > 5:
            controls.turn_right = True

        # Accélérer si on pointe approximativement vers la cible
        if abs(angle_diff) < 30:
            controls.thrust = True

        return controls


class Ship:
    def __init__(self, name, sprite, accel, maxSpeed, drag, turnSpeed):
        self.name = name
        self.sprite = sprite
        self.acceleration = accel
        self.maxSpeed = maxSpeed
        self.drag = drag
        self.turnSpeed = turnSpeed

        # État initial
        self.pos = pygame.Vector2(400, 300)  # Centre de l'écran
        self.vel = pygame.Vector2(0, 0)
        self.angle = 90.0  # Pointé vers le haut

    def update(self, dt, controls):
        # Rotation
        if controls.turn_left:
            self.angle -= self.turnSpeed * dt
        if controls.turn_right:
            self.angle += self.turnSpeed * dt
        self.angle %= 360

        # Direction avant (conversion angle -> vecteur)
        rad = math.radians(self.angle - 90)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))

        # Propulsion
        if controls.thrust:
            self.vel += forward * self.acceleration * dt

        # Freinage
        if controls.brake:
            speed_sq = self.vel.length_squared()
            if speed_sq > 0:
                old_vel = self.vel.copy()
                brake_dir = -self.vel.normalize()
                self.vel += brake_dir * self.acceleration * dt
                # Éviter de reculer
                if self.vel.dot(old_vel) < 0:
                    self.vel = pygame.Vector2(0, 0)

        # Résistance (traînée)
        speed_sq = self.vel.length_squared()
        if self.drag > 0 and speed_sq > 0:
            drag_force = -self.vel.normalize() * (self.drag * speed_sq)
            self.vel += drag_force * dt

        # Limiteur de vitesse
        if self.vel.length() > self.maxSpeed:
            self.vel.scale_to_length(self.maxSpeed)

        # Mise à jour position
        self.pos += self.vel * dt

        # Garder le vaisseau à l'écran
        self.pos.x = self.pos.x % 800
        self.pos.y = self.pos.y % 600

    def render(self, surface):
        # Rotation du sprite
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.angle)
        # Position centrée
        rect = rotated_sprite.get_rect(center=self.pos)
        surface.blit(rotated_sprite, rect)


# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Vaisseau Spatial")
clock = pygame.time.Clock()


# Création du sprite du vaisseau (triangle)
def create_ship_sprite():
    surface = pygame.Surface((30, 40), pygame.SRCALPHA)
    points = [(15, 0), (0, 40), (30, 40)]
    pygame.draw.polygon(surface, (255, 255, 255), points)
    return surface


# Création des objets
ship_sprite = create_ship_sprite()
ship1 = Ship(
    name="Vaisseau",
    sprite=ship_sprite,
    accel=2000,  # Accélération forte
    maxSpeed=145512,  # Vitesse max modérée
    drag=0,  # Faible traînée
    turnSpeed=180,  # Rotation rapide
)

ship2 = Ship(
    name="Vaisseau",
    sprite=ship_sprite,
    accel=2000,  # Accélération forte
    maxSpeed=145512,  # Vitesse max modérée
    drag=0,  # Faible traînée
    turnSpeed=180,  # Rotation rapide
)

controller = KeyboardController()
ai = SimpleAIController(ship1.pos)

# Boucle principale
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta-time en secondes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupération des commandes
    controls = controller.get_controls()
    aiControls = ai.get_controls(ship2)

    # Mise à jour du vaisseau
    ship1.update(dt, controls)
    ship2.update(dt, aiControls)

    # Rendu
    screen.fill((0, 0, 0))
    ship1.render(screen)
    ship2.render(screen)

    # Affichage des informations
    font = pygame.font.Font(None, 36)
    speed_text = font.render(
        f"Vitesse: {ship1.vel.length():.1f}", True, (255, 255, 255)
    )
    angle_text = font.render(f"Angle: {ship1.angle:.1f}°", True, (255, 255, 255))
    screen.blit(speed_text, (10, 10))
    screen.blit(angle_text, (10, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
