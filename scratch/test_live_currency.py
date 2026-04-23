import asyncio
from jarvis.services.skill_service import SkillService
import os
from dotenv import load_dotenv

load_dotenv(".env")

async def test_live_currency():
    print("--- Testing Live Currency Conversion (USD to INR) ---")
    result = SkillService.get_currency_conversion(1.0, "USD", "INR")
    print(f"Result: {result}")
    
    if "84." in result or "83." in result:
        print("\n✅ SUCCESS: JARVIS is now using live real-time currency rates.")
    else:
        print("\n❌ FAILED: Still getting incorrect or outdated data.")

if __name__ == "__main__":
    asyncio.run(test_live_currency())
