"""
Services package for MoodMatch A2A Agent.

Provides mood analysis and media recommendation services.
"""

from .mood_analyzer import (
    MoodAnalysis,
    MoodAnalyzer,
    quick_analyze,
    create_analyzer,
)
from .spotify_service import (
    MusicRecommendation,
    SpotifyMusicService,
    create_spotify_service,
    get_music_for_mood,
)
from .movie_service import (
    MovieRecommendation,
    TMDBMovieService,
    create_movie_service,
    get_movie_for_mood,
)
from .book_service import (
    BookRecommendation,
    GoogleBooksService,
    create_books_service,
    get_book_for_mood,
)

__all__ = [
    # Mood Analysis
    "MoodAnalysis",
    "MoodAnalyzer",
    "quick_analyze",
    "create_analyzer",
    # Spotify Music
    "MusicRecommendation",
    "SpotifyMusicService",
    "create_spotify_service",
    "get_music_for_mood",
    # TMDB Movies
    "MovieRecommendation",
    "TMDBMovieService",
    "create_movie_service",
    "get_movie_for_mood",
    # Google Books
    "BookRecommendation",
    "GoogleBooksService",
    "create_books_service",
    "get_book_for_mood",
]
