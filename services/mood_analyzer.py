"""
Mood Analysis Service using Pydantic AI with Gemini Flash 2.5.

This service uses Google's Gemini model to analyze natural language mood descriptions
and extract structured mood information for personalized media recommendations.
"""

import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPException, UnexpectedModelBehaviour

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Pydantic Models
# ============================================================================


class MoodAnalysis(BaseModel):
    """
    Structured mood analysis result from natural language input.
    
    This model captures the nuanced emotional state of the user including
    primary and secondary moods, intensity, context, and media preferences.
    """
    
    primary_mood: str = Field(
        ...,
        description="The dominant mood detected (e.g., 'happy', 'sad', 'anxious', 'energetic')"
    )
    
    intensity: int = Field(
        ...,
        ge=1,
        le=10,
        description="Intensity of the mood on a scale of 1-10, where 1 is very mild and 10 is overwhelming"
    )
    
    context: str | None = Field(
        None,
        description="Situational context or trigger for the mood (e.g., 'after work', 'breakup', 'achievement')"
    )
    
    music_preferences: dict[str, Any] = Field(
        default_factory=dict,
        description="Music preferences including genres, energy level, and vibe"
    )
    
    movie_preferences: dict[str, Any] = Field(
        default_factory=dict,
        description="Movie preferences including genres, tone, and preferred length"
    )
    
    book_preferences: dict[str, Any] = Field(
        default_factory=dict,
        description="Book preferences including genres, themes, pacing, and depth"
    )
    
    immediate_need: str = Field(
        ...,
        description="What the user needs right now: escape, process, uplift, calm, or match"
    )
    
    multi_mood: bool = Field(
        default=False,
        description="Whether multiple distinct moods are present"
    )
    
    secondary_moods: list[str] = Field(
        default_factory=list,
        description="Additional moods detected beyond the primary mood"
    )
    
    time_context: str | None = Field(
        None,
        description="Time-related context (e.g., 'morning', 'late night', 'weekend')"
    )
    
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence score of the analysis (0.0-1.0)"
    )
    
    @field_validator("immediate_need")
    @classmethod
    def validate_immediate_need(cls, v: str) -> str:
        """Validate immediate need is one of the allowed values."""
        allowed = {"escape", "process", "uplift", "calm", "match", "channel"}
        if v.lower() not in allowed:
            raise ValueError(f"immediate_need must be one of {allowed}")
        return v.lower()
    
    @field_validator("primary_mood", "secondary_moods")
    @classmethod
    def normalize_mood_names(cls, v: str | list[str]) -> str | list[str]:
        """Normalize mood names to lowercase."""
        if isinstance(v, str):
            return v.lower().strip()
        return [mood.lower().strip() for mood in v]


# ============================================================================
# Mood Analyzer Service
# ============================================================================


class MoodAnalyzer:
    """
    Mood analysis service using Pydantic AI with Gemini Flash 2.5.
    
    This service analyzes natural language mood descriptions and extracts
    structured information for personalized media recommendations.
    
    Attributes:
        agent: Pydantic AI agent configured with Gemini model
    """
    
    # Comprehensive system instructions for the LLM
    SYSTEM_INSTRUCTIONS = """You are an expert mood analyst and emotional intelligence specialist for the MoodMatch recommendation system. Your role is to analyze users' emotional states from their natural language descriptions and extract structured information for personalized media recommendations.

## Your Expertise

You understand:
- The full spectrum of human emotions (52 distinct moods across 6 categories)
- Emotional intensity and how it affects media consumption needs
- Context clues that indicate situational triggers
- Time-of-day patterns in emotional states
- Multi-mood states and emotional complexity
- The difference between wanting to process emotions vs. escape them

## Analysis Guidelines

### 1. Mood Identification
Detect from these 52 moods organized by category:

**Positive Emotions (10):**
happy, excited, grateful, peaceful, confident, inspired, playful, content, loving, proud

**Negative Emotions (12):**
sad, anxious, stressed, angry, lonely, heartbroken, disappointed, guilty, jealous, embarrassed, afraid, hopeless

**Energy States (8):**
energetic, tired, restless, sluggish, hyper, burnt_out, mellow, drowsy

**Social/Relational (8):**
social, introverted, romantic, nostalgic, homesick, misunderstood, betrayed, supported

**Existential/Reflective (8):**
contemplative, philosophical, curious, confused, stuck, purposeful, empty, overwhelmed

**Transitional/Complex (6):**
bittersweet, numb, vengeful, rebellious, vulnerable, bored

### 2. Intensity Assessment (1-10 scale)
- 1-3: Mild, subtle feeling
- 4-6: Moderate, noticeable but manageable
- 7-8: Strong, significantly impacting behavior
- 9-10: Overwhelming, all-consuming

### 3. Context Extraction
Look for:
- Situational triggers (work, relationships, events)
- Time indicators (morning, night, weekend)
- Duration indicators (just now, all day, for weeks)
- Social context (alone, with others, missing someone)

### 4. Multi-Mood Detection
Identify when multiple distinct moods coexist:
- "I'm happy but also anxious" → multi_mood: true
- "Feeling sad and lonely" → similar moods, might be single primary
- "Excited but tired" → conflicting energy, multi_mood: true

### 5. Immediate Need Assessment
Determine what the user needs:
- **escape**: Want distraction, entertainment, forget current state
- **process**: Need to feel and work through emotions (catharsis)
- **uplift**: Want to gradually improve mood, feel better
- **calm**: Need relaxation, stress reduction, peace
- **match**: Want content that validates current emotional state
- **channel**: Need to redirect intense energy productively

### 6. Media Preferences Extraction

**Music Preferences:**
{
  "energy_level": "very_low" | "low" | "medium" | "high" | "very_high",
  "preferred_genres": ["genre1", "genre2", ...],  // 3-5 genres
  "vibe": ["vibe1", "vibe2", ...],  // 3-5 descriptors
  "keywords": ["keyword1", "keyword2", ...]  // 3-5 search terms
}

**Movie Preferences:**
{
  "tone": "light" | "serious" | "balanced" | "dark" | "uplifting" | "intense",
  "preferred_genres": ["genre1", "genre2", ...],  // 2-4 genres
  "themes": ["theme1", "theme2", ...],  // 3-5 themes
  "length_preference": "short" | "standard" | "long" | "any"  // Based on energy/time
}

**Book Preferences:**
{
  "pacing": "very_slow" | "slow" | "moderate" | "fast" | "contemplative",
  "depth": "light" | "medium" | "deep" | "profound",
  "preferred_genres": ["genre1", "genre2", ...],  // 2-4 genres
  "themes": ["theme1", "theme2", ...]  // 3-5 themes
}

## Response Format Rules

1. Always provide a valid primary_mood from the 52 available moods
2. Set multi_mood to true only when distinctly different moods coexist
3. secondary_moods should be empty if multi_mood is false
4. Confidence should reflect certainty: 0.9-1.0 for clear statements, 0.6-0.8 for ambiguous, <0.6 for very unclear
5. Include time_context if any time-related information is mentioned
6. Be culturally sensitive and avoid assumptions
7. If unsure about exact mood, choose the closest match and lower confidence

## Example Analyses

Input: "I just broke up with my girlfriend and I'm feeling really down. Can't stop thinking about her."
Output:
{
  "primary_mood": "heartbroken",
  "intensity": 8,
  "context": "recent breakup",
  "immediate_need": "process",
  "multi_mood": true,
  "secondary_moods": ["sad", "lonely"],
  "confidence": 0.95
}

Input: "It's 2am and I can't sleep, my mind won't stop racing"
Output:
{
  "primary_mood": "restless",
  "intensity": 7,
  "context": "insomnia, racing thoughts",
  "immediate_need": "calm",
  "multi_mood": true,
  "secondary_moods": ["anxious", "tired"],
  "time_context": "late night",
  "confidence": 0.9
}

Input: "Feeling good today! Just got a promotion at work"
Output:
{
  "primary_mood": "proud",
  "intensity": 8,
  "context": "work achievement, promotion",
  "immediate_need": "match",
  "multi_mood": false,
  "secondary_moods": [],
  "confidence": 1.0
}

Input: "Idk, just kinda meh I guess"
Output:
{
  "primary_mood": "bored",
  "intensity": 4,
  "context": null,
  "immediate_need": "escape",
  "multi_mood": false,
  "secondary_moods": [],
  "confidence": 0.6
}

## Important Notes

- Be empathetic but objective in your analysis
- Don't make therapeutic recommendations - focus on mood analysis only
- Respect the user's emotional state without judgment
- If input contains crisis language (suicide, self-harm), set confidence to 0.0 and primary_mood to "afraid" (the system will handle crisis resources)
- Default to "match" for immediate_need if unclear, unless context suggests otherwise
- Consider cultural and contextual variations in emotional expression
"""

    def __init__(self, api_key: str | None = None):
        """
        Initialize the MoodAnalyzer with Pydantic AI agent.
        
        Args:
            api_key: Google API key for Gemini. If None, will use GEMINI_API_KEY env var.
            
        Raises:
            ValueError: If no API key is provided or found in environment
        """
        if not api_key:
            import os
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError(
                    "Gemini API key must be provided via api_key parameter or GEMINI_API_KEY environment variable"
                )
        
        # Initialize Pydantic AI Agent with Gemini Flash 2.5
        self.agent: Agent[None, MoodAnalysis] = Agent(
            model="google-geminiai:gemini-2.0-flash-exp",
            result_type=MoodAnalysis,
            system_prompt=self.SYSTEM_INSTRUCTIONS,
            model_settings={
                "temperature": 0.3,  # Lower temperature for more consistent analysis
                "top_p": 0.8,
                "max_tokens": 2000,
            },
        )
        
        logger.info("MoodAnalyzer initialized with Gemini Flash 2.5")
    
    async def analyze_mood(
        self,
        user_message: str,
        additional_context: dict[str, Any] | None = None
    ) -> MoodAnalysis:
        """
        Analyze a user's mood from natural language description.
        
        Args:
            user_message: The user's natural language mood description
            additional_context: Optional additional context (e.g., user history, preferences)
            
        Returns:
            MoodAnalysis object with structured mood information
            
        Raises:
            ValueError: If user_message is empty or invalid
            RuntimeError: If mood analysis fails
            
        Examples:
            >>> analyzer = MoodAnalyzer(api_key="your-key")
            >>> result = await analyzer.analyze_mood("I'm feeling really stressed today")
            >>> print(result.primary_mood)  # "stressed"
            >>> print(result.intensity)  # 7
        """
        if not user_message or not user_message.strip():
            raise ValueError("user_message cannot be empty")
        
        # Add timestamp for context
        current_time = datetime.now()
        time_info = f"\n\nCurrent context: {current_time.strftime('%A, %I:%M %p')}"
        
        # Build full prompt with context
        full_prompt = user_message.strip()
        if additional_context:
            context_str = "\n\nAdditional context:\n"
            for key, value in additional_context.items():
                context_str += f"- {key}: {value}\n"
            full_prompt += context_str
        full_prompt += time_info
        
        try:
            logger.info(f"Analyzing mood for message: {user_message[:100]}...")
            
            # Run the agent
            result = await self.agent.run(full_prompt)
            
            mood_analysis = result.data
            
            # Post-process: Ensure music preferences are populated
            if not mood_analysis.music_preferences:
                mood_analysis.music_preferences = self._default_music_preferences(
                    mood_analysis.primary_mood,
                    mood_analysis.intensity
                )
            
            # Post-process: Ensure movie preferences are populated
            if not mood_analysis.movie_preferences:
                mood_analysis.movie_preferences = self._default_movie_preferences(
                    mood_analysis.primary_mood,
                    mood_analysis.intensity
                )
            
            # Post-process: Ensure book preferences are populated
            if not mood_analysis.book_preferences:
                mood_analysis.book_preferences = self._default_book_preferences(
                    mood_analysis.primary_mood,
                    mood_analysis.intensity
                )
            
            logger.info(
                f"Mood analysis complete: primary_mood={mood_analysis.primary_mood}, "
                f"intensity={mood_analysis.intensity}, confidence={mood_analysis.confidence}"
            )
            
            return mood_analysis
            
        except ModelHTTPException as e:
            logger.error(f"HTTP error during mood analysis: {e}")
            raise RuntimeError(f"Failed to connect to Gemini API: {e}") from e
        
        except UnexpectedModelBehaviour as e:
            logger.error(f"Unexpected model behavior: {e}")
            raise RuntimeError(f"Gemini model returned unexpected response: {e}") from e
        
        except Exception as e:
            logger.error(f"Unexpected error during mood analysis: {e}")
            raise RuntimeError(f"Mood analysis failed: {e}") from e
    
    def _default_music_preferences(self, mood: str, intensity: int) -> dict[str, Any]:
        """Generate default music preferences based on mood and intensity."""
        # Map intensity to energy level
        if intensity <= 3:
            energy = "low"
        elif intensity <= 5:
            energy = "medium"
        elif intensity <= 7:
            energy = "high"
        else:
            energy = "very_high"
        
        return {
            "energy_level": energy,
            "preferred_genres": [],
            "vibe": [],
            "keywords": []
        }
    
    def _default_movie_preferences(self, mood: str, intensity: int) -> dict[str, Any]:
        """Generate default movie preferences based on mood and intensity."""
        # Map intensity to tone
        if intensity <= 4:
            tone = "light"
        elif intensity <= 7:
            tone = "balanced"
        else:
            tone = "serious"
        
        return {
            "tone": tone,
            "preferred_genres": [],
            "themes": [],
            "length_preference": "standard"
        }
    
    def _default_book_preferences(self, mood: str, intensity: int) -> dict[str, Any]:
        """Generate default book preferences based on mood and intensity."""
        # Map intensity to depth
        if intensity <= 3:
            depth = "light"
        elif intensity <= 6:
            depth = "medium"
        elif intensity <= 8:
            depth = "deep"
        else:
            depth = "profound"
        
        return {
            "pacing": "moderate",
            "depth": depth,
            "preferred_genres": [],
            "themes": []
        }
    
    async def batch_analyze_moods(
        self,
        messages: list[str]
    ) -> list[MoodAnalysis]:
        """
        Analyze multiple mood messages in batch.
        
        Args:
            messages: List of user mood descriptions
            
        Returns:
            List of MoodAnalysis objects
            
        Note:
            This method processes messages sequentially. For true parallel processing,
            use asyncio.gather() with multiple analyze_mood() calls.
        """
        results = []
        for message in messages:
            try:
                result = await self.analyze_mood(message)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze message '{message[:50]}...': {e}")
                # Continue with other messages
                continue
        
        return results
    
    def get_mood_summary(self, analysis: MoodAnalysis) -> str:
        """
        Generate a human-readable summary of the mood analysis.
        
        Args:
            analysis: MoodAnalysis object
            
        Returns:
            Human-readable summary string
        """
        summary_parts = [
            f"Primary mood: {analysis.primary_mood.title()} (intensity: {analysis.intensity}/10)"
        ]
        
        if analysis.multi_mood and analysis.secondary_moods:
            summary_parts.append(
                f"Also feeling: {', '.join(m.title() for m in analysis.secondary_moods)}"
            )
        
        if analysis.context:
            summary_parts.append(f"Context: {analysis.context}")
        
        summary_parts.append(f"Recommendation strategy: {analysis.immediate_need.title()}")
        
        if analysis.confidence < 0.8:
            summary_parts.append(f"(Confidence: {analysis.confidence:.0%})")
        
        return " | ".join(summary_parts)


# ============================================================================
# Convenience Functions
# ============================================================================


async def quick_analyze(user_message: str, api_key: str | None = None) -> MoodAnalysis:
    """
    Quick convenience function for one-off mood analysis.
    
    Args:
        user_message: User's mood description
        api_key: Optional Gemini API key
        
    Returns:
        MoodAnalysis object
        
    Example:
        >>> result = await quick_analyze("I'm feeling overwhelmed with work")
    """
    analyzer = MoodAnalyzer(api_key=api_key)
    return await analyzer.analyze_mood(user_message)


def create_analyzer(api_key: str | None = None) -> MoodAnalyzer:
    """
    Factory function to create a MoodAnalyzer instance.
    
    Args:
        api_key: Optional Gemini API key
        
    Returns:
        Configured MoodAnalyzer instance
    """
    return MoodAnalyzer(api_key=api_key)
