"""
JARVIS — Main Entry Point
Runs the primary Voice AI loop entirely locally.
"""

import sys
import time

from config import WAKE_WORD
from voice.speech_to_text import listen_and_transcribe
from voice.text_to_speech import speak, stop_speech
from agents.controller import handle_user_input

def main():
    print("="*50)
    print("           JARVIS-X LOCAL AGENT STARTED           ")
    print("="*50)
    print(f"Wake word: '{WAKE_WORD}'")
    print("Say 'exit' or press Ctrl+C to stop.")
    print("Initializing systems...")
    
    # Optional: Initial greeting
    speak("Jarvis is online and ready.")

    try:
        while True:
            # Listen continuously
            command = listen_and_transcribe()
            
            if not command:
                continue
            
            # 🔥 Immediate stop when hearing a new command
            stop_speech()

            print(f"[USER] {command}")

                
            # 1. EXIT CHECK
            if any(word in command.lower() for word in ["exit", "stop", "quit", "goodbye"]):
                speak("Goodbye.")
                break

            # 2. WAKE WORD CHECK
            if WAKE_WORD.lower() in command.lower():
                speak("Yes?")
                continue
                
            # 3. SEND TO AI (Agent Processing)
            response = handle_user_input(command)
            
            speak(response)

            
    except KeyboardInterrupt:
        print("\n[JARVIS] Shutting down...")
    except Exception as e:
        print(f"\n[JARVIS Fatal Error] {e}")
    finally:
        print("\n[JARVIS] Offline.")
        sys.exit(0)

if __name__ == "__main__":
    main()

