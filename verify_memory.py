import requests
import json
import time

API_URL = "http://127.0.0.1:8000/jarvis"
USER_ID = "test_user_persistence"

def test_memory():
    print(f"--- Phase 1: Memory Verification (User: {USER_ID}) ---")
    
    # 1. Establish a fact
    payload1 = {
        "input": "Remember that my secret code is 998877.",
        "user_id": USER_ID
    }
    print(f"Sending: {payload1['input']}")
    res1 = requests.post(API_URL, json=payload1)
    print(f"Assistant: {res1.json().get('response')}\n")
    
    time.sleep(2) # Brief pause
    
    # 2. Ask about the fact
    payload2 = {
        "input": "What was my secret code?",
        "user_id": USER_ID
    }
    print(f"Sending: {payload2['input']}")
    res2 = requests.post(API_URL, json=payload2)
    response = res2.json().get('response')
    print(f"Assistant: {response}\n")
    
    if "998877" in response:
        print("✅ SUCCESS: Phase 1 Persistent Memory is WORKING!")
    else:
        print("❌ FAILURE: Phase 1 Persistent Memory did not recall the fact.")

if __name__ == "__main__":
    try:
        test_memory()
    except Exception as e:
        print(f"Verification Error: {e}")

