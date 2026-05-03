---
description: Run all remaining analytics analyses — geography, search terms, comments, retention curves, velocity, CTR by source, end screens
model: opus
---

# /deep-analytics — Run All Remaining Video Analytics

Execute all 7 remaining analytics analyses to completion. Build tools, fetch data, generate reports, write interpreted findings, wire actionable results into existing tools, and save memory files.

## Context

Previous analyses already completed (DO NOT redo):
- Title CTR patterns (niche-validated, 388 videos)
- Thumbnail niche benchmark (650 videos, 14 channels)
- Hook-retention correlation
- Retention-to-script content type mapping (42 videos, 4200 data points) → `retention_analysis.py`
- Description SEO benchmark (150 descriptions) → `description_analyzer.py`
- Competitor script patterns (15 transcripts, 5 channels)
- SRT pacing-to-retention (non-finding: pacing ≠ retention driver) → `pacing_analysis.py`
- Traffic source analysis (48 videos) → `traffic_analysis.py`

## Analyses To Run (all 7)

### Analysis 1: Audience Geography (HIGH IMPACT)
**Tool:** `tools/youtube_analytics/geography_analysis.py`
**API:** YouTube Analytics — `dimensions=country`, `filters=video==VIDEO_ID`, `metrics=views,estimatedMinutesWatched,subscribersGained`
**Questions to answer:**
- Which countries watch which topic types?
- Which geographic monopolies (from `GEOGRAPHIC_MONOPOLY_TARGETS` in `tools/topic_pipeline.py`) are actually converting?
- Does country mix correlate with retention or subscriber conversion?
- Which videos have the most international (non-US/UK) audience?
**Report:** `channel-data/patterns/GEOGRAPHY-ANALYSIS.md`
**Wire findings into:** `topic_pipeline.py` (validate/update geo monopoly scores), `recommender.py` (country-weighted recommendations)

### Analysis 2: Search Term Analysis (HIGH IMPACT)
**Tool:** `tools/youtube_analytics/search_term_analysis.py`
**API:** YouTube Analytics — `dimensions=insightTrafficSourceDetail`, `filters=video==VIDEO_ID;insightTrafficSourceType==YT_SEARCH`, `metrics=views,estimatedMinutesWatched`
**Questions to answer:**
- What exact search queries bring people to each video?
- Are there title-search mismatches (people search X but title says Y)?
- What untapped search terms could be added to descriptions?
- Which search terms have the highest watch time per view (= best audience fit)?
**Report:** `channel-data/patterns/SEARCH-TERM-ANALYSIS.md`
**Wire findings into:** `/publish` description generation (keyword suggestions), `METADATA-CHECKLIST.md` (search term optimization rules)

### Analysis 3: Comment Engagement Analysis (HIGH IMPACT)
**Tool:** `tools/youtube_analytics/comment_analysis.py`
**API:** YouTube Data API v3 — `commentThreads.list(videoId=VIDEO_ID, part='snippet', maxResults=100, order='relevance')`
**Also check:** `tools/youtube_analytics/comments.py` (may already exist — read first, extend if needed)
**Questions to answer:**
- Which videos generate the most comments per view? (engagement rate)
- What topics do viewers request in comments? (demand signal)
- What questions do viewers ask? (FAQ = future video ideas)
- Which comment sentiments correlate with subscriber conversion?
**Report:** `channel-data/patterns/COMMENT-ENGAGEMENT-ANALYSIS.md`
**Wire findings into:** `channel-data/TOPIC-PIPELINE.md` (viewer-requested topics), `recommender.py` (comment engagement as scoring signal)

### Analysis 4: Retention Curve Shape Classification (MEDIUM IMPACT)
**Tool:** `tools/youtube_analytics/curve_shape_analysis.py`
**Data:** Retention curves already cached in `_retention_cache/` (from `retention_analysis.py`). Use `--cached` mode.
**Classification:** For each video's 100-point retention curve, classify the SHAPE:
- **"cliff"** — sharp early drop (>30% loss in first 10%), then relatively flat
- **"slow_burn"** — gradual linear decline throughout
- **"bump"** — mid-video recovery (retention increases at some point after initial drop)
- **"plateau"** — drops early, then holds nearly flat for extended period
**Questions to answer:**
- Which curve shapes correlate with higher Suggested/Related traffic? (from `traffic_analysis.py` data)
- Which shapes correlate with higher total views?
- Do topic types produce different curve shapes?
- Does hook type predict curve shape?
**Report:** `channel-data/patterns/RETENTION-CURVE-SHAPES.md`
**Wire findings into:** `structure-checker-v2.md` (curve shape prediction), `script-writer-v2.md` (structural patterns that produce "bump" curves)

### Analysis 5: First 48-Hour Velocity (MEDIUM IMPACT)
**Tool:** `tools/youtube_analytics/velocity_analysis.py`
**API:** YouTube Analytics — `dimensions=day`, `filters=video==VIDEO_ID`, `metrics=views,estimatedMinutesWatched,subscribersGained`, `startDate=PUBLISH_DATE`, `endDate=PUBLISH_DATE+7`
**Questions to answer:**
- How fast do impressions ramp in the first 48 hours?
- Do some videos get a delayed algorithm push (day 3-7 spike)?
- Which topic types get the fastest initial velocity?
- Does publishing day affect velocity curve shape?
- Is there a correlation between first-48h velocity and total lifetime views?
**Report:** `channel-data/patterns/VELOCITY-ANALYSIS.md`
**Wire findings into:** `SWAP-PROTOCOL.md` (refine 48h swap trigger), `DAY_SCORES` in `preflight/scorer.py`

### Analysis 6: CTR by Traffic Source (LOWER IMPACT)
**Tool:** `tools/youtube_analytics/ctr_by_source_analysis.py`
**API:** YouTube Analytics — `dimensions=insightTrafficSourceType`, `metrics=views,impressions` (if impressions available per source)
**Note:** YouTube Analytics may not provide impressions broken down by traffic source. Check API capabilities first. If not available, use the `_traffic_sources.json` data + overall CTR from POST-PUBLISH-ANALYSIS files to estimate.
**Questions to answer:**
- Do titles perform differently in Search vs Browse vs Suggested?
- Are we optimizing titles for the wrong context?
- Which traffic sources have the highest CTR?
**Report:** `channel-data/patterns/CTR-BY-SOURCE-ANALYSIS.md`
**Wire findings into:** Title scoring context notes

### Analysis 7: End Screen Click-Through (LOWER IMPACT)
**Tool:** `tools/youtube_analytics/endscreen_analysis.py`
**API:** YouTube Analytics — `metrics=annotationClickThroughRate,annotationImpressions,annotationClicks` OR card/endscreen metrics if available
**Note:** Check which end screen metrics the API actually exposes. May need `cardClickRate`, `cardImpressions`.
**Questions to answer:**
- Which videos successfully send traffic to other videos?
- Which topic pairings (source video → end screen target) get the most clicks?
- What's the average end screen CTR? Is it worth optimizing?
**Report:** `channel-data/patterns/ENDSCREEN-ANALYSIS.md`
**Wire findings into:** `/publish` (end screen recommendations), `/prep` (edit guide end screen suggestions)

## Execution Instructions

1. **Read existing code first.** Before building each tool, read:
   - `tools/youtube_analytics/retention_analysis.py` — patterns for SRT matching, API calls, caching
   - `tools/youtube_analytics/traffic_analysis.py` — patterns for traffic source API calls
   - `tools/youtube_analytics/auth.py` — authentication pattern
   - `tools/youtube_analytics/analytics.db` — schema (video metadata, topic types)
   - `tools/logging_config.py` — logging pattern

2. **Run analyses 1-3 in parallel** (independent API calls, highest impact). Then 4-5. Then 6-7.

3. **For each analysis:**
   - Build the tool at the specified path
   - Run it to generate the report
   - Add an "Interpreted Findings" section with human-readable insights
   - Wire actionable findings into the specified target files
   - Save a memory file at `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\` with key findings
   - Update `MEMORY.md` with a summary line

4. **After all 7 complete:**
   - Run `python -m pytest tests/ --tb=short -q` to verify nothing broke
   - Give a final summary of all findings and what was wired where

## Quality Standards
- Every tool must run without errors
- Every report must have interpreted findings (not just raw data)
- Every actionable finding must be wired into at least one existing tool/agent/command
- Cache all API data so analyses can re-run with `--cached` flag
- Handle missing data gracefully (some videos may lack certain metrics)
