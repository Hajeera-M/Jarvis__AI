"""
JARVIS — Main Entry Point
Runs the primary Voice AI loop with real-time speech interrupt.
"""

import sys
import threading

from jarvis.config import WAKE_WORD
from jarvis.voice.speech_to_text import listen_and_transcribe
from jarvis.voice.text_to_speech import speak, speak_async, stop_speaking, is_speaking

from jarvis.agents.controller import MasterController
from jarvis.memory.postgres_db import init_db



def main():
    print("=" * 50)
    print("           JARVIS-X LOCAL AGENT STARTED           ")
    print("=" * 50)
    print(f"Wake word: '{WAKE_WORD}'")
    print("Say 'exit' or press Ctrl+C to stop.")
    print("Initializing systems...")
    
    init_db()

    # Startup greeting (blocking — waits until done)
    speak("JARVIS initialized. All systems are operational. How can I assist you?")

    # State Memory for Contextual Understanding
    context = {"intent": None, "entity": None, "entities": {}, "active_intents": set(), "last_skill": None}
    image_mode = False

    try:
        while True:
            # Listen continuously (this blocks until speech is detected)
            command = listen_and_transcribe()

            if not command:
                continue

            command_low = command.lower()

            # ── INTERRUPT: if speaking and user says stop ──
            if is_speaking and any(w in command_low for w in ["stop", "wait", "jarvis stop", "quiet"]):
                stop_speaking()
                print("[JARVIS] Speech interrupted by user.")
                continue

            # Any new command also interrupts current speech
            stop_speaking()

            # 1. EXIT CHECK
            if any(word in command_low for word in ["exit", "quit", "goodbye"]):
                speak("Goodbye.")
                break

            # 2. WAKE WORD CHECK
            if command_low.startswith(WAKE_WORD.lower()):
                speak("Yes?")
                continue

            # 3. SEND TO SKILLS SYSTEM (with persistent user_id) using Agent Controller
            output, updated_context = MasterController.handle_user_input(command, context, user_id="local_user")
            
            response = output.get("response")
            source = output.get("source")

            # Update States
            context = updated_context

            if response:
                speak_async(response)  # Non-blocking: JARVIS speaks while still listening

    except KeyboardInterrupt:
        print("\n[JARVIS] Shutting down...")
    except Exception as e:
        print(f"\n[JARVIS Fatal Error] {e}")
    finally:
        print("\n[JARVIS] Offline.")
        sys.exit(0)


if __name__ == "__main__":
    main()
