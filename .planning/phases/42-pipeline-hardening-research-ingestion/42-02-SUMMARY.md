---
phase: 42-pipeline-hardening-research-ingestion
plan: "02"
subsystem: research-tools
tags: [nlm-ingestion, research-workflow, claim-extraction, verified-research]
dependency_graph:
  requires: []
  provides: [nlm-ingestion-tool, research-ingest-command]
  affects: [research-workflow, verified-research-pipeline]
tech_stack:
  added: [tools/research/nlm_ingest.py, tools/research/__init__.py]
  patterns: [regex-based-parsing, dict-return-api, class-per-concern, error-dict-never-raise]
key_files:
  created:
    - tools/research/nlm_ingest.py
    - tools/research/__init__.py
  modified:
    - .claude/commands/research.md
decisions:
  - "Hybrid parsing strategy: structured (bullet) first, fall back to freeform sentence splitting — handles both NLM output modes without configuration"
  - "Error dict API (never raise) keeps slash command integration simple — Claude can check 'error' key before proceeding"
  - "Five class concerns: Parser, Extractor, ReviewGenerator, ReviewReader, Writer — each independently testable, each with one job"
  - "Claim type detection by keyword heuristics (quote > definition > statistic > event > claim) — order matters, most-specific first"
  - "Fallback section INGESTED CLAIMS (Unsorted) created at end of file when no matching section heading found — ensures no claim is ever silently dropped"
metrics:
  duration: "4 minutes"
  completed: "2026-02-20"
  tasks_completed: 2
  files_created: 2
  files_modified: 1
---

# Phase 42 Plan 02: NLM Ingestion Tool Summary

NLM-to-VERIFIED-RESEARCH pipeline: regex claim extraction, typed confidence scoring, markdown checklist review, and section-mapped file writing — replacing manual copy-paste reformatting.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Create NLM ingestion tool | 3496c99 | tools/research/nlm_ingest.py, tools/research/__init__.py |
| 2 | Integrate into /research command | 82df069 | .claude/commands/research.md |

## What Was Built

### tools/research/nlm_ingest.py (430 lines)

Five-class pipeline for the full ingestion flow:

**NLMParser** — Parses raw NotebookLM output into claim-candidate chunks. Tries structured (bullet-point) format first via `re` bullet detection, falls back to freeform sentence-splitting near citation markers. Six citation pattern regexes cover `Author (Year, p.XX)`, `[Source N, p.XX]`, `page XX`, `p.XX`, `on page XX`, and parenthetical variants. Returns chunks with `text`, `citation`, `source_ref`, `line_number`, and parse stats including `citation_coverage`.

**ClaimExtractor** — Categorizes chunks by type (statistic / quote / event / definition / claim) using keyword heuristics applied in specificity order. Assigns confidence (`high` = author + page, `medium` = one of those, `low` = neither). Produces `by_type` summary counts.

**ReviewGenerator** — Writes a markdown checklist file to `_research/_NLM-REVIEW-[timestamp].md`. Groups claims by type (statistics first, then quotes, events, definitions, general claims). Each claim gets a `- [ ] **[ID]**` checkbox line, citation sub-line, confidence sub-line, and full-text expansion for claims over 120 chars.

**ReviewReader** — Parses the user-edited review file. Tracks current section to preserve type context across state changes. Extracts approved (`[x]`) and rejected (`[ ]`) items with their (potentially edited) text and citation. Skips placeholder "none found" citations.

**VerifiedResearchWriter** — Inserts approved claims into the correct section of `01-VERIFIED-RESEARCH.md` using section heading candidates per type (e.g. statistics → KEY STATISTICS / ECONOMIC DATA / VERIFIED NUMBERS). Falls back to creating `## INGESTED CLAIMS (Unsorted)` at end of file when no matching heading exists. Each claim written in VERIFIED-RESEARCH format with status, claim text, source, and ingestion date.

**Orchestration functions** (`ingest()` and `apply_review()`) connect the steps for slash command use. Both return error dicts on failure, never raise.

### tools/research/__init__.py (7 lines)

Package init with docstring and version.

### .claude/commands/research.md (updated)

Added `--ingest` and `--apply-review` to flags table. Added full "NLM INGESTION WORKFLOW" section after EXISTING PROJECT WORKFLOW, documenting Steps 1-5: getting NLM output, locating project folder, running `ingest()` via Bash, user review, and running `apply_review()` via Bash. Includes example stats output and explicit note that Claude executes the Python tool via Bash (not direct import).

## Verification Results

All 6 plan verification steps passed:

1. All 5 classes importable: PASS
2. Parse test: 2 chunks from sample text (Smith + Allen): PASS
3. Extract test: statistic categorized correctly: PASS
4. Review roundtrip: generate 3-claim file, approve 2, read back, write to VR: PASS
5. /research command: --ingest flag, --apply-review flag, NLM INGESTION WORKFLOW section, Steps 1-5, nlm_ingest references: PASS

## Deviations from Plan

None — plan executed exactly as written.

## Self-Check

Files created:
- tools/research/nlm_ingest.py: EXISTS
- tools/research/__init__.py: EXISTS
- .claude/commands/research.md: MODIFIED

Commits:
- 3496c99: feat(42-02): create NLM ingestion tool
- 82df069: feat(42-02): integrate NLM ingestion into /research slash command

## Self-Check: PASSED
