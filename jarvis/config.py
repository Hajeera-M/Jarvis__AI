"""
JARVIS-X Configuration
Loads environment variables and defines global settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── API Keys ────────────────────────────────────────────────
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")

# ─── Database ────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/jarvis_db")

# ─── Model Settings ──────────────────────────────────────────
GROQ_REASONING_MODEL = "llama-3.3-70b-versatile"
GROQ_WHISPER_MODEL = "whisper-large-v3"
HUGGINGFACE_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"

# ─── Wake Word Settings ──────────────────────────────────────
WAKE_WORD = "alexa"

# ─── File System Sandbox ─────────────────────────────────────
SANDBOX_DIR = os.path.join(os.path.dirname(__file__), "sandbox")
os.makedirs(SANDBOX_DIR, exist_ok=True)
