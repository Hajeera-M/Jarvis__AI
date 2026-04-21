"""
JARVIS — Reflection Agent
Evaluates execution results and determines if the task is complete.
"""

import json
from models.groq_client import think

REFLECTION_SYSTEM_PROMPT = """You are the Reflection Module of JARVIS.

Your task is to evaluate whether an AI assistant's response adequately addresses the user's request.

Output ONLY valid JSON in this exact format (no markdown, no explanation):
{
  "is_complete": true/false,
  "quality_score": 1-10,
  "feedback": "brief explanation",
  "needs_retry": true/false
}

Rules:
- is_complete: true if the response reasonably addresses the user's request
- quality_score: 1 = terrible, 10 = perfect
- needs_retry: true ONLY if the response is fundamentally wrong or missing critical information
- For simple conversations (greetings, time, etc.), almost always mark as complete with high score
- Be lenient — a good-enough response is better than infinite retries
"""


async def reflect(user_input: str, response: str, execution_results: list) -> dict:
    """
    Evaluate whether the execution results and response are satisfactory.
    
    Args:
        user_input: Original user request
        response: The generated response text  
        execution_results: List of step results from executor
    
    Returns:
        Dict with is_complete, quality_score, feedback, needs_retry
    """
    prompt = f"""User request: {user_input}

Generated response: {response}

Execution steps taken: {json.dumps(execution_results, default=str)}

Evaluate if this response adequately addresses the user's request."""

    raw = await think(prompt, system_prompt=REFLECTION_SYSTEM_PROMPT, temperature=0.2)

    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            cleaned = "\n".join(lines)
        evaluation = json.loads(cleaned)
    except json.JSONDecodeError:
        # Default: assume it's complete (avoid infinite loops)
        evaluation = {
            "is_complete": True,
            "quality_score": 7,
            "feedback": "Unable to parse reflection, proceeding with response.",
            "needs_retry": False,
        }

    return evaluation

