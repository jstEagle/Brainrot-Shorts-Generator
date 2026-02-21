from pydub import AudioSegment
import os
import shutil


def extract_notes(file_name):
    file_path = f"Songs/{file_name}"
    # Load audio file (supports mp3, wav, ogg, flac, m4a, etc.)
    audio = AudioSegment.from_file(file_path)

    # Define the duration of each note (in milliseconds)
    note_duration = 200

    # Define the output folder to store the notes
    output_folder = "notes"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        shutil.rmtree(output_folder)
        os.makedirs(output_folder)

    # Split the audio into individual notes (skip first/last 6 seconds)
    for i, start_time in enumerate(range(note_duration * 30, len(audio) - note_duration * 30, note_duration)):
        note = audio[start_time:start_time+note_duration]

        output_file = os.path.join(output_folder, f"note_{i}.wav")
        note.export(output_file, format="wav")

    return output_folder
