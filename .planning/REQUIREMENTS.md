# Requirements: History vs Hype Workspace v1.6

**Defined:** 2026-02-06
**Core Value:** Every video shows sources on screen

## v1.6 Requirements

Requirements for Click & Keep milestone. Each maps to roadmap phases.

### A/B Test Tracking

- [ ] **AB-01**: User can enter CTR from YouTube Studio via CLI prompt and store in database
- [ ] **AB-02**: User can register thumbnail variants with file paths and visual pattern tags (map, face, text, document)
- [ ] **AB-03**: User can register title variants with formula tags (mechanism, document, paradox)
- [ ] **AB-04**: System tracks CTR snapshots at meaningful intervals (48h, 7d, 14d) per variant
- [ ] **AB-05**: User can calculate statistical significance between two variants given impressions and CTR
- [ ] **AB-06**: User can see channel-specific CTR benchmarks by topic category (territorial, ideological, legal)

### Script Pacing Analysis

- [ ] **PACE-01**: User can check sentence length variance per section and get flagged when variance exceeds threshold
- [ ] **PACE-02**: User can detect readability delta between sections (Flesch Reading Ease drop >20 points flagged)
- [ ] **PACE-03**: User can detect entity density hotspots (sections with >25% proper nouns flagged as "wall of nouns")
- [ ] **PACE-04**: System generates complexity score per section (0-100) combining variance, readability, and entity density
- [ ] **PACE-05**: System flags gaps >150 words without modern relevance hook or pattern interrupt
- [ ] **PACE-06**: User can see energy arc visualization showing pacing rhythm across full script

### Feedback Loop Integration

- [ ] **FEED-01**: System parses POST-PUBLISH-ANALYSIS markdown files and stores structured data in database
- [ ] **FEED-02**: User can query past performance insights for similar topics before creating new video
- [ ] **FEED-03**: System extracts success patterns from videos with CTR >8% or retention >35%
- [ ] **FEED-04**: System extracts failure patterns from videos with impressions <500 or retention <25%
- [ ] **FEED-05**: System automatically surfaces relevant insights during /script generation for matching topics

### Model Assignment Refresh

- [ ] **MOD-01**: All 13 slash command files updated from Claude 3.5 tier names to Claude 4.x model IDs
- [ ] **MOD-02**: Agent model assignments updated to current Claude 4.5/4.6 lineup

## Future Requirements

Deferred to later milestones.

### Retention Prediction (v2.0+)

- **RET-01**: System predicts retention curve shape from script features (requires 30+ videos with retention data)
- **RET-02**: System correlates specific script features with retention drop points

### Advanced Thumbnail Analysis (v2.0+)

- **THUMB-01**: System auto-categorizes thumbnails using perceptual hash clustering without manual tags
- **THUMB-02**: System estimates competitor CTR from public view velocity data

### DaVinci Integration (v2.0+)

- **DAV-01**: Export markers in DaVinci-compatible format
- **DAV-02**: Import shot list as timeline markers

## Out of Scope

Explicitly excluded from v1.6.

| Feature | Reason |
|---------|--------|
| Real-time CTR dashboard | Low volume (1-2 videos/month), creates anxiety without actionable insights |
| AI auto-generated thumbnails | Channel differentiator is evidence-based thumbnails in Photoshop |
| Automated title optimization | Channel DNA requires factual accuracy over clickbait optimization |
| Browser automation for YouTube Studio | High maintenance, CTR manual entry takes 10 seconds |
| Generic YouTube "best practices" enforcement | Channel data contradicts generic advice (maps > faces) |
| Retention heatmap prediction | Insufficient training data (~15 videos, need 30+) |
| Batch processing / multi-video automation | Solo creator workflow, 1-2 videos/month |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| AB-01 | TBD | Pending |
| AB-02 | TBD | Pending |
| AB-03 | TBD | Pending |
| AB-04 | TBD | Pending |
| AB-05 | TBD | Pending |
| AB-06 | TBD | Pending |
| PACE-01 | TBD | Pending |
| PACE-02 | TBD | Pending |
| PACE-03 | TBD | Pending |
| PACE-04 | TBD | Pending |
| PACE-05 | TBD | Pending |
| PACE-06 | TBD | Pending |
| FEED-01 | TBD | Pending |
| FEED-02 | TBD | Pending |
| FEED-03 | TBD | Pending |
| FEED-04 | TBD | Pending |
| FEED-05 | TBD | Pending |
| MOD-01 | TBD | Pending |
| MOD-02 | TBD | Pending |

**Coverage:**
- v1.6 requirements: 19 total
- Mapped to phases: 0
- Unmapped: 19

---
*Requirements defined: 2026-02-06*
*Last updated: 2026-02-06 after initial definition*
