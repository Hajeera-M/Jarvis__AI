"""
JARVIS-X Configuration
Loads environment variables and defines global settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── API Keys ────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")

# ─── Model Settings ──────────────────────────────────────────
GROQ_REASONING_MODEL = "llama-3.3-70b-versatile"
GROQ_WHISPER_MODEL = "whisper-large-v3"
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

# ─── TTS Settings ────────────────────────────────────────────
TTS_VOICE = "en-US-GuyNeural"
TTS_RATE = "+0%"
TTS_VOLUME = "+0%"

# ─── Memory Settings ─────────────────────────────────────────
CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_data")
CHROMA_COLLECTION_NAME = "jarvis_memory"

# ─── File System Sandbox ─────────────────────────────────────
SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")
os.makedirs(SANDBOX_DIR, exist_ok=True)

# ─── Server Settings ─────────────────────────────────────────
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
