"""
JARVIS — Speech to Text
Uses SpeechRecognition to record audio and Groq Whisper to transcribe.
"""

import speech_recognition as sr
import io
import wave
from config import GROQ_API_KEY, GROQ_WHISPER_MODEL

# We'll initialize the Groq client lazily
_groq_client = None

def _get_groq_client():
    global _groq_client
    if _groq_client is None:
        from groq import Groq
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not set.")
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client


def listen_and_transcribe() -> str:
    """
    Listens to the microphone until silence, then transcribes using Google Speech Recognition (en-IN).
    
    Returns:
        Transcribed text string
    """
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("[JARVIS] Listening... (en-IN mode)")
        # Adjust for ambient noise for 1 second as requested
        r.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Listen until silence
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            print("[JARVIS] Transcribing...")
        except sr.WaitTimeoutError:
            return ""

    try:
        # Use Google Speech Recognition with Indian English locale for better accuracy
        transcript = r.recognize_google(audio, language="en-IN")
        print(f"[USER] {transcript}")
        return transcript.strip()

    except sr.UnknownValueError:
        # Silently ignore if no speech was understood
        return ""
    except Exception as e:
        print(f"[JARVIS] Transcription error: {e}")
        return ""
