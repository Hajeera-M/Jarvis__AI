import time
from voice.text_to_speech import speak

print("Initiating voice test...")
speak("Hello, I am Jarvis. Your speech system is now stable and ready for the demo.")

# Give it a few seconds to finish the threaded speech
time.sleep(5)
print("Test complete.")
