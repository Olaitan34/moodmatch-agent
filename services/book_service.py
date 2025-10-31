"""
Google Books recommendation service using httpx library.

Provides mood-based book recommendations from Google Books API.
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


GOOGLE_BOOKS_BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# Average reading speed (pages per hour)
READING_SPEED = 50

# Curated fallback books for different moods
FALLBACK_BOOKS = {
    "happy": {
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "themes": ["hope", "second chances", "happiness"]
    },
    "sad": {
        "title": "The Kite Runner",
        "author": "Khaled Hosseini",
        "themes": ["loss", "redemption", "friendship"]
    },
    "anxious": {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "themes": ["journey", "destiny", "peace"]
    },
    "calm": {
        "title": "Walden",
        "author": "Henry David Thoreau",
        "themes": ["nature", "simplicity", "reflection"]
    },
    "motivated": {
        "title": "Atomic Habits",
        "author": "James Clear",
        "themes": ["growth", "productivity", "success"]
    },
}


# ============================================================================
# Pydantic Models
# ============================================================================


class BookRecommendation(BaseModel):
    """Book recommendation model."""
    
    title: str = Field(..., description="Book title")
    author: str | None = Field(None, description="Book author(s)")
    year: int | None = Field(None, description="Publication year")
    pages: int | None = Field(None, description="Page count")
    rating: float | None = Field(None, description="Average rating (0-5)")
    mood_match: str = Field(..., description="How this matches the user's mood")
    why: str = Field(..., description="Explanation of why this book was recommended")
    themes: list[str] = Field(default_factory=list, description="Book themes")
    reading_time: str = Field(..., description="Estimated reading time")
    urls: dict[str, str] = Field(default_factory=dict, description="Purchase and preview URLs")
    cover_url: str | None = Field(None, description="Book cover image URL")
    description: str | None = Field(None, description="Book description")
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "title": "The Midnight Library",
                "author": "Matt Haig",
                "year": 2020,
                "pages": 304,
                "rating": 4.2,
                "mood_match": "Uplifting story about second chances and finding happiness",
                "why": "This novel explores themes of hope and self-discovery, perfect for your contemplative mood",
                "themes": ["hope", "second chances", "meaning"],
                "reading_time": "6h 5m",
                "urls": {
                    "google_books": "https://books.google.com/books?id=...",
                    "amazon": "https://www.amazon.com/s?k=...",
                    "goodreads": "https://www.goodreads.com/search?q=..."
                },
                "cover_url": "http://books.google.com/books/content?id=...",
                "description": "Between life and death there is a library..."
            }
        }


# ============================================================================
# Google Books Service
# ============================================================================


class GoogleBooksService:
    """
    Google Books recommendation service.
    
    Uses Google Books API to find mood-based book recommendations.
    """
    
    def __init__(self, api_key: str | None = None):
        """
        Initialize Google Books service.
        
        Args:
            api_key: Google Books API key (optional, increases rate limits)
        """
        self.api_key = api_key
        self.base_url = GOOGLE_BOOKS_BASE_URL
        
        # Create httpx client
        self.client = httpx.AsyncClient(timeout=30.0)
        
        logger.info("Google Books service initialized successfully")
    
    async def close(self):
        """Close the httpx client."""
        await self.client.aclose()
    
    async def get_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> BookRecommendation | None:
        """
        Get book recommendation based on mood analysis.
        
        Args:
            mood_analysis: The analyzed mood with preferences
            
        Returns:
            BookRecommendation object or None if no results found
        """
        try:
            # Try specific search first
            recommendation = await self._search_books(mood_analysis)
            
            if recommendation:
                return recommendation
            
            # Fallback to broader search
            logger.info("No books found with specific search, trying broader search")
            recommendation = await self._search_books(mood_analysis, broader=True)
            
            if recommendation:
                return recommendation
            
            # Final fallback to curated books
            logger.info("No API results, using curated fallback")
            return await self._get_fallback_book(mood_analysis)
            
        except Exception as e:
            logger.error(f"Error getting Google Books recommendation: {e}")
            return await self._get_fallback_book(mood_analysis)
    
    async def _search_books(
        self,
        mood_analysis: MoodAnalysis,
        broader: bool = False
    ) -> BookRecommendation | None:
        """
        Search for books using Google Books API.
        
        Args:
            mood_analysis: The analyzed mood
            broader: Whether to use broader search terms
            
        Returns:
            BookRecommendation or None
        """
        # Build search query
        search_query = self._build_search_query(mood_analysis, broader)
        
        if not search_query:
            logger.info("No search query could be built")
            return None
        
        logger.info(f"Searching books with query: {search_query}")
        
        # Build request parameters
        params = {
            "q": search_query,
            "langRestrict": "en",
            "printType": "books",
            "orderBy": "relevance",
            "maxResults": 20,  # Get more results to filter
        }
        
        # Add API key if available
        if self.api_key:
            params["key"] = self.api_key
        
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            
            if not items:
                logger.info("No books found in search")
                return None
            
            # Filter and sort books
            quality_books = self._filter_quality_books(items)
            
            if not quality_books:
                logger.info("No quality books after filtering")
                return None
            
            # Get the best match
            best_book = quality_books[0]
            
            return self._create_recommendation(best_book, mood_analysis)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Google Books API error: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return None
    
    async def _get_fallback_book(
        self,
        mood_analysis: MoodAnalysis
    ) -> BookRecommendation | None:
        """
        Get curated fallback book based on mood.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            BookRecommendation or None
        """
        # Find best fallback book for mood
        primary_mood = mood_analysis.primary_mood.lower()
        
        fallback = FALLBACK_BOOKS.get(
            primary_mood,
            FALLBACK_BOOKS.get("happy")  # Default fallback
        )
        
        if not fallback:
            return None
        
        logger.info(f"Using fallback book: {fallback['title']}")
        
        # Search for the specific fallback book to get real data
        search_query = f"{fallback['title']} {fallback['author']}"
        
        params = {
            "q": search_query,
            "langRestrict": "en",
            "maxResults": 1,
        }
        
        if self.api_key:
            params["key"] = self.api_key
        
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            
            if items:
                return self._create_recommendation(items[0], mood_analysis)
            
        except Exception as e:
            logger.error(f"Fallback book search failed: {e}")
        
        # Create manual fallback if API fails completely
        return self._create_manual_fallback(fallback, mood_analysis)
    
    def _build_search_query(
        self,
        mood_analysis: MoodAnalysis,
        broader: bool = False
    ) -> str:
        """
        Build search query from mood analysis.
        
        Args:
            mood_analysis: The analyzed mood
            broader: Use broader search terms
            
        Returns:
            Search query string
        """
        query_parts = []
        book_prefs = mood_analysis.book_preferences or {}
        
        if broader:
            # Broader search: just use mood and one genre/theme
            query_parts.append(mood_analysis.primary_mood)
            
            genres = book_prefs.get("preferred_genres", [])
            if genres:
                query_parts.append(genres[0])
        else:
            # Specific search: combine genres and themes
            genres = book_prefs.get("preferred_genres", [])
            themes = book_prefs.get("themes", [])
            keywords = book_prefs.get("keywords", [])
            
            # Add top genres
            query_parts.extend(genres[:2])
            
            # Add themes
            query_parts.extend(themes[:2])
            
            # Add keywords if space
            if len(query_parts) < 4:
                query_parts.extend(keywords[:1])
        
        # Build query string
        query = " ".join(query_parts[:4])  # Max 4 terms
        
        return query if query.strip() else mood_analysis.primary_mood
    
    def _filter_quality_books(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Filter books by quality indicators.
        
        Args:
            items: List of book items from API
            
        Returns:
            Filtered and sorted list of quality books
        """
        quality_books = []
        
        for item in items:
            volume_info = item.get("volumeInfo", {})
            
            # Skip if missing critical info
            if not volume_info.get("title"):
                continue
            
            # Skip if no authors
            if not volume_info.get("authors"):
                continue
            
            # Skip if no description
            if not volume_info.get("description"):
                continue
            
            # Prefer books with ratings
            rating = volume_info.get("averageRating")
            ratings_count = volume_info.get("ratingsCount", 0)
            
            # Skip if rated but too low
            if rating and rating < 3.5:
                continue
            
            # Calculate quality score
            quality_score = 0
            
            if rating:
                quality_score += rating * 20  # Max 100 for 5-star rating
            
            if ratings_count:
                quality_score += min(ratings_count / 10, 50)  # Max 50 bonus
            
            # Prefer books with preview
            if volume_info.get("previewLink"):
                quality_score += 10
            
            # Prefer books with page count
            if volume_info.get("pageCount"):
                quality_score += 5
            
            quality_books.append({
                "item": item,
                "score": quality_score
            })
        
        # Sort by quality score
        quality_books.sort(key=lambda x: x["score"], reverse=True)
        
        return [qb["item"] for qb in quality_books]
    
    def _create_recommendation(
        self,
        book_item: dict[str, Any],
        mood_analysis: MoodAnalysis
    ) -> BookRecommendation:
        """
        Create BookRecommendation from Google Books data.
        
        Args:
            book_item: Book item from API
            mood_analysis: The mood analysis
            
        Returns:
            BookRecommendation object
        """
        volume_info = book_item.get("volumeInfo", {})
        
        # Extract basic info
        title = volume_info.get("title", "Unknown Title")
        authors = volume_info.get("authors", [])
        author = authors[0] if authors else None
        
        # Extract year from publishedDate
        published_date = volume_info.get("publishedDate", "")
        year = None
        if published_date:
            try:
                year = int(published_date.split("-")[0])
            except (ValueError, IndexError):
                pass
        
        # Get page count
        pages = volume_info.get("pageCount")
        
        # Get rating
        rating = volume_info.get("averageRating")
        
        # Get description
        description = volume_info.get("description")
        if description and len(description) > 500:
            description = description[:497] + "..."
        
        # Get cover image
        image_links = volume_info.get("imageLinks", {})
        cover_url = image_links.get("thumbnail") or image_links.get("smallThumbnail")
        
        # Calculate reading time
        reading_time = self._calculate_reading_time(pages)
        
        # Extract themes from categories
        categories = volume_info.get("categories", [])
        themes = categories[:3] if categories else []
        
        # Add mood-based themes if empty
        if not themes:
            book_prefs = mood_analysis.book_preferences or {}
            themes = book_prefs.get("themes", [])[:3]
        
        # Generate URLs
        urls = self._generate_urls(
            title=title,
            author=author,
            google_link=volume_info.get("canonicalVolumeLink"),
            preview_link=volume_info.get("previewLink")
        )
        
        # Generate mood match and explanation
        mood_match = self._generate_mood_match(mood_analysis, title, themes)
        why = self._generate_explanation(mood_analysis, title, themes, description)
        
        return BookRecommendation(
            title=title,
            author=author,
            year=year,
            pages=pages,
            rating=rating,
            mood_match=mood_match,
            why=why,
            themes=themes,
            reading_time=reading_time,
            urls=urls,
            cover_url=cover_url,
            description=description
        )
    
    def _create_manual_fallback(
        self,
        fallback: dict[str, Any],
        mood_analysis: MoodAnalysis
    ) -> BookRecommendation:
        """
        Create manual fallback recommendation when API completely fails.
        
        Args:
            fallback: Fallback book data
            mood_analysis: The mood analysis
            
        Returns:
            BookRecommendation object
        """
        title = fallback["title"]
        author = fallback["author"]
        themes = fallback["themes"]
        
        # Generate URLs
        urls = self._generate_urls(title=title, author=author)
        
        # Generate mood match and explanation
        mood_match = self._generate_mood_match(mood_analysis, title, themes)
        why = self._generate_explanation(mood_analysis, title, themes, None)
        
        return BookRecommendation(
            title=title,
            author=author,
            year=None,
            pages=None,
            rating=None,
            mood_match=mood_match,
            why=why,
            themes=themes,
            reading_time="Unknown",
            urls=urls,
            cover_url=None,
            description=None
        )
    
    def _calculate_reading_time(self, pages: int | None) -> str:
        """
        Calculate estimated reading time.
        
        Args:
            pages: Number of pages
            
        Returns:
            Formatted reading time string
        """
        if not pages:
            return "Unknown"
        
        # Calculate hours based on reading speed
        hours = pages / READING_SPEED
        
        if hours < 1:
            minutes = int(hours * 60)
            return f"{minutes}m"
        
        hours_int = int(hours)
        minutes = int((hours - hours_int) * 60)
        
        if minutes > 0:
            return f"{hours_int}h {minutes}m"
        return f"{hours_int}h"
    
    def _generate_urls(
        self,
        title: str,
        author: str | None = None,
        google_link: str | None = None,
        preview_link: str | None = None
    ) -> dict[str, str]:
        """
        Generate purchase and preview URLs.
        
        Args:
            title: Book title
            author: Book author
            google_link: Canonical Google Books link
            preview_link: Preview link
            
        Returns:
            Dictionary of URLs
        """
        urls = {}
        
        # Google Books link
        if google_link:
            urls["google_books"] = google_link
        elif preview_link:
            urls["google_books"] = preview_link
        else:
            # Fallback search URL
            search_query = quote(f"{title} {author or ''}")
            urls["google_books"] = f"https://books.google.com/books?q={search_query}"
        
        # Amazon link
        amazon_query = quote(f"{title} {author or ''}")
        urls["amazon"] = f"https://www.amazon.com/s?k={amazon_query}&i=stripbooks"
        
        # Goodreads link
        goodreads_query = quote(f"{title} {author or ''}")
        urls["goodreads"] = f"https://www.goodreads.com/search?q={goodreads_query}"
        
        # Add preview if available
        if preview_link and preview_link != google_link:
            urls["preview"] = preview_link
        
        return urls
    
    def _generate_mood_match(
        self,
        mood_analysis: MoodAnalysis,
        title: str,
        themes: list[str]
    ) -> str:
        """
        Generate mood match explanation.
        
        Args:
            mood_analysis: The mood analysis
            title: Book title
            themes: Book themes
            
        Returns:
            Mood match explanation
        """
        mood = mood_analysis.primary_mood.capitalize()
        immediate_need = mood_analysis.immediate_need
        book_prefs = mood_analysis.book_preferences or {}
        pacing = book_prefs.get("pacing", "moderate")
        
        theme_str = " and ".join(themes[:2]) if themes else "compelling story"
        
        if immediate_need == "escape":
            return f"An immersive {pacing}-paced read to escape your {mood.lower()} state"
        elif immediate_need == "process":
            return f"A thoughtful exploration of {theme_str}, perfect for processing your {mood.lower()} mood"
        elif immediate_need == "uplift":
            return f"An uplifting story to lift you from feeling {mood.lower()}"
        elif immediate_need == "calm":
            return f"A {pacing}-paced book to calm your {mood.lower()} mind"
        elif immediate_need == "match":
            return f"Resonates perfectly with your {mood.lower()} mood through themes of {theme_str}"
        elif immediate_need == "channel":
            return f"An engaging read to productively channel your {mood.lower()} energy"
        else:
            return f"A meaningful read that matches your {mood.lower()} state"
    
    def _generate_explanation(
        self,
        mood_analysis: MoodAnalysis,
        title: str,
        themes: list[str],
        description: str | None
    ) -> str:
        """
        Generate detailed explanation of recommendation.
        
        Args:
            mood_analysis: The mood analysis
            title: Book title
            themes: Book themes
            description: Book description
            
        Returns:
            Detailed explanation
        """
        book_prefs = mood_analysis.book_preferences or {}
        depth = book_prefs.get("depth", "moderate")
        pacing = book_prefs.get("pacing", "moderate")
        preferred_genres = book_prefs.get("preferred_genres", [])
        
        parts = []
        
        # Genre context
        if preferred_genres:
            genre_str = preferred_genres[0]
            parts.append(f"This {genre_str} book")
        else:
            parts.append("This book")
        
        # Themes
        if themes:
            theme_str = ", ".join(themes[:2])
            parts.append(f"explores {theme_str}")
        
        # Depth and pacing
        parts.append(f"with {depth} depth and {pacing} pacing")
        
        # Mood connection
        immediate_need = mood_analysis.immediate_need
        if immediate_need == "process":
            parts.append("offering space for reflection and emotional processing")
        elif immediate_need == "escape":
            parts.append("providing an engaging escape from current feelings")
        elif immediate_need == "uplift":
            parts.append("designed to inspire and elevate your mood")
        elif immediate_need == "calm":
            parts.append("creating a calming reading experience")
        
        explanation = ", ".join(parts) + "."
        
        return explanation


# ============================================================================
# Convenience Functions
# ============================================================================


def create_books_service(api_key: str | None = None) -> GoogleBooksService:
    """
    Create a GoogleBooksService instance.
    
    Args:
        api_key: Google Books API key (optional)
        
    Returns:
        GoogleBooksService instance
    """
    return GoogleBooksService(api_key=api_key)


async def get_book_for_mood(
    mood_analysis: MoodAnalysis,
    api_key: str | None = None
) -> BookRecommendation | None:
    """
    Convenience function to get book recommendation for a mood.
    
    Args:
        mood_analysis: The analyzed mood
        api_key: Google Books API key (optional)
        
    Returns:
        BookRecommendation or None
    """
    service = GoogleBooksService(api_key=api_key)
    try:
        return await service.get_recommendation(mood_analysis)
    finally:
        await service.close()
