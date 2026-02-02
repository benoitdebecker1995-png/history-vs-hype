# Phase 20 Research: Pattern Extraction

**Phase:** 20-pattern-extraction
**Goal:** System identifies "winning patterns" from top performers
**Research Date:** 2026-02-02

## Requirements Analysis

| Requirement | Description |
|-------------|-------------|
| PATN-01 | System extracts "winning pattern" profile from top-performing videos |
| PATN-02 | System identifies channel strengths (document-heavy, academic, legal/territorial) |
| PATN-03 | System tracks what attributes top converters share |

## Existing Codebase Analysis

### Phase 19 Foundation (video_performance table)

**Available from Phase 19:**
- `performance.py` - Fetcher with `classify_topic_type()`, `classify_own_video()`
- `performance_report.py` - Report generator with `aggregate_by_topic()`, `aggregate_by_angle()`
- `database.py` - KeywordDB with 7 performance methods:
  - `get_top_converters(limit)` - Videos sorted by conversion_rate DESC
  - `get_all_video_performance(limit)` - All video records
  - `get_performance_by_topic(topic_type)` - Filter by topic
  - `get_performance_by_angle(angle)` - Filter by angle (JSON search)
  - `add_video_performance(...)` - Insert/update records

**Data available per video:**
```python
{
    'video_id': str,
    'title': str,
    'views': int,
    'subscribers_gained': int,
    'subscribers_lost': int,
    'conversion_rate': float,  # (subs/views)*100
    'watch_time_minutes': float,
    'avg_view_duration_seconds': int,
    'likes': int,
    'comments': int,
    'shares': int,
    'topic_type': str,  # territorial, ideological, colonial, etc.
    'angles': List[str],  # [legal, historical, geographic, etc.]
    'fetched_at': str
}
```

### Classification System (Phase 16)

**Available classifiers:**
- `classify_format(title, channel_name)` - animation/documentary/unknown
- `classify_angles(title)` - [political, legal, historical, economic, geographic]

**Topic vocabulary from performance.py/patterns.py:**
```python
TAG_VOCABULARY = {
    'territorial': ['dispute', 'border', 'territory', 'claim', 'annex', 'occupation', 'icj', 'sovereignty'],
    'ideological': ['myth', 'debunk', 'fact-check', 'propaganda', 'narrative', 'lie'],
    'colonial': ['colonial', 'empire', 'independence', 'decolonization', 'imperial'],
    'politician': ['vance', 'netanyahu', 'trump', 'fuentes', 'reagan', 'politician'],
    'archaeological': ['dna', 'excavation', 'artifact', 'manuscript', 'archaeology'],
    'medieval': ['medieval', 'dark ages', 'crusade', 'viking', 'middle ages'],
    'legal': ['treaty', 'court', 'icj', 'ruling', 'law', 'sovereignty', 'referendum'],
}
```

### Channel Context (from CLAUDE.md)

**Known channel strengths:**
- Document-heavy format (primary sources on screen)
- Academic sourcing (university press, real quotes with page numbers)
- Legal/territorial angles (ICJ cases, treaty analysis, border disputes)
- History-first framing (not news-first)

**Best performers (VidIQ validated):**
- Territorial disputes: 12x baseline performance
- Map-focused thumbnails: 26x better than face-focused
- Legal angle: correlates with strong conversion

## What "Winning Pattern" Means

A winning pattern profile should answer:
1. **What topic types convert best?** (territorial > ideological > colonial)
2. **What angles correlate with high conversion?** (legal > historical > political)
3. **What attributes do top 5-10 videos share?** (duration, topic, angles, engagement)
4. **What is the channel's competitive advantage?** (document-heavy, academic sourcing)

### Pattern Profile Structure

```python
{
    'extracted_at': '2026-02-02T12:00:00Z',
    'videos_analyzed': 20,

    # Topic performance ranking
    'topic_ranking': [
        {'topic': 'territorial', 'avg_conversion': 0.85, 'count': 5},
        {'topic': 'colonial', 'avg_conversion': 0.62, 'count': 3},
        # ...
    ],

    # Angle performance ranking
    'angle_ranking': [
        {'angle': 'legal', 'avg_conversion': 0.92, 'count': 4},
        {'angle': 'historical', 'avg_conversion': 0.71, 'count': 8},
        # ...
    ],

    # Shared attributes among top N converters
    'top_converter_profile': {
        'n': 5,
        'dominant_topic': 'territorial',  # Most common topic
        'dominant_angles': ['legal', 'historical'],  # Top 2 angles
        'avg_duration_seconds': 720,
        'avg_views': 8500,
        'avg_likes_per_view': 0.04,
        'avg_comments_per_view': 0.002,
    },

    # Channel strength scores (0-100)
    'channel_strengths': {
        'document_heavy': 85,  # Based on topic/angle distribution
        'academic': 90,  # Based on performance of fact-check content
        'legal_territorial': 95,  # Based on legal + territorial performance
    },

    # Actionable insights
    'insights': [
        'Territorial topics convert 1.4x better than average',
        'Legal angle correlates with 23% higher conversion',
        'Top 5 converters share legal + territorial combination',
    ]
}
```

## Technical Approach

### Step 1: Extract Pattern from Database

Use existing Phase 19 data:
```python
from database import KeywordDB
db = KeywordDB()

# Get all performance data
all_videos = db.get_all_video_performance(limit=500)

# Get top converters
top_n = db.get_top_converters(limit=10)

# Aggregate by topic/angle (from performance_report.py)
topic_stats = aggregate_by_topic(all_videos, min_count=1)
angle_stats = aggregate_by_angle(all_videos, min_count=1)
```

### Step 2: Identify Channel Strengths

Calculate strength scores based on:
1. **Document-heavy:** Proportion of videos with legal/historical angles
2. **Academic:** Proportion of ideological (fact-check/myth) content
3. **Legal/territorial:** Performance of legal + territorial topics vs others

```python
def calculate_strength_scores(topic_stats, angle_stats):
    """Calculate channel strength scores 0-100."""

    # Document-heavy: legal + historical angle prevalence and performance
    legal_perf = angle_stats.get('legal', {}).get('avg_conversion_rate', 0)
    hist_perf = angle_stats.get('historical', {}).get('avg_conversion_rate', 0)
    avg_all = mean([s['avg_conversion_rate'] for s in angle_stats.values()])
    document_heavy = min(100, ((legal_perf + hist_perf) / 2 / avg_all) * 50)

    # Similar calculations for academic and legal_territorial
    # ...
```

### Step 3: Generate Profile Report

Output as markdown saved to `channel-data/patterns/WINNING-PATTERNS.md`:
- Summary of top topics by conversion
- Summary of top angles by conversion
- Top converter profile (shared attributes)
- Channel strength assessment
- Actionable recommendations

### Step 4: CLI Integration

Add to performance.py:
```bash
python performance.py --patterns           # Extract and show winning patterns
python performance.py --patterns --save    # Extract and save to file
python performance.py --strengths          # Show channel strength scores
```

## Implementation Tasks

### Task 1: Pattern Extractor Module

Create `tools/youtube-analytics/pattern_extractor.py`:
- `extract_topic_ranking(videos)` - Rank topics by conversion
- `extract_angle_ranking(videos)` - Rank angles by conversion
- `extract_top_converter_profile(top_n)` - Common attributes
- `calculate_channel_strengths(topic_stats, angle_stats)` - Strength scores
- `generate_insights(profile)` - Actionable insight strings
- `generate_winning_patterns_report()` - Full markdown report

### Task 2: CLI Integration + Report Generation

Extend `performance.py` CLI:
- `--patterns` flag to show/save winning patterns
- `--strengths` flag to show channel strength scores
- Integration with existing `--report` output

## Data Flow

```
video_performance table (Phase 19)
        |
        v
pattern_extractor.py (Phase 20 - NEW)
  - extract_topic_ranking()
  - extract_angle_ranking()
  - extract_top_converter_profile()
  - calculate_channel_strengths()
        |
        v
WINNING-PATTERNS.md (output)
  - Topic ranking
  - Angle ranking
  - Top converter profile
  - Channel strengths
  - Insights
```

## Dependencies

- Phase 19 complete (video_performance table, performance.py, performance_report.py)
- User has run `python performance.py --fetch-all` to populate database
- At least 5-10 videos with performance data for meaningful patterns

## Discovery Level

**Level 0 - Skip**

Rationale:
- All work follows established codebase patterns
- Uses existing Phase 19 infrastructure
- No new external dependencies
- Pure internal feature extension

## Estimated Scope

- 1 plan
- 2-3 tasks
- ~40% context (moderate complexity, building on Phase 19)
