import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("JARVIS")

class SearchService:
    @staticmethod
    def get_live_search(query: str) -> str:
        """
        Pulls snippets from DuckDuckGo HTML (stable) or falls back to Wikipedia.
        """
        logger.info(f"[Search Service] Executing live search for: {query}")
        
        # Tier 1: DuckDuckGo HTML Scraping (Avoids API 403s)
        try:
            url = f"https://duckduckgo.com/html/?q={query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # DDG HTML result snippets are typically in 'a' tags with result__snippet class
                snippets = [s.get_text().strip() for s in soup.find_all("a", class_="result__snippet")]
                
                if snippets:
                    combined = " ".join(snippets[:3])
                    if len(combined) > 50: # Ensure meaningful content
                         return f"According to currently available reports: {combined[:600]}"
        except Exception as e:
            logger.warning(f"Search Tier 1 (Scraping) Failed: {e}")

        # Tier 2: Wikipedia API Fallback (Historical/Contextual)
        try:
            # Enhanced heuristic to extract a clean topic
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
                    return f"Here is the context based on current records: {extract}"
        except Exception as e:
            logger.warning(f"Search Tier 2 (Wikipedia) Failed: {e}")

        # Signal failure to controller for AI fallback
        return ""
