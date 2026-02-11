---
phase: 34-notebooklm-research-bridge
plan: 02
subsystem: research-workflow
tags: [notebooklm, citation-extraction, prompt-library, research-automation]
dependency_graph:
  requires: []
  provides:
    - "NotebookLM citation extraction to VERIFIED-RESEARCH.md format"
    - "Static research prompt library for NotebookLM sessions"
    - "/verify --extract-nlm command"
  affects:
    - "Pre-production Phase 2 (NotebookLM research workflow)"
tech_stack:
  added:
    - "Regex-based citation parsing (stdlib only)"
  patterns:
    - "Error dict pattern (no exceptions raised)"
    - "CLI argparse interface"
    - "Multi-pattern regex extraction"
key_files:
  created:
    - "tools/citation_extractor.py"
    - ".claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md"
  modified:
    - ".claude/commands/verify.md"
decisions:
  - decision: "Use regex-based parsing instead of LLM for citation extraction"
    rationale: "NotebookLM citation formats are predictable ([1], [2] markers, SOURCES sections) — regex is fast, free, and deterministic"
    alternatives: ["Claude API parsing", "spaCy NER"]
  - decision: "Static prompt library as reference document"
    rationale: "Prompts are stable templates that don't need dynamic generation — reference doc is simpler and always available"
  - decision: "Separate NOTEBOOKLM-EXTRACTIONS.md output (not direct VERIFIED-RESEARCH.md write)"
    rationale: "Preserves human review step before facts enter single source of truth"
metrics:
  tasks_completed: 3
  files_created: 2
  files_modified: 1
  commits: 3
  completed_date: 2026-02-11
---

# Phase 34 Plan 02: Citation Extractor + Prompt Library Summary

**One-liner:** Regex-based NotebookLM citation parser extracts structured citations, plus a static prompt library with 5+ research prompts organized by phase and video type.

## What Was Built

### 1. Citation Extractor (`tools/citation_extractor.py`, 356 LOC)

Python CLI tool that parses NotebookLM chat output and extracts structured citations into NOTEBOOKLM-EXTRACTIONS.md format compatible with VERIFIED-RESEARCH.md.

**Core functions:**
- `parse_citations(text)` — Multi-pattern regex extraction:
  - Pattern A: Source legend markers `[1] Author, Title, p. 45`
  - Pattern B: SOURCES/REFERENCES section parsing
  - Pattern C: Inline parenthetical citations `(Author, Year, p. X)`
- `extract_citations(file_path)` — Reads input file with UTF-8 (latin-1 fallback), calls parser
- `write_extractions(citations, output_path, format)` — Writes NOTEBOOKLM-EXTRACTIONS.md
- `main()` — argparse CLI entry point

**CLI arguments:**
- `input` (positional): Path to NotebookLM chat output file
- `--output`: Output file path (default: NOTEBOOKLM-EXTRACTIONS.md in same directory)
- `--format`: detailed (full checklist) or compact (table)
- `--stats-only`: Print statistics without writing file

### 2. Prompt Library (`.claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md`, 404 lines)

Static reference document with copy-paste-ready research prompts:
- **5 Core Prompts:** Claim verification, quote extraction, counter-evidence, timeline construction, cross-source synthesis
- **3 Video-Type Variants:** Territorial (treaties/ICJ), ideological (manuscripts/historiography), fact-check (court filings/official records)
- **Audio Overview Prompts:** Customized prompts for NotebookLM's Audio Overview feature
- **Output Format Guide:** Formatting instructions for extractor-compatible output

### 3. Command Integration (`.claude/commands/verify.md`)

Updated `/verify` command with:
- `--extract-nlm` flag in flags table
- Full NOTEBOOKLM CITATION EXTRACTION section with CLI usage
- Arguments table, output description, requirements

## Deviations from Plan

None significant — all three tasks executed as planned.

## Verification Results

✅ **citation_extractor.py:** CLI works (`--help` shows all arguments), error handling functional
✅ **NOTEBOOKLM-RESEARCH-PROMPTS.md:** 404 lines, contains all required prompt categories
✅ **verify.md:** `--extract-nlm` flag documented with full CLI usage instructions

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| 1 | 98ee560 | Create NotebookLM citation extractor tool |
| 2 | 1e82cf0 | Create NotebookLM research prompt library |
| 3 | 402139d | Update /verify command with NotebookLM extraction |

## Self-Check: PASSED

All files exist, commits verified, CLI functional.
