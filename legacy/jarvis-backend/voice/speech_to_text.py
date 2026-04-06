"""
JARVIS-X — Speech-to-Text
Uses Groq Whisper API to transcribe audio.
"""

from models.groq_client import transcribe


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """
    Transcribe raw audio bytes to text using Groq Whisper.
    
    Args:
        audio_bytes: Raw audio data (WebM, WAV, MP3, etc.)
        filename: Filename hint for the audio format
    
    Returns:
        Transcribed text string
    """
    if not audio_bytes:
        return ""

    transcript = await transcribe(audio_bytes, filename=filename)
    return transcript
