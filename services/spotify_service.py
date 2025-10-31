"""
Spotify music recommendation service using Spotipy library.

Provides mood-based music recommendations from Spotify's catalog.
"""

import asyncio
import logging
from typing import Any

import spotipy
from pydantic import BaseModel, Field
from spotipy.oauth2 import SpotifyClientCredentials

from services.mood_analyzer import MoodAnalysis

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# Pydantic Models
# ============================================================================


class MusicRecommendation(BaseModel):
    """Spotify music recommendation model."""
    
    title: str = Field(..., description="Title of the playlist or track")
    platform: str = Field(default="spotify", description="Platform name (always 'spotify')")
    url: str = Field(..., description="Spotify URL to the playlist or track")
    mood_match: str = Field(..., description="Explanation of how this matches the user's mood")
    duration: str | None = Field(None, description="Playlist duration or track length")
    use_case: str = Field(..., description="When/how to listen to this recommendation")
    artists: list[str] | None = Field(None, description="List of artists (for tracks)")
    image_url: str | None = Field(None, description="Cover art or playlist image URL")
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "title": "Chill Vibes",
                "platform": "spotify",
                "url": "https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6",
                "mood_match": "Perfect for winding down after a stressful day",
                "duration": "2h 30m",
                "use_case": "Evening relaxation or before bed",
                "artists": None,
                "image_url": "https://i.scdn.co/image/ab67616d0000b273..."
            }
        }


# ============================================================================
# Spotify Music Service
# ============================================================================


class SpotifyMusicService:
    """
    Spotify music recommendation service.
    
    Uses Spotipy library to search Spotify's catalog for mood-based
    music recommendations.
    """
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize Spotify service with credentials.
        
        Args:
            client_id: Spotify API client ID
            client_secret: Spotify API client secret
            
        Raises:
            ValueError: If credentials are missing
        """
        if not client_id or not client_secret:
            raise ValueError("Spotify client_id and client_secret are required")
        
        self.client_id = client_id
        self.client_secret = client_secret
        
        # Initialize Spotify client with ClientCredentials auth
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
            logger.info("Spotify client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Spotify client: {e}")
            self.spotify = None
    
    async def get_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation | None:
        """
        Get music recommendation based on mood analysis.
        
        Args:
            mood_analysis: The analyzed mood with preferences
            
        Returns:
            MusicRecommendation object or None if no results found
        """
        if not self.spotify:
            logger.warning("Spotify client not initialized, generating fallback URL")
            return self._generate_fallback_recommendation(mood_analysis)
        
        try:
            # Try playlist search first
            recommendation = await self._search_playlists(mood_analysis)
            
            if recommendation:
                return recommendation
            
            # Fallback to track search
            logger.info("No playlists found, trying track search")
            recommendation = await self._search_tracks(mood_analysis)
            
            if recommendation:
                return recommendation
            
            # Final fallback to search URL
            logger.info("No tracks found, generating search URL")
            return self._generate_fallback_recommendation(mood_analysis)
            
        except Exception as e:
            logger.error(f"Error getting Spotify recommendation: {e}")
            return self._generate_fallback_recommendation(mood_analysis)
    
    async def _search_playlists(
        self,
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation | None:
        """
        Search for playlists matching the mood.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            MusicRecommendation or None
        """
        # Build search query from mood preferences
        search_query = self._build_search_query(mood_analysis)
        
        logger.info(f"Searching playlists with query: {search_query}")
        
        try:
            # Run sync Spotify API call in thread pool
            results = await asyncio.to_thread(
                self.spotify.search,
                q=search_query,
                type="playlist",
                limit=10
            )
            
            playlists = results.get("playlists", {}).get("items", [])
            
            if not playlists:
                logger.info("No playlists found for query")
                return None
            
            # Sort by follower count (popularity)
            playlists.sort(
                key=lambda p: p.get("tracks", {}).get("total", 0),
                reverse=True
            )
            
            # Get the most relevant playlist
            best_playlist = playlists[0]
            
            return self._create_playlist_recommendation(best_playlist, mood_analysis)
            
        except Exception as e:
            logger.error(f"Playlist search failed: {e}")
            return None
    
    async def _search_tracks(
        self,
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation | None:
        """
        Search for tracks matching the mood.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            MusicRecommendation or None
        """
        # Build search query
        search_query = self._build_search_query(mood_analysis, for_tracks=True)
        
        logger.info(f"Searching tracks with query: {search_query}")
        
        try:
            # Run sync Spotify API call in thread pool
            results = await asyncio.to_thread(
                self.spotify.search,
                q=search_query,
                type="track",
                limit=10
            )
            
            tracks = results.get("tracks", {}).get("items", [])
            
            if not tracks:
                logger.info("No tracks found for query")
                return None
            
            # Sort by popularity
            tracks.sort(key=lambda t: t.get("popularity", 0), reverse=True)
            
            # Get the most popular track
            best_track = tracks[0]
            
            return self._create_track_recommendation(best_track, mood_analysis)
            
        except Exception as e:
            logger.error(f"Track search failed: {e}")
            return None
    
    def _build_search_query(
        self,
        mood_analysis: MoodAnalysis,
        for_tracks: bool = False
    ) -> str:
        """
        Build Spotify search query from mood analysis.
        
        Args:
            mood_analysis: The analyzed mood
            for_tracks: Whether this is for track search (vs playlist)
            
        Returns:
            Search query string
        """
        query_parts = []
        
        music_prefs = mood_analysis.music_preferences or {}
        
        # Add genres
        genres = music_prefs.get("preferred_genres", [])
        if genres:
            # Take top 2 genres
            query_parts.extend(genres[:2])
        
        # Add vibe/keywords
        vibe = music_prefs.get("vibe", [])
        keywords = music_prefs.get("keywords", [])
        
        # Combine vibe and keywords
        mood_keywords = (vibe + keywords)[:2]  # Top 2 mood descriptors
        query_parts.extend(mood_keywords)
        
        # Add primary mood if not already covered
        if mood_analysis.primary_mood not in query_parts:
            query_parts.append(mood_analysis.primary_mood)
        
        # Add energy level for tracks
        if for_tracks:
            energy = music_prefs.get("energy_level", "")
            if energy and energy not in query_parts:
                query_parts.append(energy)
        
        # Build query string
        query = " ".join(query_parts[:4])  # Max 4 terms for better results
        
        return query
    
    def _create_playlist_recommendation(
        self,
        playlist: dict[str, Any],
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation:
        """
        Create MusicRecommendation from Spotify playlist.
        
        Args:
            playlist: Spotify playlist data
            mood_analysis: The mood analysis
            
        Returns:
            MusicRecommendation object
        """
        # Extract playlist data
        title = playlist.get("name", "Unknown Playlist")
        url = playlist.get("external_urls", {}).get("spotify", "")
        track_count = playlist.get("tracks", {}).get("total", 0)
        
        # Get image
        images = playlist.get("images", [])
        image_url = images[0].get("url") if images else None
        
        # Estimate duration (rough estimate: 3.5 min per track)
        duration_min = track_count * 3.5
        duration_str = self._format_duration(duration_min)
        
        # Generate mood match explanation
        mood_match = self._generate_mood_match_explanation(
            mood_analysis,
            content_type="playlist",
            title=title
        )
        
        # Generate use case
        use_case = self._generate_use_case(mood_analysis)
        
        return MusicRecommendation(
            title=title,
            platform="spotify",
            url=url,
            mood_match=mood_match,
            duration=duration_str,
            use_case=use_case,
            artists=None,  # Playlists don't have single artists
            image_url=image_url
        )
    
    def _create_track_recommendation(
        self,
        track: dict[str, Any],
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation:
        """
        Create MusicRecommendation from Spotify track.
        
        Args:
            track: Spotify track data
            mood_analysis: The mood analysis
            
        Returns:
            MusicRecommendation object
        """
        # Extract track data
        title = track.get("name", "Unknown Track")
        url = track.get("external_urls", {}).get("spotify", "")
        duration_ms = track.get("duration_ms", 0)
        
        # Get artists
        artists_data = track.get("artists", [])
        artists = [a.get("name", "") for a in artists_data if a.get("name")]
        
        # Get album image
        album = track.get("album", {})
        images = album.get("images", [])
        image_url = images[0].get("url") if images else None
        
        # Format duration
        duration_str = self._format_duration(duration_ms / 60000)  # ms to minutes
        
        # Generate mood match explanation
        mood_match = self._generate_mood_match_explanation(
            mood_analysis,
            content_type="track",
            title=title,
            artists=artists
        )
        
        # Generate use case
        use_case = self._generate_use_case(mood_analysis)
        
        return MusicRecommendation(
            title=title,
            platform="spotify",
            url=url,
            mood_match=mood_match,
            duration=duration_str,
            use_case=use_case,
            artists=artists if artists else None,
            image_url=image_url
        )
    
    def _generate_fallback_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation:
        """
        Generate fallback recommendation with Spotify search URL.
        
        Args:
            mood_analysis: The mood analysis
            
        Returns:
            MusicRecommendation with search URL
        """
        # Build search query
        search_query = self._build_search_query(mood_analysis)
        
        # Create Spotify search URL
        search_url = f"https://open.spotify.com/search/{search_query.replace(' ', '%20')}"
        
        # Generate explanation
        mood_match = self._generate_mood_match_explanation(
            mood_analysis,
            content_type="search",
            title=search_query
        )
        
        use_case = self._generate_use_case(mood_analysis)
        
        return MusicRecommendation(
            title=f"Search: {search_query}",
            platform="spotify",
            url=search_url,
            mood_match=mood_match,
            duration=None,
            use_case=use_case,
            artists=None,
            image_url=None
        )
    
    def _generate_mood_match_explanation(
        self,
        mood_analysis: MoodAnalysis,
        content_type: str,
        title: str,
        artists: list[str] | None = None
    ) -> str:
        """
        Generate explanation of how content matches the mood.
        
        Args:
            mood_analysis: The mood analysis
            content_type: "playlist", "track", or "search"
            title: Content title
            artists: Artist names (for tracks)
            
        Returns:
            Mood match explanation
        """
        mood = mood_analysis.primary_mood.capitalize()
        intensity = mood_analysis.intensity
        immediate_need = mood_analysis.immediate_need
        
        # Build explanation based on immediate need
        if immediate_need == "escape":
            return f"Helps you escape from feeling {mood.lower()} with uplifting and distracting music"
        elif immediate_need == "process":
            return f"Music that resonates with your {mood.lower()} mood, helping you process these feelings"
        elif immediate_need == "uplift":
            return f"Upbeat and energizing tracks to lift you out of feeling {mood.lower()}"
        elif immediate_need == "calm":
            return f"Soothing music to calm your {mood.lower()} state (intensity: {intensity}/10)"
        elif immediate_need == "match":
            return f"Perfect match for your {mood.lower()} mood - amplify what you're feeling"
        elif immediate_need == "channel":
            return f"Channel your {mood.lower()} energy productively with this energetic music"
        else:
            return f"Matches your {mood.lower()} mood and current emotional state"
    
    def _generate_use_case(self, mood_analysis: MoodAnalysis) -> str:
        """
        Generate use case recommendation.
        
        Args:
            mood_analysis: The mood analysis
            
        Returns:
            Use case description
        """
        immediate_need = mood_analysis.immediate_need
        energy = mood_analysis.music_preferences.get("energy_level", "medium")
        
        use_cases = {
            "escape": "When you need a mental break or distraction",
            "process": "During quiet reflection or journaling time",
            "uplift": "Morning routine or workout to boost energy",
            "calm": "Evening wind-down or meditation sessions",
            "match": "Anytime you want to amplify your current mood",
            "channel": "During high-energy activities or workouts"
        }
        
        base_case = use_cases.get(immediate_need, "Anytime you want mood-appropriate music")
        
        # Add energy-based context
        if energy in ["very_high", "high"]:
            base_case += " - great for active listening"
        elif energy in ["very_low", "low"]:
            base_case += " - perfect for background listening"
        
        return base_case
    
    def _format_duration(self, minutes: float) -> str:
        """
        Format duration in minutes to human-readable string.
        
        Args:
            minutes: Duration in minutes
            
        Returns:
            Formatted duration string
        """
        if minutes < 1:
            return f"{int(minutes * 60)}s"
        elif minutes < 60:
            return f"{int(minutes)}m"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            return f"{hours}h {mins}m" if mins > 0 else f"{hours}h"


# ============================================================================
# Convenience Functions
# ============================================================================


def create_spotify_service(client_id: str, client_secret: str) -> SpotifyMusicService:
    """
    Create a SpotifyMusicService instance.
    
    Args:
        client_id: Spotify API client ID
        client_secret: Spotify API client secret
        
    Returns:
        SpotifyMusicService instance
    """
    return SpotifyMusicService(client_id=client_id, client_secret=client_secret)


async def get_music_for_mood(
    mood_analysis: MoodAnalysis,
    client_id: str,
    client_secret: str
) -> MusicRecommendation | None:
    """
    Convenience function to get music recommendation for a mood.
    
    Args:
        mood_analysis: The analyzed mood
        client_id: Spotify API client ID
        client_secret: Spotify API client secret
        
    Returns:
        MusicRecommendation or None
    """
    service = SpotifyMusicService(client_id=client_id, client_secret=client_secret)
    return await service.get_recommendation(mood_analysis)
