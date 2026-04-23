import asyncio
from jarvis.agents.controller import MasterController
import os
from dotenv import load_dotenv

load_dotenv(".env")

async def test_product_price():
    print("--- Testing Product Price Routing ---")
    context = {"last_tool": None}
    user_input = "price of honda bike"
    
    print(f"User Input: {user_input}")
    output, new_context = await asyncio.to_thread(
        MasterController.handle_user_input, user_input, context, "test_user"
    )
    
    print("\n--- JARVIS RESPONSE ---")
    print(f"Text: {output['response']}")
    print(f"Source: {output['source']}")
    
    # Check if it avoided the stock error
    if "identify which stock" in output['response']:
        print("\n❌ FAILED: Still incorrectly identifying as stock.")
    elif output['source'] == "search" or output['source'] == "ai":
        print(f"\n✅ SUCCESS: Correctly routed to {output['source']} for product price.")
    else:
        print(f"\n❓ UNEXPECTED SOURCE: {output['source']}")

if __name__ == "__main__":
    asyncio.run(test_product_price())
