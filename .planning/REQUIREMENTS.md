# Requirements: History vs Hype Workspace

**Defined:** 2026-03-16
**Core Value:** Every video shows sources on screen. Viewers see the evidence themselves and can evaluate the interpretation.

## v7.0 Requirements

Requirements for Packaging & Hooks Overhaul. Each maps to roadmap phases.

### Benchmarking

- [x] **BENCH-01**: Title scorer anchors "passing" (65/100) to 4%+ CTR based on edu/history competitor norms, not own-channel baseline
- [x] **BENCH-02**: Scorer flags when a pattern score is based on fewer than 5 examples and falls back to competitor benchmarks
- [x] **BENCH-03**: Scorer applies different CTR targets by topic type (territorial 3%+, political fact-check 5%+, ideological 4%+)

### Title Generation

- [x] **TITLE-01**: `/publish --titles` reads the script and extracts specific numbers, document names, and contradictions as raw material for title candidates
- [x] **TITLE-02**: Title generation produces versus and declarative variants as default output when topic has two competing entities
- [x] **TITLE-03**: Titles with year (-46% CTR), colon (-28%), "The X That Y" (1.2% CTR), and question (-36%) patterns receive heavy score penalties and are shown ranked last with warning labels — never silently dropped (reinterpreted per Phase 68 CONTEXT.md: data-driven scoring, not blind rejection)

### Hook Quality

- [x] **HOOK-01**: Hook scorer verifies first sentence/5 seconds matches the title's promise (catches the 17% dropout from title-fulfillment mismatch)
- [x] **HOOK-02**: Hook generator recommends style based on topic type (cold_fact for territorial, myth-contradiction for ideological, specific-claim for political fact-check)

### Metadata & Thumbnails

- [x] **META-01**: `/publish` enforces description template: keyword-rich first sentence + specific document/claim + source citations + timestamps
- [x] **META-02**: Thumbnail concept generator reads script, outputs 3 concepts (split-map conflict, document-on-map, geo+evidence) with specific visual elements
- [x] **META-03**: Metadata bundle coherence check verifies title + thumbnail concept + description all reference the same hook element

## Future Requirements

### Advanced Scoring

- **BENCH-04**: Full competitor formula library ingestion with weighted pattern matching
- **BENCH-05**: Longitudinal hook score tracking (which hook types user picks when scored variants are presented)

### Hook Generation

- **HOOK-03**: 4-beat completeness check (cold_fact + myth + contradiction + payoff all present)
- **HOOK-04**: "Authority stack" hook template (multiple authorities believe myth, all wrong)

### Metadata

- **META-04**: Tag generation from script entities (people, places, treaties) + related search terms (15-20 tags)

## Out of Scope

| Feature | Reason |
|---------|--------|
| A/B thumbnail testing framework | Channel gets 100-500 views per video; any A/B result is statistical noise |
| CTR prediction ML model | 48 videos is nowhere near enough for reliable ML; will overfit |
| Automated thumbnail creation | Solo creator uses Photoshop; automation adds fragility without time savings |
| Engagement rate optimization | High engagement + low views = niche audience YouTube can't place; optimize CTR/impressions instead |
| Generic YouTube algorithm tips | "Upload at 3pm!" is noise at 475 subs; surface only data-backed channel-specific rules |
| Retroactive retitling all 48 videos | Destroys ability to measure; swap 1-2 per week via existing /retitle |
| Hook word-count targets | Hook quality is about 4-beat structure, not word count |
| Description hashtag optimization | Wastes prime keyword real estate in first 3 lines |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BENCH-01 | Phase 67 | Complete |
| BENCH-02 | Phase 67 | Complete |
| BENCH-03 | Phase 67 | Complete |
| TITLE-01 | Phase 68 | Complete |
| TITLE-02 | Phase 68 | Complete |
| TITLE-03 | Phase 68 | Complete |
| HOOK-01 | Phase 69 | Complete |
| HOOK-02 | Phase 69 | Complete |
| META-01 | Phase 70 | Complete |
| META-02 | Phase 70 | Complete |
| META-03 | Phase 70 | Complete |

**Coverage:**
- v7.0 requirements: 11 total
- Mapped to phases: 11
- Unmapped: 0

---
*Requirements defined: 2026-03-16*
*Last updated: 2026-03-16 after v7.0 roadmap creation (traceability complete)*
