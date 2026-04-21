"""
JARVIS — STT Service
Handles backend-only Speech-to-Text using Groq Whisper.
Includes transcript normalization to fix common Indian accent/slang mistakes.
"""

from typing import Optional
from groq import Groq
from jarvis.config import GROQ_API_KEY
import os

client = Groq(api_key=GROQ_API_KEY)

# Normalization map for common Indian SLT (Speech-Language Transformation) errors
NORMALIZATION_MAP = {
    "hajra": "Hajeera",
    "hajira": "Hajeera",
    "hazeera": "Hajeera",
    "hajeera": "Hajeera",
    "jarvis x": "JARVIS",
    "hinglish": "Hinglish",
    "kyun": "kyun", # Example Hinglish fix
    "kaise ho": "kaise ho",
}

def normalize_transcript(text: str) -> str:
    """Corrects common STT mis-transcriptions for the JARVIS ecosystem."""
    text_lower = text.lower()
    for error, correction in NORMALIZATION_MAP.items():
        if error in text_lower:
            # Case-insensitive replacement
            import re
            pattern = re.compile(re.escape(error), re.IGNORECASE)
            text = pattern.sub(correction, text)
    return text.strip()

class STTService:
    @staticmethod
    def transcribe_audio(audio_file_path: str) -> Optional[str]:
        """
        Sends audio to Groq Whisper and returning normalized transcript.
        """
        try:
            with open(audio_file_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(audio_file_path), file.read()),
                    model="whisper-large-v3",
                    response_format="text",
                    # Context for better Indian accent/Hinglish recognition
                    prompt="The user might speak in Indian English, Hindi, Urdu, or Hinglish. Names like Hajeera and Sana might be mentioned."
                )
            

            clean_text = normalize_transcript(str(transcription))
            return clean_text
            
        except Exception as e:
            print(f"[STTService Error] Transcription failed: {e}")
            return None

