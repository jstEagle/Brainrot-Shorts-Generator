import random

# Curated color palettes optimized for phone screens (high contrast, neon-on-dark)
# Each palette: bg, primary, secondary, accent, ring
PALETTES = [
    {
        'name': 'neon_blue',
        'bg': (10, 10, 30),
        'primary': (0, 180, 255),
        'secondary': (0, 255, 200),
        'accent': (255, 100, 200),
        'ring': (40, 40, 80),
    },
    {
        'name': 'neon_pink',
        'bg': (15, 5, 20),
        'primary': (255, 50, 150),
        'secondary': (255, 150, 50),
        'accent': (200, 50, 255),
        'ring': (60, 20, 60),
    },
    {
        'name': 'electric_green',
        'bg': (5, 15, 10),
        'primary': (50, 255, 100),
        'secondary': (100, 200, 255),
        'accent': (255, 255, 50),
        'ring': (20, 50, 30),
    },
    {
        'name': 'sunset',
        'bg': (20, 10, 5),
        'primary': (255, 120, 30),
        'secondary': (255, 50, 80),
        'accent': (255, 220, 50),
        'ring': (60, 30, 15),
    },
    {
        'name': 'cyber_purple',
        'bg': (12, 5, 25),
        'primary': (180, 50, 255),
        'secondary': (50, 200, 255),
        'accent': (255, 80, 180),
        'ring': (40, 15, 60),
    },
    {
        'name': 'ice',
        'bg': (5, 10, 20),
        'primary': (150, 220, 255),
        'secondary': (200, 255, 255),
        'accent': (100, 150, 255),
        'ring': (30, 40, 60),
    },
    {
        'name': 'fire',
        'bg': (20, 5, 0),
        'primary': (255, 80, 20),
        'secondary': (255, 200, 0),
        'accent': (255, 30, 30),
        'ring': (50, 20, 10),
    },
    {
        'name': 'ocean',
        'bg': (5, 10, 25),
        'primary': (0, 150, 200),
        'secondary': (0, 220, 180),
        'accent': (50, 100, 255),
        'ring': (15, 30, 55),
    },
    {
        'name': 'toxic',
        'bg': (5, 15, 5),
        'primary': (100, 255, 0),
        'secondary': (200, 255, 50),
        'accent': (0, 255, 150),
        'ring': (20, 40, 10),
    },
    {
        'name': 'gold',
        'bg': (15, 10, 5),
        'primary': (255, 200, 50),
        'secondary': (255, 150, 30),
        'accent': (255, 255, 150),
        'ring': (50, 35, 15),
    },
    {
        'name': 'aurora',
        'bg': (5, 10, 15),
        'primary': (50, 255, 150),
        'secondary': (150, 50, 255),
        'accent': (50, 200, 255),
        'ring': (15, 30, 40),
    },
    {
        'name': 'cherry',
        'bg': (20, 5, 10),
        'primary': (255, 30, 80),
        'secondary': (255, 100, 150),
        'accent': (255, 200, 220),
        'ring': (50, 15, 25),
    },
    {
        'name': 'pastel_dark',
        'bg': (20, 20, 30),
        'primary': (200, 150, 255),
        'secondary': (150, 220, 200),
        'accent': (255, 180, 200),
        'ring': (50, 50, 70),
    },
    {
        'name': 'white_clean',
        'bg': (240, 240, 245),
        'primary': (30, 30, 60),
        'secondary': (60, 60, 120),
        'accent': (255, 80, 80),
        'ring': (180, 180, 200),
    },
]


def get_palette():
    """Return a random curated palette."""
    return random.choice(PALETTES)


def is_dark_bg(palette):
    """Check if the palette has a dark background (for glow effects)."""
    bg = palette['bg']
    return (bg[0] + bg[1] + bg[2]) / 3 < 80


def get_similar_colors(base_color, count, variance=30):
    """Generate similar colors based on a base color with controlled variance."""
    colors = []
    for _ in range(count):
        r = max(0, min(255, base_color[0] + random.randint(-variance, variance)))
        g = max(0, min(255, base_color[1] + random.randint(-variance, variance)))
        b = max(0, min(255, base_color[2] + random.randint(-variance, variance)))
        colors.append((r, g, b))
    return colors
