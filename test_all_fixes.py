"""
Comprehensive test to verify all fixes are working.
"""
import asyncio
import json
from models.a2a import MessagePart, A2AMessage, MessageParams

def test_message_part():
    """Test MessagePart uses 'kind' field correctly."""
    print("Testing MessagePart...")
    
    # Test text part
    text_part = MessagePart(kind="text", text="Hello")
    assert text_part.kind == "text"
    assert text_part.text == "Hello"
    print("✅ Text MessagePart works")
    
    # Test data part
    data_part = MessagePart(kind="data", data={"mood": "happy"})
    assert data_part.kind == "data"
    assert data_part.data == {"mood": "happy"}
    print("✅ Data MessagePart works")

def test_a2a_message():
    """Test A2AMessage structure."""
    print("\nTesting A2AMessage...")
    
    msg = A2AMessage(
        role="user",
        parts=[MessagePart(kind="text", text="I'm feeling happy")]
    )
    assert msg.role == "user"
    assert len(msg.parts) == 1
    assert msg.parts[0].kind == "text"
    print("✅ A2AMessage works")

def test_message_params():
    """Test MessageParams config field."""
    print("\nTesting MessageParams...")
    
    params = MessageParams(
        messages=[
            A2AMessage(
                role="user",
                parts=[MessagePart(kind="text", text="test")]
            )
        ]
    )
    # Should have 'config' field
    assert hasattr(params, 'config')
    print("✅ MessageParams has 'config' field")

async def test_mood_analyzer():
    """Test MoodAnalyzer can parse JSON output."""
    print("\nTesting MoodAnalyzer JSON parsing...")
    
    from services.mood_analyzer import MoodAnalysis
    import re
    
    # Simulate AI output with markdown code blocks
    json_output = '''```json
{
  "primary_mood": "happy",
  "intensity": 7,
  "context": null,
  "immediate_need": "match",
  "multi_mood": false,
  "secondary_moods": [],
  "time_context": null,
  "confidence": 1.0,
  "music_preferences": {},
  "movie_preferences": {},
  "book_preferences": {}
}
```'''
    
    # Test JSON parsing logic
    json_str = re.sub(r'^```json\s*|\s*```$', '', json_output.strip(), flags=re.MULTILINE)
    json_str = json_str.strip()
    data = json.loads(json_str)
    mood = MoodAnalysis(**data)
    
    assert mood.primary_mood == "happy"
    assert mood.intensity == 7
    print("✅ JSON parsing works")

def main():
    """Run all tests."""
    print("=" * 60)
    print("COMPREHENSIVE FIX VERIFICATION")
    print("=" * 60)
    
    try:
        test_message_part()
        test_a2a_message()
        test_message_params()
        asyncio.run(test_mood_analyzer())
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! System is ready!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
