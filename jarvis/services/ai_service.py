"""
JARVIS — AI Service
Friendly "Smart Companion" reasoning layer.
Detects language (EN/HI/UR/Hinglish) and matches conversation style.
"""

import re
from typing import List, Tuple, Dict, Any
from langdetect import detect
from jarvis.models.groq_model import think as groq_reason

LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ur": "Urdu",
    "hinglish": "Hinglish"
}

def detect_language(text: str) -> str:
    """
    Rule-based language detection:
    1. Devanagari -> Hindi
    2. Common Hinglish keywords -> Hinglish
    3. langdetect fallback
    """
    text_lower = text.lower().strip()
    
    # 1. Devanagari Check
    if re.search(r'[\u0900-\u097F]', text):
        return "hi"
    
    # 2. Hinglish Keywords Heuristic
    hinglish_keywords = [
        "kaise", "kyun", "kyu", "ho", "hai", "kar", "aap", "tum", "kya", 
        "toh", "ka", "ke", "ki", "ko", "gaya", "gye", "baat", "main", "hum",
        "rha", "rhi", "rhey", "theek", "thik", "acha", "achha"
    ]
    if any(rf"\b{word}\b" in text_lower for word in hinglish_keywords) or any(word in text_lower for word in ["karna", "baat"]):
        return "hinglish"
    
    # 3. Fallback to langdetect
    try:
        lang = detect(text)
        if lang in ["en", "hi", "ur"]:
            return lang
        return "en"
    except:
        return "en"

class AIService:
    @staticmethod
    def get_reasoning(cmd: str, context_str: str, owner_name: str, user_name: str, target_lang_code: str = "en") -> Tuple[str, str]:
        """
        Executes friendly companion-style reasoning with historical context.
        STRICT LANGUAGE MIRRORING enforced via target_lang_code.
        """
        # 1. Linguistic Mapping
        target_lang = LANG_MAP.get(target_lang_code, "English")

        # 2. Expert Prompt Engineering (Smart Companion Persona)
        system_prompt = (
            f"You are JARVIS, a high-premium AI Smart Companion. "
            f"OWNER: {owner_name}. CURRENT USER: {user_name}. "
            f"STRICT UNYIELDING RULE: MIRROR MODE. "
            f"You MUST reply in the same language as the user input ({target_lang}). "
            f"1. If input is English -> response MUST be 100% English. NO Hindi/Hinglish greetings (Aap/Kaise), NO Hinglish words. "
            f"2. If input is Hinglish -> response MUST be 100% Hinglish (Roman Hindi). Do NOT switch to pure English. "
            f"3. If input is Hindi -> response MUST be 100% Hindi (Devanagari). "
            f"Do NOT mix languages. Do NOT summarize in a different language unless explicitly asked.\n"
            f"PERSONALITY: Friendly, helpful, confident, and professional.\n"
            f"DEMO STABILITY RULES:\n"
            f"- NEVER say 'I don't have real-time updates', 'temporarily unavailable', 'would you like me to', or 'information is limited'.\n"
            f"- For news or global events, ALWAYS provide a confident 2-3 sentence overview based on your broad intelligence.\n"
            f"- Your goal is to sound brilliant and well-informed at all times.\n"
            f"CRITICAL: Keep spoken output under 3 SENTENCES. Do NOT use markdown or emojis."
        )
        
        # 3. Prompt Construction
        final_prompt = (
            f"IDENTITY CONTEXT:\n- Owner: {owner_name}\n- User: {user_name}\n\n"
            f"CONVERSATION CONTEXT:\n{context_str}\n\n"
            f"User: {cmd}\nAI:"
        )
        
        result = groq_reason(final_prompt, system_prompt=system_prompt)
        if not result:
            return "Thinking...", target_lang_code
            
        # 4. Professional Polish
        text = str(result).strip()
        # Clean up some common robot pre-fixes
        text = text.replace("It seems", "").replace("I think", "").replace("I believe", "").strip()
        return text, target_lang_code

