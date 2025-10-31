"""
Examples demonstrating the TMDB movie recommendation service.

Run with: python examples/movie_example.py
"""

import asyncio
import os
from dotenv import load_dotenv

from services import (
    MoodAnalysis,
    TMDBMovieService,
    create_movie_service,
    get_movie_for_mood,
)

# Load environment variables
load_dotenv()


# ============================================================================
# Example 1: Basic Movie Recommendation
# ============================================================================


async def basic_example():
    """Basic example of getting movie recommendation for a mood."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Movie Recommendation")
    print("=" * 70)
    
    # Get TMDB API key from environment
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  TMDB API key not found in environment")
        print("Please set TMDB_API_KEY in your .env file")
        return
    
    # Create TMDB service
    service = TMDBMovieService(api_key=api_key)
    
    try:
        # Create a sample mood analysis
        mood = MoodAnalysis(
            primary_mood="happy",
            intensity=8,
            immediate_need="match",
            movie_preferences={
                "tone": "light",
                "preferred_genres": ["Comedy", "Romance"],
                "themes": ["friendship", "love"],
                "keywords": ["feel-good", "heartwarming"],
                "length_preference": "standard"
            },
            music_preferences={},
            book_preferences={}
        )
        
        # Get recommendation
        print(f"\n🎬 Getting movie for mood: {mood.primary_mood} (intensity: {mood.intensity}/10)")
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print("\n✅ Recommendation found!")
            print(f"Title: {recommendation.title} ({recommendation.year})")
            print(f"Rating: {recommendation.rating}/10" if recommendation.rating else "Rating: N/A")
            print(f"Runtime: {recommendation.runtime}" if recommendation.runtime else "Runtime: N/A")
            print(f"Genres: {', '.join(recommendation.genres)}")
            print(f"Mood Match: {recommendation.mood_match}")
            print(f"Why: {recommendation.why}")
            print(f"Platforms: {', '.join(recommendation.platforms)}")
            print(f"URL: {recommendation.url}")
            if recommendation.poster_url:
                print(f"Poster: {recommendation.poster_url[:60]}...")
            if recommendation.overview:
                print(f"Overview: {recommendation.overview[:150]}...")
        else:
            print("❌ No recommendation found")
    finally:
        await service.close()


# ============================================================================
# Example 2: Different Mood States
# ============================================================================


async def mood_states_example():
    """Test recommendations for different mood states."""
    print("\n" + "=" * 70)
    print("Example 2: Different Mood States")
    print("=" * 70)
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  TMDB API key not found")
        return
    
    service = TMDBMovieService(api_key=api_key)
    
    try:
        # Test different moods
        moods = [
            MoodAnalysis(
                primary_mood="sad",
                intensity=7,
                immediate_need="process",
                movie_preferences={
                    "tone": "serious",
                    "preferred_genres": ["Drama"],
                    "themes": ["loss", "grief", "healing"],
                    "keywords": ["emotional", "touching"],
                },
                music_preferences={},
                book_preferences={}
            ),
            MoodAnalysis(
                primary_mood="adventurous",
                intensity=8,
                immediate_need="escape",
                movie_preferences={
                    "tone": "exciting",
                    "preferred_genres": ["Action", "Adventure"],
                    "themes": ["exploration", "heroism"],
                    "keywords": ["thrilling", "epic"],
                },
                music_preferences={},
                book_preferences={}
            ),
            MoodAnalysis(
                primary_mood="scared",
                intensity=6,
                immediate_need="channel",
                movie_preferences={
                    "tone": "dark",
                    "preferred_genres": ["Thriller", "Horror"],
                    "themes": ["suspense", "mystery"],
                    "keywords": ["scary", "intense"],
                },
                music_preferences={},
                book_preferences={}
            ),
        ]
        
        for mood in moods:
            print(f"\n🎬 Mood: {mood.primary_mood} | Need: {mood.immediate_need}")
            recommendation = await service.get_recommendation(mood)
            
            if recommendation:
                print(f"   ✓ {recommendation.title} ({recommendation.year})")
                print(f"   → {recommendation.mood_match}")
                print(f"   ⭐ Rating: {recommendation.rating}/10" if recommendation.rating else "   ⭐ Rating: N/A")
                print(f"   🔗 {recommendation.url}")
            else:
                print("   ✗ No recommendation found")
    finally:
        await service.close()


# ============================================================================
# Example 3: Multi-Mood Recommendation
# ============================================================================


async def multi_mood_example():
    """Get recommendation for complex multi-mood state."""
    print("\n" + "=" * 70)
    print("Example 3: Multi-Mood Recommendation")
    print("=" * 70)
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  TMDB API key not found")
        return
    
    service = TMDBMovieService(api_key=api_key)
    
    try:
        # Complex mood with multiple feelings
        mood = MoodAnalysis(
            primary_mood="nostalgic",
            intensity=6,
            immediate_need="process",
            multi_mood=True,
            secondary_moods=["bittersweet", "reflective"],
            movie_preferences={
                "tone": "balanced",
                "preferred_genres": ["Drama", "Romance"],
                "themes": ["coming-of-age", "memories", "growth"],
                "keywords": ["nostalgic", "heartfelt", "meaningful"],
                "length_preference": "standard"
            },
            music_preferences={},
            book_preferences={}
        )
        
        print(f"\n🎬 Primary mood: {mood.primary_mood}")
        print(f"   Secondary moods: {', '.join(mood.secondary_moods)}")
        print(f"   Immediate need: {mood.immediate_need}")
        
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print("\n✅ Recommendation:")
            print(f"   Title: {recommendation.title} ({recommendation.year})")
            print(f"   Genres: {', '.join(recommendation.genres)}")
            print(f"   Rating: {recommendation.rating}/10" if recommendation.rating else "   Rating: N/A")
            print(f"   Match: {recommendation.mood_match}")
            print(f"   Why: {recommendation.why}")
            print(f"   Platforms: {', '.join(recommendation.platforms)}")
            print(f"   Link: {recommendation.url}")
    finally:
        await service.close()


# ============================================================================
# Example 4: Convenience Function
# ============================================================================


async def convenience_function_example():
    """Use the convenience function for quick recommendations."""
    print("\n" + "=" * 70)
    print("Example 4: Convenience Function")
    print("=" * 70)
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  TMDB API key not found")
        return
    
    mood = MoodAnalysis(
        primary_mood="inspired",
        intensity=7,
        immediate_need="uplift",
        movie_preferences={
            "tone": "uplifting",
            "preferred_genres": ["Biography", "Drama"],
            "themes": ["achievement", "perseverance", "success"],
            "keywords": ["inspiring", "motivational"],
        },
        music_preferences={},
        book_preferences={}
    )
    
    print(f"\n🎬 Using convenience function for: {mood.primary_mood}")
    
    # Use the convenience function (automatically handles service cleanup)
    recommendation = await get_movie_for_mood(
        mood_analysis=mood,
        api_key=api_key
    )
    
    if recommendation:
        print(f"\n✅ {recommendation.title} ({recommendation.year})")
        print(f"   Genres: {', '.join(recommendation.genres)}")
        print(f"   Perfect for: {recommendation.mood_match}")
        print(f"   {recommendation.url}")


# ============================================================================
# Example 5: Batch Recommendations
# ============================================================================


async def batch_recommendations_example():
    """Get recommendations for multiple moods in parallel."""
    print("\n" + "=" * 70)
    print("Example 5: Batch Recommendations")
    print("=" * 70)
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  TMDB API key not found")
        return
    
    service = TMDBMovieService(api_key=api_key)
    
    try:
        # Multiple moods to process
        moods = [
            MoodAnalysis(
                primary_mood="relaxed",
                intensity=4,
                immediate_need="calm",
                movie_preferences={
                    "tone": "light",
                    "preferred_genres": ["Animation", "Family"],
                    "themes": ["friendship", "adventure"],
                    "keywords": ["wholesome", "fun"],
                },
                music_preferences={},
                book_preferences={}
            ),
            MoodAnalysis(
                primary_mood="curious",
                intensity=6,
                immediate_need="match",
                movie_preferences={
                    "tone": "thought-provoking",
                    "preferred_genres": ["Documentary", "Sci-Fi"],
                    "themes": ["discovery", "knowledge"],
                    "keywords": ["fascinating", "mind-bending"],
                },
                music_preferences={},
                book_preferences={}
            ),
            MoodAnalysis(
                primary_mood="romantic",
                intensity=7,
                immediate_need="match",
                movie_preferences={
                    "tone": "warm",
                    "preferred_genres": ["Romance", "Comedy"],
                    "themes": ["love", "relationships"],
                    "keywords": ["romantic", "charming"],
                },
                music_preferences={},
                book_preferences={}
            ),
        ]
        
        print(f"\n🎬 Getting recommendations for {len(moods)} moods...")
        
        # Get recommendations in parallel
        tasks = [service.get_recommendation(mood) for mood in moods]
        recommendations = await asyncio.gather(*tasks)
        
        print("\n✅ Results:")
        for mood, rec in zip(moods, recommendations):
            if rec:
                print(f"\n   {mood.primary_mood.upper()}:")
                print(f"   → {rec.title} ({rec.year})")
                print(f"   → {', '.join(rec.genres)}")
                print(f"   → Rating: {rec.rating}/10" if rec.rating else "   → Rating: N/A")
            else:
                print(f"\n   {mood.primary_mood.upper()}: No recommendation found")
    finally:
        await service.close()


# ============================================================================
# Example 6: Genre-Specific Search
# ============================================================================


async def genre_specific_example():
    """Test genre-specific movie recommendations."""
    print("\n" + "=" * 70)
    print("Example 6: Genre-Specific Search")
    print("=" * 70)
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  TMDB API key not found")
        return
    
    service = TMDBMovieService(api_key=api_key)
    
    try:
        # Test specific genre combinations
        genre_tests = [
            ("Sci-Fi Thriller", ["Sci-Fi", "Thriller"], "tense"),
            ("Fantasy Adventure", ["Fantasy", "Adventure"], "exciting"),
            ("Crime Drama", ["Crime", "Drama"], "serious"),
        ]
        
        for name, genres, tone in genre_tests:
            mood = MoodAnalysis(
                primary_mood="engaged",
                intensity=7,
                immediate_need="escape",
                movie_preferences={
                    "tone": tone,
                    "preferred_genres": genres,
                    "themes": ["story"],
                    "keywords": ["gripping"],
                },
                music_preferences={},
                book_preferences={}
            )
            
            print(f"\n🎬 Searching for: {name}")
            recommendation = await service.get_recommendation(mood)
            
            if recommendation:
                print(f"   ✓ {recommendation.title}")
                print(f"   → Genres: {', '.join(recommendation.genres)}")
                print(f"   → Rating: {recommendation.rating}/10" if recommendation.rating else "   → Rating: N/A")
            else:
                print("   ✗ No recommendation found")
    finally:
        await service.close()


# ============================================================================
# Example 7: Error Handling
# ============================================================================


async def error_handling_example():
    """Demonstrate error handling and fallback mechanisms."""
    print("\n" + "=" * 70)
    print("Example 7: Error Handling")
    print("=" * 70)
    
    # Test with invalid API key
    print("\n📝 Testing with invalid API key...")
    
    service = TMDBMovieService(api_key="invalid_api_key")
    
    try:
        mood = MoodAnalysis(
            primary_mood="happy",
            intensity=7,
            immediate_need="match",
            movie_preferences={
                "tone": "light",
                "preferred_genres": ["Comedy"],
                "themes": ["friendship"],
                "keywords": ["funny"],
            },
            music_preferences={},
            book_preferences={}
        )
        
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print(f"✅ Fallback handled gracefully")
            print(f"   (Would have returned: {recommendation.title})")
        else:
            print("✅ Correctly returned None for invalid API key")
    finally:
        await service.close()
    
    # Test with missing API key
    print("\n\n📝 Testing with missing API key...")
    try:
        service = TMDBMovieService(api_key="")
        print("❌ Should have raised ValueError")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")


# ============================================================================
# Example 8: Factory Function
# ============================================================================


async def factory_function_example():
    """Use the factory function to create service."""
    print("\n" + "=" * 70)
    print("Example 8: Factory Function")
    print("=" * 70)
    
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  TMDB API key not found")
        return
    
    # Use factory function
    service = create_movie_service(api_key=api_key)
    
    try:
        mood = MoodAnalysis(
            primary_mood="contemplative",
            intensity=5,
            immediate_need="process",
            movie_preferences={
                "tone": "thoughtful",
                "preferred_genres": ["Drama", "Mystery"],
                "themes": ["meaning", "philosophy"],
                "keywords": ["deep", "contemplative"],
            },
            music_preferences={},
            book_preferences={}
        )
        
        print(f"\n🎬 Created service using factory function")
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print(f"\n✅ {recommendation.title} ({recommendation.year})")
            print(f"   {recommendation.mood_match}")
            print(f"   {recommendation.url}")
    finally:
        await service.close()


# ============================================================================
# Main Runner
# ============================================================================


async def main():
    """Run all examples."""
    print("\n" + "🎬" * 35)
    print("TMDB MOVIE RECOMMENDATION SERVICE EXAMPLES")
    print("🎬" * 35)
    
    # Run all examples
    await basic_example()
    await mood_states_example()
    await multi_mood_example()
    await convenience_function_example()
    await batch_recommendations_example()
    await genre_specific_example()
    await error_handling_example()
    await factory_function_example()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
