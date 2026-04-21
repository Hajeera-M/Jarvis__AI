import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"


headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def generate_image(prompt):
    """
    Generates an image from a text prompt using Hugging Face Inference API.
    Returns (file_path, error_message).
    """
    if not HF_API_KEY:
        return None, "Hugging Face API Token not found in .env"

    try:
        print(f"[JARVIS Tool] Requesting image for: {prompt}...")
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=80
        )
        
        print("HF RESPONSE:", response.status_code)

        if response.status_code != 200:
            return None, "Image service temporarily unavailable"


        image_path = "generated_image.png"

        with open(image_path, "wb") as f:
            f.write(response.content)

        return image_path, None

    except Exception as e:
        print(f"[JARVIS Error] Image generation failed: {e}")
        return None, str(e)

if __name__ == "__main__":
    # Test the generator
    path, err = generate_image("A futuristic city at night")
    if path:
        print(f"Success! Image saved to {path}")
    else:
        print(f"Error: {err}")

