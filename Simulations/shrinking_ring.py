import pygame
import ball as b
import ring as r
import random
import note_play
import os
import util
import config
import palettes
from effects import ParticleSystem, draw_screen_flash, draw_vignette
from text_overlay import TextOverlay, draw_stat
import hooks


def simulation(output_name="final"):
    pygame.init()

    width, height = config.WIDTH, config.HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, frames_folder, song = util.init_folders(random.choice([True, True, True, False]))

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
    initial_ring_r = ring_r
    ring_width = random.randint(5, 20)
    ring = r.Ring(ring_x, ring_y, ring_r, background_colour, ring_colour, ring_width)

    def create_properties():
        ball_r = random.randint(10, 50)
        ball_trail = random.randint(0, 50)

        ball_properties = {
            'colour': ball_colour,
            'r': ball_r,
            'x': random.randint(ring_x - ring_r + ball_r, ring_x + ring_r - ball_r),
            'y': random.randint(ring_y - ring_r + ball_r, ring_y),
            'x_vel': random.randint(2, 10),
            'y_vel': random.randint(2, 10),
            'gravity': random.uniform(0.5, 1),
            'trail': ball_trail,
            'fading': random.choice([True, True, True, False]),
            'border': random.choice([True, False, False]),
            'efficiency': random.uniform(0.98, 1),
            'friction': 0,
        }
        return ball_properties

    properties = create_properties()
    while properties['gravity'] + properties['friction'] * (1 / properties['efficiency']) > 7:
        properties = create_properties()

    sphere = b.Ball(**properties)

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'shrinking_ring', height)

    particles = ParticleSystem()

    running = True
    check = True
    frame_count, max_frames, end_count = 0, config.MAX_FRAMES, 0
    rate = random.uniform(0.98, 0.994)
    frames, sounds = [], []
    flash_timer = 0

    while running and frame_count < max_frames and end_count < config.END_FRAMES:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Slow-mo near climax
        dt = 1.0
        if not check and end_count < config.SLOWMO_FRAMES:
            dt = config.SLOWMO_DT

        surface.fill(background_colour)
        ring.draw(surface, glow=dark_bg)
        sphere.draw(surface, glow=dark_bg)
        sphere.update(dt=dt)

        if check:
            if sphere.check_collision_with_ring(ring) and sphere.r <= ring.r:
                ring.r *= rate
                sounds.append((note_play.get_next_note() if song else note_play.get_sound(notes_folder), frame_count))
                particles.emit(int(sphere.x), int(sphere.y), sphere.colour, count=10)
            elif sphere.check_collision_with_ring(ring):
                sphere.trail_frames = []
                sphere.r = ring.r
                sphere.x, sphere.y = width / 2, height / 2
                sphere.x_vel, sphere.y_vel = 0, 0
                sphere.gravity = 0
                check = False
                flash_timer = config.FLASH_FRAMES
        else:
            end_count += 1

        # Screen flash on climax
        if flash_timer > 0:
            draw_screen_flash(surface, alpha=config.FLASH_ALPHA)
            flash_timer -= 1

        # Particles
        particles.update()
        particles.draw(surface)

        # Vignette
        draw_vignette(surface)

        # Stat counter: ring percentage remaining
        if initial_ring_r > 0:
            ring_pct = int((ring.r / initial_ring_r) * 100)
            draw_stat(surface, f"Ring: {max(ring_pct, 0)}%")

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

    if len(frames) < config.MIN_FRAMES:
        util.clear_folder(frames_folder)
        if song:
            util.clear_folder(notes_folder)
            note_play.init()
        return False, "fail", "fail"

    shrinking_similes = [
        "diminishing", "contracting", "reducing", "narrowing", "waning",
        "decreasing", "lessening", "condensing", "compressing", "receding"
    ]
    ring_similes = [
        "circle", "hoop", "loop", "band", "coil",
        "disk", "circlet", "round", "annulus", "torus"
    ]

    title = f"{random.choice(shrinking_similes)} {random.choice(ring_similes)}"
    description = "The ring shrinks with every bounce, Watch to the end!"

    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
