import os
import random
import util
from pydub import AudioSegment

loaded_files = []

# Supported audio extensions
_AUDIO_EXTS = {'.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac', '.wma'}

# Cache of sound files in Sounds/ folder
_sound_files = None


def init():
    global loaded_files
    loaded_files = []
    folder_path = "notes"
    files_in_folder = os.listdir(folder_path)
    num_files = len(files_in_folder)

    # Preload all sound files (skip first/last 30 to avoid silence at edges)
    for i in range(30, num_files - 30):
        sound_file = f"note_{i}.wav"
        file_path = os.path.join(folder_path, sound_file)
        loaded_files.append(file_path)


def get_next_note():
    try:
        return loaded_files.pop(0)
    except IndexError:
        init()
        return get_next_note()


def _load_sound_files():
    """Scan Sounds/ folder and cache the list of audio files."""
    global _sound_files
    os.makedirs("Sounds", exist_ok=True)
    _sound_files = [
        os.path.join("Sounds", f)
        for f in os.listdir("Sounds")
        if os.path.splitext(f)[1].lower() in _AUDIO_EXTS
    ]


def get_sound():
    """Return a random sound file path from the Sounds/ folder."""
    if _sound_files is None:
        _load_sound_files()
    if not _sound_files:
        return None
    return random.choice(_sound_files)


# Function to create an empty WAV file and add sounds at specific times
def create_and_add_sounds_at_times(output_file, sound_timeline, duration):
    # Create an empty (silent) audio segment of the specified duration (in milliseconds)
    duration = (duration / 60) * 1000
    empty_audio = AudioSegment.silent(duration=duration)

    count = 0
    # Add each sound file to the empty audio at the specified time
    for sound_file, start_time in sound_timeline:
        if sound_file is None:
            count += 1
            continue
        start_time = (start_time / 60) * 1000
        sound = AudioSegment.from_file(sound_file)
        empty_audio = empty_audio.overlay(sound, position=start_time)
        util.loading_bar_sound(count, len(sound_timeline))
        count += 1

    # Limit max volume to a comfortable level
    max_dbfs = -6.0
    if empty_audio.max_dBFS > max_dbfs:
        empty_audio = empty_audio.apply_gain(max_dbfs - empty_audio.max_dBFS)

    # Export the final audio to a WAV file
    empty_audio.export(output_file, format="wav")
