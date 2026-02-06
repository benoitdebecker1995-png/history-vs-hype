# Requirements: History vs Hype Workspace v1.5

**Defined:** 2026-02-03
**Core Value:** Every video shows sources on screen

## v1.5 Requirements

Requirements for Production Acceleration milestone. Each maps to roadmap phases.

### Teleprompter

- [x] **TELE-01**: User can export script to clean teleprompter text (no markdown, read-aloud format)

*Note: Verify existing `/script --teleprompter` functionality — may just need documentation.*

### B-Roll Generation

- [x] **BROLL-01**: User can generate shot list from script with timestamps/sections
- [x] **BROLL-02**: System auto-detects entities (treaties, places, people, documents) from script text
- [x] **BROLL-03**: System suggests source URLs for detected entities (Wikimedia Commons, archive.org, map services)
- [x] **BROLL-04**: Shots are categorized by type (map, document, portrait, event photo)

### Edit Guide

- [x] **EDIT-01**: User can see section breakdown with estimated durations (words → time)
- [x] **EDIT-02**: User can see inline B-roll markers in script (`[B-ROLL: description]`)
- [x] **EDIT-03**: User can generate timing sheet (section name, start time estimate, B-roll cues)

### Metadata Draft

- [x] **META-01**: System extracts title candidates from script (opening hook, key claims)
- [x] **META-02**: System generates description template with section timestamps
- [x] **META-03**: System suggests tags based on script content and existing patterns

### Package Command

- [x] **PKG-01**: User can run single `/prep --package` command to generate all outputs
- [x] **PKG-02**: Package outputs saved to project folder (B-ROLL-CHECKLIST.md, EDIT-GUIDE.md, METADATA-DRAFT.md)

## Future Requirements

Deferred to later milestones.

### DaVinci Integration (v1.6+)

- **DAV-01**: Export markers in DaVinci-compatible format
- **DAV-02**: Import shot list as timeline markers

### Thumbnail Pipeline (v1.6+)

- **THUMB-01**: Generate thumbnail concepts from script key frames
- **THUMB-02**: A/B test tracking with performance correlation

## Out of Scope

Explicitly excluded from v1.5.

| Feature | Reason |
|---------|--------|
| Actual image downloading | Complexity, copyright concerns — suggest URLs only |
| DaVinci Resolve import | Future milestone, needs format research |
| Thumbnail generation | Different domain, separate milestone |
| Video editing automation | Out of workspace scope entirely |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| TELE-01 | Phase 26 | Complete |
| BROLL-01 | Phase 23 | Complete |
| BROLL-02 | Phase 22 | Complete |
| BROLL-03 | Phase 23 | Complete |
| BROLL-04 | Phase 23 | Complete |
| EDIT-01 | Phase 24 | Complete |
| EDIT-02 | Phase 24 | Complete |
| EDIT-03 | Phase 24 | Complete |
| META-01 | Phase 25 | Complete |
| META-02 | Phase 25 | Complete |
| META-03 | Phase 25 | Complete |
| PKG-01 | Phase 26 | Complete |
| PKG-02 | Phase 26 | Complete |

**Coverage:**
- v1.5 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0

---
*Requirements defined: 2026-02-03*
*Traceability updated: 2026-02-05 after Phase 26 completion (v1.5 complete)*
