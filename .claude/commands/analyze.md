---
description: Run complete post-publish analysis on any video
model: sonnet
---

# /analyze - Post-Publish Video Analysis

Run comprehensive performance analysis for a published video with automated lessons.

## Usage

```
/analyze VIDEO_ID_OR_URL [--ctr VALUE] [--script PATH]
/analyze VIDEO_ID --diagnose                # Single-verdict failure diagnosis
/analyze --backfill
```

**Arguments:**
- `VIDEO_ID_OR_URL`: YouTube video ID or full URL (required, unless --backfill)
- `--ctr VALUE`: Manually provide CTR percentage from YouTube Studio (optional)
- `--script PATH`: Path to script file for section-level retention analysis (optional)
- `--diagnose`: Synthesize all signals into ONE verdict + root cause + concrete fix (closes the "I don't know why this flopped" loop)
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
python -m tools.youtube_analytics.analyze VIDEO_ID --save --markdown
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
sys.path.insert(0, 'tools/youtube_analytics')
from pathlib import Path
from backfill import run_backfill

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
from backfill import generate_channel_insights_report
result = generate_channel_insights_report(Path('.'))
if 'error' not in result:
    print(f"Channel insights updated: {result['saved_to']}")
```

This runs automatically after each `/analyze VIDEO_ID --save`. No separate flag needed.

---

## Requirements

- YouTube Analytics API configured (Phase 7)
- OAuth token valid (`tools/youtube_analytics/credentials/token.json`)

## SECTION-LEVEL RETENTION DIAGNOSTICS (`--script`)

When a script file is provided, the system maps retention drops to specific script sections and provides actionable fix recommendations.

### How It Works

1. Fetches retention curve from YouTube Analytics API
2. Parses script into H2 sections with word counts
3. Maps retention drop points to sections using word-count-based timing (150 WPM)
4. Diagnoses root causes for each drop
5. Recommends specific voice patterns from WRITING-VOICE-AND-STYLE.md PART 1 (Core Voice) and PART 5 (Techniques Toolkit)

### Output

- **Retention Drop Map:** Table showing which sections lost viewers, with magnitude and severity
- **Section Diagnostics:** Root cause analysis with specific pattern recommendations
- Each recommendation references exact WRITING-VOICE-AND-STYLE.md PART 1 (Core Voice) and PART 5 (Techniques Toolkit) patterns

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

### PLAYBOOK UPDATE (Auto-Update — retention playbook)

After each video analysis with the --script flag, the retention playbook is automatically updated:

```bash
# Manual update (standalone)
python -m tools.youtube_analytics.playbook_synthesizer --update
```

This re-synthesizes the retention playbook from all available retention data, incorporating patterns from the newly analyzed video.

**Automatic trigger:** analyze.py automatically updates the playbook after `/analyze VIDEO_ID --script PATH` completes section diagnostics. No separate flag needed.

---

---

## DIAGNOSE MODE (`--diagnose`) — Why did this video fail?

**Why this exists:** The most expensive failure mode is shipping a video, watching it underperform, and not knowing whether the title flopped, the hook bailed, the topic was wrong, or all three. `/analyze --diagnose` synthesizes every available signal into ONE verdict + ONE root cause + ONE concrete fix.

**Auto-triggers:** When the standard `/analyze` run determines the video is below channel benchmark on either CTR (<channel median - 0.5%) OR retention (median <25%), the diagnose flow runs automatically. Manual invocation: `/analyze VIDEO_ID --diagnose`.

### Step 1: Collect every signal

Run these in parallel (all already exist as tools — no new code needed):

```bash
# Performance vs channel + niche
python -m tools.youtube_analytics.analyze VIDEO_ID --json
python -m tools.youtube_analytics.performance --video-id VIDEO_ID --json

# Retention curve + drop classification
python -m tools.youtube_analytics.retention --video-id VIDEO_ID --classify

# Title score vs measured CTR
python -m tools.title_scorer "$TITLE" --topic $TOPIC --json

# Hook score vs measured retention at 0:30
python -m tools.research.hook_scorer --score-from-script SCRIPT.md --json

# Niche benchmark (CTR + retention) for this topic type
python -m tools.youtube_analytics.benchmarks --topic $TOPIC --json

# Traffic source breakdown (was it search-anchored or browse-dependent?)
python -m tools.youtube_analytics.traffic_analysis --video-id VIDEO_ID --json
```

### Step 2: Compute the bleed map

For each layer of the funnel, compare the video's measured value to its expected value (channel median + niche benchmark) and record the gap:

| Layer | Signal | Compare against | Gap = "bleed" |
|-------|--------|----------------|---------------|
| **Impressions** | Search/browse impressions in 48h | Channel 48h median by topic type | Low impressions = topic/SEO bleed |
| **CTR** | Measured CTR % | (channel median for topic) AND (niche benchmark for topic) | Low CTR = packaging bleed |
| **Hook (0:00-1:00)** | Retention at 60s | 90% baseline (channel median = 88%) | High drop = hook bleed |
| **Body (1:00-end)** | Retention at midpoint | 50% baseline (channel median ~50%) | High drop = pacing/evidence bleed |
| **Subscriber conversion** | Subs gained / views | Channel median by topic type | Low = topic-fit bleed (delivered ≠ promised audience) |

### Step 3: Identify the LOAD-BEARING failure

Most underperforming videos fail at exactly one layer — the rest are downstream symptoms. Pick the single highest-impact gap:

- **If impressions are low** → topic was wrong (no demand) OR title has zero search hooks → root cause is upstream of packaging
- **If impressions normal but CTR low** → packaging bled (title or thumbnail didn't earn the click)
- **If CTR normal but 0:00-1:00 retention drops >15% past baseline** → hook bled (title earned the click, hook didn't deliver)
- **If hook held but body collapses** → pacing/evidence bleed (script-side problem)
- **If everything held but subscriber conversion is low** → topic-fit bleed (right audience didn't find lasting value)

### Step 4: Output the verdict block

Single block, no scrolling required. Format:

```
=== /analyze --diagnose VERDICT ===

VIDEO: [title] (published [date], [N] views in [age] days)
PERFORMANCE: [percentile in channel — top 10% / above median / below median / bottom 25%]

LOAD-BEARING FAILURE: [one of: TOPIC / PACKAGING / HOOK / BODY / TOPIC-FIT]

THE BLEED:
  Impressions:     [measured] vs [expected]   — [PASS / GAP: -X%]
  CTR:             [measured] vs [expected]   — [PASS / GAP: -X%]
  Hook (0:00-1:00): [measured] vs [expected]   — [PASS / GAP: -X% with timestamp]
  Body (mid):      [measured] vs [expected]   — [PASS / GAP: -X% with timestamp]
  Sub conversion:  [measured] vs [expected]   — [PASS / GAP: -X%]

ROOT CAUSE (one sentence):
  [Specific decision that caused the load-bearing failure. Examples: "Title promised 'forensic close-read' but hook delivered general overview — packaging bled." / "Topic had no search demand: 'X' has <100 monthly searches — impressions bled." / "Hook used abstract opening ('To understand...') without a concrete date or named person — hook bled at 0:38."]

CONCRETE FIX (one action for next video):
  [Specific, copy-pasteable. Examples: "Lead next title with a date or named person — your top 3 CTR titles all do." / "Stop opening with 'To understand X' — your hooks under 30% retention at 0:30 all start abstractly." / "Pick topics with VidIQ search volume >1K — 0/3 of your <500-search videos broke 1K views."]

PATTERN CHECK (cross-video):
  [If this failure mode has happened before, surface the streak: "This is the 4th video in 6 months that failed on PACKAGING — title-hook coherence is the channel's #1 unfixed leak." / If first time: "Isolated incident — no cross-video pattern yet."]

=== END VERDICT ===
```

### Step 5: Persist the diagnosis

Append the verdict block to:
- `POST-PUBLISH-ANALYSIS.md` in the project folder (under `## DIAGNOSIS` heading)
- `channel-data/DIAGNOSIS-LOG.md` (chronological log of failure modes — fuels Step 4 "Pattern check" on future runs)

### Step 6: Wire the next /script

If the failure mode is one of {PACKAGING, HOOK, TOPIC-FIT}, prepend the diagnosis verdict to the next `/script --new` invocation as additional context. The next script gets generated with explicit awareness of the last failure mode — this is the feedback loop the channel was missing.

**Implementation note:** the next `/script --new` reads `channel-data/DIAGNOSIS-LOG.md` (last 3 entries) as part of its PRE-SCRIPT INTELLIGENCE step (already established at line 226 of `script.md`). Add a one-line read of DIAGNOSIS-LOG.md alongside channel-insights.md.

**Graceful degradation:** If any of the underlying tools fail (API timeout, missing data), surface partial results with a note: "Diagnose ran on [N of 6] signals — [verdict tentative]." Never block on missing data.

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
python -m tools.youtube_analytics.performance --fetch-all

# See which topic types convert best
python -m tools.youtube_analytics.performance --by-topic

# See which angles convert best
python -m tools.youtube_analytics.performance --by-angle

# Generate full performance report
python -m tools.youtube_analytics.performance --report --save
```

The performance report shows:
- Which topic types (territorial, ideological, colonial) have highest subscriber conversion
- Which content angles (legal, historical, political) correlate with more subscribers
- Top converting videos with their topics and angles
- Recommendations for future content based on patterns
