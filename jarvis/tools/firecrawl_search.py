from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firecrawl Client
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

if FIRECRAWL_API_KEY:
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
else:
    app = None

def clean_text(text):
    """
    Cleans markdown characters and returns only the first coherent sentence.
    """
    if not text:
        return ""
    # Remove common markdown symbols
    text = text.replace("#", "").replace("*", "").replace("`", "").replace("_", "")
    # Remove extra newlines and tabs
    text = text.replace("\n", " ").replace("\r", " ").strip()
    # Normalize spaces
    text = " ".join(text.split())
    
    # Return first sentence
    if "." in text:
        return text.split(".")[0] + "."
    return text[:200]

def firecrawl_search(query):
    """
    Performs a real-time search and scrapes the most relevant result using Firecrawl.
    Returns a clean, speakable snippet.
    """
    if not app:
        return "Firecrawl API key is missing. Please add it to your .env file."

    try:
        # Search for the query and get the first result
        result = app.search(query=query, limit=1)

        if result and "data" in result and len(result["data"]) > 0:
            content = result["data"][0].get("content", "")
            
            if not content:
                # Fallback to description/metadata if content is empty
                content = result["data"][0].get("description", "")
            
            if not content:
                return "I found the page, but there was no readable content."

            # Final Clean: Speakable and concise
            return clean_text(content)

        return "Sorry, I couldn't find any relevant real-time information."

    except Exception as e:
        print(f"[JARVIS Error] Firecrawl search failed: {e}")
        return "Unable to fetch live data right now due to a technical issue."

