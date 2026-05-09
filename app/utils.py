import os
import subprocess
import shutil

ALLOWED_EXTENSIONS = [".mp3", ".wav"]
ALLOWED_MIME_TYPES = [
    "audio/mpeg", 
    "audio/wav", 
    "audio/x-wav",
    "application/octet-stream"  # Generic binary fallback for CLI tools
]


def validate_audio_file(filename: str, content_type: str = None):
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension {ext} not supported. Supported: {ALLOWED_EXTENSIONS}")
    
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"MIME type {content_type} not supported.")


def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg is not installed or not in PATH")


def convert_to_wav(input_path: str, output_path: str):
    check_ffmpeg()
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

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg conversion failed: {result.stderr}")