"""
JARVIS — Vision Service
Provides screen capture and visual reasoning capabilities.
"""

import os
import time
import base64
import logging
from PIL import ImageGrab
import io
from groq import Groq

logger = logging.getLogger("JARVIS")

class VisionService:
    @staticmethod
    def capture_screen() -> str:
        """Captures the primary screen and returns a base64 encoded string."""
        try:
            # Capture the entire screen
            screenshot = ImageGrab.grab()
            
            # Save to bytes
            buffered = io.BytesIO()
            screenshot.save(buffered, format="PNG")
            
            # Encode to base64
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return img_str
        except Exception as e:
            logger.error(f"Vision Capture Failed: {e}")
            return ""

    @staticmethod
    def analyze_screen(prompt: str = "What is on my screen?") -> str:
        """Uses a Vision-capable LLM to analyze the current screen."""
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return "Vision API key missing."

        image_base64 = VisionService.capture_screen()
        if not image_base64:
            return "Unable to capture screen."

        try:
            client = Groq(api_key=api_key)
            # Using llama-3.2-11b-vision-preview or similar if available on Groq
            # For now, we use the standard completion if vision is not yet fully global,
            # but ideally we use a vision model.
            
            # NOTE: Groq's vision models are in preview. 
            # If not available, we can use a placeholder or fallback.
            model = "llama-3.2-11b-vision-preview"
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Vision Analysis Failed: {e}")
            return f"I can see your screen, but I'm having trouble analyzing it: {str(e)}"
