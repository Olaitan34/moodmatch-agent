"""
MoodMatch Agent - Main orchestrator for mood analysis and media recommendations.

Integrates mood analysis with music, movie, and book recommendation services,
implementing the A2A protocol for agent-to-agent communication.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from models.a2a import (
    A2AMessage,
    Artifact,
    MessageConfiguration,
    MessagePart,
    TaskResult,
    TaskStatus,
)
from services.mood_analyzer import MoodAnalysis, MoodAnalyzer
from services.spotify_service import MusicRecommendation, SpotifyMusicService
from services.movie_service import MovieRecommendation, TMDBMovieService
from services.book_service import BookRecommendation, GoogleBooksService

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# Pydantic Models
# ============================================================================


class UnifiedRecommendation(BaseModel):
    """Unified recommendation containing all media types."""
    
    mood_analysis: MoodAnalysis = Field(..., description="The analyzed mood")
    music: MusicRecommendation | None = Field(None, description="Music recommendation")
    movie: MovieRecommendation | None = Field(None, description="Movie recommendation")
    book: BookRecommendation | None = Field(None, description="Book recommendation")
    summary: str = Field(..., description="Overall recommendation summary")
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "mood_analysis": {"primary_mood": "happy", "intensity": 8},
                "music": {"title": "Happy Hits", "platform": "spotify"},
                "movie": {"title": "The Grand Budapest Hotel", "year": 2014},
                "book": {"title": "The Midnight Library", "author": "Matt Haig"},
                "summary": "Uplifting recommendations to match your happy mood"
            }
        }


# ============================================================================
# MoodMatch Agent
# ============================================================================


class MoodMatchAgent:
    """
    Main MoodMatch agent orchestrating mood analysis and media recommendations.
    
    Implements the A2A protocol for processing user messages and returning
    personalized music, movie, and book recommendations based on mood analysis.
    """
    
    def __init__(
        self,
        gemini_api_key: str,
        tmdb_api_key: str,
        spotify_client_id: str,
        spotify_client_secret: str,
        google_books_api_key: str | None = None
    ):
        """
        Initialize MoodMatch agent with all service credentials.
        
        Args:
            gemini_api_key: Google Gemini API key for mood analysis
            tmdb_api_key: TMDB API key for movie recommendations
            spotify_client_id: Spotify API client ID
            spotify_client_secret: Spotify API client secret
            google_books_api_key: Google Books API key (optional)
            
        Raises:
            ValueError: If required credentials are missing
        """
        # Validate required credentials
        if not gemini_api_key:
            raise ValueError("Gemini API key is required")
        if not tmdb_api_key:
            raise ValueError("TMDB API key is required")
        if not spotify_client_id or not spotify_client_secret:
            raise ValueError("Spotify credentials are required")
        
        # Initialize mood analyzer
        try:
            self.mood_analyzer = MoodAnalyzer(api_key=gemini_api_key)
            logger.info("MoodAnalyzer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize MoodAnalyzer: {e}")
            raise
        
        # Initialize music service
        try:
            self.music_service = SpotifyMusicService(
                client_id=spotify_client_id,
                client_secret=spotify_client_secret
            )
            logger.info("Spotify music service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Spotify service: {e}")
            raise
        
        # Initialize movie service
        try:
            self.movie_service = TMDBMovieService(api_key=tmdb_api_key)
            logger.info("TMDB movie service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize TMDB service: {e}")
            raise
        
        # Initialize book service
        try:
            self.book_service = GoogleBooksService(api_key=google_books_api_key)
            logger.info("Google Books service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Google Books service: {e}")
            raise
        
        # Context storage (in-memory for now)
        self.contexts: dict[str, list[A2AMessage]] = {}
        
        logger.info("MoodMatch agent fully initialized")
    
    async def close(self):
        """Close all service clients."""
        tasks = []
        
        if self.movie_service:
            tasks.append(self.movie_service.close())
        
        if self.book_service:
            tasks.append(self.book_service.close())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info("All services closed")
    
    async def process_messages(
        self,
        messages: list[A2AMessage],
        context_id: str | None = None,
        task_id: str | None = None,
        config: MessageConfiguration | None = None
    ) -> TaskResult:
        """
        Process user messages and return mood-based recommendations.
        
        This is the main entry point for the A2A protocol, handling message
        processing, mood analysis, and recommendation generation.
        
        Args:
            messages: List of A2A messages from the conversation
            context_id: Optional context ID for conversation tracking
            task_id: Optional task ID for this interaction
            config: Optional message configuration
            
        Returns:
            TaskResult with recommendations or error
        """
        # Generate IDs if not provided
        if not context_id:
            context_id = str(uuid4())
        if not task_id:
            task_id = str(uuid4())
        
        logger.info(f"Processing task {task_id} in context {context_id}")
        
        try:
            # Extract user message text
            user_message_text = self._extract_user_message(messages)
            
            if not user_message_text:
                return self._create_error_result(
                    context_id=context_id,
                    task_id=task_id,
                    message="No user message found to process"
                )
            
            logger.info(f"User message: {user_message_text[:100]}...")
            
            # Step 1: Analyze mood
            try:
                mood_analysis = await self.mood_analyzer.analyze_mood(user_message_text)
                logger.info(f"Mood analyzed: {mood_analysis.primary_mood} (intensity: {mood_analysis.intensity})")
            except Exception as e:
                logger.error(f"Mood analysis failed: {e}")
                return self._create_error_result(
                    context_id=context_id,
                    task_id=task_id,
                    message=f"Failed to analyze mood: {str(e)}"
                )
            
            # Step 2: Get recommendations in parallel
            music_task = self._get_music_safe(mood_analysis)
            movie_task = self._get_movie_safe(mood_analysis)
            book_task = self._get_book_safe(mood_analysis)
            
            music, movie, book = await asyncio.gather(
                music_task,
                movie_task,
                book_task,
                return_exceptions=True
            )
            
            # Handle exceptions from gather
            music = music if not isinstance(music, Exception) else None
            movie = movie if not isinstance(movie, Exception) else None
            book = book if not isinstance(book, Exception) else None
            
            # Log results
            logger.info(f"Recommendations: Music={'✓' if music else '✗'}, Movie={'✓' if movie else '✗'}, Book={'✓' if book else '✗'}")
            
            # Check if we got any recommendations
            if not any([music, movie, book]):
                return self._create_error_result(
                    context_id=context_id,
                    task_id=task_id,
                    message="Unable to generate recommendations at this time. Please try again."
                )
            
            # Step 3: Build response
            response_message = self._build_response_message(
                mood_analysis=mood_analysis,
                music=music,
                movie=movie,
                book=book,
                context_id=context_id,
                task_id=task_id
            )
            
            # Step 4: Create artifacts
            artifacts = self._create_artifacts(
                mood_analysis=mood_analysis,
                music=music,
                movie=movie,
                book=book
            )
            
            # Step 5: Build conversation history
            history = self._build_history(messages, response_message)
            
            # Store context
            self.contexts[context_id] = history
            
            # Step 6: Create successful task result
            return TaskResult(
                taskId=task_id,
                contextId=context_id,
                status=TaskStatus(
                    state="completed",
                    timestamp=datetime.utcnow(),
                    message="Recommendations generated successfully"
                ),
                artifacts=artifacts,
                history=history
            )
            
        except Exception as e:
            logger.error(f"Unexpected error in process_messages: {e}", exc_info=True)
            return self._create_error_result(
                context_id=context_id,
                task_id=task_id,
                message=f"An unexpected error occurred: {str(e)}"
            )
    
    def _extract_user_message(self, messages: list[A2AMessage]) -> str:
        """
        Extract user message text from A2A messages.
        
        Args:
            messages: List of A2A messages
            
        Returns:
            Concatenated user message text
        """
        text_parts = []
        
        for message in messages:
            if message.role == "user":
                for part in message.parts:
                    if part.kind == "text" and part.text:
                        text_parts.append(part.text)
        
        return " ".join(text_parts)
    
    async def _get_music_safe(self, mood_analysis: MoodAnalysis) -> MusicRecommendation | None:
        """Safely get music recommendation with error handling."""
        try:
            return await self.music_service.get_recommendation(mood_analysis)
        except Exception as e:
            logger.error(f"Music recommendation failed: {e}")
            return None
    
    async def _get_movie_safe(self, mood_analysis: MoodAnalysis) -> MovieRecommendation | None:
        """Safely get movie recommendation with error handling."""
        try:
            return await self.movie_service.get_recommendation(mood_analysis)
        except Exception as e:
            logger.error(f"Movie recommendation failed: {e}")
            return None
    
    async def _get_book_safe(self, mood_analysis: MoodAnalysis) -> BookRecommendation | None:
        """Safely get book recommendation with error handling."""
        try:
            return await self.book_service.get_recommendation(mood_analysis)
        except Exception as e:
            logger.error(f"Book recommendation failed: {e}")
            return None
    
    def _build_response_message(
        self,
        mood_analysis: MoodAnalysis,
        music: MusicRecommendation | None,
        movie: MovieRecommendation | None,
        book: BookRecommendation | None,
        context_id: str,
        task_id: str
    ) -> A2AMessage:
        """
        Build friendly response message with recommendations.
        
        Args:
            mood_analysis: The analyzed mood
            music: Music recommendation
            movie: Movie recommendation
            book: Book recommendation
            context_id: Context ID
            task_id: Task ID
            
        Returns:
            A2AMessage with formatted response
        """
        # Build empathetic opening
        mood = mood_analysis.primary_mood.capitalize()
        intensity = mood_analysis.intensity
        
        response_parts = []
        
        # Opening
        if intensity >= 7:
            response_parts.append(f"I can sense you're feeling quite {mood.lower()} right now.")
        else:
            response_parts.append(f"I understand you're feeling {mood.lower()}.")
        
        # Immediate need context
        need_phrases = {
            "escape": "Let me help you find some great ways to escape and shift your perspective.",
            "process": "Here are some thoughtful recommendations to help you process these feelings.",
            "uplift": "I've found some uplifting options to help improve your mood.",
            "calm": "These recommendations should help you find some calm and peace.",
            "match": "Here are some perfect matches for your current mood.",
            "channel": "These recommendations will help you channel that energy productively."
        }
        
        response_parts.append(need_phrases.get(
            mood_analysis.immediate_need,
            "Here are some personalized recommendations for you."
        ))
        
        response_text = " ".join(response_parts) + "\n\n"
        
        # Add music recommendation
        if music:
            response_text += f"🎵 **Music**: {music.title}\n"
            response_text += f"   {music.mood_match}\n"
            response_text += f"   Perfect for: {music.use_case}\n"
            if music.duration:
                response_text += f"   Duration: {music.duration}\n"
            response_text += f"   🔗 [Listen here]({music.url})\n\n"
        
        # Add movie recommendation
        if movie:
            response_text += f"🎬 **Movie**: {movie.title}"
            if movie.year:
                response_text += f" ({movie.year})"
            response_text += "\n"
            response_text += f"   {movie.mood_match}\n"
            response_text += f"   {movie.why}\n"
            if movie.genres:
                response_text += f"   Genres: {', '.join(movie.genres)}\n"
            if movie.rating:
                response_text += f"   Rating: {movie.rating}/10\n"
            response_text += f"   🔗 [Watch here]({movie.url})\n\n"
        
        # Add book recommendation
        if book:
            response_text += f"📚 **Book**: {book.title}\n"
            if book.author:
                response_text += f"   by {book.author}\n"
            response_text += f"   {book.mood_match}\n"
            response_text += f"   {book.why}\n"
            response_text += f"   Reading time: {book.reading_time}\n"
            if book.rating:
                response_text += f"   Rating: {book.rating}/5\n"
            google_books_url = book.urls.get("google_books", "")
            if google_books_url:
                response_text += f"   🔗 [Find it here]({google_books_url})\n\n"
        
        # Closing
        response_text += "\n💙 I hope these recommendations help! Let me know if you'd like different suggestions."
        
        # Create A2A message
        return A2AMessage(
            role="agent",
            parts=[MessagePart(kind="text", text=response_text)],
            messageId=str(uuid4()),
            contextId=context_id,
            taskId=task_id
        )
    
    def _create_artifacts(
        self,
        mood_analysis: MoodAnalysis,
        music: MusicRecommendation | None,
        movie: MovieRecommendation | None,
        book: BookRecommendation | None
    ) -> list[Artifact]:
        """
        Create artifacts for each media recommendation.
        
        Args:
            mood_analysis: The analyzed mood
            music: Music recommendation
            movie: Movie recommendation
            book: Book recommendation
            
        Returns:
            List of Artifact objects
        """
        artifacts = []
        
        # Mood analysis artifact
        artifacts.append(Artifact(
            artifactId=str(uuid4()),
            name="mood_analysis",
            parts=[MessagePart(
                kind="data",
                data=mood_analysis.model_dump()
            )]
        ))
        
        # Music artifact
        if music:
            artifacts.append(Artifact(
                artifactId=str(uuid4()),
                name="music_recommendation",
                parts=[MessagePart(
                    kind="data",
                    data=music.model_dump()
                )]
            ))
        
        # Movie artifact
        if movie:
            artifacts.append(Artifact(
                artifactId=str(uuid4()),
                name="movie_recommendation",
                parts=[MessagePart(
                    kind="data",
                    data=movie.model_dump()
                )]
            ))
        
        # Book artifact
        if book:
            artifacts.append(Artifact(
                artifactId=str(uuid4()),
                name="book_recommendation",
                parts=[MessagePart(
                    kind="data",
                    data=book.model_dump()
                )]
            ))
        
        return artifacts
    
    def _build_history(
        self,
        user_messages: list[A2AMessage],
        agent_message: A2AMessage
    ) -> list[A2AMessage]:
        """
        Build conversation history with user and agent messages.
        
        Args:
            user_messages: Original user messages
            agent_message: Agent's response message
            
        Returns:
            Complete conversation history
        """
        history = []
        
        # Add user messages
        for msg in user_messages:
            if msg.role == "user":
                history.append(msg)
        
        # Add agent response
        history.append(agent_message)
        
        return history
    
    def _create_error_result(
        self,
        context_id: str,
        task_id: str,
        message: str
    ) -> TaskResult:
        """
        Create error task result.
        
        Args:
            context_id: Context ID
            task_id: Task ID
            message: Error message
            
        Returns:
            TaskResult with error state
        """
        logger.error(f"Creating error result: {message}")
        
        error_message = A2AMessage(
            role="agent",
            parts=[MessagePart(
                kind="text",
                text=f"I apologize, but I encountered an issue: {message}\n\nPlease try again or rephrase your message."
            )],
            messageId=str(uuid4()),
            contextId=context_id,
            taskId=task_id
        )
        
        return TaskResult(
            taskId=task_id,
            contextId=context_id,
            status=TaskStatus(
                state="failed",
                timestamp=datetime.utcnow(),
                message=message
            ),
            artifacts=[],
            history=[error_message]
        )


# ============================================================================
# Recommendation Orchestrator
# ============================================================================


class RecommendationOrchestrator:
    """
    Orchestrates mood-based recommendations across all media types.
    
    Coordinates Spotify music, TMDB movies, and Google Books recommendations
    based on a single mood analysis.
    """
    
    def __init__(
        self,
        spotify_client_id: str | None = None,
        spotify_client_secret: str | None = None,
        tmdb_api_key: str | None = None,
        google_books_api_key: str | None = None
    ):
        """
        Initialize the orchestrator with API credentials.
        
        Args:
            spotify_client_id: Spotify API client ID
            spotify_client_secret: Spotify API client secret
            tmdb_api_key: TMDB API key
            google_books_api_key: Google Books API key (optional)
        """
        # Initialize services
        self.music_service = None
        self.movie_service = None
        self.book_service = None
        
        # Create Spotify service if credentials provided
        if spotify_client_id and spotify_client_secret:
            try:
                self.music_service = SpotifyMusicService(
                    client_id=spotify_client_id,
                    client_secret=spotify_client_secret
                )
                logger.info("Spotify service initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Spotify service: {e}")
        
        # Create TMDB service if API key provided
        if tmdb_api_key:
            try:
                self.movie_service = TMDBMovieService(api_key=tmdb_api_key)
                logger.info("TMDB service initialized")
            except Exception as e:
                logger.error(f"Failed to initialize TMDB service: {e}")
        
        # Create Google Books service
        try:
            self.book_service = GoogleBooksService(api_key=google_books_api_key)
            logger.info("Google Books service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Google Books service: {e}")
    
    async def close(self):
        """Close all service clients."""
        tasks = []
        
        if self.movie_service:
            tasks.append(self.movie_service.close())
        
        if self.book_service:
            tasks.append(self.book_service.close())
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info("All services closed")
    
    async def get_all_recommendations(
        self,
        mood_analysis: MoodAnalysis
    ) -> UnifiedRecommendation:
        """
        Get recommendations for all media types.
        
        Args:
            mood_analysis: The analyzed mood with preferences
            
        Returns:
            UnifiedRecommendation with all available recommendations
        """
        logger.info(f"Getting recommendations for mood: {mood_analysis.primary_mood}")
        
        # Get all recommendations in parallel
        music_task = self._get_music_recommendation(mood_analysis)
        movie_task = self._get_movie_recommendation(mood_analysis)
        book_task = self._get_book_recommendation(mood_analysis)
        
        music, movie, book = await asyncio.gather(
            music_task,
            movie_task,
            book_task,
            return_exceptions=True
        )
        
        # Handle exceptions
        music = music if not isinstance(music, Exception) else None
        movie = movie if not isinstance(movie, Exception) else None
        book = book if not isinstance(book, Exception) else None
        
        # Generate summary
        summary = self._generate_summary(mood_analysis, music, movie, book)
        
        return UnifiedRecommendation(
            mood_analysis=mood_analysis,
            music=music,
            movie=movie,
            book=book,
            summary=summary
        )
    
    async def get_music_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation | None:
        """
        Get music recommendation only.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            MusicRecommendation or None
        """
        return await self._get_music_recommendation(mood_analysis)
    
    async def get_movie_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> MovieRecommendation | None:
        """
        Get movie recommendation only.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            MovieRecommendation or None
        """
        return await self._get_movie_recommendation(mood_analysis)
    
    async def get_book_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> BookRecommendation | None:
        """
        Get book recommendation only.
        
        Args:
            mood_analysis: The analyzed mood
            
        Returns:
            BookRecommendation or None
        """
        return await self._get_book_recommendation(mood_analysis)
    
    async def _get_music_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> MusicRecommendation | None:
        """Internal method to get music recommendation."""
        if not self.music_service:
            logger.warning("Spotify service not available")
            return None
        
        try:
            return await self.music_service.get_recommendation(mood_analysis)
        except Exception as e:
            logger.error(f"Error getting music recommendation: {e}")
            return None
    
    async def _get_movie_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> MovieRecommendation | None:
        """Internal method to get movie recommendation."""
        if not self.movie_service:
            logger.warning("TMDB service not available")
            return None
        
        try:
            return await self.movie_service.get_recommendation(mood_analysis)
        except Exception as e:
            logger.error(f"Error getting movie recommendation: {e}")
            return None
    
    async def _get_book_recommendation(
        self,
        mood_analysis: MoodAnalysis
    ) -> BookRecommendation | None:
        """Internal method to get book recommendation."""
        if not self.book_service:
            logger.warning("Google Books service not available")
            return None
        
        try:
            return await self.book_service.get_recommendation(mood_analysis)
        except Exception as e:
            logger.error(f"Error getting book recommendation: {e}")
            return None
    
    def _generate_summary(
        self,
        mood_analysis: MoodAnalysis,
        music: MusicRecommendation | None,
        movie: MovieRecommendation | None,
        book: BookRecommendation | None
    ) -> str:
        """
        Generate overall recommendation summary.
        
        Args:
            mood_analysis: The mood analysis
            music: Music recommendation
            movie: Movie recommendation
            book: Book recommendation
            
        Returns:
            Summary string
        """
        mood = mood_analysis.primary_mood.capitalize()
        intensity = mood_analysis.intensity
        immediate_need = mood_analysis.immediate_need
        
        # Count available recommendations
        available = sum([
            music is not None,
            movie is not None,
            book is not None
        ])
        
        if available == 0:
            return f"Unable to generate recommendations for your {mood.lower()} mood at this time."
        
        # Build summary
        parts = [f"For your {mood.lower()} mood (intensity: {intensity}/10)"]
        
        # Add immediate need context
        need_context = {
            "escape": "to help you escape",
            "process": "to help you process your feelings",
            "uplift": "to uplift your spirits",
            "calm": "to calm your mind",
            "match": "that match your current state",
            "channel": "to channel your energy"
        }
        
        context = need_context.get(immediate_need, "tailored to your needs")
        parts.append(context)
        
        # Add recommendations summary
        rec_parts = []
        
        if music:
            rec_parts.append(f"music from {music.platform}")
        
        if movie:
            if movie.year:
                rec_parts.append(f"a {movie.year} film")
            else:
                rec_parts.append("a movie")
        
        if book:
            if book.author:
                rec_parts.append(f"a book by {book.author}")
            else:
                rec_parts.append("a book")
        
        if rec_parts:
            parts.append(f", we recommend {', '.join(rec_parts[:-1])}")
            if len(rec_parts) > 1:
                parts.append(f" and {rec_parts[-1]}")
            else:
                parts.append(rec_parts[0])
        
        summary = "".join(parts) + "."
        
        return summary


# ============================================================================
# Convenience Functions
# ============================================================================


def create_orchestrator(
    spotify_client_id: str | None = None,
    spotify_client_secret: str | None = None,
    tmdb_api_key: str | None = None,
    google_books_api_key: str | None = None
) -> RecommendationOrchestrator:
    """
    Create a RecommendationOrchestrator instance.
    
    Args:
        spotify_client_id: Spotify API client ID
        spotify_client_secret: Spotify API client secret
        tmdb_api_key: TMDB API key
        google_books_api_key: Google Books API key
        
    Returns:
        RecommendationOrchestrator instance
    """
    return RecommendationOrchestrator(
        spotify_client_id=spotify_client_id,
        spotify_client_secret=spotify_client_secret,
        tmdb_api_key=tmdb_api_key,
        google_books_api_key=google_books_api_key
    )


async def get_recommendations_for_mood(
    mood_analysis: MoodAnalysis,
    spotify_client_id: str | None = None,
    spotify_client_secret: str | None = None,
    tmdb_api_key: str | None = None,
    google_books_api_key: str | None = None
) -> UnifiedRecommendation:
    """
    Convenience function to get all recommendations for a mood.
    
    Args:
        mood_analysis: The analyzed mood
        spotify_client_id: Spotify API client ID
        spotify_client_secret: Spotify API client secret
        tmdb_api_key: TMDB API key
        google_books_api_key: Google Books API key
        
    Returns:
        UnifiedRecommendation with all available recommendations
    """
    orchestrator = RecommendationOrchestrator(
        spotify_client_id=spotify_client_id,
        spotify_client_secret=spotify_client_secret,
        tmdb_api_key=tmdb_api_key,
        google_books_api_key=google_books_api_key
    )
    
    try:
        return await orchestrator.get_all_recommendations(mood_analysis)
    finally:
        await orchestrator.close()
