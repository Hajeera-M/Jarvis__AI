import pyttsx3
import logging

class OutputModule:
    def __init__(self, rate=175, volume=1.0):
        self.logger = logging.getLogger(__name__)
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Set voice (optional: find a female voice if available)
            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                # Try to pick a standard female voice if it exists
                self.engine.setProperty('voice', voices[1].id)
            elif len(voices) > 0:
                self.engine.setProperty('voice', voices[0].id)
                
        except Exception as e:
            self.logger.error(f"TTS Initialization Error: {str(e)}")
            self.engine = None

    def speak(self, text):
        """
        Converts text to speech and plays it.
        
        Args:
            text (str): The text to be spoken.
        """
        if not text:
            return

        print(f"JARVIS: {text}")
        
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                self.logger.error(f"TTS Speech Error: {str(e)}")
        else:
            self.logger.warning("TTS Engine not available. Speaking text is disabled.")

if __name__ == "__main__":
    # Test cases
    output = OutputModule()
    output.speak("Hello! I am Jarvis. System check complete.")
