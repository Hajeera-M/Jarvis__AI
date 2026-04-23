import asyncio
from jarvis.agents.controller import MasterController
import os
from dotenv import load_dotenv

load_dotenv(".env")

async def test_commodity_price():
    print("--- Testing Commodity Price Routing ---")
    context = {"last_tool": None}
    
    # Test 1: Gold (should hit stock tool now)
    user_input = "gold price right now ?"
    print(f"User Input: {user_input}")
    output, _ = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, "test_user")
    print(f"Response: {output['response']}")
    print(f"Source: {output['source']}")
    
    # Test 2: Crude Oil (should hit stock tool now)
    user_input = "stock price of crude oil"
    print(f"\nUser Input: {user_input}")
    output, _ = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, "test_user")
    print(f"Response: {output['response']}")
    print(f"Source: {output['source']}")

    # Verification
    if output['source'] == "stock" and "crude oil" in output['response'].lower():
        print("\n✅ SUCCESS: Commodities correctly handled by market service.")
    else:
        print(f"\n❌ FAILED: Still falling through or incorrect source ({output['source']})")

if __name__ == "__main__":
    asyncio.run(test_commodity_price())
