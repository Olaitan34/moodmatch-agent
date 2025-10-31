"""
Configuration package for MoodMatch A2A Agent.

Exports mood mappings and helper functions for mood-to-media recommendations.
Provides comprehensive coverage of 52 distinct moods across 6 categories.
"""

from .mood_mappings import (
    # Main mapping dictionaries
    MOOD_MAPPINGS,
    MOOD_SIMILARITIES,
    MOOD_OPPOSITES,
    
    # Helper functions
    get_mood_mapping,
    find_similar_moods,
    merge_mood_mappings,
    get_mood_category,
    get_opposite_mood,
    get_available_moods,
    search_moods_by_category,
    validate_mood_mapping,
    
    # Energy constants
    ENERGY_VERY_LOW,
    ENERGY_LOW,
    ENERGY_MEDIUM,
    ENERGY_HIGH,
    ENERGY_VERY_HIGH,
    
    # Tone constants
    TONE_LIGHT,
    TONE_SERIOUS,
    TONE_BALANCED,
    TONE_DARK,
    TONE_UPLIFTING,
    TONE_INTENSE,
    
    # Pacing constants
    PACING_VERY_SLOW,
    PACING_SLOW,
    PACING_MODERATE,
    PACING_FAST,
    PACING_CONTEMPLATIVE,
    
    # Depth constants
    DEPTH_LIGHT,
    DEPTH_MEDIUM,
    DEPTH_DEEP,
    DEPTH_PROFOUND,
    
    # Strategy constants
    STRATEGY_MATCH,
    STRATEGY_UPLIFT,
    STRATEGY_PROCESS,
    STRATEGY_ESCAPE,
    STRATEGY_CHANNEL,
    
    # Metadata
    AVAILABLE_MOODS,
    TOTAL_MOODS,
)

__all__ = [
    # Main mappings
    "MOOD_MAPPINGS",
    "MOOD_SIMILARITIES",
    "MOOD_OPPOSITES",
    
    # Helper functions
    "get_mood_mapping",
    "find_similar_moods",
    "merge_mood_mappings",
    "get_mood_category",
    "get_opposite_mood",
    "get_available_moods",
    "search_moods_by_category",
    "validate_mood_mapping",
    
    # Energy constants
    "ENERGY_VERY_LOW",
    "ENERGY_LOW",
    "ENERGY_MEDIUM",
    "ENERGY_HIGH",
    "ENERGY_VERY_HIGH",
    
    # Tone constants
    "TONE_LIGHT",
    "TONE_SERIOUS",
    "TONE_BALANCED",
    "TONE_DARK",
    "TONE_UPLIFTING",
    "TONE_INTENSE",
    
    # Pacing constants
    "PACING_VERY_SLOW",
    "PACING_SLOW",
    "PACING_MODERATE",
    "PACING_FAST",
    "PACING_CONTEMPLATIVE",
    
    # Depth constants
    "DEPTH_LIGHT",
    "DEPTH_MEDIUM",
    "DEPTH_DEEP",
    "DEPTH_PROFOUND",
    
    # Strategy constants
    "STRATEGY_MATCH",
    "STRATEGY_UPLIFT",
    "STRATEGY_PROCESS",
    "STRATEGY_ESCAPE",
    "STRATEGY_CHANNEL",
    
    # Metadata
    "AVAILABLE_MOODS",
    "TOTAL_MOODS",
]
