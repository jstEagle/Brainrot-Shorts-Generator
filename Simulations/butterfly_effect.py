import pygame
import ball as b
import ring as r
import random
import note_play
import os
import util
import config
import palettes
from effects import draw_vignette
from text_overlay import TextOverlay, draw_stat
import hooks


def simulation(output_name="final"):
    pygame.init()

    width, height = config.WIDTH, config.HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, frames_folder, song = util.init_folders(False)

    # Use curated palette
    palette = palettes.get_palette()
    dark_bg = palettes.is_dark_bg(palette)
    background_colour = palette['bg']
    ring_colour = palette['ring']

    # Create a random ring
    ring_x = int(width / 2)
    ring_y = int(height / 2)
    ring_r = random.randint(int(width / 3), int(width / 2))
    ring_width = random.randint(5, 20)
    ring = r.Ring(ring_x, ring_y, ring_r, background_colour, ring_colour, ring_width)

    def create_properties():
        ball_r = random.randint(15, 60)
        ball_properties = {
            'colour': palette['primary'],
            'r': ball_r,
            'x': random.randint(ring_x - ring_r + ball_r * 2, ring_x + ring_r - ball_r * 2),
            'y': random.randint(ring_y - ring_r + ball_r * 2, ring_y),
            'x_vel': random.randint(2, 10),
            'y_vel': random.randint(2, 10),
            'gravity': random.uniform(0.4, 0.7),
            'trail': random.randint(0, 10),
            'fading': random.choice([True, True, True, False]),
            'border': random.choice([True, False, False, False]),
            'efficiency': random.uniform(0.95, 1),
            'friction': random.randint(0, 5),
        }
        return ball_properties

    balls = []
    properties = create_properties()
    while properties['gravity'] + properties['friction'] * (1 / properties['efficiency']) > 7:
        properties = create_properties()

    ball_range = random.randint(10, 50)
    # Generate colors from palette with variance
    colours = palettes.get_similar_colors(palette['primary'], ball_range, variance=40)

    # Escalation: gradually increase gravity over time
    base_gravity = properties['gravity']

    for i in range(ball_range):
        properties['colour'] = colours[i]
        properties['x'] += i / 1000
        properties['y'] += i / 1000
        balls.append(b.Ball(**properties))

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'butterfly_effect', height)

    running = True
    frame_count, max_frames = 0, config.MAX_FRAMES
    frames, sounds = [], []

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill(background_colour)

        ring.draw(surface, glow=dark_bg)

        # Escalation: gradually increase gravity
        gravity_multiplier = 1.0 + (frame_count / max_frames) * 0.5

        for ball in balls:
            ball.gravity = base_gravity * gravity_multiplier
            ball.update()
            ball.draw(surface, glow=dark_bg)
            flag = ball.check_collision_with_ring(ring)
            if flag:
                sounds.append((note_play.get_sound(notes_folder), frame_count))

        # Vignette
        draw_vignette(surface)

        # Stat counter
        draw_stat(surface, f"Balls: {ball_range}")

        # Text overlays
        if frame_count == 0:
            hooks.setup_cta(text_overlay, max_frames, height)
        text_overlay.draw(surface, frame_count)

        # Save the current frame
        frame_path = os.path.join(frames_folder, f'frame_{frame_count:04d}.png')
        pygame.image.save(surface, frame_path)
        util.loading_bar_frames(frame_count, max_frames)

        frame_count += 1
        frames.append(frame_path)

    pygame.quit()
    print()

    butterfly_similes = [
        "fluttering", "delicate", "graceful", "light", "colorful",
        "fragile", "transient", "ethereal", "flitting", "whimsical"
    ]
    effect_similes = [
        "impact", "result", "consequence", "repercussion", "influence",
        "outcome", "reaction", "reverberation", "ripple", "aftershock"
    ]

    title = f"{random.choice(butterfly_similes)} {random.choice(effect_similes)}"
    description = f"{ball_range} balls spawn at almost the same point. Watch what happens!"

    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
