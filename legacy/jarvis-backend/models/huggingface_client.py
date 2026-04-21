"""
JARVIS — HuggingFace Client
Handles text generation via HuggingFace Inference API.
"""

from huggingface_hub import InferenceClient
from config import HUGGINGFACE_API_TOKEN, HUGGINGFACE_MODEL

_client = None


def _get_client() -> InferenceClient:
    global _client
    if _client is None:
        if not HUGGINGFACE_API_TOKEN:
            raise RuntimeError(
                "HUGGINGFACE_API_TOKEN is not set. Please add it to your .env file."
            )
        _client = InferenceClient(
            model=HUGGINGFACE_MODEL,
            token=HUGGINGFACE_API_TOKEN,
        )
    return _client


async def generate(prompt: str, system_prompt: str = "", temperature: float = 0.7, max_tokens: int = 1024) -> str:
    """
    Generate a response using HuggingFace Inference API.
    Used for final response generation after the agent pipeline.
    """
    client = _get_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat_completion(
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()

