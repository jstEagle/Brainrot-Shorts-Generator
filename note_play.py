import os
import util
from pydub import AudioSegment

loaded_files = []

def init():    
    folder_path = "notes"
    # Get a list of all files in the folder
    files_in_folder = os.listdir(folder_path)

    # Count the number of files in the folder
    num_files = len(files_in_folder)
    path = folder_path

    # Preload all sound files
    for i in range(30, num_files - 30):
        sound_file = f"note_{i}.wav"
        file_path = os.path.join(folder_path, sound_file)
        loaded_files.append(file_path)

def get_next_note():
    try:
        return loaded_files.pop(0)
    except IndexError as e:
        init()
        get_next_note()

def get_sound(sound_name):
    return f"Sounds/{sound_name}"
    
# Function to create an empty WAV file and add sounds at specific times
def create_and_add_sounds_at_times(output_file, sound_timeline, duration):
    # Create an empty (silent) audio segment of the specified duration (in milliseconds)
    duration = (duration / 60) * 1000
    empty_audio = AudioSegment.silent(duration=duration)
    
    count = 0
    # Add each sound file to the empty audio at the specified time
    for sound_file, start_time in sound_timeline:
        start_time = (start_time / 60) * 1000
        sound = AudioSegment.from_wav(sound_file)
        empty_audio = empty_audio.overlay(sound, position=start_time)
        util.loading_bar_sound(count, len(sound_timeline))
        count += 1
    
    # Export the final audio to a WAV file
    empty_audio.export(output_file, format="wav")