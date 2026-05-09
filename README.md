# Transcription Pipeline

Simple speech-to-text transcription API built with FastAPI and OpenAI Whisper.

This project accepts audio uploads (`MP3` or `WAV`), normalizes audio using FFmpeg, transcribes speech into text, and returns timestamped transcript segments in JSON format.

---

# Features

- FastAPI REST API
- Upload MP3 or WAV audio files
- Audio normalization using FFmpeg
- Speech-to-text transcription using OpenAI Whisper
- Timestamped transcript segments
- JSON API response
- Simple and clean project structure
- Ready for future async/background processing

---

# Tech Stack

- Python 3.11+
- FastAPI
- OpenAI Whisper
- FFmpeg
- Uvicorn

---

# Project Structure

```txt
transcription-pipeline/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── transcriber.py
│   └── utils.py
│
├── uploads/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Requirements

Before running the application, install:

- Python 3.11+
- FFmpeg

---

# Install FFmpeg

## Windows

Download FFmpeg:

https://www.gyan.dev/ffmpeg/builds/

Extract it and add the `bin` folder to Windows PATH.

Verify installation:

```bash
ffmpeg -version
```

---

## Mac

```bash
brew install ffmpeg
```

---

## Ubuntu / Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

---

# Setup Project

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/transcription-pipeline.git
```

```bash
cd transcription-pipeline
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Application

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Application will run on:

```txt
http://127.0.0.1:8000
```

Swagger documentation:

```txt
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## POST /transcribe

Upload audio file and receive transcription.

### Request

Multipart form-data:

```txt
file=@sample.mp3
```

---

# Example Using cURL

```bash
curl -X POST "http://127.0.0.1:8000/transcribe" \
  -F "file=@sample.mp3"
```

---

# Example Response

```json
{
  "success": true,
  "filename": "sample.mp3",
  "transcript": {
    "text": "Hello world",
    "segments": [
      {
        "start": 0.0,
        "end": 2.5,
        "text": "Hello world"
      }
    ]
  }
}
```

---

# How It Works

## 1. File Upload

The API validates uploaded audio files (`MP3` and `WAV`).

---

## 2. Audio Normalization

FFmpeg converts uploaded audio into:

- mono channel
- 16kHz sample rate
- WAV format

This improves transcription consistency.

---

## 3. Speech-to-Text

OpenAI Whisper processes normalized audio and generates:

- full transcript text
- timestamped segments

---

# Whisper Model

Current implementation uses:

```python
whisper.load_model("small")
```

Possible models:

| Model | Speed | Accuracy |
|---|---|---|
| tiny | fastest | lowest |
| base | fast | good |
| small | balanced | better |
| medium | slower | high |
| large | slowest | best |

---

# Example Segment Structure

```json
{
  "start": 0.0,
  "end": 5.12,
  "text": "Hello world"
}
```

---

# Future Improvements

Possible production improvements:

- Background processing with Celery/RQ
- Queue system (Redis/RabbitMQ/Kafka)
- S3/GCS object storage
- Authentication & rate limiting
- Docker support
- GPU inference
- Speaker diarization
- Async chunk processing for long audio
- WebSocket progress updates

---

# Handling Long Audio Files

For production-scale systems:

- split large audio into chunks
- process asynchronously
- merge transcript results afterward

This reduces memory usage and improves scalability.

---

# Error Handling

Current implementation includes:

- file type validation
- FFmpeg conversion checks
- HTTP error responses
- exception handling

Example errors:

```json
{
  "detail": "Only MP3 and WAV files are supported"
}
```

---

# Notes

- First Whisper run may take longer because model downloads automatically.
- CPU inference is supported.
- GPU inference significantly improves performance if CUDA is available.

Example warning on CPU:

```txt
FP16 is not supported on CPU; using FP32 instead
```

This is normal behavior.

---

# License

MIT License

---

# Author

Milos Djonovic