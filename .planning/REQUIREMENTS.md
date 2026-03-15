# Requirements: History vs Hype Workspace

**Defined:** 2026-03-01
**Core Value:** Every video shows sources on screen

## v5.2 Requirements

Requirements for v5.2 Growth Engine. Each maps to roadmap phases.

### Title & CTR Optimization

- [x] **CTR-01**: Title pattern analyzer correlates title structure (length, keywords, format) with actual CTR from YouTube Analytics API
- [x] **CTR-02**: Title scorer predicts CTR for new title variants based on own-channel historical patterns
- [x] **CTR-03**: Published title tracked in DB with resulting CTR, closing the feedback loop
- [x] **CTR-04**: `/publish --titles` ranks generated variants by predicted CTR with confidence interval

### Search & Discovery

- [x] **SEO-01**: Video titles audited against search keywords — flags titles with low keyword overlap vs search demand
- [x] **SEO-02**: Search traffic percentage tracked per video (YouTube Analytics API insightTrafficSourceType)
- [x] **SEO-03**: Keyword gap detection — high-demand keywords where channel has no video or underperforms

### Competitor Gap Analysis

- [x] **GAP-01**: 870+ competitor videos classified by topic AND angle (document-first, narrative, legal, explainer)
- [x] **GAP-02**: Cross-reference with own videos to identify uncovered topic-angle combinations
- [x] **GAP-03**: Gap scoring formula: demand signal × competitor absence × channel competitive advantage
- [x] **GAP-04**: `/next` surfaces top gaps with "No competitor covers [X] from [angle]" recommendations

### Retention Intelligence

- [x] **RET-01**: Per-video retention percentage pulled from YouTube Analytics API and stored in DB
- [x] **RET-02**: Retention correlated with script structure (hook type, section count, evidence density, video length)
- [x] **RET-03**: Opening hook type → first-30-second retention mapping (the algorithm gate signal)
- [x] **RET-04**: Script-writer-v2 Rule 20 encodes retention findings as generation constraints

### Growth Dashboard

- [x] **GROW-01**: Subscriber velocity trend calculated (monthly growth rate, acceleration/deceleration detection)
- [x] **GROW-02**: Per-video ROI ranking: views, subs gained, conversion rate, CTR — sortable
- [x] **GROW-03**: Traffic source breakdown per video (search, suggested, browse, external)
- [x] **GROW-04**: Monetization countdown projections (1K subs, 4K watch hours)
- [x] **GROW-05**: Monthly growth report accessible via `/growth` command

### Data Foundation

- [x] **DATA-01**: Full analytics backfill from YouTube Analytics API into analytics.db (all long-form videos)
- [x] **DATA-02**: Publish timestamps stored for all videos
- [x] **DATA-03**: Traffic source data stored per video
- [x] **DATA-04**: Automated refresh command pulls latest analytics on demand

### Retitle & Rethumb Pipeline

- [x] **RETITLE-01**: `/retitle` command audits underperformers ranked by wasted impressions with retention weighting (min 500 impressions, top 5)
- [x] **RETITLE-02**: `/retitle` generates script-based title candidates scored by title_scorer, outputs SWAP-CHECKLIST.md with old title, new title, new description, thumbnail concept
- [x] **RETITLE-03**: `/retitle --audit` shows ranked underperformer list without generating candidates
- [x] **RETITLE-04**: `/retitle --check [video-id]` measures 7-day post-swap CTR, enforces minimum wait, triggers ctr_ingest on success
- [x] **RETITLE-05**: `/retitle --revert [video-id]` surfaces old title from SWAP LOG for copy-paste revert
- [x] **RETITLE-06**: SWAP LOG section in POST-PUBLISH-ANALYSIS.md tracks swap history per video (date, old/new title, pre/post CTR, result)

### Proactive Topic Discovery

- [x] **DISC-01**: YouTube autocomplete miner scans channel niches (territorial disputes, colonial history, border conflicts, ideological myths) and surfaces search suggestions NOT already in the topic pipeline or production folders
- [x] **DISC-02**: Competitor release tracker monitors target channels (RealLifeLore, Wendover, Kraut, Knowing Better, etc.), detects new uploads, and flags coverage gaps where competitors got views but the channel has no video
- [x] **DISC-03**: Google Trends pulse detects rising search interest in channel-relevant topics before competitors notice, with breakout detection and 30/90-day trend direction
- [x] **DISC-04**: Discovery feed command (`/discover --scan`) combines autocomplete, competitor, and trends signals into ranked opportunities scored by the Belize formula (demand + map angle + news hook + no competitor coverage)
- [x] **DISC-05**: Discovery feed deduplicates against existing pipeline (`keywords.db`, `_IN_PRODUCTION/`, `_ARCHIVED/`) so only genuinely new opportunities surface

## Future Requirements

### Thumbnail Optimization

- **THUMB-01**: Thumbnail style correlation with CTR (map vs face vs document)
- **THUMB-02**: A/B testing framework for thumbnail variants

### Publish Timing

- **TIME-01**: Day-of-week + time-of-day correlation with first-7-day performance
- **TIME-02**: Competitor publish schedule awareness

## Out of Scope

| Feature | Reason |
|---------|--------|
| VidIQ API integration | No public API available — use manual VidIQ + /publish --prompts workflow |
| Automated publishing | Risk too high for solo creator — always publish manually |
| Comment sentiment analysis | Low ROI at current scale (21 comments/month) |
| Shorts optimization | Channel growth strategy is long-form first |
| Thumbnail A/B testing | YouTube native A/B testing requires 10K+ views/video |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 55 | Complete |
| DATA-02 | Phase 55 | Complete |
| DATA-03 | Phase 55 | Complete |
| DATA-04 | Phase 55 | Complete |
| CTR-01 | Phase 56 | Complete |
| CTR-02 | Phase 56 | Complete |
| CTR-03 | Phase 56 | Complete |
| CTR-04 | Phase 56 | Complete |
| SEO-01 | Phase 56 | Complete |
| SEO-02 | Phase 56 | Complete |
| SEO-03 | Phase 56 | Complete |
| GAP-01 | Phase 57 | Complete |
| GAP-02 | Phase 57 | Complete |
| GAP-03 | Phase 57 | Complete |
| GAP-04 | Phase 57 | Complete |
| RET-01 | Phase 58 | Complete |
| RET-02 | Phase 58 | Complete |
| RET-03 | Phase 58 | Complete |
| RET-04 | Phase 58 | Complete |
| GROW-01 | Phase 59 | Complete |
| GROW-02 | Phase 59 | Complete |
| GROW-03 | Phase 59 | Complete |
| GROW-04 | Phase 59 | Complete |
| GROW-05 | Phase 59 | Complete |
| RETITLE-01 | Phase 60 | Complete |
| RETITLE-02 | Phase 60 | Complete |
| RETITLE-03 | Phase 60 | Complete |
| RETITLE-04 | Phase 60 | Complete |
| RETITLE-05 | Phase 60 | Complete |
| RETITLE-06 | Phase 60 | Complete |
| GATE-01 | Phase 61 | Complete |
| GATE-02 | Phase 61 | Complete |
| GATE-03 | Phase 61 | Complete |
| GATE-04 | Phase 61 | Complete |
| GATE-05 | Phase 61 | Complete |
| DISC-01 | Phase 62 | Complete |
| DISC-02 | Phase 62 | Complete |
| DISC-03 | Phase 62 | Complete |
| DISC-04 | Phase 62 | Complete |
| DISC-05 | Phase 62 | Complete |

**Coverage:**
- v5.2 requirements: 24 total
- v6.0 requirements: 16 total (RETITLE 6 + GATE 5 + DISC 5)
- Mapped to phases: 40
- Unmapped: 0

---
*Requirements updated: 2026-03-15*
