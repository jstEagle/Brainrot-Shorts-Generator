import subprocess
import shutil
import pygame
import config


class VideoWriter:
    """Pipes raw RGB frames directly to FFmpeg — no intermediate PNGs."""

    def __init__(self, output_path="simulation.mp4", width=None, height=None, fps=None):
        self.output_path = output_path
        self.width = width or config.WIDTH
        self.height = height or config.HEIGHT
        self.fps = fps or config.FPS

        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg is None:
            raise RuntimeError("ffmpeg not found on PATH")

        self.proc = subprocess.Popen(
            [
                ffmpeg,
                "-y",
                "-f", "rawvideo",
                "-pix_fmt", "rgb24",
                "-s", f"{self.width}x{self.height}",
                "-r", str(self.fps),
                "-i", "pipe:0",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-crf", config.VIDEO_CRF,
                "-b:v", config.VIDEO_BITRATE,
                "-movflags", "+faststart",
                "-an",
                self.output_path,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.frame_count = 0

    def write_frame(self, surface):
        """Write a pygame Surface as one video frame."""
        raw = pygame.image.tobytes(surface, "RGB")
        self.proc.stdin.write(raw)
        self.frame_count += 1

    def close(self):
        """Finish encoding."""
        if self.proc.stdin:
            self.proc.stdin.close()
        self.proc.wait()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def combine_mp4_and_wav(video_file, audio_file, output_file):
    """Mux video + audio into final mp4 using FFmpeg directly."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg not found on PATH")

    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            output_file,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
