import pygame
import random
import math

# ── Caches ────────────────────────────────────────────────────────────────────

_vignette_cache = {}   # (w, h) -> Surface
_glow_cache = {}       # (color, radius, intensity) -> Surface
_flash_cache = {}      # (w, h, alpha) -> Surface

_GLOW_CACHE_LIMIT = 64


def draw_glow(surface, color, pos, radius, intensity=6):
    """Draw a neon glow effect around a position using concentric alpha circles."""
    key = (color[:3], radius, intensity)
    glow_surf = _glow_cache.get(key)
    if glow_surf is None:
        if len(_glow_cache) >= _GLOW_CACHE_LIMIT:
            _glow_cache.pop(next(iter(_glow_cache)))
        glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        glow_surf.fill((0, 0, 0, 0))
        cx, cy = radius * 2, radius * 2
        for i in range(intensity, 0, -1):
            alpha = int(40 * (i / intensity))
            glow_r = int(radius + radius * (intensity - i + 1) * 0.35)
            glow_color = (*color[:3], alpha)
            pygame.draw.circle(glow_surf, glow_color, (cx, cy), glow_r)
        _glow_cache[key] = glow_surf
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


class ParticleSystem:
    """Manages particle bursts for collision effects."""
    def __init__(self):
        self.particles = []
        self._scratch = None   # reusable scratch surface
        self._scratch_size = 0

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
            if p.life <= 0:
                continue
            alpha = int(255 * p.life)
            r = max(1, int(p.radius * p.life))
            size = r * 2
            # Reuse / grow scratch surface
            if self._scratch is None or size > self._scratch_size:
                self._scratch_size = size
                self._scratch = pygame.Surface((size, size), pygame.SRCALPHA)
                self._scratch.fill((0, 0, 0, 0))
            scratch = self._scratch
            if scratch.get_width() < size or scratch.get_height() < size:
                self._scratch_size = size
                self._scratch = pygame.Surface((size, size), pygame.SRCALPHA)
                self._scratch.fill((0, 0, 0, 0))
                scratch = self._scratch
            # Clear only the region we need
            scratch.fill((0, 0, 0, 0), (0, 0, size, size))
            pygame.draw.circle(scratch, (*p.color[:3], alpha), (r, r), r)
            surface.blit(scratch, (int(p.x - r), int(p.y - r)), (0, 0, size, size))


def draw_screen_flash(surface, alpha=180):
    """Draw a white flash overlay on the entire surface."""
    w, h = surface.get_size()
    key = (w, h, alpha)
    flash = _flash_cache.get(key)
    if flash is None:
        flash = pygame.Surface((w, h), pygame.SRCALPHA)
        flash.fill((255, 255, 255, alpha))
        _flash_cache[key] = flash
    surface.blit(flash, (0, 0))


def draw_vignette(surface):
    """Draw a subtle vignette (darkened edges) for cinematic feel."""
    w, h = surface.get_size()
    key = (w, h)
    cached = _vignette_cache.get(key)
    if cached is not None:
        surface.blit(cached, (0, 0))
        return
    vignette = pygame.Surface((w, h), pygame.SRCALPHA)
    bands = 12
    for i in range(bands):
        frac = i / bands
        alpha = int(80 * (frac ** 2))
        if alpha < 2:
            continue
        band_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        band_surf.fill((0, 0, 0, alpha))
        inner_w = int(w * (1 - frac * 0.3))
        inner_h = int(h * (1 - frac * 0.3))
        pygame.draw.ellipse(band_surf, (0, 0, 0, 0),
                            ((w - inner_w) // 2, (h - inner_h) // 2, inner_w, inner_h))
        vignette.blit(band_surf, (0, 0))
    _vignette_cache[key] = vignette
    surface.blit(vignette, (0, 0))
