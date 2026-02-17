---
phase: 40-translation-pipeline
plan: 01
subsystem: translation-pipeline
tags: [translation, claude-api, structure-detection, split-screen, legal-documents]
dependency_graph:
  requires:
    - "Phase 39: document_discovery (structure assessor for timing estimates)"
    - "anthropic SDK (pip install anthropic>=0.40.0)"
  provides:
    - "tools/translation/ package"
    - "Structure detection (article/clause boundaries)"
    - "Claude-based clause-by-clause translation"
    - "Split-screen paired output formatting"
  affects:
    - "Plan 40-02: crosscheck uses translator output"
    - "Plan 40-03: surprise detection uses translated sections"
tech_stack:
  added:
    - "Anthropic Claude API (claude-sonnet-4-20250514)"
    - "Multi-language regex patterns (French, Spanish, German, Latin)"
  patterns:
    - "Error dict pattern (return {'error': msg}, never raise)"
    - "Optional dependency integration (Phase 39 structure assessor)"
    - "Full document context per clause (highlight active clause)"
    - "Progress callbacks for CLI feedback"
key_files:
  created:
    - "tools/translation/__init__.py (14 lines)"
    - "tools/translation/structure_detector.py (297 lines)"
    - "tools/translation/formatter.py (219 lines)"
    - "tools/translation/translator.py (301 lines)"
    - "tools/translation/cli.py (291 lines)"
  modified: []
decisions:
  - "Clause-by-clause translation approach (one API call per article/section) for accuracy over token cost"
  - "Full document context sent with each clause (highlighted with >>> TRANSLATE THIS CLAUSE <<< markers)"
  - "Auto-detection with user confirmation via --dry-run before committing to API calls"
  - "Split on double newlines as fallback when no article markers detected"
  - "Lower temperature (0.3) for translation consistency"
  - "Notes field captures translator observations (ambiguous terms, alternative renderings)"
metrics:
  duration_minutes: 4
  lines_of_code: 1122
  files_created: 5
  commits: 2
  completed_date: "2026-02-17"
---

# Phase 40 Plan 01: Core Translation Engine Summary

**Built the foundation of the translation pipeline:** structure detection, Claude-based clause-by-clause translation with full document context, split-screen paired output formatting, and comprehensive CLI for the entire package.

## What Was Built

### Structure Detection (297 lines)

Multi-language article/clause boundary detection:

**Supported markers:**
- French: `Article N`, `Art. N`, `ARTICLE N`
- Spanish: `Artículo N`, `Art. N`
- German: `Artikel N`, `§ N`
- Latin: `Articulus N`
- Generic: `Section N`, `Chapter N`, `Clause N`
- Roman numerals: `I.`, `II.`, `III.`

**Detection algorithm:**
1. Try regex patterns for article markers
2. Extract preamble (text before first article)
3. Define section boundaries (start to next marker or end)
4. Fall back to paragraph splitting (double newline) if no markers found

**Output:** Section list with IDs, headings, body text, line ranges

**Optional integration:** If Phase 39 structure assessor available, includes video timing estimates

### Translation Engine (301 lines)

Claude-based clause-by-clause translation:

**Key approach:**
- Each clause sent to Claude API with **full document context**
- Active clause highlighted: `>>> TRANSLATE THIS CLAUSE <<<`
- Context prevents mistranslation of terms that depend on surrounding clauses
- Lower temperature (0.3) for consistency

**System prompt priorities:**
1. Accuracy and precision over readability
2. Preserve original register and formality
3. Don't paraphrase or simplify
4. Flag terms with no direct English equivalent
5. Note ambiguous passages

**Output per clause:**
- Original text
- Faithful translation
- Notes (translator observations)
- Model used

**Error handling:**
- Returns `{'error': msg}` on failure (no exceptions)
- Checks for anthropic SDK installation
- Checks for ANTHROPIC_API_KEY env var
- Individual clause failures don't stop batch translation

### Formatter (219 lines)

Split-screen paired output for video production:

**Markdown format:**
```
## Article 1: [heading]

### Original
> [original text, blockquoted for left panel]

### Translation
[English translation for right panel]

---
**Notes:**
1. [footnote about legal terms]
```

**Also supports:**
- JSON output for machine consumption
- Summary headers with metadata
- Split-screen helper (separate left/right extracts)

**Design rationale:**
- Blockquoted originals visually separate from translation
- Self-contained sections ready for split-screen display
- Footnotes preserve scholarly depth without cluttering reading flow

### CLI (291 lines)

Comprehensive command-line interface:

**Subcommand: `detect`**
Preview document structure before translating:
```bash
python tools/translation/cli.py detect --file document.txt
python tools/translation/cli.py detect "Article 1\nText"
cat document.txt | python tools/translation/cli.py detect -
```

Output: detected type, section count, section list with IDs and previews

**Subcommand: `translate`**
Full translation pipeline:
```bash
python tools/translation/cli.py translate --file doc.txt --language french
python tools/translation/cli.py translate "text" --language spanish --context "1940 statute"
cat doc.txt | python tools/translation/cli.py translate - --language french --output out.md
```

Flags:
- `--language LANG` (required): source language
- `--type TYPE`: override auto-detection
- `--context "desc"`: document context for better translation
- `--output PATH`: write to file (default stdout)
- `--format FORMAT`: markdown (default) or json
- `--dry-run`: show plan without API calls

**Dry-run output:**
- Detected type
- Section count
- Estimated API calls
- Section list with character counts
- Prompt to remove flag when ready

**Input modes:**
1. `--file PATH`: read from file
2. `-` (stdin): pipe from other commands
3. Direct text argument

**Progress display:**
Prints to stderr: "Translating clause 3/10... (article-3)"

**Placeholder subcommands:**
- `crosscheck`: "Will be available after Plan 40-02"
- `annotate`: "Will be available after Plan 40-02"
- `surprise`: "Will be available after Plan 40-03"

## Deviations from Plan

None. Plan executed exactly as written.

## Implementation Highlights

### 1. Full Document Context Per Clause

**Design decision:** Send full document with each API call, highlighting active clause.

**Why:** Legal/historical terms often depend on definitions or context from other clauses. A term in Article 5 might reference Article 2. Without full context, Claude might mistranslate based on modern usage instead of document-specific meaning.

**Trade-off:** More tokens per call, higher cost. Accepted because accuracy > cost for this use case.

### 2. Auto-Detection with Dry-Run Confirmation

**Design decision:** Auto-detect structure, but require user to review via `--dry-run` before translating.

**Why:** User sees what will be translated and how many API calls before committing. Prevents surprises like "I thought it was 5 articles but it detected 50 paragraphs."

**Flow:**
1. Run with `--dry-run` first
2. See detected structure
3. Remove flag when satisfied
4. Proceed with translation

### 3. Error Dict Pattern Throughout

**Design decision:** All functions return `{'error': msg}` on failure, never raise exceptions.

**Why:** Consistent with project codebase (memory note: error dict pattern, never raise). CLI can handle errors gracefully without try/except blocks everywhere.

**Applied to:**
- Translator initialization (missing SDK, missing API key)
- Input validation (empty text, file not found)
- API calls (network errors, rate limits)
- Structure detection (no sections found)

### 4. Optional Phase 39 Integration

**Design decision:** Try to import Phase 39 structure assessor for timing estimates, but don't require it.

**Implementation:**
```python
try:
    from structure_assessor import StructureAssessor
    timing_estimates = assessor.TIMING_ESTIMATES.get(detected_type)
except (ImportError, Exception):
    # Phase 39 not available - continue without timing
    pass
```

**Why:** Translation pipeline works standalone, but enhances with Phase 39 if available. Users who only need translation don't need to install document_discovery tools.

### 5. Paragraph Fallback for Unstructured Documents

**Design decision:** If no article markers detected, split on double newlines (paragraph boundaries).

**Why:** Some documents (letters, unstructured decrees) don't have numbered articles but still need clause-by-clause translation. Better than failing with "no structure detected."

**Example:** Diplomatic correspondence, proclamations, letters.

## Testing Results

**All verification checks passed:**

1. ✅ All modules importable
2. ✅ Structure detector parses French articles (Article 1, Article 2)
3. ✅ Structure detector parses Spanish articles (Artículo 1, Artículo 2)
4. ✅ Structure detector parses German articles (Artikel 1, § 2)
5. ✅ Formatter produces paired markdown with blockquoted originals
6. ✅ Formatter includes footnotes when provided
7. ✅ CLI handles empty input gracefully (error message)
8. ✅ CLI shows all translate flags in --help
9. ✅ CLI detect subcommand outputs structure
10. ✅ CLI translate --dry-run shows plan without API calls
11. ✅ Error dict pattern used (no raised exceptions)

## File Structure

```
tools/translation/
├── __init__.py              # Package init (14 lines)
├── structure_detector.py    # Article boundary detection (297 lines)
├── formatter.py             # Split-screen output (219 lines)
├── translator.py            # Claude translation engine (301 lines)
└── cli.py                   # Command-line interface (291 lines)
```

**Total:** 1,122 lines across 5 files

## Integration Points

**From Phase 39:**
- Optional import of `structure_assessor.TIMING_ESTIMATES` for video length estimates
- Same document type taxonomy (legal_code, treaty, decree, book, letter, other)

**To Plan 40-02 (Cross-check & Annotation):**
- Translator output format expected by crosscheck module
- Section structure expected by annotate module
- CLI placeholder subcommands ready to implement

**To Plan 40-03 (Surprise Detection):**
- Translated sections with original/translation pairs
- Section IDs for referencing specific clauses

**To Phase 41 (Production Integration):**
- Split-screen formatted markdown ready for `/prep --edit-guide`
- Paired original/translation suitable for DaVinci Resolve overlay
- Footnotes ready for on-screen annotation

## Usage Examples

**Preview structure before translating:**
```bash
python tools/translation/cli.py detect --file "Statut-des-Juifs-1940.txt"
```

**Translate with context:**
```bash
python tools/translation/cli.py translate \
  --file "Statut-des-Juifs-1940.txt" \
  --language french \
  --context "1940 French law defining Jewish status under Vichy regime" \
  --output "translation-output.md"
```

**Dry-run to see plan:**
```bash
python tools/translation/cli.py translate \
  --file document.txt \
  --language spanish \
  --dry-run
```

**From stdin (pipeline integration):**
```bash
curl https://archive.org/download/treaty.txt | \
  python tools/translation/cli.py translate - --language latin --output treaty-en.md
```

**JSON output for machine consumption:**
```bash
python tools/translation/cli.py translate \
  --file doc.txt \
  --language german \
  --format json > translation.json
```

## Next Steps (Plan 40-02)

**Cross-check translation:**
- Compare Claude translation against DeepL and Google Translate
- Flag semantic differences (not stylistic)
- Generate discrepancy report

**Legal term annotation:**
- Identify terms with no direct English equivalent
- Look up historical definitions
- Flag common mistranslations
- Generate footnotes

**CLI integration:**
- Implement `crosscheck` subcommand
- Implement `annotate` subcommand
- Enhance `translate` to auto-run crosscheck if API keys available

## Self-Check: PASSED

**Files exist:**
```bash
[ -f "tools/translation/__init__.py" ] && echo "FOUND"
[ -f "tools/translation/structure_detector.py" ] && echo "FOUND"
[ -f "tools/translation/formatter.py" ] && echo "FOUND"
[ -f "tools/translation/translator.py" ] && echo "FOUND"
[ -f "tools/translation/cli.py" ] && echo "FOUND"
```
✅ All files exist

**Commits exist:**
```bash
git log --oneline --all | grep "c8703b3" && echo "FOUND: c8703b3"
git log --oneline --all | grep "3696ae4" && echo "FOUND: 3696ae4"
```
✅ Both commits present:
- c8703b3: feat(40-01): add structure detector and formatter modules
- 3696ae4: feat(40-01): add Claude translator engine and CLI

**Functionality verified:**
```bash
python -c "import sys; sys.path.insert(0, 'tools/translation'); from structure_detector import StructureDetector; from translator import Translator; from formatter import Formatter; print('All imports OK')"
```
✅ All modules importable

**CLI functional:**
```bash
python tools/translation/cli.py detect --help
python tools/translation/cli.py translate --help
```
✅ Both subcommands operational

---

**Plan 40-01 complete.** Core translation engine ready for cross-checking (Plan 40-02) and surprise detection (Plan 40-03).
