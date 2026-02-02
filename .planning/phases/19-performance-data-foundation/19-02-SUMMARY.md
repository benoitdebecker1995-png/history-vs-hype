---
phase: 19
plan: 02
subsystem: analytics
tags: [youtube-analytics, performance-report, subscriber-conversion, pattern-analysis]

dependency_graph:
  requires:
    - Phase 19-01 (performance.py, video_performance table)
    - Phase 15-16 (KeywordDB methods)
  provides:
    - Performance report generator
    - Topic/angle aggregation functions
    - CLI report commands
  affects:
    - /analyze command workflow (documented link)
    - Future /next command (will use insights)

tech_stack:
  added: []
  patterns:
    - Statistics module for mean/median calculations
    - JSON parsing for multi-value angle fields
    - Markdown report generation with tables
    - Graceful degradation for missing data

file_tracking:
  created:
    - tools/youtube-analytics/performance_report.py
  modified:
    - tools/youtube-analytics/performance.py
    - .claude/commands/analyze.md

decisions:
  - key: min_count_default
    choice: "1 for reports, 2 for pattern detection"
    rationale: Show all data in reports but require 2+ for statistical insights
  - key: insight_generation
    choice: Compare best vs worst performers with ratio
    rationale: Actionable "X converts Nx better than Y" format
  - key: report_save_path
    choice: "channel-data/patterns/PERFORMANCE-REPORT.md"
    rationale: Aligns with existing patterns folder, easy to find

metrics:
  duration: 3 minutes
  completed: 2026-02-02
---

# Phase 19 Plan 02: Pattern Analysis Summary

**One-liner:** Report generator showing which topic types and content angles correlate with highest subscriber conversion rates.

## What Was Built

### 1. Performance Report Generator (performance_report.py)

New module providing aggregation and reporting functions:

**Aggregation functions:**
- `aggregate_by_topic(videos, min_count)` - Groups videos by topic type, calculates avg/median conversion, total subs
- `aggregate_by_angle(videos, min_count)` - Groups by angle (handles multi-angle videos), same stats
- `identify_top_converters(videos, n)` - Returns top N by conversion rate
- `identify_conversion_patterns(topic_stats, angle_stats)` - Generates actionable insight strings

**Report generation:**
- `generate_performance_report()` - Full markdown report with tables and recommendations
- `save_report(report, path)` - Write to channel-data/patterns/PERFORMANCE-REPORT.md

**Report structure:**
```markdown
# Performance Report: Subscriber Conversion Analysis

**Generated:** 2026-02-02 18:21 UTC
**Videos analyzed:** 15

## Key Insights
- Territorial topics have highest conversion: 0.85 subs/100 views (5 videos)
- Legal angle correlates with strong conversion: 0.92 subs/100 views

## Conversion by Topic Type
| Topic | Videos | Avg Conversion | Median | Total Subs |

## Conversion by Angle
| Angle | Videos | Avg Conversion | Median | Total Subs |

## Top Converters
| Rank | Title | Conversion | Views | Subs Gained |

## Recommendations
- [ ] Prioritize territorial topics for subscriber growth
- [ ] Use legal angle in upcoming videos
```

### 2. CLI Extensions (performance.py)

Added new commands to existing CLI:

```bash
python performance.py --report              # Generate full report to stdout
python performance.py --report --save       # Generate and save to file
python performance.py --by-topic            # Table of topics with conversion rates
python performance.py --by-angle            # Table of angles with conversion rates
```

New helper functions:
- `print_topic_aggregation()` - Console table for topic stats
- `print_angle_aggregation()` - Console table for angle stats

Updated help text with organized command categories (Data Commands, Report Commands).

### 3. Documentation Updates (analyze.md)

Added "Related Tools" section to /analyze command showing:
- How to fetch performance data for all videos
- How to view topic and angle aggregations
- How to generate and save full report
- What the performance report shows

## Integration Points

### From Phase 19-01
```python
from database import KeywordDB
db.get_all_video_performance()  # For report generation
```

### From performance_report.py to performance.py
```python
from performance_report import (
    generate_performance_report,
    aggregate_by_topic,
    aggregate_by_angle,
    save_report
)
```

## Commits

| Hash | Message |
|------|---------|
| 80227bd | feat(19-02): create performance report generator |
| cf7de92 | feat(19-02): extend performance CLI with report commands |
| 5458dee | docs(19-02): add performance tools to /analyze command |

## Files Changed

| File | Change |
|------|--------|
| tools/youtube-analytics/performance_report.py | New report generator (487 lines) |
| tools/youtube-analytics/performance.py | Added CLI commands (+205 lines) |
| .claude/commands/analyze.md | Added Related Tools section |

## Verification Results

All verification checks passed:
1. performance_report.py imports successfully
2. aggregate_by_topic returns dict with topic -> stats mapping
3. aggregate_by_angle returns dict with angle -> stats mapping
4. generate_performance_report produces valid markdown
5. CLI --report outputs full report
6. CLI --by-topic shows topic aggregation table
7. CLI --by-angle shows angle aggregation table
8. Report includes actionable recommendations

## Success Criteria Met

- **PERF-02 complete:** User can see which topic types correlate with high conversion via --by-topic and report
- **PERF-03 complete:** User can see which angles correlate with high conversion via --by-angle and report
- Report provides ranked insights with recommendations
- CLI is intuitive with clear help text
- Integration with existing workflow documented

## Deviations from Plan

None - plan executed exactly as written.

## Next Steps

**Phase 19 complete.** Performance data foundation ready for:

1. **User action required:** Populate database with:
   ```bash
   python tools/youtube-analytics/performance.py --fetch-all
   ```

2. **Generate report:**
   ```bash
   python tools/youtube-analytics/performance.py --report --save
   ```

3. **Future integration:** /next command can use this data to:
   - Prioritize topics that historically convert well
   - Recommend angles based on subscriber growth patterns
   - Balance opportunity scores with proven performance
