"""
JARVIS Web Backend — Natural Voice AI Bridge
FastAPI orchestrator for speech-to-text, reasoning, and neural TTS response.
"""

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import os
import asyncio
import logging
import traceback
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure the 'jarvis' folder is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jarvis.agents.controller import MasterController
from jarvis.memory.postgres_db import init_db
from jarvis.services.stt_service import STTService

# 1. Structured Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join("logs", "latest_api.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("JARVIS")

# Database initialization
try:
    init_db()
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

app = FastAPI(title="JARVIS Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static folder exists and mount it
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class JarvisRequest(BaseModel):
    input: str
    user_id: str = "default_user"

# Global Context State
context = {"intent": None, "entities": {}, "active_intents": set(), "last_skill": None}

@app.get("/health")
async def health():
    return {"status": "running", "service": "JARVIS"}

@app.get("/")
async def root():
    return {"status": "JARVIS backend is running"}

@app.post("/jarvis")
async def jarvis_api(req: JarvisRequest):
    global context
    logger.info(f"EVENT: jarvis_request | USER: {req.user_id} | INPUT: {req.input}")
    
    try:
        # Agent Orchestration (Dispatcher Logic)
        output, new_context = await asyncio.to_thread(
            MasterController.handle_user_input, req.input, context, req.user_id
        )
        
        context = new_context
        logger.info(f"EVENT: jarvis_response | USER: {req.user_id} | OUTPUT: {output}")
        
        status_val = output.pop("status", "success")
        return {**output, "status": status_val}

    except Exception as e:
        logger.error(f"EVENT: jarvis_error | USER: {req.user_id} | ERROR: {str(e)}")
        return {"error": "Internal Processing Error", "status": "error"}

@app.post("/stt")
async def stt_api(audio: UploadFile = File(...)):
    """Backend-only STT path for high-fidelity Indian accent recognition."""
    try:
        # Temporary storage for audio processing
        temp_filename = f"temp_{uuid.uuid4()}.wav"
        with open(temp_filename, "wb") as buffer:
            buffer.write(await audio.read())
        
        # Backend Transcription
        transcript = await asyncio.to_thread(STTService.transcribe_audio, temp_filename)
        
        # Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        return {"transcript": transcript, "status": "success"} if transcript else {"error": "STT Failed", "status": "error"}

    except Exception as e:
        logger.error(f"EVENT: stt_error | ERROR: {str(e)}")
        return {"error": "Internal STT Error", "status": "error"}

