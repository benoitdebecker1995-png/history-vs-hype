# Roadmap: History vs Hype Workspace Optimization

**Created:** 2025-01-19
**Depth:** Comprehensive
**Phases:** 6
**Requirements:** 15 v1 mapped

## Overview

This roadmap transforms a content production workspace that grew organically into a streamlined system for solo creator efficiency. The work clusters into natural delivery boundaries: cleanup first, then foundational systems (style, research), then production pipeline (scripts), then workflow simplification, then competitive intelligence. Each phase delivers verifiable capability before the next begins.

---

## Phase 0.1: Edit Guide Optimization (INSERTED - URGENT)

**Goal:** Improve edit-guide command with cut candidates, pacing analysis, and runtime comparison — ready for Iran Part 1 video shipping Thursday

**Dependencies:** None (urgent production need)

**Requirements:**
- EDIT-01: Add CUT CANDIDATES section to identify trimmable content with priority levels
- EDIT-02: Add pacing/retention risk analysis to flag dropout zones
- EDIT-03: Add runtime comparison (script estimate vs actual SRT)
- EDIT-04: Test improved guide against Iran Part 1 script

**Plans:** 2 plans

Plans:
- [ ] 0.1-01-PLAN.md — Finalize edit-guide.md with clean structure, cut detection heuristics, runtime estimation
- [ ] 0.1-02-PLAN.md — Test against Iran Part 1 (requires SRT file)

**Success Criteria:**
1. Running /edit-guide on Iran SRT produces actionable cut recommendations
2. Pacing analysis identifies sections at high dropout risk
3. Guide helps editor trim 29-min recording to ~25-min target

**Deadline:** Thursday (Iran Part 1 release)

---

## Phase 1: File Cleanup

**Goal:** Workspace contains only current, relevant files with clear organization

**Dependencies:** None (foundation)

**Requirements:**
- CLNP-01: Remove outdated files that no longer reflect current workflow
- CLNP-02: Consolidate duplicate files into single sources of truth
- CLNP-03: Establish and document file naming conventions

**Plans:** 4 plans

Plans:
- [ ] 01-01-PLAN.md - Delete confirmed outdated files and review candidates
- [ ] 01-02-PLAN.md - Consolidate duplicate files in transcripts/ and research/
- [ ] 01-03-PLAN.md - Relocate misplaced files and update references
- [ ] 01-04-PLAN.md - Fix naming convention violations and document standards

**Success Criteria:**
1. User can find any file in under 30 seconds using documented naming patterns
2. No duplicate files exist for the same purpose (one source of truth per concept)
3. Archive folders contain only files with clear "why archived" documentation
4. New file creation follows documented naming convention without ambiguity

---

## Phase 2: Style Consolidation

**Goal:** Single authoritative style reference that scriptwriter enforces consistently

**Dependencies:** Phase 1 (cleanup removes conflicting style docs)

**Requirements:**
- STYL-01: Consolidate scattered style notes into one authoritative reference
- STYL-02: Scriptwriter enforces spoken-delivery voice (not essay voice)
- STYL-03: Preference tracking system (captures word choices, patterns from feedback)

**Success Criteria:**
1. Scriptwriter produces scripts that sound natural when read aloud on first draft
2. User's speaking patterns (dashes, contractions, embedded explanations) appear consistently in generated scripts
3. New style preferences from feedback get captured and applied to future scripts
4. No conflicting style guidance exists anywhere in workspace

---

## Phase 3: Research Structure

**Goal:** Research is organized for both per-video use and cross-video reuse

**Dependencies:** Phase 1 (cleanup establishes naming conventions)

**Requirements:**
- RSCH-01: Per-video organized research files with clear structure
- RSCH-02: Cross-video verified facts database (reusable across videos)
- RSCH-03: Standard source attribution format (every fact traces to citation)

**Success Criteria:**
1. User can find any verified fact and its source citation within 60 seconds
2. Facts verified for one video are discoverable when researching related topics
3. Every claim in research files has complete attribution (source, page, date accessed)
4. NotebookLM outputs integrate cleanly into research file structure

---

## Phase 4: Script Management

**Goal:** One canonical script per video with teleprompter-ready output

**Dependencies:** Phase 2 (style guide), Phase 3 (research structure)

**Requirements:**
- SCRP-01: One canonical script file per video (git tracks changes, no version sprawl)
- SCRP-02: Teleprompter-ready export format (clean, readable output)

**Success Criteria:**
1. Each video project has exactly one script file (no V2, V3, FINAL, FINAL-FINAL)
2. Script history is visible via git log, not file proliferation
3. Teleprompter export produces clean text without markdown formatting or metadata
4. User never asks "which script is the real one?"

---

## Phase 5: Workflow Simplification

**Goal:** Common tasks have obvious entry points with up-to-date documentation

**Dependencies:** Phases 1-4 (core systems must work before simplifying access)

**Requirements:**
- WKFL-01: Clear entry points for common tasks (obvious starting commands)
- WKFL-02: Documentation cleanup (remove/update outdated guides)

**Success Criteria:**
1. User can start any common task (new video, fact-check, script) with one obvious command
2. All documentation references current workflow (no outdated screenshots or examples)
3. START-HERE.md accurately reflects the actual workflow
4. No guide references deprecated commands or file structures

---

## Phase 6: Competitive Intelligence

**Goal:** Systematic tracking of what works for top history creators

**Dependencies:** Phase 1 (organized workspace for storing intelligence)

**Requirements:**
- COMP-01: Technique tracking (document what works for top history creators)
- COMP-02: Gap identification (find underserved topics/angles in the niche)

**Success Criteria:**
1. User can look up proven techniques by creator or category (hooks, evidence presentation, pacing)
2. Gap analysis identifies at least 5 underserved topic areas with supporting evidence
3. New creator techniques get captured in structured format when discovered
4. Competitive insights inform topic selection for new videos

---

## Progress

| Phase | Status | Requirements | Mapped |
|-------|--------|--------------|--------|
| 0.1 - Edit Guide Optimization | **PLANNED** | EDIT-01, EDIT-02, EDIT-03, EDIT-04 | 4 |
| 1 - File Cleanup | Planned | CLNP-01, CLNP-02, CLNP-03 | 3 |
| 2 - Style Consolidation | Pending | STYL-01, STYL-02, STYL-03 | 3 |
| 3 - Research Structure | Pending | RSCH-01, RSCH-02, RSCH-03 | 3 |
| 4 - Script Management | Pending | SCRP-01, SCRP-02 | 2 |
| 5 - Workflow Simplification | Pending | WKFL-01, WKFL-02 | 2 |
| 6 - Competitive Intelligence | Pending | COMP-01, COMP-02 | 2 |

**Total:** 15/15 requirements mapped

---

## Dependency Graph

```
Phase 0.1 (Edit Guide - URGENT)
    |
    v
Phase 1 (Cleanup)
    |
    +---> Phase 2 (Style)
    |         |
    |         v
    +---> Phase 3 (Research) ---> Phase 4 (Scripts)
    |                                   |
    +-----------------------------------+
    |
    v
Phase 5 (Workflow)

Phase 1 ---> Phase 6 (Competitive Intel)
```

---

*Roadmap created: 2025-01-19*
*Phase 0.1 planned: 2025-01-19*
*Phase 1 planned: 2025-01-19*
