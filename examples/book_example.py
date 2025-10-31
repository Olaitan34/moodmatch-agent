"""
Examples demonstrating the Google Books recommendation service.

Run with: python examples/book_example.py
"""

import asyncio
import os
from dotenv import load_dotenv

from services import (
    MoodAnalysis,
    GoogleBooksService,
    create_books_service,
    get_book_for_mood,
)

# Load environment variables
load_dotenv()


# ============================================================================
# Example 1: Basic Book Recommendation
# ============================================================================


async def basic_example():
    """Basic example of getting book recommendation for a mood."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Book Recommendation")
    print("=" * 70)
    
    # Get Google Books API key from environment (optional)
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    if api_key:
        print("✅ Using Google Books API key (higher rate limits)")
    else:
        print("ℹ️  No API key provided (using default rate limits)")
    
    # Create Google Books service
    service = GoogleBooksService(api_key=api_key)
    
    try:
        # Create a sample mood analysis
        mood = MoodAnalysis(
            primary_mood="contemplative",
            intensity=6,
            immediate_need="process",
            book_preferences={
                "pacing": "moderate",
                "depth": "profound",
                "preferred_genres": ["Fiction", "Literary Fiction"],
                "themes": ["meaning", "identity", "growth"],
                "keywords": ["thoughtful", "introspective"]
            },
            music_preferences={},
            movie_preferences={}
        )
        
        # Get recommendation
        print(f"\n📚 Getting book for mood: {mood.primary_mood} (intensity: {mood.intensity}/10)")
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print("\n✅ Recommendation found!")
            print(f"Title: {recommendation.title}")
            print(f"Author: {recommendation.author}" if recommendation.author else "Author: Unknown")
            print(f"Year: {recommendation.year}" if recommendation.year else "Year: Unknown")
            print(f"Pages: {recommendation.pages}" if recommendation.pages else "Pages: Unknown")
            print(f"Rating: {recommendation.rating}/5" if recommendation.rating else "Rating: N/A")
            print(f"Reading Time: {recommendation.reading_time}")
            print(f"Themes: {', '.join(recommendation.themes)}")
            print(f"Mood Match: {recommendation.mood_match}")
            print(f"Why: {recommendation.why}")
            print(f"\nWhere to find it:")
            for platform, url in recommendation.urls.items():
                print(f"  • {platform.replace('_', ' ').title()}: {url[:60]}...")
            if recommendation.cover_url:
                print(f"\nCover: {recommendation.cover_url[:60]}...")
            if recommendation.description:
                print(f"\nDescription: {recommendation.description[:200]}...")
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
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    service = GoogleBooksService(api_key=api_key)
    
    try:
        # Test different moods
        moods = [
            MoodAnalysis(
                primary_mood="happy",
                intensity=8,
                immediate_need="match",
                book_preferences={
                    "pacing": "fast",
                    "depth": "light",
                    "preferred_genres": ["Humor", "Fiction"],
                    "themes": ["joy", "friendship", "adventure"],
                    "keywords": ["funny", "uplifting"]
                },
                music_preferences={},
                movie_preferences={}
            ),
            MoodAnalysis(
                primary_mood="anxious",
                intensity=7,
                immediate_need="calm",
                book_preferences={
                    "pacing": "slow",
                    "depth": "moderate",
                    "preferred_genres": ["Self-Help", "Philosophy"],
                    "themes": ["peace", "mindfulness", "acceptance"],
                    "keywords": ["calming", "wisdom"]
                },
                music_preferences={},
                movie_preferences={}
            ),
            MoodAnalysis(
                primary_mood="motivated",
                intensity=8,
                immediate_need="channel",
                book_preferences={
                    "pacing": "moderate",
                    "depth": "practical",
                    "preferred_genres": ["Business", "Self-Improvement"],
                    "themes": ["success", "productivity", "growth"],
                    "keywords": ["actionable", "inspiring"]
                },
                music_preferences={},
                movie_preferences={}
            ),
        ]
        
        for mood in moods:
            print(f"\n📚 Mood: {mood.primary_mood} | Need: {mood.immediate_need}")
            recommendation = await service.get_recommendation(mood)
            
            if recommendation:
                print(f"   ✓ {recommendation.title}")
                if recommendation.author:
                    print(f"     by {recommendation.author}")
                print(f"   → {recommendation.mood_match}")
                print(f"   ⏱️  Reading time: {recommendation.reading_time}")
                if recommendation.rating:
                    print(f"   ⭐ {recommendation.rating}/5")
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
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    service = GoogleBooksService(api_key=api_key)
    
    try:
        # Complex mood with multiple feelings
        mood = MoodAnalysis(
            primary_mood="bittersweet",
            intensity=6,
            immediate_need="process",
            multi_mood=True,
            secondary_moods=["nostalgic", "hopeful"],
            book_preferences={
                "pacing": "moderate",
                "depth": "profound",
                "preferred_genres": ["Literary Fiction", "Memoir"],
                "themes": ["memory", "loss", "healing", "hope"],
                "keywords": ["emotional", "beautiful", "poignant"]
            },
            music_preferences={},
            movie_preferences={}
        )
        
        print(f"\n📚 Primary mood: {mood.primary_mood}")
        print(f"   Secondary moods: {', '.join(mood.secondary_moods)}")
        print(f"   Immediate need: {mood.immediate_need}")
        
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print("\n✅ Recommendation:")
            print(f"   Title: {recommendation.title}")
            if recommendation.author:
                print(f"   Author: {recommendation.author}")
            print(f"   Themes: {', '.join(recommendation.themes)}")
            print(f"   Match: {recommendation.mood_match}")
            print(f"   Why: {recommendation.why}")
            print(f"   Reading time: {recommendation.reading_time}")
            print(f"\n   Find it on:")
            for platform, url in list(recommendation.urls.items())[:2]:
                print(f"     • {platform.replace('_', ' ').title()}: {url[:50]}...")
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
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    mood = MoodAnalysis(
        primary_mood="curious",
        intensity=7,
        immediate_need="escape",
        book_preferences={
            "pacing": "moderate",
            "depth": "moderate",
            "preferred_genres": ["Science", "History", "Non-Fiction"],
            "themes": ["discovery", "exploration", "knowledge"],
            "keywords": ["fascinating", "informative"]
        },
        music_preferences={},
        movie_preferences={}
    )
    
    print(f"\n📚 Using convenience function for: {mood.primary_mood}")
    
    # Use the convenience function (automatically handles service cleanup)
    recommendation = await get_book_for_mood(
        mood_analysis=mood,
        api_key=api_key
    )
    
    if recommendation:
        print(f"\n✅ {recommendation.title}")
        if recommendation.author:
            print(f"   by {recommendation.author}")
        print(f"   Perfect for: {recommendation.mood_match}")
        print(f"   Reading time: {recommendation.reading_time}")
        print(f"   {recommendation.urls.get('google_books', 'N/A')[:60]}...")


# ============================================================================
# Example 5: Batch Recommendations
# ============================================================================


async def batch_recommendations_example():
    """Get recommendations for multiple moods in parallel."""
    print("\n" + "=" * 70)
    print("Example 5: Batch Recommendations")
    print("=" * 70)
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    service = GoogleBooksService(api_key=api_key)
    
    try:
        # Multiple moods to process
        moods = [
            MoodAnalysis(
                primary_mood="relaxed",
                intensity=4,
                immediate_need="calm",
                book_preferences={
                    "pacing": "slow",
                    "depth": "light",
                    "preferred_genres": ["Travel", "Nature"],
                    "themes": ["peace", "beauty"],
                    "keywords": ["serene", "pleasant"]
                },
                music_preferences={},
                movie_preferences={}
            ),
            MoodAnalysis(
                primary_mood="adventurous",
                intensity=8,
                immediate_need="escape",
                book_preferences={
                    "pacing": "fast",
                    "depth": "moderate",
                    "preferred_genres": ["Fantasy", "Science Fiction"],
                    "themes": ["adventure", "heroism"],
                    "keywords": ["epic", "thrilling"]
                },
                music_preferences={},
                movie_preferences={}
            ),
            MoodAnalysis(
                primary_mood="reflective",
                intensity=5,
                immediate_need="process",
                book_preferences={
                    "pacing": "slow",
                    "depth": "profound",
                    "preferred_genres": ["Philosophy", "Poetry"],
                    "themes": ["existence", "truth"],
                    "keywords": ["deep", "contemplative"]
                },
                music_preferences={},
                movie_preferences={}
            ),
        ]
        
        print(f"\n📚 Getting recommendations for {len(moods)} moods...")
        
        # Get recommendations in parallel
        tasks = [service.get_recommendation(mood) for mood in moods]
        recommendations = await asyncio.gather(*tasks)
        
        print("\n✅ Results:")
        for mood, rec in zip(moods, recommendations):
            if rec:
                print(f"\n   {mood.primary_mood.upper()}:")
                print(f"   → {rec.title}")
                if rec.author:
                    print(f"      by {rec.author}")
                print(f"   → Reading time: {rec.reading_time}")
                if rec.rating:
                    print(f"   → Rating: {rec.rating}/5")
            else:
                print(f"\n   {mood.primary_mood.upper()}: No recommendation found")
    finally:
        await service.close()


# ============================================================================
# Example 6: Genre-Specific Search
# ============================================================================


async def genre_specific_example():
    """Test genre-specific book recommendations."""
    print("\n" + "=" * 70)
    print("Example 6: Genre-Specific Search")
    print("=" * 70)
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    service = GoogleBooksService(api_key=api_key)
    
    try:
        # Test specific genre combinations
        genre_tests = [
            ("Mystery Thriller", ["Mystery", "Thriller"], ["suspense", "intrigue"]),
            ("Historical Fiction", ["Historical Fiction", "Drama"], ["history", "period"]),
            ("Romance", ["Romance", "Contemporary"], ["love", "relationships"]),
        ]
        
        for name, genres, themes in genre_tests:
            mood = MoodAnalysis(
                primary_mood="engaged",
                intensity=7,
                immediate_need="escape",
                book_preferences={
                    "pacing": "moderate",
                    "depth": "moderate",
                    "preferred_genres": genres,
                    "themes": themes,
                    "keywords": ["engaging"]
                },
                music_preferences={},
                movie_preferences={}
            )
            
            print(f"\n📚 Searching for: {name}")
            recommendation = await service.get_recommendation(mood)
            
            if recommendation:
                print(f"   ✓ {recommendation.title}")
                if recommendation.author:
                    print(f"     by {recommendation.author}")
                print(f"   → Themes: {', '.join(recommendation.themes)}")
                if recommendation.pages:
                    print(f"   → {recommendation.pages} pages ({recommendation.reading_time})")
            else:
                print("   ✗ No recommendation found")
    finally:
        await service.close()


# ============================================================================
# Example 7: Fallback Handling
# ============================================================================


async def fallback_example():
    """Demonstrate fallback mechanisms."""
    print("\n" + "=" * 70)
    print("Example 7: Fallback Handling")
    print("=" * 70)
    
    # Test with no API key and vague search (triggers fallback)
    print("\n📝 Testing fallback with curated recommendations...")
    
    service = GoogleBooksService(api_key=None)
    
    try:
        # Vague mood that might trigger fallback
        mood = MoodAnalysis(
            primary_mood="happy",
            intensity=7,
            immediate_need="match",
            book_preferences={
                "pacing": "moderate",
                "depth": "moderate",
                "preferred_genres": ["Fiction"],
                "themes": ["happiness"],
                "keywords": []
            },
            music_preferences={},
            movie_preferences={}
        )
        
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print(f"\n✅ Fallback/recommendation provided:")
            print(f"   Title: {recommendation.title}")
            if recommendation.author:
                print(f"   Author: {recommendation.author}")
            print(f"   Match: {recommendation.mood_match}")
            print(f"   Available at:")
            for platform in list(recommendation.urls.keys())[:2]:
                print(f"     • {platform.replace('_', ' ').title()}")
        else:
            print("✅ Correctly handled edge case")
    finally:
        await service.close()


# ============================================================================
# Example 8: Factory Function
# ============================================================================


async def factory_function_example():
    """Use the factory function to create service."""
    print("\n" + "=" * 70)
    print("Example 8: Factory Function")
    print("=" * 70)
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    
    # Use factory function
    service = create_books_service(api_key=api_key)
    
    try:
        mood = MoodAnalysis(
            primary_mood="inspired",
            intensity=8,
            immediate_need="uplift",
            book_preferences={
                "pacing": "moderate",
                "depth": "practical",
                "preferred_genres": ["Biography", "Memoir"],
                "themes": ["achievement", "perseverance"],
                "keywords": ["inspiring", "motivational"]
            },
            music_preferences={},
            movie_preferences={}
        )
        
        print(f"\n📚 Created service using factory function")
        recommendation = await service.get_recommendation(mood)
        
        if recommendation:
            print(f"\n✅ {recommendation.title}")
            if recommendation.author:
                print(f"   by {recommendation.author}")
            print(f"   {recommendation.mood_match}")
            print(f"   Reading time: {recommendation.reading_time}")
    finally:
        await service.close()


# ============================================================================
# Main Runner
# ============================================================================


async def main():
    """Run all examples."""
    print("\n" + "📚" * 35)
    print("GOOGLE BOOKS RECOMMENDATION SERVICE EXAMPLES")
    print("📚" * 35)
    
    # Run all examples
    await basic_example()
    await mood_states_example()
    await multi_mood_example()
    await convenience_function_example()
    await batch_recommendations_example()
    await genre_specific_example()
    await fallback_example()
    await factory_function_example()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
