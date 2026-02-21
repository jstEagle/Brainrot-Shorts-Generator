import pygame
import ball as b
import ring as r
import random
import note_play
import os
import util
import config
import palettes
from effects import ParticleSystem, draw_vignette
from text_overlay import TextOverlay, draw_stat
import hooks


def simulation(output_name="final"):
    pygame.init()

    width, height = config.WIDTH, config.HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, frames_folder, song = util.init_folders(True)

    # Use curated palette
    palette = palettes.get_palette()
    dark_bg = palettes.is_dark_bg(palette)
    background_colour = palette['bg']
    ball_colour = palette['primary']
    ring_colour = palette['ring']

    # Create a random ring
    ring_x = int(width / 2)
    ring_y = int(height / 2)
    ring_r = random.randint(int(width / 3), int(width / 2))
    ring_width = random.randint(5, 20)
    ring = r.Ring(ring_x, ring_y, ring_r, background_colour, ring_colour, ring_width)

    def create_properties():
        ball_r = random.randint(10, 50)
        ball_trail = random.randint(0, 30)

        ball_properties = {
            'colour': ball_colour,
            'r': ball_r,
            'x': random.randint(ring_x - ring_r + ball_r, ring_x + ring_r - ball_r),
            'y': random.randint(ring_y - ring_r + ball_r, ring_y),
            'x_vel': random.randint(2, 10),
            'y_vel': random.randint(2, 10),
            'gravity': random.uniform(0.2, 0.6),
            'trail': ball_trail,
            'fading': True,
            'border': random.choice([True, True, False]),
            'efficiency': random.uniform(0.8, 1.1),
            'friction': random.randint(0, 5),
        }
        return ball_properties

    properties = create_properties()
    current_ball = b.Ball(**properties)

    print("Bounce countdown")
    print()

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'bounce_countdown', height)

    particles = ParticleSystem()

    running = True
    frame_count, max_frames = 0, config.MAX_FRAMES
    max_bounces = random.randint(1, 6)
    initial_max_bounces = max_bounces
    balls = []
    flag = False
    current_flag = False
    ring_flag = False
    frames, sounds = [], []
    ball_count = 1

    while running and frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill(background_colour)
        ring.draw(surface, glow=dark_bg)
        current_ball.draw(surface, glow=dark_bg)
        current_ball.update()
        ring_flag = current_ball.check_collision_with_ring(ring)

        for ball in balls:
            if ball is not current_ball:
                current_flag = current_ball.check_collision_with_ball(ball, True)
                if current_flag:
                    particles.emit(int(current_ball.x), int(current_ball.y), current_ball.colour, count=8)

        if current_ball.bounces >= max_bounces:
            balls.append(current_ball)
            current_ball = None
            flag = True
            ball_count += 1
            # Escalation: decrease max_bounces for later balls to speed up fill rate
            if max_bounces > 1 and ball_count % 3 == 0:
                max_bounces = max(1, max_bounces - 1)

        for ball in balls:
            ball.x_vel, ball.y_vel, ball.gravity, ball.friction = 0, 0, 0, 0
            ball.update()
            ball.draw(surface, glow=dark_bg)

        if flag:
            # Use palette colors for variety
            properties['colour'] = random.choice([palette['primary'], palette['secondary'], palette['accent']])
            current_ball = b.Ball(**properties)
            current_ball.x_vel = random.randint(0, 5)
            current_ball.y_vel = random.randint(0, 5)
            flag = False

        if ring_flag:
            sounds.append((note_play.get_next_note() if song else note_play.get_sound(notes_folder), frame_count))

        if current_flag:
            sounds.append((note_play.get_next_note() if song else note_play.get_sound(notes_folder), frame_count))

        # Particles
        particles.update()
        particles.draw(surface)

        # Vignette
        draw_vignette(surface)

        # Stat counter
        bounces_left = max_bounces - current_ball.bounces if current_ball else 0
        draw_stat(surface, f"Bounces: {current_ball.bounces if current_ball else max_bounces}/{max_bounces}")

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

    bounce_similes = [
        "spring", "rebound", "leap", "jump", "ricochet",
        "boing", "skip", "hop", "bound", "pop"
    ]
    countdown_similes = [
        "timer", "clock", "ticker", "count", "chronometer",
        "timekeeper", "timepiece", "chronograph", "stopwatch", "time-count"
    ]

    title = f"{random.choice(bounce_similes)} {random.choice(countdown_similes)}"
    description = f"Each ball stops after {initial_max_bounces} bounces!"

    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
