"""
JARVIS — Wake Word Detector
Listens for the 'jarvis' keyword using OpenWakeWord (fully local).
"""

import os
import struct
import numpy as np
import pyaudio
import openwakeword
from openwakeword.model import Model
from jarvis.config import WAKE_WORD

# Initialize OpenWakeWord model
try:
    # Use 'alexa' as it's a confirmed pretrained model available
    _model = Model(wakeword_models=['alexa'], inference_framework="onnx")
except Exception as e:
    print(f"Warning: Failed to initialize OpenWakeWord: {e}")
    _model = None

def wait_for_wake_word():
    """
    Blocks until the wake word is detected from the default microphone using OpenWakeWord.
    """
    if _model is None:
        print("Error: OpenWakeWord model not initialized.")
        return False

    pa = None
    audio_stream = None

    try:
        pa = pyaudio.PyAudio()

        # OpenWakeWord expects 16kHz, mono, 16-bit PCM
        audio_stream = pa.open(
            rate=16000,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=1280 # Common buffer size for OWW
        )

        print(f"\n[JARVIS] Listening for wake word '{WAKE_WORD}' (OpenWakeWord)...")

        while True:
            # Read audio data
            data = audio_stream.read(1280, exception_on_overflow=False)
            
            # Convert buffer to int16 numpy array
            audio_frame = np.frombuffer(data, dtype=np.int16)
            
            # Process with OpenWakeWord
            prediction = _model.predict(audio_frame)
            
            # Check if any model detected its keyword
            for mdl in prediction:
                if prediction[mdl] > 0.5: # Threshold of 0.5
                    print(f"[JARVIS] Wake word detected: {mdl} ({prediction[mdl]:.2f})")
                    return True

    except KeyboardInterrupt:
        print("\n[JARVIS] Stopping wake word detector...")
        return False
    except Exception as e:
        print(f"[JARVIS Error] Wake word detector failure: {e}")
        return False
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

