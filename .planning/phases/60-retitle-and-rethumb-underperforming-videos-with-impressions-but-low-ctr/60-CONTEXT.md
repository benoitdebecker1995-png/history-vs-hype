# Phase 60: Retitle and Rethumb Underperforming Videos - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Execute retitle and rethumb swaps on existing videos that have impressions but low CTR. Surface the worst-performing packaging, generate better alternatives from actual video content, output a checklist for manual YouTube Studio execution, and measure results. Create a /retitle slash command to make this repeatable.

</domain>

<decisions>
## Implementation Decisions

### Selection criteria
- Claude's discretion on ranking formula (likely wasted impressions x retention to prioritize high-retention videos trapped by bad titles)
- Top 5 videos per batch — measure before doing more
- Minimum 500 impressions threshold — below that, YouTube hasn't tested the packaging enough to diagnose

### Execution workflow
- Output: Markdown SWAP-CHECKLIST.md with all swap details per video
- Each checklist entry includes: OLD TITLE (for revert), NEW TITLE, NEW DESCRIPTION (first 3 lines), THUMBNAIL CONCEPT (if needed)
- Title generation: Script-based — read actual SRT/scripts, extract thesis, generate titles from real content
- Description: Updated first 3 lines to match new title framing
- Tracking: Per-video in POST-PUBLISH-ANALYSIS.md (SWAP LOG section with date, old title, new title, pre/post CTR)

### Thumbnail strategy
- Include thumbnail concept (map type, color scheme, layout description) — user creates in Photoshop
- Auto-suggest map type from video content: split-map (vs topics), arrow-flow (movement/extraction), document-on-map (treaty/legal)
- Skip compliant thumbnails — run thumbnail_checker on current concept first. If already map-based, no face, no text: only swap the title

### Success measurement
- Re-check at 7 days post-swap (not 48h — older videos don't get the 48h push)
- Success threshold: +0.5% CTR or more
- Feed successful swap data back via ctr_ingest (Phase 61 feedback loop) — update CROSS-VIDEO-SYNTHESIS, run ingest, scores auto-update

### Rollback strategy
- If CTR drops or stays flat after 7 days: revert to original title
- SWAP-CHECKLIST always includes old title for one-click copy-paste revert
- No second-chance candidates — revert first, reassess later

### Stagger timing
- Swap all 5 on the same day — at 475 subs, videos don't compete with each other
- Measure all at the same 7-day mark for clean comparison

### Slash command: /retitle
- `/retitle` — Full pipeline: audit → generate candidates → output SWAP-CHECKLIST.md (top 5)
- `/retitle --audit` — Just show ranked list of underperformers with wasted impressions
- `/retitle --check [video-id]` — 7-day post-swap measurement, compare pre/post CTR, trigger ctr_ingest if successful
- `/retitle --revert [video-id]` — Pull old title from SWAP LOG for copy-paste revert

### Claude's Discretion
- Exact ranking formula (wasted impressions × retention weighting)
- Which map type to suggest per video when auto-suggesting
- How to handle videos without SRT/script files (fallback to existing RETITLE-RECOMMENDATIONS.md candidates)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/retitle_audit.py`: Already ranks videos by wasted impressions, parses CROSS-VIDEO-SYNTHESIS.md performance table
- `tools/retitle_gen.py`: Already generates + scores replacements with script thesis extraction, has VIDEO_PROJECT_MAP for SRT lookup
- `tools/title_scorer.py`: DB-enriched scoring via Phase 61 — score_title(title, db_path=db.db_path)
- `tools/preflight/thumbnail_checker.py`: check_thumbnail() and check_project() for compliance checking
- `tools/SWAP-PROTOCOL.md`: Full 48h swap protocol (adapt to 7-day for retitle context)
- `channel-data/RETITLE-RECOMMENDATIONS.md`: Pre-generated candidates from 2026-03-10 (fallback pool)
- `tools/ctr_ingest.py`: Phase 61 feedback loop — ingest CTR from synthesis table into keywords.db

### Established Patterns
- POST-PUBLISH-ANALYSIS files in video-projects/ and channel-data/analyses/ — add SWAP LOG section
- title_scorer returns dict with score, grade, pattern, db_enriched, rejection_reason
- Slash commands are .md files in .claude/commands/ that Claude interprets at runtime

### Integration Points
- `/retitle` command connects to retitle_audit.py + retitle_gen.py + title_scorer.py + thumbnail_checker.py
- `/retitle --check` connects to POST-PUBLISH-ANALYSIS swap log + ctr_ingest.py
- SWAP-CHECKLIST.md output goes to channel-data/ for user to action in YouTube Studio

</code_context>

<specifics>
## Specific Ideas

- SWAP-CHECKLIST.md should be a clean, copy-paste-friendly format — user opens it alongside YouTube Studio and works through each video
- Each video entry should be self-contained: old title, new title, new description lines, thumbnail concept (if applicable), video ID, Studio link
- The checklist is ephemeral (regenerated each run), but SWAP LOG in POST-PUBLISH-ANALYSIS is permanent history

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 60-retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr*
*Context gathered: 2026-03-14*
