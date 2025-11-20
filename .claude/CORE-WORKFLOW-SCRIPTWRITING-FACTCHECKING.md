# Core Workflow: Scriptwriting + Fact-Checking
**Purpose:** Write accurate scripts faster with zero fact-check errors

---

## THE PROBLEM WE'RE SOLVING

**Old way:**
```
Research → Write script → Fact-check → Find errors → Rewrite
```

**Result:** Fuentes script had 2 errors, wasted 3 hours rewriting

**New way:**
```
Research + Verify simultaneously → Write from verified facts → No errors
```

**Result:** Script is pre-verified, ready to film immediately

---

## NEW WORKFLOW (3 Phases)

### PHASE 1: Research + Verification (Simultaneous)

**File:** `01-VERIFIED-RESEARCH.md` (single source of truth)

**As you research with NotebookLM, immediately verify each fact:**

```markdown
# VERIFIED RESEARCH - [Topic]

**Project:** [Name]
**Date Started:** [Date]
**Completion:** [X]% verified

---

## SECTION 1: [Topic Category - e.g., "Jerusalem Massacre"]

### ✅ CLAIM 1: Death Toll
**What opponent claims:** "Tens of thousands killed"
**What's actually true:** Modern estimate ~3,000
**Sources:**
1. Thomas Asbridge (Tier 2) - *The Crusades*, p. 98
2. Jonathan Riley-Smith (Tier 2) - *The Crusades: A History*, p. 45

**Primary Source Quote (EXACT):**
> "About ten thousand were beheaded. Not one of them was allowed to live. They did not spare the women and children."
> — Fulcher of Chartres, *Historia Hierosolymitana* (Krey translation, 1921)

**Context:** Medieval sources inflated (10K-70K). Modern scholarship: ~3,000.

**Script-Ready:** ✅ YES
**How to use in script:** Show Fulcher quote (medieval claim), then modern estimate (scholarly correction)

---

### ✅ CLAIM 2: Date of Event
**Fact:** July 15, 1099 (Friday)
**Sources:**
1. Multiple primary sources confirm (Fulcher, Raymond, Gesta)
2. Asbridge confirms date

**Script-Ready:** ✅ YES

---

### ⏳ CLAIM 3: Specific Building Attacked
**Status:** STILL RESEARCHING
**What I need:** Verify which specific buildings in Temple Mount
**Sources to check:** [List]
**Script-Ready:** ❌ NO - Don't use until verified

---

### ❌ CLAIM 4: Unverifiable Statistic
**What opponent claims:** "15,000 Muslims killed"
**Problem:** No credible source found
**Sources checked:** [List what you searched]
**Decision:** DON'T USE - unverifiable
**Script approach:** Use verified 3,000 figure instead

---

## VERIFICATION STATS
- Total claims identified: 25
- Verified (✅): 18
- Researching (⏳): 5
- Unverifiable (❌): 2
- **Ready to write script:** 72% (need 90%+ to start)

---

## QUOTES - WORD-FOR-WORD VERIFIED

### Quote 1: Fulcher of Chartres - Jerusalem Massacre
**Source:** *Historia Hierosolymitana*, Book I, Chapter XXVII
**Translation:** Krey (1921), cross-checked with Ryan (1969)
**Exact text:**
> "Within this Temple about ten thousand were beheaded. If you had been there, your feet would have been stained up to the ankles with the blood of the slain. What more shall I tell? Not one of them was allowed to live. They did not spare the women and children."

**Verified:** ✅ Word-for-word exact (both translations match)
**Script-Ready:** ✅ YES
**Usage:** Lines 56-58 of script

---

### Quote 2: Raymond d'Aguilers - Blood to Knees
**Source:** *Historia Francorum qui ceperunt Iherusalem*
**Translation:** Hill & Hill (1968)
**Exact text:**
> "In the Temple and porch of Solomon, men rode in blood up to their knees and bridle reins."

**Verified:** ✅ Word-for-word exact
**Script-Ready:** ✅ YES
**Usage:** Lines 110-111 of script

---

[Add all verified quotes here BEFORE writing script]

---

## ARCHIVAL REFERENCES - EXACT

### Reference 1: Höfle Telegram
**Archive:** UK National Archives, Kew
**Exact Reference:** HW 16/23 (NOT HW 16/32 - common error!)
**Date of document:** January 11, 1943
**Verified from:** UK National Archives catalogue + Witte & Tyas (2001)
**Script-Ready:** ✅ YES

---

## NUMBERS - VERIFIED

| Claim | Number | Sources | Verified | Use in Script |
|-------|--------|---------|----------|---------------|
| Jerusalem deaths | ~3,000 | Asbridge, Riley-Smith | ✅ | YES |
| Höfle total | 1,274,166 | HW 16/23 document | ✅ | YES |
| Fourth Crusade debt | 34,000 marks | Phillips (2004) | ✅ | YES |
| Jizya rate (poor) | 1 dinar/year | Abu Yusuf | ✅ | YES |
| Rhineland Jews killed | 3,000-5,000 | Chazan, Baron | ✅ | YES |

**All numbers cross-checked against primary sources.**

---

## READY TO WRITE SCRIPT?

**Checklist:**
- [ ] 90%+ of major claims verified
- [ ] All quotes exact word-for-word
- [ ] All archival references precise
- [ ] All numbers have 2+ sources
- [ ] No [TK] placeholders remaining
- [ ] Contested claims identified and labeled

**Status:** NOT READY / READY TO WRITE

**When ready → Proceed to Phase 2**
```

---

### PHASE 2: Script Writing (From Verified Facts Only)

**File:** `02-SCRIPT-DRAFT.md`

**Rule:** ONLY use facts from `01-VERIFIED-RESEARCH.md`

**If you need a fact that's not verified → STOP → Go verify it first**

**Script Template with Built-in Verification:**

```markdown
# Script Draft - [Topic]

**Based on:** 01-VERIFIED-RESEARCH.md
**All facts pre-verified:** YES/NO
**Retention optimized:** YES/NO

---

## HOOK (0:00-0:45) [~60 words]

[Modern relevance hook]
{Fact used: [Reference to verified claim in research doc]}

**Verification:** ✅ Line 15 of VERIFIED-RESEARCH.md

---

## MAIN CLAIM TO DEBUNK (0:45-1:00)

[Opponent's claim quoted exactly]
{Quote source: [Verified quote from research doc]}

**Verification:** ✅ Quote verified line 45 of VERIFIED-RESEARCH.md

---

## EVIDENCE SECTION 1 (2:00-4:00)

[PRIMARY SOURCE 1]
{Quote: [Exact quote from VERIFIED-RESEARCH.md]}
{Attribution: [Exact source reference]}

**Verification:** ✅ Quote #1 from VERIFIED-RESEARCH.md (Fulcher)

[STATISTIC]
{Number: [From verified numbers table]}

**Verification:** ✅ Death toll verified (line 89 of VERIFIED-RESEARCH.md)

---

[Continue for each section...]

---

## SELF-CHECK BEFORE CALLING "FINAL"

**Script Quality:**
- [ ] Hook in first 30 seconds
- [ ] Structure telegraph (tells viewers what's coming)
- [ ] Callback hooks every 90 seconds
- [ ] Read out loud - no awkward phrasing
- [ ] Runtime: 10-12 minutes

**Fact Verification:**
- [ ] Every fact references VERIFIED-RESEARCH.md
- [ ] No claims without verification
- [ ] All quotes exact word-for-word
- [ ] All numbers match verified table
- [ ] All archival refs match verified list

**If all ✅ → Proceed to Phase 3**
**If any ❌ → Fix before Phase 3**
```

---

### PHASE 3: Final Verification (Cross-Check)

**File:** `03-FACT-CHECK-VERIFICATION.md`

**This is a CROSS-CHECK, not new research:**

```markdown
# Final Fact-Check Verification

**Script:** 02-SCRIPT-DRAFT.md
**Verified Against:** 01-VERIFIED-RESEARCH.md
**Status:** IN PROGRESS / COMPLETE

---

## CROSS-CHECK PROCESS

For each claim in script:
1. Find it in VERIFIED-RESEARCH.md
2. Confirm exact match
3. Mark ✅

---

## SCRIPT LINE-BY-LINE CHECK

### Line 56: Fulcher Quote
**Script says:** "About ten thousand were beheaded. Not one of them was allowed to live."
**Research doc says:** (Quote #1, line 45) - EXACT MATCH ✅
**Status:** ✅ VERIFIED

### Line 113: Höfle Telegram Reference
**Script says:** "UK National Archives, reference HW 16/23"
**Research doc says:** (Reference #1, line 67) - HW 16/23 ✅
**Status:** ✅ VERIFIED (NOT HW 16/32)

### Line 125: Jerusalem Death Toll
**Script says:** "Modern historians estimate around 3,000"
**Research doc says:** (Numbers table, line 89) - ~3,000 (Asbridge, Riley-Smith) ✅
**Status:** ✅ VERIFIED

---

[Cross-check EVERY claim]

---

## VERIFICATION SUMMARY

**Total claims in script:** 42
**Cross-checked:** 42/42 (100%)
**Matches verified research:** 42/42 ✅
**Errors found:** 0

**Quotes verified word-for-word:** 8/8 ✅
**Numbers match sources:** 12/12 ✅
**Archival refs exact:** 3/3 ✅

**VERDICT:** ✅ APPROVED FOR FILMING

**NO errors like Fuentes script (HW 16/32, 8,000 Italian Jews)**
```

---

## KEY DIFFERENCES FROM OLD WORKFLOW

### OLD WAY (Fuentes Project):
1. Research in NotebookLM
2. Write script from memory/notes
3. Fact-check after writing
4. Find errors (HW 16/32, 8,000 vs 1,023)
5. Rewrite script
6. Re-fact-check
7. Finally ready to film

**Time:** 8-10 hours
**Errors:** 2 major errors

---

### NEW WAY (This Workflow):
1. Research + verify simultaneously (01-VERIFIED-RESEARCH.md)
2. Write script ONLY from verified facts (02-SCRIPT-DRAFT.md)
3. Cross-check script against verified research (03-FACT-CHECK-VERIFICATION.md)
4. Ready to film (no errors)

**Time:** 4-6 hours
**Errors:** 0 (facts pre-verified)

---

## RULES TO PREVENT ERRORS

### RULE 1: No Unverified Facts in Script
**If it's not in VERIFIED-RESEARCH.md → Don't use it**

**Example:**
```
❌ BAD: "I think it was around 8,000 Italian Jews..."
✅ GOOD: Check VERIFIED-RESEARCH.md → 1,023 from Rome raid
```

---

### RULE 2: Exact Quotes Only
**Never paraphrase. Use exact text from VERIFIED-RESEARCH.md**

**Example:**
```
❌ BAD: Fulcher said something about blood and killing
✅ GOOD: "About ten thousand were beheaded. Not one of them was allowed to live."
```

---

### RULE 3: Verify Archive References
**Check exact catalogue numbers**

**Example:**
```
❌ BAD: HW 16/32 (looks right, but wrong!)
✅ GOOD: HW 16/23 (verified in UK National Archives catalogue)
```

---

### RULE 4: 90% Rule
**Don't start writing until 90%+ of claims verified**

**Why:** If you start too early, you'll use unverified facts out of laziness

---

### RULE 5: One Research Doc Only
**No RESEARCH-SUMMARY.md AND NOTEBOOKLM-OUTPUT.md AND CLAIMS.md**
**Just:** 01-VERIFIED-RESEARCH.md (updated as you go)

---

## QUALITY GATES (Can't Proceed Until Pass)

### Gate 1: Research → Script
**Can't start writing until:**
- [ ] 90%+ claims verified
- [ ] All major quotes word-for-word exact
- [ ] All archival refs precise
- [ ] All numbers have 2+ sources

---

### Gate 2: Script → Filming
**Can't film until:**
- [ ] Script cross-checked against VERIFIED-RESEARCH.md
- [ ] 100% of claims in script match verified research
- [ ] 0 errors found in cross-check
- [ ] Read out loud test passed

---

## TIME SAVINGS

**Old workflow:**
- Research: 3 hours
- Write: 2 hours
- Fact-check: 2 hours
- Fix errors: 1 hour
- Re-check: 1 hour
- **Total: 9 hours**

**New workflow:**
- Research + Verify: 4 hours (slower, but thorough)
- Write from verified facts: 1 hour (faster - no thinking needed)
- Cross-check: 30 min (quick - just matching)
- **Total: 5.5 hours**

**Savings: 3.5 hours per video**

---

## NEXT VIDEO: IMPLEMENTATION PLAN

### Day 1: Research Phase
1. Create `01-VERIFIED-RESEARCH.md`
2. Load NotebookLM sources
3. For each claim:
   - Research in NotebookLM
   - Immediately verify with 2+ sources
   - Add to VERIFIED-RESEARCH.md
   - Mark ✅ or ⏳
4. Don't stop until 90%+ verified

### Day 2: Script Phase
1. Create `02-SCRIPT-DRAFT.md`
2. Write ONLY from verified facts
3. Every claim → reference line # in VERIFIED-RESEARCH.md
4. If you need unverified fact → STOP → Go verify it
5. Self-check before calling "final"

### Day 3: Cross-Check Phase
1. Create `03-FACT-CHECK-VERIFICATION.md`
2. Check every line of script
3. Confirm matches VERIFIED-RESEARCH.md
4. If 100% match → ✅ APPROVED FOR FILMING
5. If any mismatch → Fix immediately

**Result:** Script ready to film with ZERO fact-check errors

---

## TEMPLATES READY TO USE

I'll create these for you:
1. `01-VERIFIED-RESEARCH-TEMPLATE.md`
2. `02-SCRIPT-DRAFT-TEMPLATE.md`
3. `03-FACT-CHECK-VERIFICATION-TEMPLATE.md`

**Want me to create these templates now for your next video?**
