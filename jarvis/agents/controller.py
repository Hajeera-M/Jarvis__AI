"""
JARVIS-X Master Controller — True Intent/Entity Architecture
Orchestration layer managing Services and Skill execution.
Decides if a query needs a Tool, a Web Search, or AI reasoning.
"""

from typing import Optional, Dict, Tuple, Set, Any
import logging
from jarvis.services.memory_service import MemoryService
from jarvis.services.ai_service import AIService
from jarvis.services.tool_service import ToolService

# ─────────────────────── AGENT ORCHESTRATOR ──────────────────

class MasterController:
    @staticmethod
    def handle_user_input(user_input: str, context: Dict[str, Any], user_id: str = "default_user") -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        True Agent Controller.
        Returns: (response_data_dict, updated_context)
        """
        query = user_input.lower()
        response = ""
        source = "ai"
        lang = "en"

        # 1. Fetch persistent history (GIVES AI MEMORY)
        history = MemoryService.get_recent_history(user_id, limit=5)

        # 2. INTELLIGENT AGENT ROUTING (Logic-based Dispatcher)
        
        # A. Stock Price (yfinance)
        if any(w in query for w in ["price", "stock", "market", "trade"]):
            response = ToolService.get_stock_price(user_input)
            source = "tool"
            
        # B. Time (Internal Logic)
        elif "time" in query:
            # Extract country from query or entities
            country_ent = context.get("entities", {}).get("country", "india")
            response = ToolService.get_current_time(country_ent)
            source = "tool"

        # C. General News/Search (Firecrawl)
        elif any(w in query for w in ["news", "latest", "search", "weather"]):
            response = ToolService.web_search(user_input)
            source = "tool"

        # D. Reasoning (Groq + History)
        else:
            response, lang = AIService.get_reasoning(user_input, history)
            source = "ai"

        # 3. PERSISTENT LONG-TERM MEMORY (SAVE INTERACTION)
        if response:
            MemoryService.save_interaction(user_id, user_input, response)

        # 4. Standardized Output Format
        output = {
            "response": response,
            "source": source,
            "language": lang
        }

        # 5. Intent Tracking for follow-ups
        context["last_query"] = user_input
        
        return output, context
