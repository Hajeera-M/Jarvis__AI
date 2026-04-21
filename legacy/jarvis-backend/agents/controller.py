"""
JARVIS — Agent Controller
Orchestrates the full agentic pipeline: Plan → Execute → Reflect → Respond
"""

from agents.planner_agent import plan
from agents.executor_agent import execute
from agents.reflection_agent import reflect
from memory.vector_store import search_memory, store_interaction

MAX_RETRIES = 1  # Maximum re-planning attempts


async def run_agent(user_input: str) -> str:
    """
    Main entry point for the agent system.
    Runs the full pipeline: Memory → Plan → Execute → Reflect → Store → Respond
    
    Args:
        user_input: The user's request (text)
    
    Returns:
        Final response string to be spoken/displayed
    """
    # 1. Retrieve relevant memory context
    memory_context = ""
    try:
        memories = search_memory(user_input, k=3)
        if memories:
            memory_context = "\n".join(memories)
    except Exception:
        pass  # Memory is optional, don't block on failure

    # 2. Plan
    action_plan = await plan(user_input, memory_context=memory_context)
    print(f"[JARVIS] Plan: {action_plan.get('intent', 'unknown')}")

    # 3. Execute
    execution = await execute(action_plan, user_input)
    final_response = execution["final_response"]

    # 4. Reflect (with retry loop)
    retries = 0
    while retries < MAX_RETRIES:
        evaluation = await reflect(
            user_input, final_response, execution["results"]
        )
        print(f"[JARVIS] Reflection: score={evaluation.get('quality_score')}, "
              f"complete={evaluation.get('is_complete')}")

        if evaluation.get("is_complete") and not evaluation.get("needs_retry"):
            break

        # Re-plan and re-execute
        print(f"[JARVIS] Retrying (attempt {retries + 1})...")
        feedback = evaluation.get("feedback", "")
        enhanced_input = f"{user_input}\n\n[Previous attempt feedback: {feedback}]"
        action_plan = await plan(enhanced_input, memory_context=memory_context)
        execution = await execute(action_plan, user_input)
        final_response = execution["final_response"]
        retries += 1

    # 5. Store in memory
    try:
        store_interaction(user_input, final_response)
    except Exception:
        pass  # Memory storage is optional

    return final_response

