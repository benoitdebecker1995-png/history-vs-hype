# Requirements: History vs Hype v1.3 Niche Discovery

**Defined:** 2026-01-31
**Core Value:** Find high-potential topics with low competition that fit the channel's document-heavy format

## v1.3 Requirements

Requirements for niche discovery milestone. Each maps to roadmap phases.

### Demand Research

- [x] **DEM-01**: User can get search volume estimate for a topic (from autocomplete position proxy)
- [x] **DEM-02**: User can see trend direction for a topic (rising, stable, declining)
- [x] **DEM-03**: User can expand a seed keyword into related queries
- [x] **DEM-04**: User can see competition ratio score (demand vs. supply quantification)

### Competition Analysis

- [ ] **COMP-01**: User can see video count and channel count for a keyword
- [ ] **COMP-02**: User can filter competition by quality (not just quantity)
- [ ] **COMP-03**: User can see competitor format and angle (animation vs. documentary, political vs. legal)
- [ ] **COMP-04**: User can see differentiation score (what angle is missing in existing coverage)

### Format Filtering

- [ ] **FMT-01**: Topics requiring animation are flagged as hard blocks
- [ ] **FMT-02**: Topics are scored for document-friendliness (0-4 scale)
- [ ] **FMT-03**: User can check academic source availability for a topic

### Opportunity Scoring

- [ ] **OPP-01**: User can see combined opportunity score (demand × gap × fit / effort)
- [ ] **OPP-02**: Production constraints are weighted in the scoring formula
- [ ] **OPP-03**: Channel DNA rules auto-filter topics (reject clickbait, news-first framing)
- [ ] **OPP-04**: Opportunities track lifecycle status (DISCOVERED → IN_RESEARCH → SCRIPTED → PUBLISHED)
- [ ] **OPP-05**: User can generate Markdown opportunity report for a topic

## Future Requirements (v1.4+)

Deferred to future release. Tracked but not in current roadmap.

### Validation Loop

- **VAL-01**: Compare predicted opportunity score to actual video performance
- **VAL-02**: Calibrate scoring weights based on validation results
- **VAL-03**: Track filter accuracy over time (false negatives)

### Advanced Competition

- **COMP-05**: Auto-detect competitor channel uploads (weekly monitoring)
- **COMP-06**: Alert when competition grows for queued topics

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| AI auto-generated topic lists | Generic output violates channel voice |
| Clickbait title generators | Violates documentary tone requirement |
| Viral prediction scores | Educational content follows different patterns |
| Real-time trending alerts | Can't respond fast with academic research workflow |
| Comment auto-responder | Brand voice can't be automated |
| Retention heatmap prediction | Requires 30+ videos with data (not available yet) |

## Traceability

Which phases cover which requirements. All v1.3 requirements mapped.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DEM-01 | Phase 15 | Complete |
| DEM-02 | Phase 15 | Complete |
| DEM-03 | Phase 15 | Complete |
| DEM-04 | Phase 15 | Complete |
| COMP-01 | Phase 16 | Pending |
| COMP-02 | Phase 16 | Pending |
| COMP-03 | Phase 16 | Pending |
| COMP-04 | Phase 16 | Pending |
| FMT-01 | Phase 17 | Pending |
| FMT-02 | Phase 17 | Pending |
| FMT-03 | Phase 17 | Pending |
| OPP-01 | Phase 18 | Pending |
| OPP-02 | Phase 18 | Pending |
| OPP-03 | Phase 18 | Pending |
| OPP-04 | Phase 18 | Pending |
| OPP-05 | Phase 18 | Pending |

**Coverage:**
- v1.3 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0 ✓

---
*Requirements defined: 2026-01-31*
*Last updated: 2026-01-31 after roadmap creation*
