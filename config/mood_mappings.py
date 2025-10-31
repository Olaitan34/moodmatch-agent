"""
Mood-to-Media Mappings for MoodMatch Agent.

This module provides psychologically-informed mappings from emotional states to
appropriate media recommendations (music, movies, books). Each mood is mapped to
genres, energy levels, themes, and keywords that align with psychological research
on mood regulation and emotional well-being.

The mappings support both mood matching (validating feelings) and mood shifting
(helping transition to desired emotional states).

Coverage: 52 distinct moods across 6 categories:
- Positive Emotions (10 moods)
- Negative Emotions (12 moods)  
- Energy States (8 moods)
- Social/Relational (8 moods)
- Existential/Reflective (8 moods)
- Transitional/Complex (6 moods)
"""

from typing import Any
from difflib import get_close_matches


# ============================================================================
# Mood-to-Media Mappings - 52 Comprehensive Moods
# ============================================================================

MOOD_MAPPINGS: dict[str, dict[str, Any]] = {
    # ========================================================================
    # POSITIVE EMOTIONS (10 moods)
    # ========================================================================
    
    "happy": {
        "music_genres": ["upbeat pop", "indie pop", "dance", "feel good", "sunshine"],
        "music_energy": "high",
        "music_vibe": ["uplifting", "cheerful", "energizing", "joyful"],
        "music_keywords": ["happy", "feel good", "positive vibes", "good mood"],
        "movie_genres": ["Comedy", "Romance", "Animation", "Musical"],
        "movie_tone": "light",
        "movie_themes": ["friendship", "love", "triumph", "joy"],
        "movie_keywords": ["feel-good", "heartwarming", "uplifting", "fun"],
        "book_genres": ["Fiction", "Romance", "Humor", "Young Adult"],
        "book_themes": ["happiness", "love", "friendship", "success"],
        "book_pacing": "moderate",
        "book_depth": "light",
        "book_keywords": ["uplifting", "heartwarming", "feel-good", "joyful"],
        "avoid_themes": ["tragedy", "dark", "depressing"],
        "recommendation_strategy": "match"
    },
    
    "excited": {
        "music_genres": ["upbeat pop", "dance", "electronic", "rock", "party"],
        "music_energy": "very_high",
        "music_vibe": ["energizing", "celebratory", "powerful", "fun"],
        "music_keywords": ["party", "pump up", "celebration", "high energy"],
        "movie_genres": ["Action", "Adventure", "Comedy", "Animation"],
        "movie_tone": "uplifting",
        "movie_themes": ["triumph", "adventure", "success", "excitement"],
        "movie_keywords": ["thrilling", "exciting", "entertaining", "inspiring"],
        "book_genres": ["Adventure", "Thriller", "Biography", "Self-Help"],
        "book_themes": ["achievement", "journey", "success", "ambition"],
        "book_pacing": "fast",
        "book_depth": "light",
        "book_keywords": ["motivating", "success stories", "adventure", "exciting"],
        "avoid_themes": ["sad", "slow", "depressing", "boring"],
        "recommendation_strategy": "match"
    },
    
    "grateful": {
        "music_genres": ["acoustic", "folk", "indie", "soul", "gospel"],
        "music_energy": "medium",
        "music_vibe": ["warm", "heartfelt", "uplifting", "peaceful"],
        "music_keywords": ["grateful", "thankful", "blessings", "appreciation"],
        "movie_genres": ["Drama", "Biography", "Documentary", "Family"],
        "movie_tone": "uplifting",
        "movie_themes": ["kindness", "family", "community", "appreciation"],
        "movie_keywords": ["heartwarming", "inspiring", "meaningful", "touching"],
        "book_genres": ["Memoir", "Self-Help", "Philosophy", "Biography"],
        "book_themes": ["gratitude", "appreciation", "kindness", "perspective"],
        "book_pacing": "contemplative",
        "book_depth": "medium",
        "book_keywords": ["gratitude", "thankfulness", "appreciation", "mindfulness"],
        "avoid_themes": ["cynical", "negative", "ungrateful"],
        "recommendation_strategy": "match"
    },
    
    "peaceful": {
        "music_genres": ["ambient", "classical", "acoustic", "nature sounds", "meditation"],
        "music_energy": "low",
        "music_vibe": ["calming", "serene", "gentle", "tranquil"],
        "music_keywords": ["peaceful", "calm", "relaxing", "meditation"],
        "movie_genres": ["Documentary", "Drama", "Animation", "Romance"],
        "movie_tone": "balanced",
        "movie_themes": ["nature", "harmony", "simplicity", "tranquility"],
        "movie_keywords": ["peaceful", "serene", "contemplative", "gentle"],
        "book_genres": ["Poetry", "Philosophy", "Nature", "Fiction"],
        "book_themes": ["peace", "mindfulness", "nature", "harmony"],
        "book_pacing": "slow",
        "book_depth": "medium",
        "book_keywords": ["peaceful", "calm", "serene", "mindfulness"],
        "avoid_themes": ["violent", "chaotic", "intense", "stressful"],
        "recommendation_strategy": "match"
    },
    
    "confident": {
        "music_genres": ["hip hop", "rock", "electronic", "pop", "power"],
        "music_energy": "high",
        "music_vibe": ["powerful", "empowering", "bold", "strong"],
        "music_keywords": ["confidence", "powerful", "boss", "unstoppable"],
        "movie_genres": ["Action", "Biography", "Drama", "Sport"],
        "movie_tone": "uplifting",
        "movie_themes": ["empowerment", "success", "overcoming", "strength"],
        "movie_keywords": ["empowering", "inspiring", "triumphant", "bold"],
        "book_genres": ["Self-Help", "Biography", "Business", "Psychology"],
        "book_themes": ["confidence", "empowerment", "success", "leadership"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["confidence", "empowerment", "success", "strength"],
        "avoid_themes": ["defeat", "weakness", "failure"],
        "recommendation_strategy": "match"
    },
    
    "inspired": {
        "music_genres": ["classical", "epic", "orchestral", "indie folk", "cinematic"],
        "music_energy": "medium",
        "music_vibe": ["inspiring", "uplifting", "powerful", "creative"],
        "music_keywords": ["inspiring", "motivational", "creative", "epic"],
        "movie_genres": ["Biography", "Drama", "Documentary", "Adventure"],
        "movie_tone": "uplifting",
        "movie_themes": ["achievement", "creativity", "innovation", "transformation"],
        "movie_keywords": ["inspiring", "motivational", "transformative", "powerful"],
        "book_genres": ["Biography", "Self-Help", "Philosophy", "History"],
        "book_themes": ["inspiration", "creativity", "innovation", "achievement"],
        "book_pacing": "moderate",
        "book_depth": "deep",
        "book_keywords": ["inspiring", "motivational", "creative", "wisdom"],
        "avoid_themes": ["pessimistic", "defeat", "cynical"],
        "recommendation_strategy": "match"
    },
    
    "playful": {
        "music_genres": ["indie pop", "funk", "dance", "quirky", "upbeat"],
        "music_energy": "high",
        "music_vibe": ["fun", "lighthearted", "cheerful", "carefree"],
        "music_keywords": ["fun", "playful", "quirky", "lighthearted"],
        "movie_genres": ["Comedy", "Animation", "Adventure", "Family"],
        "movie_tone": "light",
        "movie_themes": ["fun", "adventure", "humor", "whimsy"],
        "movie_keywords": ["funny", "lighthearted", "entertaining", "playful"],
        "book_genres": ["Humor", "Fiction", "Young Adult", "Graphic Novels"],
        "book_themes": ["fun", "adventure", "humor", "whimsy"],
        "book_pacing": "fast",
        "book_depth": "light",
        "book_keywords": ["funny", "lighthearted", "entertaining", "fun"],
        "avoid_themes": ["serious", "heavy", "dark"],
        "recommendation_strategy": "match"
    },
    
    "content": {
        "music_genres": ["acoustic", "indie folk", "chill", "soft rock", "jazz"],
        "music_energy": "medium",
        "music_vibe": ["comfortable", "warm", "relaxed", "satisfied"],
        "music_keywords": ["content", "relaxed", "comfortable", "chill"],
        "movie_genres": ["Drama", "Romance", "Comedy", "Documentary"],
        "movie_tone": "balanced",
        "movie_themes": ["satisfaction", "comfort", "simplicity", "harmony"],
        "movie_keywords": ["comfortable", "satisfying", "pleasant", "easy"],
        "book_genres": ["Fiction", "Memoir", "Poetry", "Essays"],
        "book_themes": ["contentment", "simplicity", "appreciation", "peace"],
        "book_pacing": "slow",
        "book_depth": "medium",
        "book_keywords": ["comfortable", "satisfying", "peaceful", "reflective"],
        "avoid_themes": ["chaotic", "intense", "disturbing"],
        "recommendation_strategy": "match"
    },
    
    "loving": {
        "music_genres": ["r&b", "soul", "romantic", "acoustic", "indie"],
        "music_energy": "low",
        "music_vibe": ["romantic", "warm", "tender", "affectionate"],
        "music_keywords": ["love", "romantic", "intimate", "tender"],
        "movie_genres": ["Romance", "Drama", "Comedy"],
        "movie_tone": "light",
        "movie_themes": ["love", "romance", "connection", "intimacy"],
        "movie_keywords": ["romantic", "heartwarming", "sweet", "touching"],
        "book_genres": ["Romance", "Fiction", "Poetry", "Memoir"],
        "book_themes": ["love", "romance", "connection", "passion"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["romantic", "love", "heartwarming", "tender"],
        "avoid_themes": ["heartbreak", "betrayal", "cynical"],
        "recommendation_strategy": "match"
    },
    
    "proud": {
        "music_genres": ["orchestral", "rock", "hip hop", "epic", "triumphant"],
        "music_energy": "high",
        "music_vibe": ["triumphant", "powerful", "celebratory", "victorious"],
        "music_keywords": ["triumph", "victory", "success", "achievement"],
        "movie_genres": ["Biography", "Sport", "Drama", "Documentary"],
        "movie_tone": "uplifting",
        "movie_themes": ["achievement", "success", "overcoming", "triumph"],
        "movie_keywords": ["inspiring", "triumphant", "victorious", "powerful"],
        "book_genres": ["Biography", "Self-Help", "History", "Business"],
        "book_themes": ["achievement", "success", "pride", "accomplishment"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["success", "achievement", "inspiring", "triumphant"],
        "avoid_themes": ["failure", "defeat", "humiliation"],
        "recommendation_strategy": "match"
    },
    
    # ========================================================================
    # NEGATIVE EMOTIONS (12 moods)
    # ========================================================================
    
    "sad": {
        "music_genres": ["sad", "acoustic", "indie folk", "piano", "melancholic"],
        "music_energy": "low",
        "music_vibe": ["melancholic", "emotional", "somber", "heartfelt"],
        "music_keywords": ["sad", "crying", "emotional", "heartbreak"],
        "movie_genres": ["Drama", "Romance", "Animation"],
        "movie_tone": "serious",
        "movie_themes": ["loss", "grief", "healing", "catharsis"],
        "movie_keywords": ["emotional", "moving", "cathartic", "poignant"],
        "book_genres": ["Fiction", "Literary Fiction", "Poetry", "Memoir"],
        "book_themes": ["sadness", "loss", "healing", "human condition"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["emotional", "moving", "cathartic", "healing"],
        "avoid_themes": ["superficial", "overly cheerful"],
        "recommendation_strategy": "process"
    },
    
    "anxious": {
        "music_genres": ["ambient", "lo-fi", "classical", "meditation", "calm"],
        "music_energy": "very_low",
        "music_vibe": ["calming", "soothing", "peaceful", "gentle"],
        "music_keywords": ["anxiety relief", "calming", "meditation", "peaceful"],
        "movie_genres": ["Animation", "Comedy", "Documentary", "Family"],
        "movie_tone": "light",
        "movie_themes": ["comfort", "safety", "reassurance", "peace"],
        "movie_keywords": ["comforting", "gentle", "safe", "predictable"],
        "book_genres": ["Self-Help", "Fiction", "Poetry", "Meditation"],
        "book_themes": ["anxiety", "mindfulness", "peace", "grounding"],
        "book_pacing": "slow",
        "book_depth": "medium",
        "book_keywords": ["anxiety", "calm", "mindfulness", "peace"],
        "avoid_themes": ["thriller", "suspense", "horror", "chaos"],
        "recommendation_strategy": "uplift"
    },
    
    "stressed": {
        "music_genres": ["ambient", "lo-fi", "acoustic", "classical", "chill"],
        "music_energy": "low",
        "music_vibe": ["calming", "peaceful", "soothing", "gentle"],
        "music_keywords": ["stress relief", "deep focus", "calm", "meditation"],
        "movie_genres": ["Comedy", "Animation", "Drama"],
        "movie_tone": "light",
        "movie_themes": ["feel-good", "comfort", "low-stakes", "uplifting"],
        "movie_keywords": ["relaxing", "heartwarming", "gentle"],
        "book_genres": ["Self-Help", "Fiction", "Poetry"],
        "book_themes": ["mindfulness", "rest", "simplicity", "balance"],
        "book_pacing": "contemplative",
        "book_depth": "medium",
        "book_keywords": ["stress management", "calm", "peace"],
        "avoid_themes": ["intense", "dark", "complex plots"],
        "recommendation_strategy": "uplift"
    },
    
    "angry": {
        "music_genres": ["rock", "metal", "punk", "aggressive", "intense"],
        "music_energy": "very_high",
        "music_vibe": ["powerful", "intense", "cathartic", "aggressive"],
        "music_keywords": ["anger", "intense", "power", "release"],
        "movie_genres": ["Action", "Thriller", "Drama"],
        "movie_tone": "intense",
        "movie_themes": ["justice", "revenge", "overcoming", "empowerment"],
        "movie_keywords": ["intense", "powerful", "cathartic", "justice"],
        "book_genres": ["Thriller", "Fiction", "Biography", "Self-Help"],
        "book_themes": ["justice", "anger management", "empowerment", "transformation"],
        "book_pacing": "fast",
        "book_depth": "medium",
        "book_keywords": ["anger", "justice", "empowerment", "cathartic"],
        "avoid_themes": ["passive", "weak", "submissive"],
        "recommendation_strategy": "channel"
    },
    
    "lonely": {
        "music_genres": ["indie", "acoustic", "singer-songwriter", "sad", "soul"],
        "music_energy": "low",
        "music_vibe": ["melancholic", "intimate", "emotional", "reflective"],
        "music_keywords": ["lonely", "alone", "solitude", "connection"],
        "movie_genres": ["Drama", "Romance", "Comedy", "Animation"],
        "movie_tone": "balanced",
        "movie_themes": ["connection", "friendship", "belonging", "community"],
        "movie_keywords": ["connection", "friendship", "warmth", "belonging"],
        "book_genres": ["Fiction", "Romance", "Memoir", "Self-Help"],
        "book_themes": ["loneliness", "connection", "belonging", "friendship"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["loneliness", "connection", "friendship", "belonging"],
        "avoid_themes": ["isolation", "abandonment", "despair"],
        "recommendation_strategy": "process"
    },
    
    "heartbroken": {
        "music_genres": ["sad", "breakup", "emotional", "soul", "r&b"],
        "music_energy": "low",
        "music_vibe": ["heartfelt", "emotional", "cathartic", "healing"],
        "music_keywords": ["heartbreak", "breakup", "sad love", "healing"],
        "movie_genres": ["Romance", "Drama", "Comedy"],
        "movie_tone": "balanced",
        "movie_themes": ["heartbreak", "healing", "self-discovery", "growth"],
        "movie_keywords": ["emotional", "cathartic", "healing", "moving on"],
        "book_genres": ["Romance", "Fiction", "Self-Help", "Poetry"],
        "book_themes": ["heartbreak", "healing", "recovery", "resilience"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["heartbreak", "healing", "moving on", "recovery"],
        "avoid_themes": ["toxic relationships", "betrayal", "cynical"],
        "recommendation_strategy": "process"
    },
    
    "disappointed": {
        "music_genres": ["indie", "acoustic", "melancholic", "soft rock", "alternative"],
        "music_energy": "low",
        "music_vibe": ["reflective", "somber", "hopeful", "gentle"],
        "music_keywords": ["disappointed", "let down", "reflective", "hopeful"],
        "movie_genres": ["Drama", "Biography", "Comedy"],
        "movie_tone": "balanced",
        "movie_themes": ["resilience", "overcoming", "hope", "growth"],
        "movie_keywords": ["inspiring", "hopeful", "uplifting", "resilient"],
        "book_genres": ["Self-Help", "Biography", "Fiction", "Philosophy"],
        "book_themes": ["disappointment", "resilience", "perspective", "growth"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["resilience", "overcoming", "hope", "perspective"],
        "avoid_themes": ["failure", "giving up", "pessimistic"],
        "recommendation_strategy": "uplift"
    },
    
    "guilty": {
        "music_genres": ["acoustic", "indie folk", "melancholic", "soft", "reflective"],
        "music_energy": "low",
        "music_vibe": ["reflective", "somber", "contemplative", "gentle"],
        "music_keywords": ["regret", "reflection", "forgiveness", "healing"],
        "movie_genres": ["Drama", "Biography"],
        "movie_tone": "serious",
        "movie_themes": ["redemption", "forgiveness", "growth", "learning"],
        "movie_keywords": ["redemptive", "thoughtful", "meaningful", "forgiving"],
        "book_genres": ["Fiction", "Philosophy", "Self-Help", "Memoir"],
        "book_themes": ["guilt", "redemption", "forgiveness", "growth"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["guilt", "redemption", "forgiveness", "self-compassion"],
        "avoid_themes": ["judgmental", "harsh", "unforgiving"],
        "recommendation_strategy": "process"
    },
    
    "jealous": {
        "music_genres": ["r&b", "soul", "alternative", "emotional", "intense"],
        "music_energy": "medium",
        "music_vibe": ["intense", "emotional", "powerful", "raw"],
        "music_keywords": ["jealousy", "emotional", "intense", "raw"],
        "movie_genres": ["Drama", "Thriller", "Romance"],
        "movie_tone": "dark",
        "movie_themes": ["self-worth", "confidence", "overcoming", "growth"],
        "movie_keywords": ["intense", "emotional", "transformative", "powerful"],
        "book_genres": ["Psychology", "Self-Help", "Fiction", "Memoir"],
        "book_themes": ["jealousy", "self-worth", "confidence", "security"],
        "book_pacing": "moderate",
        "book_depth": "deep",
        "book_keywords": ["jealousy", "self-worth", "confidence", "security"],
        "avoid_themes": ["comparison", "inadequacy"],
        "recommendation_strategy": "process"
    },
    
    "embarrassed": {
        "music_genres": ["chill", "lo-fi", "indie", "soft", "comforting"],
        "music_energy": "low",
        "music_vibe": ["comforting", "gentle", "reassuring", "calm"],
        "music_keywords": ["comfort", "reassuring", "gentle", "calm"],
        "movie_genres": ["Comedy", "Drama", "Animation"],
        "movie_tone": "light",
        "movie_themes": ["acceptance", "humor", "resilience", "growth"],
        "movie_keywords": ["relatable", "comforting", "lighthearted", "accepting"],
        "book_genres": ["Humor", "Self-Help", "Memoir", "Fiction"],
        "book_themes": ["embarrassment", "acceptance", "humor", "resilience"],
        "book_pacing": "moderate",
        "book_depth": "light",
        "book_keywords": ["embarrassment", "acceptance", "humor", "relatable"],
        "avoid_themes": ["humiliation", "shame", "judgment"],
        "recommendation_strategy": "uplift"
    },
    
    "afraid": {
        "music_genres": ["ambient", "calming", "soft", "meditation", "peaceful"],
        "music_energy": "very_low",
        "music_vibe": ["soothing", "safe", "calming", "reassuring"],
        "music_keywords": ["calm", "safe", "peaceful", "reassuring"],
        "movie_genres": ["Animation", "Comedy", "Family", "Documentary"],
        "movie_tone": "light",
        "movie_themes": ["safety", "courage", "overcoming", "hope"],
        "movie_keywords": ["comforting", "reassuring", "hopeful", "safe"],
        "book_genres": ["Self-Help", "Fiction", "Biography", "Philosophy"],
        "book_themes": ["courage", "fear", "resilience", "safety"],
        "book_pacing": "slow",
        "book_depth": "medium",
        "book_keywords": ["courage", "fear", "overcoming", "resilience"],
        "avoid_themes": ["horror", "thriller", "scary", "dangerous"],
        "recommendation_strategy": "uplift"
    },
    
    "hopeless": {
        "music_genres": ["ambient", "classical", "soft", "hopeful", "uplifting"],
        "music_energy": "low",
        "music_vibe": ["gentle", "hopeful", "uplifting", "comforting"],
        "music_keywords": ["hope", "uplifting", "healing", "gentle"],
        "movie_genres": ["Drama", "Biography", "Documentary"],
        "movie_tone": "uplifting",
        "movie_themes": ["hope", "resilience", "overcoming", "triumph"],
        "movie_keywords": ["inspiring", "hopeful", "uplifting", "resilient"],
        "book_genres": ["Biography", "Self-Help", "Philosophy", "Fiction"],
        "book_themes": ["hope", "resilience", "meaning", "recovery"],
        "book_pacing": "moderate",
        "book_depth": "deep",
        "book_keywords": ["hope", "resilience", "inspiring", "meaning"],
        "avoid_themes": ["despair", "defeat", "dark", "pessimistic"],
        "recommendation_strategy": "uplift"
    },
    
    # ========================================================================
    # ENERGY STATES (8 moods)
    # ========================================================================
    
    "energetic": {
        "music_genres": ["electronic", "rock", "hip hop", "workout", "dance"],
        "music_energy": "very_high",
        "music_vibe": ["energizing", "powerful", "intense", "motivating"],
        "music_keywords": ["workout", "pump up", "energy", "motivation"],
        "movie_genres": ["Action", "Adventure", "Thriller", "Sport"],
        "movie_tone": "intense",
        "movie_themes": ["action", "adventure", "competition", "excitement"],
        "movie_keywords": ["action-packed", "thrilling", "fast-paced", "exciting"],
        "book_genres": ["Thriller", "Action", "Adventure", "Science Fiction"],
        "book_themes": ["action", "adventure", "intensity", "challenge"],
        "book_pacing": "fast",
        "book_depth": "light",
        "book_keywords": ["fast-paced", "action", "thriller", "exciting"],
        "avoid_themes": ["slow", "melancholy", "passive"],
        "recommendation_strategy": "match"
    },
    
    "tired": {
        "music_genres": ["ambient", "lo-fi", "chill", "soft", "calm"],
        "music_energy": "very_low",
        "music_vibe": ["relaxing", "gentle", "soothing", "peaceful"],
        "music_keywords": ["sleep", "rest", "relaxing", "gentle"],
        "movie_genres": ["Animation", "Comedy", "Documentary", "Family"],
        "movie_tone": "light",
        "movie_themes": ["comfort", "simplicity", "ease", "gentle"],
        "movie_keywords": ["easy", "relaxing", "comforting", "light"],
        "book_genres": ["Fiction", "Poetry", "Humor", "Short Stories"],
        "book_themes": ["rest", "comfort", "simplicity", "ease"],
        "book_pacing": "slow",
        "book_depth": "light",
        "book_keywords": ["easy read", "light", "comforting", "short"],
        "avoid_themes": ["intense", "demanding", "complex", "stressful"],
        "recommendation_strategy": "match"
    },
    
    "restless": {
        "music_genres": ["alternative", "indie rock", "electronic", "experimental", "dynamic"],
        "music_energy": "high",
        "music_vibe": ["dynamic", "interesting", "varied", "stimulating"],
        "music_keywords": ["dynamic", "varied", "interesting", "engaging"],
        "movie_genres": ["Thriller", "Mystery", "Science Fiction", "Adventure"],
        "movie_tone": "balanced",
        "movie_themes": ["mystery", "exploration", "intrigue", "discovery"],
        "movie_keywords": ["engaging", "intriguing", "captivating", "mysterious"],
        "book_genres": ["Mystery", "Thriller", "Science Fiction", "Adventure"],
        "book_themes": ["mystery", "exploration", "discovery", "intrigue"],
        "book_pacing": "fast",
        "book_depth": "medium",
        "book_keywords": ["page-turner", "engaging", "intriguing", "captivating"],
        "avoid_themes": ["boring", "predictable", "slow", "mundane"],
        "recommendation_strategy": "channel"
    },
    
    "sluggish": {
        "music_genres": ["chill", "lo-fi", "soft rock", "acoustic", "ambient"],
        "music_energy": "low",
        "music_vibe": ["gentle", "uplifting", "easy", "comforting"],
        "music_keywords": ["easy", "gentle", "uplifting", "comfortable"],
        "movie_genres": ["Comedy", "Animation", "Romance", "Documentary"],
        "movie_tone": "light",
        "movie_themes": ["motivation", "gentle energy", "uplifting", "comfort"],
        "movie_keywords": ["light", "uplifting", "easy", "motivating"],
        "book_genres": ["Fiction", "Self-Help", "Humor", "Graphic Novels"],
        "book_themes": ["motivation", "energy", "simplicity", "inspiration"],
        "book_pacing": "moderate",
        "book_depth": "light",
        "book_keywords": ["motivating", "easy", "uplifting", "energizing"],
        "avoid_themes": ["heavy", "demanding", "dark"],
        "recommendation_strategy": "uplift"
    },
    
    "hyper": {
        "music_genres": ["electronic", "dance", "fast", "intense", "high-energy"],
        "music_energy": "very_high",
        "music_vibe": ["intense", "fast", "energetic", "powerful"],
        "music_keywords": ["high energy", "intense", "fast", "powerful"],
        "movie_genres": ["Action", "Thriller", "Adventure", "Comedy"],
        "movie_tone": "intense",
        "movie_themes": ["action", "excitement", "adventure", "energy"],
        "movie_keywords": ["fast-paced", "intense", "action-packed", "exciting"],
        "book_genres": ["Thriller", "Action", "Science Fiction", "Adventure"],
        "book_themes": ["action", "intensity", "excitement", "speed"],
        "book_pacing": "fast",
        "book_depth": "light",
        "book_keywords": ["fast-paced", "action", "intense", "exciting"],
        "avoid_themes": ["slow", "calm", "boring"],
        "recommendation_strategy": "channel"
    },
    
    "burnt_out": {
        "music_genres": ["ambient", "meditation", "nature sounds", "soft", "healing"],
        "music_energy": "very_low",
        "music_vibe": ["healing", "restorative", "gentle", "peaceful"],
        "music_keywords": ["recovery", "healing", "rest", "restoration"],
        "movie_genres": ["Documentary", "Animation", "Comedy", "Nature"],
        "movie_tone": "light",
        "movie_themes": ["recovery", "rest", "simplicity", "peace"],
        "movie_keywords": ["restorative", "gentle", "peaceful", "healing"],
        "book_genres": ["Self-Help", "Memoir", "Poetry", "Philosophy"],
        "book_themes": ["burnout", "recovery", "balance", "self-care"],
        "book_pacing": "slow",
        "book_depth": "medium",
        "book_keywords": ["burnout", "recovery", "self-care", "healing"],
        "avoid_themes": ["demanding", "stressful", "intense", "work"],
        "recommendation_strategy": "uplift"
    },
    
    "mellow": {
        "music_genres": ["jazz", "chill", "acoustic", "soft rock", "indie"],
        "music_energy": "low",
        "music_vibe": ["relaxed", "smooth", "easy", "comfortable"],
        "music_keywords": ["mellow", "chill", "relaxed", "smooth"],
        "movie_genres": ["Drama", "Romance", "Comedy", "Documentary"],
        "movie_tone": "balanced",
        "movie_themes": ["ease", "comfort", "simplicity", "contentment"],
        "movie_keywords": ["relaxed", "easy", "smooth", "comfortable"],
        "book_genres": ["Fiction", "Poetry", "Essays", "Memoir"],
        "book_themes": ["ease", "reflection", "simplicity", "contentment"],
        "book_pacing": "slow",
        "book_depth": "medium",
        "book_keywords": ["relaxed", "easy", "reflective", "comfortable"],
        "avoid_themes": ["intense", "chaotic", "demanding"],
        "recommendation_strategy": "match"
    },
    
    "drowsy": {
        "music_genres": ["ambient", "sleep", "soft", "meditation", "calm"],
        "music_energy": "very_low",
        "music_vibe": ["soothing", "gentle", "peaceful", "sleepy"],
        "music_keywords": ["sleep", "bedtime", "lullaby", "gentle"],
        "movie_genres": ["Animation", "Documentary", "Nature"],
        "movie_tone": "light",
        "movie_themes": ["peaceful", "gentle", "calming", "simple"],
        "movie_keywords": ["gentle", "soothing", "peaceful", "quiet"],
        "book_genres": ["Poetry", "Short Stories", "Fiction", "Essays"],
        "book_themes": ["peace", "rest", "dreams", "comfort"],
        "book_pacing": "very slow",
        "book_depth": "light",
        "book_keywords": ["bedtime", "gentle", "peaceful", "short"],
        "avoid_themes": ["exciting", "intense", "scary", "stimulating"],
        "recommendation_strategy": "match"
    },
    
    # ========================================================================
    # SOCIAL/RELATIONAL (8 moods)
    # ========================================================================
    
    "social": {
        "music_genres": ["pop", "dance", "party", "funk", "upbeat"],
        "music_energy": "high",
        "music_vibe": ["fun", "celebratory", "energetic", "social"],
        "music_keywords": ["party", "friends", "celebration", "social"],
        "movie_genres": ["Comedy", "Romance", "Drama", "Musical"],
        "movie_tone": "light",
        "movie_themes": ["friendship", "community", "connection", "fun"],
        "movie_keywords": ["fun", "social", "ensemble", "friendship"],
        "book_genres": ["Fiction", "Contemporary", "Humor", "Romance"],
        "book_themes": ["friendship", "social", "community", "connection"],
        "book_pacing": "moderate",
        "book_depth": "light",
        "book_keywords": ["friendship", "social", "relationships", "community"],
        "avoid_themes": ["isolation", "antisocial", "lonely"],
        "recommendation_strategy": "match"
    },
    
    "introverted": {
        "music_genres": ["indie", "acoustic", "lo-fi", "ambient", "soft"],
        "music_energy": "low",
        "music_vibe": ["peaceful", "introspective", "gentle", "calm"],
        "music_keywords": ["alone time", "peaceful", "solitude", "quiet"],
        "movie_genres": ["Drama", "Documentary", "Animation", "Art House"],
        "movie_tone": "balanced",
        "movie_themes": ["solitude", "reflection", "peace", "individual"],
        "movie_keywords": ["quiet", "reflective", "contemplative", "peaceful"],
        "book_genres": ["Fiction", "Philosophy", "Poetry", "Memoir"],
        "book_themes": ["solitude", "reflection", "introspection", "peace"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["introspective", "quiet", "reflective", "solitude"],
        "avoid_themes": ["loud", "social pressure", "chaotic"],
        "recommendation_strategy": "match"
    },
    
    "romantic": {
        "music_genres": ["r&b", "soul", "love songs", "jazz", "acoustic"],
        "music_energy": "low",
        "music_vibe": ["romantic", "intimate", "tender", "warm"],
        "music_keywords": ["love", "romantic", "intimate", "passion"],
        "movie_genres": ["Romance", "Drama", "Comedy"],
        "movie_tone": "light",
        "movie_themes": ["love", "romance", "passion", "connection"],
        "movie_keywords": ["romantic", "heartwarming", "sweet", "loving"],
        "book_genres": ["Romance", "Fiction", "Poetry"],
        "book_themes": ["love", "romance", "passion", "intimacy"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["romantic", "love", "passion", "heartwarming"],
        "avoid_themes": ["heartbreak", "cynical", "bitter"],
        "recommendation_strategy": "match"
    },
    
    "nostalgic": {
        "music_genres": ["classic rock", "oldies", "80s", "90s", "retro"],
        "music_energy": "medium",
        "music_vibe": ["nostalgic", "bittersweet", "reflective", "warm"],
        "music_keywords": ["throwback", "memories", "nostalgia", "classic"],
        "movie_genres": ["Drama", "Comedy", "Family", "Animation"],
        "movie_tone": "balanced",
        "movie_themes": ["memory", "past", "childhood", "coming of age"],
        "movie_keywords": ["nostalgic", "sentimental", "memories", "classic"],
        "book_genres": ["Memoir", "Historical Fiction", "Fiction", "Classic"],
        "book_themes": ["memory", "past", "nostalgia", "time"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["nostalgic", "memories", "past", "reflective"],
        "avoid_themes": ["futuristic", "modern", "cutting-edge"],
        "recommendation_strategy": "match"
    },
    
    "homesick": {
        "music_genres": ["folk", "acoustic", "country", "soft", "comforting"],
        "music_energy": "low",
        "music_vibe": ["comforting", "warm", "familiar", "gentle"],
        "music_keywords": ["home", "comfort", "family", "familiar"],
        "movie_genres": ["Family", "Drama", "Animation", "Comedy"],
        "movie_tone": "light",
        "movie_themes": ["family", "home", "belonging", "comfort"],
        "movie_keywords": ["heartwarming", "family", "comforting", "home"],
        "book_genres": ["Fiction", "Memoir", "Family", "Contemporary"],
        "book_themes": ["home", "family", "belonging", "roots"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["family", "home", "belonging", "comfort"],
        "avoid_themes": ["displacement", "loss", "abandonment"],
        "recommendation_strategy": "process"
    },
    
    "misunderstood": {
        "music_genres": ["alternative", "indie", "emo", "rock", "emotional"],
        "music_energy": "medium",
        "music_vibe": ["emotional", "raw", "authentic", "expressive"],
        "music_keywords": ["misunderstood", "emotional", "authentic", "raw"],
        "movie_genres": ["Drama", "Biography", "Coming-of-Age"],
        "movie_tone": "serious",
        "movie_themes": ["understanding", "acceptance", "identity", "expression"],
        "movie_keywords": ["relatable", "authentic", "emotional", "validating"],
        "book_genres": ["Fiction", "Young Adult", "Memoir", "Psychology"],
        "book_themes": ["understanding", "identity", "acceptance", "expression"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["relatable", "understanding", "identity", "validation"],
        "avoid_themes": ["judgmental", "dismissive", "superficial"],
        "recommendation_strategy": "process"
    },
    
    "betrayed": {
        "music_genres": ["emotional", "alternative", "rock", "raw", "powerful"],
        "music_energy": "medium",
        "music_vibe": ["intense", "emotional", "cathartic", "powerful"],
        "music_keywords": ["betrayal", "hurt", "anger", "healing"],
        "movie_genres": ["Drama", "Thriller"],
        "movie_tone": "dark",
        "movie_themes": ["betrayal", "recovery", "strength", "justice"],
        "movie_keywords": ["intense", "emotional", "cathartic", "powerful"],
        "book_genres": ["Fiction", "Thriller", "Psychology", "Self-Help"],
        "book_themes": ["betrayal", "trust", "healing", "recovery"],
        "book_pacing": "moderate",
        "book_depth": "deep",
        "book_keywords": ["betrayal", "healing", "recovery", "trust"],
        "avoid_themes": ["trust issues", "paranoia"],
        "recommendation_strategy": "process"
    },
    
    "supported": {
        "music_genres": ["uplifting", "soul", "gospel", "indie", "warm"],
        "music_energy": "medium",
        "music_vibe": ["warm", "uplifting", "comforting", "grateful"],
        "music_keywords": ["support", "gratitude", "love", "comfort"],
        "movie_genres": ["Drama", "Family", "Biography", "Comedy"],
        "movie_tone": "uplifting",
        "movie_themes": ["support", "community", "love", "gratitude"],
        "movie_keywords": ["heartwarming", "uplifting", "supportive", "comforting"],
        "book_genres": ["Memoir", "Fiction", "Self-Help", "Biography"],
        "book_themes": ["support", "community", "gratitude", "connection"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["support", "community", "gratitude", "uplifting"],
        "avoid_themes": ["betrayal", "isolation", "abandonment"],
        "recommendation_strategy": "match"
    },
    
    # ========================================================================
    # EXISTENTIAL/REFLECTIVE (8 moods)
    # ========================================================================
    
    "contemplative": {
        "music_genres": ["ambient", "classical", "jazz", "instrumental", "meditative"],
        "music_energy": "low",
        "music_vibe": ["thoughtful", "deep", "peaceful", "reflective"],
        "music_keywords": ["contemplation", "reflection", "thought", "meditation"],
        "movie_genres": ["Drama", "Documentary", "Art House", "Foreign"],
        "movie_tone": "serious",
        "movie_themes": ["reflection", "meaning", "depth", "contemplation"],
        "movie_keywords": ["thought-provoking", "deep", "contemplative", "meaningful"],
        "book_genres": ["Philosophy", "Literary Fiction", "Poetry", "Essays"],
        "book_themes": ["contemplation", "meaning", "reflection", "depth"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["contemplative", "philosophical", "deep", "thoughtful"],
        "avoid_themes": ["superficial", "action-heavy", "shallow"],
        "recommendation_strategy": "match"
    },
    
    "philosophical": {
        "music_genres": ["classical", "ambient", "jazz", "experimental", "avant-garde"],
        "music_energy": "low",
        "music_vibe": ["intellectual", "deep", "complex", "thought-provoking"],
        "music_keywords": ["philosophical", "deep", "intellectual", "complex"],
        "movie_genres": ["Drama", "Science Fiction", "Documentary", "Art House"],
        "movie_tone": "serious",
        "movie_themes": ["existence", "meaning", "philosophy", "consciousness"],
        "movie_keywords": ["philosophical", "profound", "thought-provoking", "deep"],
        "book_genres": ["Philosophy", "Science", "Psychology", "Literary Fiction"],
        "book_themes": ["philosophy", "existence", "meaning", "consciousness"],
        "book_pacing": "slow",
        "book_depth": "profound",
        "book_keywords": ["philosophical", "deep", "meaning", "existence"],
        "avoid_themes": ["simple", "escapist", "superficial"],
        "recommendation_strategy": "match"
    },
    
    "curious": {
        "music_genres": ["world", "jazz", "experimental", "eclectic", "indie"],
        "music_energy": "medium",
        "music_vibe": ["interesting", "diverse", "exploratory", "engaging"],
        "music_keywords": ["discovery", "exploration", "learning", "diverse"],
        "movie_genres": ["Documentary", "Science Fiction", "Mystery", "Adventure"],
        "movie_tone": "balanced",
        "movie_themes": ["discovery", "learning", "exploration", "knowledge"],
        "movie_keywords": ["fascinating", "educational", "intriguing", "discovery"],
        "book_genres": ["Non-fiction", "Science", "History", "Biography"],
        "book_themes": ["curiosity", "discovery", "learning", "knowledge"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["fascinating", "learning", "discovery", "educational"],
        "avoid_themes": ["boring", "dry", "overly technical"],
        "recommendation_strategy": "match"
    },
    
    "confused": {
        "music_genres": ["ambient", "chill", "soft", "calming", "clear"],
        "music_energy": "low",
        "music_vibe": ["calming", "clarifying", "gentle", "peaceful"],
        "music_keywords": ["clarity", "calm", "peaceful", "simple"],
        "movie_genres": ["Drama", "Documentary", "Biography", "Animation"],
        "movie_tone": "balanced",
        "movie_themes": ["clarity", "understanding", "simplicity", "resolution"],
        "movie_keywords": ["clear", "insightful", "understanding", "enlightening"],
        "book_genres": ["Self-Help", "Philosophy", "Fiction", "Psychology"],
        "book_themes": ["clarity", "understanding", "guidance", "insight"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["clarity", "guidance", "understanding", "insight"],
        "avoid_themes": ["complex", "confusing", "ambiguous"],
        "recommendation_strategy": "uplift"
    },
    
    "stuck": {
        "music_genres": ["uplifting", "motivational", "rock", "indie", "inspiring"],
        "music_energy": "medium",
        "music_vibe": ["motivating", "empowering", "uplifting", "moving"],
        "music_keywords": ["breakthrough", "change", "motivation", "movement"],
        "movie_genres": ["Biography", "Drama", "Documentary", "Sport"],
        "movie_tone": "uplifting",
        "movie_themes": ["breakthrough", "change", "transformation", "overcoming"],
        "movie_keywords": ["inspiring", "transformative", "breakthrough", "motivating"],
        "book_genres": ["Self-Help", "Biography", "Psychology", "Business"],
        "book_themes": ["change", "breakthrough", "transformation", "progress"],
        "book_pacing": "moderate",
        "book_depth": "medium",
        "book_keywords": ["breakthrough", "change", "transformation", "unstuck"],
        "avoid_themes": ["stagnation", "hopeless", "trapped"],
        "recommendation_strategy": "uplift"
    },
    
    "purposeful": {
        "music_genres": ["orchestral", "epic", "motivational", "inspiring", "powerful"],
        "music_energy": "high",
        "music_vibe": ["powerful", "purposeful", "determined", "inspiring"],
        "music_keywords": ["purpose", "meaning", "mission", "drive"],
        "movie_genres": ["Biography", "Drama", "Documentary", "History"],
        "movie_tone": "uplifting",
        "movie_themes": ["purpose", "meaning", "mission", "impact"],
        "movie_keywords": ["purposeful", "meaningful", "inspiring", "impactful"],
        "book_genres": ["Biography", "Self-Help", "Philosophy", "Business"],
        "book_themes": ["purpose", "meaning", "mission", "legacy"],
        "book_pacing": "moderate",
        "book_depth": "deep",
        "book_keywords": ["purpose", "meaningful", "mission", "impact"],
        "avoid_themes": ["meaningless", "aimless", "empty"],
        "recommendation_strategy": "match"
    },
    
    "empty": {
        "music_genres": ["ambient", "soft", "healing", "gentle", "hopeful"],
        "music_energy": "low",
        "music_vibe": ["gentle", "healing", "comforting", "filling"],
        "music_keywords": ["healing", "comfort", "hope", "gentle"],
        "movie_genres": ["Drama", "Animation", "Documentary", "Biography"],
        "movie_tone": "balanced",
        "movie_themes": ["healing", "recovery", "hope", "meaning"],
        "movie_keywords": ["healing", "meaningful", "hopeful", "restorative"],
        "book_genres": ["Self-Help", "Philosophy", "Fiction", "Poetry"],
        "book_themes": ["healing", "meaning", "recovery", "fulfillment"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["healing", "meaning", "fulfillment", "hope"],
        "avoid_themes": ["nihilistic", "dark", "hopeless"],
        "recommendation_strategy": "uplift"
    },
    
    "overwhelmed": {
        "music_genres": ["ambient", "meditation", "calm", "peaceful", "simple"],
        "music_energy": "very_low",
        "music_vibe": ["calming", "simplifying", "peaceful", "grounding"],
        "music_keywords": ["calm", "simplicity", "peace", "grounding"],
        "movie_genres": ["Animation", "Comedy", "Documentary", "Nature"],
        "movie_tone": "light",
        "movie_themes": ["simplicity", "peace", "clarity", "calm"],
        "movie_keywords": ["simple", "calming", "peaceful", "gentle"],
        "book_genres": ["Self-Help", "Poetry", "Fiction", "Meditation"],
        "book_themes": ["simplicity", "mindfulness", "calm", "balance"],
        "book_pacing": "slow",
        "book_depth": "light",
        "book_keywords": ["simplicity", "calm", "mindfulness", "peace"],
        "avoid_themes": ["complex", "intense", "demanding", "chaotic"],
        "recommendation_strategy": "uplift"
    },
    
    # ========================================================================
    # TRANSITIONAL/COMPLEX (6 moods)
    # ========================================================================
    
    "bittersweet": {
        "music_genres": ["indie", "folk", "acoustic", "melancholic", "emotional"],
        "music_energy": "low",
        "music_vibe": ["bittersweet", "nostalgic", "emotional", "reflective"],
        "music_keywords": ["bittersweet", "nostalgic", "emotional", "poignant"],
        "movie_genres": ["Drama", "Romance", "Coming-of-Age"],
        "movie_tone": "balanced",
        "movie_themes": ["bittersweet", "nostalgia", "change", "growth"],
        "movie_keywords": ["bittersweet", "poignant", "moving", "emotional"],
        "book_genres": ["Fiction", "Literary Fiction", "Poetry", "Memoir"],
        "book_themes": ["bittersweet", "change", "transition", "nostalgia"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["bittersweet", "poignant", "emotional", "moving"],
        "avoid_themes": ["overly happy", "overly sad", "extreme"],
        "recommendation_strategy": "match"
    },
    
    "numb": {
        "music_genres": ["ambient", "electronic", "post-rock", "atmospheric", "minimal"],
        "music_energy": "low",
        "music_vibe": ["atmospheric", "gentle", "awakening", "stirring"],
        "music_keywords": ["awakening", "gentle", "stirring", "emotional"],
        "movie_genres": ["Drama", "Art House", "Documentary"],
        "movie_tone": "serious",
        "movie_themes": ["awakening", "feeling", "connection", "recovery"],
        "movie_keywords": ["awakening", "stirring", "emotional", "profound"],
        "book_genres": ["Fiction", "Psychology", "Memoir", "Philosophy"],
        "book_themes": ["awakening", "feeling", "recovery", "connection"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["awakening", "emotional", "recovery", "feeling"],
        "avoid_themes": ["intense", "overwhelming", "harsh"],
        "recommendation_strategy": "uplift"
    },
    
    "vengeful": {
        "music_genres": ["rock", "metal", "intense", "powerful", "aggressive"],
        "music_energy": "very_high",
        "music_vibe": ["powerful", "intense", "cathartic", "strong"],
        "music_keywords": ["power", "justice", "strength", "intense"],
        "movie_genres": ["Action", "Thriller", "Drama"],
        "movie_tone": "dark",
        "movie_themes": ["justice", "empowerment", "strength", "overcoming"],
        "movie_keywords": ["powerful", "intense", "justice", "cathartic"],
        "book_genres": ["Thriller", "Fiction", "Psychology", "Self-Help"],
        "book_themes": ["justice", "anger", "healing", "forgiveness"],
        "book_pacing": "fast",
        "book_depth": "medium",
        "book_keywords": ["justice", "empowerment", "healing", "strength"],
        "avoid_themes": ["weak", "passive", "forgiving too quickly"],
        "recommendation_strategy": "channel"
    },
    
    "rebellious": {
        "music_genres": ["punk", "rock", "alternative", "hip hop", "rebellious"],
        "music_energy": "very_high",
        "music_vibe": ["defiant", "powerful", "bold", "liberating"],
        "music_keywords": ["rebellion", "freedom", "defiance", "power"],
        "movie_genres": ["Drama", "Action", "Biography", "Thriller"],
        "movie_tone": "intense",
        "movie_themes": ["rebellion", "freedom", "independence", "justice"],
        "movie_keywords": ["rebellious", "defiant", "liberating", "powerful"],
        "book_genres": ["Fiction", "Biography", "History", "Young Adult"],
        "book_themes": ["rebellion", "freedom", "independence", "defiance"],
        "book_pacing": "fast",
        "book_depth": "medium",
        "book_keywords": ["rebellion", "freedom", "defiance", "independence"],
        "avoid_themes": ["conformity", "submission", "passive"],
        "recommendation_strategy": "channel"
    },
    
    "vulnerable": {
        "music_genres": ["acoustic", "indie", "soft", "intimate", "emotional"],
        "music_energy": "low",
        "music_vibe": ["intimate", "gentle", "tender", "authentic"],
        "music_keywords": ["vulnerable", "honest", "intimate", "authentic"],
        "movie_genres": ["Drama", "Romance", "Biography"],
        "movie_tone": "serious",
        "movie_themes": ["vulnerability", "authenticity", "connection", "courage"],
        "movie_keywords": ["honest", "intimate", "authentic", "tender"],
        "book_genres": ["Memoir", "Fiction", "Poetry", "Self-Help"],
        "book_themes": ["vulnerability", "authenticity", "courage", "openness"],
        "book_pacing": "slow",
        "book_depth": "deep",
        "book_keywords": ["vulnerable", "authentic", "honest", "courage"],
        "avoid_themes": ["harsh", "judgmental", "cold"],
        "recommendation_strategy": "process"
    },
    
    "bored": {
        "music_genres": ["eclectic", "diverse", "experimental", "interesting", "varied"],
        "music_energy": "medium",
        "music_vibe": ["interesting", "engaging", "stimulating", "diverse"],
        "music_keywords": ["interesting", "engaging", "diverse", "stimulating"],
        "movie_genres": ["Mystery", "Thriller", "Science Fiction", "Adventure"],
        "movie_tone": "balanced",
        "movie_themes": ["intrigue", "mystery", "adventure", "discovery"],
        "movie_keywords": ["engaging", "intriguing", "captivating", "exciting"],
        "book_genres": ["Mystery", "Thriller", "Science Fiction", "Adventure"],
        "book_themes": ["mystery", "intrigue", "adventure", "discovery"],
        "book_pacing": "fast",
        "book_depth": "medium",
        "book_keywords": ["engaging", "page-turner", "intriguing", "captivating"],
        "avoid_themes": ["boring", "slow", "predictable", "dull"],
        "recommendation_strategy": "escape"
    },
}


# ============================================================================
# Mood Similarity Mapping
# ============================================================================

MOOD_SIMILARITIES: dict[str, list[str]] = {
    # Positive emotions
    "happy": ["excited", "playful", "content", "grateful"],
    "excited": ["happy", "energetic", "playful", "hyper"],
    "grateful": ["happy", "content", "peaceful", "loving"],
    "peaceful": ["calm", "content", "mellow", "drowsy"],
    "confident": ["proud", "motivated", "purposeful", "empowered"],
    "inspired": ["motivated", "curious", "purposeful", "excited"],
    "playful": ["happy", "excited", "social", "energetic"],
    "content": ["happy", "peaceful", "grateful", "calm"],
    "loving": ["romantic", "grateful", "warm", "affectionate"],
    "proud": ["confident", "happy", "accomplished", "motivated"],
    
    # Negative emotions
    "sad": ["lonely", "heartbroken", "disappointed", "empty"],
    "anxious": ["stressed", "afraid", "overwhelmed", "restless"],
    "stressed": ["anxious", "overwhelmed", "burnt_out", "tired"],
    "angry": ["frustrated", "vengeful", "betrayed", "rebellious"],
    "lonely": ["sad", "homesick", "isolated", "misunderstood"],
    "heartbroken": ["sad", "betrayed", "disappointed", "empty"],
    "disappointed": ["sad", "hopeless", "let_down", "discouraged"],
    "guilty": ["ashamed", "regretful", "embarrassed", "remorseful"],
    "jealous": ["insecure", "envious", "angry", "inadequate"],
    "embarrassed": ["ashamed", "self-conscious", "awkward", "guilty"],
    "afraid": ["anxious", "scared", "worried", "panicked"],
    "hopeless": ["empty", "defeated", "sad", "despair"],
    
    # Energy states
    "energetic": ["excited", "hyper", "motivated", "restless"],
    "tired": ["exhausted", "burnt_out", "sluggish", "drowsy"],
    "restless": ["anxious", "hyper", "bored", "antsy"],
    "sluggish": ["tired", "unmotivated", "low_energy", "mellow"],
    "hyper": ["excited", "energetic", "overstimulated", "restless"],
    "burnt_out": ["tired", "exhausted", "stressed", "depleted"],
    "mellow": ["calm", "relaxed", "peaceful", "content"],
    "drowsy": ["tired", "sleepy", "calm", "peaceful"],
    
    # Social/relational
    "social": ["playful", "happy", "outgoing", "friendly"],
    "introverted": ["contemplative", "peaceful", "alone", "reflective"],
    "romantic": ["loving", "affectionate", "passionate", "tender"],
    "nostalgic": ["bittersweet", "reflective", "sentimental", "wistful"],
    "homesick": ["nostalgic", "lonely", "longing", "missing"],
    "misunderstood": ["lonely", "frustrated", "isolated", "unheard"],
    "betrayed": ["hurt", "angry", "heartbroken", "vengeful"],
    "supported": ["grateful", "loved", "secure", "comforted"],
    
    # Existential/reflective
    "contemplative": ["introspective", "thoughtful", "philosophical", "reflective"],
    "philosophical": ["contemplative", "curious", "deep", "questioning"],
    "curious": ["interested", "engaged", "exploring", "learning"],
    "confused": ["uncertain", "lost", "overwhelmed", "unclear"],
    "stuck": ["frustrated", "stagnant", "trapped", "blocked"],
    "purposeful": ["motivated", "driven", "focused", "meaningful"],
    "empty": ["numb", "hollow", "sad", "unfulfilled"],
    "overwhelmed": ["stressed", "anxious", "drowning", "too_much"],
    
    # Transitional/complex
    "bittersweet": ["nostalgic", "mixed", "poignant", "emotional"],
    "numb": ["empty", "disconnected", "detached", "apathetic"],
    "vengeful": ["angry", "betrayed", "seeking_justice", "hurt"],
    "rebellious": ["defiant", "independent", "free", "bold"],
    "vulnerable": ["exposed", "sensitive", "open", "raw"],
    "bored": ["understimulated", "restless", "need_engagement", "uninterested"],
}

# Opposite moods for uplift strategies
MOOD_OPPOSITES: dict[str, str] = {
    "sad": "happy",
    "angry": "calm",
    "anxious": "peaceful",
    "stressed": "relaxed",
    "tired": "energetic",
    "lonely": "social",
    "hopeless": "inspired",
    "confused": "clear",
    "stuck": "flowing",
    "empty": "fulfilled",
    "bored": "engaged",
    "sluggish": "energetic",
    "overwhelmed": "calm",
    "numb": "feeling",
    "afraid": "confident",
}


# ============================================================================
# Helper Functions
# ============================================================================


def get_mood_mapping(mood: str) -> dict[str, Any] | None:
    """
    Get mood mapping for a given mood with fuzzy matching.
    
    Args:
        mood: The mood to look up (case-insensitive)
        
    Returns:
        Dictionary containing mood mapping, or None if no match found
        
    Examples:
        >>> mapping = get_mood_mapping("happy")
        >>> mapping = get_mood_mapping("happyy")  # Fuzzy match to "happy"
        >>> mapping = get_mood_mapping("unknown")  # Returns None
    """
    mood_lower = mood.lower().strip()
    
    # Exact match (case-insensitive)
    if mood_lower in MOOD_MAPPINGS:
        return MOOD_MAPPINGS[mood_lower].copy()
    
    # Fuzzy matching - find close matches
    available_moods = list(MOOD_MAPPINGS.keys())
    close_matches = get_close_matches(mood_lower, available_moods, n=1, cutoff=0.6)
    
    if close_matches:
        matched_mood = close_matches[0]
        return MOOD_MAPPINGS[matched_mood].copy()
    
    return None


def find_similar_moods(mood: str) -> list[str]:
    """
    Find similar moods for a given mood.
    
    Args:
        mood: The mood to find similarities for
        
    Returns:
        List of similar mood names
        
    Examples:
        >>> similar = find_similar_moods("sad")
        >>> # Returns: ["lonely", "heartbroken", "disappointed", "empty"]
    """
    mood_lower = mood.lower().strip()
    
    # Direct lookup in similarity mapping
    if mood_lower in MOOD_SIMILARITIES:
        return MOOD_SIMILARITIES[mood_lower].copy()
    
    # Try fuzzy match first
    available_moods = list(MOOD_SIMILARITIES.keys())
    close_matches = get_close_matches(mood_lower, available_moods, n=1, cutoff=0.7)
    
    if close_matches:
        return MOOD_SIMILARITIES[close_matches[0]].copy()
    
    return []


def merge_mood_mappings(moods: list[str]) -> dict[str, Any]:
    """
    Merge multiple mood mappings for complex emotional states.
    
    Intelligently combines mappings by:
    - Prioritizing primary mood (first in list) at 60% weight
    - Blending secondary moods at 40% combined weight
    - Averaging numeric values (energy levels)
    - Taking union of genres/keywords with deduplication
    - Using primary mood's tone as default
    
    Args:
        moods: List of mood strings (first is primary)
        
    Returns:
        Merged mapping dictionary
        
    Examples:
        >>> mapping = merge_mood_mappings(["happy", "energetic"])
        >>> mapping = merge_mood_mappings(["sad", "lonely", "tired"])
    """
    if not moods:
        return get_mood_mapping("calm") or {}
    
    if len(moods) == 1:
        return get_mood_mapping(moods[0]) or {}
    
    # Get all valid mappings
    mappings = []
    for mood in moods:
        mapping = get_mood_mapping(mood)
        if mapping:
            mappings.append(mapping)
    
    if not mappings:
        return {}
    
    # Primary mood gets priority
    primary = mappings[0]
    
    # Initialize merged with primary mood's structure
    merged: dict[str, Any] = {
        "music_genres": [],
        "music_energy": primary.get("music_energy", "medium"),
        "music_vibe": [],
        "music_keywords": [],
        "movie_genres": [],
        "movie_tone": primary.get("movie_tone", "balanced"),
        "movie_themes": [],
        "movie_keywords": [],
        "book_genres": [],
        "book_themes": [],
        "book_pacing": primary.get("book_pacing", "moderate"),
        "book_depth": primary.get("book_depth", "medium"),
        "book_keywords": [],
        "avoid_themes": [],
        "recommendation_strategy": primary.get("recommendation_strategy", "match"),
    }
    
    # Collect all values
    all_music_genres = []
    all_music_vibes = []
    all_music_keywords = []
    all_movie_genres = []
    all_movie_themes = []
    all_movie_keywords = []
    all_book_genres = []
    all_book_themes = []
    all_book_keywords = []
    all_avoid_themes = []
    energy_levels = []
    
    for i, mapping in enumerate(mappings):
        # Primary mood gets more weight in selection
        weight = 0.6 if i == 0 else 0.4 / (len(mappings) - 1)
        repetitions = max(1, int(weight * 10))  # Convert weight to repetitions
        
        all_music_genres.extend(mapping.get("music_genres", []) * repetitions)
        all_music_vibes.extend(mapping.get("music_vibe", []) * repetitions)
        all_music_keywords.extend(mapping.get("music_keywords", []) * repetitions)
        all_movie_genres.extend(mapping.get("movie_genres", []) * repetitions)
        all_movie_themes.extend(mapping.get("movie_themes", []) * repetitions)
        all_movie_keywords.extend(mapping.get("movie_keywords", []) * repetitions)
        all_book_genres.extend(mapping.get("book_genres", []) * repetitions)
        all_book_themes.extend(mapping.get("book_themes", []) * repetitions)
        all_book_keywords.extend(mapping.get("book_keywords", []) * repetitions)
        all_avoid_themes.extend(mapping.get("avoid_themes", []))
        
        energy = mapping.get("music_energy", "medium")
        energy_levels.append(energy)
    
    # Remove duplicates while preserving weighted order
    merged["music_genres"] = list(dict.fromkeys(all_music_genres))[:8]
    merged["music_vibe"] = list(dict.fromkeys(all_music_vibes))[:5]
    merged["music_keywords"] = list(dict.fromkeys(all_music_keywords))[:6]
    merged["movie_genres"] = list(dict.fromkeys(all_movie_genres))[:4]
    merged["movie_themes"] = list(dict.fromkeys(all_movie_themes))[:6]
    merged["movie_keywords"] = list(dict.fromkeys(all_movie_keywords))[:5]
    merged["book_genres"] = list(dict.fromkeys(all_book_genres))[:4]
    merged["book_themes"] = list(dict.fromkeys(all_book_themes))[:6]
    merged["book_keywords"] = list(dict.fromkeys(all_book_keywords))[:5]
    merged["avoid_themes"] = list(dict.fromkeys(all_avoid_themes))[:5]
    
    # Calculate weighted average energy level
    energy_map = {"very_low": 1, "low": 2, "medium": 3, "high": 4, "very_high": 5}
    reverse_energy_map = {1: "very_low", 2: "low", 3: "medium", 4: "high", 5: "very_high"}
    avg_energy = sum(energy_map.get(e, 3) for e in energy_levels) / len(energy_levels)
    merged["music_energy"] = reverse_energy_map[round(avg_energy)]
    
    return merged


def get_mood_category(mood: str) -> str:
    """
    Get the category of a given mood.
    
    Args:
        mood: The mood to categorize
        
    Returns:
        Category name: "positive", "negative", "energy", "social", "existential", "complex"
        
    Examples:
        >>> category = get_mood_category("happy")  # Returns "positive"
        >>> category = get_mood_category("anxious")  # Returns "negative"
    """
    categories = {
        "positive": [
            "happy", "excited", "grateful", "peaceful", "confident",
            "inspired", "playful", "content", "loving", "proud"
        ],
        "negative": [
            "sad", "anxious", "stressed", "angry", "lonely", "heartbroken",
            "disappointed", "guilty", "jealous", "embarrassed", "afraid", "hopeless"
        ],
        "energy": [
            "energetic", "tired", "restless", "sluggish", "hyper",
            "burnt_out", "mellow", "drowsy"
        ],
        "social": [
            "social", "introverted", "romantic", "nostalgic", "homesick",
            "misunderstood", "betrayed", "supported"
        ],
        "existential": [
            "contemplative", "philosophical", "curious", "confused",
            "stuck", "purposeful", "empty", "overwhelmed"
        ],
        "complex": [
            "bittersweet", "numb", "vengeful", "rebellious", "vulnerable", "bored"
        ],
    }
    
    mood_lower = mood.lower().strip()
    
    for category, mood_list in categories.items():
        if mood_lower in mood_list:
            return category
    
    # Try fuzzy matching
    mapping = get_mood_mapping(mood_lower)
    if mapping:
        # Re-check with fuzzy matched mood
        for category, mood_list in categories.items():
            for known_mood in mood_list:
                if get_close_matches(mood_lower, [known_mood], n=1, cutoff=0.8):
                    return category
    
    return "unknown"


def get_opposite_mood(mood: str) -> str | None:
    """
    Get the opposite mood for uplift strategies.
    
    Args:
        mood: The mood to find opposite for
        
    Returns:
        Opposite mood name, or None if no opposite defined
        
    Examples:
        >>> opposite = get_opposite_mood("sad")  # Returns "happy"
        >>> opposite = get_opposite_mood("anxious")  # Returns "peaceful"
    """
    mood_lower = mood.lower().strip()
    
    # Direct lookup
    if mood_lower in MOOD_OPPOSITES:
        return MOOD_OPPOSITES[mood_lower]
    
    # Try fuzzy match
    available_moods = list(MOOD_OPPOSITES.keys())
    close_matches = get_close_matches(mood_lower, available_moods, n=1, cutoff=0.8)
    
    if close_matches:
        return MOOD_OPPOSITES[close_matches[0]]
    
    return None


def get_available_moods() -> list[str]:
    """
    Get list of all available moods in the system.
    
    Returns:
        Sorted list of mood names
    """
    return sorted(MOOD_MAPPINGS.keys())


def search_moods_by_category(category: str) -> list[str]:
    """
    Search for moods by category.
    
    Args:
        category: Category to search for
        
    Returns:
        List of moods in that category
    """
    categories = {
        "positive": [
            "happy", "excited", "grateful", "peaceful", "confident",
            "inspired", "playful", "content", "loving", "proud"
        ],
        "negative": [
            "sad", "anxious", "stressed", "angry", "lonely", "heartbroken",
            "disappointed", "guilty", "jealous", "embarrassed", "afraid", "hopeless"
        ],
        "energy": [
            "energetic", "tired", "restless", "sluggish", "hyper",
            "burnt_out", "mellow", "drowsy"
        ],
        "social": [
            "social", "introverted", "romantic", "nostalgic", "homesick",
            "misunderstood", "betrayed", "supported"
        ],
        "existential": [
            "contemplative", "philosophical", "curious", "confused",
            "stuck", "purposeful", "empty", "overwhelmed"
        ],
        "complex": [
            "bittersweet", "numb", "vengeful", "rebellious", "vulnerable", "bored"
        ],
    }
    
    category_lower = category.lower()
    return categories.get(category_lower, [])


def validate_mood_mapping(mood: str) -> bool:
    """
    Check if a mood has a valid mapping.
    
    Args:
        mood: Mood to validate
        
    Returns:
        True if mood has a mapping, False otherwise
    """
    return get_mood_mapping(mood) is not None


# ============================================================================
# Constants for External Use
# ============================================================================

# Energy level constants
ENERGY_VERY_LOW = "very_low"
ENERGY_LOW = "low"
ENERGY_MEDIUM = "medium"
ENERGY_HIGH = "high"
ENERGY_VERY_HIGH = "very_high"

# Tone constants
TONE_LIGHT = "light"
TONE_SERIOUS = "serious"
TONE_BALANCED = "balanced"
TONE_DARK = "dark"
TONE_UPLIFTING = "uplifting"
TONE_INTENSE = "intense"

# Pacing constants
PACING_VERY_SLOW = "very slow"
PACING_SLOW = "slow"
PACING_MODERATE = "moderate"
PACING_FAST = "fast"
PACING_CONTEMPLATIVE = "contemplative"

# Depth constants
DEPTH_LIGHT = "light"
DEPTH_MEDIUM = "medium"
DEPTH_DEEP = "deep"
DEPTH_PROFOUND = "profound"

# Strategy constants
STRATEGY_MATCH = "match"
STRATEGY_UPLIFT = "uplift"
STRATEGY_PROCESS = "process"
STRATEGY_ESCAPE = "escape"
STRATEGY_CHANNEL = "channel"

# All available moods
AVAILABLE_MOODS = get_available_moods()

# Total mood count
TOTAL_MOODS = len(MOOD_MAPPINGS)  # 52 moods
