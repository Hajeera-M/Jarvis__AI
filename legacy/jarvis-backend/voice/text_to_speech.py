"""
JARVIS — Text-to-Speech
Uses edge-tts for high-quality speech synthesis.
"""

import io
import edge_tts
from config import TTS_VOICE, TTS_RATE, TTS_VOLUME


async def synthesize_speech(text: str) -> bytes:
    """
    Convert text to speech audio (MP3 bytes) using edge-tts.
    
    Args:
        text: The text to speak
    
    Returns:
        MP3 audio as bytes
    """
    if not text:
        return b""

    communicate = edge_tts.Communicate(
        text=text,
        voice=TTS_VOICE,
        rate=TTS_RATE,
        volume=TTS_VOLUME,
    )

    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])

    return audio_buffer.getvalue()

