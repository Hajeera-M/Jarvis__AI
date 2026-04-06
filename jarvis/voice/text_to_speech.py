"""
JARVIS-X Text-to-Speech — Threaded Non-Blocking with Real-Time Interrupt
"""
import pyttsx3
import threading

# ─── Global State ───
is_speaking = False
_stop_signal = False
_speak_lock = threading.Lock()


def speak(text):
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
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)

            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)

            # Chunk by sentence for interruptible speech
            sentences = [s.strip() for s in text.split(".") if s.strip()]

            for sentence in sentences:
                if _stop_signal:
                    print("[JARVIS] Speech interrupted.")
                    break
                engine.say(sentence + ".")
                engine.runAndWait()

        except Exception as e:
            print("[JARVIS TTS Error]:", e)
        finally:
            is_speaking = False

    # Only one speech thread at a time
    with _speak_lock:
        _stop_signal = True  # kill any prior speech

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    t.join()  # Block until speech finishes (main loop listens via interrupt thread)


def speak_async(text):
    """
    Fire-and-forget version of speak().
    Returns immediately so the main loop can keep listening.
    Use this for normal responses.
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
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)

            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)

            sentences = [s.strip() for s in text.split(".") if s.strip()]

            for sentence in sentences:
                if _stop_signal:
                    print("[JARVIS] Speech interrupted.")
                    break
                engine.say(sentence + ".")
                engine.runAndWait()

        except Exception as e:
            print("[JARVIS TTS Error]:", e)
        finally:
            is_speaking = False

    with _speak_lock:
        _stop_signal = True

    t = threading.Thread(target=_run, daemon=True)
    t.start()


def stop_speaking():
    """Immediately signals speech to stop between sentences."""
    global _stop_signal, is_speaking
    _stop_signal = True
    is_speaking = False
