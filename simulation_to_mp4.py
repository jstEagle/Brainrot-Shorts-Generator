from moviepy.editor import ImageSequenceClip
from moviepy.editor import VideoFileClip, AudioFileClip
import pygame

pygame.init()

def export_to_mp4(frames):
    # Proceed if we have valid frames
    if frames:
        try:
            clip = ImageSequenceClip(frames, fps=60)
            # Write the video clip to a file
            clip.write_videofile('simulation.mp4')
        except Exception as e:
            print(f"Error creating video: {e}")
    else:
        print("No valid frames available to create video.")

def combine_mp4_and_wav(video_file, audio_file, output_file):
    # Load the video file
    video = VideoFileClip(video_file)
    
    # Load the audio file
    audio = AudioFileClip(audio_file)
    
    # Set the audio of the video to the loaded audio
    final_video = video.set_audio(audio)
    
    # Export the final combined video
    final_video.write_videofile(output_file, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True, audio_bitrate='192k')