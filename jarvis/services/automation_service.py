"""
JARVIS — Automation Service
Controls browser instances, searches, and executes desktop applications.
"""

import webbrowser
import urllib.parse
import os
import pywhatkit as kit
import subprocess

class AutomationService:
    @staticmethod
    def search_google(query: str) -> str:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return f"I have opened Google and searched for '{query}'."

    @staticmethod
    def play_youtube(query: str) -> str:
        try:
            kit.playonyt(query)
            return f"Playing '{query}' on YouTube."
        except Exception as e:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            webbrowser.open(url)
            return f"I have opened YouTube to search for '{query}'."

    @staticmethod
    def open_website(app_name: str) -> str:
        url_map = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "whatsapp": "https://web.whatsapp.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "github": "https://github.com",
            "chatgpt": "https://chat.openai.com",
            "gmail": "https://mail.google.com"
        }
        name_lower = app_name.lower().strip()
        url = url_map.get(name_lower)
        
        if url:
            webbrowser.open(url)
            return f"Opening {app_name.title()}."
        else:
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(app_name)}"
            webbrowser.open(search_url)
            return f"I couldn't find a direct link for {app_name}, so I searched Google for it."

    @staticmethod
    def open_desktop_app(app_name: str) -> str:
        import platform
        if platform.system() == "Windows":
            try:
                # 'start' command triggers windows shell execution routing
                subprocess.Popen(['start', app_name], shell=True)
                return f"Opening {app_name} on your computer."
            except Exception as e:
                return f"Failed to open {app_name}. {str(e)}"
        return "Desktop automation is only fully supported on Windows."
