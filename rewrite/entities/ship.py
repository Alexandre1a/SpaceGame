import pygame
import math


class ShipControls:
    """
    Classe qui représente l'état des commandes pour un vaisseau.
    C'est une structure de données simple qui contient les intentions
    de contrôle, peu importe d'où elles viennent.
    """

    def __init__(self):
        self.thrust = False  # Accélérer vers l'avant
        self.brake = False  # Freiner
        self.turn_left = False  # Tourner à gauche
        self.turn_right = False  # Tourner à droite


class Ship:
    def __init__(self, name, sprite, accel, maxSpeed, drag, turnSpeed):
        """
        Cette classe permet de représenter le vaisseau spacial.
        """
        self.name = name
        self.sprite = sprite
        self.acceleration = accel
        self.maxSpeed = maxSpeed
        # self.drag = drag
        self.turnSpeed = turnSpeed

        # Etat du vaisseau
        self.pos = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 90.0  # 0° -> Droit, 90° -> En Haut

    def update(self, dt, controls):
        """
        Met à jour le vaisseau en fonction des commandes reçues.

        :param dt: Delta time (temps écoulé depuis la dernière frame)
        :param controls: Un objet ShipControls contenant les commandes
        """
        # Rotation
        if controls.turn_left:
            self.angle -= self.turnSpeed * dt
        if controls.turn_right:
            self.angle += self.turnSpeed * dt
        self.angle %= 360

        # Calcul de la direction avant (angle en radians)
        rad = math.radians(self.angle - 90)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))

        # Poussée avant
        if controls.thrust:
            self.vel += forward * self.acceleration * dt

        # Freinage spatial
        if controls.brake:
            speed_sq = self.vel.length_squared()
            if speed_sq > 0:
                old_vel = self.vel.copy()
                brake_dir = -self.vel.normalize()
                self.vel += brake_dir * self.acceleration * dt
                # Éviter l'inversion de direction
                if self.vel.dot(old_vel) < 0:
                    self.vel = pygame.Vector2(0, 0)

        # Traînée proportionnelle à v²
        speed_sq = self.vel.length_squared()
        if self.drag > 0 and speed_sq > 0:
            drag_force = -self.vel.normalize() * (self.drag * speed_sq)
            self.vel += drag_force * dt

        # Limitation de la vitesse maximale
        if self.vel.length() > self.maxSpeed:
            self.vel.scale_to_length(self.maxSpeed)

        # Mise à jour de la position
        self.pos += self.vel * dt

    def render(self, surface, camera_offset, zoom):
        """
        Affiche le vaisseau à l'écran.
        """
        screen_pos = (self.pos - camera_offset) * zoom
        # Tourne et scale le sprite
        img = pygame.transform.rotozoom(self.sprite, -self.angle + 90, zoom)
        rect = img.get_rect(center=screen_pos)
        surface.blit(img, rect)
