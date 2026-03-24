"""
JARVIS — Planner Agent
Uses Groq reasoning to break user requests into logical steps.
"""

import json
from models.groq_model import think

PLANNER_PROMPT = """You are JARVIS, a highly intelligent AI assistant running locally on the user's computer.

Your task is to analyze the user's spoken request and produce a structured JSON plan of action.

Available tools:
- "search": Look up information on the web. Input: the query string.
- "memory": Store/Get user info. Input: "action|key|value" (actions: store_pref, store_contact).
- "whatsapp": Send messages. Input format: "phone_number|message".
- "read_file": Read local file contents. Input: path string.
- "write_file": Write content safely. Input: JSON string with "path" and "content".
- "system_info": Get time, date, platform info. Input: "all" or specific.
- "open_url": Open a website in browser. Input: URL string.
- "respond": Generate a direct response for the user. Input: instructions/context.

Rules:
1. Understand the user's intent based on the request and memory.
2. If the user provides a contact (e.g., "My mother's number is..."), respond directly and remember it.
3. If the user asks to send a message to a name, check memory for the number first.
4. If a tool needs a phone number but you only have a name, ask for it using "respond".
5. Output ONLY valid JSON in this exact format (no markdown, no explanation):
{
  "intent": "Brief description of the request",
  "steps": [
    {"action": "tool_name", "input": "input for tool", "reason": "why"}
  ]
}

Rules:
1. Understand the user's intent based on the request and memory
2. If the request is a simple greeting or question, use ONLY the "respond" tool
3. If external facts, time, or files are needed, use tools first, then end with "respond"
4. Always end with a "respond" step to speak back to the user
"""

def plan(user_input: str, memory_context: str = "") -> dict:
    """
    Produce an action plan from the user's input.
    """
    prompt = f"User Request: {user_input}"
    if memory_context:
        prompt = f"Relevant Past Memory:\n{memory_context}\n\n{prompt}"

    raw_response = think(prompt, system_prompt=PLANNER_PROMPT, temperature=0.3)

    try:
        # Strip markdown if model included it
        cleaned = raw_response.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[-1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[-1].split("```")[0].strip()
            
        result = json.loads(cleaned)
        return result if isinstance(result, dict) else {
            "intent": "direct response",
            "steps": [{"action": "respond", "input": user_input}]
        }
    except Exception:
        # Failsafe plan
        return {
            "intent": "respond to user directly",
            "steps": [{"action": "respond", "input": user_input, "reason": "Fallback plan due to parsing error"}]
        }

