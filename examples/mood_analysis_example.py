"""
Example usage of the MoodAnalyzer service with Pydantic AI and Gemini.

This demonstrates how to analyze user mood descriptions and extract
structured information for personalized media recommendations.
"""

import asyncio
import os
from services import MoodAnalyzer, quick_analyze


async def basic_example():
    """Basic mood analysis example."""
    print("=" * 60)
    print("Basic Mood Analysis Example")
    print("=" * 60)
    
    # Initialize analyzer (uses GEMINI_API_KEY from environment)
    analyzer = MoodAnalyzer()
    
    # Analyze a simple mood
    user_input = "I'm feeling really stressed after a long day at work"
    result = await analyzer.analyze_mood(user_input)
    
    print(f"\nUser input: {user_input}")
    print(f"\nAnalysis Results:")
    print(f"  Primary Mood: {result.primary_mood}")
    print(f"  Intensity: {result.intensity}/10")
    print(f"  Context: {result.context}")
    print(f"  Immediate Need: {result.immediate_need}")
    print(f"  Multi-mood: {result.multi_mood}")
    if result.secondary_moods:
        print(f"  Secondary Moods: {', '.join(result.secondary_moods)}")
    print(f"  Confidence: {result.confidence:.0%}")
    
    print(f"\nMusic Preferences:")
    print(f"  Energy Level: {result.music_preferences.get('energy_level')}")
    print(f"  Genres: {result.music_preferences.get('preferred_genres', [])}")
    print(f"  Vibe: {result.music_preferences.get('vibe', [])}")
    
    print(f"\nMovie Preferences:")
    print(f"  Tone: {result.movie_preferences.get('tone')}")
    print(f"  Genres: {result.movie_preferences.get('preferred_genres', [])}")
    print(f"  Length: {result.movie_preferences.get('length_preference')}")
    
    print(f"\nBook Preferences:")
    print(f"  Pacing: {result.book_preferences.get('pacing')}")
    print(f"  Depth: {result.book_preferences.get('depth')}")
    
    # Get human-readable summary
    summary = analyzer.get_mood_summary(result)
    print(f"\nSummary: {summary}")


async def multi_mood_example():
    """Example with multiple conflicting moods."""
    print("\n" + "=" * 60)
    print("Multi-Mood Analysis Example")
    print("=" * 60)
    
    analyzer = MoodAnalyzer()
    
    user_input = "I'm excited about my new job but also anxious about the change. Can't sleep thinking about it."
    result = await analyzer.analyze_mood(user_input)
    
    print(f"\nUser input: {user_input}")
    print(f"\nAnalysis Results:")
    print(f"  Primary Mood: {result.primary_mood}")
    print(f"  Intensity: {result.intensity}/10")
    print(f"  Multi-mood: {result.multi_mood}")
    print(f"  Secondary Moods: {', '.join(result.secondary_moods)}")
    print(f"  Immediate Need: {result.immediate_need}")
    print(f"  Time Context: {result.time_context}")
    
    print(f"\nRecommendation Strategy: {result.immediate_need}")


async def context_example():
    """Example with rich contextual information."""
    print("\n" + "=" * 60)
    print("Context-Rich Analysis Example")
    print("=" * 60)
    
    analyzer = MoodAnalyzer()
    
    # With additional context
    user_input = "Just broke up with my girlfriend. Feeling pretty down."
    additional_context = {
        "user_age": 25,
        "previous_searches": ["sad songs", "breakup movies"],
        "time_of_day": "late night"
    }
    
    result = await analyzer.analyze_mood(user_input, additional_context)
    
    print(f"\nUser input: {user_input}")
    print(f"Additional context: {additional_context}")
    print(f"\nAnalysis Results:")
    print(f"  Primary Mood: {result.primary_mood}")
    print(f"  Intensity: {result.intensity}/10")
    print(f"  Context: {result.context}")
    print(f"  Immediate Need: {result.immediate_need}")
    
    if result.multi_mood:
        print(f"  Secondary Moods: {', '.join(result.secondary_moods)}")


async def batch_example():
    """Example of analyzing multiple mood descriptions."""
    print("\n" + "=" * 60)
    print("Batch Analysis Example")
    print("=" * 60)
    
    analyzer = MoodAnalyzer()
    
    messages = [
        "I'm so happy! Just got promoted!",
        "Feeling lonely tonight",
        "Can't focus, mind is all over the place",
        "Exhausted but satisfied after finishing my project"
    ]
    
    print("\nAnalyzing multiple messages...")
    results = await analyzer.batch_analyze_moods(messages)
    
    print(f"\nProcessed {len(results)} messages:")
    for i, (msg, result) in enumerate(zip(messages, results), 1):
        print(f"\n{i}. '{msg}'")
        print(f"   → {result.primary_mood} (intensity: {result.intensity})")
        print(f"   → Need: {result.immediate_need}")


async def quick_analyze_example():
    """Example using the convenience function."""
    print("\n" + "=" * 60)
    print("Quick Analyze Example")
    print("=" * 60)
    
    # One-liner mood analysis
    result = await quick_analyze("Feeling overwhelmed with everything on my plate")
    
    print(f"\nQuick analysis result:")
    print(f"  Mood: {result.primary_mood} (intensity: {result.intensity})")
    print(f"  Strategy: {result.immediate_need}")


async def edge_cases_example():
    """Example with ambiguous or unclear input."""
    print("\n" + "=" * 60)
    print("Edge Cases Example")
    print("=" * 60)
    
    analyzer = MoodAnalyzer()
    
    # Ambiguous mood
    vague_input = "Idk, just kinda meh I guess"
    result1 = await analyzer.analyze_mood(vague_input)
    
    print(f"\nVague input: '{vague_input}'")
    print(f"  Primary Mood: {result1.primary_mood}")
    print(f"  Confidence: {result1.confidence:.0%}")
    
    # Very intense emotion
    intense_input = "I'm absolutely FURIOUS! They lied to me again!"
    result2 = await analyzer.analyze_mood(intense_input)
    
    print(f"\nIntense input: '{intense_input}'")
    print(f"  Primary Mood: {result2.primary_mood}")
    print(f"  Intensity: {result2.intensity}/10")
    print(f"  Immediate Need: {result2.immediate_need}")
    
    # Complex emotional state
    complex_input = "I feel nostalgic looking at old photos but it also makes me sad"
    result3 = await analyzer.analyze_mood(complex_input)
    
    print(f"\nComplex input: '{complex_input}'")
    print(f"  Primary Mood: {result3.primary_mood}")
    print(f"  Multi-mood: {result3.multi_mood}")
    if result3.secondary_moods:
        print(f"  Secondary: {', '.join(result3.secondary_moods)}")


async def error_handling_example():
    """Example of error handling."""
    print("\n" + "=" * 60)
    print("Error Handling Example")
    print("=" * 60)
    
    analyzer = MoodAnalyzer()
    
    # Empty input
    try:
        await analyzer.analyze_mood("")
    except ValueError as e:
        print(f"\nEmpty input error (expected): {e}")
    
    # Invalid API key (will fail if env var is not set correctly)
    try:
        bad_analyzer = MoodAnalyzer(api_key="invalid_key_123")
        await bad_analyzer.analyze_mood("I'm happy")
    except Exception as e:
        print(f"\nInvalid API key error (expected): {type(e).__name__}")


async def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "MoodMatch Mood Analysis Examples" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Check for API key
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  WARNING: GEMINI_API_KEY environment variable not set!")
        print("Please set it to run these examples:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        return
    
    try:
        # Run examples sequentially
        await basic_example()
        await multi_mood_example()
        await context_example()
        await batch_example()
        await quick_analyze_example()
        await edge_cases_example()
        await error_handling_example()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        raise


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())
