import logging
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

class TranslatorModule:
    def __init__(self, target_lang='en'):
        self.target_lang = target_lang
        self.logger = logging.getLogger(__name__)

    def detect_and_translate(self, text):
        """
        Detects the source language and translates the text to the target language (default: English).
        
        Args:
            text (str): Input text in any language.
            
        Returns:
            tuple: (translated_text, detected_lang)
        """
        if not text or not text.strip():
            return "", "unknown"

        try:
            # 1. Detect Language
            detected_lang = detect(text)
            self.logger.info(f"Detected language: {detected_lang}")

            # 2. Translate if not already in target language
            if detected_lang != self.target_lang:
                translated_text = GoogleTranslator(source='auto', target=self.target_lang).translate(text)
                self.logger.info(f"Translated '{text}' to '{translated_text}'")
                return translated_text, detected_lang
            else:
                return text, detected_lang

        except Exception as e:
            self.logger.error(f"Translation Error: {str(e)}")
            # Fallback to original text if translation fails
            return text, "unknown"

if __name__ == "__main__":
    # Test cases
    translator = TranslatorModule()
    test_texts = [
        "नमस्ते",         # Hindi
        "ನಮಸ್ಕಾರ",      # Kannada
        "నమస్కారం",      # Telugu
        "Hello",        # English
    ]
    
    logging.basicConfig(level=logging.INFO)
    for t in test_texts:
        res, lang = translator.detect_and_translate(t)
        print(f"Original: {t} | Detected: {lang} | Translated: {res}")
