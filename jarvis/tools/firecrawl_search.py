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
        # Search for the query
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(app.search, query=query)
            result = future.result(timeout=15)

        # Handle New SDK Structure (v4+) - result is an object with 'web' attribute
        if hasattr(result, 'web') and result.web and len(result.web) > 0:
            first_res = result.web[0]
            # Try to get content, fallback to description
            content = getattr(first_res, 'content', "") or getattr(first_res, 'description', "")
            if content:
                return clean_text(content)

        # Handle Legacy SDK Structure - result is a dictionary with 'data'
        if isinstance(result, dict) and "data" in result and len(result["data"]) > 0:
            first_res = result["data"][0]
            content = first_res.get("content", "") or first_res.get("description", "")
            if content:
                return clean_text(content)

        return "Sorry, I couldn't find any relevant real-time information."

    except Exception as e:
        print(f"[JARVIS Error] Firecrawl search failed: {e}")
        return "Unable to fetch live data right now due to a technical issue."

