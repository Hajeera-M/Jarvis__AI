import requests
import json
import time

API_URL = "http://127.0.0.1:8000/jarvis"
HEALTH_URL = "http://127.0.0.1:8000/health"
USER_ID = "full_stack_verification_user"

def test_jarvis():
    print("--- 🚀 JARVIS-X Final Stack Verification ---")
    
    # 1. Health Check
    print("[1] Checking Health Endpoint...")
    try:
        h = requests.get(HEALTH_URL)
        print(f"Health Response: {h.json()}\n")
    except Exception as e:
        print(f"Health Check Failed: {e}\n")

    # 2. Memory & Linguistic Persistence
    print("[2] Setting Fact (Hindi/Hinglish)...")
    payload1 = {
        "input": "Mera naam Hajeera hai aur mujhe coding pasand hai.",
        "user_id": USER_ID
    }
    r1 = requests.post(API_URL, json=payload1)
    print(f"User: {payload1['input']}")
    print(f"Assistant: {r1.json().get('response')}\n")

    time.sleep(2)

    print("[3] Recalling Fact (English)...")
    payload2 = {
        "input": "What is my name and what do I like?",
        "user_id": USER_ID
    }
    r2 = requests.post(API_URL, json=payload2)
    print(f"User: {payload2['input']}")
    response = r2.json().get('response')
    print(f"Assistant: {response}\n")

    # 4. Agent Tool Routing (yfinance)
    print("[4] Testing Stock Tool (yfinance)...")
    payload3 = {
        "input": "What is the price of Tesla stock?",
        "user_id": USER_ID
    }
    r3 = requests.post(API_URL, json=payload3)
    print(f"User: {payload3['input']}")
    stock_res = r3.json()
    print(f"Assistant: {stock_res.get('response')}")
    print(f"Source: {stock_res.get('source')}\n")

    # 5. Success Verification
    memory_success = "Hajeera" in response or "coding" in response.lower()
    stock_success = stock_res.get("source") == "tool" and "Tesla" in stock_res.get("response")

    if memory_success and stock_success:
        print("✅ SUCCESS: Agent Routing & Memory are VERIFIED!")
    else:
        print(f"❌ FAILURE: Memory={memory_success}, Stock={stock_success}")

    # 6. Logging Check
    if os.path.exists("jarvis_api.log"):
        print("✅ SUCCESS: Production Logging is VERIFIED!")
    else:
        print("❌ FAILURE: Log file not found.")

if __name__ == "__main__":
    import os
    try:
        test_jarvis()
    except Exception as e:
        print(f"Verification Error: {e}")
