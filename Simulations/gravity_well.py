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


def simulation(output_name="final"):
    pygame.init()

    width, height = config.WIDTH, config.HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, frames_folder, song = util.init_folders(False)

    # Use curated palette
    palette = palettes.get_palette()
    while not palettes.is_dark_bg(palette):
        palette = palettes.get_palette()  # gravity well looks best on dark bg

    background_colour = palette['bg']
    ball_colour = palette['primary']
    attractor_colour = palette['accent']
    ring_colour = palette['ring']

    # Central attractor
    attractor_x = width // 2
    attractor_y = height // 2
    attractor_r = random.randint(25, 45)
    initial_attractor_r = attractor_r
    gravity_strength = random.uniform(800, 2000)

    # Create orbiting balls
    num_balls = random.randint(5, 15)
    ball_colors = palettes.get_similar_colors(ball_colour, num_balls, variance=40)
    balls = []
    ball_r = random.randint(6, 14)

    for i in range(num_balls):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.randint(150, 400)
        x = attractor_x + dist * math.cos(angle)
        y = attractor_y + dist * math.sin(angle)
        # Give tangential velocity for orbit
        speed = random.uniform(3, 7)
        vx = -speed * math.sin(angle) + random.uniform(-0.5, 0.5)
        vy = speed * math.cos(angle) + random.uniform(-0.5, 0.5)

        ball = b.Ball(
            colour=ball_colors[i],
            x=x, y=y,
            x_vel=vx, y_vel=vy,
            r=ball_r,
            gravity=0,  # we handle gravity manually
            trail=random.randint(30, 80),
            fading=True,
            border=False,
            efficiency=1.0,
            friction=0
        )
        balls.append(ball)

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'gravity_well', height)

    particles = ParticleSystem()

    running = True
    frame_count = 0
    max_frames = config.MAX_FRAMES
    frames, sounds = [], []
    absorbed_count = 0

    while running and frame_count < max_frames and len(balls) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill(background_colour)

        # Draw attractor with glow
        draw_glow(surface, attractor_colour, (attractor_x, attractor_y), attractor_r, intensity=8)
        try:
            pygame.gfxdraw.aacircle(surface, attractor_x, attractor_y, int(attractor_r), attractor_colour)
            pygame.gfxdraw.filled_circle(surface, attractor_x, attractor_y, int(attractor_r), attractor_colour)
        except (ValueError, OverflowError):
            pygame.draw.circle(surface, attractor_colour, (attractor_x, attractor_y), int(attractor_r))

        # Update and draw balls
        to_remove = []
        for ball in balls:
            ball.apply_gravity_towards(attractor_x, attractor_y, gravity_strength)
            ball.update()
            ball.draw(surface, glow=True)

            # Check if absorbed (too close to attractor)
            dx = ball.x - attractor_x
            dy = ball.y - attractor_y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < attractor_r + ball.r * 0.5:
                to_remove.append(ball)
                # Attractor grows when absorbing
                attractor_r += ball.r * 0.4
                absorbed_count += 1
                particles.emit(int(ball.x), int(ball.y), ball.colour, count=12)
                sounds.append((note_play.get_sound(notes_folder), frame_count))

            # Keep balls on screen (soft boundary)
            margin = 100
            if ball.x < -margin or ball.x > width + margin or ball.y < -margin or ball.y > height + margin:
                to_remove.append(ball)

        for ball in to_remove:
            if ball in balls:
                balls.remove(ball)

        # Particles
        particles.update()
        particles.draw(surface)

        # Screen flash when ball absorbed
        if to_remove:
            draw_screen_flash(surface, alpha=60)

        # Vignette
        draw_vignette(surface)

        # Stat counter
        draw_stat(surface, f"Survivors: {len(balls)}")

        # Text overlays (hook + CTA)
        if frame_count == 0:
            hooks.setup_cta(text_overlay, max_frames, height)
        text_overlay.draw(surface, frame_count)

        # Save frame
        frame_path = os.path.join(frames_folder, f'frame_{frame_count:04d}.png')
        pygame.image.save(surface, frame_path)
        util.loading_bar_frames(frame_count, max_frames)

        frame_count += 1
        frames.append(frame_path)

    # End sequence: show final attractor for a bit
    end_count = 0
    while end_count < config.END_FRAMES and frame_count < max_frames:
        surface.fill(background_colour)
        draw_glow(surface, attractor_colour, (attractor_x, attractor_y), int(attractor_r), intensity=10)
        try:
            pygame.gfxdraw.aacircle(surface, attractor_x, attractor_y, int(attractor_r), attractor_colour)
            pygame.gfxdraw.filled_circle(surface, attractor_x, attractor_y, int(attractor_r), attractor_colour)
        except (ValueError, OverflowError):
            pygame.draw.circle(surface, attractor_colour, (attractor_x, attractor_y), int(attractor_r))
        particles.update()
        particles.draw(surface)
        draw_vignette(surface)
        draw_stat(surface, f"Absorbed: {absorbed_count}")
        text_overlay.draw(surface, frame_count)

        frame_path = os.path.join(frames_folder, f'frame_{frame_count:04d}.png')
        pygame.image.save(surface, frame_path)
        util.loading_bar_frames(frame_count, max_frames)
        frame_count += 1
        frames.append(frame_path)
        end_count += 1

    pygame.quit()
    print()

    if len(frames) < config.MIN_FRAMES:
        util.clear_folder(frames_folder)
        return False, "fail", "fail"

    title_words = [
        ("orbital", "cosmic", "gravitational", "stellar", "celestial"),
        ("collapse", "vortex", "abyss", "void", "well"),
    ]
    title = f"{random.choice(title_words[0])} {random.choice(title_words[1])}"
    description = f"A gravity well absorbs orbiting balls. {absorbed_count} were consumed!"

    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
