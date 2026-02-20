from pydub import AudioSegment

def lower_volume(input_file, output_file, db_reduction):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Reduce the volume
    quieter_audio = audio - db_reduction
    
    # Export the modified audio to a new file
    quieter_audio.export(output_file, format="wav")
    
def increase_volume(input_file, output_file, db_increase):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Increase the volume
    louder_audio = audio + db_increase

    # Export the modified audio to a new file
    louder_audio.export(output_file, format="wav")

# Example usage
input_file = "Sounds/hit.wav"
output_file = "Sounds/hit.wav"
db_change = 5  # Reduce volume by 10 dB

increase_volume(input_file, output_file, db_change)
