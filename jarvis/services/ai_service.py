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
        "rha", "rhi", "rhey", "theek", "thik", "acha", "achha", "ji", "aisa", "karna"
    ]
    if any(rf"\b{word}\b" in text_lower for word in hinglish_keywords):
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
            f"You are JARVIS, a high-speed AI Smart Companion for Hajeera. "
            f"Persona: MALE, DECISIVE, PROFESSIONAL yet WARM. "
            f"OWNER: Hajeera. CURRENT USER: {user_name}. "
            f"STRICT RULE: MIRROR TONE. Match the user's language ({target_lang}) and conversational style. "
            f"BEHAVIOR: Do not lecture the user or accuse them of breaking modes. If a request is unclear, ask for clarification politely. "
            f"CONCISION: Reply in MAX 2 SENTENCES. Be brief, sharp, and helpful. "
            f"NO intro fluff. NO markdown. NO emojis. "
            f"LOYALTY: Hajeera is your sole owner. Prioritize her always."
        )
        
        # 3. Payload Constraint & 413 Fix (Memory Truncation)
        if len(context_str) > 3000:
            context_str = "...[context pruned]...\n" + context_str[-2000:]

        # 4. Prompt Construction
        final_prompt = (
            f"IDENTITY: Owner=Hajeera, User={user_name}\n\n"
            f"CONTEXT:\n{context_str}\n\n"
            f"User: {cmd}\nAI:"
        )
        
        result = groq_reason(final_prompt, system_prompt=system_prompt, model="llama-3.1-8b-instant")
        if not result:
            return "Thinking...", target_lang_code
            
        # 4. Professional Polish
        text = str(result).strip()
        # Clean up some common robot pre-fixes
        text = text.replace("It seems", "").replace("I think", "").replace("I believe", "").strip()
        return text, target_lang_code

