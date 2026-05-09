import os
import subprocess


ALLOWED_EXTENSIONS = [".mp3", ".wav"]


def validate_audio_file(filename: str):
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Only MP3 and WAV files are supported")


def convert_to_wav(input_path: str, output_path: str):
    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        output_path,
    ]

    subprocess.run(command, check=True)