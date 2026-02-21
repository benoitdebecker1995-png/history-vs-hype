# Phase 44: Analytics Backfill & Feedback Loop - Context

**Gathered:** 2026-02-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Populate the analytics DB from all existing channel data (POST-PUBLISH-ANALYSIS files + YouTube API), generate a channel insights report, and auto-surface channel-specific insights during video production commands. Topic recommendations incorporate updated performance data.

</domain>

<decisions>
## Implementation Decisions

### Backfill scope & sources
- Import ALL POST-PUBLISH-ANALYSIS files (both in project folders and channel-data/analyses/)
- Enrich with YouTube API data where available — parse analysis files first, then layer on API metrics
- Include all videos 2+ minutes (exclude Shorts), even those without POST-PUBLISH-ANALYSIS files — use YouTube API to create entries
- Idempotent + update: safe to re-run anytime, upserts existing records with latest API data

### Insight surfacing behavior
- Surface ALL insight types: retention patterns, topic performance, and format insights
- Insights are advisory, not prescriptive — guide experimentation, don't constrain it
- Surface insights during ALL production commands: /script, /prep, /publish, /research --new
- Generate a standalone channel insights report file (like youtube-intelligence.md) AND load it as context during production commands
- Key principle from user: "I want insights but also keep experimenting until I find a winning formula" — insights inform, never dictate

### Topic recommendation updates
- Balance proven patterns with experimentation: boost topics matching successful categories, but also surface novel/underexplored opportunities
- Composite score blending views, retention, and subscriber conversion
- Show reasoning for each recommendation — "similar to your Essequibo video (23K views, 19 subs)"

### Command design
- Per-video progress during backfill: "Importing Essequibo (1/15)... done"

### Claude's Discretion
- Incomplete data handling threshold (how sparse is too sparse to import)
- Whether to use existing analytics.db or create new consolidated DB
- Confidence flagging for insights (strong signal vs early signal)
- Insights presentation format (brief summary before script + silent agent context, or other)
- Recency weighting for topic recommendations (~15 videos, channel is evolving)
- Command structure: whether backfill is /analyze --backfill, standalone, or other
- Where insights report command lives (/patterns --insights, /analyze --insights, or other)
- Auto-add on /analyze vs manual re-run for new videos
- Dry-run mode: whether it adds value given idempotent design
- Data quality warnings in backfill output
- Auto-regeneration of insights report after /analyze runs
- Whether to also parse CHANNEL_ANALYTICS_MASTER.md and CSV files

</decisions>

<specifics>
## Specific Ideas

- User wants to keep experimenting with formats and topics — insights should encourage range, not lock into proven formulas
- Existing POST-PUBLISH-ANALYSIS files are scattered: 6 in video-projects/_IN_PRODUCTION/*/POST-PUBLISH-ANALYSIS.md, 4 in channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md
- ~15 published videos total, ~10 have analysis files — backfill should cover all 2min+ videos
- Existing analytics infrastructure: tools/youtube-analytics/ has ~30 Python files including patterns.py, performance.py, feedback.py, topic_strategy.py, analyze.py
- YouTube Intelligence Engine (Phase 43) already generates youtube-intelligence.md — channel insights report should complement, not duplicate

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 44-analytics-backfill-feedback-loop*
*Context gathered: 2026-02-21*
