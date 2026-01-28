# Requirements: History vs Hype Workspace

**Defined:** 2026-01-27
**Core Value:** Every video shows sources on screen — viewers see the evidence themselves

## v1.2 Requirements

Requirements for Script Quality & Discovery milestone.

### Script Quality

- [x] **SCRIPT-01**: Repetition detection — scan scripts for identical/near-identical phrases, flag when threshold exceeded
- [x] **SCRIPT-02**: Flow analyzer — check narrative flow (terms defined before use, transitions between sections)
- [x] **SCRIPT-03**: Stumble test — identify sentences >25 words, complex subordinate clauses, written-style colons
- [x] **SCRIPT-04**: "Here's" counter — alert when scaffolding language exceeds 4 instances
- [ ] **SCRIPT-05**: Voice fingerprinting — analyze transcripts to learn speech patterns, flag violations

### Discovery/SEO

- [ ] **DISC-01**: Long-tail keyword extractor — pull 3-4 word phrases from YouTube autocomplete
- [ ] **DISC-02**: Search intent mapper — classify titles by query type (why/how/what)
- [ ] **DISC-03**: Impression diagnostic — if impressions <500 in 7 days = SEO issue, CTR <2% = title/thumbnail issue
- [ ] **DISC-04**: Metadata consistency check — verify keywords in title appear in description/tags

### NotebookLM Workflow

- [ ] **NBLM-01**: Structured prompt templates — expand from 5 to 15+ research use cases
- [ ] **NBLM-02**: Session logging format — standard template for capturing NotebookLM findings
- [ ] **NBLM-03**: Citation extraction helpers — parse manually pasted NotebookLM output into structured format

## Future Requirements (v1.3+)

Deferred features requiring more data or API availability.

### Script Quality

- **SCRIPT-06**: Retention heatmap prediction — requires 30+ videos with retention data
- **SCRIPT-07**: Causal chain detector — ensure minimum density of causal language

### Discovery/SEO

- **DISC-05**: Title A/B test manager — track which title patterns win empirically
- **DISC-06**: Competitor title scraper — auto-update title database from Kraut/Knowing Better/Shaun

### NotebookLM

- **NBLM-04**: API integration — when Enterprise API exits alpha, automate queries
- **NBLM-05**: Cross-source synthesizer — compare claims across multiple sources

## Out of Scope

| Feature | Reason |
|---------|--------|
| Generic hook generator | Violates documentary tone — clickbait language explicitly forbidden |
| Auto-script generator (one-click) | Quality control violation — scripts need fact verification |
| Viral title optimizer | Optimizes wrong metric — CTR without retention = clickbait penalty |
| Comment auto-responder | Brand voice requires human judgment — can't automate nuance |
| Script length trimmer | Channel philosophy is "as long as needed" — arbitrary cuts hurt quality |
| Keyword stuffing tool | YouTube 2026 penalizes keyword stuffing — natural language now required |
| NotebookLM browser automation | Brittle and slower than manual workflow |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SCRIPT-01 | Phase 11 | Complete |
| SCRIPT-02 | Phase 11 | Complete |
| SCRIPT-03 | Phase 11 | Complete |
| SCRIPT-04 | Phase 11 | Complete |
| SCRIPT-05 | Phase 12 | Pending |
| DISC-01 | Phase 13 | Pending |
| DISC-02 | Phase 13 | Pending |
| DISC-03 | Phase 13 | Pending |
| DISC-04 | Phase 13 | Pending |
| NBLM-01 | Phase 14 | Pending |
| NBLM-02 | Phase 14 | Pending |
| NBLM-03 | Phase 14 | Pending |

**Coverage:**
- v1.2 requirements: 12 total
- Mapped to phases: 12/12 (100%)
- Unmapped: 0

**Phase Distribution:**
- Phase 11 (Script Quality Checkers): 4 requirements
- Phase 12 (Voice Fingerprinting): 1 requirement
- Phase 13 (Discovery Tools): 4 requirements
- Phase 14 (NotebookLM Workflow): 3 requirements

---
*Requirements defined: 2026-01-27*
*Traceability updated: 2026-01-28*
