"""
Examples demonstrating the Spotify music recommendation service.

Run with: python examples/spotify_example.py
"""

import asyncio
import os
from dotenv import load_dotenv

from services import (
    MoodAnalysis,
    SpotifyMusicService,
    create_spotify_service,
    get_music_for_mood,
)

# Load environment variables
load_dotenv()


# ============================================================================
# Example 1: Basic Music Recommendation
# ============================================================================


async def basic_example():
    """Basic example of getting music recommendation for a mood."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Music Recommendation")
    print("=" * 70)
    
    # Get Spotify credentials from environment
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found in environment")
        print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET")
        return
    
    # Create Spotify service
    service = SpotifyMusicService(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Create a sample mood analysis
    mood = MoodAnalysis(
        primary_mood="happy",
        intensity=8,
        immediate_need="match",
        music_preferences={
            "energy_level": "high",
            "preferred_genres": ["pop", "dance"],
            "vibe": ["uplifting", "energetic"],
            "keywords": ["happy", "upbeat"]
        },
        movie_preferences={},
        book_preferences={}
    )
    
    # Get recommendation
    print(f"\n🎵 Getting music for mood: {mood.primary_mood} (intensity: {mood.intensity}/10)")
    recommendation = await service.get_recommendation(mood)
    
    if recommendation:
        print("\n✅ Recommendation found!")
        print(f"Title: {recommendation.title}")
        print(f"Platform: {recommendation.platform}")
        print(f"URL: {recommendation.url}")
        print(f"Mood Match: {recommendation.mood_match}")
        print(f"Duration: {recommendation.duration}")
        print(f"Use Case: {recommendation.use_case}")
        if recommendation.artists:
            print(f"Artists: {', '.join(recommendation.artists)}")
        if recommendation.image_url:
            print(f"Image: {recommendation.image_url[:60]}...")
    else:
        print("❌ No recommendation found")


# ============================================================================
# Example 2: Different Mood States
# ============================================================================


async def mood_states_example():
    """Test recommendations for different mood states."""
    print("\n" + "=" * 70)
    print("Example 2: Different Mood States")
    print("=" * 70)
    
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found")
        return
    
    service = SpotifyMusicService(client_id=client_id, client_secret=client_secret)
    
    # Test different moods
    moods = [
        MoodAnalysis(
            primary_mood="sad",
            intensity=6,
            immediate_need="process",
            music_preferences={
                "energy_level": "low",
                "preferred_genres": ["indie", "acoustic"],
                "vibe": ["melancholic", "introspective"],
                "keywords": ["sad", "emotional"]
            },
            movie_preferences={},
            book_preferences={}
        ),
        MoodAnalysis(
            primary_mood="energetic",
            intensity=9,
            immediate_need="channel",
            music_preferences={
                "energy_level": "very_high",
                "preferred_genres": ["electronic", "rock"],
                "vibe": ["powerful", "intense"],
                "keywords": ["energetic", "loud"]
            },
            movie_preferences={},
            book_preferences={}
        ),
        MoodAnalysis(
            primary_mood="calm",
            intensity=3,
            immediate_need="calm",
            music_preferences={
                "energy_level": "very_low",
                "preferred_genres": ["ambient", "classical"],
                "vibe": ["peaceful", "serene"],
                "keywords": ["calm", "relaxing"]
            },
            movie_preferences={},
            book_preferences={}
        ),
    ]
    
    for mood in moods:
        print(f"\n🎵 Mood: {mood.primary_mood} | Need: {mood.immediate_need}")
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print(f"   ✓ {recommendation.title}")
            print(f"   → {recommendation.mood_match}")
            print(f"   🔗 {recommendation.url}")
        else:
            print("   ✗ No recommendation found")


# ============================================================================
# Example 3: Multi-Mood Recommendation
# ============================================================================


async def multi_mood_example():
    """Get recommendation for complex multi-mood state."""
    print("\n" + "=" * 70)
    print("Example 3: Multi-Mood Recommendation")
    print("=" * 70)
    
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found")
        return
    
    service = SpotifyMusicService(client_id=client_id, client_secret=client_secret)
    
    # Complex mood with multiple feelings
    mood = MoodAnalysis(
        primary_mood="hopeful",
        intensity=6,
        immediate_need="uplift",
        multi_mood=True,
        secondary_moods=["anxious", "determined"],
        music_preferences={
            "energy_level": "medium",
            "preferred_genres": ["indie", "alternative", "folk"],
            "vibe": ["uplifting", "introspective", "hopeful"],
            "keywords": ["growth", "inspiring", "emotional"]
        },
        movie_preferences={},
        book_preferences={}
    )
    
    print(f"\n🎵 Primary mood: {mood.primary_mood}")
    print(f"   Secondary moods: {', '.join(mood.secondary_moods)}")
    print(f"   Immediate need: {mood.immediate_need}")
    
    recommendation = await service.get_recommendation(mood)
    
    if recommendation:
        print("\n✅ Recommendation:")
        print(f"   Title: {recommendation.title}")
        print(f"   Match: {recommendation.mood_match}")
        print(f"   When to listen: {recommendation.use_case}")
        print(f"   Link: {recommendation.url}")


# ============================================================================
# Example 4: Convenience Function
# ============================================================================


async def convenience_function_example():
    """Use the convenience function for quick recommendations."""
    print("\n" + "=" * 70)
    print("Example 4: Convenience Function")
    print("=" * 70)
    
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found")
        return
    
    mood = MoodAnalysis(
        primary_mood="focused",
        intensity=7,
        immediate_need="channel",
        music_preferences={
            "energy_level": "medium",
            "preferred_genres": ["lo-fi", "instrumental"],
            "vibe": ["focused", "productive"],
            "keywords": ["study", "concentration"]
        },
        movie_preferences={},
        book_preferences={}
    )
    
    print(f"\n🎵 Using convenience function for: {mood.primary_mood}")
    
    # Use the convenience function
    recommendation = await get_music_for_mood(
        mood_analysis=mood,
        client_id=client_id,
        client_secret=client_secret
    )
    
    if recommendation:
        print(f"\n✅ {recommendation.title}")
        print(f"   Perfect for: {recommendation.use_case}")
        print(f"   {recommendation.url}")


# ============================================================================
# Example 5: Batch Recommendations
# ============================================================================


async def batch_recommendations_example():
    """Get recommendations for multiple moods in parallel."""
    print("\n" + "=" * 70)
    print("Example 5: Batch Recommendations")
    print("=" * 70)
    
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found")
        return
    
    service = SpotifyMusicService(client_id=client_id, client_secret=client_secret)
    
    # Multiple moods to process
    moods = [
        MoodAnalysis(
            primary_mood="motivated",
            intensity=8,
            immediate_need="channel",
            music_preferences={
                "energy_level": "high",
                "preferred_genres": ["hip-hop", "rock"],
                "vibe": ["powerful"],
                "keywords": ["workout", "motivation"]
            },
            movie_preferences={},
            book_preferences={}
        ),
        MoodAnalysis(
            primary_mood="nostalgic",
            intensity=5,
            immediate_need="process",
            music_preferences={
                "energy_level": "medium",
                "preferred_genres": ["classic rock", "80s"],
                "vibe": ["nostalgic"],
                "keywords": ["memories", "throwback"]
            },
            movie_preferences={},
            book_preferences={}
        ),
        MoodAnalysis(
            primary_mood="romantic",
            intensity=6,
            immediate_need="match",
            music_preferences={
                "energy_level": "low",
                "preferred_genres": ["jazz", "soul"],
                "vibe": ["romantic", "smooth"],
                "keywords": ["love", "romance"]
            },
            movie_preferences={},
            book_preferences={}
        ),
    ]
    
    print(f"\n🎵 Getting recommendations for {len(moods)} moods...")
    
    # Get recommendations in parallel
    tasks = [service.get_recommendation(mood) for mood in moods]
    recommendations = await asyncio.gather(*tasks)
    
    print("\n✅ Results:")
    for mood, rec in zip(moods, recommendations):
        if rec:
            print(f"\n   {mood.primary_mood.upper()}:")
            print(f"   → {rec.title}")
            print(f"   → {rec.url}")
        else:
            print(f"\n   {mood.primary_mood.upper()}: No recommendation found")


# ============================================================================
# Example 6: Error Handling
# ============================================================================


async def error_handling_example():
    """Demonstrate error handling and fallback mechanisms."""
    print("\n" + "=" * 70)
    print("Example 6: Error Handling")
    print("=" * 70)
    
    # Test with invalid credentials (should fall back to search URL)
    print("\n📝 Testing with invalid credentials (should fallback)...")
    
    service = SpotifyMusicService(
        client_id="invalid_id",
        client_secret="invalid_secret"
    )
    
    mood = MoodAnalysis(
        primary_mood="happy",
        intensity=7,
        immediate_need="match",
        music_preferences={
            "energy_level": "high",
            "preferred_genres": ["pop"],
            "vibe": ["uplifting"],
            "keywords": ["happy"]
        },
        movie_preferences={},
        book_preferences={}
    )
    
    recommendation = await service.get_recommendation(mood)
    
    if recommendation:
        print(f"\n✅ Fallback recommendation generated:")
        print(f"   Title: {recommendation.title}")
        print(f"   URL: {recommendation.url}")
        print(f"   (This is a search URL since API failed)")
    
    # Test with missing credentials
    print("\n\n📝 Testing with missing credentials...")
    try:
        service = SpotifyMusicService(client_id="", client_secret="")
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")


# ============================================================================
# Example 7: Factory Function
# ============================================================================


async def factory_function_example():
    """Use the factory function to create service."""
    print("\n" + "=" * 70)
    print("Example 7: Factory Function")
    print("=" * 70)
    
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found")
        return
    
    # Use factory function
    service = create_spotify_service(
        client_id=client_id,
        client_secret=client_secret
    )
    
    mood = MoodAnalysis(
        primary_mood="peaceful",
        intensity=4,
        immediate_need="calm",
        music_preferences={
            "energy_level": "low",
            "preferred_genres": ["ambient", "new age"],
            "vibe": ["peaceful", "meditative"],
            "keywords": ["calm", "relaxing"]
        },
        movie_preferences={},
        book_preferences={}
    )
    
    print(f"\n🎵 Created service using factory function")
    recommendation = await service.get_recommendation(mood)
    
    if recommendation:
        print(f"\n✅ {recommendation.title}")
        print(f"   {recommendation.url}")


# ============================================================================
# Main Runner
# ============================================================================


async def main():
    """Run all examples."""
    print("\n" + "🎵" * 35)
    print("SPOTIFY MUSIC RECOMMENDATION SERVICE EXAMPLES")
    print("🎵" * 35)
    
    # Run all examples
    await basic_example()
    await mood_states_example()
    await multi_mood_example()
    await convenience_function_example()
    await batch_recommendations_example()
    await error_handling_example()
    await factory_function_example()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
