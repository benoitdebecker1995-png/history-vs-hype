---
phase: 22-script-parser-entity-detection
plan: 01
subsystem: production-tools
tags: [python, parsing, nlp, regex, dataclass, script-analysis]

# Dependency graph
requires:
  - phase: none
    provides: foundational module (no dependencies)
provides:
  - ScriptParser class for markdown script parsing
  - EntityExtractor class for named entity detection
  - Section dataclass for structured script sections
  - Entity dataclass for extracted entities
  - CLI testing interface
affects: [23-broll-generation, 24-edit-guide, 25-metadata, 26-package-command]

# Tech tracking
tech-stack:
  added: [tools/production module]
  patterns: [lazy spaCy loading, keyword dictionaries, dataclass models]

key-files:
  created:
    - tools/production/__init__.py
    - tools/production/parser.py
    - tools/production/entities.py
  modified: []

key-decisions:
  - "Hybrid regex + optional spaCy approach for entity extraction"
  - "Section types inferred from position and heading keywords"
  - "Word count excludes B-roll markers and annotations"
  - "Entity deduplication via normalized text keys"

patterns-established:
  - "Marker stripping before word count and entity extraction"
  - "Lazy spaCy loading with graceful fallback to regex-only"
  - "Domain-specific keyword dictionaries for classification"

# Metrics
duration: 15min
completed: 2026-02-04
---

# Phase 22 Plan 01: Script Parser & Entity Detection Summary

**ScriptParser and EntityExtractor module for parsing markdown scripts into structured sections and extracting named entities (documents, places, people, dates, organizations) for downstream production tools**

## Performance

- **Duration:** 15 min
- **Started:** 2026-02-04T00:06:36Z
- **Completed:** 2026-02-04T00:21:00Z
- **Tasks:** 3/3
- **Files created:** 3

## Accomplishments

- Created tools/production/ module with public API (ScriptParser, EntityExtractor, Section, Entity)
- ScriptParser extracts H2 sections with word counts and section type inference
- EntityExtractor uses hybrid regex patterns for document, place, person, date, and organization detection
- Built CLI interface for testing (`python tools/production/parser.py script.md`)
- Successfully tested against Somaliland (21 sections, 98 entities) and Chagos (12 sections, 81 entities) scripts

## Task Commits

1. **Task 1: Create ScriptParser with Section detection** - `2ac5eff` (feat)
2. **Task 2: Create EntityExtractor with hybrid detection** - `2ac5eff` (feat)
3. **Task 3: Add basic CLI and integration test** - `2ac5eff` (feat)

All tasks committed together as single atomic commit for the complete module.

## Files Created

- `tools/production/__init__.py` - Module exports (ScriptParser, EntityExtractor, Section, Entity)
- `tools/production/parser.py` - ScriptParser class with parse_file(), parse_text(), Section dataclass
- `tools/production/entities.py` - EntityExtractor class with extract(), extract_from_sections(), Entity dataclass

## Decisions Made

1. **Hybrid regex approach without spaCy dependency** - Regex patterns detect domain-specific entities reliably. spaCy is optional enhancement (use_spacy=True) for users who have it installed.

2. **Section types from position and keywords** - First section = intro, last = conclusion, middle = body. Override with keyword detection (opening, hook, conclusion, end card).

3. **Word count excludes all markers** - B-roll markers like `[MAP: ...]`, `**[ON-CAMERA]**`, `[DOCUMENT DISPLAY: ...]` are stripped before counting spoken words.

4. **Entity deduplication via normalized keys** - Lowercase, strip "the ", collapse whitespace. Same entity mentioned multiple times merges into one with aggregated mentions and positions.

5. **Person blocklist for false positives** - Filter out marker-derived false positives like "talking head", "text on screen", etc.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed false positive person entities from B-roll markers**
- **Found during:** Task 3 (CLI testing)
- **Issue:** "KING HEAD" detected as person from "[TALKING HEAD]" marker due to "king" in title keywords
- **Fix:** Added marker stripping before entity extraction and person blocklist for common false positives
- **Files modified:** tools/production/entities.py
- **Verification:** Re-ran CLI on Chagos script, "KING HEAD" no longer appears
- **Committed in:** 2ac5eff (same commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Essential for accurate entity detection. No scope creep.

## Issues Encountered

None - implementation proceeded as planned.

## User Setup Required

None - no external service configuration required. Module uses only Python standard library plus optional spaCy.

## Next Phase Readiness

- ScriptParser and EntityExtractor ready for Phase 23 (B-Roll Generation)
- API exports available via `from tools.production import ScriptParser, EntityExtractor`
- Both test scripts (Somaliland, Chagos) parse successfully
- Entity types align with B-roll generation needs (documents, places, maps, people)

---
*Phase: 22-script-parser-entity-detection*
*Completed: 2026-02-04*
