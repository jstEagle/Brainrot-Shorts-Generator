import pygame
import pygame.gfxdraw

pygame.init()

class Ring:
    def __init__(self, x, y, r, background_colour=(250, 250, 250), colour=(80, 80, 80), width=10):
        self.x = x
        self.y = y
        self.r = r
        self.width = width
        self.background = background_colour
        self.colour = colour

    def draw(self, screen, glow=False, glow_color=None):
        # Draw glow around the ring if enabled
        if glow:
            from effects import draw_glow
            color = glow_color if glow_color else self.colour
            draw_glow(screen, color, (self.x, self.y), int(self.r + self.width), intensity=4)

        # Outer circle (ring border)
        r_outer = int(self.r + self.width)
        try:
            pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), r_outer, self.colour)
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), r_outer, self.colour)
        except (ValueError, OverflowError):
            pygame.draw.circle(screen, self.colour, (self.x, self.y), r_outer)

        # Inner circle (background fill)
        r_inner = int(self.r)
        try:
            pygame.gfxdraw.aacircle(screen, int(self.x), int(self.y), r_inner, self.background)
            pygame.gfxdraw.filled_circle(screen, int(self.x), int(self.y), r_inner, self.background)
        except (ValueError, OverflowError):
            pygame.draw.circle(screen, self.background, (self.x, self.y), r_inner)
