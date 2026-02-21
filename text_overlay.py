import pygame
from PIL import Image, ImageDraw, ImageFont
import os
import config


def _get_font(size):
    """Load Montserrat Bold font at given size, fallback to default."""
    font_path = config.FONT_PATH
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    # Fallback to default
    try:
        return ImageFont.truetype("arial.ttf", size)
    except (IOError, OSError):
        return ImageFont.load_default()


def render_text(text, size, color=(255, 255, 255), outline_color=(0, 0, 0), outline_width=3):
    """
    Render anti-aliased text with outline using PIL.
    Returns a pygame Surface with alpha.
    """
    font = _get_font(size)
    # Get text bounding box
    bbox = font.getbbox(text)
    text_w = bbox[2] - bbox[0] + outline_width * 2 + 10
    text_h = bbox[3] - bbox[1] + outline_width * 2 + 10

    img = Image.new('RGBA', (text_w, text_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    x = outline_width + 5 - bbox[0]
    y = outline_width + 5 - bbox[1]

    # Draw outline
    if outline_width > 0:
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx * dx + dy * dy <= outline_width * outline_width:
                    draw.text((x + dx, y + dy), text, font=font, fill=(*outline_color, 255))

    # Draw main text
    draw.text((x, y), text, font=font, fill=(*color, 255))

    # Convert PIL Image to pygame Surface
    raw = img.tobytes()
    py_surface = pygame.image.fromstring(raw, img.size, 'RGBA')
    return py_surface


class TextOverlay:
    """Manages text overlays with fade-in/fade-out animations."""

    def __init__(self):
        self.overlays = []

    def add(self, text, size, position, fade_in_start, fade_in_end, fade_out_start, fade_out_end,
            color=(255, 255, 255), outline_color=(0, 0, 0), center_x=True):
        """
        Add a text overlay with timing.
        position: (x, y) - if center_x is True, x is ignored and text is centered.
        """
        surface = render_text(text, size, color, outline_color)
        self.overlays.append({
            'surface': surface,
            'position': position,
            'fade_in_start': fade_in_start,
            'fade_in_end': fade_in_end,
            'fade_out_start': fade_out_start,
            'fade_out_end': fade_out_end,
            'center_x': center_x,
        })

    def draw(self, screen, frame):
        """Draw all active overlays for the current frame."""
        screen_w = screen.get_width()
        for overlay in self.overlays:
            alpha = self._get_alpha(frame, overlay)
            if alpha <= 0:
                continue

            surf = overlay['surface'].copy()
            surf.set_alpha(alpha)

            x, y = overlay['position']
            if overlay['center_x']:
                x = (screen_w - surf.get_width()) // 2

            screen.blit(surf, (x, y))

    def _get_alpha(self, frame, overlay):
        """Calculate alpha based on frame and fade timing."""
        if frame < overlay['fade_in_start']:
            return 0
        elif frame < overlay['fade_in_end']:
            progress = (frame - overlay['fade_in_start']) / max(1, overlay['fade_in_end'] - overlay['fade_in_start'])
            return int(255 * progress)
        elif frame < overlay['fade_out_start']:
            return 255
        elif frame < overlay['fade_out_end']:
            progress = (frame - overlay['fade_out_start']) / max(1, overlay['fade_out_end'] - overlay['fade_out_start'])
            return int(255 * (1 - progress))
        else:
            return 0


def draw_stat(screen, text, size=None):
    """Draw a stat counter in the bottom-left corner."""
    if size is None:
        size = config.FONT_SIZE_SMALL
    surf = render_text(text, size)
    screen.blit(surf, (30, screen.get_height() - surf.get_height() - 30))
