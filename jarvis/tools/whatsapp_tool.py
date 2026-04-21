"""
JARVIS — WhatsApp Tool
Sends WhatsApp messages using pywhatkit.
"""

import pywhatkit as kit
import datetime

def send_whatsapp_message(contact_info: str, message: str) -> str:
    """
    Sends a WhatsApp message to a given number or contact name.
    
    Args:
        contact_info: Phone number (with country code) or contact name
        message: The message text to send
        
    Returns:
        Status message string
    """
    # In a real assistant, we would resolve 'contact_name' to a number using memory
    # For now, we assume contact_info IS the phone number if it starts with '+'
    
    phone_number = contact_info.strip()
    if not phone_number.startswith("+"):
        # Placeholder for contact resolution
        return f"Error: '{contact_info}' is not a valid phone number. Please provide it in international format starting with '+'."

    try:
        # sendwhatmsg_instantly opens the browser and clicks send
        # It requires the user to be logged into WhatsApp Web in their default browser
        print(f"[Tool: WhatsApp] Sending message to {phone_number}...")
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=True)
        return f"Successfully sent WhatsApp message to {phone_number}."
    except Exception as e:
        return f"Failed to send WhatsApp message: {e}"

