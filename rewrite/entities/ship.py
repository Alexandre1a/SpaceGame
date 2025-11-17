import math

import pygame


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


# Controllers (IA et Joueur)
class KeyboardController:
    """Convertit les entrées clavier en commandes de vaisseau."""

    def getControls(self):
        """
        Lit l'état du clavier et retourne un objet ShipControls.
        """
        keys = pygame.key.get_pressed()
        controls = ShipControls()
        controls.thrust = keys[pygame.K_z]
        controls.brake = keys[pygame.K_x]
        controls.turn_left = keys[pygame.K_q]
        controls.turn_right = keys[pygame.K_d]
        return controls


class SimpleAIController:
    """
    Contrôleur IA basique qui poursuit une cible.
    """

    def __init__(self, target_pos):
        self.target_pos = target_pos

    def getControls(self, ship):
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


class FollowerAIController(SimpleAIController):
    """IA qui suit une cible dynamique (le joueur) — on passe la target_pos chaque frame."""

    def __init__(self, get_target_callable):
        # get_target_callable: function returning Vector2
        self.get_target = get_target_callable

    def getControls(self, ship):
        self.target_pos = self.get_target()
        return super().getControls(ship)


class Ship:
    def __init__(self, name, brand, rank, sprite, accel, maxSpeed, drag, turnSpeed):
        """
        Cette classe permet de représenter le vaisseau spacial.
        """
        self.name = name
        self.brand = brand
        self.rank = rank
        self.sprite = sprite
        self.acceleration = accel
        self.maxSpeed = maxSpeed
        self.drag = drag
        self.turnSpeed = turnSpeed

        # Etat du vaisseau
        self.pos = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 90.0  # 0° -> Droit, 90° -> En Haut

    def getName(self):
        return self.name

    def getBrand(self):
        return self.brand

    def getRank(self):
        return self.rank

    def getAcceleration(self):
        return self.acceleration

    def getMaxSpeed(self):
        return self.maxSpeed

    def getTurnSpeed(self):
        return self.turnSpeed

    def getSprite(self):
        return self.sprite

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
