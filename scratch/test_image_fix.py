import asyncio
from jarvis.agents.controller import MasterController
import os
from dotenv import load_dotenv

load_dotenv(".env")

async def test_image_intent():
    print("--- Testing Image Intent & Response ---")
    context = {"last_tool": None}
    # Test a phrase that previously failed or was weak
    user_input = "create a eel image"
    
    print(f"User Input: {user_input}")
    output, new_context = await asyncio.to_thread(
        MasterController.handle_user_input, user_input, context, "test_user"
    )
    
    print("\n--- JARVIS RESPONSE ---")
    print(f"Text: {output['response']}")
    print(f"Spoken: {output['spoken_response']}")
    print(f"Source: {output['source']}")
    
    # Check if there are follow-up questions (heuristic: question mark or extra sentence)
    if "?" in output['response'] and "generated" in output['response']:
        print("\n❌ FAILED: Found a question in the confirmation.")
    elif output['source'] != "image":
        print(f"\n❌ FAILED: Routed to {output['source']} instead of image.")
    else:
        print("\n✅ SUCCESS: Image generated and confirmed without questioning.")

if __name__ == "__main__":
    asyncio.run(test_image_intent())
