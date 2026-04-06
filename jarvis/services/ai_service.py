"""
JARVIS — AI Service
Intelligence layer for reasoning and linguistic adaptability.
"""

from typing import List, Tuple
from langdetect import detect
from jarvis.models.groq_model import think as groq_reason
from jarvis.memory.postgres_db import Conversation

LANG_MAP = {
    "en": "English",
    "hi": "Hindi"
}

def detect_language(text: str) -> str:
    """Detects primary language and falls back to English."""
    try:
        lang = detect(text)
        return lang if lang in ["en", "hi"] else "en"
    except:
        return "en"

class AIService:
    @staticmethod
    def get_reasoning(cmd: str, history: List[Conversation]) -> Tuple[str, str]:
        """
        Executes hybrid-language reasoning with historical context.
        Returns: (response_text, lang_code)
        """
        # 1. Format context string
        history_str = ""
        for item in history:
            history_str += f"User: {item.user_message}\nAI: {item.ai_response}\n"
        
        # 2. Context Truncation
        if len(history_str) > 1000:
            history_str = "..." + history_str[-1000:]
            
        # 3. Dynamic Language Instructions
        lang_code = detect_language(cmd)
        target_lang = LANG_MAP.get(lang_code, "English")

        system_prompt = (
            f"You are JARVIS-X, the user's high-premium AI agent. "
            f"DETECTED LANGUAGE: {target_lang}. "
            f"STRICT RULE: Respond ONLY in the user's language ({target_lang}). "
            f"If the user uses Hinglish, respond in natural, smooth Hinglish. "
            f"CRITICAL: Use previous context to answer follow-up questions. "
            f"If the user mentioned a name or preference earlier, acknowledge it. "
            f"Respond in ONE short, precise, but helpful sentence. "
            f"Reference context if relevant."
        )
        
        # 4. Prompt Construction
        final_prompt = history_str + f"User: {cmd}\nAI:"
        
        result = groq_reason(final_prompt, system_prompt=system_prompt)
        if not result:
            return "Seeking clarity from the Groq mainframe...", lang_code
            
        # 5. Professional Polish
        text = str(result).strip()
        text = text.replace("It seems", "").replace("I think", "").replace("I believe", "").strip()
        if "." in text:
            text = text.split(".")[0] + "."
        return text, lang_code
