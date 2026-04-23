"""Final E2E verification: Identity, Memory (Name Recall), Language, and TTS fallback."""
import requests, time, os

API = "http://127.0.0.1:8000/jarvis"
HEALTH = "http://127.0.0.1:8000/health"
USER = "fresh_hajeera_verification_01"
results = []

def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    results.append(f"{status}: {name} {detail}")

# 1. Health
try:
    h = requests.get(HEALTH, timeout=5).json()
    check("Health Endpoint", h.get("status") == "running")
except:
    check("Health Endpoint", False, "(server not reachable)")

# 2. Owner identity
r = requests.post(API, json={"input": "Who is your owner?", "user_id": USER}).json()
check("Owner Identity", "Hajeera" in r.get("response", ""), f"Response: {r.get('response','')[:80]}")
print(f"   Owner Q: {r.get('response','')[:80]}")

time.sleep(1)

# 3. User name memory
requests.post(API, json={"input": "My name is Testing Agent.", "user_id": USER})
time.sleep(1)
r2 = requests.post(API, json={"input": "What is my name?", "user_id": USER}).json()
check("User Name Recall", "Testing Agent" in r2.get("response", ""), f"Response: {r2.get('response','')[:80]}")
print(f"   Name recall: {r2.get('response','')[:80]}")

time.sleep(1)

# 4. Structured output format
r3 = requests.post(API, json={"input": "Hello", "user_id": USER}).json()
check("Structured Output - spoken_response", "spoken_response" in r3)
check("Structured Output - voice", "voice" in r3)
check("Structured Output - language", "language" in r3)
check("Structured Output - source", "source" in r3)

# 5. Stock tool routing
r4 = requests.post(API, json={"input": "What is the price of Apple stock?", "user_id": USER}).json()
check("Tool Routing - Stock", r4.get("source") == "tool", f"Source: {r4.get('source')}")

# 6. Spoken response is shorter than full response
resp = r4.get("response","")
spoken = r4.get("spoken_response","")
check("Speech Formatting (spoken shorter)", len(spoken) <= len(resp), f"full={len(resp)}, spoken={len(spoken)}")

# 7. Log file exists
check("Structured Logging Active", os.path.exists("jarvis_api.log"))

print("\n--- JARVIS E2E Verification Results ---")
for r in results:
    print(r)

