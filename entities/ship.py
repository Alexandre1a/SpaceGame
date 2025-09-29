import pygame
import math

class Ship:
    def __init__(self, name, sprite, accel, max_speed, drag, turn_speed):
        self.name = name
        self.sprite = sprite
        self.acceleration = accel
        self.max_speed = max_speed
        self.drag = drag
        self.turn_speed = turn_speed
        self.brake_accel = accel

        # State
        self.pos = pygame.Vector2(0, 0)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 90.0  # 0° → right, 90° → up

    def update(self, dt, inputs):
        keys = inputs
        # Rotation
        if keys[pygame.K_q]: self.angle -= self.turn_speed * dt
        if keys[pygame.K_d]: self.angle += self.turn_speed * dt
        self.angle %= 360

        # Compute forward direction (0° → up)
        rad = math.radians(self.angle - 90)
        forward = pygame.Vector2(math.cos(rad), math.sin(rad))

        # Thrust
        if keys[pygame.K_z]:
            self.vel += forward * self.acceleration * dt

        # Space brake
        if keys[pygame.K_x]:
            speed_sq = self.vel.length_squared()
            if speed_sq > 0:
                old_vel = self.vel.copy()
                brake_dir = -self.vel.normalize()
                self.vel += brake_dir * self.brake_accel * dt
                # prevent reversal
                if self.vel.dot(old_vel) < 0:
                    self.vel = pygame.Vector2(0, 0)

        # Drag ∝ v²
        speed_sq = self.vel.length_squared()
        if self.drag > 0 and speed_sq > 0:
            drag_force = -self.vel.normalize() * (self.drag * speed_sq)
            self.vel += drag_force * dt

        # Cap speed
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # Update position
        self.pos += self.vel * dt

    def render(self, surface, camera_offset, zoom):
        # Screen position
        screen_pos = (self.pos - camera_offset) * zoom
        # Rotate & scale sprite
        img = pygame.transform.rotozoom(self.sprite, -self.angle+90, zoom)
        rect = img.get_rect(center=screen_pos)
        surface.blit(img, rect)