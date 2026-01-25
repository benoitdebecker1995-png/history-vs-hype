# Phase 9: Post-Publish Analysis - Context

**Gathered:** 2026-01-25
**Status:** Ready for planning

<domain>
## Phase Boundary

User can run a single command to get comprehensive analysis of any video's performance with lessons logged. Analysis pulls from Phase 8 data scripts (metrics, retention, CTR) plus YouTube Data API for comments. Report is saved in the video's project folder.

**Requirements covered:**
- ANALYSIS-01: Command to trigger post-publish analysis
- ANALYSIS-02: CTR comparison vs. channel average
- ANALYSIS-03: Retention drop-off points identified
- ANALYSIS-04: Comments pulled and categorized
- ANALYSIS-05: Lessons captured in structured format
- ANALYSIS-06: Analysis linked to video project folder

</domain>

<decisions>
## Implementation Decisions

### Command Invocation
- Slash command (`/analyze`) wraps Python script — either interface works
- Accept YouTube video URL in addition to raw video ID — extract ID automatically
- CTR data: **Find a way to get this** — user wants it despite API limitation. Research alternatives (scraping YouTube Studio, browser automation, manual prompt as last resort)

### Report Structure
- Retention analysis: Visual ASCII curve + list of all significant drop-off points with timestamps
- Benchmarks: Include BOTH channel averages AND comparison to last 5-10 videos
- Each metric should show: this video's value, channel average, recent average, and whether above/below

### Lessons Capture
- Fully automated by Claude — no manual editing needed
- Include both styles:
  - Observations about this video ("Hook retained 85% through first 30 seconds")
  - Actionable takeaways for future ("Consider shorter intros for territorial topics")
- Cross-video accumulation is Phase 10's job — keep lessons per-video only here

### Comment Categorization
- Three categories as specified: Questions, Objections, Requests
- Volume: Sample approach — all comments if under 100, top 100 (by likes/replies) if more
- Display: Full list of comments under each category (not just counts/examples)

### Claude's Discretion
- Date range handling (default to video lifetime or offer flags)
- Report file location (project folder vs central analytics folder vs both)
- Output format (Markdown only vs JSON + Markdown)
- Number of lessons to generate (based on what data reveals)
- Whether to flag comments that need creator response

</decisions>

<specifics>
## Specific Ideas

- CTR is important to the user — even though API doesn't provide it, research alternatives before falling back to manual input
- Visual retention curve (ASCII art style) preferred over just listing numbers
- Lessons should be actionable, not just observations — "next time do X" style

</specifics>

<deferred>
## Deferred Ideas

- Cross-video lesson accumulation — Phase 10 (Pattern Recognition)
- Praise/positive feedback category for comments — keep to 3 categories for now

</deferred>

---

*Phase: 09-post-publish-analysis*
*Context gathered: 2026-01-25*
