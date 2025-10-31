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
]
