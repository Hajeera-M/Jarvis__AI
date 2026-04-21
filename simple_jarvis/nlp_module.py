import datetime
from enum import Enum

class Intent(Enum):
    IMAGE_GENERATION = "IMAGE_GENERATION"
    GREETING = "GREETING"
    TIME = "TIME"
    EXIT = "EXIT"
    GENERAL = "GENERAL"

class NLPModule:
    def __init__(self):
        self.image_keywords = ["generate", "create", "draw", "image", "picture", "show me"]
        self.greeting_keywords = ["hello", "hi", "hey", "jarvis", "good morning", "good evening"]
        self.time_keywords = ["time", "clock", "hour", "date", "day"]
        self.exit_keywords = ["exit", "quit", "stop", "goodbye", "bye"]

    def process_intent(self, text):
        """
        Determines the intent of the user input and generates a basic text response.
        
        Args:
            text (str): Input text in English.
            
        Returns:
            tuple: (IntentEnum, response_text)
        """
        query = text.lower().strip()

        # 1. Check for EXIT intent first
        if any(word in query for word in self.exit_keywords):
            return Intent.EXIT, "Shutting down. Goodbye!"

        # 2. Check for IMAGE_GENERATION intent
        if any(word in query for word in self.image_keywords):
            return Intent.IMAGE_GENERATION, f"I am preparing to generate an image based on: {text}"

        # 3. Check for GREETING intent
        if any(word in query for word in self.greeting_keywords):
            return Intent.GREETING, "Hello! I am Jarvis. How can I assist you today?"

        # 4. Check for TIME intent
        if any(word in query for word in self.time_keywords):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return Intent.TIME, f"The current time is {current_time}."

        # 5. Default to GENERAL reasoning
        return Intent.GENERAL, "I'm not sure I understand that exactly, but I'm here to help."

if __name__ == "__main__":
    # Test cases
    nlp = NLPModule()
    test_queries = [
        "Hello Jarvis",
        "What time is it?",
        "Create an image of a sunset",
        "How are you?",
        "Quit the program"
    ]
    
    for q in test_queries:
        intent, resp = nlp.process_intent(q)
        print(f"Query: {q} | Intent: {intent.value} | Response: {resp}")
