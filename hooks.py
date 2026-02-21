import config
from text_overlay import TextOverlay

# Per-simulation hook messages displayed in the first 2-3 seconds
HOOKS = {
    'growing_sphere': [
        "How big can it get?",
        "Watch it GROW...",
        "It gets bigger every bounce!",
        "Will it fill the ring?",
    ],
    'shrinking_ring': [
        "The walls are closing in...",
        "Nowhere to hide.",
        "The ring gets SMALLER...",
        "How long can it survive?",
    ],
    'butterfly_effect': [
        "They start at the SAME spot...",
        "Same start. Different paths.",
        "Chaos from order.",
        "Watch them diverge!",
    ],
    'duplicating_balls': [
        "They just keep multiplying...",
        "More. And MORE.",
        "How many will there be?",
        "Every bounce = more chaos!",
    ],
    'bounce_countdown': [
        "Each ball gets limited bounces.",
        "Bounce. Stop. Repeat.",
        "How will they stack up?",
        "Count the bounces!",
    ],
    'time_countdown': [
        "Time is ticking...",
        "Each ball has a timer.",
        "Freeze! Next ball.",
        "The clock runs out!",
    ],
    'gravity_well': [
        "Will any survive the black hole?",
        "Gravity always wins.",
        "Orbiting the void...",
        "Don't get too close!",
    ],
    'chain_reaction': [
        "One ball. Total chaos.",
        "Watch the chain reaction!",
        "It only takes ONE...",
        "Domino effect!",
    ],
    'pendulum_wave': [
        "Wait for them to sync up...",
        "Mesmerizing patterns ahead.",
        "Physics is beautiful.",
        "Watch till the end!",
    ],
}

# End CTA messages
CTA_MESSAGES = [
    "Follow for more!",
    "Like & Follow!",
    "More on my page!",
]


def setup_hook(text_overlay, simulation_name, height):
    """Add hook text overlay for the first 3 seconds of a simulation."""
    import random
    messages = HOOKS.get(simulation_name, ["Watch this!"])
    message = random.choice(messages)

    text_overlay.add(
        text=message,
        size=config.FONT_SIZE_LARGE,
        position=(0, int(height * 0.15)),
        fade_in_start=config.HOOK_FADE_IN_START,
        fade_in_end=config.HOOK_FADE_IN_END,
        fade_out_start=config.HOOK_VISIBLE_END,
        fade_out_end=config.HOOK_FADE_OUT_END,
    )


def setup_cta(text_overlay, total_frames, height):
    """Add 'Follow for more!' CTA text in the final 2 seconds."""
    import random
    cta = random.choice(CTA_MESSAGES)
    start_frame = total_frames - config.CTA_DURATION

    text_overlay.add(
        text=cta,
        size=config.FONT_SIZE_MEDIUM,
        position=(0, int(height * 0.80)),
        fade_in_start=start_frame,
        fade_in_end=start_frame + 20,
        fade_out_start=total_frames - 10,
        fade_out_end=total_frames,
    )
