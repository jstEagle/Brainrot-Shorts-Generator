from pydub import AudioSegment

# Load the MP3 file
mp3_file = "Songs/Sandstorm.mp3"
audio = AudioSegment.from_mp3(mp3_file)

# Export the audio as WAV format
wav_file = "Songs/Sandstorm.wav"
audio.export(wav_file, format="wav")

print("MP3 file converted to WAV:", wav_file)
