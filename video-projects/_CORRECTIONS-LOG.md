# Corrections Log - History vs Hype

**Purpose:** Document errors discovered pre/post-publication to prevent repeats
**Last Updated:** 2025-12-04

---

## Pre-Publication Errors (Caught Before Upload)

### Bir Tawil - Claimant Dates Error
**Video:** 6-bir-tawil-2025
**Date Discovered:** 2025-12-04
**Stage:** Post-filming, pre-edit

**Error:**
Script said: "A Russian radio operator declared it the Kingdom of Middle Earth in 2014"
Reality: Dmitry Zhikharev (Russian DJ) declared it in November 2017

**Root Cause:**
- Script v4.1 claimed facts were "verified via Tier 4-5 sources"
- Verification was sloppy - sources were skimmed, not cross-checked
- Zhikharev *visited* in 2014 but *declared* kingdom in 2017 - this distinction was missed
- "Radio operator" was wrong - he's a DJ

**Fix Applied:**
- Re-record "2017" to punch over "2014" in audio
- "Radio operator" vs "DJ" left as minor error

**Lesson:**
- VERBATIM rule exists for a reason - don't paraphrase from memory
- Dates require exact source quotes, not interpretation
- "Visited" vs "declared" are different actions with different dates

---

### Bir Tawil - Hala'ib Size Error
**Video:** 6-bir-tawil-2025
**Date Discovered:** 2025-12-04
**Stage:** Post-filming, pre-edit

**Error:**
Audio says: "800,000 square miles"
Reality: 8,000 square miles

**Root Cause:**
- Likely misread or verbal slip during filming
- Not caught in filming review

**Fix Applied:**
- Text overlay showing "8,000 sq mi" on screen
- Visual overrides audio error

---

## Post-Publication Errors

*None yet*

---

## Error Prevention Checklist

Before filming, verify:
- [ ] All dates copied VERBATIM from sources
- [ ] All names spelled out with source
- [ ] All numbers double-checked against original
- [ ] Read script aloud checking for verbal traps (800 vs 800,000)
- [ ] Temporal distinctions preserved ("visited in X" vs "declared in Y")
- [ ] Occupations/titles exact from source (not paraphrased)

---

## Process Improvements Made

### 2025-12-04: Added RULE 4 to script-writer-v2.md

**File:** `.claude/agents/script-writer-v2.md`

**New rule:** HIGH-RISK DETAILS REQUIRE EXACT QUOTES

Dates, names, occupations, and temporal distinctions must be:
1. Copied verbatim from source (not typed from memory)
2. Include context ("visited" vs "declared" vs "claimed")
3. Verified before claiming "verified"

**Added to PRE-OUTPUT CHECKLIST:**
- Every year copied exactly from source?
- Every occupation/title exact?
- Temporal distinctions preserved?
- Name spellings copy-pasted?

**Triggered by:** Bir Tawil claimant dates error (2014 vs 2017, radio operator vs DJ)
