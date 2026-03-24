"""
JARVIS-X — Planner Agent
Uses Groq LLM to analyze user requests and produce structured action plans.
"""

import json
from models.groq_client import think

PLANNER_SYSTEM_PROMPT = """You are the Planning Module of JARVIS-X, an advanced autonomous AI assistant.

Your task is to analyze a user request and produce a structured execution plan.

Available tools:
- "search": Search the web for information. Input: search query string.
- "open_url": Open a URL in the browser. Input: URL string.
- "read_file": Read a file from the file system. Input: file path string.
- "write_file": Write content to a file. Input: JSON with "path" and "content" keys.
- "list_files": List files in a directory. Input: directory path string.
- "respond": Generate a direct conversational response (no tool needed). Input: context/instructions for response.

Output ONLY valid JSON in this exact format (no markdown, no explanation):
{
  "intent": "brief description of what the user wants",
  "steps": [
    {"action": "tool_name", "input": "input for the tool", "reason": "why this step"}
  ]
}

Rules:
- Think step by step
- Use the minimum number of steps needed
- For simple greetings, questions, or conversations — use a SINGLE "respond" step
- Use tools ONLY when the user explicitly needs external data, file operations, or browser actions
- Always end with a "respond" step to formulate the final answer
- Output ONLY the JSON object, nothing else
"""


async def plan(user_input: str, memory_context: str = "") -> dict:
    """
    Analyze user input and produce an action plan.
    
    Args:
        user_input: The user's request (transcribed text)
        memory_context: Relevant past conversation context from memory
    
    Returns:
        A dict with "intent" and "steps" keys
    """
    prompt = f"User request: {user_input}"
    if memory_context:
        prompt = f"Relevant context from past conversations:\n{memory_context}\n\n{prompt}"

    raw_response = await think(prompt, system_prompt=PLANNER_SYSTEM_PROMPT, temperature=0.3)

    # Parse JSON response, handling potential markdown wrapping
    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            # Remove markdown code fences
            lines = cleaned.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            cleaned = "\n".join(lines)
        plan_data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: if the model didn't return valid JSON, create a simple respond plan
        plan_data = {
            "intent": "respond to user",
            "steps": [
                {"action": "respond", "input": user_input, "reason": "Direct response"}
            ],
        }

    return plan_data
