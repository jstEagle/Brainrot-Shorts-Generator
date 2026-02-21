import pygame
import ball as b
import ring as r
import random
import note_play
import util
import config
import palettes
from simulation_to_mp4 import VideoWriter
from effects import ParticleSystem
from text_overlay import TextOverlay
import hooks


def simulation(output_name="final"):
    pygame.init()

    width, height = config.WIDTH, config.HEIGHT
    surface = pygame.Surface((width, height))

    notes_folder, song = util.init_folders(random.choice([True, True, True, False]))

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
        ball_trail = random.choice([random.randint(100, 1000), random.randint(200, 1000), random.randint(0, 20), random.randint(0, 30)])

        ball_properties = {
            'colour': ball_colour,
            'r': ball_r,
            'x': random.randint(ring_x - ring_r + ball_r, ring_x + ring_r - ball_r),
            'y': random.randint(ring_y - ring_r + ball_r, ring_y),
            'x_vel': random.randint(2, 10),
            'y_vel': random.randint(2, 10),
            'gravity': random.uniform(0.2, 0.6),
            'trail': ball_trail,
            'fading': random.choice([True, True, True, False]),
            'border': random.choice([True, False, False]) if ball_trail < 100 else True,
            'efficiency': random.uniform(0.98, 1.01),
            'friction': random.randint(0, 5),
        }
        return ball_properties

    properties = create_properties()
    while properties['gravity'] + properties['friction'] * (1 / properties['efficiency']) > 7:
        properties = create_properties()

    sphere = b.Ball(**properties)

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'growing_sphere', height)

    particles = ParticleSystem()

    running = True
    check = True
    frame_count, max_frames, end_count = 0, config.MAX_FRAMES, 0
    rate = random.uniform(1.01, 1.06)
    sounds = []
    climax_frame = -1

    writer = VideoWriter("simulation.mp4", width, height)

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
                sphere.r *= rate
                sounds.append((note_play.get_next_note() if song else note_play.get_sound(), frame_count))
                particles.emit(int(sphere.x), int(sphere.y), sphere.colour, count=10)
            elif sphere.check_collision_with_ring(ring):
                sphere.trail_frames = []
                sphere.r = ring.r
                sphere.x, sphere.y = width / 2, height / 2
                sphere.x_vel, sphere.y_vel = 0, 0
                sphere.gravity = 0
                check = False
                climax_frame = frame_count
        else:
            end_count += 1

        # Particles
        particles.update()
        particles.draw(surface)

        # Text overlays (hook text)
        if frame_count == 0:
            hooks.setup_cta(text_overlay, max_frames, height)
        text_overlay.draw(surface, frame_count)

        writer.write_frame(surface)
        util.loading_bar_frames(frame_count, max_frames)
        frame_count += 1

    writer.close()
    pygame.quit()
    print()

    if frame_count < config.MIN_FRAMES:
        if song:
            util.clear_folder(notes_folder)
            note_play.init()
        return False, "fail", "fail"

    growing_similes = [
        "expanding", "increasing", "enlarging", "blossoming", "flourishing",
        "developing", "swelling", "broadening", "amplifying", "maturing"
    ]
    sphere_similes = [
        "orb", "globe", "ball", "circle", "bubble",
        "round", "disk", "ellipsoid", "spheroid", "circular"
    ]

    title = f"{random.choice(growing_similes)} {random.choice(sphere_similes)}"
    description = "The ball grows each time it bounces. Watch to the end!"

    util.finish(output_name, sounds, frame_count, "simulation.mp4", notes_folder, song)
    return True, title, description
