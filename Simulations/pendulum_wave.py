import pygame
import pygame.gfxdraw
import random
import math
import note_play
import os
import util
import config
import palettes
from pendulum import Pendulum
from effects import draw_glow, draw_vignette
from text_overlay import TextOverlay, draw_stat
import hooks


def simulation(output_name="final"):
    pygame.init()

    width, height = config.WIDTH, config.HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, frames_folder, song = util.init_folders(False)

    # Use curated palette (dark bg for best glow look)
    palette = palettes.get_palette()
    while not palettes.is_dark_bg(palette):
        palette = palettes.get_palette()

    background_colour = palette['bg']

    # Create pendulums with slightly different lengths
    num_pendulums = random.randint(15, 20)
    pivot_y = int(height * 0.15)
    min_length = int(height * 0.2)
    max_length = int(height * 0.55)
    start_angle = random.uniform(0.4, 0.8)  # release angle in radians

    # Spread pivots evenly across width
    margin = 80
    spacing = (width - 2 * margin) / (num_pendulums - 1)

    # Colors: gradient from primary to secondary
    pendulums = []
    for i in range(num_pendulums):
        t = i / max(1, num_pendulums - 1)  # 0 to 1
        # Interpolate color from primary to secondary
        c1 = palette['primary']
        c2 = palette['secondary']
        color = (
            int(c1[0] + (c2[0] - c1[0]) * t),
            int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t),
        )
        px = int(margin + i * spacing)
        # Lengths vary slightly so periods differ -> wave patterns
        length = min_length + (max_length - min_length) * (i / max(1, num_pendulums - 1))
        bob_r = random.randint(10, 16)

        p = Pendulum(
            pivot_x=px,
            pivot_y=pivot_y,
            length=length,
            angle=start_angle,
            color=color,
            radius=bob_r,
        )
        pendulums.append(p)

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'pendulum_wave', height)

    running = True
    frame_count = 0
    max_frames = config.MAX_FRAMES
    frames, sounds = [], []
    sound_cooldown = 0

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill(background_colour)

        # Draw pivot bar
        bar_y = pivot_y
        pygame.draw.line(surface, palette['ring'],
                         (margin - 20, bar_y), (width - margin + 20, bar_y), 4)

        # Update and draw pendulums
        for p in pendulums:
            p.update()
            p.draw(surface, glow=True)

        # Draw trail lines connecting all bobs (creates the wave visual)
        if num_pendulums >= 3:
            points = [(int(p.x), int(p.y)) for p in pendulums]
            for i in range(len(points) - 1):
                alpha_color = (*palette['accent'], 80)
                wave_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.aaline(wave_surf, alpha_color, points[i], points[i + 1])
                surface.blit(wave_surf, (0, 0))

        # Sound when pendulums pass through center (angle near 0)
        if sound_cooldown <= 0:
            for p in pendulums:
                if abs(p.angle) < 0.02 and abs(p.angular_vel) > 0.01:
                    sounds.append((note_play.get_sound(notes_folder), frame_count))
                    sound_cooldown = 10
                    break
        else:
            sound_cooldown -= 1

        # Vignette
        draw_vignette(surface)

        # Stat: show elapsed time
        elapsed_sec = frame_count / config.FPS
        draw_stat(surface, f"Time: {elapsed_sec:.1f}s")

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

    pygame.quit()
    print()

    if len(frames) < config.MIN_FRAMES:
        util.clear_folder(frames_folder)
        return False, "fail", "fail"

    title_words = [
        ("mesmerizing", "hypnotic", "satisfying", "synchronized", "harmonic"),
        ("pendulums", "wave", "swing", "oscillation", "rhythm"),
    ]
    title = f"{random.choice(title_words[0])} {random.choice(title_words[1])}"
    description = f"{num_pendulums} pendulums create mesmerizing wave patterns!"

    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
