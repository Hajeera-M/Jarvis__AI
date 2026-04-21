"""
JARVIS — Executor Agent
Iterates over planned steps and dispatches to the appropriate tools.
"""

from tools.tool_registry import execute_tool
from models.huggingface_client import generate

RESPONSE_SYSTEM_PROMPT = """You are JARVIS, an advanced AI assistant speaking to the user.

Generate a clear, concise, and helpful spoken response based on the provided context and information.

Rules:
- Keep responses conversational and natural (they will be spoken aloud)
- Be concise — aim for 2-4 sentences unless the user asked for detail
- If tool results are provided, synthesize them into a natural response
- Never mention internal tools, steps, or technical processes
- Speak as a confident, knowledgeable assistant
"""


async def execute(plan: dict, user_input: str) -> dict:
    """
    Execute a plan produced by the planner agent.
    
    Args:
        plan: The plan dict with "intent" and "steps"
        user_input: Original user input for context
    
    Returns:
        Dict with "results" (list of step results) and "final_response" (string)
    """
    results = []
    tool_outputs = []

    steps = plan.get("steps", [])

    for step in steps:
        action = step.get("action", "respond")
        step_input = step.get("input", "")

        if action == "respond":
            # Generate the final response using HuggingFace
            context_parts = [f"User said: {user_input}"]
            if tool_outputs:
                context_parts.append(f"Information gathered:\n" + "\n".join(tool_outputs))
            if step_input and step_input != user_input:
                context_parts.append(f"Instructions: {step_input}")

            prompt = "\n\n".join(context_parts)

            try:
                response = await generate(prompt, system_prompt=RESPONSE_SYSTEM_PROMPT)
            except Exception as e:
                # Fallback: use Groq if HuggingFace fails
                from models.groq_client import think
                response = await think(prompt, system_prompt=RESPONSE_SYSTEM_PROMPT)

            results.append({"action": "respond", "output": response})
        else:
            # Execute a tool
            try:
                tool_result = await execute_tool(action, step_input)
                results.append({"action": action, "output": tool_result})
                tool_outputs.append(f"[{action}] {tool_result}")
            except Exception as e:
                error_msg = f"Tool '{action}' failed: {str(e)}"
                results.append({"action": action, "output": error_msg, "error": True})
                tool_outputs.append(error_msg)

    # Extract final response
    final_response = ""
    for r in reversed(results):
        if r["action"] == "respond":
            final_response = r["output"]
            break

    # If no respond step was executed, generate one now
    if not final_response:
        context = f"User said: {user_input}\n\nGathered info:\n" + "\n".join(tool_outputs)
        try:
            final_response = await generate(context, system_prompt=RESPONSE_SYSTEM_PROMPT)
        except Exception:
            from models.groq_client import think
            final_response = await think(context, system_prompt=RESPONSE_SYSTEM_PROMPT)

    return {
        "results": results,
        "final_response": final_response,
    }

