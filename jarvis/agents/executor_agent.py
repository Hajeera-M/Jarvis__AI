"""
JARVIS — Executor Agent
Evaluates plan steps by calling tools, generates final spoken response.
"""

from tools.tool_registry import call_tool
from models.hf_model import generate

RESPONSE_PROMPT = """You are JARVIS, an advanced AI assistant running locally.

Generate a clear, concise, and helpful spoken response based on the context provided.
Do NOT use markdown headers, asterisks, or code blocks — this will be spoken out loud by a voice synthesizer.

Rules:
1. Speak conversationally and directly to the user
2. Keep it concise (1-3 sentences) unless they asked for a detailed explanation
3. Do not mention "tools", "JSON", or your internal processes
4. If tool results are provided, seamlessly integrate the information
"""

def execute_plan(plan: dict, original_input: str) -> str:
    """
    Executes a structured plan and returns the final string to be spoken.
    """
    results = []
    tool_outputs = []
    
    steps = plan.get("steps", [])
    if not steps:
        steps = [{"action": "respond", "input": original_input}]
        
    for step in steps:
        action = step.get("action", "respond")
        step_input = step.get("input", "")
        
        if action == "respond":
            context_parts = [f"User asked: {original_input}"]
            if tool_outputs:
                context_parts.append("Information gathered:\n" + "\n".join(tool_outputs))
            if step_input and step_input != original_input:
                context_parts.append(f"Instructions for response: {step_input}")
                
            prompt = "\n\n".join(context_parts)
            
            # Generate the final conversational response
            final_response = generate(prompt, system_prompt=RESPONSE_PROMPT)
            results.append({"action": "respond", "output": final_response})
            
        else:
            # Call tool
            try:
                print(f"[JARVIS Agent] Using tool: {action}...")
                output = call_tool(action, step_input)
                results.append({"action": action, "output": output})
                tool_outputs.append(f"[{action} result] {output}")
            except Exception as e:
                err = f"Tool '{action}' failed: {e}"
                results.append({"action": action, "output": err, "error": True})
                tool_outputs.append(err)
                print(f"[JARVIS Agent] {err}")

    # Extract the final spoken text from the response step
    for r in reversed(results):
        if r["action"] == "respond":
            return r["output"]
            
    # Fallback if no respond step occurred
    return "I've completed the task."
