import pygame
import ball as b
import random
import note_play
import os
import util
import math
import config
import palettes
from effects import ParticleSystem, draw_vignette
from text_overlay import TextOverlay, draw_stat
import hooks


def simulation(output_name="final"):
    pygame.init()

    width, height = config.HALF_WIDTH, config.HALF_HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, frames_folder, song = util.init_folders(False)

    # Use curated palette
    palette = palettes.get_palette()
    dark_bg = palettes.is_dark_bg(palette)
    background_colour = palette['bg']

    ball_colour = palette['primary']
    fading = random.choice([True, True, True, False])
    border = random.choice([True, False, False, False])
    gravity = random.uniform(0.5, 1)
    friction = random.randint(0, 5)
    ball_r = random.randint(10, 30)

    def create_properties():
        ball_properties = {
            'colour': ball_colour,
            'r': ball_r,
            'x': random.randint(ball_r * 3, width - ball_r * 3),
            'y': random.randint(ball_r * 3, height - ball_r * 3),
            'x_vel': random.randint(3, 10),
            'y_vel': random.randint(1, 5),
            'gravity': gravity,
            'trail': random.randint(0, 10),
            'fading': fading,
            'border': border,
            'efficiency': 0.9,
            'friction': friction,
        }
        return ball_properties

    balls = []
    properties = create_properties()
    while properties['gravity'] + properties['friction'] * (1 / properties['efficiency']) > 7:
        properties = create_properties()

    def new_ball():
        x = random.randint(properties['r'] + 1, width - properties['r'] - 1)
        y = properties['r'] + 10
        flag = True
        iterations = 20

        while flag and iterations > 0:
            iterations -= 1
            flag = False
            for ball in balls:
                dx = ball.x - x
                dy = ball.y - y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance <= ball.r:
                    flag = True
                    x = random.randint(properties['r'] + 1, width - properties['r'] - 1)

        if iterations > 0:
            properties['x'] = x
            properties['y'] = y
            # Use palette colors with variance
            properties['colour'] = random.choice([palette['primary'], palette['secondary'], palette['accent']])
            balls.append(b.Ball(**properties))

    new_ball()
    new_ball()

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'duplicating_balls', height)

    particles = ParticleSystem()

    running = True
    max_balls = int((height / ball_r) * (width / ball_r) * 0.2)
    frame_count, max_frames, end_frames = 0, config.MAX_FRAMES, config.END_FRAMES
    frames, sounds = [], []
    max_bounces = random.randint(4, 10)
    original_max = max_bounces

    while running and frame_count < max_frames and end_frames > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill(background_colour)
        ball_flag = False
        frame_sounds = []

        for ball in balls:
            flag = False
            other_flag = False
            ball.update()
            ball.draw(surface, glow=dark_bg)
            flag = ball.check_collision_with_border(width, height)
            for other in balls:
                if other is not ball:
                    other_flag = ball.check_collision_with_ball(other)
                    if len(balls) <= max_balls and other_flag and (ball.bounces % max_bounces == 0 or len(balls) <= 2):
                        ball_flag = True
                        particles.emit(int(ball.x), int(ball.y), ball.colour, count=8)

            if flag or other_flag and len(frame_sounds) < 2 and (ball.x_vel > 1 or ball.y_vel > 1):
                frame_sounds.append((note_play.get_sound(notes_folder) if not song else note_play.get_next_note(), frame_count))

        if len(balls) >= max_balls:
            end_frames -= 1

        if ball_flag:
            new_ball()

        sounds = sounds + frame_sounds

        # Particles
        particles.update()
        particles.draw(surface)

        # Vignette
        draw_vignette(surface)

        # Stat counter
        draw_stat(surface, f"Balls: {len(balls)}")

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
    if len(frames) < config.MIN_FRAMES or len(balls) <= 2:
        util.clear_folder(frames_folder)
        if song:
            util.clear_folder(notes_folder)
            note_play.init()
        return False, "fail", "fail"

    duplicating_similes = [
        "replicating", "copying", "cloning", "reproducing", "mirroring",
        "imitating", "doubling", "multiplying", "echoing", "matching"
    ]
    balls_similes = [
        "spheres", "orbs", "globes", "bubbles", "marbles",
        "pellets", "beads", "bulbs", "pucks", "cylinders"
    ]

    title = f"{random.choice(duplicating_similes)} {random.choice(balls_similes)}"
    description = f"Every {original_max} bounces with another ball. A new ball spawns"

    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
