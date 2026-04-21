import speech_recognition as sr
import logging

class InputModule:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Check for microphone availability
        try:
            self.mic = sr.Microphone()
            # Calibrate for ambient noise
            with self.mic as source:
                print("Adjusting for ambient noise... please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.logger.info("Microphone initialized successfully.")
        except Exception as e:
            self.logger.error(f"Microphone Initialization Error: {str(e)}")
            self.mic = None

    def listen(self):
        """
        Listens to the user's voice and converts it to text.
        
        Returns:
            str: The recognized text, or None if an error occurs.
        """
        if not self.mic:
            self.logger.warning("No microphone detected.")
            return None

        try:
            with self.mic as source:
                print("\nListening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            self.logger.info(f"Recognized: {query}")
            return query

        except sr.WaitTimeoutError:
            self.logger.info("Listening timed out (no speech detected).")
            return None
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio.")
            return "Error: Could not understand audio"
        except sr.RequestError as e:
            self.logger.error(f"Speech Service Request Error: {str(e)}")
            return "Error: Speech service unavailable"
        except Exception as e:
            self.logger.error(f"Unexpected Mic Error: {str(e)}")
            return None

if __name__ == "__main__":
    # Test cases
    logging.basicConfig(level=logging.INFO)
    input_mod = InputModule()
    if input_mod.mic:
        result = input_mod.listen()
        print(f"Final Result: {result}")
    else:
        print("Microphone not available for test.")
