---
phase: 10
plan: 01
subsystem: youtube-analytics
tags: [pattern-analysis, topic-tagging, cross-video-comparison]
dependency-graph:
  requires:
    - 09: POST-PUBLISH-ANALYSIS file format
    - 09: channel-data/analyses/ fallback directory
  provides:
    - patterns.py module with topic analysis
    - TOPIC-ANALYSIS.md report generation
    - Auto-tagging by topic vocabulary
  affects:
    - 10-02: Title/thumbnail pattern analysis (extends patterns.py)
    - 10-03: Audience insight aggregation (uses collect_video_data)
tech-stack:
  added: []
  patterns:
    - Insights-first report format
    - Minimum sample size enforcement (3+ videos)
    - Fixed vocabulary for consistent tagging
file-tracking:
  key-files:
    created:
      - tools/youtube-analytics/patterns.py
      - channel-data/patterns/TOPIC-ANALYSIS.md
    modified: []
decisions:
  - decision: "TAG_VOCABULARY uses 6 categories"
    rationale: "Covers channel content types: territorial, ideological, colonial, politician, archaeological, medieval"
  - decision: "Minimum 3 videos per topic for aggregation"
    rationale: "Consistent with channel_averages.py threshold for meaningful patterns"
  - decision: "insights-first report format"
    rationale: "Per 10-CONTEXT.md decision - actionable insights before data tables"
metrics:
  duration: ~10 min
  completed: 2026-01-26
---

# Phase 10 Plan 01: Topic Performance Tracking Summary

Core pattern analysis module that collects video data and generates topic-based performance insights.

## One-liner

patterns.py with collect_video_data, auto_tag_video, aggregate_by_topic, identify_winners - generates TOPIC-ANALYSIS.md with insights-first format

## What Was Built

### patterns.py (809 lines)

**Core Data Collection:**
- `collect_video_data()` - Scans POST-PUBLISH-ANALYSIS files from all project folders
- `parse_analysis_file()` - Extracts video_id, title, views, retention, CTR from markdown
- `enrich_video_data()` - Adds topic tags and computed fields

**Topic Tagging:**
- `TAG_VOCABULARY` - Fixed vocabulary with 6 categories (territorial, ideological, colonial, politician, archaeological, medieval)
- `auto_tag_video()` - Keyword-based topic detection from title/description
- Videos can have multiple tags (e.g., `['territorial', 'colonial']`)

**Aggregation & Analysis:**
- `aggregate_by_topic()` - Groups videos by tag with min 3 videos threshold
- `identify_winners()` - Videos above average on BOTH CTR AND retention
- `identify_anti_patterns()` - Videos below average on both metrics
- `generate_insights()` - Creates actionable insight statements
- `generate_recommendations()` - Produces next-action suggestions

**Report Generation:**
- `generate_topic_report()` - Creates TOPIC-ANALYSIS.md with insights-first format
- Output location: `channel-data/patterns/TOPIC-ANALYSIS.md`

### CLI Interface

```bash
python patterns.py              # Show collected video data
python patterns.py --tags       # Show videos with auto-detected tags
python patterns.py --topic-report    # Generate TOPIC-ANALYSIS.md
```

## Key Links Established

| From | To | Via |
|------|------|-----|
| patterns.py | channel-data/analyses/ | glob file discovery |
| patterns.py | video-projects/*/* | project folder scanning |
| patterns.py | channel-data/patterns/ | report output directory |

## Report Structure (Insights-First)

```markdown
# Topic Performance Analysis

**Generated:** {timestamp}
**Videos analyzed:** {N}

## Key Insights
- {insight 1}
- {insight 2}

## Recommended Next Actions
- [ ] {action 1}
- [ ] {action 2}

## Performance by Topic Type
| Topic | Videos | Avg Views | Avg CTR | Avg Retention |
...

## Winners (Above Average on Both CTR AND Retention)
...

## Anti-Patterns (Below Average on Both)
...

## Videos by Topic
### {topic} ({N} videos)
- {video title 1}
- {video title 2}
```

## Deviations from Plan

None - plan executed exactly as written.

## Requirements Satisfied

- [x] PATRN-01: Cross-video comparison by topic type working
- [x] patterns.py module exists with core functionality (809 lines, exceeds 200 min)
- [x] TOPIC-ANALYSIS.md report generated with insights-first format
- [x] Minimum sample size (3) enforced for statistical validity
- [x] All functions importable as module

## Verification Results

| Test | Result |
|------|--------|
| `python patterns.py` | Shows empty data (no analysis files yet) |
| `python patterns.py --tags` | Shows empty data (no analysis files yet) |
| `python patterns.py --topic-report` | Generates TOPIC-ANALYSIS.md |
| `auto_tag_video('Belize-Guatemala border dispute')` | Returns `['territorial']` |
| Module imports | All functions importable |
| Line count | 809 lines (exceeds 200 min) |

## Next Phase Readiness

**Ready for Plan 02:** Title/thumbnail pattern analysis

Plan 02 will add:
- `extract_title_structure()` - Parse title length, format, keywords
- `extract_thumbnail_metadata()` - Get thumbnail attributes from project files
- Title pattern correlation with CTR

patterns.py provides the foundation:
- `get_youtube_metadata()` already implemented for project folder matching
- `collect_video_data()` provides base data for title analysis
- Insights-first report pattern established for reuse

---

*Generated: 2026-01-26*
*Commits: c3b498a, c240f92*
