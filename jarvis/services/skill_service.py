"""
JARVIS — Skill Service (Unified Skill Manager)
Consolidates all system actions: Automation, Data Tools, and File Handling.
"""

import os
import platform
import subprocess
import webbrowser
import urllib.parse
import datetime
import random
import glob
import uuid
import requests
import logging
import yfinance as yf
import pywhatkit as kit
from jarvis.tools.firecrawl_search import firecrawl_search

logger = logging.getLogger("JARVIS")

COUNTRY_TIME_OFFSETS = {
    "us": -5, "usa": -5, "america": -5, "new york": -5, "washington": -5,
    "uk": 0, "london": 0, "greenwich": 0, "india": 5.5, "bangalore": 5.5, "mumbai": 5.5, "delhi": 5.5,
    "saudi": 3, "riyadh": 3, "mexico": -6, "dubai": 4, "uae": 4,
    "tokyo": 9, "japan": 9, "australia": 10, "sydney": 10, "france": 1, "paris": 1, "germany": 1, "berlin": 1,
    "singapore": 8, "china": 8, "beijing": 8, "moscow": 3, "russia": 3
}

class SkillService:
    # ─── DATA TOOLS ───────────────────────────────────────────
    @staticmethod
    def get_stock_price(query: str) -> str:
        COMPANY_TO_TICKER = {
            "apple": "AAPL", "tesla": "TSLA", "microsoft": "MSFT", "google": "GOOGL",
            "alphabet": "GOOGL", "amazon": "AMZN", "nvidia": "NVDA", "meta": "META",
            "facebook": "META", "netflix": "NFLX", "bitcoin": "BTC-USD", "ethereum": "ETH-USD",
            "reliance": "RELIANCE.NS", "tcs": "TCS.NS", "infosys": "INFY.NS", 
            "hdfc": "HDFCBANK.NS", "icici": "ICICIBANK.NS", "sbi": "SBIN.NS",
            "wipro": "WIPRO.NS", "amd": "AMD", "intel": "INTC", "spotify": "SPOT", "disney": "DIS",
            "gold": "GC=F", "silver": "SI=F", "crude oil": "CL=F", "oil": "CL=F", "platinum": "PL=F"
        }
        query_low = query.lower()
        symbol = next((ticker for company, ticker in COMPANY_TO_TICKER.items() if company in query_low), None)
        if not symbol:
            words = query.split()
            symbol = next((w.strip("?.,!").upper() for w in words if w.strip("?.,!").upper() in COMPANY_TO_TICKER.values()), None)
        
        if not symbol: return "Sorry, I couldn't identify which stock you want."
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.info
            price = data.get("currentPrice") or data.get("regularMarketPrice")
            if not price: return f"I couldn't find a live price for {symbol}."
            return f"The current price of {data.get('shortName', symbol)} is {price} {data.get('currency', 'USD')}."
        except Exception as e:
            return f"I couldn't retrieve the market data for {symbol}."

    @staticmethod
    def get_currency_conversion(amount: float, source: str, target: str) -> str:
        """Fetches live currency conversion using yfinance (e.g. USDINR=X)."""
        s, t = source.upper(), target.upper()
        if s == t: return f"{amount:,.2f} {s}."
        
        try:
            # yfinance uses symbols like USDINR=X for exchange rates
            symbol = f"{s}{t}=X"
            ticker = yf.Ticker(symbol)
            # Try to get the latest regular market price
            rate = ticker.fast_info.get('last_price')
            
            if not rate:
                # Fallback to hardcoded benchmarks if API fails
                benchmarks = {"USD": 1.0, "INR": 84.05, "EUR": 0.92, "GBP": 0.79}
                if s in benchmarks and t in benchmarks:
                    rate = benchmarks[t] / benchmarks[s]
                else:
                    return f"I don't have the live conversion rate for {s} to {t} right now."
            
            final_val = amount * rate
            return f"{amount:,.2f} {s} is approximately {final_val:,.2f} {t} (Rate: {rate:.2f})."
        except:
            return f"I'm having trouble fetching live exchange rates at the moment."

    @staticmethod
    def get_weather(city: str) -> str:
        """Fetches live weather and returns a clean, spoken-friendly sentence."""
        city_name = (city or "Bangalore").strip().title()
        try:
            # Using format="%C+and+%t" for "Cloudy and +31°C"
            url = f"https://wttr.in/{city_name}?format=%C+and+%t"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                result = response.text.strip().replace("+", "")
                # Clean up punctuation and return natural sentence
                return f"Current weather in {city_name} is {result}."
        except Exception as e:
            logger.error(f"Weather Fetch Error: {e}")
        return f"I'm having trouble getting the weather for {city_name} right now."

    @staticmethod
    def get_current_time(location: str = "india") -> str:
        """Calculates current time for a given city or country based on UTC offsets."""
        loc_low = location.lower().strip()
        offset = COUNTRY_TIME_OFFSETS.get(loc_low, 5.5)
        
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        target = utc_now + datetime.timedelta(hours=offset)
        
        return f"The current time in {location.title()} is {target.strftime('%I:%M %p')}."

    # ─── AUTOMATION TOOLS ──────────────────────────────────────
    @staticmethod
    def open_website(app_name: str) -> str:
        url_map = {
            "google": "https://www.google.com", "youtube": "https://www.youtube.com",
            "whatsapp": "https://web.whatsapp.com", "github": "https://github.com",
            "chatgpt": "https://chat.openai.com", "gmail": "https://mail.google.com"
        }
        url = url_map.get(app_name.lower().strip())
        if url:
            webbrowser.open(url)
            return f"Opening {app_name.title()}."
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(app_name)}")
        return f"Searching Google for {app_name}."

    @staticmethod
    def close_app(app_name: str) -> str:
        if platform.system() == "Windows":
            proc_map = {"chrome": "chrome.exe", "edge": "msedge.exe", "whatsapp": "WhatsApp.exe", "browser": "chrome.exe"}
            target = proc_map.get(app_name.lower().strip(), f"{app_name}.exe")
            subprocess.run(["taskkill", "/F", "/IM", target, "/T"], check=False, capture_output=True)
            return f"Closed {app_name}."
        return "Closing apps is only supported on Windows."

    @staticmethod
    def play_youtube(query: str) -> str:
        try:
            kit.playonyt(query)
            return f"Playing '{query}' on YouTube."
        except:
            webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}")
            return f"Searching YouTube for '{query}'."

    # ─── FILE TOOLS ───────────────────────────────────────────
    @staticmethod
    def open_system_folder(folder_name: str) -> str:
        user_profile = os.environ.get('USERPROFILE', '')
        known = {"desktop": "Desktop", "documents": "Documents", "downloads": "Downloads", "jarvis": os.getcwd()}
        path = os.path.join(user_profile, known.get(folder_name.lower(), ""))
        if path and os.path.exists(path):
            os.startfile(path)
            return f"Opened {folder_name.title()}."
        return f"Could not find folder: {folder_name}"

    @staticmethod
    def search_and_open_file(filename: str) -> str:
        target = filename.lower()
        user_prof = os.environ.get('USERPROFILE', '')
        search_dirs = [os.path.join(user_prof, d) for d in ['Desktop', 'Documents', 'Downloads']] + [os.getcwd()]
        for root_dir in search_dirs:
            if not os.path.exists(root_dir): continue
            for dirpath, _, filenames in os.walk(root_dir):
                for f in filenames:
                    if target in f.lower():
                        os.startfile(os.path.join(dirpath, f))
                        return f"Opened file: {f}"
        return f"Could not find any file matching '{filename}'."

    # ─── IMAGE TOOLS ──────────────────────────────────────────
    @staticmethod
    def generate_image(prompt: str) -> str:
        from huggingface_hub import InferenceClient
        token = os.environ.get("HUGGINGFACE_API_TOKEN")
        if not token: return ""
        
        models = [os.environ.get("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell"), "stabilityai/stable-diffusion-xl-base-1.0"]
        image_bytes = None
        for model in models:
            try:
                client = InferenceClient(model=model, token=token.strip())
                image = client.text_to_image(prompt, timeout=30)
                import io
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                image_bytes = img_byte_arr.getvalue()
                break
            except: continue

        if not image_bytes: # Pollinations fallback
            try:
                poll_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?nologo=true"
                res = requests.get(poll_url, timeout=30)
                if res.status_code == 200: image_bytes = res.content
            except: pass

        if not image_bytes: return ""
        filename = f"gen_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join("static", filename)
        os.makedirs("static", exist_ok=True)
        with open(filepath, "wb") as f: f.write(image_bytes)
        return f"http://localhost:8000/static/{filename}"
