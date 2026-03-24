"""
JARVIS-X — Groq Client
Handles reasoning (LLM) and transcription (Whisper) via Groq API.
"""

from groq import Groq
from config import GROQ_API_KEY, GROQ_REASONING_MODEL, GROQ_WHISPER_MODEL

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not set. Please add it to your .env file.")
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


async def think(prompt: str, system_prompt: str = "", temperature: float = 0.7) -> str:
    """
    Send a reasoning/thinking request to Groq LLM.
    Used by the planner and reflection agents.
    """
    client = _get_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=GROQ_REASONING_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=2048,
    )

    return response.choices[0].message.content.strip()


async def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """
    Transcribe audio bytes using Groq Whisper.
    """
    client = _get_client()

    response = client.audio.transcriptions.create(
        model=GROQ_WHISPER_MODEL,
        file=(filename, audio_bytes),
        response_format="text",
    )

    return response.strip() if isinstance(response, str) else response.text.strip()
