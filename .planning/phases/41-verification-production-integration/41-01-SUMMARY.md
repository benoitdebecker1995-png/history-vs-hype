---
phase: 41-verification-production-integration
plan: 01
subsystem: translation-verification
tags: [verification, translation, quality-gate, pre-production]

dependency_graph:
  requires:
    - phase-40-translation-pipeline
    - tools/translation/cross_checker.py
    - tools/translation/legal_annotator.py
    - tools/translation/surprise_detector.py
  provides:
    - /verify --translation mode
    - TRANSLATION-VERIFICATION.md reports
    - GREEN/YELLOW/RED verdict system
  affects:
    - .claude/commands/verify.md
    - pre-production workflow
    - translation quality assurance

tech_stack:
  added: []
  patterns:
    - Tiered verdict calculation (GREEN/YELLOW/RED)
    - Dual verification modes (audit/fresh)
    - Scholarly comparison via Claude API
    - Markdown report generation

key_files:
  created:
    - tools/translation/verification.py: "804-line verification engine with audit/fresh modes, scholarly comparison, verdict calculation"
  modified:
    - .claude/commands/verify.md: "Added TRANSLATION VERIFICATION section with usage, modes, verdict table"

decisions:
  - "Audit mode default (fast) vs fresh mode for testing different versions"
  - "Three-tier verdict system aligned with filming decisions (proceed/review/revise)"
  - "Optional scholarly comparison - user file or Claude knowledge fallback"
  - "Coverage estimation from annotation count vs section count (rough approximation)"

metrics:
  duration_minutes: 4
  completed_date: 2026-02-18
  commits:
    - 31212d1: "feat(41-01): create translation verification module (804 lines)"
    - 53a8cdb: "feat(41-01): integrate /verify --translation mode"
---

# Phase 41 Plan 01: Translation Verification Integration Summary

**One-liner:** /verify --translation mode with audit/fresh verification, scholarly comparison, and GREEN/YELLOW/RED filming verdicts

## What Was Built

### Core Module (tools/translation/verification.py - 804 lines)

**TranslationVerifier class** with two verification modes:

**Mode 1: Audit (default) - Completeness check**
- Reads existing formatted translation output
- Checks cross-check section exists (not [PENDING])
- Verifies legal annotations present (parses **Notes:** sections)
- Detects surprise clauses if narrative analysis was run
- Counts pending [NEEDS CROSS-CHECK] placeholders
- Parses discrepancy severity (HIGH/MEDIUM/LOW) from cross-check results
- Estimates annotation coverage from footnote count vs section count

**Mode 2: Fresh - Re-run verification**
- Extracts sections from formatted output file
- Re-runs CrossChecker against independent translation
- Re-runs LegalAnnotator for legal term definitions
- Re-runs SurpriseDetector if narrative provided
- Compares fresh results against existing output
- Useful when translation updated or testing different backends

**Scholarly Comparison (optional)**
- User-provided file: Compare translation against scholarly description
- Claude knowledge fallback: Ask Claude what provisions scholars typically cite
- Uses Claude API for semantic comparison
- Identifies omissions and contradictions
- Produces alignment score (0-1)

**Verdict Calculation**
```
GREEN (proceed):
- 0 HIGH discrepancies
- >90% annotation coverage
- Scholarly alignment >0.9 (if checked)
- No pending placeholders

YELLOW (review):
- 1-2 MEDIUM discrepancies
- 80-90% annotation coverage
- Scholarly alignment 0.7-0.9
- Acceptable for filming with review

RED (revise):
- ANY HIGH discrepancies
- <80% annotation coverage
- Scholarly alignment <0.7
- Must fix before filming
```

**Report Generation**
- Full report to TRANSLATION-VERIFICATION.md in project folder
- Sections: Verdict, Completeness, Discrepancies, Annotations, Scholarly Comparison, Recommendation
- Condensed terminal summary: Verdict + top 3 issues + report path
- Color-coded terminal output (green/yellow/red)

### Command Integration (.claude/commands/verify.md)

Added comprehensive TRANSLATION VERIFICATION section:

**Usage patterns:**
```bash
/verify --translation [project]                        # Audit mode
/verify --translation [project] --fresh                # Re-run verification
/verify --translation [project] --scholarly-summary FILE  # Compare scholarly
```

**Documentation added:**
- Mode explanations (audit vs fresh, when to use each)
- Scholarly comparison option (user file or Claude knowledge)
- Process workflow (4 steps: locate → verify → generate → print)
- Output format examples (terminal + full report)
- Verdict interpretation table
- Post-verification workflow guidance (what to do after GREEN/YELLOW/RED)

**Updated sections:**
- Usage block: Added `/verify --translation [project]`
- Flags table: Added `--translation` row with example
- Section heading: "TRANSLATION VERIFICATION (`--translation`)"

## Deviations from Plan

None - plan executed exactly as written.

## Verification

**Task 1 verification:**
```bash
$ python tools/translation/verification.py --help
# ✓ Shows usage with --mode, --scholarly-summary, --document-name flags

$ python -c "from tools.translation.verification import TranslationVerifier; v = TranslationVerifier(); print('Import successful')"
# ✓ Import successful
```

**Task 2 verification:**
```bash
$ grep -n "TRANSLATION VERIFICATION" .claude/commands/verify.md
# ✓ 317:## TRANSLATION VERIFICATION (`--translation`)

$ grep -n "TranslationVerifier" .claude/commands/verify.md
# ✓ 350:2. Run TranslationVerifier in specified mode

$ grep -n "\-\-translation" .claude/commands/verify.md
# ✓ Multiple matches in usage, flags, and section content
```

## Integration Points

**Consumes (from Phase 40):**
- tools/translation/cross_checker.py - CrossChecker class for independent translation
- tools/translation/legal_annotator.py - LegalAnnotator class for term definitions
- tools/translation/surprise_detector.py - SurpriseDetector class for narrative analysis
- Formatted translation output files (with ## Article sections, ### Original, ### Translation)

**Produces:**
- TRANSLATION-VERIFICATION.md report in project folder
- Terminal summary with verdict + top issues
- Exit code 0 (GREEN/YELLOW) or 1 (RED) for scripting

**Used by (Phase 41 Plans 02-03):**
- /verify --translation command → pre-production quality gate
- Plan 41-02: /script --document-mode reads verified translations
- Plan 41-03: /prep --split-screen uses verified output for edit guides

## Files Modified

| File | Lines Changed | Purpose |
|------|---------------|---------|
| tools/translation/verification.py | 804 (new) | Core verification engine |
| .claude/commands/verify.md | +96 | Command documentation |

## What's Next

**Phase 41 Plan 02: Document-Structured Script Generation**
- /script --document-mode flag
- Clause-by-clause script structure
- Surprise beats as script sections
- Document evidence markers for B-roll

**Phase 41 Plan 03: Split-Screen Edit Guide**
- /prep --split-screen mode
- Timing calculations for split-screen display
- Asset lists (original doc pages, translation overlays)
- Surprise moment B-roll suggestions

## Requirements Satisfied

- **VERF-01:** User can run /verify --translation to verify translated documents ✓
- **VERF-02:** System checks translation completeness (cross-check done, annotations present) ✓
- **VERF-03:** System compares translation against scholarly descriptions when provided ✓

## Usage Example

```bash
# Step 1: Run translation pipeline (Phase 40)
python tools/translation/cli.py translate vichy-statute-original.txt --language french

# Step 2: Verify before filming
/verify --translation 37-vichy-statute

# Terminal output:
# TRANSLATION VERIFICATION: Vichy Statute on Jews
# VERDICT: YELLOW
#
# Top issues:
# 1. 2 MEDIUM severity discrepancies (reviewable)
# 2. Annotation coverage moderate (85%)
# 3. No issues found
#
# Full report: video-projects/37-vichy-statute/TRANSLATION-VERIFICATION.md

# Step 3: Review TRANSLATION-VERIFICATION.md report

# Step 4: If acceptable, proceed to script generation
/script --document-mode
```

## Self-Check: PASSED

**Verification module exists:**
```bash
$ [ -f "tools/translation/verification.py" ] && echo "FOUND" || echo "MISSING"
FOUND ✓
```

**Integration documented:**
```bash
$ grep -q "TRANSLATION VERIFICATION" .claude/commands/verify.md && echo "FOUND" || echo "MISSING"
FOUND ✓
```

**Commits exist:**
```bash
$ git log --oneline --all | grep -q "31212d1" && echo "FOUND: 31212d1" || echo "MISSING"
FOUND: 31212d1 ✓

$ git log --oneline --all | grep -q "53a8cdb" && echo "FOUND: 53a8cdb" || echo "MISSING"
FOUND: 53a8cdb ✓
```

**Import test passes:**
```bash
$ python -c "from tools.translation.verification import TranslationVerifier; print('OK')"
OK ✓
```

All verification checks passed. Plan delivered as specified.
