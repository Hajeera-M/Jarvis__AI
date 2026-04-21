"""
JARVIS — Groq Model Wrapper
Handles reasoning/thinking calls via Groq API.
"""

from jarvis.config import GROQ_API_KEY, GROQ_REASONING_MODEL
import sys

_groq_client = None

def _get_groq_client():
    global _groq_client
    if _groq_client is None:
        try:
            from groq import Groq
            if not GROQ_API_KEY:
                print("Error: GROQ_API_KEY is not set.")
                print("Please get a free key from console.groq.com and add it to your .env file.")
                sys.exit(1)
            _groq_client = Groq(api_key=GROQ_API_KEY)
        except ImportError:
            print("Error: 'groq' package not installed. Run 'pip install groq'")
            sys.exit(1)
    return _groq_client


def think(prompt: str, system_prompt: str = "", temperature: float = 0.7) -> str:
    """
    Send a reasoning/thinking request to Groq LLM.
    Used by the planner and reflection agents.
    
    Args:
        prompt: User input or context to reason about
        system_prompt: System instructions (Default: Multi-lingual Voice Assistant)
        temperature: Creativity vs precision control

        
    Returns:
        Generated text string
    """
    client = _get_groq_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=GROQ_REASONING_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=2048,
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[JARVIS Error] Groq API call failed: {e}")
        return ""

