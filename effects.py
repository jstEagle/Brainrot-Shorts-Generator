import pygame
import random
import math


def draw_glow(surface, color, pos, radius, intensity=6):
    """Draw a neon glow effect around a position using concentric alpha circles."""
    glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    cx, cy = radius * 2, radius * 2
    for i in range(intensity, 0, -1):
        alpha = int(40 * (i / intensity))
        glow_r = int(radius + radius * (intensity - i + 1) * 0.35)
        glow_color = (*color[:3], alpha)
        pygame.draw.circle(glow_surf, glow_color, (cx, cy), glow_r)
    surface.blit(glow_surf, (int(pos[0] - radius * 2), int(pos[1] - radius * 2)))


class Particle:
    """A single particle for burst effects."""
    def __init__(self, x, y, color):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.radius = random.uniform(2, 5)
        self.life = 1.0  # 1.0 = full, 0.0 = dead
        self.decay = random.uniform(0.02, 0.05)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.96
        self.vy *= 0.96
        self.life -= self.decay

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = int(255 * self.life)
        r = max(1, int(self.radius * self.life))
        particle_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, (*self.color[:3], alpha), (r, r), r)
        surface.blit(particle_surf, (int(self.x - r), int(self.y - r)))


class ParticleSystem:
    """Manages particle bursts for collision effects."""
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10):
        """Emit a burst of particles at position."""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


def draw_screen_flash(surface, alpha=180):
    """Draw a white flash overlay on the entire surface."""
    flash = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    flash.fill((255, 255, 255, alpha))
    surface.blit(flash, (0, 0))


def draw_vignette(surface):
    """Draw a subtle vignette (darkened edges) for cinematic feel."""
    w, h = surface.get_size()
    vignette = pygame.Surface((w, h), pygame.SRCALPHA)
    max_dist = math.sqrt((w / 2) ** 2 + (h / 2) ** 2)
    # Only draw a few bands for performance
    bands = 12
    for i in range(bands):
        frac = i / bands
        # Outer bands get darker
        alpha = int(80 * (frac ** 2))
        if alpha < 2:
            continue
        # Draw as a filled rect with a transparent center hole
        band_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        band_surf.fill((0, 0, 0, alpha))
        # Cut out a centered ellipse
        inner_w = int(w * (1 - frac * 0.3))
        inner_h = int(h * (1 - frac * 0.3))
        pygame.draw.ellipse(band_surf, (0, 0, 0, 0),
                            ((w - inner_w) // 2, (h - inner_h) // 2, inner_w, inner_h))
        vignette.blit(band_surf, (0, 0))
    surface.blit(vignette, (0, 0))
