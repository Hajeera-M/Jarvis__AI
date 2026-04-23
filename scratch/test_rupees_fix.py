import asyncio
from jarvis.agents.controller import MasterController
import os
from dotenv import load_dotenv

load_dotenv(".env")

async def test_combined_price_rupees():
    print("--- Testing Product Price in Rupees ---")
    context = {"last_tool": None}
    user_input = "price of fireblade bike in rupees"
    
    print(f"User Input: {user_input}")
    output, _ = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, "test_user")
    
    print("\n--- JARVIS RESPONSE ---")
    print(f"Text: {output['response']}")
    print(f"Source: {output['source']}")
    
    # Check if it avoided the "ask for stock" error
    if "ask for a stock price first" in output['response'] or "identify which stock" in output['response']:
        print("\n❌ FAILED: Still incorrectly hitting stock/currency logic.")
    elif output['source'] == "search" or output['source'] == "ai":
        print(f"\n✅ SUCCESS: Correctly routed to {output['source']} for product price with currency.")
    else:
        print(f"\n❓ UNEXPECTED SOURCE: {output['source']}")

if __name__ == "__main__":
    asyncio.run(test_combined_price_rupees())
