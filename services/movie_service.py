"""
TMDB movie recommendation service using httpx library.

Provides mood-based movie recommendations from The Movie Database (TMDB).
"""

import logging
from typing import Any
from urllib.parse import quote

import httpx
from pydantic import BaseModel, Field

from services.mood_analyzer import MoodAnalysis

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# Constants
# ============================================================================


TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# TMDB Genre ID mapping
GENRE_IDS = {
    "comedy": 35,
    "drama": 18,
    "action": 28,
    "romance": 10749,
    "thriller": 53,
    "horror": 27,
    "sci-fi": 878,
    "science fiction": 878,
    "fantasy": 14,
    "animation": 16,
    "documentary": 99,
    "mystery": 9648,
    "crime": 80,
    "adventure": 12,
    "family": 10751,
    "war": 10752,
    "western": 37,
    "music": 10402,
    "history": 36,
}

# Streaming platform search URLs
PLATFORM_SEARCH_URLS = {
    "netflix": "https://www.netflix.com/search?q={}",
    "prime video": "https://www.amazon.com/s?k={}&i=prime-video",
    "amazon prime": "https://www.amazon.com/s?k={}&i=prime-video",
    "disney+": "https://www.disneyplus.com/search?q={}",
    "disney plus": "https://www.disneyplus.com/search?q={}",
    "hulu": "https://www.hulu.com/search?q={}",
    "hbo max": "https://play.max.com/search?q={}",
    "apple tv+": "https://tv.apple.com/search?term={}",
    "paramount+": "https://www.paramountplus.com/search/?query={}",
}


# ============================================================================
# Pydantic Models
# ============================================================================


class MovieRecommendation(BaseModel):
    """Movie recommendation model."""
    
    title: str = Field(..., description="Movie title")
    year: int | None = Field(None, description="Release year")
    rating: float | None = Field(None, description="TMDB rating (0-10)")
    runtime: str | None = Field(None, description="Movie runtime in human-readable format")
    mood_match: str = Field(..., description="How this matches the user's mood")
    why: str = Field(..., description="Explanation of why this movie was recommended")
    genres: list[str] = Field(default_factory=list, description="Movie genres")
    platforms: list[str] = Field(default_factory=list, description="Suggested streaming platforms")
    url: str = Field(..., description="Universal search URL or TMDB URL")
    poster_url: str | None = Field(None, description="Movie poster image URL")
    overview: str | None = Field(None, description="Movie overview/synopsis")
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "title": "The Shawshank Redemption",
                "year": 1994,
                "rating": 8.7,
                "runtime": "2h 22m",
                "mood_match": "Uplifting and hopeful, perfect for processing difficult emotions",
                "why": "This powerful drama explores themes of hope and redemption, matching your need to process feelings",
                "genres": ["Drama", "Crime"],
                "platforms": ["Netflix", "Prime Video"],
                "url": "https://www.themoviedb.org/movie/278",
                "poster_url": "https://image.tmdb.org/t/p/w500/q6y0Go1ts...",
                "overview": "Framed in the 1940s for the double murder..."
            }
        }


# ============================================================================
# TMDB Movie Service
# ============================================================================


class TMDBMovieService:
    """
    TMDB movie recommendation service.
    
    Uses The Movie Database API to find mood-based movie recommendations.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize TMDB service with API key.
        
        Args:
            api_key: TMDB API key
            
        Raises:
            ValueError: If API key is missing
        """
        if not api_key:
            raise ValueError("TMDB API key is required")
        
        self.api_key = api_key
        self.base_url = TMDB_BASE_URL
        self.image_base_url = TMDB_IMAGE_BASE_URL
        
        # Create httpx client with default params
        self.client = httpx.AsyncClient(
            timeout=30.0,
            params={"api_key": api_key}
        )
        
        logger.info("TMDB service initialized successfully")
    
    async def close(self):
        """Close the httpx client."""
        await self.client.aclose()
    
    async def get_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> MovieRecommendation | None:
        """
        Get movie recommendation based on mood analysis.
        
        Args:
            mood_analysis: The analyzed mood with preferences
            
        Returns:
            MovieRecommendation object or None if no results found
        """
        try:
            # Try discover endpoint first (better for genre-based search)
            recommendation = await self._discover_movies(mood_analysis)
            
            if recommendation:
                return recommendation
            
            # Fallback to keyword search
            logger.info("No movies found via discover, trying search")
            recommendation = await self._search_movies(mood_analysis)
            
            if recommendation:
                return recommendation
            
            # Final fallback to top-rated movies
            logger.info("No keyword matches, falling back to top-rated")
            recommendation = await self._get_top_rated(mood_analysis)
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error getting TMDB recommendation: {e}")
            return None
    
    async def _discover_movies(
        self,
        mood_analysis: MoodAnalysis
    ) -> MovieRecommendation | None:
        """
        Discover movies using genre-based filtering.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            MovieRecommendation or None
        """
        # Get genre IDs from mood preferences
        genre_ids = self._get_genre_ids(mood_analysis)
        
        if not genre_ids:
            logger.info("No genre IDs matched, skipping discover")
            return None
        
        # Determine sort order based on mood
        sort_by = self._get_sort_order(mood_analysis)
        
        # Build discover query
        params = {
            "with_genres": ",".join(map(str, genre_ids[:3])),  # Max 3 genres
            "sort_by": sort_by,
            "vote_average.gte": 7.0,  # Minimum rating
            "vote_count.gte": 1000,  # Minimum votes for reliability
            "include_adult": "false",
            "language": "en-US",
            "page": 1
        }
        
        logger.info(f"Discovering movies with genres: {genre_ids[:3]}")
        
        try:
            response = await self.client.get(
                f"{self.base_url}/discover/movie",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            movies = data.get("results", [])
            
            if not movies:
                logger.info("No movies found in discover")
                return None
            
            # Get the best match
            best_movie = movies[0]
            
            # Get additional details
            movie_details = await self._get_movie_details(best_movie["id"])
            
            return self._create_recommendation(
                movie_data=best_movie,
                movie_details=movie_details,
                mood_analysis=mood_analysis
            )
            
        except httpx.HTTPStatusError as e:
            logger.error(f"TMDB API error in discover: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Discover failed: {e}")
            return None
    
    async def _search_movies(
        self,
        mood_analysis: MoodAnalysis
    ) -> MovieRecommendation | None:
        """
        Search movies by keywords from mood.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            MovieRecommendation or None
        """
        # Build search query from mood
        search_query = self._build_search_query(mood_analysis)
        
        if not search_query:
            logger.info("No search query could be built")
            return None
        
        logger.info(f"Searching movies with query: {search_query}")
        
        try:
            response = await self.client.get(
                f"{self.base_url}/search/movie",
                params={
                    "query": search_query,
                    "include_adult": "false",
                    "language": "en-US",
                    "page": 1
                }
            )
            response.raise_for_status()
            data = response.json()
            
            movies = data.get("results", [])
            
            if not movies:
                logger.info("No movies found in search")
                return None
            
            # Filter by rating and votes
            quality_movies = [
                m for m in movies
                if m.get("vote_average", 0) >= 6.5
                and m.get("vote_count", 0) >= 500
            ]
            
            if not quality_movies:
                quality_movies = movies  # Use unfiltered if no quality matches
            
            # Sort by popularity and rating
            quality_movies.sort(
                key=lambda m: (m.get("popularity", 0) * m.get("vote_average", 0)),
                reverse=True
            )
            
            best_movie = quality_movies[0]
            
            # Get additional details
            movie_details = await self._get_movie_details(best_movie["id"])
            
            return self._create_recommendation(
                movie_data=best_movie,
                movie_details=movie_details,
                mood_analysis=mood_analysis
            )
            
        except httpx.HTTPStatusError as e:
            logger.error(f"TMDB API error in search: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return None
    
    async def _get_top_rated(
        self,
        mood_analysis: MoodAnalysis
    ) -> MovieRecommendation | None:
        """
        Get top-rated movies as fallback.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            MovieRecommendation or None
        """
        logger.info("Fetching top-rated movies as fallback")
        
        try:
            response = await self.client.get(
                f"{self.base_url}/movie/top_rated",
                params={
                    "language": "en-US",
                    "page": 1
                }
            )
            response.raise_for_status()
            data = response.json()
            
            movies = data.get("results", [])
            
            if not movies:
                logger.error("No top-rated movies found")
                return None
            
            # Pick a movie based on mood tone
            movie_index = self._select_by_mood_tone(mood_analysis, len(movies))
            best_movie = movies[movie_index]
            
            # Get additional details
            movie_details = await self._get_movie_details(best_movie["id"])
            
            return self._create_recommendation(
                movie_data=best_movie,
                movie_details=movie_details,
                mood_analysis=mood_analysis
            )
            
        except Exception as e:
            logger.error(f"Failed to get top-rated movies: {e}")
            return None
    
    async def _get_movie_details(self, movie_id: int) -> dict[str, Any] | None:
        """
        Get detailed movie information.
        
        Args:
            movie_id: TMDB movie ID
            
        Returns:
            Movie details dict or None
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/movie/{movie_id}",
                params={"language": "en-US"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get movie details: {e}")
            return None
    
    def _get_genre_ids(self, mood_analysis: MoodAnalysis) -> list[int]:
        """
        Get TMDB genre IDs from mood analysis.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            List of genre IDs
        """
        genre_ids = []
        movie_prefs = mood_analysis.movie_preferences or {}
        
        # Get preferred genres from mood
        preferred_genres = movie_prefs.get("preferred_genres", [])
        
        for genre in preferred_genres:
            genre_lower = genre.lower()
            if genre_lower in GENRE_IDS:
                genre_ids.append(GENRE_IDS[genre_lower])
        
        # Add genres based on mood tone if needed
        if not genre_ids:
            tone = movie_prefs.get("tone", "").lower()
            if "light" in tone or "funny" in tone:
                genre_ids.append(GENRE_IDS["comedy"])
            elif "serious" in tone or "dark" in tone:
                genre_ids.append(GENRE_IDS["drama"])
            elif "intense" in tone:
                genre_ids.append(GENRE_IDS["thriller"])
        
        return genre_ids
    
    def _get_sort_order(self, mood_analysis: MoodAnalysis) -> str:
        """
        Determine sort order based on mood.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            Sort order string
        """
        immediate_need = mood_analysis.immediate_need
        intensity = mood_analysis.intensity
        
        # High intensity or escape -> popular/exciting movies
        if intensity >= 7 or immediate_need in ["escape", "channel"]:
            return "popularity.desc"
        
        # Process or calm -> highly rated/quality
        if immediate_need in ["process", "calm"]:
            return "vote_average.desc"
        
        # Default to balanced
        return "popularity.desc"
    
    def _build_search_query(self, mood_analysis: MoodAnalysis) -> str:
        """
        Build search query from mood analysis.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            Search query string
        """
        query_parts = []
        movie_prefs = mood_analysis.movie_preferences or {}
        
        # Add keywords
        keywords = movie_prefs.get("keywords", [])
        query_parts.extend(keywords[:2])
        
        # Add themes
        themes = movie_prefs.get("themes", [])
        query_parts.extend(themes[:2])
        
        # Add mood if not covered
        if mood_analysis.primary_mood not in query_parts:
            query_parts.append(mood_analysis.primary_mood)
        
        return " ".join(query_parts[:3])  # Max 3 terms
    
    def _select_by_mood_tone(self, mood_analysis: MoodAnalysis, max_index: int) -> int:
        """
        Select movie index based on mood tone.
        
        Args:
            mood_analysis: The analyzed mood
            max_index: Maximum index available
            
        Returns:
            Selected index
        """
        # Use intensity to vary selection
        intensity = mood_analysis.intensity
        
        # Map intensity to index (0-10 -> 0-max_index)
        index = min(int((intensity / 10) * max_index), max_index - 1)
        
        return max(0, index)
    
    def _create_recommendation(
        self,
        movie_data: dict[str, Any],
        movie_details: dict[str, Any] | None,
        mood_analysis: MoodAnalysis
    ) -> MovieRecommendation:
        """
        Create MovieRecommendation from TMDB data.
        
        Args:
            movie_data: Basic movie data from search/discover
            movie_details: Detailed movie information
            mood_analysis: The mood analysis
            
        Returns:
            MovieRecommendation object
        """
        # Extract basic info
        title = movie_data.get("title", "Unknown Movie")
        movie_id = movie_data.get("id")
        
        # Extract year from release date
        release_date = movie_data.get("release_date", "")
        year = int(release_date[:4]) if release_date else None
        
        # Get rating
        rating = movie_data.get("vote_average")
        if rating:
            rating = round(rating, 1)
        
        # Get runtime from details
        runtime = None
        if movie_details:
            runtime_minutes = movie_details.get("runtime")
            if runtime_minutes:
                runtime = self._format_runtime(runtime_minutes)
        
        # Get genres
        genres = []
        if movie_details:
            genre_data = movie_details.get("genres", [])
            genres = [g["name"] for g in genre_data]
        else:
            # Fallback to genre IDs from basic data
            genre_ids = movie_data.get("genre_ids", [])
            id_to_name = {v: k.title() for k, v in GENRE_IDS.items()}
            genres = [id_to_name.get(gid, "") for gid in genre_ids if gid in id_to_name]
        
        # Get poster
        poster_path = movie_data.get("poster_path")
        poster_url = f"{self.image_base_url}{poster_path}" if poster_path else None
        
        # Get overview
        overview = movie_data.get("overview")
        
        # Generate mood match and explanation
        mood_match = self._generate_mood_match(mood_analysis, title, genres)
        why = self._generate_explanation(mood_analysis, title, genres, overview)
        
        # Get platform suggestions
        platforms = self._suggest_platforms(mood_analysis)
        
        # Create URL (TMDB or platform search)
        url = f"https://www.themoviedb.org/movie/{movie_id}"
        if platforms:
            # Use first platform's search URL
            platform_key = platforms[0].lower()
            if platform_key in PLATFORM_SEARCH_URLS:
                url = PLATFORM_SEARCH_URLS[platform_key].format(quote(title))
        
        return MovieRecommendation(
            title=title,
            year=year,
            rating=rating,
            runtime=runtime,
            mood_match=mood_match,
            why=why,
            genres=genres,
            platforms=platforms,
            url=url,
            poster_url=poster_url,
            overview=overview
        )
    
    def _format_runtime(self, minutes: int) -> str:
        """
        Format runtime in minutes to human-readable string.
        
        Args:
            minutes: Runtime in minutes
            
        Returns:
            Formatted runtime string
        """
        if minutes < 60:
            return f"{minutes}m"
        
        hours = minutes // 60
        mins = minutes % 60
        
        if mins > 0:
            return f"{hours}h {mins}m"
        return f"{hours}h"
    
    def _generate_mood_match(
        self,
        mood_analysis: MoodAnalysis,
        title: str,
        genres: list[str]
    ) -> str:
        """
        Generate mood match explanation.
        
        Args:
            mood_analysis: The mood analysis
            title: Movie title
            genres: Movie genres
            
        Returns:
            Mood match explanation
        """
        mood = mood_analysis.primary_mood.capitalize()
        immediate_need = mood_analysis.immediate_need
        intensity = mood_analysis.intensity
        
        genre_str = ", ".join(genres[:2]) if genres else "movie"
        
        if immediate_need == "escape":
            return f"An engaging {genre_str} to help you escape feeling {mood.lower()}"
        elif immediate_need == "process":
            return f"A thoughtful {genre_str} that resonates with your {mood.lower()} mood"
        elif immediate_need == "uplift":
            return f"An uplifting {genre_str} to lift your spirits from feeling {mood.lower()}"
        elif immediate_need == "calm":
            return f"A calming {genre_str} to soothe your {mood.lower()} state (intensity: {intensity}/10)"
        elif immediate_need == "match":
            return f"Perfect {genre_str} match for your {mood.lower()} mood"
        elif immediate_need == "channel":
            return f"An intense {genre_str} to channel your {mood.lower()} energy"
        else:
            return f"A {genre_str} that fits your current {mood.lower()} mood"
    
    def _generate_explanation(
        self,
        mood_analysis: MoodAnalysis,
        title: str,
        genres: list[str],
        overview: str | None
    ) -> str:
        """
        Generate detailed explanation of recommendation.
        
        Args:
            mood_analysis: The mood analysis
            title: Movie title
            genres: Movie genres
            overview: Movie overview
            
        Returns:
            Detailed explanation
        """
        movie_prefs = mood_analysis.movie_preferences or {}
        themes = movie_prefs.get("themes", [])
        tone = movie_prefs.get("tone", "balanced")
        
        parts = []
        
        # Genre match
        if genres:
            parts.append(f"This {', '.join(genres[:2]).lower()} film")
        else:
            parts.append("This movie")
        
        # Theme match
        if themes:
            theme_str = " and ".join(themes[:2])
            parts.append(f"explores {theme_str}")
        
        # Tone match
        if tone:
            parts.append(f"with a {tone} tone")
        
        # Mood connection
        immediate_need = mood_analysis.immediate_need
        if immediate_need == "process":
            parts.append("helping you process your emotions")
        elif immediate_need == "escape":
            parts.append("providing an immersive escape")
        elif immediate_need == "uplift":
            parts.append("designed to uplift and inspire")
        
        explanation = ", ".join(parts) + "."
        
        return explanation
    
    def _suggest_platforms(self, mood_analysis: MoodAnalysis) -> list[str]:
        """
        Suggest streaming platforms based on mood.
        
        Args:
            mood_analysis: The mood analysis
            
        Returns:
            List of suggested platform names
        """
        # Default platform suggestions
        # In production, this could be user-specific or region-specific
        platforms = ["Netflix", "Prime Video", "Disney+"]
        
        # Adjust based on mood (example logic)
        movie_prefs = mood_analysis.movie_preferences or {}
        genres = movie_prefs.get("preferred_genres", [])
        
        if "animation" in [g.lower() for g in genres]:
            platforms = ["Disney+", "Netflix", "Prime Video"]
        elif "documentary" in [g.lower() for g in genres]:
            platforms = ["Netflix", "Prime Video", "HBO Max"]
        
        return platforms[:2]  # Return top 2 platforms


# ============================================================================
# Convenience Functions
# ============================================================================


def create_movie_service(api_key: str) -> TMDBMovieService:
    """
    Create a TMDBMovieService instance.
    
    Args:
        api_key: TMDB API key
        
    Returns:
        TMDBMovieService instance
    """
    return TMDBMovieService(api_key=api_key)


async def get_movie_for_mood(
    mood_analysis: MoodAnalysis,
    api_key: str
) -> MovieRecommendation | None:
    """
    Convenience function to get movie recommendation for a mood.
    
    Args:
        mood_analysis: The analyzed mood
        api_key: TMDB API key
        
    Returns:
        MovieRecommendation or None
    """
    service = TMDBMovieService(api_key=api_key)
    try:
        return await service.get_recommendation(mood_analysis)
    finally:
        await service.close()
