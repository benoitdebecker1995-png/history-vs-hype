---
description: Cross-Video Pattern Analysis
model: sonnet
---

# /patterns - Cross-Video Pattern Analysis

Analyze patterns across all published videos to identify what's working.

## Usage

```
/patterns [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| (none) | Generate all pattern reports |
| `--topic` | Topic performance analysis only |
| `--title` | Title/thumbnail patterns only |
| `--monthly` | Current month summary only |
| `--last N` | Filter to last N days |

## What It Does

1. **Collects** all POST-PUBLISH-ANALYSIS files from project folders
2. **Tags** videos automatically by topic (territorial, ideological, colonial, etc.)
3. **Aggregates** performance metrics by topic, title structure, thumbnail type
4. **Generates** insights-first reports with actionable recommendations
5. **Surfaces** feedback loop insights from POST-PUBLISH-ANALYSIS parsed data

## Reports Generated

### TOPIC-ANALYSIS.md
- Performance breakdown by topic type
- Winners (above average on both CTR AND retention)
- Anti-patterns (below average on both)
- Sample size warnings

### TITLE-PATTERNS.md
- Title structure correlations (colon, question mark, year, etc.)
- Detected title patterns (e.g., "Why [X] Is [Y]")
- Thumbnail type performance
- High/low performer examples

### MONTHLY-{YYYY}-{MM}.md
- Month-at-a-glance stats
- Best performer highlight
- Topic breakdown for the month
- All videos listed

### FEEDBACK-PATTERNS.md (NEW - Phase 31)
- Success patterns from high-performing videos (above-average conversion by topic)
- Failure patterns from low-performing videos (below-average)
- Content attribute analysis (topic type, angles, retention)
- Production attribute analysis (thumbnails, titles, pacing)
- Recommendations based on pattern extraction

## Examples

```bash
# Generate all reports (recommended)
/patterns

# Just topic analysis
/patterns --topic

# See what worked in December 2025
/patterns --monthly 12 2025

# Patterns from last 90 days only
/patterns --last 90
```

## Output Location

Reports saved to: `channel-data/patterns/`

## Execution

When user runs `/patterns` (no flags), run both existing patterns and feedback patterns:

```bash
python -m tools.youtube_analytics.patterns --all
```

Then also run feedback patterns:
```bash
python -m tools.youtube_analytics.feedback patterns
```

Display the key insights from all reports in the response.

For specific options:
- `/patterns --topic` -> `python -m tools.youtube_analytics.patterns --topic-report`
- `/patterns --title` -> `python -m tools.youtube_analytics.patterns --title-report`
- `/patterns --monthly` -> `python -m tools.youtube_analytics.patterns --monthly`
- `/patterns --last 30` -> `python -m tools.youtube_analytics.patterns --last 30 --all`

For feedback patterns specifically:
- `/patterns --feedback` -> `python -m tools.youtube_analytics.feedback patterns`
- `/patterns --feedback --markdown` -> `python -m tools.youtube_analytics.feedback patterns --markdown`

## Related Commands

- `/analyze VIDEO_ID` - Single video analysis (feeds into patterns)
- `/status` - Project status overview

## Note on Data Quality

Pattern analysis requires POST-PUBLISH-ANALYSIS files to exist. Run `/analyze` on published videos to build up the data set. Minimum 3 videos per category for reliable patterns.
