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

When user runs `/patterns`, execute:

```bash
cd tools/youtube-analytics && python patterns.py --all
```

Display the key insights from each report in the response.

For specific options:
- `/patterns --topic` -> `python patterns.py --topic-report`
- `/patterns --title` -> `python patterns.py --title-report`
- `/patterns --monthly` -> `python patterns.py --monthly`
- `/patterns --last 30` -> `python patterns.py --last 30 --all`

## Related Commands

- `/analyze VIDEO_ID` - Single video analysis (feeds into patterns)
- `/status` - Project status overview

## Note on Data Quality

Pattern analysis requires POST-PUBLISH-ANALYSIS files to exist. Run `/analyze` on published videos to build up the data set. Minimum 3 videos per category for reliable patterns.
