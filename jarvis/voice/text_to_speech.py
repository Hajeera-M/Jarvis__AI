"""
JARVIS Text-to-Speech — Threaded Non-Blocking with Real-Time Interrupt
Features:
- Native Indian Accent via gTTS (co.in TLD)
- Graceful Pygame Audio playing
- Fallback to pyttsx3 offline voice if internet fails
"""
import pyttsx3
import threading
import pygame
import io
import time
from gtts import gTTS

# ─── Global State ───
is_speaking = False
_stop_signal = False
_speak_lock = threading.Lock()

# Initialize Pygame Mixer for high-quality audio
pygame.mixer.init()

def _play_gtts(text, lang_code="en"):
    """Generates Indian Accent TTS in memory and plays it via Pygame."""
    try:
        # Prevent audio thread overlapping by forcefully stopping mixer first
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        # Language mapping for proper native TTS rendering
        if lang_code == "hi":
            tts_lang = "hi"
            tld = "co.in"
        elif lang_code == "ur":
            tts_lang = "ur"
            tld = "com" 
        else:
            tts_lang = "en"
            tld = "co.in" # Natural Google Assistant Indian English accent
            
        tts = gTTS(text=text, lang=tts_lang, tld=tld)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        pygame.mixer.music.load(fp, 'mp3')
        pygame.mixer.music.play()
        
        # Block until speaking is done, or interrupted
        while pygame.mixer.music.get_busy():
            if _stop_signal:
                pygame.mixer.music.stop()
                break
            time.sleep(0.05)
        return True
    except Exception as e:
        print(f"[gTTS Error]: {e} - Falling back to offline voice.")
        return False

def _play_pyttsx3(text):
    """Offline Fallback."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    sentences = [s.strip() for s in text.split(".") if s.strip()]
    for sentence in sentences:
        if _stop_signal:
            break
        engine.say(sentence + ".")
        engine.runAndWait()


def speak(text, lang="en"):
    """
    Speaks text in a background thread.
    The main loop stays free to listen for 'stop' commands.
    """
    global is_speaking, _stop_signal
    if not text:
        return

    print(f"[JARVIS] {text}")

    def _run():
        global is_speaking, _stop_signal
        _stop_signal = False
        is_speaking = True

        try:
            # Try high-fidelity online voice first
            success = _play_gtts(text, lang_code=lang)
            if not success:
                # Fallback to robotic offline voice
                _play_pyttsx3(text)
        finally:
            is_speaking = False

    with _speak_lock:
        _stop_signal = True

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    
    # Safely block and handle KeyboardInterrupt gracefully
    try:
        while t.is_alive():
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_speaking()
        print("\n[JARVIS] Gracefully stopping speech...")


def speak_async(text, lang="en"):
    """
    Fire-and-forget version of speak().
    Returns immediately.
    """
    global is_speaking, _stop_signal
    if not text:
        return

    print(f"[JARVIS] {text}")

    def _run():
        global is_speaking, _stop_signal
        _stop_signal = False
        is_speaking = True

        try:
            success = _play_gtts(text, lang_code=lang)
            if not success:
                _play_pyttsx3(text)
        finally:
            is_speaking = False

    with _speak_lock:
        _stop_signal = True

    t = threading.Thread(target=_run, daemon=True)
    t.start()


def stop_speaking():
    """Immediately signals speech to stop."""
    global _stop_signal, is_speaking
    _stop_signal = True
    is_speaking = False
    
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

