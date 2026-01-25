---
phase: 08-data-pull-scripts
plan: 01
subsystem: api
tags: [youtube-analytics, metrics, engagement, python]

# Dependency graph
requires: [07-02]
provides:
  - Core engagement metrics fetcher (metrics.py)
  - Reusable get_video_metrics() function
  - Video title lookup via Data API
affects: [08-02, 08-03, 09-01]

# Tech tracking
tech-stack:
  added: []
  patterns: [api-response-parsing, error-dict-pattern, cli-with-optional-args]

key-files:
  created:
    - tools/youtube-analytics/metrics.py
  modified: []

key-decisions:
  - "Default date range 2020-01-01 to today - captures full video lifetime"
  - "Error dict pattern - return {error: msg} instead of raising exceptions"
  - "Title lookup failure returns None - doesn't crash the whole request"
  - "Snake_case keys in output - consistent with Python conventions"

patterns-established:
  - "API response parsing: map columnHeaders to values via dict(zip())"
  - "Graceful degradation: Title lookup failure doesn't block metrics"
  - "CLI with optional args: --start-date and --end-date flags"

# Metrics
duration: 5min
completed: 2026-01-24
---

# Phase 8 Plan 01: Core Engagement Metrics Fetcher Summary

**Callable Python script that fetches views, watch time, likes, comments, shares, and subscriber changes for any video via YouTube Analytics API, with human-readable video title**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-01-24
- **Completed:** 2026-01-24
- **Tasks:** 2 (both auto)
- **Files created:** 1

## Accomplishments

- Created metrics.py with get_video_metrics() function
- Added get_video_title() helper for human-readable output
- Implemented comprehensive error handling (400, 403, 404, generic)
- CLI interface with optional date range arguments
- Default date range captures full video lifetime (2020-01-01 to today)

## Task Commits

Both tasks were committed in a single atomic commit (new file):

1. **Task 1: Core metrics fetcher** - `11eb823` (feat)
   - YouTube Analytics API query for engagement metrics
   - Returns structured JSON with snake_case keys
   - Error handling returns dict instead of crashing

2. **Task 2: Video title lookup** - `11eb823` (same commit - new file)
   - Added get_video_title() using YouTube Data API v3
   - Integrated into get_video_metrics() return structure
   - Graceful failure returns None

**Note:** Both tasks committed together because metrics.py was a new untracked file.

## Files Created

- `tools/youtube-analytics/metrics.py` - Core engagement metrics fetcher (220 lines)
  - Exports: `get_video_metrics()`, `get_video_title()`
  - CLI: `python metrics.py VIDEO_ID [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]`

## Output Structure

```json
{
  "video_id": "abc123",
  "title": "Video Title",
  "views": 19767,
  "watch_time_minutes": 8017.0,
  "avg_view_duration_seconds": 243,
  "likes": 542,
  "dislikes": 0,
  "comments": 87,
  "shares": 23,
  "subscribers_gained": 15,
  "subscribers_lost": 2,
  "date_range": {"start": "2020-01-01", "end": "2026-01-24"},
  "fetched_at": "2026-01-24T10:30:00Z"
}
```

## Error Handling

| HTTP Status | Response |
|-------------|----------|
| 400 | `{"error": "Invalid video ID or bad request", ...}` |
| 403 | `{"error": "API quota exceeded or permission denied", ...}` |
| 404 | `{"error": "Video not found", ...}` |
| No data | `{"error": "No data found for video", ...}` |

Script never crashes - always returns valid JSON.

## Decisions Made

- **Date range default:** 2020-01-01 to today to capture full video lifetime
- **Error dict pattern:** Return `{error: msg}` instead of raising exceptions
- **Title lookup graceful:** Returns None on failure, doesn't block metrics
- **Snake_case output:** Python convention for downstream processing

## Deviations from Plan

None - plan executed exactly as written.

## Integration Points

**Import pattern (for Phase 8-9 scripts):**
```python
from metrics import get_video_metrics

result = get_video_metrics('VIDEO_ID')
print(f"{result['title']}: {result['views']} views")
```

**CLI usage:**
```bash
python metrics.py VIDEO_ID
python metrics.py VIDEO_ID --start-date 2025-01-01 --end-date 2025-12-31
```

## Next Phase Readiness

- Ready for Plan 08-02: Retention curve fetcher
- Ready for Plan 08-03: CTR/impressions fetcher
- get_video_metrics() provides foundation for combined reports
- Error dict pattern should be followed by retention.py and ctr.py

---
*Phase: 08-data-pull-scripts*
*Completed: 2026-01-24*
