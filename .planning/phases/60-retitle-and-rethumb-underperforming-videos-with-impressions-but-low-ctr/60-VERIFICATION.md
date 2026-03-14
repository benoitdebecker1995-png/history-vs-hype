---
phase: 60-retitle-and-rethumb-underperforming-videos-with-impressions-but-low-ctr
verified: 2026-03-14T23:30:00Z
status: passed
score: 9/9 must-haves verified
re_verification: false
---

# Phase 60: Retitle and Rethumb Underperforming Videos Verification Report

**Phase Goal:** Retitle and rethumb underperforming videos with impressions but low CTR
**Verified:** 2026-03-14
**Status:** PASSED
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can run `/retitle` and get a SWAP-CHECKLIST.md with 5 retitle candidates | VERIFIED | Command fully documents full pipeline: audit → retention sort → generate → score → SWAP-CHECKLIST.md output at `channel-data/SWAP-CHECKLIST.md`. Steps 1-7 specified with Python code. |
| 2 | User can run `/retitle --audit` and see ranked underperformers without generating candidates | VERIFIED | `## AUDIT ONLY (--audit)` section (line 232) documents this mode explicitly. Runs audit top_n=10, applies retention weighting, displays format_report() with no generation. |
| 3 | Each checklist entry has old title, new title, new description lines, thumbnail concept, Studio link | VERIFIED | SWAP-CHECKLIST.md format (lines 143-209) specifies: OLD TITLE, NEW TITLE, All Scored Candidates, NEW DESCRIPTION (3 lines), THUMBNAIL section (status/type/concept/color/checker result), PRE-SWAP METRICS, Studio link. |
| 4 | Title candidates are scored by title_scorer and only non-REJECTED options appear | VERIFIED | Step 4c (lines 97-109) imports `score_title`, sorts by score, filters `grade != 'REJECTED' and score >= 65`. Shows rejection reason if no valid candidates. |
| 5 | Videos without SRT/scripts fall back to CANDIDATES dict or RETITLE-RECOMMENDATIONS.md | VERIFIED | Step 4b (lines 88-91) documents two-step fallback: `CANDIDATES.get(video_id)` first, then `channel-data/RETITLE-RECOMMENDATIONS.md`. Source indicated per video. |
| 6 | User can run `/retitle --check [video-id]` and get pre/post CTR comparison with success/revert recommendation | VERIFIED | `## POST-SWAP MEASUREMENT (--check)` section (lines 298-369) fully documented: locate file, 7-day guard, collect post-CTR, evaluate delta, update SWAP LOG, conditional ctr_ingest. |
| 7 | `/retitle --check` refuses to measure if swap is less than 7 days old | VERIFIED | Lines 319-322: explicitly checks days since swap, refuses with "Check back on [date + 7 days]" message if < 7 days. |
| 8 | User can run `/retitle --revert [video-id]` and get old title for copy-paste revert | VERIFIED | `## REVERT (--revert)` section (lines 373-394) fully documented: dual-location search, displays OLD TITLE verbatim with Studio link, updates SWAP LOG after user confirms. |
| 9 | SWAP LOG section in POST-PUBLISH-ANALYSIS tracks swap history with date, old/new title, pre/post CTR, result | VERIFIED | `## SWAP LOG INJECTION` section (lines 261-294) specifies format, append-not-overwrite rule, create-if-missing logic. Table format matches 60-RESEARCH.md spec: Date | Type | Old Value | New Value | Pre-CTR | Post-CTR | Result. |

**Score:** 9/9 truths verified

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `.claude/commands/retitle.md` | Slash command orchestrating retitle pipeline | VERIFIED | 426 lines — exceeds 80-line minimum. YAML frontmatter (description, model). All 4 operating modes documented with Python code blocks. |
| `tools/retitle_audit.py` | `audit()` and `format_report()` APIs | VERIFIED | 255 lines. `audit(min_impressions: int = 0, top_n: int = 0)` and `format_report(results)` present. Returns dict with: title, views, retention, ctr, impressions, title_issues, wasted_impressions, diagnosis. |
| `tools/retitle_gen.py` | `generate_script_titles()`, `CANDIDATES`, `VIDEO_PROJECT_MAP` | VERIFIED | 903 lines. All three required symbols present at expected locations. |
| `tools/title_scorer.py` | `score_title()` | VERIFIED | `score_title(title, db_path=None)` at line 115. |
| `tools/preflight/thumbnail_checker.py` | `check_thumbnail()`, `check_project()` | VERIFIED | 332 lines. Both functions present at lines 126 and 231. |
| `tools/ctr_ingest.py` | `ingest_synthesis_ctr()` (optional dependency) | VERIFIED | Exists. `ingest_synthesis_ctr()` at line 34. Command correctly guards invocation with `os.path.exists('tools/ctr_ingest.py')` check. |
| `channel-data/RETITLE-RECOMMENDATIONS.md` | Fallback candidate pool | VERIFIED | File exists as fallback source. |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `.claude/commands/retitle.md` | `tools/retitle_audit` | `from tools.retitle_audit import audit, format_report` | WIRED | Explicit import at lines 53 and 239. |
| `.claude/commands/retitle.md` | `tools/retitle_gen` | `from tools.retitle_gen import generate_script_titles, CANDIDATES, VIDEO_PROJECT_MAP` | WIRED | Explicit import at line 83. |
| `.claude/commands/retitle.md` | `tools/title_scorer` | `from tools.title_scorer import score_title` | WIRED | Explicit import at line 97. |
| `.claude/commands/retitle.md` | `tools/preflight/thumbnail_checker` | `from tools.preflight.thumbnail_checker import check_project` | WIRED | Explicit import at line 116. |
| `.claude/commands/retitle.md` | `tools/ctr_ingest` | `from tools.ctr_ingest import ingest_synthesis_ctr` (conditional) | WIRED | Lines 349-357: existence guard then conditional import on success path. |
| `.claude/commands/retitle.md` | POST-PUBLISH-ANALYSIS | SWAP LOG section read/write | WIRED | Dual-location search (channel-data/analyses/ + video-projects/), append-not-overwrite rules, create-if-missing logic. |

---

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| RETITLE-01 | Plan 01 | `/retitle` audits underperformers ranked by wasted impressions with retention weighting (min 500 impressions, top 5) | SATISFIED | Step 2-3 in command: `audit(min_impressions=500, top_n=5)` + retention_bonus formula. |
| RETITLE-02 | Plan 01 | `/retitle` generates script-based title candidates scored by title_scorer, outputs SWAP-CHECKLIST.md | SATISFIED | Steps 4-6 in command: `generate_script_titles()` → `score_title()` → SWAP-CHECKLIST.md write. |
| RETITLE-03 | Plan 01 | `/retitle --audit` shows ranked underperformer list without generating candidates | SATISFIED | `## AUDIT ONLY (--audit)` section explicitly documents audit-only mode with no file generation. |
| RETITLE-04 | Plan 02 | `/retitle --check [video-id]` measures 7-day post-swap CTR, enforces minimum wait, triggers ctr_ingest on success | SATISFIED | Full `--check` flow documented with 7-day guard, CTR collection, delta evaluation, conditional ctr_ingest trigger. |
| RETITLE-05 | Plan 02 | `/retitle --revert [video-id]` surfaces old title from SWAP LOG for copy-paste revert | SATISFIED | `## REVERT (--revert)` section documented with SWAP LOG read, verbatim old title display, Studio link. |
| RETITLE-06 | Plan 02 | SWAP LOG section in POST-PUBLISH-ANALYSIS.md tracks swap history per video | SATISFIED | SWAP LOG injection section specifies format (Date/Type/Old Value/New Value/Pre-CTR/Post-CTR/Result), append semantics, create-if-missing. No existing SWAP LOG entries found — correct, as no swaps have been executed yet (tooling phase). |

**Orphaned requirements:** None. All 6 RETITLE-* IDs from REQUIREMENTS.md are claimed by plans in this phase.

---

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None found | — | — | — | — |

No TODO/FIXME/placeholder comments, empty implementations, or console.log-only stubs found in `.claude/commands/retitle.md`. All code blocks contain substantive logic, not scaffolding.

---

## Human Verification Required

### 1. End-to-end pipeline run

**Test:** Run `/retitle --audit` in Claude Code, verify ranked underperformer list appears.
**Expected:** Top 10 videos ranked by wasted_impressions with retention-weighted priority column.
**Why human:** Python tool execution and output formatting requires live Claude Code invocation.

### 2. SWAP-CHECKLIST.md generation

**Test:** Run `/retitle` (full pipeline), verify SWAP-CHECKLIST.md is created in `channel-data/`.
**Expected:** File with 5 video entries each containing OLD TITLE, NEW TITLE with score, NEW DESCRIPTION, THUMBNAIL section, PRE-SWAP METRICS, Studio link.
**Why human:** Actual file generation requires Claude Code to execute the pipeline.

### 3. 7-day guard enforcement

**Test:** Run `/retitle --check [video-id]` with a video swapped less than 7 days ago.
**Expected:** Claude refuses measurement and displays date to return.
**Why human:** Requires a real SWAP LOG entry with a recent date.

---

## Gaps Summary

No gaps. All 9 observable truths verified, all 6 requirements satisfied, all key links wired. The single remaining concern is expected: no SWAP LOG entries exist in POST-PUBLISH-ANALYSIS files, but that is correct — RETITLE-06 requires the spec and tooling to exist, not that swaps have already been executed. The command fully implements the injection mechanism.

The audit function signature uses default `min_impressions=0` (not `=500`), but the command correctly passes `min_impressions=500` at call time, so the behavior matches the requirement.

---

_Verified: 2026-03-14_
_Verifier: Claude (gsd-verifier)_
