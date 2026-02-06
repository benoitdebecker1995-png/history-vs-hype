# Phase 27: Database Foundation - Context

**Gathered:** 2026-02-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Schema extensions to existing keywords.db enabling CTR tracking, thumbnail/title variant storage, and feedback storage. All changes are additive — zero breaking changes to existing tools (discovery, performance, recommendations). This phase builds the data layer that Phases 29-31 will consume.

</domain>

<decisions>
## Implementation Decisions

### Variant Storage Model
- Separate tables for thumbnail_variants and title_variants (not embedded in existing tables)
- Support 3-4 variants per video (not limited to A/B)
- Thumbnail variants store: file path, image perceptual hash (ImageHash), visual pattern tags
- Title variants store: full title text, character count, variant letter (A/B/C/D), free-text formula tags
- Title formula tags: keep the A/B/C variant letter system from Phase 25 AND allow free-text formula tags (e.g., "question-hook", "colon-split", "how-X-deleted-Y")
- Full content + metadata stored (not just references)

### CTR Snapshot Design
- Monthly snapshots — one per video per month (not 48h/7d/14d windows)
- Each snapshot stores: CTR percentage, impression count, view count, timestamp, active variant ID
- Active variant tracked per snapshot (which thumbnail/title was live)
- Full snapshot data (CTR + impressions + views) to enable statistical significance in Phase 30
- Late entries accepted — store with actual timestamp, mark as late but still usable
- No fixed window enforcement — record whenever the user gets to it

### Feedback Data Structure
- Hybrid storage: key metrics in typed columns + JSON blob for freeform notes/lessons
- Both video-level and section-level granularity supported
- Video-level: overall performance summary, what worked, what didn't
- Section-level: optional notes linked to specific script sections (e.g., "intro too long", "section 3 retention dip")

### Migration Strategy
- High data concern — treat keywords.db as precious
- Auto-migrate with confirmation: detect old schema on first access, print what will change, proceed automatically
- Migration is additive only (new tables, new columns) — old tools continue working unchanged

### Claude's Discretion
- Visual pattern tag approach for thumbnails (free-text vs predefined vocabulary)
- Schema design for feedback categories (auto-categorize or not — optimize for Phase 31 feedback loop)
- Rollback approach (backup before migrate or rely on additive-only safety)
- Schema version tracking method (version table vs table-existence checks — match existing codebase patterns)
- Reminder system for pending snapshots (integrate into /status or separate)
- Exact JSON structure for freeform feedback blobs

</decisions>

<specifics>
## Specific Ideas

- Monthly snapshot cadence matches the user's actual review rhythm (not artificial 48h/7d/14d windows)
- Existing _ensure_table() auto-migration pattern in codebase should inform the approach
- Phase 25 already generates 3 title variants (mechanism A, document B, paradox C) — title_variants table should be compatible with that output
- ImageHash 4.3.2 library planned for perceptual hashing of thumbnails
- textstat 0.7.12 upgrade planned for pacing analysis (Phase 28, not this phase)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 27-database-foundation*
*Context gathered: 2026-02-06*
