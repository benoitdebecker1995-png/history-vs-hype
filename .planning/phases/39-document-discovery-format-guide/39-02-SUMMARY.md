---
phase: 39-document-discovery-format-guide
plan: 02
subsystem: documentation
tags: [format-guide, untranslated-evidence, series-standards, document-videos]
dependency_graph:
  requires: [SCPT-03]
  provides: [format-reference]
  affects: [script-writer-v2, verify-command, prep-command]
tech_stack:
  added: []
  patterns: [episode-structure-template, split-screen-visual-approach, translation-cross-check-protocol]
key_files:
  created:
    - .claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md
  modified: []
decisions:
  - "Split-screen as core visual approach without locking exact layout (left/right vs top/bottom TBD in production)"
  - "Video length: as long as needed for completeness (no arbitrary caps)"
  - "Three episode types: full-document, excerpt-based, related-document-bundles"
  - "Qualification criteria: no full English translation OR misleading existing translations"
  - "Translation protocol: Claude primary + DeepL/Google cross-check"
  - "Tone: same 'Calm Prosecutor' voice as main channel, not gotcha journalism"
  - "Format guide without branding commitment (sub-series vs category TBD)"
  - "Filming technique details deferred to production phase"
metrics:
  duration: "234 seconds (3.9 minutes)"
  completed: "2026-02-17"
  tasks_completed: 1
  commits: 1
  files_created: 1
---

# Phase 39 Plan 02: Format Reference Guide Summary

**One-liner:** Comprehensive 712-line format guide establishing episode structure, split-screen visual approach, translation cross-check protocol, and "Calm Prosecutor" tone for document-based videos without committing to branding or production techniques.

---

## What Was Built

Created `.claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md` - a complete format reference for the Untranslated Evidence series (or category - branding TBD).

**File already existed** from a previous session with all requirements met. Verified completeness and committed to repository.

---

## Four Major Sections

### Section 1: Episode Structure Template (5-part flow)

1. **Cold Open / Hook (1-2 min):** Modern consequence or myth that untranslated document contradicts
2. **Document Introduction (2-3 min):** What/when/where/who, show archival scan for authenticity
3. **Clause-by-Clause Walkthrough (bulk):** Context → original → translation → significance → myth connection
4. **Synthesis / "What They Got Wrong" (3-5 min):** Aggregate distortions, steelman common narrative
5. **Modern Relevance Close (1-2 min):** Who cites document today, why accurate translation matters

**Episode types defined:**
- **Option A:** Full-document coverage (5-15 articles, ~20-35 min)
- **Option B:** Excerpt-based (select 5-8 key clauses, ~15-25 min)
- **Option C:** Related document bundles (decree + regulations, ~30-50+ min)

**Example included:** Statut des Juifs (October 3, 1940) walkthrough with 25-minute estimate.

---

### Section 2: Visual / Staging Standards

**Core visual approach:** Split-screen with original-language text on one side, English translation on the other.

**Layout intentionally unspecified:** Left/right, top/bottom, proportions - TBD during production. Guide establishes the CONCEPT (parallel display), not locked specifications.

**Key principles:**
- Text must be readable on mobile (font size, contrast)
- Original language shown as-is (never modernized)
- Active clause visually distinguished (highlight, zoom, isolation)
- Archival scan shown at least once per video (authenticity marker)

**Display ratio:** ~50-60% document display, ~40-50% talking head (heavier document usage than standard channel videos at ~30-40% B-roll).

**Filming technique details deferred** - guide establishes WHAT to show, not HOW to film it.

---

### Section 3: Quality Bar & Source Rules

**Source hierarchy:**
1. **Tier 1:** Academic critical editions (Brill, Cambridge, Oxford) with scholarly apparatus
2. **Tier 2:** Official archives (Légifrance, UK National Archives, etc.)
3. **Tier 3:** Wikisource (cross-reference with archival scan to verify)

**Translation protocol:**
- **Primary:** Claude AI translation
- **Cross-check:** At least one independent source (DeepL, Google Translate, second AI model)
- **Legal/technical terms:** Annotated with historical dictionary definitions
- **Disagreements:** Present as discovery, not error ("DeepL says X, but literal is Y - here's why...")

**Qualification criteria for series:**
- **(A)** No full English translation exists, OR
- **(B)** Existing translations are misleading/distorted

**Surprise clause detection:** Flag provisions where translation contradicts common English-language narratives - these are highlight moments.

**Citation standard:** Every clause references article/section number and page number from critical edition.

---

### Section 4: Tone & Framing Rules

**Voice:** Same "Calm Prosecutor" as main channel (reference STYLE-GUIDE.md 6 times).

**Framing:** "Let's read what it actually says" - NOT "they lied to you."

**Key rules:**
- Acknowledge translation difficulty openly (intellectual honesty, not weakness)
- Steelman common narrative before correcting it (Alex O'Connor style)
- No political editorializing about document morality (document speaks for itself)
- Respect original language (correct pronunciation, explain etymologies)
- Translation disagreements framed as discovery, not error

**Approved phrases:**
- "If we look at the specific language..."
- "The original is more precise..."
- "Article X contradicts the common claim that..."

**Forbidden phrases:**
- "The smoking gun," "Hidden clause," "What they don't want you to know" (conspiracy framing)

---

## Deviations from Plan

**None.** File was created in a previous session and met all requirements on verification:

- ✓ All four sections present
- ✓ Split-screen mentioned without locked layout
- ✓ References STYLE-GUIDE.md for base voice (6 references)
- ✓ Example video outline included (Statut des Juifs)
- ✓ "As long as needed" video length philosophy
- ✓ Both full-document and excerpt-based types covered
- ✓ Qualification criteria defined
- ✓ No locked branding decisions
- ✓ Filming technique details deferred
- ✓ 712 lines (minimum 150 required)

Task executed exactly as specified.

---

## Key Decisions

**1. Split-screen as approach, not specification**
- Establishes parallel display concept
- Layout details (left/right, top/bottom, proportions) TBD in production
- Allows flexibility for production testing

**2. Video length: completeness over brevity**
- No arbitrary time caps
- 10-article statute = ~25 min
- Complex treaty = 45+ min if needed
- Quality and thoroughness drive length

**3. Three episode types**
- Full-document: every clause (short documents)
- Excerpt-based: 5-8 key clauses (long documents)
- Related bundles: decree + regulations (connected stories)

**4. Qualification criteria clarified**
- Not just "no translation exists"
- Also includes misleading/distorted existing translations
- Partial translations don't disqualify

**5. Translation cross-check protocol**
- Primary: Claude AI
- Verification: DeepL, Google Translate, or second AI
- Legal terms get historical dictionary annotation
- Disagreements presented as discovery opportunity

**6. Tone: same channel voice**
- "Calm Prosecutor" maintained
- Not gotcha journalism or conspiracy framing
- Intellectual honesty (acknowledge uncertainty)
- Steelman before correcting

**7. Format guide, not series bible**
- No branding commitment (sub-series vs category TBD)
- Establishes structure regardless of branding decision
- Allows production flexibility

**8. Filming technique deferred**
- Guide establishes WHAT to show (split-screen, highlights, archival scans)
- HOW to achieve it (camera setup, overlays, etc.) decided in production
- Prevents over-specification before testing

---

## Files Created

### `.claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md` (712 lines)

**Contents:**
- **Section 1:** Episode structure template with 5-part flow
- **Section 2:** Visual/staging standards (split-screen, readability, authenticity)
- **Section 3:** Quality bar & source rules (hierarchy, translation protocol, citation standards)
- **Section 4:** Tone & framing rules (voice, intellectual honesty, forbidden/approved phrases)
- **Example:** Statut des Juifs outline (~25 min video estimate)
- **Checklist:** Pre-production, translation, script, visual prep, quality gate (5 sections, 30 items)

**Key features:**
- References STYLE-GUIDE.md 6 times for base channel voice
- Covers both full-document and excerpt-based episodes
- Defines qualification criteria (no translation OR misleading translations)
- Maintains "as long as needed" video length philosophy
- No locked branding or production technique decisions

**Integration points:**
- script-writer-v2 (Phase 41): Document mode implementation
- /verify command (Phase 41): Translation verification mode
- /prep command (Phase 41): Split-screen edit guides

---

## Integration Notes

**For Phase 40 (Translation Pipeline):**
- Translation cross-check protocol established (Claude + DeepL/Google)
- Legal term annotation requirements defined
- Surprise clause detection criteria specified

**For Phase 41 (Verification & Production Integration):**
- Episode structure template ready for script-writer-v2 document mode
- Visual standards ready for EDITING-GUIDE-SHOT-BY-SHOT.md integration
- Translation verification standards ready for /verify --translation mode

**Deferred to production:**
- Split-screen layout specifics (left/right vs top/bottom, proportions)
- Filming technique (camera setup, overlays, green screen usage)
- Exact highlighting method (yellow highlight, zoom, isolation - choose during editing)

---

## Verification Results

**All task requirements met:**

1. ✓ File exists at `.claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md`
2. ✓ Four sections cover: episode structure, visual/staging, quality bar, tone/framing
3. ✓ Split-screen approach established without locked layout specifics
4. ✓ Example video outline demonstrates template with real document (Statut des Juifs)
5. ✓ No branding commitment (format guide, not series bible)
6. ✓ Standard channel quality rules referenced via STYLE-GUIDE.md (6 references)
7. ✓ 712 lines (exceeds 150-line minimum by 375%)
8. ✓ Both full-document and excerpt-based episode types covered
9. ✓ Qualification criteria clearly defined
10. ✓ Filming technique details deferred as planned

**Success criteria achieved:**

- ✓ Format reference guide comprehensive enough for script-writer-v2 integration
- ✓ Episode structure template concrete enough for document-based script generation
- ✓ Visual standards establish split-screen without over-specifying production details
- ✓ Quality bar specific about source selection, translation accuracy, citation standards
- ✓ Tone rules maintain channel voice while adding document-specific guidance

---

## Self-Check: PASSED

**File existence check:**
```bash
$ ls -la "G:\History vs Hype\.claude\REFERENCE\UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md"
-rw-r--r-- 1 benoi 197609 32252 Feb 16 19:07 UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md
```
✓ File exists (32,252 bytes, 712 lines)

**Commit verification:**
```bash
$ git log --oneline -1
f664262 docs(39-02): create Untranslated Evidence format reference guide
```
✓ Commit f664262 exists in repository

**Content verification:**
- ✓ Section 1 present (Episode Structure Template)
- ✓ Section 2 present (Visual / Staging Standards)
- ✓ Section 3 present (Quality Bar & Source Rules)
- ✓ Section 4 present (Tone & Framing Rules)
- ✓ Example video outline included (Statut des Juifs, lines 537-635)
- ✓ References STYLE-GUIDE.md (6 occurrences)
- ✓ Split-screen mentioned with layout unspecified (lines 148-156)
- ✓ Video length philosophy: "as long as needed" (lines 132-142)
- ✓ No branding commitment (lines 11-16)

All claims verified. Ready to proceed to state updates.

---

## Commits

| Commit | Message | Files |
|--------|---------|-------|
| f664262 | docs(39-02): create Untranslated Evidence format reference guide | .claude/REFERENCE/UNTRANSLATED-EVIDENCE-FORMAT-GUIDE.md |

---

## Duration

**Total time:** 234 seconds (3.9 minutes)
- Task 1 (Write format guide): File already existed, verification and commit only

**Efficiency note:** Pre-existing file from previous session allowed rapid completion. All requirements were already met.

---

## Next Steps

**Phase 39 Plan 02 complete.** File committed to repository.

**For Phase 40 (Translation Pipeline):**
- Implement Claude + DeepL cross-check protocol (Section 3)
- Build legal term annotation system (Section 3)
- Create surprise clause detection workflow (Section 3)
- Develop split-screen formatting output (Section 2)

**For Phase 41 (Verification & Production Integration):**
- Integrate episode structure template into script-writer-v2 (Section 1)
- Add document mode to /script command
- Add translation verification to /verify command (Section 3 protocol)
- Generate split-screen edit guides in /prep command (Section 2 standards)

---

*Summary completed: 2026-02-17*
*Plan execution: 1 task, 1 commit, 234 seconds*
*Status: All requirements met, ready for Phase 40 planning*
