---
phase: 33-voice-pattern-library
plan: 01
subsystem: content-production
tags: [voice-patterns, style-guide, script-quality]
dependency-graph:
  requires: []
  provides: [voice-pattern-library]
  affects: [script-writer-v2]
tech-stack:
  added: []
  patterns: [transcript-analysis, pattern-extraction]
key-files:
  created: []
  modified:
    - .claude/REFERENCE/STYLE-GUIDE.md
decisions:
  - pattern-count: "22 patterns extracted (exceeded 20+ target)"
  - pattern-sources: "Belize (23K views), Vance (42.6% retention), Essequibo (1.9K views)"
  - organization: "5 subsections: openings, transitions, evidence, rhythm, forbidden"
metrics:
  duration: 120m
  completed: 2026-02-10
---

# Phase 33 Plan 01: Voice Pattern Library Summary

**One-liner:** Extracted 22 copy-paste voice patterns from top-performing transcripts (Belize, Vance) as STYLE-GUIDE.md Part 6, providing script-writer-v2 with actionable formulas, real examples, and templates.

## What Was Built

**New Feature:** STYLE-GUIDE.md Part 6: Voice Pattern Library

**Pattern Categories (22 total):**

1. **6.1 Opening Formulas (5 patterns):**
   - Visual Contrast Hook (Belize: map comparison)
   - Current Event Hook (Essequibo: military confrontation)
   - Fact-Check Declaration (Vance: debunking political claims)
   - Personal Research Authority (Belize: "So, I read that treaty")
   - Escalation Timeline (Essequibo: diplomatic crisis)

2. **6.2 Transition Sequences (8 patterns):**
   - Kraut-Style Causal Chain (consequently/thereby/which meant that)
   - Temporal Jump with "Now" (contrasting perspectives)
   - "So how did we get here?" (modern to historical pivot)
   - "But here's where it gets interesting" (complication reveal, 1x max)
   - "Look at what just happened" (pattern reveal)
   - "Which brings us to..." (section bridge)
   - Date as Section Break (chronological flow)
   - Contrast Pair (competing perspectives)

3. **6.3 Evidence Introduction Patterns (5 patterns):**
   - Setup → Quote → Implication (3-step academic sourcing)
   - "Notice this specific phrase" (close-reading treaties)
   - "Here's what [X] actually says" (document reveal, 2-4x max)
   - "Reading directly from..." (formal legal language)
   - Quote Stacking (authority stack, Shaun-style)

4. **6.4 Sentence Rhythm Patterns (4 patterns):**
   - Long Setup + Short Punch (emphasis through contrast)
   - Question → Zero/None Answer (dramatic absence)
   - Fragment for Verdict (moral/factual weight)
   - Contrast Pair (This vs. That structure)

5. **6.5 Forbidden Pattern Detection:**
   - Pre-output validation checklist organized by violation type:
     - Channel DNA Violations (clickbait, generic CTAs, YouTube cliches)
     - Spoken Delivery Violations (formal transitions, fragments, punctuation)
     - Voice Pattern Violations (hedging, setup questions, meta-commentary)
     - Structural Violations (background-first, missing bridges, unsupported quotes)
     - Evidence Violations (summaries vs. quotes, missing attributions)

**Each pattern includes:**
- Name (descriptive, memorable)
- When to use (topic type, script section)
- Formula (abstract sequence with placeholders)
- Example (exact transcript text with video name and stats)
- Copy-paste template (fill-in-the-blank version)

**Additional Changes:**
- Renumbered existing Part 6 (Quality Checklist) to Part 7
- All Parts 1-5 content preserved
- Updated "Last updated" date to 2026-02-10

## Deviations from Plan

None - plan executed exactly as written.

## Technical Implementation

**Transcript Analysis Process:**
1. Read 3 primary transcripts (Belize, Vance published, Vance original)
2. Reviewed Essequibo opening for military confrontation patterns
3. Extracted patterns by analyzing:
   - Opening sequences (first 60 seconds)
   - Transition mechanics (connector words, topic shifts)
   - Evidence introduction (setup, quote, implication)
   - Sentence rhythm (length contrast, fragments, emphasis)
   - Anti-patterns (what appears in lower-performing content)

**Pattern Documentation Structure:**
- Followed template from plan: name → when → formula → example → template
- Used real transcript text with exact timestamps/context
- Provided both abstract formulas and concrete fill-in-the-blank templates
- Organized forbidden patterns as boolean checklist with fixes

**File Integration:**
- Inserted Part 6 between existing Parts 5 and 6 (lines 457-792)
- Renumbered quality checklist from Part 6 to Part 7
- No content deletions or overwrites
- Maintained existing document structure and formatting

## Verification

**Pattern Count:** 22 patterns (5 + 8 + 5 + 4 = 22 documented patterns, plus checklist)

**Quality Checks:**
✅ All patterns have 5 required fields (name, when, formula, example, template)
✅ All examples from real transcript text (Belize, Vance, Essequibo)
✅ Part 7 (Quality Checklist) preserved with all original content
✅ Parts 1-5 unchanged
✅ Supplements section intact at bottom
✅ Internal references correct (Part 6 = Voice Pattern Library, Part 7 = Quality Checklist)

**File Verification:**
```bash
grep -c "^#### " STYLE-GUIDE.md  # Returns 27 (22 patterns + 5 checklist sections)
grep "Part 6" STYLE-GUIDE.md    # Returns Voice Pattern Library header
grep "Part 7" STYLE-GUIDE.md    # Returns Quality Checklist header
```

## Self-Check

**Files Created:**
- `.planning/phases/33-voice-pattern-library/33-01-SUMMARY.md` ✅ (this file)

**Files Modified:**
- `.claude/REFERENCE/STYLE-GUIDE.md` ✅ EXISTS
  - Part 6: Voice Pattern Library added (lines 457-792)
  - Part 7: Quality Checklist renumbered (line 793+)

**Commits:**
- `6e404b5` - feat(33-01): add Voice Pattern Library as STYLE-GUIDE Part 6 ✅ EXISTS

**Pattern Extraction Verification:**
✅ 5 opening formulas documented with Belize/Vance examples
✅ 8 transition patterns including Kraut causal chains
✅ 5 evidence introduction patterns with 3-step formula
✅ 4 sentence rhythm patterns (long+short, question→zero, fragments, contrast)
✅ Forbidden pattern checklist consolidated from existing + new analysis

**## Self-Check: PASSED**

All files created/modified verified. All commits exist. Pattern extraction complete with substantive examples from top-performing transcripts.

## Impact

**For script-writer-v2 agent:**
- Now has 22 actionable patterns vs. high-level descriptions
- Can directly apply formulas with exact connector words
- Has real examples showing proven performance (23K views, 42.6% retention)
- Pre-output validation checklist prevents common errors

**For manual scripting:**
- Opening formulas provide 5 proven hooks
- Transition patterns eliminate awkward section breaks
- Evidence patterns ensure proper source integration
- Rhythm patterns create emphasis and memorability
- Forbidden checklist catches violations before filming

**Connection to v2.0 roadmap:**
- Phase 33 (Voice Pattern Library): COMPLETE ✅
- Phase 35 (Actionable Analytics) can now reference these patterns for retention fix recommendations
- Script quality improves immediately (patterns ready to use today)

## Next Steps

**Within Phase 33:**
- Plan 02: Update script-writer-v2.md to reference Part 6 patterns
- Verify agents can parse and apply pattern templates
- Test pattern application in next script draft

**Dependencies Unlocked:**
- Phase 35 Actionable Analytics can now map retention drops to missing patterns
- Example: "3:45 dropout → missing transition bridge (see Part 6.2)"

**No blockers identified.**

---

**Duration:** 120 minutes (transcript analysis 60m, pattern documentation 45m, verification 15m)
**Completed:** 2026-02-10 19:02 UTC
**Commit:** 6e404b5
