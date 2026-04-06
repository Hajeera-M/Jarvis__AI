from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query):
    try:
        response = client.search(query=query, search_depth="advanced")

        if response and "results" in response and len(response["results"]) > 0:
            content = response["results"][0]["content"]
            # Speak only the first sentence for a smarter, concise feel
            first_sentence = content.split(".")[0]
            if len(first_sentence) < 10 and "." in content: # Handle very short fragments
                 first_sentence = content.split(".")[0] + content.split(".")[1]
            return first_sentence + "."


        return "Sorry, I couldn't find relevant information."

    except Exception as e:
        print(f"[JARVIS Error] Tavily Search failed: {e}")
        return "Unable to fetch live data right now"
