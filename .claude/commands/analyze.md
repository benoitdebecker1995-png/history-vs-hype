---
description: Run complete post-publish analysis on any video
model: sonnet
---

# /analyze - Post-Publish Video Analysis

Run comprehensive performance analysis for a published video with automated lessons.

## Usage

```
/analyze VIDEO_ID_OR_URL [--ctr VALUE] [--script PATH]
/analyze --backfill
```

**Arguments:**
- `VIDEO_ID_OR_URL`: YouTube video ID or full URL (required, unless --backfill)
- `--ctr VALUE`: Manually provide CTR percentage from YouTube Studio (optional)
- `--script PATH`: Path to script file for section-level retention analysis (optional)
- `--backfill`: Run full analytics backfill (imports JSON + markdown + reclassifies + generates insights)

## What It Does

1. **Fetches performance data** via YouTube Analytics API:
   - Views, watch time, likes, comments, shares
   - Subscriber gain/loss
   - Retention curve with drop-off detection
   - CTR (if available via API, otherwise prompts for manual input)

2. **Calculates benchmarks** against channel average:
   - Compares this video vs. last 10 videos
   - Shows above/below/at average for each metric

3. **Analyzes comments** (Questions, Objections, Requests):
   - Fetches top 100 comments by relevance
   - Categorizes into actionable buckets

4. **Generates automated lessons**:
   - Observations about what the data shows
   - Actionable takeaways for future videos

5. **Saves analysis** to video's project folder:
   - Attempts to find matching project in `video-projects/`
   - Falls back to `channel-data/analyses/` if not found

## Example

```
/analyze wCFReiCGiks
/analyze https://youtu.be/wCFReiCGiks
/analyze wCFReiCGiks --ctr 4.2
/analyze wCFReiCGiks --script video-projects/_ARCHIVED/1-belize-2025/SCRIPT.md
```

## Output

Creates `POST-PUBLISH-ANALYSIS.md` containing:
- Quick summary (above/below benchmarks)
- Performance metrics table with comparisons
- Retention analysis with drop-off points
- All significant drop-off points with timestamps
- Categorized comments (full list under each category)
- Lessons: observations and actionable takeaways

## Execution

When user runs `/analyze VIDEO_ID`, execute:

```bash
cd tools/youtube-analytics && python analyze.py VIDEO_ID --save --markdown
```

Then:
1. Display the markdown output to user
2. Confirm where file was saved
3. If CTR unavailable, suggest: "Add CTR with: /analyze VIDEO_ID --ctr VALUE"

## BACKFILL ANALYTICS (`--backfill`)

Run the full analytics backfill pipeline to populate the DB from all existing channel data.

```python
import sys
sys.path.insert(0, '.')
from pathlib import Path
from tools.youtube_analytics.backfill import run_backfill

project_root = Path('.')
result = run_backfill(project_root)

print(f"JSON import: {result['imported_json']} videos")
print(f"Markdown import: {result['imported_md']} analyses")
print(f"Reclassified: {result['reclassified']} topics")
print(f"Insights saved to: {result.get('insights_path', 'N/A')}")
```

This is safe to re-run anytime (idempotent upsert design).

---

## Auto-Regenerate Channel Insights

After saving any analysis, regenerate the channel insights report to keep it current:

```python
from tools.youtube_analytics.backfill import generate_channel_insights_report
result = generate_channel_insights_report(Path('.'))
if 'error' not in result:
    print(f"Channel insights updated: {result['saved_to']}")
```

This runs automatically after each `/analyze VIDEO_ID --save`. No separate flag needed.

---

## Requirements

- YouTube Analytics API configured (Phase 7)
- OAuth token valid (`tools/youtube-analytics/credentials/token.json`)

## SECTION-LEVEL RETENTION DIAGNOSTICS (`--script`)

When a script file is provided, the system maps retention drops to specific script sections and provides actionable fix recommendations.

### How It Works

1. Fetches retention curve from YouTube Analytics API
2. Parses script into H2 sections with word counts
3. Maps retention drop points to sections using word-count-based timing (150 WPM)
4. Diagnoses root causes for each drop
5. Recommends specific voice patterns from STYLE-GUIDE.md Part 6

### Output

- **Retention Drop Map:** Table showing which sections lost viewers, with magnitude and severity
- **Section Diagnostics:** Root cause analysis with specific pattern recommendations
- Each recommendation references exact STYLE-GUIDE.md Part 6 patterns

### Requirements

- Video must have retention data (published and >48 hours old)
- Script file must be a markdown file with H2 section headings

### Example

```bash
/analyze wCFReiCGiks --script video-projects/_ARCHIVED/1-belize-2025/SCRIPT.md
```

Output includes:
- Retention Drop Map table (sorted by severity: HIGH > MEDIUM > LOW)
- Diagnostics with root causes (abstract opening, missing causal chains, no evidence introduction, etc.)
- Recommended fixes with specific voice patterns to apply
- Insertion hints for where to add patterns

### Anti-Patterns Detected

- Abstract opening (starts with "The concept", "To understand")
- Missing causal chains (no "consequently", "thereby", "which meant that")
- No evidence introduction (no "according to", page numbers, quotes)
- Missing modern relevance (no "today", "2024", "2025", etc.)
- Long sections without pacing variation
- Weak opening hook (section-specific for intro drops)

### PLAYBOOK UPDATE (Auto-Update Part 9)

After each video analysis with the --script flag, the retention playbook (STYLE-GUIDE.md Part 9) is automatically updated:

```bash
# Manual update (standalone)
python tools/youtube-analytics/playbook_synthesizer.py --update
```

This re-synthesizes Part 9 from all available retention data, incorporating patterns from the newly analyzed video.

**Automatic trigger:** analyze.py automatically updates Part 9 after `/analyze VIDEO_ID --script PATH` completes section diagnostics. No separate flag needed.

---

## Note on CTR

CTR may not be available via YouTube Analytics API (known limitation). If unavailable:
- Analysis shows "Check YouTube Studio manually"
- Use `--ctr VALUE` to manually provide the CTR percentage
- CTR can be found in: YouTube Studio > Analytics > Reach tab

## Related Commands

- `/status` - Check project state
- `/engage` - Handle comments, corrections
- `/publish` - YouTube metadata optimization

## Related Tools

After running `/analyze` on multiple videos, use the performance tools to identify patterns:

```bash
# Fetch performance data for all published videos
python tools/youtube-analytics/performance.py --fetch-all

# See which topic types convert best
python tools/youtube-analytics/performance.py --by-topic

# See which angles convert best
python tools/youtube-analytics/performance.py --by-angle

# Generate full performance report
python tools/youtube-analytics/performance.py --report --save
```

The performance report shows:
- Which topic types (territorial, ideological, colonial) have highest subscriber conversion
- Which content angles (legal, historical, political) correlate with more subscribers
- Top converting videos with their topics and angles
- Recommendations for future content based on patterns
