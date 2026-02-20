from pydub import AudioSegment
import os
import shutil

def extract_notes(file_path_mp3):
    file_path = f"Songs/{file_path_mp3}"
    # Load the MP3 file
    audio = AudioSegment.from_mp3(file_path)

    # Define the duration of each note (in milliseconds)
    note_duration = 200  # Assuming each note lasts for 1 second

    # Define the output folder to store the notes
    output_folder = "notes"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        shutil.rmtree(output_folder)
        os.makedirs(output_folder)

    # Split the audio into individual notes
    for i, start_time in enumerate(range(note_duration * 30, len(audio) - note_duration * 30, note_duration)):
        # Extract each note segment
        note = audio[start_time:start_time+note_duration]
        
        # Save the note as a new audio file
        output_file = os.path.join(output_folder, f"note_{i}.wav")
        note.export(output_file, format="wav")

    return output_folder