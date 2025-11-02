"""
Simple test script to verify MoodMatch is working.
"""
import requests
import json
import time

print("=" * 60)
print("TESTING MOODMATCH AGENT")
print("=" * 60)

# Wait for server to be ready
print("\n⏳ Waiting for server to initialize...")
time.sleep(3)

# Test 1: Health Check
print("\n1️⃣ Testing Health Check...")
try:
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        print("✅ Health check passed!")
        print(f"   Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Health check error: {e}")

# Test 2: Execute - Happy Mood
print("\n2️⃣ Testing Execute with 'happy' mood...")
payload = {
    "jsonrpc": "2.0",
    "id": "test-happy",
    "method": "execute",
    "params": {
        "messages": [
            {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": "I am happy"
                    }
                ]
            }
        ]
    }
}

try:
    response = requests.post(
        "http://localhost:8000/a2a/moodmatch",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        
        if "result" in result:
            task_result = result["result"]
            status = task_result.get("status", {})
            state = status.get("state")
            
            if state == "completed":
                print("✅ Execute test PASSED!")
                print(f"   Task ID: {task_result.get('taskId')}")
                print(f"   Artifacts: {len(task_result.get('artifacts', []))}")
                
                # Show artifacts
                for i, artifact in enumerate(task_result.get('artifacts', []), 1):
                    print(f"   Artifact {i}: {artifact.get('name', 'Unknown')}")
                    
            elif state == "failed":
                print(f"❌ Task failed: {status.get('message')}")
            else:
                print(f"⚠️ Unexpected state: {state}")
        else:
            print(f"❌ No result in response")
    else:
        print(f"❌ Request failed: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Execute test error: {e}")

# Test 3: Execute - Stressed Mood
print("\n3️⃣ Testing Execute with 'stressed' mood...")
payload = {
    "jsonrpc": "2.0",
    "id": "test-stressed",
    "method": "execute",
    "params": {
        "messages": [
            {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": "I'm feeling stressed and overwhelmed with work"
                    }
                ]
            }
        ]
    }
}

try:
    response = requests.post(
        "http://localhost:8000/a2a/moodmatch",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        
        if "result" in result:
            task_result = result["result"]
            status = task_result.get("status", {})
            state = status.get("state")
            
            if state == "completed":
                print("✅ Stressed mood test PASSED!")
                artifacts = task_result.get('artifacts', [])
                print(f"   Got {len(artifacts)} recommendations")
            elif state == "failed":
                print(f"❌ Task failed: {status.get('message')}")
        else:
            print(f"❌ No result in response")
    else:
        print(f"❌ Request failed: {response.status_code}")
        
except Exception as e:
    print(f"❌ Stressed test error: {e}")

print("\n" + "=" * 60)
print("TESTING COMPLETE!")
print("=" * 60)
