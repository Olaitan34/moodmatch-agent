"""
Simple test script to verify the MoodMatch server is working.
"""

import json
import requests

def test_health():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_a2a_endpoint():
    """Test the A2A endpoint with a simple mood request."""
    print("\n🔍 Testing A2A endpoint...")
    
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
                            "type": "text",
                            "text": "I'm feeling stressed and need to relax"
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
        
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Response ID: {result.get('id')}")
            print(f"📄 JSON-RPC: {result.get('jsonrpc')}")
            
            if 'result' in result:
                task_result = result['result']
                print(f"📄 Task State: {task_result.get('state')}")
                
                # Print agent's message
                messages = task_result.get('messages', [])
                if messages:
                    agent_message = messages[0]
                    parts = agent_message.get('parts', [])
                    if parts:
                        print(f"\n💬 Agent Response:\n{parts[0].get('text', '')[:500]}...")
                
                # Print artifact count
                artifacts = task_result.get('artifacts', [])
                print(f"\n📦 Artifacts: {len(artifacts)}")
                for artifact in artifacts:
                    print(f"   - {artifact.get('name')}: {artifact.get('description')}")
                
                return True
            elif 'error' in result:
                print(f"❌ Error: {result['error']}")
                return False
        else:
            print(f"❌ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ A2A test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🎭 MoodMatch Server Test")
    print("=" * 60)
    
    # Test health
    health_ok = test_health()
    
    if not health_ok:
        print("\n❌ Health check failed. Make sure the server is running:")
        print("   python main.py")
        return
    
    # Test A2A endpoint
    print("\n" + "=" * 60)
    a2a_ok = test_a2a_endpoint()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"A2A Endpoint: {'✅ PASS' if a2a_ok else '❌ FAIL'}")
    
    if health_ok and a2a_ok:
        print("\n🎉 All tests passed! Your MoodMatch server is working!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")


if __name__ == "__main__":
    main()
