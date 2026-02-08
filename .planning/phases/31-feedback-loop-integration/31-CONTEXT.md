# Phase 31: Feedback Loop Integration - Context

**Gathered:** 2026-02-08
**Status:** Ready for planning

<domain>
## Phase Boundary

Past performance insights surface automatically during creation. Parses POST-PUBLISH-ANALYSIS markdown files into structured database records, extracts success/failure patterns from top/bottom performers, and surfaces relevant insights during /script, /prep, and /publish generation without manual lookup.

</domain>

<decisions>
## Implementation Decisions

### Parsing Strategy
- Best-effort parsing for existing analysis files (regex/heuristic matching for known fields)
- Create canonical template for all future POST-PUBLISH-ANALYSIS files (consistent structure improves parsing over time)
- Extract both numeric metrics (CTR, retention rate, drop points, views, subscriber conversion) AND qualitative insights (what worked, what failed, lessons learned)
- Auto-parse when /analyze generates a new analysis file
- Backfill command to import all existing analysis files at once (`python feedback.py backfill`)

### Insight Surfacing
- Automatic preamble before script/prep/publish generation: show 3-5 relevant insights from past videos
- Matching strategy: category-specific insights first (by topic type), then 1-2 universal insights that apply to all videos (e.g., pacing patterns, engagement hooks)
- Keyword/entity similarity as secondary matching signal (overlapping entities between current topic and past videos)
- Surface insights during ALL creation commands: /script, /prep, and /publish — each gets category-appropriate insights
  - /script: content and pacing insights (retention drops, section structure, hook effectiveness)
  - /prep: production insights (B-roll density, edit pacing, visual evidence patterns)
  - /publish: CTR and title insights (which title formulas worked, thumbnail styles, metadata patterns)

### Pattern Extraction
- Compare both content attributes (topic type, angle, script length, entity density, section count) AND production attributes (thumbnail style, title formula, video length, pacing score, B-roll density)
- Store patterns in both database (for querying during /script) and markdown report (for human review)
- Database records for machine-readable querying, PATTERNS.md for browsable human review

### Query Interface
- Standalone CLI for power queries: `python feedback.py query --topic territorial --metric retention`
- Extend /patterns command with feedback data (aggregated insights view)
- Output: default table format for terminal, --markdown flag for full report (matches existing tool patterns like benchmarks.py)
- Query by individual video (`--video VIDEO_ID`) OR by category (`--topic territorial`) with different output for each

### Claude's Discretion
- Storage location: Claude picks best approach (likely extend keywords.db given Phase 27 section_feedback table already exists)
- Insight depth: Claude decides balance of numbers vs. qualitative based on available data
- Performance threshold: Claude determines what counts as "high-performing" (likely top quartile or above-average, adapting to ~10 video catalog)
- Pattern extraction trigger: Claude determines optimal timing (after each /analyze vs. periodic)
- Comparison views: Claude picks most useful presentation for query results (side-by-side vs. list)

</decisions>

<specifics>
## Specific Ideas

- Phase 27 already created section_feedback table and feedback columns in video_performance (retention_drop_point, discovery_issues, lessons_learned as JSON) — this phase populates those tables
- Existing /analyze command generates POST-PUBLISH-ANALYSIS files — hook into that output pipeline
- Pattern extraction should integrate with existing pattern_extractor.py from Phase 20 where possible
- BENCHMARKS_AVAILABLE / DISCOVERY_AVAILABLE graceful import pattern should be followed (FEEDBACK_AVAILABLE flag)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 31-feedback-loop-integration*
*Context gathered: 2026-02-08*
