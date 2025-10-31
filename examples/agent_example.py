"""
Examples demonstrating the MoodMatch Agent with A2A protocol integration.

This shows the complete workflow from receiving A2A messages to returning
TaskResults with personalized recommendations.

Run with: python examples/agent_example.py
"""

import asyncio
import os
from dotenv import load_dotenv

from agents import MoodMatchAgent
from models.a2a import A2AMessage, MessagePart, MessageConfiguration

# Load environment variables
load_dotenv()


# ============================================================================
# Example 1: Basic Agent Workflow
# ============================================================================


async def basic_agent_example():
    """Complete workflow with MoodMatch agent."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Agent Workflow")
    print("=" * 70)
    
    # Get API credentials
    gemini_key = os.getenv("GEMINI_API_KEY")
    tmdb_key = os.getenv("TMDB_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if not all([gemini_key, tmdb_key, spotify_id, spotify_secret]):
        print("⚠️  Required API keys not found. Please set:")
        print("   - GEMINI_API_KEY")
        print("   - TMDB_API_KEY")
        print("   - SPOTIFY_CLIENT_ID")
        print("   - SPOTIFY_CLIENT_SECRET")
        return
    
    # Initialize agent
    print("\n🤖 Initializing MoodMatch Agent...")
    agent = MoodMatchAgent(
        gemini_api_key=gemini_key,
        tmdb_api_key=tmdb_key,
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        google_books_api_key=books_key
    )
    
    try:
        # Create user message
        user_message = A2AMessage(
            role="user",
            parts=[MessagePart(
                type="text",
                text="I'm feeling really stressed from work. I need something to help me unwind and relax."
            )]
        )
        
        print("\n💬 User message:")
        print(f"   '{user_message.parts[0].text}'")
        
        # Process message
        print("\n🔍 Processing message...")
        result = await agent.process_messages(
            messages=[user_message],
            context_id=None,  # Will be auto-generated
            task_id=None,  # Will be auto-generated
            config=None
        )
        
        # Display result
        print(f"\n✅ Task completed: {result.status.state}")
        print(f"   Context ID: {result.contextId}")
        print(f"   Task ID: {result.id}")
        
        # Show agent response
        print("\n🤖 Agent response:")
        for message in result.history:
            if message.role == "agent":
                for part in message.parts:
                    if part.type == "text":
                        print(f"\n{part.text}")
        
        # Show artifacts
        print(f"\n📦 Artifacts generated: {len(result.artifacts)}")
        for artifact in result.artifacts:
            print(f"   • {artifact.name}")
            
    finally:
        await agent.close()


# ============================================================================
# Example 2: Multiple Interactions with Context
# ============================================================================


async def context_persistence_example():
    """Multiple interactions using the same context."""
    print("\n" + "=" * 70)
    print("Example 2: Multiple Interactions with Context")
    print("=" * 70)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    tmdb_key = os.getenv("TMDB_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if not all([gemini_key, tmdb_key, spotify_id, spotify_secret]):
        print("⚠️  Required API keys not found")
        return
    
    agent = MoodMatchAgent(
        gemini_api_key=gemini_key,
        tmdb_api_key=tmdb_key,
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        google_books_api_key=books_key
    )
    
    try:
        # First interaction
        print("\n💬 Interaction 1: User is happy")
        message1 = A2AMessage(
            role="user",
            parts=[MessagePart(
                type="text",
                text="I'm feeling great today! Just got promoted at work!"
            )]
        )
        
        result1 = await agent.process_messages(messages=[message1])
        context_id = result1.contextId
        
        print(f"   ✅ Context created: {context_id}")
        print(f"   📊 Artifacts: {len(result1.artifacts)}")
        
        # Second interaction (same context)
        print("\n💬 Interaction 2: User wants different mood")
        message2 = A2AMessage(
            role="user",
            parts=[MessagePart(
                type="text",
                text="Actually, I want to calm down a bit. Something more relaxing."
            )]
        )
        
        result2 = await agent.process_messages(
            messages=[message2],
            context_id=context_id  # Reuse context
        )
        
        print(f"   ✅ Same context: {result2.contextId == context_id}")
        print(f"   📊 Artifacts: {len(result2.artifacts)}")
        
        # Show context history
        print(f"\n📚 Context history has {len(agent.contexts.get(context_id, []))} messages")
        
    finally:
        await agent.close()


# ============================================================================
# Example 3: Different Mood States
# ============================================================================


async def different_moods_example():
    """Test agent with various mood states."""
    print("\n" + "=" * 70)
    print("Example 3: Different Mood States")
    print("=" * 70)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    tmdb_key = os.getenv("TMDB_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if not all([gemini_key, tmdb_key, spotify_id, spotify_secret]):
        print("⚠️  Required API keys not found")
        return
    
    agent = MoodMatchAgent(
        gemini_api_key=gemini_key,
        tmdb_api_key=tmdb_key,
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        google_books_api_key=books_key
    )
    
    try:
        test_messages = [
            "I'm feeling sad and lonely. Need something comforting.",
            "So excited about my upcoming vacation! Can't wait!",
            "Feeling anxious about my presentation tomorrow.",
            "Just want to chill and do nothing productive today.",
        ]
        
        for i, text in enumerate(test_messages, 1):
            print(f"\n{'─' * 70}")
            print(f"Test {i}: {text[:50]}...")
            
            message = A2AMessage(
                role="user",
                parts=[MessagePart(type="text", text=text)]
            )
            
            result = await agent.process_messages(messages=[message])
            
            print(f"   Status: {result.status.state}")
            print(f"   Artifacts: {len(result.artifacts)}")
            
            # Extract mood from artifacts
            for artifact in result.artifacts:
                if artifact.name == "mood_analysis":
                    mood_data = artifact.parts[0].data
                    print(f"   Detected mood: {mood_data.get('primary_mood')} (intensity: {mood_data.get('intensity')}/10)")
                    print(f"   Immediate need: {mood_data.get('immediate_need')}")
                    break
    
    finally:
        await agent.close()


# ============================================================================
# Example 4: Error Handling
# ============================================================================


async def error_handling_example():
    """Test agent error handling."""
    print("\n" + "=" * 70)
    print("Example 4: Error Handling")
    print("=" * 70)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    tmdb_key = os.getenv("TMDB_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if not all([gemini_key, tmdb_key, spotify_id, spotify_secret]):
        print("⚠️  Required API keys not found")
        return
    
    agent = MoodMatchAgent(
        gemini_api_key=gemini_key,
        tmdb_api_key=tmdb_key,
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        google_books_api_key=books_key
    )
    
    try:
        # Test 1: Empty message
        print("\n📝 Test 1: Empty message")
        empty_message = A2AMessage(
            role="user",
            parts=[MessagePart(type="text", text="")]
        )
        
        result = await agent.process_messages(messages=[empty_message])
        print(f"   Status: {result.status.state}")
        print(f"   Message: {result.status.message}")
        
        # Test 2: No user messages
        print("\n📝 Test 2: No user messages")
        system_message = A2AMessage(
            role="system",
            parts=[MessagePart(type="text", text="System message")]
        )
        
        result = await agent.process_messages(messages=[system_message])
        print(f"   Status: {result.status.state}")
        print(f"   Handled gracefully: {result.status.state == 'failed'}")
        
    finally:
        await agent.close()


# ============================================================================
# Example 5: Artifact Inspection
# ============================================================================


async def artifact_inspection_example():
    """Inspect the artifacts generated by the agent."""
    print("\n" + "=" * 70)
    print("Example 5: Artifact Inspection")
    print("=" * 70)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    tmdb_key = os.getenv("TMDB_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if not all([gemini_key, tmdb_key, spotify_id, spotify_secret]):
        print("⚠️  Required API keys not found")
        return
    
    agent = MoodMatchAgent(
        gemini_api_key=gemini_key,
        tmdb_api_key=tmdb_key,
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        google_books_api_key=books_key
    )
    
    try:
        message = A2AMessage(
            role="user",
            parts=[MessagePart(
                type="text",
                text="I need something inspiring. Feeling motivated to make changes!"
            )]
        )
        
        print("\n🔍 Processing message...")
        result = await agent.process_messages(messages=[message])
        
        print(f"\n📦 Generated {len(result.artifacts)} artifacts:\n")
        
        for artifact in result.artifacts:
            print(f"{'─' * 70}")
            print(f"Artifact: {artifact.name}")
            print(f"ID: {artifact.artifactId}")
            
            for part in artifact.parts:
                if part.type == "data" and part.data:
                    data = part.data
                    
                    if artifact.name == "mood_analysis":
                        print(f"  Mood: {data.get('primary_mood')}")
                        print(f"  Intensity: {data.get('intensity')}/10")
                        print(f"  Confidence: {data.get('confidence')}")
                        print(f"  Multi-mood: {data.get('multi_mood')}")
                    
                    elif artifact.name == "music_recommendation":
                        print(f"  Title: {data.get('title')}")
                        print(f"  Platform: {data.get('platform')}")
                        print(f"  Duration: {data.get('duration')}")
                        print(f"  URL: {data.get('url')[:60]}...")
                    
                    elif artifact.name == "movie_recommendation":
                        print(f"  Title: {data.get('title')}")
                        print(f"  Year: {data.get('year')}")
                        print(f"  Rating: {data.get('rating')}/10")
                        print(f"  Genres: {', '.join(data.get('genres', []))}")
                    
                    elif artifact.name == "book_recommendation":
                        print(f"  Title: {data.get('title')}")
                        print(f"  Author: {data.get('author')}")
                        print(f"  Pages: {data.get('pages')}")
                        print(f"  Reading time: {data.get('reading_time')}")
        
        print(f"\n{'─' * 70}")
        
    finally:
        await agent.close()


# ============================================================================
# Example 6: Configuration Options
# ============================================================================


async def configuration_example():
    """Test agent with different message configurations."""
    print("\n" + "=" * 70)
    print("Example 6: Configuration Options")
    print("=" * 70)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    tmdb_key = os.getenv("TMDB_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if not all([gemini_key, tmdb_key, spotify_id, spotify_secret]):
        print("⚠️  Required API keys not found")
        return
    
    agent = MoodMatchAgent(
        gemini_api_key=gemini_key,
        tmdb_api_key=tmdb_key,
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        google_books_api_key=books_key
    )
    
    try:
        message = A2AMessage(
            role="user",
            parts=[MessagePart(
                type="text",
                text="I'm feeling contemplative and philosophical today."
            )]
        )
        
        # Test with configuration
        config = MessageConfiguration(
            blocking=True,
            acceptedOutputModes=["text", "data"]
        )
        
        print("\n🔧 Processing with configuration...")
        print(f"   Blocking: {config.blocking}")
        print(f"   Accepted modes: {config.acceptedOutputModes}")
        
        result = await agent.process_messages(
            messages=[message],
            config=config
        )
        
        print(f"\n✅ Status: {result.status.state}")
        print(f"   Generated {len(result.artifacts)} artifacts")
        print(f"   History has {len(result.history)} messages")
        
    finally:
        await agent.close()


# ============================================================================
# Main Runner
# ============================================================================


async def main():
    """Run all examples."""
    print("\n" + "🤖" * 35)
    print("MOODMATCH AGENT EXAMPLES (A2A Protocol)")
    print("🤖" * 35)
    
    # Run examples
    await basic_agent_example()
    await context_persistence_example()
    await different_moods_example()
    await error_handling_example()
    await artifact_inspection_example()
    await configuration_example()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
