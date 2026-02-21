import pygame
import pygame.gfxdraw
import math


class Pendulum:
    """Simple pendulum with adjustable length for pendulum wave simulation."""

    def __init__(self, pivot_x, pivot_y, length, angle, color, radius=8):
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.length = length
        self.angle = angle  # in radians
        self.angular_vel = 0.0
        self.color = color
        self.radius = radius
        self.gravity = 0.4  # effective gravity for visual appeal

    @property
    def x(self):
        return self.pivot_x + self.length * math.sin(self.angle)

    @property
    def y(self):
        return self.pivot_y + self.length * math.cos(self.angle)

    def update(self, dt=1.0):
        """Update pendulum using simple pendulum equation: a = -(g/L) * sin(theta)."""
        angular_acc = -(self.gravity / self.length) * math.sin(self.angle)
        self.angular_vel += angular_acc * dt
        self.angular_vel *= 0.999  # tiny damping for stability
        self.angle += self.angular_vel * dt

    def draw(self, screen, glow=False):
        """Draw the pendulum arm and bob with anti-aliasing."""
        bx, by = int(self.x), int(self.y)
        px, py = int(self.pivot_x), int(self.pivot_y)

        # Draw arm
        pygame.draw.aaline(screen, self.color, (px, py), (bx, by))

        # Draw glow on bob
        if glow:
            from effects import draw_glow
            draw_glow(screen, self.color, (bx, by), self.radius)

        # Draw bob (anti-aliased)
        try:
            pygame.gfxdraw.aacircle(screen, bx, by, self.radius, self.color)
            pygame.gfxdraw.filled_circle(screen, bx, by, self.radius, self.color)
        except (ValueError, OverflowError):
            pygame.draw.circle(screen, self.color, (bx, by), self.radius)
