# Brainrot Shorts Generator

Automatically generates physics-based simulation videos optimized for YouTube Shorts and uploads them directly to your channel. Each video features satisfying bouncing balls, orbital mechanics, chain reactions, and pendulum waves -- with neon glow effects, curated color palettes, and engagement hooks.

## Simulations

| Simulation | Description |
|---|---|
| **Growing Sphere** | A ball grows each time it bounces off the ring until it fills the entire space |
| **Shrinking Ring** | The ring contracts with every collision, trapping the ball in a smaller area |
| **Butterfly Effect** | 10-50 balls spawn at nearly identical positions, demonstrating chaos theory |
| **Duplicating Balls** | Balls multiply on collision -- starts with 2, ends with dozens |
| **Bounce Countdown** | Each ball freezes after a set number of bounces, stacking up inside the ring |
| **Time Countdown** | Like bounce countdown, but each ball freezes after a time limit |
| **Gravity Well** | Balls orbit a central attractor with realistic 1/r^2 gravity -- some survive, some get absorbed |
| **Chain Reaction** | One ball triggers a domino-style cascade across a grid of dormant circles |
| **Pendulum Wave** | 15-20 pendulums of different lengths create mesmerizing wave patterns |

## Visual Features

- **Anti-aliased rendering** via `pygame.gfxdraw` for smooth circle edges
- **Neon glow effects** on balls and rings (on dark backgrounds)
- **Particle bursts** on collisions
- **14 curated color palettes** optimized for phone screens (high contrast, neon-on-dark)
- **Slow-motion endings** for dramatic effect

## Engagement Features

- **Hook text** in the first 3 seconds (e.g., "How big can it get?", "The walls are closing in...")
- **CTA text** ("Follow for more!") in the final 2 seconds
- **Auto-shrinking text** -- hook text automatically scales down to fit the screen width
- **Escalation pacing** -- gravity increases over time in butterfly effect, bounce limits decrease in countdown
- **`#Shorts`** auto-appended to descriptions with optimized tags

## Requirements

- Python 3.10+
- FFmpeg (must be on PATH)
- A YouTube API OAuth `client_secrets.json` for uploading

### Core Dependencies

```
pygame==2.5.2
pillow==10.3.0
pydub==0.25.1
numpy==1.26.4
google-api-python-client==2.134.0
oauth2client==4.1.3
pyinstaller==6.4.0
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jstEagle/Brainrot-Shorts-Generator.git
   cd Brainrot-Generator
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. **Add sound files**
   - Place sound effects in `Sounds/` (supports `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, `.aac`, `.wma`)
   - Optionally place songs in `Songs/` (same formats supported) -- they will be automatically cut up into notes and randomly used in videos
   - Both folders are auto-created on first run if they don't exist

4. **Set up YouTube upload (optional)**
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the YouTube Data API v3
   - Create OAuth 2.0 credentials and download as `client_secrets.json`
   - Place `client_secrets.json` in the project root

## Usage

### Generate + Upload (Production)

```bash
python main.py
```

This randomly picks a simulation, renders it, and uploads to YouTube.

### Test Simulations Locally (No Upload)

Use `test_simulation.py` to generate videos without uploading. This is the best way to verify everything works.

```bash
# Show all available simulations
python test_simulation.py

# Run a specific simulation by name
python test_simulation.py growing_sphere
python test_simulation.py gravity_well
python test_simulation.py pendulum_wave

# Run by number
python test_simulation.py 1    # growing_sphere
python test_simulation.py 7    # gravity_well

# Partial name match
python test_simulation.py gravity
python test_simulation.py chain

# Run ALL simulations (full test suite)
python test_simulation.py all
```

Output videos are saved as `test_<name>.mp4` in the project root (e.g., `test_growing_sphere.mp4`). These are gitignored so they won't clutter the repo.

The `all` command runs every simulation and prints a pass/fail summary at the end -- useful for verifying nothing is broken after making changes.

## Compiling to EXE & Running on Startup

The easiest way to build and set up auto-start is with the compile script:

```bash
python compile.py
```

This does two things:
1. Builds `dist/main.exe` using PyInstaller (via `main.spec`)
2. Creates a startup shortcut so the generator runs automatically on login

| Platform | Startup method |
|---|---|
| **Windows** | Creates a `.lnk` shortcut in the Windows Startup folder (`shell:startup`) |
| **Mac** | Creates a LaunchAgent plist in `~/Library/LaunchAgents/` |

The shortcut's working directory is set to the project folder so it can find `Songs/`, `Sounds/`, `fonts/`, and `client_secrets.json`.

> **Note:** On Windows, the script will auto-install `winshell` and `pywin32` if they aren't already installed.

### Manual Build (without startup shortcut)

If you only want the exe without the startup shortcut:

```bash
pyinstaller main.spec --noconfirm
```

The executable will be at `dist/main.exe`. Make sure `client_secrets.json` is in the project root when running.

## Audio

### Drop-in Sound Effects

Place any audio files in the `Sounds/` folder. A random sound is picked for each collision/bounce event. Supported formats: `.wav`, `.mp3`, `.ogg`, `.flac`, `.m4a`, `.aac`, `.wma`.

### Drop-in Songs

Place any audio files in the `Songs/` folder. Songs are automatically split into individual notes and used as bounce sounds, creating musical simulations. Same formats supported.

### Volume Limiting

All generated audio is automatically limited to -6 dBFS to prevent uncomfortable volume spikes.

## Project Structure

```
Brainrot-Generator/
├── main.py                 # Entry point - picks and runs a random simulation
├── compile.py              # Build script - compiles exe and adds to startup
├── test_simulation.py      # Test runner - generate videos without uploading
├── main.spec               # PyInstaller build specification
├── config.py               # Centralized settings (resolution, FPS, timing)
├── ball.py                 # Ball physics class (collision, gravity, anti-aliasing)
├── ring.py                 # Ring rendering class (anti-aliased)
├── pendulum.py             # Pendulum physics class for wave simulation
├── palettes.py             # 14 curated color palettes
├── effects.py              # Glow, particles (with surface caching)
├── text_overlay.py         # PIL-based anti-aliased text with outlines
├── hooks.py                # Engagement hook messages and CTA text
├── util.py                 # File management, color utilities
├── simulation_to_mp4.py    # VideoWriter (FFmpeg pipe) and audio muxing
├── upload_video.py         # YouTube API upload
├── note_play.py            # Sound file loading and audio assembly
├── notes_extraction.py     # Extract note segments from songs
├── fonts/
│   └── Montserrat-Bold.ttf # Bundled font (OFL license)
├── Simulations/
│   ├── growing_sphere.py
│   ├── shrinking_ring.py
│   ├── butterfly_effect.py
│   ├── duplicating_balls.py
│   ├── bounce_countdown.py
│   ├── time_countdown.py
│   ├── gravity_well.py
│   ├── chain_reaction.py
│   └── pendulum_wave.py
├── Songs/                  # Drop audio files here for musical simulations
└── Sounds/                 # Drop sound effects here for bounce sounds
```

## Creating a New Simulation

Each simulation is a Python module in `Simulations/` with a `simulation(output_name)` function that returns `(success: bool, title: str, description: str)`.

Template:

```python
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

    notes_folder, song = util.init_folders(False)
    palette = palettes.get_palette()
    dark_bg = palettes.is_dark_bg(palette)

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'your_sim_name', height)
    particles = ParticleSystem()

    frame_count, max_frames = 0, config.MAX_FRAMES
    sounds = []

    writer = VideoWriter("simulation.mp4", width, height)

    while frame_count < max_frames:
        surface.fill(palette['bg'])

        # Your simulation logic here...

        particles.update()
        particles.draw(surface)

        if frame_count == 0:
            hooks.setup_cta(text_overlay, max_frames, height)
        text_overlay.draw(surface, frame_count)

        writer.write_frame(surface)
        util.loading_bar_frames(frame_count, max_frames)
        frame_count += 1

    writer.close()
    pygame.quit()

    # ... title/description generation ...
    util.finish(output_name, sounds, frame_count, "simulation.mp4", notes_folder, song)
    return True, title, description
```

Then register it in `main.py` and add hook messages in `hooks.py`.

## Output Specs

| Property | Value |
|---|---|
| Resolution | 1080 x 1920 (9:16 vertical) |
| Frame Rate | 60 FPS |
| Duration | ~59 seconds |
| Codec | H.264 (libx264) |
| Quality | CRF 18, 8000k bitrate |
| Audio | AAC 192kbps, limited to -6 dBFS |

## Font License

[Montserrat](https://github.com/JulietaUla/Montserrat) is licensed under the [SIL Open Font License 1.1](https://scripts.sil.org/OFL).

## License

MIT
