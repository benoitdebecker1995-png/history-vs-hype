---
phase: 41-verification-production-integration
plan: 03
subsystem: production-integration
tags: [split-screen, edit-guide, timing, transitions, assets, surprises]
requirements_completed: [PROD-01, PROD-02, PROD-03]
tech_stack_added: []
patterns_added:
  - Per-clause timing estimation (150 WPM + pause times)
  - Hybrid transition markers (explicit + ratio guidance)
  - Auto-asset sourcing from Phase 39 archive lookup
  - Surprise clause emphasis flagging (MAJOR/NOTABLE only)
key_files:
  created:
    - tools/production/split_screen_guide.py
  modified:
    - .claude/commands/prep.md
decisions:
  - "Per-clause timing uses 150 WPM with 2.5-second pauses for read/translate"
  - "Hybrid transition approach: explicit markers for key switches + ratio guidance per section"
  - "Auto-asset sourcing from archive lookup with manual placeholders for context visuals"
  - "Surprise markers only for MAJOR/NOTABLE severity (MINOR left to editor judgment)"
  - "Section grouping: 5 clauses per section for manageable timing blocks"
duration_minutes: 3.4
completed_date: 2026-02-18
---

# Phase 41 Plan 03: Split-Screen Edit Guide Integration Summary

**One-liner:** Split-screen edit guide generation for document walkthrough videos with clause-level timing, transition markers, asset sourcing, and surprise emphasis.

## What Was Built

### Core Module: split_screen_guide.py (742 lines)

**SplitScreenGuide class** generates editor-ready guides for document walkthrough videos:

1. **Per-clause timing breakdown:**
   - Context setup (talking head): word count / 150 WPM
   - Read original (split-screen): word count / 150 WPM + 2.5 sec pause
   - Translate (split-screen): word count / 150 WPM + 2.5 sec pause
   - Explain significance (talking head): estimated from script
   - Connect to myth (talking head): estimated from script

2. **Section-level aggregation:**
   - Groups clauses into sections (5 clauses each)
   - Calculates section totals with cumulative running times
   - Computes visual ratios (talking head % vs split-screen %)

3. **Hybrid transition markers:**
   - Explicit timestamped switches at key moments (talking head ↔ split-screen)
   - Ratio guidance per section for overall pacing

4. **Asset sourcing:**
   - Auto-generates URLs from Phase 39 archive lookup (if available)
   - Creates manual placeholders for context visuals (maps, photos, timelines)

5. **Surprise emphasis:**
   - Flags MAJOR surprises with concrete editor suggestions (slow zoom, highlight box)
   - Flags NOTABLE surprises with lighter emphasis notes
   - Omits MINOR surprises to avoid noise

**Input:**
- Translation output file (formatted from Phase 40)
- Script file (optional, for precise word counts)
- Archive lookup results (optional, for document URLs)

**Output:**
- SPLIT-SCREEN-EDIT-GUIDE.md with 7 sections:
  1. Overview (duration, format, counts)
  2. Section-by-section breakdown (timing, visual staging, transitions)
  3. Surprise markers (editor emphasis notes)
  4. Asset checklist (auto-sourced + manual needed)
  5. Pacing notes (opening, middle, synthesis)
  6. Synthesis section (recap structure)
  7. Conclusion (closing guidance)

### /prep Integration: --split-screen Mode

**Added to .claude/commands/prep.md:**

1. **Flag documentation:**
   - Usage: `/prep --split-screen [project]`
   - Purpose: Split-screen edit guide for document videos

2. **Comprehensive section (157 lines):**
   - When to use: Untranslated Evidence format videos
   - Prerequisites: translation output + script + verified translation
   - Process steps: locate files → parse structure → timing → transitions → assets → surprises
   - Output format: SPLIT-SCREEN-EDIT-GUIDE.md structure
   - Example usage with auto-detect and explicit file paths
   - Workflow integration with Phase 40 translation pipeline

3. **Reference links:**
   - `.claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md`
   - `tools/translation/cli.py`
   - `tools/production/split_screen_guide.py`

## Deviations from Plan

None - plan executed exactly as written.

## Technical Decisions

### 1. Timing Estimation Approach

**Decision:** 150 WPM fixed rate with 2.5-second pauses after read/translate.

**Rationale:**
- Matches channel's existing retention mapping rate
- Pause times allow visual processing (viewers need time to read on-screen text)
- Script word counts provide better estimates than translation-only fallback

### 2. Transition Marker Strategy

**Decision:** Hybrid approach with explicit markers + ratio guidance.

**Rationale:**
- Explicit markers for key moments (context → split-screen → talking head)
- Ratio guidance prevents marker overload while maintaining pacing awareness
- Editor has both tactical (specific timestamps) and strategic (section ratios) info

### 3. Asset Sourcing Pattern

**Decision:** Auto-generate from archive lookup with manual placeholders.

**Rationale:**
- Phase 39 archive lookup provides document URLs when available
- Manual placeholders ensure editor knows what context visuals are needed
- Auto-sourcing reduces prep time for documents with known archives

### 4. Surprise Emphasis Scope

**Decision:** Flag MAJOR/NOTABLE only, omit MINOR.

**Rationale:**
- MAJOR = must highlight (contradicts narrative)
- NOTABLE = worth highlighting (adds nuance)
- MINOR = editor judgment (legal terms, less significant surprises)
- Prevents noise while ensuring key moments are emphasized

### 5. Section Grouping Size

**Decision:** 5 clauses per section.

**Rationale:**
- Manageable timing blocks for filming sessions
- Aligns with natural document structure (articles often grouped in 5s)
- Cumulative times allow "stop after Article 5 for 10-minute session" planning

## Integration Points

### Phase 39 → Phase 41
- Archive lookup results used for auto-asset sourcing
- Document URLs from digitized archives included in asset checklist

### Phase 40 → Phase 41
- Translation formatter output parsed for clause structure
- Surprise markers (MAJOR/NOTABLE/MINOR) detected and filtered
- Legal term annotations could inform asset needs (future enhancement)

### /prep Command Flow
```
/prep --split-screen [project]
  ↓
Auto-detect translation file (*-TRANSLATION-FORMATTED.md)
  ↓
Read SCRIPT.md for word counts
  ↓
Check archive lookup for document URLs
  ↓
Generate SPLIT-SCREEN-EDIT-GUIDE.md
  ↓
Display asset counts and duration
```

## Files Created

### tools/production/split_screen_guide.py (742 lines)
- SplitScreenGuide class
- Per-clause timing calculation
- Section aggregation and ratio computation
- Transition marker generation (explicit + ratio)
- Asset collection (auto + manual)
- Surprise extraction and flagging
- Guide markdown builder
- CLI interface

**Exports:**
- `SplitScreenGuide` class
- `generate_guide()` method

**CLI usage:**
```bash
python tools/production/split_screen_guide.py --translation PATH [--script PATH] [--output PATH]
```

## Files Modified

### .claude/commands/prep.md (+157 lines)
- Added `--split-screen` to usage examples
- Added flag to flags table
- Created "SPLIT-SCREEN EDIT GUIDE" section (157 lines)
- Documented prerequisites, process, output format
- Added example usage and workflow integration
- Referenced split_screen_guide.py module

## Requirements Completed

✅ **PROD-01:** User can generate split-screen edit guides with /prep --split-screen
- Command documented in .claude/commands/prep.md
- Auto-detects translation file from project folder
- Generates SPLIT-SCREEN-EDIT-GUIDE.md with 7 sections

✅ **PROD-02:** Edit guide shows dual-panel staging with per-clause timing
- Per-clause breakdown: context, read, translate, explain, connect
- Section-level totals with cumulative running times
- Visual ratio guidance (talking head % vs split-screen %)

✅ **PROD-03:** Asset sourcing auto-generates from Phase 39 archive lookup where possible
- Archive lookup results queried for document URLs
- Auto-sourced assets listed with direct URLs
- Manual placeholders for context visuals (maps, photos, timelines)

## Success Criteria Verification

- [x] User can run /prep --split-screen and generate edit guide
- [x] Guide includes per-clause timing (read + translate + explain at 150 WPM)
- [x] Section-level totals show cumulative running times for planning
- [x] Transition markers show explicit switch points + ratio guidance
- [x] Archive lookup auto-sources document URLs when available
- [x] Manual placeholders created for maps, photos, context visuals
- [x] MAJOR surprises flagged with concrete editor emphasis suggestions
- [x] NOTABLE surprises flagged with lighter emphasis notes
- [x] Output saved to SPLIT-SCREEN-EDIT-GUIDE.md in project folder

## Example Output Structure

```markdown
# SPLIT-SCREEN EDIT GUIDE: [Document Name]

**Estimated Runtime:** 25 min 30 sec

## SECTION 1: Articles 1-5 (8:30)
**Visual Ratio:** 40% talking head, 60% split-screen

### Article 1 (00:00 - 01:45)
**TIMING BREAKDOWN:**
- Context setup: 0:25 (35 words)
- Read original: 0:30 (45 words + 2.5 sec pause)
- Translate: 0:25 (35 words + 2.5 sec pause)
- Explain significance: 0:15 (25 words)
- Connect to myth: 0:10 (15 words)

**VISUAL STAGING:**
[00:00 - 00:25] TALKING HEAD
[00:25 - 00:55] SWITCH TO SPLIT-SCREEN (LEFT panel)
[00:55 - 01:20] REVEAL TRANSLATION (RIGHT panel)
[01:20 - 01:35] RETURN TO TALKING HEAD
[01:35 - 01:45] TALKING HEAD (continued)

## SURPRISE MARKERS
⚠️ MAJOR SURPRISE - Article 7 (12:45)
Suggestion: Slow zoom on key phrase, highlight box
```

## Performance Metrics

- **Duration:** 3.4 minutes (205 seconds)
- **Tasks completed:** 2/2 (100%)
- **Files created:** 1 (split_screen_guide.py)
- **Files modified:** 1 (prep.md)
- **Lines added:** 898 (741 module + 157 docs)
- **Commits:** 2
  - 7113f81: feat(41-03): create split-screen guide generator module
  - 144f9ae: feat(41-03): integrate /prep --split-screen mode

## Next Steps

**Immediate (Phase 41):**
- No remaining plans in Phase 41 - this completes the phase
- Update STATE.md to mark Phase 41 complete
- Update ROADMAP.md with plan progress

**Future enhancements (outside Phase 41 scope):**
- Legal term tooltips in asset suggestions (use Phase 40 legal annotations)
- B-roll clip timing for surprise moments (specific shot durations)
- Template-based asset creation (auto-generate Canva templates from clause text)
- Multi-document guides (compare two documents side-by-side)

## Lessons Learned

### What Worked Well
1. **Hybrid transition markers** - Combining explicit timestamps with ratio guidance provides both tactical and strategic editing info
2. **Section grouping** - 5-clause sections create natural filming/editing blocks
3. **Surprise filtering** - MAJOR/NOTABLE only prevents marker noise while ensuring key moments are flagged
4. **Auto-asset sourcing** - Phase 39 archive lookup integration reduces manual work

### What Could Be Better
1. **Script word count estimation** - Fallback estimates when script unavailable are rough (30/50/20% split)
2. **Asset placeholder specificity** - Generic "[NEEDED] - Map" could suggest specific map types based on document content
3. **Synthesis section timing** - Currently generic; could parse script for actual synthesis word counts

### Architectural Notes
- Error dict pattern maintained: `{'error': msg}` on failure
- Modular design: guide generation independent of /prep command
- Future-proof: archive_results parameter ready for Phase 39 integration
- CLI + library interface: can be used standalone or via /prep

---

**Phase 41 Plan 03 Status:** ✅ COMPLETE

**Requirements delivered:** PROD-01, PROD-02, PROD-03 (3/3)

**Integration status:** /prep --split-screen mode ready for production use

---

## Self-Check: PASSED

Verification completed:
- ✓ FOUND: tools/production/split_screen_guide.py
- ✓ FOUND: commit 7113f81 (split-screen guide generator module)
- ✓ FOUND: commit 144f9ae (/prep --split-screen integration)

All files and commits verified successfully.
