# Phase 19 Research: Performance Data Foundation

**Phase:** 19-performance-data-foundation
**Goal:** User can see what's working based on subscriber conversion
**Research Date:** 2026-02-02

## Requirements Analysis

| Requirement | Description |
|-------------|-------------|
| PERF-01 | User can see subscriber conversion per video for entire published catalog |
| PERF-02 | User can see which topic types correlate with high conversion |
| PERF-03 | User can see which angles correlate with high conversion |
| INTG-01 | Data pulls from existing YouTube Analytics API integration |

## Existing Codebase Analysis

### YouTube Analytics API (tools/youtube-analytics/)

**Available subscriber metrics:**
- `subscribersGained` - subscribers gained from a video
- `subscribersLost` - subscribers lost from a video
- Both available via `metrics.py:get_video_metrics()` function

**Key files:**
- `metrics.py` - Fetches engagement metrics including `subscribers_gained`, `subscribers_lost`
- `channel_averages.py` - Calculates channel benchmarks including `avg_subscribers_gained`
- `video_report.py` - Generates comprehensive report with subscriber efficiency metric
- `patterns.py` - Cross-video pattern analysis (topic tagging, aggregation)
- `analyze.py` - Post-publish analysis orchestrator

**Subscriber conversion already calculated in video_report.py (lines 275-280):**
```python
subs = engagement.get('subscribers_gained', 0) or 0
views = engagement.get('views', 0) or 0
if views > 0 and subs > 0:
    subs_per_100_views = round(subs / views * 100, 2)
    lines.append(f"- **Subscribers per 100 views:** {subs_per_100_views}")
```

### Classification System (tools/discovery/)

**Available from Phase 16:**
- `classifiers.py` - Format and angle classification
  - `classify_format(title, channel_name)` - Returns 'animation', 'documentary', 'unknown'
  - `classify_angles(title)` - Returns list like ['legal', 'historical', 'political']
- `database.py` - KeywordDB with classification storage

**Angle categories available:**
- political
- legal
- historical
- economic
- geographic

### Pattern Analysis (tools/youtube-analytics/patterns.py)

**Existing topic tagging (TAG_VOCABULARY):**
- territorial, ideological, colonial, politician, archaeological, medieval

**Existing aggregation functions:**
- `aggregate_by_topic()` - Groups videos by topic tag
- `identify_winners()` - Finds videos above average on both CTR and retention
- `generate_topic_report()` - Creates TOPIC-ANALYSIS.md

**Key insight:** patterns.py already has infrastructure for cross-video analysis but:
1. Does NOT track subscriber conversion per video
2. Does NOT use Phase 16 angle classification system
3. Relies on parsing POST-PUBLISH-ANALYSIS.md files (indirect)

## Data Flow Design

### Current State

```
YouTube Analytics API
        |
        v
metrics.py (subscribers_gained, subscribers_lost)
        |
        v
video_report.py (calculates subs_per_100_views)
        |
        v
analyze.py (saves POST-PUBLISH-ANALYSIS.md)
        |
        v
patterns.py (parses files, aggregates by topic)
```

### Problem: No centralized performance database

- Performance data scattered across POST-PUBLISH-ANALYSIS.md files
- Must parse markdown files to get metrics
- No direct API-to-database-to-analysis pipeline
- Classification system (Phase 16) not integrated with performance analysis

### Proposed Architecture

```
YouTube Analytics API
        |
        v
metrics.py (fetch all video metrics)
        |
        v
performance.py (NEW)
  - VideoPerformance dataclass
  - fetch_catalog_metrics()
  - calculate_conversion_rates()
  - classify_videos_by_angle()
        |
        v
performance_db.py (NEW - extend keywords.db or new db)
  - video_performance table
  - store/retrieve performance metrics
  - aggregation queries
        |
        v
performance_report.py (NEW)
  - generate_conversion_report()
  - aggregate_by_topic_type()
  - aggregate_by_angle()
  - identify_winning_patterns()
```

## Technical Approach

### Option A: Extend keywords.db
**Pros:**
- Single database for all discovery/analysis
- Consistent with Phase 15-18 patterns
- Can link keywords to video performance

**Cons:**
- keywords.db is about keyword research, not video performance
- Semantic mismatch

### Option B: New performance.db
**Pros:**
- Clean separation of concerns
- Purpose-built for performance tracking
- Can evolve independently

**Cons:**
- Another database to manage
- Duplication if we need keyword-performance correlation later

### Recommendation: Option A (Extend keywords.db)

Reasons:
1. The end goal of v1.4 is to recommend topics based on performance + competition + constraints
2. Linking video performance to keywords enables "this keyword converts well" insights
3. Consistent with existing codebase architecture patterns

### Database Schema Extension

```sql
-- New table: video_performance
CREATE TABLE IF NOT EXISTS video_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT UNIQUE NOT NULL,
    title TEXT,
    views INTEGER,
    subscribers_gained INTEGER,
    subscribers_lost INTEGER,
    conversion_rate REAL,  -- subs_gained / views * 100
    watch_time_minutes REAL,
    avg_view_duration_seconds INTEGER,
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    -- Classification (from Phase 16 classifiers)
    topic_type TEXT,       -- territorial, ideological, colonial, etc.
    angles TEXT,           -- JSON array: ["legal", "historical"]
    -- Timestamps
    published_at DATE,
    fetched_at DATE NOT NULL,
    classified_at DATE
);

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_performance_conversion ON video_performance(conversion_rate DESC);
CREATE INDEX IF NOT EXISTS idx_performance_topic ON video_performance(topic_type);
CREATE INDEX IF NOT EXISTS idx_performance_angles ON video_performance(angles);
```

### Classification Integration

Use Phase 16 classifiers but adapt for own channel:

```python
from classifiers import classify_angles

# For own videos, use title for angle classification
angles = classify_angles(video_title)

# Topic type from patterns.py TAG_VOCABULARY
topic_type = auto_tag_video(video_title)[0]  # Primary tag
```

### CLI Design

```bash
# Fetch performance for all videos
python performance.py --fetch-all

# Fetch performance for specific video
python performance.py VIDEO_ID

# Generate conversion report
python performance.py --report

# Show top converters
python performance.py --top 10

# Show conversion by topic type
python performance.py --by-topic

# Show conversion by angle
python performance.py --by-angle
```

## Implementation Tasks

### Task 1: Database Schema + Performance Fetcher
- Add video_performance table to keywords.db schema
- Create `tools/youtube-analytics/performance.py`
- Implement `fetch_catalog_metrics()` using existing `get_recent_video_ids()` and `get_video_metrics()`
- Calculate conversion rates
- Store to database

### Task 2: Classification + Aggregation + Report
- Integrate Phase 16 classifiers for angle detection
- Implement aggregation queries (by topic, by angle)
- Generate performance report markdown
- CLI interface

### Task 3: Integration with /analyze
- Extend `/analyze` slash command to show conversion context
- Update patterns.py to use performance database instead of file parsing

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API quota limits | Medium | High | Cache aggressively, batch requests |
| Missing data for old videos | Low | Medium | Graceful handling, show "N/A" |
| Classification accuracy | Medium | Low | Human can correct classifications |

## Dependencies

- Phase 10 (YouTube Analytics API) - COMPLETE
- Phase 16 (Classification System) - COMPLETE
- User has published videos with analytics data

## Discovery Level

**Level 0 - Skip**

Rationale:
- All work follows established codebase patterns
- Uses existing metrics.py, classifiers.py
- No new external dependencies
- Pure internal feature extension

## Estimated Scope

- 2 plans
- ~3-4 tasks total
- ~40% context per plan (moderate complexity)
