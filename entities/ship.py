import math

import pygame


class ShipControls:
    """
    A Class that hold imput states for a ship
    A simple data structure that hold movement intent,
    from wherever they come from
    """

    def __init__(self):
        self.thrust = False
        self.brake = False
        self.turnLeft = False
        self.turnRight = False


# Controllers (IA et Joueur)
class KeyboardController:
    """
    Convert keyboard inputs to ship commands
    This is the keybinds
    """

    def getControls(self):
        """
        Reads keyboard state and returns a ShipControls object
        """
        keys = pygame.key.get_pressed()
        controls = ShipControls()
        controls.thrust = keys[pygame.K_z]
        controls.brake = keys[pygame.K_s]
        controls.turnLeft = keys[pygame.K_q]
        controls.turnRight = keys[pygame.K_d]
        return controls


class SimpleAIController:
    """
    Basic AI who follows a target
    """

    def __init__(self, targetPos):
        self.targetPos = targetPos

    def getControls(self, ship):
        """
        Computes the controls to reach target ship
        """
        controls = ShipControls()

        toTarget = self.targetPos - ship.pos

        if toTarget.length() < 50:
            controls.brake = True
            return controls

        targetAngle = math.degrees(math.atan2(toTarget.y, toTarget.x)) + 90
        targetAngle %= 360
        angleDiff = (targetAngle - ship.angle + 180) % 360 - 180

        if angleDiff < -5:
            controls.turnLeft = True
        elif angleDiff > 5:
            controls.turnRight = True

        if abs(angleDiff) < 30:
            controls.thrust = True

        return controls


class FollowerAIController(SimpleAIController):
    """
    AI that follow a dynamic target,
    we pass the target pos at each frame
    """

    def __init__(self, getTargetCallable):
        """
        getTargetCallable is a function that returns a 2 dimentional Vector
        """
        self.getTarget = getTargetCallable

    def getControls(self, ship):
        self.targetPos = self.getTarget()
        return super().getControls(ship)


class Ship:
    def __init__(self, name, brand, rank, sprite, accel, maxSpeed, drag, turnSpeed):
        """
        This Class represents the SpaceShip
        """
        self.name = name
        self.brand = brand
        self.rank = rank
        self.sprite = sprite
        self.acceleration = accel
        self.maxSpeed = maxSpeed
        self.drag = drag
        self.turnSpeed = turnSpeed
        self.cargo = []

        # The ship default state
        self.pos = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 90.0


    #===========
    #= Getters =
    #===========
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
        Update the ship from controllers inputs
        dt: Delta Time
        controls: A ShipControls object who has the inputs
        """
        if controls.turnLeft:
            self.angle -= self.turnSpeed * dt
        if controls.turnRight:
            self.angle += self.turnSpeed * dt
        self.angle %= 360

        rad = math.radians(self.angle - 90)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))

        if controls.thrust:
            self.vel += forward * self.acceleration * dt

        if controls.brake:
            speedSq = self.vel.length_squared()
            if speedSq > 0:
                oldVel = self.vel.copy()
                brakeDir = -self.vel.normalize()
                self.vel += brakeDir * self.acceleration * dt
                # Prevent direction inversion
                if self.vel.dot(oldVel) < 0:
                    self.vel = pygame.Vector2(0, 0)

        # Drag (not used atm, could be used to simulate atmo)
        speed_sq = self.vel.length_squared()
        if self.drag > 0 and speed_sq > 0:
            drag_force = -self.vel.normalize() * (self.drag * speed_sq)
            self.vel += drag_force * dt

        # Speed Limiter
        if self.vel.length() > self.maxSpeed:
            self.vel.scale_to_length(self.maxSpeed)

        self.pos += self.vel * dt

    def render(self, surface, camera_offset, zoom):
        """
        Display the ship to the screen
        surface: The pygame surface to display to
        camera_offset: the offset of the camera
        zoom: current zoom, used to scale the sprite
        """
        screen_pos = (self.pos - camera_offset) * zoom
        img = pygame.transform.rotozoom(self.sprite, -self.angle + 90, zoom)
        rect = img.get_rect(center=screen_pos)
        surface.blit(img, rect)
