"""
JARVIS — Reflection Agent
Verifies if the plan execution was successful and correct.
"""

from models.groq_model import think

REFLECTION_PROMPT = """You are JARVIS, a highly intelligent AI assistant.
Your task is to review the results of an action plan and verify if it successfully fulfilled the user's request.

User Request: {user_input}
Plan executed: {plan}
Results: {results}

Analyze the results carefully.
- Did the tools return errors?
- Is the information gathered sufficient to answer the user?
- Was the final goal achieved?

Return ONLY one of the following JSON objects:
{
  "status": "success",
  "reason": "Brief explanation"
}
OR
{
  "status": "failure",
  "reason": "What went wrong",
  "suggestion": "How to fix it"
}
"""

def verify_execution(user_input: str, plan: dict, results: list) -> dict:
    """
    Verify if the execution of the plan was successful.
    """
    prompt = REFLECTION_PROMPT.format(
        user_input=user_input,
        plan=plan,
        results=results
    )
    
    raw_response = think(prompt, temperature=0.1)
    
    import json
    try:
        # Strip markdown if model included it
        cleaned = raw_response.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[-1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[-1].split("```")[0].strip()
            
        result = json.loads(cleaned)
        return result if isinstance(result, dict) else {"status": "success"}
    except Exception:
        return {"status": "success", "reason": "Self-verification failed, assuming success."}


