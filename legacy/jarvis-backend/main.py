"""
JARVIS-X — Main FastAPI Server
Voice-based agentic AI assistant.
"""

import io
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from config import CORS_ORIGINS
from voice.speech_to_text import transcribe_audio
from voice.text_to_speech import synthesize_speech
from agents.controller import run_agent

# ─── App ──────────────────────────────────────────────────────
app = FastAPI(
    title="JARVIS-X",
    description="Voice-Based Agentic AI Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Models ───────────────────────────────────────────────────
class TextCommandRequest(BaseModel):
    text: str


class TextCommandResponse(BaseModel):
    transcript: str
    response: str


# ─── Routes ───────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "JARVIS-X"}


@app.post("/voice-command")
async def voice_command(audio: UploadFile = File(...)):
    """
    Full voice pipeline:
    1. Receive audio blob from frontend
    2. Transcribe with Groq Whisper
    3. Run through agent system
    4. Synthesize response to speech
    5. Return audio stream
    """
    try:
        # 1. Read uploaded audio
        audio_bytes = await audio.read()

        # 2. Speech-to-Text
        transcript = await transcribe_audio(audio_bytes)
        if not transcript.strip():
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        # 3. Agent reasoning pipeline
        response_text = await run_agent(transcript)

        # 4. Text-to-Speech
        audio_output = await synthesize_speech(response_text)

        # 5. Return audio with transcript in headers
        return StreamingResponse(
            io.BytesIO(audio_output),
            media_type="audio/mpeg",
            headers={
                "X-Transcript": transcript,
                "X-Response-Text": response_text,
                "Access-Control-Expose-Headers": "X-Transcript, X-Response-Text",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/text-command", response_model=TextCommandResponse)
async def text_command(request: TextCommandRequest):
    """
    Text-based fallback (no audio needed).
    Useful for testing and accessibility.
    """
    try:
        response_text = await run_agent(request.text)
        return TextCommandResponse(
            transcript=request.text,
            response=response_text,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice-command-full")
async def voice_command_full(audio: UploadFile = File(...)):
    """
    Same as /voice-command but returns JSON with both text and audio URL.
    Frontend can choose to use either.
    """
    try:
        audio_bytes = await audio.read()
        transcript = await transcribe_audio(audio_bytes)
        if not transcript.strip():
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        response_text = await run_agent(transcript)
        audio_output = await synthesize_speech(response_text)

        import base64
        audio_b64 = base64.b64encode(audio_output).decode("utf-8")

        return {
            "transcript": transcript,
            "response": response_text,
            "audio_base64": audio_b64,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
