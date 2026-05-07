import asyncio
from jarvis.agents.controller import MasterController
import os
from dotenv import load_dotenv

load_dotenv(".env")

async def test_fixes():
    print("--- Testing Routing Fixes ---")
    context = {"last_tool": None}
    user_id = "test_user"

    # 1. Test Weather with "today"
    print("\n[Testing: will it rain today or not?]")
    user_input = "will it rain today or not?"
    output, context = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, user_id)
    print(f"Source: {output['source']}")
    try:
        print(f"Response: {output['response']}")
    except:
        print("Response: [Unicode characters suppressed]")
    assert output['source'] == "weather", f"Expected weather, got {output['source']}"

    # 2. Test Weather without preposition
    print("\n[Testing: what is weather now]")
    user_input = "what is weather now"
    output, context = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, user_id)
    print(f"Source: {output['source']}")
    try:
        print(f"Response: {output['response']}")
    except:
        print("Response: [Unicode characters suppressed]")
    assert "Bangalore" in output['response'], f"Expected default to Bangalore, got {output['response']}"

    # 3. Test Weather with city
    print("\n[Testing: what is weather in Mumbai]")
    user_input = "what is weather in Mumbai"
    output, context = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, user_id)
    print(f"Source: {output['source']}")
    try:
        print(f"Response: {output['response']}")
    except:
        print("Response: [Unicode characters suppressed]")
    assert "Mumbai" in output['response'], f"Expected Mumbai, got {output['response']}"

    # 4. Test Time
    print("\n[Testing: what time is it]")
    user_input = "what time is it"
    output, context = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, user_id)
    print(f"Source: {output['source']}")
    try:
        print(f"Response: {output['response']}")
    except:
        print("Response: [Unicode characters suppressed]")
    assert output['source'] == "system", f"Expected system, got {output['source']}"

    print("\nALL ROUTING TESTS PASSED")

if __name__ == "__main__":
    asyncio.run(test_fixes())
