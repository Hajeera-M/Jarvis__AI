from models.groq_model import think

def generate(prompt: str, system_prompt: str = "", temperature: float = 0.7, max_new_tokens: int = 1024) -> str:
    """
    JARVIS — Generation Wrapper (Redirected to Groq)
    """
    print("[JARVIS] Using Groq for generation (HuggingFace bypassed)")
    return think(prompt, system_prompt, temperature)

