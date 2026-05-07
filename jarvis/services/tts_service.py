"""
JARVIS — TTS Service
Cloud-to-Local fallback TTS with speech formatting and language-aware voice selection.
"""

import re
import os
import logging

logger = logging.getLogger("JARVIS")

# Configurable voice map — no hard-coded provider IDs in core logic
VOICE_MAP = {
    "en": os.getenv("VOICE_EN", "en-IN-Wavenet-B"),
    "hi": os.getenv("VOICE_HI", "hi-IN-Wavenet-A"),
    "ur": os.getenv("VOICE_UR", "ur-PK-Wavenet-A"),
    "hinglish": os.getenv("VOICE_HINGLISH", "en-IN-Wavenet-B"),
}

FALLBACK_VOICE = "default"


def format_for_speech(text: str) -> str:
    """Strips markdown, shortens, and makes text speech-friendly."""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # bold
    text = re.sub(r'\*(.+?)\*', r'\1', text)       # italic
    text = re.sub(r'`(.+?)`', r'\1', text)         # code
    text = re.sub(r'#{1,6}\s*', '', text)           # headings
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text) # links
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)  # emojis
    
    # Remove bullet points and numbered lists
    text = re.sub(r'^\s*[-*•]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # Collapse whitespace
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def select_voice(lang_code: str) -> str:
    """Returns the voice ID for the detected language with fallback."""
    return VOICE_MAP.get(lang_code, VOICE_MAP.get("en", FALLBACK_VOICE))


class TTSService:
    @staticmethod
    def generate_spoken_response(full_response: str, lang_code: str) -> dict:
        """
        Returns a dict with spoken_response text and selected voice.
        Audio generation is handled by the frontend using the voice hint.
        """
        spoken = format_for_speech(full_response)
        voice = select_voice(lang_code)
        
        return {
            "spoken_response": spoken,
            "voice": voice
        }

