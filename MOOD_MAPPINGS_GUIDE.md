# MoodMatch Agent - Comprehensive Mood Mappings Guide

## Overview

The MoodMatch agent includes **52 distinct moods** covering the full human emotional spectrum, organized into 6 categories. Each mood is mapped to psychologically-informed media recommendations across music, movies, and books.

## 📊 Mood Categories (52 Total)

### 1. **POSITIVE EMOTIONS** (10 moods)
- `happy` - General happiness and joy
- `excited` - High energy and anticipation
- `grateful` - Thankful and appreciative
- `peaceful` - Serene and tranquil
- `confident` - Self-assured and empowered
- `inspired` - Motivated and creative
- `playful` - Fun-loving and lighthearted
- `content` - Satisfied and comfortable
- `loving` - Affectionate and warm
- `proud` - Accomplished and successful

### 2. **NEGATIVE EMOTIONS** (12 moods)
- `sad` - General sadness and feeling down
- `anxious` - Worried and nervous
- `stressed` - Overwhelmed and pressured
- `angry` - Frustrated and irritated
- `lonely` - Isolated and disconnected
- `heartbroken` - Grief and romantic loss
- `disappointed` - Let down and discouraged
- `guilty` - Remorseful and regretful
- `jealous` - Envious and insecure
- `embarrassed` - Ashamed and self-conscious
- `afraid` - Scared and fearful
- `hopeless` - Despair and defeated

### 3. **ENERGY STATES** (8 moods)
- `energetic` - High energy and pumped
- `tired` - Exhausted and drained
- `restless` - Antsy and can't settle
- `sluggish` - Low motivation and lethargic
- `hyper` - Overstimulated and wired
- `burnt_out` - Depleted and overworked
- `mellow` - Relaxed and easygoing
- `drowsy` - Sleepy and ready for rest

### 4. **SOCIAL/RELATIONAL** (8 moods)
- `social` - Want connection and outgoing
- `introverted` - Need alone time
- `romantic` - Loving and in love
- `nostalgic` - Missing the past
- `homesick` - Longing for home/family
- `misunderstood` - Not heard and frustrated
- `betrayed` - Trust broken and hurt
- `supported` - Cared for and safe

### 5. **EXISTENTIAL/REFLECTIVE** (8 moods)
- `contemplative` - Thoughtful and pondering
- `philosophical` - Questioning and seeking meaning
- `curious` - Want to learn and explore
- `confused` - Uncertain and lost
- `stuck` - Stagnant and trapped
- `purposeful` - Driven and meaningful
- `empty` - Numb and hollow
- `overwhelmed` - Too much and drowning

### 6. **TRANSITIONAL/COMPLEX** (6 moods)
- `bittersweet` - Mixed joy and sadness
- `numb` - Emotionally disconnected
- `vengeful` - Angry and seeking justice
- `rebellious` - Defiant and breaking free
- `vulnerable` - Exposed and sensitive
- `bored` - Understimulated and need engagement

## 🎯 Mapping Structure

Each of the 52 moods includes **15 comprehensive fields**:

```python
{
    # Music Mappings (4 fields)
    "music_genres": list[str],        # 3-5 Spotify genres
    "music_energy": str,              # very_low/low/medium/high/very_high
    "music_vibe": list[str],          # 3-5 vibe descriptors
    "music_keywords": list[str],      # 3-5 search terms
    
    # Movie Mappings (4 fields)
    "movie_genres": list[str],        # 2-4 TMDB genres
    "movie_tone": str,                # light/serious/balanced/dark/uplifting/intense
    "movie_themes": list[str],        # 3-5 thematic elements
    "movie_keywords": list[str],      # 3-5 mood descriptors
    
    # Book Mappings (5 fields)
    "book_genres": list[str],         # 2-4 Google Books categories
    "book_themes": list[str],         # 3-5 thematic elements
    "book_pacing": str,               # fast/moderate/slow/contemplative/very slow
    "book_depth": str,                # light/medium/deep/profound
    "book_keywords": list[str],       # 3-5 search terms
    
    # Strategy (2 fields)
    "avoid_themes": list[str],        # 2-4 themes to avoid
    "recommendation_strategy": str    # match/uplift/process/escape/channel
}
```

## 🛠️ Helper Functions

### Core Functions

#### `get_mood_mapping(mood: str) -> dict | None`
Get mood mapping with fuzzy matching support.

```python
from config import get_mood_mapping

# Exact match
mapping = get_mood_mapping("happy")

# Fuzzy match (handles typos)
mapping = get_mood_mapping("happyy")  # Matches to "happy"

# Returns None if no match
mapping = get_mood_mapping("unknown")  # None
```

#### `find_similar_moods(mood: str) -> list[str]`
Find similar moods for better recommendations.

```python
from config import find_similar_moods

similar = find_similar_moods("sad")
# Returns: ["lonely", "heartbroken", "disappointed", "empty"]
```

#### `merge_mood_mappings(moods: list[str]) -> dict`
Intelligently combine multiple moods (primary mood weighted 60%).

```python
from config import merge_mood_mappings

# Multi-mood handling
mapping = merge_mood_mappings(["sad", "lonely", "tired"])

# Primary mood (first) gets priority
mapping = merge_mood_mappings(["happy", "excited"])
```

#### `get_mood_category(mood: str) -> str`
Get category for a mood.

```python
from config import get_mood_category

category = get_mood_category("happy")  # "positive"
category = get_mood_category("anxious")  # "negative"
category = get_mood_category("energetic")  # "energy"
```

#### `get_opposite_mood(mood: str) -> str | None`
Get opposite mood for uplift strategies.

```python
from config import get_opposite_mood

opposite = get_opposite_mood("sad")  # "happy"
opposite = get_opposite_mood("anxious")  # "peaceful"
opposite = get_opposite_mood("tired")  # "energetic"
```

### Utility Functions

#### `get_available_moods() -> list[str]`
Returns all 52 available moods (sorted).

#### `search_moods_by_category(category: str) -> list[str]`
Filter moods by category.

```python
from config import search_moods_by_category

positive_moods = search_moods_by_category("positive")
negative_moods = search_moods_by_category("negative")
energy_moods = search_moods_by_category("energy")
```

#### `validate_mood_mapping(mood: str) -> bool`
Check if a mood has a valid mapping.

## 🎼 Music Energy Levels

- **very_low** - Sleep, deep rest, meditation
- **low** - Relaxing, calming, gentle
- **medium** - Balanced, comfortable, moderate
- **high** - Energizing, upbeat, motivating
- **very_high** - Intense, powerful, explosive

## 🎬 Movie Tones

- **light** - Easy, fun, undemanding
- **serious** - Thoughtful, deep, meaningful
- **balanced** - Mix of light and serious
- **dark** - Intense, heavy, challenging
- **uplifting** - Inspiring, hopeful, motivating
- **intense** - Action-packed, thrilling, powerful

## 📚 Book Pacing

- **very slow** - Bedtime, gentle, minimal
- **slow** - Contemplative, meditative, peaceful
- **moderate** - Balanced, comfortable reading
- **fast** - Page-turner, exciting, engaging
- **contemplative** - Deep reflection, thoughtful

## 📖 Book Depth

- **light** - Easy read, entertainment, fun
- **medium** - Some depth, relatable, engaging
- **deep** - Meaningful, thought-provoking, complex
- **profound** - Philosophical, existential, transformative

## 🎯 Recommendation Strategies

1. **match** - Validate current mood (e.g., sad music for sad mood)
2. **uplift** - Gradually lift mood (e.g., calm content for anxiety)
3. **process** - Help process emotions (e.g., cathartic content)
4. **escape** - Distract from mood (e.g., adventure for boredom)
5. **channel** - Redirect energy (e.g., action for restlessness)

## 🧠 Psychological Design Principles

### Mood Matching vs. Mood Shifting

- **Validation First**: Allow emotional processing before shifting
- **Gradual Transitions**: Don't jump from sad to happy too quickly
- **Contextual Appropriateness**: Consider time of day and consumption type
- **Cultural Sensitivity**: Avoid harmful or triggering content

### Multi-Mood Handling

When users express multiple moods:
1. **Primary mood** (first) gets 60% weight
2. **Secondary moods** share remaining 40%
3. Energy levels are averaged
4. Genres/themes are merged with deduplication
5. Avoid themes are combined

### Time-Based Considerations

- **Music**: Instant mood regulation
- **Movies**: Evening consumption (2-3 hours)
- **Books**: Extended engagement (days/weeks)

## 📦 Constants Available

```python
from config import (
    # Energy levels
    ENERGY_VERY_LOW, ENERGY_LOW, ENERGY_MEDIUM, ENERGY_HIGH, ENERGY_VERY_HIGH,
    
    # Tones
    TONE_LIGHT, TONE_SERIOUS, TONE_BALANCED, TONE_DARK, TONE_UPLIFTING, TONE_INTENSE,
    
    # Pacing
    PACING_VERY_SLOW, PACING_SLOW, PACING_MODERATE, PACING_FAST, PACING_CONTEMPLATIVE,
    
    # Depth
    DEPTH_LIGHT, DEPTH_MEDIUM, DEPTH_DEEP, DEPTH_PROFOUND,
    
    # Strategies
    STRATEGY_MATCH, STRATEGY_UPLIFT, STRATEGY_PROCESS, STRATEGY_ESCAPE, STRATEGY_CHANNEL,
    
    # Metadata
    AVAILABLE_MOODS,  # List of all 52 moods
    TOTAL_MOODS,      # 52
)
```

## 💡 Usage Examples

### Basic Mood Lookup

```python
from config import get_mood_mapping

# Get recommendations for a happy mood
mapping = get_mood_mapping("happy")
print(mapping["music_genres"])  # ["upbeat pop", "indie pop", "dance", ...]
print(mapping["movie_tone"])    # "light"
print(mapping["recommendation_strategy"])  # "match"
```

### Complex Multi-Mood Scenario

```python
from config import merge_mood_mappings, get_mood_category

# User feels "sad, tired, and lonely"
moods = ["sad", "tired", "lonely"]
combined = merge_mood_mappings(moods)

# Get category for each mood
for mood in moods:
    category = get_mood_category(mood)
    print(f"{mood} is {category}")
```

### Uplift Strategy

```python
from config import get_mood_mapping, get_opposite_mood

# User is anxious
current_mood = "anxious"
target_mood = get_opposite_mood(current_mood)  # "peaceful"

# Get calming recommendations
anxious_mapping = get_mood_mapping(current_mood)
print(anxious_mapping["recommendation_strategy"])  # "uplift"
print(anxious_mapping["music_keywords"])  # ["anxiety relief", "calming", ...]
```

### Mood Discovery

```python
from config import search_moods_by_category, find_similar_moods

# Explore positive moods
positive = search_moods_by_category("positive")
print(f"Found {len(positive)} positive moods: {positive}")

# Find similar moods
similar_to_happy = find_similar_moods("happy")
print(f"Similar to happy: {similar_to_happy}")
```

## 🔍 API Integration Ready

All mappings are optimized for:
- **Spotify API**: Genre and keyword search
- **TMDB API**: Genre filtering and keyword discovery
- **Google Books API**: Category and keyword search

The mappings provide production-ready search terms and filters that work directly with these APIs.

## 📈 Coverage Statistics

- **Total Moods**: 52
- **Categories**: 6
- **Fields per Mood**: 15
- **Average Genres per Mood**: 4-5
- **Average Keywords per Mood**: 4-5
- **Total Mapping Entries**: 780+ (52 × 15)

## 🎨 Customization

The mappings are designed to be extensible:

1. Add new moods to `MOOD_MAPPINGS`
2. Update `MOOD_SIMILARITIES` for relationships
3. Add opposite pairs to `MOOD_OPPOSITES`
4. Update category mappings in helper functions

---

**Built for**: MoodMatch A2A Agent  
**Version**: 1.0  
**Last Updated**: October 31, 2025  
**Python**: 3.13+
