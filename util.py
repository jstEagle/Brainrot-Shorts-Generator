import note_play
import simulation_to_mp4 as export
import notes_extraction
import sys
import os
import random
import palettes

def finish(output_name, sounds, frames, frame_count, frames_folder, notes_folder, song):
    note_play.create_and_add_sounds_at_times("output.wav", sounds, frame_count)
    export.export_to_mp4(frames)
    export.combine_mp4_and_wav("simulation.mp4", "output.wav", f"{output_name}.mp4")
    clear_folder(frames_folder)
    if song: clear_folder(notes_folder)
    delete_file("output.wav")
    delete_file("simulation.mp4")

def loading_bar_frames(frame_count, max_frames):
    progress = int((frame_count / max_frames) * 100)
    
    sys.stdout.write(f"\rFrames Progress: {progress}%")
    sys.stdout.flush()
    
def loading_bar_sound(count, duration):
    progress = int((count / duration) * 100)
    
    sys.stdout.write(f"\rSounds Progress: {progress}%")
    
def init_folders(song):
    if song:
        files = os.listdir("Songs")
        song_name = random.choice(files)
        notes_folder = notes_extraction.extract_notes(song_name)
        note_play.init()
    else:
        files = os.listdir("Sounds")
        notes_folder = random.choice(files)
    frames_folder = "frames"
    os.makedirs(frames_folder, exist_ok=True)

    return notes_folder, frames_folder, song

def clear_folder(folder_path):
    files_in_folder = os.listdir(folder_path)

    for file in files_in_folder:
        file_path = os.path.join(folder_path, file)
        os.remove(file_path)

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def random_colour(lower_bound, upper_bound):
    return (random.randint(lower_bound, upper_bound), random.randint(lower_bound, upper_bound), random.randint(lower_bound, upper_bound))

def create_colour_pair():
    first_colour = (random_colour(20, 240))
    second_colour = (250 - first_colour[0], 250 - first_colour[1], 250 - first_colour[2])

    return first_colour, second_colour

def create_background_colour():
    light = random.randint(200, 250)
    dark = random.randint(0, 100)
    colours = [(light, light, light), (dark, dark, dark)]
    
    return random.choice(colours)

def get_palette():
    """Get a curated color palette. Wrapper for palettes module."""
    return palettes.get_palette()

def create_similar_colours(start_colour, num_colours, variance):
    colours = []
    for i in range(0, num_colours):
        r = 250 - start_colour[0]
        if r - variance < 0:
            r = r + random.randint(0, variance)
        elif r + variance > 250:
            r = r - random.randint(0, variance)
        else:
            r += random.randint(-variance, variance)

        g = 250 - start_colour[1] + random.randint(-variance, variance)
        if g - variance < 0:
            g = g + random.randint(0, variance)
        elif g + variance > 250:
            g = g - random.randint(0, variance)
        else:
            g += random.randint(-variance, variance)

        b = 250 - start_colour[2] + random.randint(-variance, variance)
        if b - variance < 0:
            b = b + random.randint(0, variance)
        elif b + variance > 250:
            b = b - random.randint(0, variance)
        else:
            b += random.randint(-variance, variance)

        colours.append((r, g, b))

    return colours