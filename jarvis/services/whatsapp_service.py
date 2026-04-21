"""
JARVIS — WhatsApp Automation Service
Controls WhatsApp Web via pywhatkit.
"""

import pywhatkit as kit
import webbrowser
import urllib.parse
import time

class WhatsAppService:
    @staticmethod
    def open_whatsapp() -> str:
        """Just opens WhatsApp Web."""
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp Web."

    @staticmethod
    def send_message(contact: str, message: str) -> str:
        """Sends a message immediately using URL scheme for stability, falling back to pywhatkit if it's a direct phone number."""
        contact = contact.strip()
        
        # If it's a 10 digit number or has a +, format it safely
        if contact.replace("+", "").isdigit() and len(contact) >= 10:
            phone_num = contact if contact.startswith("+") else f"+91{contact[-10:]}"
            try:
                kit.sendwhatmsg_instantly(phone_num, message, wait_time=10, tab_close=True)
                return f"Message sent to {contact}."
            except Exception as e:
                return f"Failed to send to {contact} automatically."
                
        # If it's a text name, WhatsApp Web URL scheme doesn't auto-send nicely without selenium.
        # But we can open web.whatsapp with a pre-filled text buffer.
        safe_msg = urllib.parse.quote(message)
        webbrowser.open(f"https://web.whatsapp.com/send?text={safe_msg}")
        return f"I've opened WhatsApp with your message ready to send to {contact.title()}."
