import os
import io
import time
import requests
import logging
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

class ImageGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        load_dotenv()
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        self.model = os.getenv("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")
        
        # Folder for images
        self.output_dir = os.path.join(os.path.dirname(__file__), "generated_images")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if not self.api_token:
            self.logger.warning("HUGGINGFACE_API_TOKEN not found in .env. Image generation will fail.")

    def enhance_prompt(self, user_prompt):
        """
        Enhances a simple user prompt into a high-quality descriptive prompt.
        """
        # Remove common command words
        clean_prompt = user_prompt.lower()
        for word in ["generate", "create", "draw", "an image of", "a picture of", "image of", "show me"]:
            clean_prompt = clean_prompt.replace(word, "")
        
        clean_prompt = clean_prompt.strip()
        
        # Add high-quality qualifiers
        enhanced = (
            f"A highly detailed, hyper-realistic, 4k digital art piece of {clean_prompt}. "
            f"Cinematic lighting, ultra HD, masterpiece, focused, sharp textures."
        )
        return enhanced

    def generate_image(self, user_prompt):
        """
        Calls Hugging Face Inference API to generate an image using direct requests.
        """
        if not self.api_token:
            return None, "Error: Hugging Face API token is missing. Please check your .env file."

        enhanced_prompt = self.enhance_prompt(user_prompt)
        self.logger.info(f"Generating image for: {enhanced_prompt}")

        API_URL = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": enhanced_prompt}

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                
                # Save the image
                timestamp = int(time.time())
                filename = f"generated_{timestamp}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                image.save(filepath)
                self.logger.info(f"Image saved to: {filepath}")
                
                # Open/Display image
                try:
                    image.show()
                except Exception as e:
                    self.logger.warning(f"Could not automatically display image: {str(e)}")

                return filepath, f"Image successfully generated and saved as {filename}."
            
            else:
                error_info = response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
                self.logger.error(f"API Error ({response.status_code}): {error_info}")
                
                if response.status_code == 503:
                    return None, "Error: Service unavailable. The model is likely loading. Please try again in a few seconds."
                elif response.status_code == 401:
                    return None, "Error: Invalid Hugging Face API token."
                
                return None, f"Error: API returned status {response.status_code}. {error_info}"

        except requests.exceptions.Timeout:
            return None, "Error: The request to Hugging Face timed out. Please check your connection."
        except Exception as e:
            self.logger.error(f"Unexpected Error: {str(e)}")
            return None, f"Error: An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    # Test cases (Will fail without API Token)
    logging.basicConfig(level=logging.INFO)
    gen = ImageGenerator()
    path, msg = gen.generate_image("A futuristic city at night")
    print(msg)
