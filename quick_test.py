#!/usr/bin/env python3
"""
Quick test script for MoodMatch A2A Agent.
Make sure the server is running first: python main.py
"""

import json
import sys

try:
    import requests
except ImportError:
    print("❌ requests library not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


def test_health():
    """Test the health endpoint."""
    print("=" * 60)
    print("1️⃣  Testing Health Endpoint")
    print("=" * 60)
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Make sure the server is running: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_mood_request(mood_text):
    """Test a mood analysis request."""
    print("\n" + "=" * 60)
    print("2️⃣  Testing Mood Analysis")
    print("=" * 60)
    print(f"Input: {mood_text}")
    print("-" * 60)
    
    payload = {
        "jsonrpc": "2.0",
        "id": "test-123",
        "method": "message/send",
        "params": {
            "messages": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "kind": "text",
                            "text": mood_text
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        print("📤 Sending request...")
        response = requests.post(
            "http://localhost:8000/a2a/moodmatch",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract task result
            if "result" in result:
                task_result = result["result"]
                print(f"\n📊 Task State: {task_result.get('state')}")
                
                # Print agent message
                messages = task_result.get("messages", [])
                if messages:
                    agent_msg = messages[0]
                    parts = agent_msg.get("parts", [])
                    if parts:
                        agent_text = parts[0].get("text", "")
                        print(f"\n💬 Agent Response:")
                        print("-" * 60)
                        print(agent_text)
                        print("-" * 60)
                
                # Print artifacts summary
                artifacts = task_result.get("artifacts", [])
                print(f"\n📦 Artifacts ({len(artifacts)}):")
                for artifact in artifacts:
                    print(f"   • {artifact.get('name')}: {artifact.get('description')}")
                
                return True
            
            elif "error" in result:
                error = result["error"]
                print(f"\n❌ Error Code: {error.get('code')}")
                print(f"❌ Error Message: {error.get('message')}")
                return False
        
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            print(response.text)
            return False
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>30s)")
        print("   The AI model might be slow to respond.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run the tests."""
    print("\n🎭 MoodMatch A2A Agent - Quick Test")
    print("=" * 60)
    
    # Test 1: Health
    if not test_health():
        print("\n⚠️  Cannot proceed without a healthy server.")
        sys.exit(1)
    
    # Test 2: Mood request
    mood_text = "I'm feeling stressed and overwhelmed with work. I need something to help me unwind and relax."
    success = test_mood_request(mood_text)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    if success:
        print("✅ All tests passed!")
        print("\n💡 Try it yourself:")
        print('   curl -X POST http://localhost:8000/a2a/moodmatch \\')
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"jsonrpc":"2.0","id":"1","method":"message/send",')
        print('          "params":{"messages":[{"role":"user","parts":[')
        print('          {"kind":"text","text":"I need motivation"}]}]}}\'')
    else:
        print("❌ Tests failed!")
    
    print("\n")


if __name__ == "__main__":
    main()
