"""
JARVIS — Tool Service
Real-time data fetching for stocks, time, and external search.
"""

from typing import Dict, Any, Optional
import yfinance as yf
import datetime
import random
from jarvis.tools.firecrawl_search import firecrawl_search

# Configuration for time offsets (moved to service)
COUNTRY_TIME_OFFSETS = {
    "us": -5, "usa": -5, "america": -5,
    "uk": 0, "london": 0, "india": 5.5,
    "saudi": 3, "mexico": -6, "dubai": 4,
    "japan": 9, "australia": 10, "france": 1, "germany": 1,
}

class ToolService:
    @staticmethod
    def get_stock_price(query: str) -> str:
        """
        Fetches high-fidelity stock data using yfinance.
        """
        # Simple symbol extractor (handles common ones or uppercase words)
        words = query.split()
        symbol = None
        for w in words:
            w_clean = w.strip("?.,!").upper()
            if w_clean in ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NVDA", "BTC-USD"]:
                symbol = w_clean
                break
        
        # Fallback to TSLA if no symbol found but 'stock' mentioned
        if not symbol:
            symbol = "TSLA" 

        try:
            ticker = yf.Ticker(symbol)
            data = ticker.info
            price = data.get("currentPrice") or data.get("regularMarketPrice")
            
            if not price:
                return f"I couldn't find a live price for {symbol}."
                
            currency = data.get("currency", "USD")
            name = data.get("shortName", symbol)
            
            return f"The current price of {name} ({symbol}) is {price} {currency}."
        except Exception as e:
            return f"Error fetching stock data for {symbol}: {str(e)}"

    @staticmethod
    def get_current_time(country: str = "india") -> str:
        """
        Returns accurate time based on UTC offset.
        """
        country = country.lower()
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        
        offset = COUNTRY_TIME_OFFSETS.get(country, 5.5) # Default to India
        target = utc_now + datetime.timedelta(hours=offset)
        time_str = target.strftime("%I:%M %p")
        
        responses = [
            f"The current time in {country.title()} is {time_str}.",
            f"It's {time_str} in {country.title()} right now.",
        ]
        return random.choice(responses)

    @staticmethod
    def web_search(query: str) -> str:
        """
        Uses Firecrawl/General search for news and non-structured data.
        """
        try:
            return firecrawl_search(query)
        except:
            return "I'm unable to access live news at the moment."
