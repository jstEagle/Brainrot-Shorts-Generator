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
- **Cinematic vignette** overlay
- **Screen flash** on climactic moments
- **Slow-motion endings** for dramatic effect

## Engagement Features

- **Hook text** in the first 3 seconds (e.g., "How big can it get?", "The walls are closing in...")
- **Live stat counters** (Size %, Balls count, Bounces, Ring %, Survivors, Time)
- **CTA text** ("Follow for more!") in the final 2 seconds
- **Escalation pacing** -- gravity increases over time in butterfly effect, bounce limits decrease in countdown
- **`#Shorts`** auto-appended to descriptions with optimized tags

## Requirements

- Python 3.10+
- FFmpeg (must be on PATH)
- A YouTube API OAuth `client_secrets.json` for uploading

### Core Dependencies

```
pygame==2.5.2
moviepy==1.0.3
pillow==10.3.0
pydub==0.25.1
numpy==1.26.4
google-api-python-client==2.134.0
oauth2client==4.1.3
imageio==2.34.1
imageio-ffmpeg==0.5.1
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Brainrot-Generator.git
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
   - Place `.wav` sound effects in `Sounds/` (at least one file required)
   - Optionally place `.mp3` songs in `Songs/` for musical simulations

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

## Project Structure

```
Brainrot-Generator/
├── main.py                 # Entry point - picks and runs a random simulation
├── test_simulation.py      # Test runner - generate videos without uploading
├── config.py               # Centralized settings (resolution, FPS, timing)
├── ball.py                 # Ball physics class (collision, gravity, anti-aliasing)
├── ring.py                 # Ring rendering class (anti-aliased)
├── pendulum.py             # Pendulum physics class for wave simulation
├── palettes.py             # 14 curated color palettes
├── effects.py              # Glow, particles, screen flash, vignette
├── text_overlay.py         # PIL-based anti-aliased text with outlines
├── hooks.py                # Engagement hook messages and CTA text
├── util.py                 # File management, color utilities
├── simulation_to_mp4.py    # Frame sequence to MP4 conversion
├── upload_video.py         # YouTube API upload
├── note_play.py            # Audio playback management
├── notes_extraction.py     # Extract audio segments from songs
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
├── Songs/                  # MP3 files for musical simulations
├── Sounds/                 # WAV sound effects
└── frames/                 # Temporary frame output (auto-cleaned)
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

    notes_folder, frames_folder, song = util.init_folders(False)
    palette = palettes.get_palette()
    dark_bg = palettes.is_dark_bg(palette)

    # Setup text overlays
    text_overlay = TextOverlay()
    hooks.setup_hook(text_overlay, 'your_sim_name', height)
    particles = ParticleSystem()

    frame_count, max_frames = 0, config.MAX_FRAMES
    frames, sounds = [], []

    while frame_count < max_frames:
        surface.fill(palette['bg'])

        # Your simulation logic here...

        particles.update()
        particles.draw(surface)
        draw_vignette(surface)
        draw_stat(surface, "Your stat here")

        if frame_count == 0:
            hooks.setup_cta(text_overlay, max_frames, height)
        text_overlay.draw(surface, frame_count)

        frame_path = os.path.join(frames_folder, f'frame_{frame_count:04d}.png')
        pygame.image.save(surface, frame_path)
        util.loading_bar_frames(frame_count, max_frames)
        frame_count += 1
        frames.append(frame_path)

    pygame.quit()
    # ... title/description generation ...
    util.finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song)
    return True, title, description
```

Then register it in `main.py` and add hook messages in `hooks.py`.

## Compiling to EXE & Running on Startup

### Step 1: Compile with PyInstaller

```bash
pyinstaller --onefile ^
    --add-data "fonts;fonts" ^
    --add-data "Simulations;Simulations" ^
    --add-data "Sounds;Sounds" ^
    --hidden-import=Simulations.growing_sphere ^
    --hidden-import=Simulations.shrinking_ring ^
    --hidden-import=Simulations.butterfly_effect ^
    --hidden-import=Simulations.duplicating_balls ^
    --hidden-import=Simulations.bounce_countdown ^
    --hidden-import=Simulations.time_countdown ^
    --hidden-import=Simulations.gravity_well ^
    --hidden-import=Simulations.chain_reaction ^
    --hidden-import=Simulations.pendulum_wave ^
    --hidden-import=pygame.gfxdraw ^
    main.py
```

This creates `dist/main.exe`. Make sure `client_secrets.json` is in the same directory as the exe when running.

### Step 2: Run on Windows Startup

1. Press `Win + R`, type `shell:startup`, press Enter
2. This opens the Startup folder (`C:\Users\<you>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`)
3. Create a shortcut to `dist/main.exe` (or copy an existing one) into this folder
4. The generator will now run automatically every time you log in

Alternatively, use Task Scheduler for more control:

1. Open **Task Scheduler** (`Win + R` -> `taskschd.msc`)
2. Click **Create Basic Task**
3. Name: "Brainrot Generator"
4. Trigger: **When I log on**
5. Action: **Start a program** -> browse to `dist/main.exe`
6. Set **Start in** to the directory containing `client_secrets.json` and `Sounds/`
7. Finish

## Output Specs

| Property | Value |
|---|---|
| Resolution | 1080 x 1920 (9:16 vertical) |
| Frame Rate | 60 FPS |
| Duration | ~59 seconds |
| Codec | H.264 (libx264) |
| Quality | CRF 18, 8000k bitrate |
| Audio | AAC 192kbps |

## Font License

[Montserrat](https://github.com/JulietaUla/Montserrat) is licensed under the [SIL Open Font License 1.1](https://scripts.sil.org/OFL).

## License

MIT
