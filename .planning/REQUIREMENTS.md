# Requirements: History vs Hype Workspace

**Defined:** 2026-02-12
**Core Value:** Every video shows sources on screen

## v3.0 Requirements

Requirements for v3.0 Adaptive Scriptwriter. Each maps to roadmap phases.

### Retention Science

- [ ] **RET-01**: Retention playbook synthesized from channel data exists as STYLE-GUIDE.md Part 9, readable by script-writer-v2
- [ ] **RET-02**: Script sections scored for predicted retention based on length, evidence density, and modern relevance proximity
- [ ] **RET-03**: Retention drop patterns from published videos encoded as warnings that flag risky script sections

### Creator Analysis

- [ ] **CRE-01**: Transcript analysis pipeline parses existing 80+ transcripts and extracts structural patterns (hooks, transitions, pacing, evidence presentation)
- [ ] **CRE-02**: Cross-creator synthesis identifies patterns appearing across 3+ successful creators as universal best practices
- [ ] **CRE-03**: Creator technique library stored in DB and surfaced as STYLE-GUIDE.md Part 8, searchable by technique type
- [ ] **CRE-04**: Script-writer-v2 reads Part 8 techniques and applies relevant ones during generation (Rule 17)

### Choice Architecture

- [ ] **CHO-01**: Script-writer-v2 generates 2-3 opening hook variants before writing full script when --variants flag is set
- [ ] **CHO-02**: Script-writer-v2 proposes 2 structural approaches (e.g., chronological vs payoff-first) per video
- [ ] **CHO-03**: User's hook and structure choices logged to database with project context
- [ ] **CHO-04**: After 5+ logged choices, system recommends preferred option based on past choice patterns

### Integration

- [ ] **INT-01**: Database migrated to schema v28 with script_choices and creator_techniques tables
- [ ] **INT-02**: /script skill supports --variants flag for variant generation mode
- [ ] **INT-03**: Script-writer-v2 agent prompt consolidated (Rules 13 simplified, Rules 15-17 added) within 1,500 line budget

## v3.1 Requirements

Deferred to next milestone. Not in current roadmap.

### Edit Learning

- **EDL-01**: Version comparison diffs generated script against user's edited version
- **EDL-02**: Each edit classified by type (tone, accuracy, voice, structural) using Claude API
- **EDL-03**: Recurring edits (3+ consistent) promoted to confirmed preferences in preferences.json
- **EDL-04**: Preference dashboard shows accumulated preferences for user review and adjustment

## Out of Scope

| Feature | Reason |
|---------|--------|
| ML model for preference learning | Too complex for solo creator, small dataset |
| Real-time editing integration | Compare versions after editing, not during |
| Video editing automation | Out of scope for content production workspace |
| spaCy/NLTK for transcript analysis | Claude API provides better classification |
| Automatic style mimicry ("write like Kraut") | Produces generic imitation, not authentic voice |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| RET-01 | Phase 36 | Pending |
| RET-02 | Phase 36 | Pending |
| RET-03 | Phase 36 | Pending |
| CRE-01 | Phase 37 | Pending |
| CRE-02 | Phase 37 | Pending |
| CRE-03 | Phase 37 | Pending |
| CRE-04 | Phase 37 | Pending |
| INT-01 | Phase 37 | Pending |
| CHO-01 | Phase 38 | Pending |
| CHO-02 | Phase 38 | Pending |
| CHO-03 | Phase 38 | Pending |
| CHO-04 | Phase 38 | Pending |
| INT-02 | Phase 38 | Pending |
| INT-03 | Phase 38 | Pending |

**Coverage:**
- v3.0 requirements: 14 total
- Mapped to phases: 14
- Unmapped: 0 ✓

---
*Requirements defined: 2026-02-12*
*Last updated: 2026-02-13 after roadmap creation*
