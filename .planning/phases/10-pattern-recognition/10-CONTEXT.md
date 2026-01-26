# Phase 10: Pattern Recognition - Context

**Gathered:** 2026-01-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Cross-video pattern analysis that reveals what's working and what's not. Users can see performance breakdown by topic type, monthly summaries, and title/thumbnail correlations with CTR. This is an analysis and reporting feature, not data collection (Phase 8-9 handle that).

</domain>

<decisions>
## Implementation Decisions

### Topic Categorization
- Flexible tags per video (not single category) — e.g., "territorial + colonial + Africa"
- Auto-detection from title/description keywords
- Fixed vocabulary for consistency — predefined tag list (territorial, ideological, colonial, myth-busting, etc.)
- Override available via `--tags` flag for manual correction

### Output Format & Depth
- Insights-first presentation — lead with actionable insights, data tables as supporting evidence
- Both observations AND explicit "Recommended next actions" section
- Light statistical caveats — include sample size ("based on 4 territorial videos") but no heavy statistics
- Reports saved to `channel-data/patterns/` (MONTHLY-2026-01.md, TOPIC-ANALYSIS.md, etc.)

### Time Windows & Triggers
- Both on-demand AND auto-update after `/analyze`
- Rolling windows: last 30/90/365 days (automatically shifts)
- Minimum 3 videos for meaningful patterns (consistent with channel averages threshold)
- Monthly summaries auto-generate when a new month's video is analyzed

### Correlation Presentation
- Title analysis: structure (length, question vs statement, colons/numbers) + keyword patterns
- Thumbnail attributes pulled from project files (YOUTUBE-METADATA.md, thumbnail briefs)
- Show actual high/low performers as examples alongside pattern observations
- Combined CTR + retention view — show how patterns affect both metrics together
- "Winners" = above average on BOTH CTR and retention
- Explicit anti-pattern analysis — "Videos with X pattern averaged 40% lower CTR"
- Retention patterns analyzed per topic type (do territorial videos hold better than ideological?)

### Claude's Discretion
- Whether to include title/thumbnail suggestions for upcoming videos
- Exact fixed tag vocabulary (will propose during research/planning)
- Report section ordering and formatting details
- How to handle videos with missing thumbnail metadata

</decisions>

<specifics>
## Specific Ideas

- Pattern examples should show actual video titles/thumbnails, not abstract descriptions
- "Winning formula" concept: videos that beat channel average on both CTR and retention
- Anti-patterns explicitly called out to learn from failures
- Retention patterns by topic type answers "do territorial videos hold attention better?"

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 10-pattern-recognition*
*Context gathered: 2026-01-25*
