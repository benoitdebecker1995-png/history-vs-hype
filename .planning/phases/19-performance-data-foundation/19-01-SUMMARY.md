---
phase: 19
plan: 01
subsystem: analytics
tags: [youtube-analytics, database, performance-tracking, subscriber-conversion]

dependency_graph:
  requires:
    - Phase 8 (metrics.py, channel_averages.py)
    - Phase 15-16 (KeywordDB, classifiers.py)
  provides:
    - video_performance table schema
    - Performance fetcher module with CLI
    - Conversion rate calculation
  affects:
    - 19-02 (pattern analysis will use this data)
    - Future /next command (needs conversion data)

tech_stack:
  added: []
  patterns:
    - Automatic table migration via _ensure_performance_table()
    - JSON storage for angles list with parse on retrieval
    - Graceful degradation when database unavailable

file_tracking:
  created:
    - tools/youtube-analytics/performance.py
  modified:
    - tools/discovery/schema.sql
    - tools/discovery/database.py

decisions:
  - key: conversion_formula
    choice: "(subscribers_gained / views) * 100"
    rationale: Standard conversion rate calculation, returns percentage
  - key: topic_classification
    choice: Reuse TAG_VOCABULARY from patterns.py
    rationale: Consistency with existing topic analysis
  - key: angle_classification
    choice: Reuse classify_angles from Phase 16
    rationale: Code reuse, already tested classifier
  - key: json_angle_storage
    choice: Store angles as JSON TEXT
    rationale: SQLite lacks native array type, JSON allows list storage

metrics:
  duration: 4 minutes
  completed: 2026-02-02
---

# Phase 19 Plan 01: Performance Data Foundation Summary

**One-liner:** Database schema and fetcher module for tracking subscriber conversion per video with topic/angle classification.

## What Was Built

### 1. Database Schema Extension (schema.sql)

Added `video_performance` table with:
- Core identifiers: video_id (unique), title
- Engagement metrics: views, likes, comments, shares
- Subscriber metrics: subscribers_gained, subscribers_lost
- Calculated field: conversion_rate
- Watch metrics: watch_time_minutes, avg_view_duration_seconds
- Classification: topic_type, angles (JSON)
- Timestamps: published_at, fetched_at, classified_at

Indexes for:
- conversion_rate DESC (top converter queries)
- topic_type (filter by topic)
- fetched_at DESC (recent data queries)

### 2. Database Methods (database.py)

Added to KeywordDB class:
- `_ensure_performance_table()` - Auto-migration for existing databases
- `add_video_performance()` - Insert or update video metrics
- `get_video_performance()` - Retrieve single video
- `get_all_video_performance()` - Retrieve all with limit
- `get_performance_by_topic()` - Filter by topic type
- `get_performance_by_angle()` - JSON search for angle
- `get_top_converters()` - Top N by conversion rate

### 3. Performance Fetcher (performance.py)

New module providing:
- `calculate_conversion_rate(views, subs)` - Core calculation
- `classify_topic_type(title)` - Topic classification
- `classify_own_video(title)` - Combined topic + angle classification
- `fetch_video_performance(video_id)` - Single video fetch + store
- `fetch_catalog_metrics(max_videos)` - Batch fetch for catalog

CLI interface:
```bash
python performance.py VIDEO_ID           # Fetch single video
python performance.py --fetch-all        # Fetch all recent videos
python performance.py --fetch-all -n 20  # Fetch last 20 videos
python performance.py --top 10           # Show top 10 converters
python performance.py --no-save VIDEO_ID # Fetch without saving
```

## Integration Points

### Imports from Phase 8
```python
from metrics import get_video_metrics
from channel_averages import get_recent_video_ids
```

### Imports from Phase 15-16
```python
from database import KeywordDB
from classifiers import classify_angles
```

### Topic Vocabulary
Reused TAG_VOCABULARY pattern from patterns.py:
- territorial, ideological, colonial, politician
- archaeological, medieval, legal, general

## Commits

| Hash | Message |
|------|---------|
| baa27b8 | feat(19-01): add video_performance table and database methods |
| ecef579 | feat(19-01): create performance fetcher module with CLI |

## Files Changed

| File | Change |
|------|--------|
| tools/discovery/schema.sql | Added video_performance table + indexes |
| tools/discovery/database.py | Added 7 methods for performance tracking |
| tools/youtube-analytics/performance.py | New fetcher module (497 lines) |

## Verification Results

All verification checks passed:
1. video_performance table exists in schema
2. KeywordDB methods: add, get, get_all available
3. performance.py loads without errors
4. Conversion rate: 0.5 for 10000 views, 50 subs
5. Topic classification: 'territorial' for border dispute
6. Angle classification: returns topic_type + angles
7. Data persistence: insert + retrieve works

## Deviations from Plan

None - plan executed exactly as written.

## Next Phase Readiness

**Blockers:** None

**Ready for 19-02:** Pattern analysis can now:
- Query video_performance table for all videos
- Get top converters with `get_top_converters()`
- Filter by topic with `get_performance_by_topic()`
- Filter by angle with `get_performance_by_angle()`

**User action required:** To populate data, run:
```bash
cd tools/youtube-analytics
python performance.py --fetch-all
```
This requires YouTube Analytics API authentication (configured in Phase 7).
