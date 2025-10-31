"""
Examples demonstrating the unified recommendation orchestrator.

This orchestrator coordinates all three media services (music, movies, books)
to provide comprehensive mood-based recommendations.

Run with: python examples/unified_example.py
"""

import asyncio
import os
from dotenv import load_dotenv

from services import MoodAnalysis, MoodAnalyzer
from agents import (
    RecommendationOrchestrator,
    create_orchestrator,
    get_recommendations_for_mood,
)

# Load environment variables
load_dotenv()


# ============================================================================
# Example 1: Complete Recommendation Suite
# ============================================================================


async def complete_suite_example():
    """Get recommendations for all media types at once."""
    print("\n" + "=" * 70)
    print("Example 1: Complete Recommendation Suite")
    print("=" * 70)
    
    # Get API credentials
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    tmdb_key = os.getenv("TMDB_API_KEY")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    # Create orchestrator
    orchestrator = RecommendationOrchestrator(
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        tmdb_api_key=tmdb_key,
        google_books_api_key=books_key
    )
    
    try:
        # Create mood analysis
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
            movie_preferences={
                "tone": "light",
                "preferred_genres": ["Comedy", "Romance"],
                "themes": ["friendship", "love"],
                "keywords": ["feel-good", "heartwarming"]
            },
            book_preferences={
                "pacing": "moderate",
                "depth": "light",
                "preferred_genres": ["Fiction", "Humor"],
                "themes": ["happiness", "joy"],
                "keywords": ["uplifting", "funny"]
            }
        )
        
        print(f"\n🎯 Mood: {mood.primary_mood} (Intensity: {mood.intensity}/10)")
        print(f"   Need: {mood.immediate_need}")
        print("\n🔍 Getting recommendations across all media types...")
        
        # Get all recommendations
        recommendations = await orchestrator.get_all_recommendations(mood)
        
        print(f"\n📋 {recommendations.summary}")
        print("\n" + "=" * 70)
        
        # Display music recommendation
        if recommendations.music:
            print("\n🎵 MUSIC RECOMMENDATION:")
            print(f"   Title: {recommendations.music.title}")
            print(f"   Platform: {recommendations.music.platform}")
            print(f"   Match: {recommendations.music.mood_match}")
            print(f"   Use Case: {recommendations.music.use_case}")
            print(f"   Duration: {recommendations.music.duration}")
            print(f"   🔗 {recommendations.music.url}")
        else:
            print("\n🎵 MUSIC: Not available")
        
        # Display movie recommendation
        if recommendations.movie:
            print("\n🎬 MOVIE RECOMMENDATION:")
            print(f"   Title: {recommendations.movie.title} ({recommendations.movie.year})")
            print(f"   Rating: {recommendations.movie.rating}/10" if recommendations.movie.rating else "   Rating: N/A")
            print(f"   Genres: {', '.join(recommendations.movie.genres)}")
            print(f"   Match: {recommendations.movie.mood_match}")
            print(f"   Why: {recommendations.movie.why}")
            print(f"   Platforms: {', '.join(recommendations.movie.platforms)}")
            print(f"   🔗 {recommendations.movie.url}")
        else:
            print("\n🎬 MOVIE: Not available")
        
        # Display book recommendation
        if recommendations.book:
            print("\n📚 BOOK RECOMMENDATION:")
            print(f"   Title: {recommendations.book.title}")
            if recommendations.book.author:
                print(f"   Author: {recommendations.book.author}")
            print(f"   Rating: {recommendations.book.rating}/5" if recommendations.book.rating else "   Rating: N/A")
            print(f"   Reading Time: {recommendations.book.reading_time}")
            print(f"   Themes: {', '.join(recommendations.book.themes)}")
            print(f"   Match: {recommendations.book.mood_match}")
            print(f"   🔗 {recommendations.book.urls.get('google_books', 'N/A')[:60]}...")
        else:
            print("\n📚 BOOK: Not available")
            
    finally:
        await orchestrator.close()


# ============================================================================
# Example 2: Individual Service Requests
# ============================================================================


async def individual_services_example():
    """Request recommendations from individual services."""
    print("\n" + "=" * 70)
    print("Example 2: Individual Service Requests")
    print("=" * 70)
    
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    tmdb_key = os.getenv("TMDB_API_KEY")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    orchestrator = RecommendationOrchestrator(
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        tmdb_api_key=tmdb_key,
        google_books_api_key=books_key
    )
    
    try:
        mood = MoodAnalysis(
            primary_mood="calm",
            intensity=4,
            immediate_need="calm",
            music_preferences={
                "energy_level": "low",
                "preferred_genres": ["ambient", "classical"],
                "vibe": ["peaceful"],
                "keywords": ["relaxing"]
            },
            movie_preferences={
                "tone": "peaceful",
                "preferred_genres": ["Drama", "Documentary"],
                "themes": ["nature", "beauty"],
                "keywords": ["serene"]
            },
            book_preferences={
                "pacing": "slow",
                "depth": "moderate",
                "preferred_genres": ["Nature", "Philosophy"],
                "themes": ["peace", "mindfulness"],
                "keywords": ["calm"]
            }
        )
        
        print(f"\n🎯 Mood: {mood.primary_mood} (Intensity: {mood.intensity}/10)")
        
        # Request each service individually
        print("\n🎵 Getting music recommendation...")
        music = await orchestrator.get_music_recommendation(mood)
        if music:
            print(f"   ✓ {music.title} - {music.use_case}")
        
        print("\n🎬 Getting movie recommendation...")
        movie = await orchestrator.get_movie_recommendation(mood)
        if movie:
            print(f"   ✓ {movie.title} ({movie.year})")
        
        print("\n📚 Getting book recommendation...")
        book = await orchestrator.get_book_recommendation(mood)
        if book:
            print(f"   ✓ {book.title}" + (f" by {book.author}" if book.author else ""))
            
    finally:
        await orchestrator.close()


# ============================================================================
# Example 3: End-to-End with Mood Analysis
# ============================================================================


async def end_to_end_example():
    """Complete workflow: analyze mood → get recommendations."""
    print("\n" + "=" * 70)
    print("Example 3: End-to-End with Mood Analysis")
    print("=" * 70)
    
    # Get API keys
    gemini_key = os.getenv("GEMINI_API_KEY")
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    tmdb_key = os.getenv("TMDB_API_KEY")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if not gemini_key:
        print("⚠️  GEMINI_API_KEY not found, skipping this example")
        return
    
    # Step 1: Analyze user's mood
    print("\n📝 User message: 'I'm feeling overwhelmed and stressed from work...'")
    print("\n🧠 Analyzing mood with Gemini...")
    
    analyzer = MoodAnalyzer(api_key=gemini_key)
    mood = await analyzer.analyze_mood(
        "I'm feeling overwhelmed and stressed from work. Need something to help me decompress."
    )
    
    print(f"\n✅ Mood Analysis:")
    print(f"   Primary Mood: {mood.primary_mood}")
    print(f"   Intensity: {mood.intensity}/10")
    print(f"   Immediate Need: {mood.immediate_need}")
    print(f"   Confidence: {mood.confidence}")
    
    # Step 2: Get recommendations
    print("\n🔍 Getting personalized recommendations...")
    
    orchestrator = RecommendationOrchestrator(
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        tmdb_api_key=tmdb_key,
        google_books_api_key=books_key
    )
    
    try:
        recommendations = await orchestrator.get_all_recommendations(mood)
        
        print(f"\n✨ {recommendations.summary}\n")
        
        if recommendations.music:
            print(f"🎵 Listen: {recommendations.music.title}")
            print(f"   {recommendations.music.mood_match}")
        
        if recommendations.movie:
            print(f"\n🎬 Watch: {recommendations.movie.title}")
            print(f"   {recommendations.movie.mood_match}")
        
        if recommendations.book:
            print(f"\n📚 Read: {recommendations.book.title}")
            print(f"   {recommendations.book.mood_match}")
            
    finally:
        await orchestrator.close()


# ============================================================================
# Example 4: Convenience Function
# ============================================================================


async def convenience_function_example():
    """Use convenience function for quick recommendations."""
    print("\n" + "=" * 70)
    print("Example 4: Convenience Function")
    print("=" * 70)
    
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    tmdb_key = os.getenv("TMDB_API_KEY")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    mood = MoodAnalysis(
        primary_mood="inspired",
        intensity=8,
        immediate_need="channel",
        music_preferences={
            "energy_level": "high",
            "preferred_genres": ["rock", "electronic"],
            "vibe": ["powerful", "energetic"],
            "keywords": ["motivating"]
        },
        movie_preferences={
            "tone": "inspiring",
            "preferred_genres": ["Drama", "Biography"],
            "themes": ["achievement", "perseverance"],
            "keywords": ["motivational"]
        },
        book_preferences={
            "pacing": "moderate",
            "depth": "practical",
            "preferred_genres": ["Self-Improvement", "Biography"],
            "themes": ["success", "growth"],
            "keywords": ["inspiring"]
        }
    )
    
    print(f"\n🎯 Using convenience function for: {mood.primary_mood} mood")
    
    # Use the convenience function (auto-cleanup)
    recommendations = await get_recommendations_for_mood(
        mood_analysis=mood,
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        tmdb_api_key=tmdb_key,
        google_books_api_key=books_key
    )
    
    print(f"\n✅ {recommendations.summary}")
    
    rec_count = sum([
        recommendations.music is not None,
        recommendations.movie is not None,
        recommendations.book is not None
    ])
    
    print(f"\n📊 Received {rec_count}/3 recommendations")


# ============================================================================
# Example 5: Different Mood States
# ============================================================================


async def mood_states_comparison():
    """Compare recommendations across different moods."""
    print("\n" + "=" * 70)
    print("Example 5: Different Mood States Comparison")
    print("=" * 70)
    
    spotify_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    tmdb_key = os.getenv("TMDB_API_KEY")
    books_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    orchestrator = RecommendationOrchestrator(
        spotify_client_id=spotify_id,
        spotify_client_secret=spotify_secret,
        tmdb_api_key=tmdb_key,
        google_books_api_key=books_key
    )
    
    try:
        moods = [
            ("Happy", "match", 8),
            ("Sad", "process", 6),
            ("Anxious", "calm", 7),
        ]
        
        for mood_name, need, intensity in moods:
            mood = MoodAnalysis(
                primary_mood=mood_name.lower(),
                intensity=intensity,
                immediate_need=need,
                music_preferences={"energy_level": "medium"},
                movie_preferences={"tone": "balanced"},
                book_preferences={"pacing": "moderate"}
            )
            
            print(f"\n{'─' * 70}")
            print(f"🎯 {mood_name} mood (Need: {need}, Intensity: {intensity}/10)")
            
            recommendations = await orchestrator.get_all_recommendations(mood)
            
            print(f"   Summary: {recommendations.summary}")
            
            if recommendations.music:
                print(f"   🎵 {recommendations.music.title}")
            if recommendations.movie:
                print(f"   🎬 {recommendations.movie.title}")
            if recommendations.book:
                print(f"   📚 {recommendations.book.title}")
                
    finally:
        await orchestrator.close()


# ============================================================================
# Example 6: Partial API Coverage
# ============================================================================


async def partial_api_example():
    """Demonstrate graceful handling of missing API credentials."""
    print("\n" + "=" * 70)
    print("Example 6: Partial API Coverage")
    print("=" * 70)
    
    # Only provide TMDB key (simulate missing Spotify credentials)
    tmdb_key = os.getenv("TMDB_API_KEY")
    
    print("\n📝 Testing with only TMDB API key (no Spotify credentials)")
    
    orchestrator = RecommendationOrchestrator(
        spotify_client_id=None,  # Missing
        spotify_client_secret=None,  # Missing
        tmdb_api_key=tmdb_key,
        google_books_api_key=None  # Optional
    )
    
    try:
        mood = MoodAnalysis(
            primary_mood="excited",
            intensity=8,
            immediate_need="match",
            music_preferences={},
            movie_preferences={
                "preferred_genres": ["Action", "Adventure"],
                "tone": "exciting"
            },
            book_preferences={}
        )
        
        recommendations = await orchestrator.get_all_recommendations(mood)
        
        print(f"\n✅ {recommendations.summary}")
        print("\n📊 Available services:")
        print(f"   Music: {'✓' if recommendations.music else '✗'}")
        print(f"   Movie: {'✓' if recommendations.movie else '✗'}")
        print(f"   Book: {'✓' if recommendations.book else '✗'}")
        
    finally:
        await orchestrator.close()


# ============================================================================
# Main Runner
# ============================================================================


async def main():
    """Run all examples."""
    print("\n" + "🎯" * 35)
    print("UNIFIED RECOMMENDATION ORCHESTRATOR EXAMPLES")
    print("🎯" * 35)
    
    # Run examples
    await complete_suite_example()
    await individual_services_example()
    await end_to_end_example()
    await convenience_function_example()
    await mood_states_comparison()
    await partial_api_example()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
