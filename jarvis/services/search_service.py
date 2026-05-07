import requests
import logging
from bs4 import BeautifulSoup
from jarvis.tools.firecrawl_search import firecrawl_search
from jarvis.tools.web_search import get_news # Google News RSS tool already exists

logger = logging.getLogger("JARVIS")

class SearchService:
    @staticmethod
    def get_live_search(query: str) -> str:
        """
        Multi-tier search orchestrator:
        Tier 1: Google News (for news-specific intent)
        Tier 2: Firecrawl (High-fidelity live scraping)
        Tier 3: Wikipedia (Contextual fallback)
        """
        logger.info(f"[Search Service] Executing live search for: {query}")
        
        # Priority Tier: News Intent
        if any(w in query.lower() for w in ["news", "latest headlines", "what is happening"]):
            news_resp = get_news()
            if "I couldn't find any news" not in news_resp:
                return news_resp

        # Tier 1: Firecrawl (Scraping/Live Search)
        try:
            fire_resp = firecrawl_search(query)
            if fire_resp and "Sorry, I couldn't find" not in fire_resp and "Firecrawl API key" not in fire_resp:
                # Use AI to synthesize the raw firecrawl response into a clean answer
                from jarvis.services.ai_service import AIService
                summary, _ = AIService.get_reasoning(
                    f"Summarize this search data for the query '{query}': {fire_resp[:2000]}", 
                    context_str="SEARCH_SYNTHESIS_MODE", 
                    owner_name="Hajeera", 
                    user_name="Hajeera"
                )
                return summary if summary else f"Based on live search results: {fire_resp[:300]}..."
        except Exception as e:
            logger.warning(f"Search Tier 1 (Firecrawl) Failed: {e}")

        # Tier 2: Wikipedia Fallback (Historical/Contextual)
        try:
            # ... existing wiki logic ...
            clean_q = query.lower()
            for noise in ["latest update on", "news regarding", "what is happening in", "tell me about", "what's going on in", "situation in", "is happening in"]:
                clean_q = clean_q.replace(noise, "")
            
            topic = clean_q.strip("? .!").title()
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
            response = requests.get(wiki_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                extract = data.get("extract", "")
                if extract:
                    # Synthesize Wikipedia too
                    from jarvis.services.ai_service import AIService
                    summary, _ = AIService.get_reasoning(
                        f"Provide a concise summary based on this Wikipedia extract for '{topic}': {extract}", 
                        context_str="WIKI_SYNTHESIS_MODE", 
                        owner_name="Hajeera", 
                        user_name="Hajeera"
                    )
                    return summary if summary else extract
        except Exception as e:
            logger.warning(f"Search Tier 2 (Wikipedia) Failed: {e}")

        return ""
