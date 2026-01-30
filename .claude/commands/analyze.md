---
description: Run complete post-publish analysis on any video
model: sonnet
---

# /analyze - Post-Publish Video Analysis

Run comprehensive performance analysis for a published video with automated lessons.

## Usage

```
/analyze VIDEO_ID_OR_URL [--ctr VALUE]
```

**Arguments:**
- `VIDEO_ID_OR_URL`: YouTube video ID or full URL (required)
- `--ctr VALUE`: Manually provide CTR percentage from YouTube Studio (optional)

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

## Requirements

- YouTube Analytics API configured (Phase 7)
- OAuth token valid (`tools/youtube-analytics/credentials/token.json`)

## Note on CTR

CTR may not be available via YouTube Analytics API (known limitation). If unavailable:
- Analysis shows "Check YouTube Studio manually"
- Use `--ctr VALUE` to manually provide the CTR percentage
- CTR can be found in: YouTube Studio > Analytics > Reach tab

## Related Commands

- `/status` - Check project state
- `/engage` - Handle comments, corrections
- `/publish` - YouTube metadata optimization
