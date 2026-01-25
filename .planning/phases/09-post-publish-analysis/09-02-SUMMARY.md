---
phase: 09-post-publish-analysis
plan: 02
subsystem: analytics-tools
tags: [python, orchestrator, analysis, lessons]
completed: 2026-01-25
duration: ~15 minutes

dependency-graph:
  requires: ["09-01"]
  provides: ["complete-analysis-engine", "automated-lessons"]
  affects: ["09-03"]

tech-stack:
  added: []
  patterns: ["orchestrator-pattern", "graceful-degradation"]

key-files:
  created:
    - tools/youtube-analytics/analyze.py
  modified: []

decisions:
  - id: "ascii-curve-note"
    choice: "Reference retention.py for curve visualization"
    rationale: "Full data points needed for ASCII curve; video_report only includes summary"

metrics:
  tasks: 2
  commits: 1
  files_created: 1
  files_modified: 0
---

# Phase 9 Plan 02: Analysis Orchestrator Summary

**One-liner:** Complete analysis orchestrator combining video_report, comments, and channel_averages with automated lesson generation and manual CTR fallback.

## What Was Built

### analyze.py (770 lines)

Main orchestrator script that powers the `/analyze` command.

**Core Functions:**
- `extract_video_id(url_or_id)` - Parses all YouTube URL formats (watch, youtu.be, shorts, embed)
- `run_analysis(video_id_or_url, manual_ctr=None)` - Main entry point combining all data sources
- `generate_lessons(analysis_data)` - Automated insights from retention, engagement, benchmarks, comments
- `format_analysis_markdown(analysis)` - Human-readable output with benchmark comparison table

**CLI Interface:**
```bash
python analyze.py VIDEO_ID              # JSON output
python analyze.py VIDEO_ID --markdown   # Markdown output
python analyze.py https://youtu.be/ID   # URL input
python analyze.py VIDEO_ID --ctr 4.5    # Manual CTR override
```

**Output Structure:**
```python
{
    'video_id': '...',
    'title': '...',
    'fetched_at': 'ISO timestamp',
    'engagement': {...},      # From video_report.py
    'ctr': {...},             # From ctr.py with manual fallback
    'retention': {...},       # From retention.py
    'benchmarks': {
        'channel_averages': {...},
        'comparison': {...}
    },
    'comments': {
        'total': N,
        'questions': [...],
        'objections': [...],
        'requests': [...]
    },
    'lessons': {
        'observations': [...],
        'actionable': [...]
    },
    'errors': [...]
}
```

## Lesson Generation Rules

The `generate_lessons()` function applies pattern-based rules:

**Retention:**
- >= 35%: "Strong retention - hook and pacing working well"
- 25-35%: "Average retention - room for improvement"
- < 25%: "Retention needs work - review first 30 seconds"
- Drop > 10%: "Major drop-off at X% - review that section"
- Drops > 5: "Multiple drop-offs - tighten overall pacing"

**Engagement:**
- Subs/100 views >= 1: "Strong subscriber conversion"
- Engagement rate >= 5%: "Excellent engagement"
- Engagement rate < 1%: "Low engagement - add prompts"

**Benchmarks:**
- Views > 50% above avg: "Outperforming channel average"
- Views > 50% below avg: "Underperforming vs channel"

**Comments:**
- Questions > 5: "Audience seeking clarification"
- Objections > 3: "Review for accuracy"
- Requests > 3: "Note for future topics"

## CTR Handling

**When CTR unavailable via API:**
- Markdown shows: "CTR: Not available via API"
- Includes hint: "Check YouTube Studio > Analytics > Reach tab"

**When manual CTR provided:**
- `run_analysis('VIDEO_ID', manual_ctr=4.5)`
- Or: `python analyze.py VIDEO_ID --ctr 4.5`
- Shows: "CTR: 4.5% (manual entry)"
- Validates: 0-100 range

## Integration Points

**Imports from Plan 01:**
```python
from video_report import generate_video_report
from comments import fetch_and_categorize_comments
from channel_averages import get_channel_averages, compare_to_channel
```

**Ready for Plan 03:**
- `run_analysis()` callable from slash command
- `format_analysis_markdown()` for display
- Complete dict for file saving

## Verification Results

| Test | Command | Result |
|------|---------|--------|
| Import | `from analyze import run_analysis` | OK |
| JSON output | `python analyze.py wCFReiCGiks` | Returns complete analysis |
| Markdown output | `python analyze.py ID --markdown` | All sections present |
| URL input | `python analyze.py https://youtu.be/ID` | Extracts ID correctly |
| Manual CTR | `python analyze.py ID --ctr 4.5 --markdown` | Shows "(manual entry)" |
| CTR validation | `python analyze.py ID --ctr 150` | Error: must be 0-100 |

## Commits

| Hash | Description |
|------|-------------|
| 49ee37a | feat(09-02): create analyze.py orchestrator for post-publish analysis |

## Deviations from Plan

None - plan executed exactly as written. Both Task 1 (orchestrator) and Task 2 (CTR fallback) were implemented in a single file as the functionality was tightly coupled.

## Requirements Coverage

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| ANALYSIS-01 | Partial | Engine ready, command wrapper in Plan 03 |
| ANALYSIS-02 | Complete | CTR comparison + manual fallback |
| ANALYSIS-03 | Complete | All drop-offs with timestamps/locations |
| ANALYSIS-04 | Complete | Comments fetched and categorized |
| ANALYSIS-05 | Complete | Lessons in observations + actionable format |

## Next Phase Readiness

Plan 03 can proceed - analyze.py provides complete analysis engine:
- `run_analysis()` for data fetching
- `format_analysis_markdown()` for display
- Structured dict for file operations

No blockers identified.
