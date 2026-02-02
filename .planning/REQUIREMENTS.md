# Requirements: History vs Hype v1.4

**Defined:** 2026-02-02
**Core Value:** Every video shows sources on screen

## v1.4 Requirements

Requirements for Learning Loop milestone. Each maps to roadmap phases.

### Performance Analysis

- [ ] **PERF-01**: User can see subscriber conversion per video from published catalog
- [ ] **PERF-02**: User can see which topic types correlate with high conversion (territorial, legal, ideological)
- [ ] **PERF-03**: User can see which angles correlate with high conversion (document-heavy, legal, colonial)

### Pattern Extraction

- [ ] **PATN-01**: System extracts "winning pattern" profile from top-performing videos
- [ ] **PATN-02**: System identifies channel strengths (document-heavy, academic, legal/territorial)
- [ ] **PATN-03**: System tracks what attributes top converters share

### Recommendation Engine

- [ ] **RECD-01**: User can get ranked NEW topic recommendations via `/next` command
- [ ] **RECD-02**: Recommendations are filtered against existing `_IN_PRODUCTION/` and `_ARCHIVED/` work
- [ ] **RECD-03**: Each recommendation shows reasoning (fit score, competition gap, feasibility)
- [ ] **RECD-04**: Recommendations integrate with existing opportunity scoring (v1.3)

### Integration

- [ ] **INTG-01**: System pulls performance data from existing YouTube Analytics API (v1.1)
- [ ] **INTG-02**: System uses competition data from existing discovery tools (v1.3)
- [ ] **INTG-03**: System respects production constraints from existing filters (v1.3)

## Out of Scope

| Feature | Reason |
|---------|--------|
| ML-based prediction | 20 videos is too small for ML; simple correlation is sufficient |
| Real-time trending alerts | Academic workflow can't respond fast enough |
| Automated topic generation | Generic AI suggestions violate channel DNA |
| Retention heatmap analysis | Requires 30+ videos with retention data |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PERF-01 | Phase 19 | Pending |
| PERF-02 | Phase 19 | Pending |
| PERF-03 | Phase 19 | Pending |
| PATN-01 | Phase 20 | Pending |
| PATN-02 | Phase 20 | Pending |
| PATN-03 | Phase 20 | Pending |
| RECD-01 | Phase 21 | Pending |
| RECD-02 | Phase 21 | Pending |
| RECD-03 | Phase 21 | Pending |
| RECD-04 | Phase 21 | Pending |
| INTG-01 | Phase 19 | Pending |
| INTG-02 | Phase 21 | Pending |
| INTG-03 | Phase 21 | Pending |

**Coverage:**
- v1.4 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0

---
*Requirements defined: 2026-02-02*
*Last updated: 2026-02-02 after initial definition*
