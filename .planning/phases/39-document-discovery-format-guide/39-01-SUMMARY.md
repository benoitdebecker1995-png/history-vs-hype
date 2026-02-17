---
phase: 39-document-discovery-format-guide
plan: 01
subsystem: discovery
tags: [translation, document-structure, archives, notebooklm]

# Dependency graph
requires:
  - phase: 38-choice-architecture
    provides: Tool architecture patterns (error dict, module structure, CLI design)
provides:
  - GapChecker class for translation gap verification across 10+ search categories
  - StructureAssessor class for document type classification and video length estimation
  - ArchiveLookup class with extensible ARCHIVE_REGISTRY (14 archives, academic editions prioritized)
  - Unified CLI with gap/structure/archive subcommands
affects: [40-translation-pipeline, 41-verification-integration]

# Tech tracking
tech-stack:
  added: []  # Pure Python, no new dependencies
  patterns:
    - Error dict pattern (returns {'error': msg}, never raises)
    - Extensible registry pattern for country-specific archives
    - Hybrid video length estimation (per-section formulas + overhead)

key-files:
  created:
    - tools/document_discovery/__init__.py
    - tools/document_discovery/gap_checker.py
    - tools/document_discovery/structure_assessor.py
    - tools/document_discovery/archive_lookup.py
    - tools/document_discovery/cli.py
  modified: []

key-decisions:
  - "Language-agnostic design from the start (works for French, Spanish, Latin, German documents)"
  - "Academic editions prioritized in archive lookups (critical editions with scholarly apparatus preferred)"
  - "Video length estimates use channel philosophy: 'As long as needed — optimize for completeness, not brevity'"
  - "Full vs excerpt scope options for user flexibility (full document or selected sections)"

patterns-established:
  - "ARCHIVE_REGISTRY extensible design: append new archives to list for country-specific additions"
  - "Document type classification: legal_code, treaty, book, letter, decree, other"
  - "Hybrid video length formula: base time per section + intro/conclusion overhead"
  - "Markdown and JSON output modes for all CLI commands"

requirements-completed: [DISC-01, DISC-02, DISC-03]

# Metrics
duration: 3min
completed: 2026-02-17
---

# Phase 39 Plan 01: Document Discovery Toolkit Summary

**Translation gap checker, document structure assessor, and archive lookup with 14+ sources — foundation for Untranslated Evidence Pipeline**

## Performance

- **Duration:** 3 minutes
- **Started:** 2026-02-17T13:17:35Z
- **Completed:** 2026-02-17T13:20:35Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- GapChecker verifies translation gaps across 10+ search categories (academic sourcebooks, Google Scholar, JSTOR, government portals, general web)
- StructureAssessor classifies documents by type and estimates video length (legal code ~2 min/article, book ~6 min/chapter)
- ArchiveLookup covers 14 archives with academic editions prioritized (Google Scholar critical editions, WorldCat, Légifrance, Gallica, Wikisource variants, Internet Archive, HathiTrust, Europeana, Library of Congress)
- Unified CLI with gap/structure/archive subcommands supporting markdown and JSON output

## Task Commits

Each task was committed atomically:

1. **Task 1: Gap checker + archive lookup modules** - `25f1ec6` (feat)
2. **Task 2: Structure assessor + CLI** - `0cd5401` (feat)

## Files Created/Modified
- `tools/document_discovery/__init__.py` - Package init with convenience imports
- `tools/document_discovery/gap_checker.py` - GapChecker class (DISC-01): translation gap verification across academic sourcebooks, Scholar, JSTOR, government portals, general web
- `tools/document_discovery/archive_lookup.py` - ArchiveLookup class (DISC-03): 14 archives with ARCHIVE_REGISTRY extensible design, academic editions prioritized
- `tools/document_discovery/structure_assessor.py` - StructureAssessor class (DISC-02): document type classification, video length estimation, markdown outline generation
- `tools/document_discovery/cli.py` - Unified CLI entry point with gap/structure/archive subcommands, markdown and JSON output modes

## Decisions Made

**Language-agnostic from the start:** Designed to work for any language (French, Spanish, Latin, German, etc.) without language-specific hardcoding. Verified with "Brevisima relacion de la destruccion de las Indias" test case.

**Academic editions prioritized:** ArchiveLookup always lists Google Scholar critical editions and WorldCat first, before free archives. Priority note explains scholarly apparatus value.

**Video length philosophy honored:** Estimates reflect channel philosophy "As long as needed — optimize for completeness, not brevity." Example: 10-article statute = 24 min, 16-chapter book = 102 min.

**Full vs excerpt flexibility:** Structure assessor provides both full-document and excerpt-based estimates, allowing user to choose scope after seeing document structure.

**Extensible registry pattern:** ARCHIVE_REGISTRY designed for easy country-specific additions (append to list) without code changes.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - all verification tests passed on first run.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Foundation complete for Phase 40 (Translation Pipeline). Ready to build:
- Translation workflow using gap checker to verify documents qualify
- Structure assessor output to plan video scope
- Archive lookup results to locate digitized originals

Verification commands working:
```bash
python tools/document_discovery/cli.py gap "Statut des Juifs 1940"
python tools/document_discovery/cli.py structure "Statut des Juifs 1940" --type legal_code --sections 10
python tools/document_discovery/cli.py archive "Statut des Juifs 1940" --language french
python tools/document_discovery/cli.py gap "query" --json
```

## Self-Check: PASSED

**Files created:**
- FOUND: tools/document_discovery/__init__.py
- FOUND: tools/document_discovery/gap_checker.py
- FOUND: tools/document_discovery/archive_lookup.py
- FOUND: tools/document_discovery/structure_assessor.py
- FOUND: tools/document_discovery/cli.py

**Commits exist:**
- FOUND: 25f1ec6 (Task 1)
- FOUND: 0cd5401 (Task 2)

---
*Phase: 39-document-discovery-format-guide*
*Completed: 2026-02-17*
