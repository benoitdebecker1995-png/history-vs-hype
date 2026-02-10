# Requirements: History vs Hype Workspace v2.0

**Defined:** 2026-02-09
**Core Value:** Every video shows sources on screen

## v2.0 Requirements

Requirements for Channel Intelligence milestone. Each maps to roadmap phases.

### Voice Pattern Library

- [ ] **VOICE-01**: System extracts voice patterns (sentence structures, transitions, phrases) from transcripts of top-performing videos
- [ ] **VOICE-02**: STYLE-GUIDE.md Part 6 expanded with documented patterns for Kraut-style causal chains, Alex O'Connor transitions, and creator's proven phrases
- [ ] **VOICE-03**: Script-writer-v2 agent applies Part 6 voice patterns to produce scripts matching creator's calm prosecutor tone
- [ ] **VOICE-04**: System validates generated scripts for forbidden phrases, missing term definitions, and channel DNA violations before output

### NotebookLM Research Bridge

- [ ] **NLMB-01**: Given a topic, system generates academic source list (university press books with titles, authors, ISBNs, and download/purchase links)
- [ ] **NLMB-02**: System parses NotebookLM chat output and extracts citations into VERIFIED-RESEARCH.md format with page numbers
- [ ] **NLMB-03**: System provides structured NotebookLM prompts for efficient fact extraction (targeted queries for claims, quotes, counter-evidence)

### Actionable Analytics

- [ ] **ACTN-01**: System maps retention drop points to specific script sections with root cause analysis
- [ ] **ACTN-02**: System generates concrete fix recommendations referencing specific lines, sentences, or sections (not just metrics)
- [ ] **ACTN-03**: System provides topic strategy analysis showing which video types perform best with specific recommendations
- [ ] **ACTN-04**: System proactively surfaces relevant past performance insights before /script generation (not just in /analyze reports)

## Future Requirements

Deferred to later milestones.

### Retention Prediction (v2.1+)

- **RET-01**: System predicts retention curve shape from script features (requires 30+ videos with retention data)
- **RET-02**: System correlates specific script features with retention drop points

### Advanced Thumbnail Analysis (v2.1+)

- **THUMB-01**: System auto-categorizes thumbnails using perceptual hash clustering without manual tags
- **THUMB-02**: System estimates competitor CTR from public view velocity data

### Evidence Display Timing (v2.1+)

- **EVID-01**: System validates source display timing against retention patterns
- **EVID-02**: System suggests optimal B-roll placement based on past video performance

### Competitor Analysis (v2.1+)

- **COMP-01**: System parses competitor transcripts to extract structure patterns
- **COMP-02**: System identifies gaps between competitor coverage and channel strengths

## Out of Scope

Explicitly excluded from v2.0.

| Feature | Reason |
|---------|--------|
| Auto-generate thumbnails | Defeats evidence-based thumbnail strategy (maps > faces) |
| AI voice cloning | Talking head format requires on-camera authority |
| Real-time CTR dashboard | Creates anxiety without action for 1-2 videos/month |
| Automated title optimization | Risks clickbait violations of documentary tone |
| Script auto-revision | Removes creator voice — scripts need human judgment |
| NotebookLM API automation | No public API available (enterprise-only alpha) |
| DaVinci Resolve integration | Video editing automation out of scope |
| Full YouTube automation | Loses intellectual competence signal that drives subscribers |
| Python 3.14 migration | Wait for spaCy wheels (use 3.11-3.13 for now) |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| VOICE-01 | TBD | Pending |
| VOICE-02 | TBD | Pending |
| VOICE-03 | TBD | Pending |
| VOICE-04 | TBD | Pending |
| NLMB-01 | TBD | Pending |
| NLMB-02 | TBD | Pending |
| NLMB-03 | TBD | Pending |
| ACTN-01 | TBD | Pending |
| ACTN-02 | TBD | Pending |
| ACTN-03 | TBD | Pending |
| ACTN-04 | TBD | Pending |

**Coverage:**
- v2.0 requirements: 11 total
- Mapped to phases: 0
- Unmapped: 11 (roadmap pending)

---
*Requirements defined: 2026-02-09*
*Last updated: 2026-02-09 after initial definition*
