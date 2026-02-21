import pygame
import pygame.gfxdraw
import ball as b
import random
import math
import note_play
import os
import util
import config
import palettes
from effects import ParticleSystem, draw_glow, draw_screen_flash, draw_vignette
from text_overlay import TextOverlay, draw_stat
import hooks


class DormantCircle:
    """A dormant colored circle that activates on contact."""
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.active = False
        self.activation_timer = 0
        self.expanding = False
        self.expand_r = 0

    def activate(self):
        if not self.active:
            self.active = True
            self.expanding = True
            self.expand_r = self.r

    def update(self):
        if self.expanding:
            self.expand_r += 2
            self.activation_timer += 1
            if self.activation_timer > 15:
                self.expanding = False

    def draw(self, surface, dark_bg=True):
        if self.active:
            if self.expanding:
                # Glow burst on activation
                if dark_bg:
                    draw_glow(surface, self.color, (int(self.x), int(self.y)), int(self.expand_r), intensity=6)
            try:
                pygame.gfxdraw.aacircle(surface, int(self.x), int(self.y), int(self.r), self.color)
                pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y), int(self.r), self.color)
            except (ValueError, OverflowError):
                pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.r))
        else:
            # Dormant: dim version
            dim = tuple(max(20, c // 4) for c in self.color)
            try:
                pygame.gfxdraw.aacircle(surface, int(self.x), int(self.y), int(self.r), dim)
                pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y), int(self.r), dim)
            except (ValueError, OverflowError):
                pygame.draw.circle(surface, dim, (int(self.x), int(self.y)), int(self.r))


def simulation(output_name="final"):
    pygame.init()

    width, height = config.WIDTH, config.HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, frames_folder, song = util.init_folders(False)

    # Use curated palette
    palette = palettes.get_palette()
    while not palettes.is_dark_bg(palette):
        palette = palettes.get_palette()

    background_colour = palette['bg']
    ball_colour = palette['primary']

    # Create grid of dormant circles
    circle_r = random.randint(18, 28)
    spacing = circle_r * 3
    margin_x = 80
    margin_y = 300  # leave space at top for hook text

    circles = []
    colors = [palette['primary'], palette['secondary'], palette['accent']]
    cols = (width - 2 * margin_x) // spacing
    rows = (height - margin_y - 200) // spacing

    for row in range(rows):
        for col in range(cols):
            cx = margin_x + col * spacing + spacing // 2
            cy = margin_y + row * spacing + spacing // 2
            color = random.choice(colors)
            circles.append(DormantCircle(cx, cy, circle_r, color))

    # Activation radius: how close a neighbor must be to activate
    activation_radius = spacing * 1.3

    # Create the trigger ball
    ball_r = random.randint(12, 20)
    trigger_ball = b.Ball(
        colour=palette['accent'],
        x=width // 2,
        y=50,
        x_vel=random.uniform(-3, 3),
        y_vel=random.uniform(4, 8),
        r=ball_r,
        gravity=0.3,
        trail=20,
        fading=True,
        border=False,
        efficiency=0.95,
        friction=0
    )

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'chain_reaction', height)

    particles = ParticleSystem()

    running = True
    frame_count = 0
    max_frames = config.MAX_FRAMES
    frames, sounds = [], []
    activated_count = 0
    total_circles = len(circles)

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill(background_colour)

        # Update trigger ball
        trigger_ball.update()
        trigger_ball.check_collision_with_border(width, height)

        # Check ball -> dormant circle activation
        for circle in circles:
            if not circle.active:
                dx = trigger_ball.x - circle.x
                dy = trigger_ball.y - circle.y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < trigger_ball.r + circle.r:
                    circle.activate()
                    activated_count += 1
                    particles.emit(int(circle.x), int(circle.y), circle.color, count=8)
                    sounds.append((note_play.get_sound(notes_folder), frame_count))

        # Chain reaction: active circles activate dormant neighbors
        newly_activated = []
        for circle in circles:
            if circle.active and circle.activation_timer <= 3:
                for other in circles:
                    if not other.active:
                        dx = circle.x - other.x
                        dy = circle.y - other.y
                        dist = math.sqrt(dx * dx + dy * dy)
                        if dist < activation_radius:
                            newly_activated.append(other)

        for c in newly_activated:
            if not c.active:
                c.activate()
                activated_count += 1
                particles.emit(int(c.x), int(c.y), c.color, count=6)
                if random.random() < 0.3:
                    sounds.append((note_play.get_sound(notes_folder), frame_count))

        # Update circles
        for circle in circles:
            circle.update()

        # Draw circles
        for circle in circles:
            circle.draw(surface, dark_bg=True)

        # Draw trigger ball
        trigger_ball.draw(surface, glow=True)

        # Particles
        particles.update()
        particles.draw(surface)

        # Flash on mass activation
        if len(newly_activated) > 5:
            draw_screen_flash(surface, alpha=40)

        # Vignette
        draw_vignette(surface)

        # Stat
        pct = int(activated_count / max(1, total_circles) * 100)
        draw_stat(surface, f"Activated: {pct}%")

        # Text overlays
        if frame_count == 0:
            hooks.setup_cta(text_overlay, max_frames, height)
        text_overlay.draw(surface, frame_count)

        # Save frame
        frame_path = os.path.join(frames_folder, f'frame_{frame_count:04d}.png')
        pygame.image.save(surface, frame_path)
        util.loading_bar_frames(frame_count, max_frames)

        frame_count += 1
        frames.append(frame_path)

        # End early if all activated + buffer
        if activated_count >= total_circles:
            # Run for a few more seconds then stop
            end_buffer = 120
            while end_buffer > 0 and frame_count < max_frames:
                surface.fill(background_colour)
                for circle in circles:
                    circle.update()
                    circle.draw(surface, dark_bg=True)
                trigger_ball.update()
                trigger_ball.check_collision_with_border(width, height)
                trigger_ball.draw(surface, glow=True)
                particles.update()
                particles.draw(surface)
                draw_vignette(surface)
                draw_stat(surface, f"Activated: 100%")
                text_overlay.draw(surface, frame_count)
                frame_path = os.path.join(frames_folder, f'frame_{frame_count:04d}.png')
                pygame.image.save(surface, frame_path)
                util.loading_bar_frames(frame_count, max_frames)
                frame_count += 1
                frames.append(frame_path)
                end_buffer -= 1
            break

    pygame.quit()
    print()

    if len(frames) < config.MIN_FRAMES:
        util.clear_folder(frames_folder)
        return False, "fail", "fail"

    title_words = [
        ("chain", "domino", "cascade", "ripple", "viral"),
        ("reaction", "effect", "explosion", "burst", "wave"),
    ]
    title = f"{random.choice(title_words[0])} {random.choice(title_words[1])}"
    description = f"One ball triggers a chain reaction across {total_circles} circles!"

    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
