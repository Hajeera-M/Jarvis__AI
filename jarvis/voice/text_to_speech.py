import pyttsx3

# Initialize engine globally
try:
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 170)
    
    # Set to female voice (Index 1 is usually Zira on Windows)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
except:
    engine = None

def speak(text: str):
    """
    Speaks text synchronously using pyttsx3 for 100% offline stability.
    """
    if not text or not engine:
        if not engine: print(f"[JARVIS - no TTS] {text}")
        return

    print(f"[JARVIS] {text}")

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech error:", e)

def stop_speech():
    """Immediately stops the engine."""
    if engine:
        try:
            engine.stop()
        except:
            pass






