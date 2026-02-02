---
phase: 20
plan: 01
subsystem: analytics
tags: [pattern-extraction, performance, channel-strengths, python]

dependency-graph:
  requires:
    - phase-19 (video_performance table, performance.py, performance_report.py)
  provides:
    - pattern_extractor.py with 7 extraction functions
    - CLI --patterns and --strengths commands
    - WINNING-PATTERNS.md report template
  affects:
    - phase-21 (topic recommendations will use winning patterns)

tech-stack:
  added: []
  patterns:
    - aggregate-then-rank for topic/angle performance
    - strength scoring normalized 0-100
    - insight generation from comparative analysis

file-tracking:
  created:
    - tools/youtube-analytics/pattern_extractor.py
    - channel-data/patterns/WINNING-PATTERNS.md
  modified:
    - tools/youtube-analytics/performance.py

decisions:
  - pattern: strength-normalization
    choice: min(100, (category_avg / overall_avg) * 50)
    reason: Normalizes scores to 0-100 scale with 50 as baseline
  - pattern: dominant-extraction
    choice: Counter.most_common() for topics and angles
    reason: Simple, efficient, and handles ties appropriately
  - pattern: insight-generation
    choice: Compare best vs average and best vs worst
    reason: Provides actionable comparative insights

metrics:
  duration: 7 minutes
  completed: 2026-02-02
---

# Phase 20 Plan 01: Pattern Extraction Summary

**One-liner:** Pattern extractor module with 7 functions that identifies winning topics, angles, and channel strengths from video performance data.

## What Was Built

### 1. Pattern Extractor Module (pattern_extractor.py)

Created `tools/youtube-analytics/pattern_extractor.py` with 7 functions:

| Function | Purpose | Output |
|----------|---------|--------|
| `extract_topic_ranking()` | Rank topics by conversion rate | List of topic stats |
| `extract_angle_ranking()` | Rank angles by conversion rate | List of angle stats |
| `extract_top_converter_profile()` | Find shared attributes of top N | Profile dict |
| `calculate_channel_strengths()` | Normalize strength scores 0-100 | Strength dict |
| `generate_insights()` | Create actionable insight strings | List of strings |
| `extract_winning_patterns()` | Orchestrate all extraction | Complete profile |
| `generate_winning_patterns_report()` | Save markdown report | File path |

### 2. CLI Integration (performance.py)

Extended `performance.py` with new commands:

```bash
python performance.py --patterns              # Extract and display winning patterns
python performance.py --patterns --save       # Extract and save WINNING-PATTERNS.md
python performance.py --strengths             # Show channel strength assessment
```

### 3. Report Template (WINNING-PATTERNS.md)

Report sections:
- Summary with actionable insights
- Topic Ranking table (sorted by conversion)
- Angle Ranking table (sorted by conversion)
- Top Converter Profile (shared attributes)
- Channel Strengths (with ASCII progress bars)
- Recommendations checklist

## Requirements Satisfied

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| PATN-01 | DONE | `extract_topic_ranking()` + `extract_angle_ranking()` = winning pattern profile |
| PATN-02 | DONE | `calculate_channel_strengths()` returns document_heavy, academic, legal_territorial |
| PATN-03 | DONE | `extract_top_converter_profile()` identifies shared attributes |

## Key Algorithms

### Topic/Angle Ranking
```python
# Group by category, calculate stats, sort by avg_conversion DESC
for topic, videos in by_topic.items():
    ranking.append({
        'topic': topic,
        'avg_conversion': mean([v['conversion_rate'] for v in videos]),
        'count': len(videos),
        'total_subs': sum([v['subscribers_gained'] for v in videos])
    })
ranking.sort(key=lambda x: x['avg_conversion'], reverse=True)
```

### Channel Strength Normalization
```python
# Formula: min(100, (category_avg / overall_avg) * 50)
# Score of 50 = average, 100 = 2x better than average
document_heavy = min(100, ((legal_perf + historical_perf) / 2 / overall_avg) * 50)
```

### Insight Generation
```python
# Compare best topic to average
ratio = best['avg_conversion'] / avg_conversion
insights.append(f"{best['topic']} converts {ratio:.1f}x better than average")
```

## Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| `tools/youtube-analytics/pattern_extractor.py` | Created | 690 |
| `tools/youtube-analytics/performance.py` | Modified | +198 |
| `channel-data/patterns/WINNING-PATTERNS.md` | Created | 34 |

## Commits

| Hash | Type | Description |
|------|------|-------------|
| da4f490 | feat | Create pattern extractor module with 7 functions |
| a5bfa36 | feat | Extend performance.py CLI with --patterns and --strengths |
| 609e3a1 | docs | Generate sample WINNING-PATTERNS.md report |

## Usage Examples

### Extract Winning Patterns (Python)
```python
from pattern_extractor import extract_winning_patterns

profile = extract_winning_patterns()
print(f"Best topic: {profile['topic_ranking'][0]['topic']}")
print(f"Best angle: {profile['angle_ranking'][0]['angle']}")
print(f"Document-heavy score: {profile['channel_strengths']['document_heavy']}")
```

### Generate Report (CLI)
```bash
# After fetching performance data:
python performance.py --fetch-all

# Extract and save patterns:
python performance.py --patterns --save
```

### Quick Strength Check
```bash
python performance.py --strengths
```

## Edge Cases Handled

1. **Empty database** - Returns error with helpful message to run --fetch-all
2. **Limited data (<5 videos)** - Adds warning insight about unreliable patterns
3. **Missing angles** - Defaults to ['general'] when no angles found
4. **Division by zero** - Guards against zero averages in strength calculation
5. **JSON string angles** - Handles both parsed list and raw JSON string formats

## Integration Points

### Upstream (Phase 19)
- Uses `KeywordDB.get_all_video_performance()` and `get_top_converters()`
- Uses `aggregate_by_topic()` and `aggregate_by_angle()` from performance_report.py

### Downstream (Phase 21)
- `extract_winning_patterns()` provides data for topic recommendations
- Channel strengths inform production feasibility scoring
- Insights guide priority of suggested topics

## Deviations from Plan

None - plan executed exactly as written.

## Next Phase Readiness

Phase 21 (Topic Recommendations) can now:
1. Access winning pattern profile via `extract_winning_patterns()`
2. Use topic/angle rankings to score potential topics
3. Filter topics by channel strengths
4. Generate recommendations based on historical performance

---

*Summary generated after 20-01-PLAN.md completion*
