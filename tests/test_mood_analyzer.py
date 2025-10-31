"""
Unit tests for the MoodAnalyzer service.

Run with: pytest tests/test_mood_analyzer.py -v
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services import MoodAnalysis, MoodAnalyzer


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_api_key():
    """Mock API key for testing."""
    return "test_api_key_12345"


@pytest.fixture
def sample_mood_analysis():
    """Sample MoodAnalysis object for testing."""
    return MoodAnalysis(
        primary_mood="happy",
        intensity=7,
        context="work achievement",
        music_preferences={
            "energy_level": "high",
            "preferred_genres": ["pop", "dance"],
            "vibe": ["uplifting", "energetic"],
            "keywords": ["happy", "upbeat"]
        },
        movie_preferences={
            "tone": "light",
            "preferred_genres": ["Comedy", "Romance"],
            "themes": ["friendship", "success"],
            "length_preference": "standard"
        },
        book_preferences={
            "pacing": "moderate",
            "depth": "light",
            "preferred_genres": ["Fiction", "Humor"],
            "themes": ["happiness", "success"]
        },
        immediate_need="match",
        multi_mood=False,
        secondary_moods=[],
        confidence=0.95
    )


# ============================================================================
# MoodAnalysis Model Tests
# ============================================================================


class TestMoodAnalysisModel:
    """Tests for the MoodAnalysis Pydantic model."""
    
    def test_mood_analysis_creation(self):
        """Test creating a valid MoodAnalysis object."""
        analysis = MoodAnalysis(
            primary_mood="sad",
            intensity=6,
            immediate_need="process",
            music_preferences={},
            movie_preferences={},
            book_preferences={}
        )
        
        assert analysis.primary_mood == "sad"
        assert analysis.intensity == 6
        assert analysis.immediate_need == "process"
        assert not analysis.multi_mood
        assert analysis.secondary_moods == []
    
    def test_intensity_validation(self):
        """Test intensity field validation (1-10 range)."""
        # Valid intensity
        analysis = MoodAnalysis(
            primary_mood="happy",
            intensity=5,
            immediate_need="match",
            music_preferences={},
            movie_preferences={},
            book_preferences={}
        )
        assert analysis.intensity == 5
        
        # Invalid intensity (too high)
        with pytest.raises(ValueError):
            MoodAnalysis(
                primary_mood="happy",
                intensity=11,
                immediate_need="match",
                music_preferences={},
                movie_preferences={},
                book_preferences={}
            )
        
        # Invalid intensity (too low)
        with pytest.raises(ValueError):
            MoodAnalysis(
                primary_mood="happy",
                intensity=0,
                immediate_need="match",
                music_preferences={},
                movie_preferences={},
                book_preferences={}
            )
    
    def test_immediate_need_validation(self):
        """Test immediate_need field validation."""
        # Valid immediate_need
        for need in ["escape", "process", "uplift", "calm", "match", "channel"]:
            analysis = MoodAnalysis(
                primary_mood="happy",
                intensity=5,
                immediate_need=need,
                music_preferences={},
                movie_preferences={},
                book_preferences={}
            )
            assert analysis.immediate_need == need
        
        # Invalid immediate_need
        with pytest.raises(ValueError):
            MoodAnalysis(
                primary_mood="happy",
                intensity=5,
                immediate_need="invalid_need",
                music_preferences={},
                movie_preferences={},
                book_preferences={}
            )
    
    def test_mood_normalization(self):
        """Test that mood names are normalized to lowercase."""
        analysis = MoodAnalysis(
            primary_mood="HAPPY",
            intensity=5,
            immediate_need="match",
            music_preferences={},
            movie_preferences={},
            book_preferences={},
            secondary_moods=["SAD", "Anxious"]
        )
        
        assert analysis.primary_mood == "happy"
        assert "sad" in analysis.secondary_moods
        assert "anxious" in analysis.secondary_moods
    
    def test_default_values(self):
        """Test that default values are set correctly."""
        analysis = MoodAnalysis(
            primary_mood="calm",
            intensity=4,
            immediate_need="match"
        )
        
        assert analysis.music_preferences == {}
        assert analysis.movie_preferences == {}
        assert analysis.book_preferences == {}
        assert not analysis.multi_mood
        assert analysis.secondary_moods == []
        assert analysis.confidence == 1.0
        assert analysis.context is None


# ============================================================================
# MoodAnalyzer Initialization Tests
# ============================================================================


class TestMoodAnalyzerInit:
    """Tests for MoodAnalyzer initialization."""
    
    def test_init_with_api_key(self, mock_api_key):
        """Test initialization with explicit API key."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        assert analyzer.agent is not None
    
    def test_init_with_env_var(self, monkeypatch, mock_api_key):
        """Test initialization with API key from environment."""
        monkeypatch.setenv("GEMINI_API_KEY", mock_api_key)
        analyzer = MoodAnalyzer()
        assert analyzer.agent is not None
    
    def test_init_without_api_key(self, monkeypatch):
        """Test initialization fails without API key."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="API key must be provided"):
            MoodAnalyzer()


# ============================================================================
# MoodAnalyzer Analysis Tests
# ============================================================================


class TestMoodAnalyzerAnalysis:
    """Tests for mood analysis functionality."""
    
    @pytest.mark.asyncio
    async def test_analyze_mood_empty_message(self, mock_api_key):
        """Test that empty message raises ValueError."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        with pytest.raises(ValueError, match="cannot be empty"):
            await analyzer.analyze_mood("")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            await analyzer.analyze_mood("   ")
    
    @pytest.mark.asyncio
    async def test_analyze_mood_success(self, mock_api_key, sample_mood_analysis):
        """Test successful mood analysis."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        # Mock the agent.run method
        mock_result = MagicMock()
        mock_result.data = sample_mood_analysis
        analyzer.agent.run = AsyncMock(return_value=mock_result)
        
        result = await analyzer.analyze_mood("I'm feeling great today!")
        
        assert isinstance(result, MoodAnalysis)
        assert result.primary_mood == "happy"
        assert result.intensity == 7
        assert result.immediate_need == "match"
    
    @pytest.mark.asyncio
    async def test_analyze_mood_with_context(self, mock_api_key, sample_mood_analysis):
        """Test mood analysis with additional context."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        mock_result = MagicMock()
        mock_result.data = sample_mood_analysis
        analyzer.agent.run = AsyncMock(return_value=mock_result)
        
        additional_context = {
            "user_age": 25,
            "time_of_day": "morning"
        }
        
        result = await analyzer.analyze_mood(
            "Feeling good!",
            additional_context=additional_context
        )
        
        assert isinstance(result, MoodAnalysis)
        # Verify context was passed to the agent
        analyzer.agent.run.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_mood_populates_preferences(self, mock_api_key):
        """Test that missing preferences are populated."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        # Create analysis without preferences
        incomplete_analysis = MoodAnalysis(
            primary_mood="stressed",
            intensity=7,
            immediate_need="calm"
        )
        
        mock_result = MagicMock()
        mock_result.data = incomplete_analysis
        analyzer.agent.run = AsyncMock(return_value=mock_result)
        
        result = await analyzer.analyze_mood("I'm stressed out")
        
        # Check that preferences were populated
        assert result.music_preferences is not None
        assert "energy_level" in result.music_preferences
        assert result.movie_preferences is not None
        assert "tone" in result.movie_preferences
        assert result.book_preferences is not None
        assert "pacing" in result.book_preferences
    
    @pytest.mark.asyncio
    async def test_batch_analyze_moods(self, mock_api_key, sample_mood_analysis):
        """Test batch mood analysis."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        mock_result = MagicMock()
        mock_result.data = sample_mood_analysis
        analyzer.agent.run = AsyncMock(return_value=mock_result)
        
        messages = [
            "I'm happy",
            "Feeling sad",
            "So excited!"
        ]
        
        results = await analyzer.batch_analyze_moods(messages)
        
        assert len(results) == 3
        assert all(isinstance(r, MoodAnalysis) for r in results)


# ============================================================================
# Helper Method Tests
# ============================================================================


class TestMoodAnalyzerHelpers:
    """Tests for helper methods."""
    
    def test_default_music_preferences_low_intensity(self, mock_api_key):
        """Test default music preferences for low intensity."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        prefs = analyzer._default_music_preferences("calm", intensity=2)
        
        assert prefs["energy_level"] == "low"
    
    def test_default_music_preferences_high_intensity(self, mock_api_key):
        """Test default music preferences for high intensity."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        prefs = analyzer._default_music_preferences("angry", intensity=9)
        
        assert prefs["energy_level"] == "very_high"
    
    def test_default_movie_preferences(self, mock_api_key):
        """Test default movie preferences."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        # Low intensity
        prefs_low = analyzer._default_movie_preferences("calm", intensity=3)
        assert prefs_low["tone"] == "light"
        
        # High intensity
        prefs_high = analyzer._default_movie_preferences("angry", intensity=9)
        assert prefs_high["tone"] == "serious"
    
    def test_default_book_preferences(self, mock_api_key):
        """Test default book preferences."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        # Low intensity
        prefs_low = analyzer._default_book_preferences("content", intensity=2)
        assert prefs_low["depth"] == "light"
        
        # High intensity
        prefs_high = analyzer._default_book_preferences("overwhelmed", intensity=9)
        assert prefs_high["depth"] == "profound"
    
    def test_get_mood_summary(self, mock_api_key, sample_mood_analysis):
        """Test mood summary generation."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        summary = analyzer.get_mood_summary(sample_mood_analysis)
        
        assert "Happy" in summary
        assert "7/10" in summary
        assert "Match" in summary
    
    def test_get_mood_summary_multi_mood(self, mock_api_key):
        """Test mood summary with multiple moods."""
        analyzer = MoodAnalyzer(api_key=mock_api_key)
        
        multi_mood_analysis = MoodAnalysis(
            primary_mood="sad",
            intensity=6,
            immediate_need="process",
            multi_mood=True,
            secondary_moods=["lonely", "tired"],
            music_preferences={},
            movie_preferences={},
            book_preferences={}
        )
        
        summary = analyzer.get_mood_summary(multi_mood_analysis)
        
        assert "Sad" in summary
        assert "Lonely" in summary or "Tired" in summary
        assert "6/10" in summary


# ============================================================================
# Convenience Function Tests
# ============================================================================


@pytest.mark.asyncio
async def test_quick_analyze(mock_api_key, sample_mood_analysis):
    """Test quick_analyze convenience function."""
    from services import quick_analyze
    
    with patch('services.mood_analyzer.MoodAnalyzer') as MockAnalyzer:
        mock_analyzer = MockAnalyzer.return_value
        mock_analyzer.analyze_mood = AsyncMock(return_value=sample_mood_analysis)
        
        result = await quick_analyze("I'm happy!", api_key=mock_api_key)
        
        assert isinstance(result, MoodAnalysis)
        assert result.primary_mood == "happy"


def test_create_analyzer(mock_api_key):
    """Test create_analyzer factory function."""
    from services import create_analyzer
    
    analyzer = create_analyzer(api_key=mock_api_key)
    
    assert isinstance(analyzer, MoodAnalyzer)
    assert analyzer.agent is not None


# ============================================================================
# Integration Test Markers
# ============================================================================


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api_call():
    """
    Integration test with real API call.
    
    Only runs when explicitly requested with: pytest -m integration
    Requires GEMINI_API_KEY environment variable to be set.
    """
    import os
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY not set, skipping integration test")
    
    analyzer = MoodAnalyzer(api_key=api_key)
    result = await analyzer.analyze_mood("I'm feeling happy today!")
    
    assert isinstance(result, MoodAnalysis)
    assert result.primary_mood is not None
    assert 1 <= result.intensity <= 10
    assert result.immediate_need in ["escape", "process", "uplift", "calm", "match", "channel"]
