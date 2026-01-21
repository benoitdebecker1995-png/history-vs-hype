---
phase: 03-research-structure
plan: 01
subsystem: templates
tags: [research, source-attribution, notebooklm, templates]

dependency-graph:
  requires:
    - Phase 2 (style consolidation complete)
  provides:
    - Unified source attribution format
    - Standard _research subfolder structure
    - NotebookLM-ready bibliographic format
  affects:
    - Plan 03-02 (claims database integration)
    - /new-video command workflow
    - All future video research

tech-stack:
  added: []
  patterns:
    - "[P]/[A]/[M] prefix notation for source categorization"
    - "Author (Tier X) - Title, p. page format for claims"
    - "Structured _research/ subfolder for 10+ source projects"

key-files:
  created:
    - .claude/templates/_RESEARCH-SUBFOLDER-TEMPLATE.md
  modified:
    - .claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md

decisions:
  - "Unified source attribution uses Author (Tier X) - Title, p. page format"
  - "[P]/[A]/[M] prefixes categorize sources as Primary/Academic/Modern"
  - "_research/ subfolder recommended for 10+ source projects, optional for simpler ones"
  - "NotebookLM filename format: [P1] Document-Name.pdf"

metrics:
  duration: "2 minutes"
  completed: "2026-01-21"
---

# Phase 03 Plan 01: Research Template Standardization Summary

**One-liner:** Unified source attribution format using Tier/page/prefix notation across research templates.

## What Was Done

### Task 1: Updated 01-VERIFIED-RESEARCH-TEMPLATE.md

**Changes:**
- Added NOTEBOOKLM SOURCES section with categorized format:
  - Primary Sources [P]: Government documents, treaties, archives
  - Academic Sources [A]: Monographs, journals, book chapters
  - Modern Context [M]: News articles, reports, recent events
- Updated claim format to require minimum 2 sources with explicit Tier and page numbers
- Updated quote format with Source/Tier/Verified/Used in script fields
- Streamlined document by removing redundant sections
- Added "Check VERIFIED-CLAIMS-DATABASE.md" to quality gate checklist

**Commit:** `022def2`

### Task 2: Created _RESEARCH-SUBFOLDER-TEMPLATE.md

**Contents:**
- Standard folder structure diagram for video projects
- Complete starter template for `00-NOTEBOOKLM-SOURCE-LIST.md`
- Complete starter template for `01-PRELIMINARY-RESEARCH.md`
- Complete starter template for `02-NOTEBOOKLM-PROMPTS.md` with verification prompt template
- Usage notes for when to create vs. skip _research/ subfolder
- Integration guidance (01-VERIFIED-RESEARCH.md remains single source of truth)

**Commit:** `a66d074`

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Unified format: Author (Tier X) - *Title*, p. page | Matches existing best practice in Flat Earth project; includes all needed info |
| [P]/[A]/[M] prefix notation | Clear categorization; matches NotebookLM filename convention |
| _research/ for 10+ sources only | Simple projects don't need overhead; complex projects need organization |
| Keep 01-VERIFIED-RESEARCH.md at project root | Single source of truth principle; script pulls only from this file |

## Verification Results

| Check | Status |
|-------|--------|
| Claim format includes "Sources (min 2)" with Tier and page | PASS |
| Quote format includes Source/Tier/Verified/Used in script fields | PASS |
| Bibliographic format uses [P1]/[A1] prefix notation | PASS |
| Both templates use consistent attribution format | PASS |
| No conflicting format guidance remains | PASS |

## Deviations from Plan

None - plan executed exactly as written.

## Files Changed

| File | Action | Lines |
|------|--------|-------|
| `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md` | Modified | +121/-88 |
| `.claude/templates/_RESEARCH-SUBFOLDER-TEMPLATE.md` | Created | +335 |

## Next Phase Readiness

**Ready for Plan 03-02:** Claims database workflow integration

**Blockers:** None

**Dependencies satisfied:**
- Unified source attribution format now defined
- _research/ subfolder template available
- Both templates internally consistent

## Commits

1. `022def2`: feat(03-01): update research template with unified source attribution
2. `a66d074`: feat(03-01): create _research subfolder template
