"""
JARVIS — Main Entry Point
Runs the primary Voice AI loop with real-time speech interrupt.
"""

import sys
import threading
import os
import json

from jarvis.config import WAKE_WORD
from jarvis.voice.speech_to_text import listen_and_transcribe
from jarvis.voice.text_to_speech import speak, speak_async, stop_speaking, is_speaking

from jarvis.agents.controller import MasterController
from jarvis.memory.postgres_db import init_db

def main():
    print("=" * 50)
    print("           JARVIS LOCAL AGENT STARTED           ")
    print("=" * 50)
    print(f"Wake word: '{WAKE_WORD}'")
    print("Say 'exit' or press Ctrl+C to stop.")
    print("Initializing systems...")
    
    init_db()

    # Startup greeting (Natural Speech)
    speak("JARVIS initialized. Hello Hajeera, how can I help you?")

    # State Context
    context = {"intent": None, "entities": {}, "active_intents": set(), "last_skill": None}

    try:
        while True:
            # 1. Continuous Listen (Local/Frontend integration)
            command = listen_and_transcribe()

            if not command:
                continue

            command_low = command.lower()

            # 2. INTERRUPT: if speaking and user says stop ──
            if is_speaking and any(w in command_low for w in ["stop", "wait", "jarvis stop", "quiet", "chup"]):
                stop_speaking()
                print("[JARVIS] Speech interrupted by user.")
                continue

            stop_speaking()

            # 3. EXIT CHECK
            if any(word in command_low for word in ["exit", "quit", "goodbye"]):
                speak("Goodbye.")
                break

            # 4. WAKE WORD CHECK
            if command_low.startswith(WAKE_WORD.lower()):
                speak("Yes Hajeera?")
                continue

            # 5. AGENT ORCHESTRATION (MasterController)
            output, updated_context = MasterController.handle_user_input(
                command, context, user_id="local_user"
            )

            # Update States
            context = updated_context
            
            response = output.get("response")
            spoken_response = output.get("spoken_response")
            lang = output.get("language", "en")
            source = output.get("source")

            if spoken_response:
                print(f"[JARVIS ({source})] Spoken: {spoken_response}")
                speak_async(spoken_response, lang=lang) # Non-blocking speech

    except KeyboardInterrupt:
        print("\n[JARVIS] Shutting down...")
    except Exception as e:
        print(f"\n[JARVIS Fatal Error] {e}")
    finally:
        print("\n[JARVIS] Offline.")
        sys.exit(0)

if __name__ == "__main__":
    main()

