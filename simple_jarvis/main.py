import sys
import argparse
import logging
from input_module import InputModule
from translation_module import TranslatorModule
from nlp_module import NLPModule, Intent
from image_generator import ImageGenerator
from output_module import OutputModule

# Configure logging to hide internal logs from the user's terminal
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class JarvisAssistant:
    def __init__(self, use_text_mode=False):
        self.text_mode = use_text_mode
        
        # Initialize Modules
        self.output = OutputModule()
        self.translator = TranslatorModule()
        self.nlp = NLPModule()
        self.image_gen = ImageGenerator()
        
        # Only initialize Mic if not in text mode
        if not self.text_mode:
            self.input_mod = InputModule()
            if not self.input_mod.mic:
                print("Warning: Microphone not detected. Falling back to Keyboard Mode.")
                self.text_mode = True
        else:
            self.input_mod = None

    def get_user_input(self):
        """
        Gets input from either Microphone or Keyboard depending on mode.
        """
        if self.text_mode:
            try:
                user_text = input("\nYou: ")
                return user_text
            except (KeyboardInterrupt, EOFError):
                return "exit"
        else:
            return self.input_mod.listen()

    def run(self):
        self.output.speak("System initialized. I am ready.")
        if self.text_mode:
            print("(Running in Keyboard Mode)")
        else:
            print("(Running in Voice Mode - type Ctrl+C to stop)")

        while True:
            try:
                # 1. Capture Input
                raw_input = self.get_user_input()
                
                if raw_input is None:
                    continue
                
                if "Error:" in raw_input:
                    self.output.speak(raw_input)
                    continue

                # 2. Translate to English
                english_text, source_lang = self.translator.detect_and_translate(raw_input)
                
                # 3. Detect Intent and Logic
                intent, response_text = self.nlp.process_intent(english_text)

                # 4. Handle Actions
                if intent == Intent.EXIT:
                    self.output.speak(response_text)
                    break
                
                elif intent == Intent.IMAGE_GENERATION:
                    self.output.speak("Understood. I'm generating your image now...")
                    filepath, message = self.image_gen.generate_image(english_text)
                    if filepath:
                        print(f"Success: {message}")
                        self.output.speak("The image has been generated and opened for you.")
                    else:
                        print(f"Failed: {message}")
                        self.output.speak(message)
                
                else:
                    # Time, Greeting, General
                    self.output.speak(response_text)

            except KeyboardInterrupt:
                print("\nInterrupted by user.")
                self.output.speak("Goodbye!")
                break
            except Exception as e:
                print(f"System Error: {str(e)}")
                self.output.speak("I encountered an internal error. Standing by.")

def main():
    parser = argparse.ArgumentParser(description="Jarvis AI Assistant")
    parser.add_argument("--text", action="store_true", help="Run in keyboard-only mode")
    args = parser.parse_args()

    jarvis = JarvisAssistant(use_text_mode=args.text)
    jarvis.run()

if __name__ == "__main__":
    main()
