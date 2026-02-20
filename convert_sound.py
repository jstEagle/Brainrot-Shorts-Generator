from pydub import AudioSegment
import librosa
import numpy as np
import os

# Load the original sound file
original_audio_file = "Songs/Sandstorm.wav"
audio, sr = librosa.load(original_audio_file, mono=True)  # Convert audio to mono

# Create a "notes" folder if it doesn't exist
if not os.path.exists("notes"):
    os.makedirs("notes")

# Define parameters for onset detection
hop_length = 1484
onset_frames = librosa.onset.onset_detect(y=audio, sr=sr, hop_length=hop_length)

# Extract notes and convert to a different instrument
for i, onset_frame in enumerate(onset_frames):
    # Extract note based on onset frame and hop length
    start_sample = onset_frame * hop_length
    end_sample = start_sample + hop_length
    note_audio = audio[start_sample:end_sample]

    # Convert the note to an AudioSegment
    audio_segment = AudioSegment(
        note_audio.tobytes(),  # Convert NumPy array to bytes
        frame_rate=sr,
        sample_width=note_audio.dtype.itemsize,
        channels=2  # Mono audio
    )

    # Save the note as a WAV file in the "notes" folder
    note_file = f"notes/note_{i}.wav"
    audio_segment.export(note_file, format="wav")

# Print the number of notes saved
num_notes = len(onset_frames)
print(f"{num_notes} notes saved in the 'notes' folder.")
