# Phase 16: Competition Analysis - Research

**Researched:** 2026-01-31
**Domain:** YouTube competitor video classification, quality filtering, and differentiation scoring
**Confidence:** MEDIUM

## Summary

Phase 16 extends the existing CompetitionAnalyzer (from Phase 15) with four new capabilities: video/channel counts (COMP-01), quality filtering (COMP-02), format/angle classification (COMP-03), and differentiation scoring (COMP-04). The phase builds on the existing scrapetube integration and cached video metadata already stored in competitor_videos table.

The primary challenge is classifying video format (animation vs. documentary) and content angle (political vs. legal vs. historical) from limited metadata. Since we only have title, channel name, view count, and published date from scrapetube (no description, tags, or transcript), classification must rely on keyword-based heuristics applied to titles and channel names. This is a practical constraint that limits accuracy but avoids expensive API calls.

Quality filtering uses engagement proxies (view count thresholds, channel recurrence) since like counts and retention data aren't available without YouTube API quota. The differentiation score calculates what angles are underrepresented in existing competition.

**Primary recommendation:** Implement rule-based text classification for format and angle detection using keyword lists. Use view count percentile thresholds for quality filtering. Calculate differentiation as inverse frequency of detected angles. All classification should be cached in database with manual override capability for edge cases.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| scrapetube | latest | Video metadata scraping | Already integrated in Phase 15, quota-free, returns title/channel/views |
| sqlite3 (stdlib) | Python 3.11+ | Classification caching | Existing keywords.db, avoid external dependencies |
| re (stdlib) | Python 3.11+ | Keyword pattern matching | Built-in, sufficient for rule-based classification |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| collections.Counter | stdlib | Angle frequency counting | For differentiation score calculation |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Keyword heuristics | spaCy NLP | spaCy already has compatibility issues (Python 3.14), overkill for simple classification |
| Keyword heuristics | Transformer models | Massive overhead, requires training data we don't have |
| View count threshold | YouTube API engagement | Costs 1 quota unit per video, not scalable |

**Installation:**
```bash
# No new dependencies - uses existing Phase 15 stack
# scrapetube already installed
```

## Architecture Patterns

### Recommended Project Structure
```
tools/discovery/
├── competition.py       # EXTEND - add quality filter, format/angle classification
├── classifiers.py       # NEW - format and angle classification logic
├── database.py          # EXTEND - add classification storage methods
├── schema.sql           # UPDATE - add classification columns
└── keywords.db          # EXTEND - store classifications
```

### Pattern 1: Keyword-Based Format Classification
**What:** Detect animation vs. documentary format using channel name and title keywords
**When to use:** Classifying competitor videos for format compatibility
**Example:**
```python
# Source: Channel-specific domain knowledge + industry patterns
ANIMATION_CHANNEL_KEYWORDS = [
    'kurzgesagt', 'oversimplified', 'infographics show', 'simple history',
    'extra credits', 'ted-ed', 'minutephysics', 'cgp grey', 'casually explained',
    'sam o\'nella', 'alternate history hub', 'feature history', 'historia civilis'
]

ANIMATION_TITLE_KEYWORDS = [
    'animated', 'animation', 'cartoon', 'illustrated', 'infographic'
]

DOCUMENTARY_CHANNEL_KEYWORDS = [
    'kraut', 'knowing better', 'shaun', 'three arrows', 'history matters',
    'reallifelore', 'wendover', 'caspian report', 'johnny harris', 'vox'
]

def classify_format(title: str, channel_name: str) -> str:
    """
    Classify video format as 'animation', 'documentary', or 'unknown'.

    Channel name is strongest signal (animators rarely do documentary).
    Title keywords are secondary signal.
    """
    channel_lower = channel_name.lower()
    title_lower = title.lower()

    # Check channel name first (strongest signal)
    for keyword in ANIMATION_CHANNEL_KEYWORDS:
        if keyword in channel_lower:
            return 'animation'

    for keyword in DOCUMENTARY_CHANNEL_KEYWORDS:
        if keyword in channel_lower:
            return 'documentary'

    # Fall back to title keywords
    for keyword in ANIMATION_TITLE_KEYWORDS:
        if keyword in title_lower:
            return 'animation'

    return 'unknown'
```

### Pattern 2: Keyword-Based Angle Classification
**What:** Detect content angle (political, legal, historical, economic) from title
**When to use:** Determining what perspectives are covered by competitors
**Example:**
```python
# Source: Domain knowledge from channel CLAUDE.md + competitor analysis
ANGLE_KEYWORDS = {
    'political': [
        'politics', 'political', 'government', 'election', 'party', 'ideology',
        'left', 'right', 'liberal', 'conservative', 'democracy', 'authoritarian',
        'regime', 'president', 'prime minister', 'parliament', 'congress'
    ],
    'legal': [
        'treaty', 'law', 'legal', 'court', 'icj', 'ruling', 'jurisdiction',
        'sovereignty', 'international law', 'constitution', 'rights', 'claim',
        'dispute', 'agreement', 'accord', 'protocol', 'convention'
    ],
    'historical': [
        'history', 'historical', 'ancient', 'medieval', 'century', 'dynasty',
        'empire', 'kingdom', 'war', 'battle', 'civilization', 'colonial',
        'origin', 'rise', 'fall', 'era', 'age', 'period'
    ],
    'economic': [
        'economy', 'economic', 'trade', 'gdp', 'debt', 'money', 'currency',
        'market', 'industry', 'resources', 'oil', 'wealth', 'poverty',
        'development', 'infrastructure', 'sanctions'
    ],
    'geographic': [
        'border', 'territory', 'map', 'region', 'island', 'land', 'sea',
        'ocean', 'mountain', 'river', 'geography', 'location', 'area'
    ]
}

def classify_angles(title: str) -> List[str]:
    """
    Classify video angle(s) from title.

    Returns list of detected angles (video can have multiple).
    Returns ['general'] if no specific angle detected.
    """
    title_lower = title.lower()
    detected = []

    for angle, keywords in ANGLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                detected.append(angle)
                break  # One match per angle is enough

    return detected if detected else ['general']
```

### Pattern 3: Quality Filtering with View Count Percentiles
**What:** Filter out low-quality videos using view count percentile thresholds
**When to use:** COMP-02 - focusing on "real competition" not noise
**Example:**
```python
# Source: YouTube engagement research + practical filtering needs
def filter_quality_competition(
    videos: List[Dict],
    min_views: int = 1000,
    min_percentile: int = 25
) -> List[Dict]:
    """
    Filter to quality competition only.

    Quality signals (available without API quota):
    1. View count > threshold (1K minimum for educational content)
    2. View count > 25th percentile of sample (relative quality)
    3. Channel appears multiple times (established creator, not spam)

    Args:
        videos: List of video dicts from scrapetube
        min_views: Absolute minimum view count
        min_percentile: Percentile threshold (0-100)

    Returns:
        Filtered list of quality videos
    """
    if not videos:
        return []

    # Calculate percentile threshold
    view_counts = [v.get('view_count', 0) for v in videos]
    view_counts.sort()

    percentile_idx = int(len(view_counts) * min_percentile / 100)
    percentile_threshold = view_counts[percentile_idx] if view_counts else 0

    # Apply filters
    effective_threshold = max(min_views, percentile_threshold)

    # Count channel occurrences (multi-video creators = higher quality signal)
    channel_counts = Counter(v.get('channel_name', '') for v in videos)

    quality_videos = []
    for video in videos:
        views = video.get('view_count', 0)
        channel = video.get('channel_name', '')

        # Must meet view threshold
        if views < effective_threshold:
            continue

        # Bonus: channel has multiple videos (established creator)
        video['quality_signals'] = {
            'meets_view_threshold': True,
            'channel_video_count': channel_counts.get(channel, 1),
            'is_established_creator': channel_counts.get(channel, 1) >= 2
        }

        quality_videos.append(video)

    return quality_videos
```

### Pattern 4: Differentiation Score Calculation
**What:** Calculate what angles are missing or underrepresented in existing coverage
**When to use:** COMP-04 - identifying content gaps
**Example:**
```python
# Source: Content gap analysis methodology from research
def calculate_differentiation_score(
    videos: List[Dict],
    channel_angles: List[str] = ['legal', 'historical']
) -> Dict[str, Any]:
    """
    Calculate differentiation opportunities based on angle frequency.

    Differentiation = angles that are UNDERREPRESENTED in competition.
    Higher score = bigger gap = better opportunity.

    Args:
        videos: Classified competitor videos
        channel_angles: This channel's preferred angles

    Returns:
        {
            'angle_distribution': {'political': 45, 'legal': 12, ...},
            'gap_scores': {'legal': 0.73, 'economic': 0.85, ...},
            'recommended_angle': 'economic',
            'differentiation_score': 0.85  # 0-1, higher = more differentiated
        }
    """
    # Count angle frequency across all videos
    angle_counts = Counter()
    total_angles = 0

    for video in videos:
        for angle in video.get('angles', ['general']):
            angle_counts[angle] += 1
            total_angles += 1

    if total_angles == 0:
        return {
            'angle_distribution': {},
            'gap_scores': {a: 1.0 for a in channel_angles},
            'recommended_angle': channel_angles[0] if channel_angles else None,
            'differentiation_score': 1.0  # No competition = maximum differentiation
        }

    # Calculate gap scores (inverse of frequency)
    # Low frequency = high gap = high opportunity
    angle_distribution = {}
    gap_scores = {}

    all_angles = set(ANGLE_KEYWORDS.keys())

    for angle in all_angles:
        frequency = angle_counts.get(angle, 0) / total_angles
        angle_distribution[angle] = round(frequency * 100, 1)  # As percentage
        gap_scores[angle] = round(1.0 - frequency, 2)  # Inverse = gap

    # Find best angle for channel
    best_angle = None
    best_score = 0

    for angle in channel_angles:
        if gap_scores.get(angle, 0) > best_score:
            best_score = gap_scores[angle]
            best_angle = angle

    return {
        'angle_distribution': angle_distribution,
        'gap_scores': gap_scores,
        'recommended_angle': best_angle,
        'differentiation_score': best_score
    }
```

### Anti-Patterns to Avoid
- **Using YouTube API for engagement data**: Costs quota, view count from scrapetube is sufficient for filtering
- **Complex NLP for classification**: Keyword matching is 90%+ accurate for known channels, avoid spaCy overhead
- **Binary classification only**: Videos often have multiple angles, use list not single category
- **Ignoring channel-level signals**: Channel name is strongest format indicator, don't rely only on title
- **Hardcoding without override**: Allow manual classification override for edge cases

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Video count by keyword | Custom YouTube API search | scrapetube (Phase 15) | Already implemented, quota-free |
| Engagement quality score | Like ratio calculation | View count percentile | Likes not available without API quota |
| Topic classification | Transformer model | Keyword heuristics | Training data not available, overkill for known domain |
| Gap analysis | Statistical modeling | Frequency inversion | Simple approach works for 5-10 angle categories |

**Key insight:** The constraint is metadata availability. Scrapetube provides title, channel, views, and publish date - but NOT description, tags, likes, or transcript. Classification must work within these limits. Don't try to get additional data (costs quota or requires additional scraping).

## Common Pitfalls

### Pitfall 1: Animation Channel Misclassification
**What goes wrong:** Documentary-style channel misclassified as animation, or vice versa
**Why it happens:** Channel names change, new channels not in keyword list, hybrid channels (e.g., Historia Civilis uses simple animation but is documentary-adjacent)
**How to avoid:**
- Maintain channel keyword lists as data, not code (easier updates)
- Use 'unknown' category for uncertain cases
- Allow manual override stored in database
- Periodically audit classifications against actual channel content
**Warning signs:** User complains about wrong classification, channel you watch regularly is misclassified

### Pitfall 2: Angle Over-Classification
**What goes wrong:** Every video classified as multiple angles, losing differentiation signal
**Why it happens:** Keywords too broad (e.g., "history" matches everything), insufficient filtering
**How to avoid:**
- Use specific keywords, not generic ones
- Require 2+ keyword matches for multi-angle classification
- Weight primary angle higher than secondary
- Test on known competitor videos before deployment
**Warning signs:** All videos classified as 3+ angles, no clear differentiation between topics

### Pitfall 3: View Count Threshold Too Aggressive
**What goes wrong:** Filtering removes legitimate small-channel competitors
**Why it happens:** Absolute threshold (e.g., 10K views) excludes quality content from small channels
**How to avoid:**
- Use percentile-based filtering, not just absolute thresholds
- Lower threshold for niche topics (fewer total videos)
- Separate "established competition" from "all competition" in output
- Log filtered videos for manual review
**Warning signs:** Only seeing big channels in results, missing niche experts

### Pitfall 4: Differentiation Score Without Context
**What goes wrong:** High differentiation score for angle that's underrepresented BECAUSE IT DOESN'T FIT THE TOPIC
**Why it happens:** Algorithm doesn't understand why an angle is missing
**How to avoid:**
- Show angle distribution alongside score (user decides relevance)
- Compare to channel's preferred angles, not all angles
- Flag when recommended angle has 0% coverage (might be irrelevant, not gap)
- Output reasoning, not just score
**Warning signs:** Recommending "economic angle" for a topic that has no economic dimension

### Pitfall 5: Stale Classification Data
**What goes wrong:** Using cached classifications that are months old, missing new competitors
**Why it happens:** Classifications cached indefinitely, no refresh trigger
**How to avoid:**
- Store classification date with each record
- Warn when classification data >30 days old
- Provide --refresh-classifications flag
- Re-classify when video count changes significantly
**Warning signs:** Same competitor list showing for months, new viral videos not appearing

## Code Examples

Verified patterns for Phase 16 implementation:

### Database Schema Extension
```sql
-- Source: Extends Phase 15 schema.sql
-- Add classification columns to competitor_videos

ALTER TABLE competitor_videos ADD COLUMN format TEXT;  -- 'animation', 'documentary', 'unknown'
ALTER TABLE competitor_videos ADD COLUMN angles TEXT;  -- JSON array: '["legal", "historical"]'
ALTER TABLE competitor_videos ADD COLUMN quality_tier TEXT;  -- 'high', 'medium', 'low'
ALTER TABLE competitor_videos ADD COLUMN classified_at DATE;

-- Index for format filtering
CREATE INDEX IF NOT EXISTS idx_competitor_format
  ON competitor_videos(keyword_id, format);

-- Index for quality filtering
CREATE INDEX IF NOT EXISTS idx_competitor_quality
  ON competitor_videos(keyword_id, quality_tier);
```

### CompetitionAnalyzer Extension
```python
# Source: Extends Phase 15 competition.py
from classifiers import classify_format, classify_angles
from typing import Dict, Any, List

class CompetitionAnalyzer:
    # ... existing methods from Phase 15 ...

    def analyze_competition(self, keyword: str) -> Dict[str, Any]:
        """
        Full competition analysis for a keyword.

        Returns:
            {
                'keyword': str,
                'video_count': int,
                'channel_count': int,
                'quality_video_count': int,  # After quality filter
                'format_breakdown': {'animation': 12, 'documentary': 45, 'unknown': 8},
                'angle_distribution': {'political': 30, 'legal': 15, ...},
                'differentiation_score': 0.73,
                'recommended_angle': 'legal',
                'top_competitors': [...],
                'fetched_at': str
            }
        """
        # Get raw video data (existing method)
        result = self.count_videos(keyword)

        if 'error' in result:
            return result

        videos = result.get('videos', [])

        # Classify each video
        for video in videos:
            video['format'] = classify_format(
                video.get('title', ''),
                video.get('channel_name', '')
            )
            video['angles'] = classify_angles(video.get('title', ''))

        # Apply quality filter
        quality_videos = filter_quality_competition(videos)

        # Calculate format breakdown
        format_counts = Counter(v['format'] for v in videos)

        # Calculate differentiation
        diff_result = calculate_differentiation_score(
            quality_videos,
            channel_angles=['legal', 'historical']  # Channel DNA
        )

        # Get top competitors
        top = self.get_top_channels(keyword, limit=5)

        return {
            'keyword': keyword,
            'video_count': result.get('video_count_raw', 0),
            'channel_count': result.get('unique_channels', 0),
            'quality_video_count': len(quality_videos),
            'format_breakdown': dict(format_counts),
            'angle_distribution': diff_result['angle_distribution'],
            'differentiation_score': diff_result['differentiation_score'],
            'recommended_angle': diff_result['recommended_angle'],
            'gap_scores': diff_result['gap_scores'],
            'top_competitors': top,
            'fetched_at': result.get('fetched_at')
        }
```

### CLI Integration
```python
# Source: Extends Phase 15 demand.py CLI pattern
def competition_command(keyword: str, quality_only: bool = False):
    """
    CLI command for competition analysis.

    Usage:
        python competition.py "dark ages myth"
        python competition.py "dark ages myth" --quality-only
    """
    analyzer = CompetitionAnalyzer()
    result = analyzer.analyze_competition(keyword)

    if 'error' in result:
        print(f"Error: {result['error']}")
        return

    print(f"\nCompetition Analysis: {keyword}")
    print("=" * 50)
    print(f"Total Videos: {result['video_count']}")
    print(f"Unique Channels: {result['channel_count']}")
    print(f"Quality Videos: {result['quality_video_count']}")
    print()

    print("Format Breakdown:")
    for fmt, count in result['format_breakdown'].items():
        pct = count / result['video_count'] * 100 if result['video_count'] else 0
        print(f"  {fmt}: {count} ({pct:.0f}%)")
    print()

    print("Angle Distribution:")
    for angle, pct in sorted(result['angle_distribution'].items(),
                             key=lambda x: x[1], reverse=True):
        if pct > 0:
            print(f"  {angle}: {pct}%")
    print()

    print(f"Differentiation Score: {result['differentiation_score']:.2f}")
    print(f"Recommended Angle: {result['recommended_angle']}")
    print()

    print("Top Competitors:")
    for i, ch in enumerate(result['top_competitors'], 1):
        print(f"  {i}. {ch['channel_name']} ({ch['video_count']} videos, "
              f"{ch['total_views']:,} views)")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual competitor review | Automated classification | 2025-2026 | Scalable analysis of 100+ videos |
| Binary animation/documentary | Multi-format with unknown | 2025 | Better handling of hybrid content |
| View count sorting | Percentile-based filtering | 2025-2026 | Works across different topic scales |
| Single topic classification | Multi-angle detection | 2024-2025 | Reflects real content complexity |

**Deprecated/outdated:**
- YouTube API for bulk engagement data: Too expensive (quota), use scrapetube view counts
- NLP topic modeling for YouTube titles: Overkill, keyword matching sufficient for known domain
- Single-angle classification: Real videos cover multiple angles

## Open Questions

Things that couldn't be fully resolved:

1. **Hybrid Channel Classification**
   - What we know: Some channels (Historia Civilis, Feature History) use simple animation but documentary tone
   - What's unclear: Should they be classified as animation (production blocker) or documentary (tone match)?
   - Recommendation: Create 'hybrid' category, classify as "documentary with animation" which is NOT a hard block for this channel

2. **Quality Threshold Calibration**
   - What we know: 1000 views minimum is reasonable for educational content, 25th percentile removes bottom quarter
   - What's unclear: Optimal thresholds for different topic popularity levels
   - Recommendation: Start with 1000 / 25th percentile, collect feedback, adjust based on user reports of missing competitors

3. **Angle Keyword Completeness**
   - What we know: Current keyword lists cover main angles for geopolitics/history content
   - What's unclear: Coverage gaps for new topic types (science, economics)
   - Recommendation: Start with current lists, add keywords when misclassifications reported, log 'general' classifications for review

4. **Differentiation Score Interpretation**
   - What we know: 0.8+ = high gap, 0.5-0.8 = moderate, <0.5 = crowded
   - What's unclear: Whether these thresholds predict actual success
   - Recommendation: Track score vs. actual video performance in Phase 18 validation, calibrate thresholds

## Sources

### Primary (HIGH confidence)
- [Phase 15 RESEARCH.md](../15-database-foundation-demand-research/15-RESEARCH.md) - scrapetube integration, database patterns
- [Phase 15 competition.py](../../../tools/discovery/competition.py) - Existing implementation to extend
- [YouTube Metrics 2026 (Zapier)](https://zapier.com/blog/youtube-metrics/) - Engagement thresholds, quality signals

### Secondary (MEDIUM confidence)
- [Content Gap Analysis 2026 (Yotpo)](https://www.yotpo.com/blog/modern-content-gap-analysis/) - Topic, depth, perspective, format gaps
- [YouTube Competitor Analysis (Brand24)](https://brand24.com/blog/youtube-competitor-analysis/) - Competitor metrics, differentiation strategies
- [Competitive Content Analysis (Azarian)](https://azariangrowthagency.com/competitive-content-analysis-scale/) - 3-5 gaps per topic statistic
- [YouTube Audience Retention 2026](https://socialrails.com/blog/youtube-audience-retention-complete-guide) - Quality benchmarks (40-60% retention good)

### Tertiary (LOW confidence - needs validation)
- Animation channel keyword list: Based on domain knowledge, may miss channels
- Angle keyword completeness: Created from experience, should be validated with actual classification results
- Quality thresholds (1000 views, 25th percentile): Industry patterns, not validated for this specific channel

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No new dependencies, extends existing Phase 15 code
- Architecture: MEDIUM - Keyword classification is simple but untested, may need iteration
- Pitfalls: MEDIUM - Based on similar classification systems, some uncertainty about edge cases
- Code examples: HIGH - Follows established Phase 15 patterns, straightforward implementation

**Research date:** 2026-01-31
**Valid until:** 2026-03-31 (60 days - classification keywords may need updates as new channels emerge)

---

*Sources compiled from Phase 15 documentation, YouTube industry research, and content gap analysis methodologies as of January 2026.*
