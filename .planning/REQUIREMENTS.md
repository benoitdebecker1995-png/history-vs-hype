# Requirements: History vs Hype Workspace

**Defined:** 2026-02-19
**Core Value:** Every video shows sources on screen

## v5.0 Requirements

Requirements for v5.0 Production Intelligence. Each maps to roadmap phases.

### Pipeline Reliability

- [x] **PIPE-01**: Translation CLI reads API keys from .env file (falls back to environment variable)
- [x] **PIPE-02**: Translation CLI provides actionable error messages when API key missing, network fails, or rate limited
- [x] **PIPE-03**: End-to-end pipeline smoke test validates full flow (detect → translate → cross-check → annotate → format)

### Research Ingestion

- [x] **RES-01**: User can paste NLM output and tool extracts claims with citations into structured format
- [x] **RES-02**: Extracted claims shown for review with approve/reject per claim
- [x] **RES-03**: Approved claims auto-write to 01-VERIFIED-RESEARCH.md in correct section format

### YouTube Intelligence Engine

- [ ] **INTEL-01**: Local knowledge base stores algorithm mechanics (AVD, CTR, satisfaction signals, browse vs search priorities)
- [ ] **INTEL-02**: Knowledge base stores niche-specific patterns (what history/edu formats, lengths, hooks are performing)
- [ ] **INTEL-03**: Web scraper refreshes algorithm knowledge from authoritative sources (Creator Insider, Think Media, vidIQ blog, etc.)
- [ ] **INTEL-04**: Competitor tracker monitors top history/edu channels for viral content and format trends

### Intelligence Surfacing

- [ ] **INTEL-05**: Intelligence auto-surfaces relevant insights during /script, /prep, /publish generation

### Hook Optimization

- [ ] **HOOK-01**: Rule 19 in script-writer generates algorithm-optimized first 60 seconds (cold fact → myth → contradiction → payoff)
- [ ] **HOOK-02**: Hook pass references YouTube Intelligence Engine data for current best practices
- [ ] **HOOK-03**: Hook includes retention triggers (information gap, visual carrot, authority signals)

### Analytics Feedback Loop

- [ ] **ANLYT-01**: Backfill command populates analytics DB from existing POST-PUBLISH-ANALYSIS files and YouTube API
- [ ] **ANLYT-02**: Channel-specific insights surface automatically during /script generation (what works for YOUR channel)
- [ ] **ANLYT-03**: Analytics data feeds into topic recommendations with updated performance patterns

### Project Dashboard

- [ ] **DASH-01**: /status shows all projects in production with current phase, next action, and days since last activity
- [ ] **DASH-02**: Projects ranked by priority (filming-ready first, then research phase, then ideas)
- [ ] **DASH-03**: Dashboard integrates with YouTube Intelligence Engine to flag time-sensitive topics

## Future Requirements

Deferred to future release.

### Automated NotebookLM Integration
- **NLM-01**: Direct API integration with NotebookLM when Enterprise API becomes available
- **NLM-02**: Automatic notebook creation and source upload

### Advanced Analytics
- **ADV-01**: Retention heatmap prediction from script structure (requires 30+ videos)
- **ADV-02**: Automated A/B testing for thumbnails via YouTube API

## Out of Scope

| Feature | Reason |
|---------|--------|
| Video editing automation | DaVinci Resolve workflow, not scriptable from this workspace |
| VidIQ API integration | No public API available |
| Multi-person workflow | Solo creator optimization only |
| NotebookLM API automation | Waiting for Enterprise API availability |
| Retention heatmap prediction | Requires 30+ videos with retention data |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PIPE-01 | Phase 42 | Complete |
| PIPE-02 | Phase 42 | Complete |
| PIPE-03 | Phase 42 | Complete |
| RES-01 | Phase 42 | Complete |
| RES-02 | Phase 42 | Complete |
| RES-03 | Phase 42 | Complete |
| INTEL-01 | Phase 43 | Pending |
| INTEL-02 | Phase 43 | Pending |
| INTEL-03 | Phase 43 | Pending |
| INTEL-04 | Phase 43 | Pending |
| INTEL-05 | Phase 45 | Pending |
| HOOK-01 | Phase 45 | Pending |
| HOOK-02 | Phase 45 | Pending |
| HOOK-03 | Phase 45 | Pending |
| ANLYT-01 | Phase 44 | Pending |
| ANLYT-02 | Phase 44 | Pending |
| ANLYT-03 | Phase 44 | Pending |
| DASH-01 | Phase 46 | Pending |
| DASH-02 | Phase 46 | Pending |
| DASH-03 | Phase 46 | Pending |

**Coverage:**
- v5.0 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-02-19*
*Last updated: 2026-02-19 after roadmap creation*
