# Phase 10: Pattern Recognition - Research

**Researched:** 2026-01-25
**Domain:** Cross-video analytics aggregation and pattern detection
**Confidence:** HIGH

## Summary

Phase 10 builds on the existing YouTube Analytics infrastructure (Phases 7-9) to detect cross-video patterns. The research confirms this is primarily a **data aggregation and analysis** problem, not a new API integration. All required data is already available through existing scripts and can be enriched with metadata from project files.

The approach is straightforward: collect POST-PUBLISH-ANALYSIS.md files (or re-query the API for fresh data), parse YOUTUBE-METADATA.md files for title/thumbnail attributes, apply topic tags, and compute aggregated statistics. Python's standard library plus the existing code patterns are sufficient.

**Primary recommendation:** Build a `patterns.py` module that aggregates data from existing sources, applies topic tagging, and generates Markdown reports in `channel-data/patterns/`.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib | 3.11+ | File parsing, JSON, regex, statistics | Already in use throughout Phase 8-9 |
| pathlib | stdlib | Path manipulation | Already used in analyze.py |
| statistics | stdlib | Mean, median, stdev calculations | No external dependency needed |
| re | stdlib | Title pattern extraction | Already used in analyze.py |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| json | stdlib | Data serialization | Already used throughout |
| glob | stdlib | File discovery | Already used in analyze.py |
| datetime | stdlib | Timestamps, date math | Already used throughout |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Python statistics | pandas | Overkill for simple aggregations; adds dependency |
| Manual JSON | SQLite | Overkill for ~50-100 videos; unnecessary complexity |
| Markdown files | JSON database | Markdown is human-readable, matches existing pattern |

**Installation:**
```bash
# No additional dependencies - uses existing environment
```

## Architecture Patterns

### Recommended Project Structure
```
tools/youtube-analytics/
    patterns.py          # NEW: Main pattern analysis module
    analyze.py           # Existing: Updated to trigger pattern refresh
    channel_averages.py  # Existing: Provides benchmark data
    video_report.py      # Existing: Individual video data

channel-data/patterns/   # NEW: Output directory
    MONTHLY-2026-01.md   # Monthly summary
    TOPIC-ANALYSIS.md    # Performance by topic type
    TITLE-PATTERNS.md    # Title structure correlations
    PATTERN-DATA.json    # Persistent structured data
```

### Pattern 1: Data Aggregation from Multiple Sources
**What:** Collect video data from POST-PUBLISH-ANALYSIS.md files OR re-query API
**When to use:** Running pattern analysis
**Example:**
```python
# Source: Existing analyze.py pattern
def collect_video_data() -> list[dict]:
    """
    Collect all analyzed video data.

    Strategy:
    1. Scan channel-data/analyses/ for POST-PUBLISH-ANALYSIS-*.md files
    2. Scan video-projects/*/ for POST-PUBLISH-ANALYSIS.md files
    3. Parse each file for structured data
    4. OR: Query API for fresh data if --refresh flag
    """
    analyses = []

    # Check fallback location
    for f in glob.glob(str(PROJECT_ROOT / 'channel-data/analyses/*.md')):
        analyses.append(parse_analysis_file(f))

    # Check project folders
    for lifecycle in ['_IN_PRODUCTION', '_READY_TO_FILM', '_ARCHIVED']:
        pattern = PROJECT_ROOT / 'video-projects' / lifecycle / '*' / 'POST-PUBLISH-ANALYSIS.md'
        for f in glob.glob(str(pattern)):
            analyses.append(parse_analysis_file(f))

    return analyses
```

### Pattern 2: Topic Auto-Detection from Title/Description
**What:** Apply topic tags based on keyword matching
**When to use:** Categorizing videos for pattern analysis
**Example:**
```python
# Source: Based on CHANNEL_ANALYTICS_MASTER.md categories
TAG_VOCABULARY = {
    'territorial': ['dispute', 'border', 'territory', 'claim', 'annex', 'occupation', 'icj'],
    'ideological': ['myth', 'debunk', 'fact-check', 'propaganda', 'narrative'],
    'colonial': ['colonial', 'empire', 'independence', 'decolonization'],
    'politician': ['vance', 'netanyahu', 'trump', 'fuentes', 'reagan'],
    'archaeological': ['dna', 'excavation', 'artifact', 'manuscript'],
    'medieval': ['medieval', 'dark ages', 'crusade', 'viking'],
}

def auto_tag_video(title: str, description: str = '') -> list[str]:
    """Auto-detect topic tags from video metadata."""
    text = f"{title} {description}".lower()
    tags = []
    for tag, keywords in TAG_VOCABULARY.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    return tags or ['uncategorized']
```

### Pattern 3: Title Structure Extraction
**What:** Parse title structure (length, format, keywords)
**When to use:** Correlating title patterns with CTR
**Example:**
```python
# Source: Based on COMPETITOR-TITLE-DATABASE.md patterns
def extract_title_structure(title: str) -> dict:
    """Extract structural attributes from title."""
    return {
        'length': len(title),
        'word_count': len(title.split()),
        'has_colon': ':' in title,
        'has_question': '?' in title,
        'has_number': bool(re.search(r'\d+', title)),
        'has_year': bool(re.search(r'\b(19|20)\d{2}\b', title)),
        'pattern': detect_title_pattern(title),  # e.g., "[Country]'s [Noun] Problem"
        'first_word': title.split()[0] if title else '',
    }

def detect_title_pattern(title: str) -> str:
    """Identify which proven pattern the title matches."""
    patterns = [
        (r"^.+'s\s+\w+\s+Problem$", "[X]'s [Noun] Problem"),
        (r"^Why\s+.+\s+Is\s+", "Why [X] Is [Verb]ing"),
        (r"^How\s+.+\s+Got\s+So\s+", "How [X] Got So [Adj]"),
        (r"^The\s+.+\s+That\s+", "The [X] That [Verb]"),
        (r"\?$", "[Question]"),
        (r":\s+.+$", "[Topic]: [Subtitle]"),
    ]
    for regex, pattern_name in patterns:
        if re.search(regex, title, re.IGNORECASE):
            return pattern_name
    return "other"
```

### Pattern 4: Thumbnail Metadata from Project Files
**What:** Extract thumbnail attributes from YOUTUBE-METADATA.md or thumbnail briefs
**When to use:** Correlating thumbnail characteristics with CTR
**Example:**
```python
# Source: Based on existing YOUTUBE-METADATA.md structure
def extract_thumbnail_metadata(project_folder: str) -> dict:
    """Extract thumbnail attributes from project files."""
    metadata = {
        'type': 'unknown',  # map, face, document, mixed
        'has_text': False,
        'has_person': False,
        'has_map': False,
    }

    # Check YOUTUBE-METADATA.md for thumbnail notes
    metadata_path = Path(project_folder) / 'YOUTUBE-METADATA.md'
    if metadata_path.exists():
        content = metadata_path.read_text()

        # Parse thumbnail section
        if 'map-focused' in content.lower() or 'map thumbnail' in content.lower():
            metadata['type'] = 'map'
            metadata['has_map'] = True
        if 'face' in content.lower():
            metadata['has_person'] = True
            if metadata['type'] == 'unknown':
                metadata['type'] = 'face'
        if 'text overlay' in content.lower():
            metadata['has_text'] = True

    return metadata
```

### Pattern 5: Insights-First Report Generation
**What:** Lead with actionable insights, tables as supporting evidence
**When to use:** Generating pattern reports
**Example:**
```python
# Source: User decision from 10-CONTEXT.md
def format_topic_analysis_report(data: dict) -> str:
    """Generate insights-first Markdown report."""
    lines = [
        "# Topic Performance Analysis",
        "",
        f"**Generated:** {datetime.now().isoformat()}",
        f"**Videos analyzed:** {data['total_videos']}",
        "",
        "## Key Insights",
        "",
    ]

    # Lead with actionable insights
    for insight in data['insights']:
        lines.append(f"- {insight}")

    lines.extend([
        "",
        "## Recommended Next Actions",
        "",
    ])

    for action in data['recommendations']:
        lines.append(f"- [ ] {action}")

    # Supporting data tables follow
    lines.extend([
        "",
        "## Performance by Topic Type",
        "",
        "*Based on {} videos with 3+ videos per category*".format(data['total_videos']),
        "",
        "| Topic | Videos | Avg Views | Avg CTR | Avg Retention |",
        "|-------|--------|-----------|---------|---------------|",
    ])

    for topic, stats in data['by_topic'].items():
        lines.append(
            f"| {topic} | {stats['count']} | {stats['avg_views']:,.0f} | "
            f"{stats['avg_ctr']:.1f}% | {stats['avg_retention']:.1f}% |"
        )

    return "\n".join(lines)
```

### Anti-Patterns to Avoid
- **Over-engineering with database:** Don't add SQLite/PostgreSQL - file-based storage matches existing patterns and is sufficient for ~100 videos
- **Real-time dashboards:** Don't build web UI - Markdown reports are readable and version-controlled
- **Complex ML models:** Don't add sklearn for "pattern detection" - simple statistics (mean, comparison to average) are more interpretable
- **Separate data store:** Don't create a separate JSON database duplicating POST-PUBLISH-ANALYSIS.md data - parse files on demand

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Channel averages | Custom average calculation | `channel_averages.py` | Already handles minimum 3 videos, 5% threshold |
| Video metrics | Custom API calls | `metrics.py`, `video_report.py` | Already handles errors, date ranges |
| Date parsing | Custom logic | `datetime.fromisoformat()` | Standard library handles ISO format |
| Path manipulation | String concatenation | `pathlib.Path` | Already used in analyze.py |

**Key insight:** Phase 8-9 built robust infrastructure. Pattern analysis is aggregation on top of it, not replacement.

## Common Pitfalls

### Pitfall 1: Insufficient Sample Sizes
**What goes wrong:** Calculating averages with 1-2 videos per category gives misleading results
**Why it happens:** Eager to show "patterns" before data accumulates
**How to avoid:** Enforce minimum 3 videos per category (consistent with channel_averages.py)
**Warning signs:** "territorial topics average 5x views" based on 1 video

### Pitfall 2: Conflating Correlation with Causation
**What goes wrong:** "Question titles cause higher CTR" when really "certain topics use questions AND perform well"
**Why it happens:** Title structure and topic type are confounded
**How to avoid:** Present observations, not causal claims; show sample sizes; compare within topic types
**Warning signs:** Absolute statements like "Always use colons in titles"

### Pitfall 3: Ignoring Time Effects
**What goes wrong:** Recent videos have fewer views but aren't "underperforming"
**Why it happens:** Views accumulate over time; comparing 1-week-old to 1-year-old videos
**How to avoid:** Normalize by age OR compare 30-day windows OR show publication date
**Warning signs:** "All new videos underperform" when really they're just young

### Pitfall 4: Overwriting Pattern Data
**What goes wrong:** Pattern analysis runs overwrite previous monthly summaries
**Why it happens:** Not using timestamped filenames or append mode
**How to avoid:** Use dated filenames (MONTHLY-2026-01.md); never overwrite; create new files
**Warning signs:** Missing historical pattern data

### Pitfall 5: Duplicate Data Collection
**What goes wrong:** Re-fetching API data that's already in POST-PUBLISH-ANALYSIS.md
**Why it happens:** Not checking existing files first
**How to avoid:** Parse existing files as primary source; only refresh on explicit request
**Warning signs:** Slow pattern analysis runs; API quota warnings

## Code Examples

Verified patterns from existing codebase:

### File Discovery Pattern
```python
# Source: analyze.py lines 77-98
def find_analysis_files() -> list[Path]:
    """Find all POST-PUBLISH-ANALYSIS files in project."""
    search_paths = [
        PROJECT_ROOT / 'channel-data' / 'analyses',
        PROJECT_ROOT / 'video-projects' / '_IN_PRODUCTION',
        PROJECT_ROOT / 'video-projects' / '_READY_TO_FILM',
        PROJECT_ROOT / 'video-projects' / '_ARCHIVED',
    ]

    files = []
    for base in search_paths:
        # Direct analyses folder
        for f in base.glob('POST-PUBLISH-ANALYSIS*.md'):
            files.append(f)
        # Project subfolders
        for f in base.glob('*/POST-PUBLISH-ANALYSIS.md'):
            files.append(f)

    return files
```

### Aggregation with Minimum Threshold
```python
# Source: channel_averages.py lines 148-156
def aggregate_by_topic(videos: list[dict], min_count: int = 3) -> dict:
    """
    Aggregate metrics by topic tag with minimum sample size.

    Args:
        videos: List of video data dicts with 'tags' and metrics
        min_count: Minimum videos to include topic (default 3)
    """
    from collections import defaultdict
    from statistics import mean

    by_topic = defaultdict(list)

    for v in videos:
        for tag in v.get('tags', ['uncategorized']):
            by_topic[tag].append(v)

    # Filter to topics with enough data
    result = {}
    for topic, vids in by_topic.items():
        if len(vids) >= min_count:
            result[topic] = {
                'count': len(vids),
                'avg_views': mean(v['views'] for v in vids),
                'avg_ctr': mean(v.get('ctr', 0) for v in vids),
                'avg_retention': mean(v.get('retention', 0) for v in vids),
                'videos': [v['title'] for v in vids],
            }

    return result
```

### Winner Detection
```python
# Source: Based on 10-CONTEXT.md decision
def identify_winners(videos: list[dict], channel_avg: dict) -> list[dict]:
    """
    Identify videos that beat channel average on BOTH CTR and retention.

    "Winners" = above average on both metrics (per user decision).
    """
    winners = []

    avg_ctr = channel_avg.get('avg_ctr', 0)
    avg_retention = channel_avg.get('avg_retention', 0)

    for v in videos:
        ctr = v.get('ctr', 0)
        retention = v.get('retention', 0)

        if ctr > avg_ctr and retention > avg_retention:
            winners.append({
                **v,
                'ctr_delta': ctr - avg_ctr,
                'retention_delta': retention - avg_retention,
            })

    return sorted(winners, key=lambda x: x['views'], reverse=True)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual spreadsheet analysis | Automated pattern detection | Phase 10 | Consistent, reproducible insights |
| Single-video focus | Cross-video comparison | Phase 10 | Reveals patterns invisible in single videos |
| Generic categories | Flexible multi-tag system | Phase 10 decision | Better reflects hybrid content |

**Deprecated/outdated:**
- None - this is new functionality building on Phase 8-9

## Open Questions

Things that couldn't be fully resolved:

1. **Thumbnail attribute extraction reliability**
   - What we know: YOUTUBE-METADATA.md contains thumbnail notes in unstructured format
   - What's unclear: Extraction accuracy when format varies between projects
   - Recommendation: Start with keyword detection; add structured thumbnail metadata section to YOUTUBE-METADATA template for future videos

2. **CTR data availability**
   - What we know: CTR not always available via API; manual entry supported
   - What's unclear: What percentage of videos will have CTR for pattern analysis
   - Recommendation: Compute patterns for videos WITH CTR; flag when sample size drops below threshold

3. **Monthly summary trigger timing**
   - What we know: Auto-generate when new month's video is analyzed
   - What's unclear: Edge case when first video of month is analyzed but month is incomplete
   - Recommendation: Generate at end of month OR on-demand; don't auto-trigger mid-month

## Sources

### Primary (HIGH confidence)
- `tools/youtube-analytics/analyze.py` - Existing analysis orchestrator (reviewed lines 1-947)
- `tools/youtube-analytics/channel_averages.py` - Channel benchmark calculations (reviewed lines 1-352)
- `tools/youtube-analytics/metrics.py` - Core metrics fetching (reviewed lines 1-221)
- `tools/youtube-analytics/retention.py` - Retention curve analysis (reviewed lines 1-235)
- `channel-data/CHANNEL_ANALYTICS_MASTER.md` - Manual analytics and category definitions

### Secondary (MEDIUM confidence)
- `channel-data/COMPETITOR-TITLE-DATABASE.md` - Title patterns from successful channels
- `video-projects/_IN_PRODUCTION/*/YOUTUBE-METADATA.md` - Existing metadata format examples

### Tertiary (LOW confidence)
- None - research based on existing codebase analysis

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using existing Python patterns from Phase 8-9
- Architecture: HIGH - Clear extension of existing analyze.py patterns
- Pitfalls: HIGH - Based on statistical analysis fundamentals and existing code review

**Research date:** 2026-01-25
**Valid until:** 2026-02-25 (30 days - stable infrastructure phase)
