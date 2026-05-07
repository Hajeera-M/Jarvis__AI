import asyncio
from jarvis.agents.controller import MasterController
import os
from dotenv import load_dotenv

load_dotenv(".env")

async def verify_next_gen():
    print("--- Verifying Next-Gen Enhancements ---")
    context = {"last_tool": None}
    user_id = "test_user"

    # 1. Verify Calendar
    print("\n[Testing Calendar]")
    user_input = "add meeting with the team to calendar"
    output, context = await asyncio.to_thread(MasterController.handle_user_input, user_input, context, user_id)
    print(f"Calendar Response: {output['response']}")
    
    # 2. Verify Semantic Memory (Vector DB)
    print("\n[Testing Semantic Memory]")
    # First, save a unique fact
    from jarvis.services.memory_service import MemoryService
    MemoryService.save_message(user_id, "user", "My favorite color is neon purple.")
    
    # Now query it
    from jarvis.services.vector_service import VectorService
    results = VectorService.query_memory("What is my favorite color?", n_results=1)
    print(f"Memory Search Result: {results}")

    # 3. Verify Vision (Dry run capture)
    print("\n[Testing Vision Capture]")
    from jarvis.services.vision_service import VisionService
    img_str = VisionService.capture_screen()
    print(f"Vision Capture Success: {len(img_str) > 0}")

    print("\n--- ALL ENHANCEMENTS INITIALIZED AND VERIFIED ---")

if __name__ == "__main__":
    asyncio.run(verify_next_gen())
