import requests
from bs4 import BeautifulSoup

def get_news():
    """
    Fetches the top 3 news headlines from Google News RSS feed (India).
    """
    url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "xml")

        items = soup.find_all("item")

        headlines = []

        # Get top 3 news headlines
        for item in items[:3]:
            headlines.append(item.title.text)

        if not headlines:
            return "I couldn't find any news at the moment."

        return "Here are the latest news: " + ". ".join(headlines)

    except Exception as e:
        print(f"[JARVIS Error] News fetch failed: {e}")
        return "Sorry, I'm having trouble fetching the news right now."
def get_world_news():
    """
    Fetches the top 3 global news headlines from Google News RSS feed (US).
    """
    url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "xml")

        items = soup.find_all("item")
        headlines = [item.title.text for item in items[:3]]

        if not headlines:
            return "I couldn't find any global news at the moment."

        return "Here is the latest world news: " + ". ".join(headlines)

    except Exception as e:
        print(f"[JARVIS Error] World news fetch failed: {e}")
        return "Sorry, I'm having trouble fetching global news."

import re

def extract_city(text):
    """
    Intelligently extracts city name from phrases like 'weather in Mexico' or 'status of London'.
    """
    # Look for 'in [City]' or 'of [City]' or 'at [City]'
    match = re.search(r"(?:in|of|at)\s+([a-zA-Z\s]+)", text, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        # Verify it's not just a filler or stop word
        if city.lower() not in ["the", "this", "my", "your"]:
            return city
            
    # Fallback to last word if no preposition found (if more than 1 word)
    words = text.split()
    if len(words) > 1 and words[-1].lower() != "weather":
        return words[-1].strip()
        
    return "Bangalore"

def get_weather(user_input):
    """
    Fetches the current weather for a city extracted from user input.
    """
    city = extract_city(user_input)
    url = f"https://wttr.in/{city}?format=3"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # Fix encoding for Windows console/voice output
            clean_text = response.text.encode('latin1').decode('utf-8').strip()
            return f"Weather status for {city}: {clean_text}"
        return f"I couldn't get the weather status right now."

    except Exception as e:
        print(f"[JARVIS Error] Weather fetch failed: {e}")
        return "Unable to fetch the weather status."

def get_bitcoin_price_value():
    """
    Fetches ONLY the numeric Bitcoin price in USD (integer).
    Used for structured memory and conversions.
    """
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=5)
        return int(float(response.json()["price"]))
    except:
        return None

def get_bitcoin_price():
    """
    Fetches the current Bitcoin price in USD from Binance.
    """
    price = get_bitcoin_price_value()
    if price:
        return f"The current Bitcoin price is {price} US dollars."
    return "I'm unable to fetch the latest Bitcoin price right now."



if __name__ == "__main__":
    # Test the news tool
    print("--- INDIA NEWS ---")
    print(get_news())
    print("\n--- WORLD NEWS ---")
    print(get_world_news())
    print("\n--- WEATHER ---")
    print(get_weather())
    print("\n--- BITCOIN ---")
    print(get_bitcoin_price())

