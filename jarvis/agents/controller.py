import datetime
import webbrowser
import os
from models.groq_model import think as groq_reason

# Optional: Initializing memory manager lazily if still needed for history
_memory_manager = None
def _get_memory():
    global _memory_manager
    if _memory_manager is None:
        try:
            from memory import memory_manager
            _memory_manager = memory_manager
        except ImportError:
            pass
    return _memory_manager

def handle_user_input(user_input: str) -> str:
    """
    JARVIS — Simplified Agent Handler (Specific Command Overrides)
    """
    try:
        user_input_low = user_input.lower()

        # 1. TIME
        if "time" in user_input_low:
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {now}."

        # 🔥 STOP COMMAND
        if any(cmd in user_input_low for cmd in ["stop", "jarvis stop", "quiet", "shut up"]):
            from voice.text_to_speech import stop_speech
            stop_speech()
            return "Stopped."




        # 2. GOOGLE / CHROME
        if "open google" in user_input_low:
            webbrowser.open("https://www.google.com")
            return "Opening Google in your browser."

        if any(cmd in user_input_low for cmd in ["close google", "close chrome"]):
            # Forcing shutdown of Chrome process as requested
            os.system("taskkill /f /im chrome.exe")
            return "Closing Google Chrome."

        # 3. YOUTUBE / MEDIA
        if "play" in user_input_low:
            query = user_input_low.replace("play", "").replace("jarvis", "").strip()
            print(f"[JARVIS Agent] Overriding with local YOUTUBE AUTO-PLAY for: {query}")
            try:
                import pywhatkit
                pywhatkit.playonyt(query)
                return f"Playing {query} on YouTube."
            except Exception as e:
                return f"I couldn't play {query}: {e}"

        if "open youtube" in user_input_low:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

        if "search youtube" in user_input_low:
            query = user_input_low.replace("search youtube", "").strip()
            url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(url)
            return f"Searching YouTube for {query}."

        # 4. WHATSAPP
        if "open whatsapp" in user_input_low:
            webbrowser.open("https://web.whatsapp.com")
            return "Opening WhatsApp Web."

        if "send whatsapp message" in user_input_low:
            try:
                import pywhatkit
                pywhatkit.sendwhatmsg_instantly("+910000000000", "Hello from JARVIS", wait_time=15)
                return "Opening WhatsApp Web to send your message."
            except Exception as we:
                return f"I couldn't send the WhatsApp message: {we}"

        # 5. SEARCH (Generic Search Handler)
        if "search" in user_input_low:
            query = user_input_low.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {query} on Google."

        # 6. FILES / FOLDERS
        if "open downloads" in user_input_low:
            os.startfile("C:\\Users\\Hajeera\\Downloads")
            return "Opening your Downloads folder."

        # 7. APPLICATIONS
        if "open chrome" in user_input_low:
            os.system("start chrome")
            return "Opening Google Chrome."

        if "open notepad" in user_input_low:
            os.system("notepad")
            return "Opening Notepad."

        print("[JARVIS Agent] Processing with Groq...")

        # Optional: Include small context if memory exists
        mem_mgr = _get_memory()
        context = ""
        if mem_mgr:
            recent_history = mem_mgr.get_recent_history(limit=2)
            if recent_history:
                context = "Recent history:\n" + "\n".join(recent_history) + "\n\n"
        
        system_prompt = """
You are Jarvis, a voice assistant.

IMPORTANT RULE:
- Always reply in the SAME language as the user's input.
- If the user speaks in Hindi, reply in Hindi.
- If the user speaks in English, reply in English.
- If the user mixes languages, reply in that mixed language.

Keep answers short (1-2 sentences).
Do not translate unless asked.
"""
        full_prompt = context + f"User: {user_input}"

        # THE DIRECT AI CALL
        response = groq_reason(full_prompt, system_prompt=system_prompt)

        if not response:
            return "I apologize, but I'm having trouble thinking right now."

        # Save to memory if available
        if mem_mgr:
            mem_mgr.save_interaction(user_input, response.strip())

        return response.strip()

    except Exception as e:
        print(f"[JARVIS Error] Processing failed: {e}")
        return "I encountered an error trying to process that."





