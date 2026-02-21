# Centralized configuration for Brainrot Shorts Generator

# Video resolution (vertical for YouTube Shorts)
WIDTH = 1080
HEIGHT = 1920

# Half resolution (used by duplicating_balls)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# Frame rate and duration
FPS = 60
MAX_FRAMES = 3540  # ~59 seconds at 60 FPS
MIN_FRAMES = 600   # minimum viable video length

# End sequence
END_FRAMES = 180   # 3 seconds of ending

# Hook text timing (in frames)
HOOK_FADE_IN_START = 15
HOOK_FADE_IN_END = 45
HOOK_VISIBLE_END = 135
HOOK_FADE_OUT_END = 165

# CTA text timing (frames from end)
CTA_DURATION = 120  # 2 seconds

# Slow-mo settings
SLOWMO_FRAMES = 60       # last 60 frames before climax
SLOWMO_DT = 0.3          # time scale during slow-mo

# Screen flash
FLASH_FRAMES = 3
FLASH_ALPHA = 180

# Video encoding
VIDEO_BITRATE = '8000k'
VIDEO_CRF = '18'

# Font
FONT_PATH = 'fonts/Montserrat-Bold.ttf'
FONT_SIZE_LARGE = 72
FONT_SIZE_MEDIUM = 48
FONT_SIZE_SMALL = 36
