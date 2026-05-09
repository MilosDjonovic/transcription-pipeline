# Transcription Pipeline

A robust, asynchronous transcription service built with FastAPI, OpenAI Whisper, and FFmpeg.

## Project Structure

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

## 🚀 Design Decisions

### 1. Asynchronous Processing Pattern
Transcription is a computationally expensive and time-consuming task. To ensure the API remains responsive and to avoid HTTP timeouts, I implemented an **Asynchronous Polling Pattern**:
- **Immediate Acknowledgement**: The `/transcribe` endpoint returns a `job_id` and status `pending` immediately after the file is validated and saved.
- **Background Execution**: The actual transcription runs out-of-band using FastAPI's `BackgroundTasks`.
- **Status Polling**: Users can check progress via the `/status/{job_id}` endpoint.

### 2. Audio Normalization with FFmpeg
Whisper and other STT models are highly sensitive to audio sample rates and channel counts. To ensure maximum accuracy and support for various input formats:
- I integrated **FFmpeg** to normalize all incoming audio to **16kHz mono WAV** files before they reach the model.
- This preprocessing step standardizes the input, reduces model inference errors, and minimizes file size for processing.

### 3. Speech-to-Text with OpenAI Whisper
I chose the **OpenAI Whisper** model because of its state-of-the-art accuracy, robust handling of different accents, and support for multi-language transcription.
- The implementation returns both the full text and **timestamped segments**, which is critical for downstream uses like subtitling or media indexing.

### 4. Robust Validation
Security and stability are handled at the "edge" of the application:
- **Dual-Layer Validation**: Every upload is checked for both its file extension (.mp3, .wav) and its MIME type (Content-Type header).
- **FFmpeg as a Validator**: The conversion process acts as an implicit integrity check; if the file is not valid audio, FFmpeg will fail safely.

---

## 🛠 Tech Stack
- **Framework**: FastAPI (Python)
- **AI Model**: OpenAI Whisper (Small)
- **Preprocessing**: FFmpeg
- **Validation**: Pydantic
- **Environment**: Uvicorn

---

## 🛰 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/transcribe` | Upload MP3/WAV and get a `job_id`. |
| `GET` | `/status/{id}` | Check job status and get JSON results. |
| `GET` | `/status/{id}/text` | Get the final transcript as plain text. |
| `GET` | `/jobs` | List all recent transcription jobs. |

## Example Using cURL
```bash
curl -X POST "http://127.0.0.1:8000/transcribe" \
  -F "file=@sample.mp3"
```

---

## Example Response

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

## 📈 Future Scaling (System Design)
For a production-grade system, I would implement the following:
1. **Task Queue**: Move from local background tasks to **Celery with Redis/RabbitMQ** to allow workers to scale horizontally across multiple GPU-enabled nodes.
2. **Object Storage**: Replace local disk storage with **AWS S3** for audio files, utilizing signed URLs for security.
3. **Database**: Use **PostgreSQL (JSONB)** to persist transcription results instead of the current in-memory mock.
4. **Reliability**: Implement **Exponential Backoff Retries** for failed tasks and a **Dead Letter Queue (DLQ)** for manual auditing of failed transcriptions.
5. **Real-time Notifications**: Use **Webhooks** to notify external services when a transcript is ready, eliminating the need for client polling.

---

## ⚙️ Installation & Running

1. **Install FFmpeg**: Ensure FFmpeg is installed and added to your system PATH.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App**:
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Interactive Docs**: Visit `http://localhost:8000/docs` to test the API.
