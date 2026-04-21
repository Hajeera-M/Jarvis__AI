"""
JARVIS — System Tool
Handles system-level operations like time, dates, and opening apps.
"""

import datetime
import platform
import webbrowser
import os

def get_system_info(query_type: str = "all") -> str:
    """
    Return basic system context: time, date, OS.
    """
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d, %Y")
    os_name = platform.system()
    os_rel = platform.release()
    
    if query_type == "time":
        return f"The current time is {time_str}"
    elif query_type == "date":
        return f"Today's date is {date_str}"
    
    return f"Time: {time_str}\nDate: {date_str}\nPlatform: {os_name} {os_rel}"

def open_url(url: str) -> str:
    """
    Open a URL in the default system browser.
    """
    if not url.startswith("http"):
        url = "https://" + url
        
    try:
        webbrowser.open(url)
        return f"Successfully opened {url} in your default browser."
    except Exception as e:
        return f"Failed to open URL: {e}"

