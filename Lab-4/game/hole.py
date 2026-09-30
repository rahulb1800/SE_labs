import math
import pygame


class Hole:
    def __init__(self, x, y, radius=50):
        self.x = x
        self.y = y
        self.radius = radius
        self.active = False
        self.spawn_time = 0
        self.up_ms = 0

    def activate(self, now, up_ms):
        self.active = True
        self.spawn_time = now
        self.up_ms = up_ms

    def deactivate(self):
        self.active = False

    def update(self, now):
        if self.active and now - self.spawn_time >= self.up_ms:
            self.deactivate()

    def distance_to(self, pos):
        return math.hypot(pos[0] - self.x, pos[1] - self.y)

    def draw(self, surface):
        # Hole
        pygame.draw.ellipse(
            surface, (60, 40, 20),
            (self.x - self.radius, self.y - self.radius // 2,
             self.radius * 2, self.radius),
        )
        if self.active:
            # Mole body
            pygame.draw.circle(surface, (130, 90, 50), (self.x, self.y - 10), self.radius - 12)
            # Eyes and nose
            pygame.draw.circle(surface, (255, 255, 255), (self.x - 13, self.y - 20), 7)
            pygame.draw.circle(surface, (255, 255, 255), (self.x + 13, self.y - 20), 7)
            pygame.draw.circle(surface, (0, 0, 0), (self.x - 13, self.y - 20), 3)
            pygame.draw.circle(surface, (0, 0, 0), (self.x + 13, self.y - 20), 3)
            pygame.draw.circle(surface, (220, 120, 120), (self.x, self.y - 6), 6)