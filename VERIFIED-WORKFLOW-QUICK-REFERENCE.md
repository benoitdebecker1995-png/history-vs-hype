# Verified Workflow - Quick Reference

**Last Updated:** 2025-01-16
**Purpose:** Zero-error scriptwriting workflow for History vs Hype videos

---

## THE PROBLEM WE SOLVED

**Old workflow:**
```
Research → Write → Fact-check → Find errors → Rewrite → Re-check
Time: 9 hours | Errors: 2+ per video (Fuentes: HW 16/32, 8,000 Italian Jews)
```

**New workflow:**
```
Research + Verify → Write from verified facts → Quick cross-check → Film
Time: 5.5 hours | Errors: 0
```

**Savings:** 3.5 hours per video + zero rewrites

---

## QUICK START: YOUR NEXT VIDEO

### 1. Create New Project

```bash
/new-video
```

This creates:
- `01-VERIFIED-RESEARCH.md` (start here)
- `02-SCRIPT-DRAFT.md` (use later)
- `03-FACT-CHECK-VERIFICATION.md` (final check)
- `PROJECT-STATUS.md` (track progress)

---

### 2. Phase 1: Research + Verify (3-4 hours)

**File:** `01-VERIFIED-RESEARCH.md`

**As you research in NotebookLM:**

#### For each claim:
```markdown
### ✅ CLAIM 1: Death Toll
**What opponent claims:** "Tens of thousands killed"
**What's actually true:** Modern estimate ~3,000
**Sources:**
1. Asbridge (Tier 2) - The Crusades, p. 98
2. Riley-Smith (Tier 2) - The Crusades: A History, p. 45
**Script-Ready:** ✅ YES
```

#### For each quote:
```markdown
### Quote 1: Fulcher of Chartres
**Exact text:**
> "About ten thousand were beheaded. Not one of them was allowed to live."
**Verified:** ✅ Word-for-word exact (Krey translation, 1921)
**Script-Ready:** ✅ YES
```

#### For each number:
```markdown
| Claim | Number | Sources | Verified |
|-------|--------|---------|----------|
| Jerusalem deaths | ~3,000 | Asbridge, Riley-Smith | ✅ |
```

**Don't proceed until:** 90%+ claims marked ✅ VERIFIED

---

### 2.5. Choose Format Template (NEW - 2026-01-04) (5 minutes)

**Before writing, identify if topic fits a signature format:**

**Format Options:**
1. ⭐ **BOTH EXTREMES ARE WRONG** - Two polarized online claims? (Primary series)
2. **DOCUMENT SHOWDOWN** - Two competing documents? (Secondary series)
3. **TREATY AUTOPSY** - Legal treaty with modern dispute? (ICJ cases)
4. **THE MAP THEY IGNORED** - Documented alternative borders? (Quarterly)
5. **SAME DAY DIFFERENT WAR** - Multiple theaters, same date? (Special)
6. **CUSTOM** - None fit? (Write custom structure)

**If format identified:**
- See `.claude/REFERENCE/FORMAT-TEMPLATES.md` for full Act structure
- Follow template exactly (builds viewer expectations)
- Use series branding (title formula, intro, thumbnail)

**Example:** Medieval Flat Earth = "Both Extremes Are Wrong" format
- Extreme A: Modern flat-earthers claim medieval "truth"
- Extreme B: Science advocates claim Church suppressed knowledge
- Act structure: False binary → Debunk A → Debunk B → Real story

---

### 3. Phase 2: Write Script (1-1.5 hours)

**File:** `02-SCRIPT-DRAFT.md`

**RULE:** Only use facts from `01-VERIFIED-RESEARCH.md`

**If you need a fact that's not verified → STOP → Go verify it first**

**Structure:**
- Hook (0:00-0:45): Modern relevance
- Main claim to debunk (0:45-1:00)
- Structure telegraph (1:00-1:15)
- Evidence sections with callback hooks every ~4 minutes
- Modern connections (8:30-10:00)
- CTA (10:30-11:00)

**As you write, note verification references:**
```markdown
[Fulcher quote here]

**Verification Reference:** ✅ Quote #1 from 01-VERIFIED-RESEARCH.md (line 45)
```

**Don't proceed until:** Script self-check passes (all boxes checked)

---

### 4. Phase 3: Cross-Check (30 minutes)

**File:** `03-FACT-CHECK-VERIFICATION.md`

**For each claim in script:**
1. Find in `01-VERIFIED-RESEARCH.md`
2. Confirm exact match
3. Mark ✅

**Check:**
- [ ] All quotes word-for-word exact
- [ ] All numbers match verified research
- [ ] All archival refs precise (no HW 16/32 errors)
- [ ] No unverified claims
- [ ] Contested claims properly labeled

**Result:** ✅ APPROVED FOR FILMING or ❌ NEEDS REVISION

---

### 5. Optional: Academic Peer Review

**For high-stakes topics** (Holocaust, genocide, politically controversial):

```bash
/fact-check
```

Uses `.claude/ACADEMIC-PEER-REVIEW-PROTOCOL.md`:
- 3 reviewers (source verification, methodology, completeness)
- Journal-publication-level verification
- Catches logical fallacies, omissions, bias

---

## THE 3 FILES EXPLAINED

### 📄 01-VERIFIED-RESEARCH.md
**Purpose:** Single source of truth for verified facts
**When to use:** During research phase
**When to update:** As you verify each claim in NotebookLM
**Status markers:** ✅ VERIFIED, ⏳ RESEARCHING, ❌ UNVERIFIABLE

### 📄 02-SCRIPT-DRAFT.md
**Purpose:** Production-ready script written from verified facts
**When to use:** After 90%+ research verified
**Rule:** Every claim must reference line # in 01-VERIFIED-RESEARCH.md
**Status:** Ready when self-check passes

### 📄 03-FACT-CHECK-VERIFICATION.md
**Purpose:** Final quality gate before filming
**When to use:** After script complete
**Goal:** 100% match between script and verified research
**Status:** ✅ APPROVED or ❌ NEEDS REVISION

---

## QUALITY GATES (Don't Skip!)

### Gate 1: Research → Script
**Can't start writing until:**
- [ ] 90%+ claims verified
- [ ] All major quotes word-for-word exact
- [ ] All archival refs precise
- [ ] All numbers have 2+ sources

### Gate 2: Script → Filming
**Can't film until:**
- [ ] 100% of claims cross-checked
- [ ] Zero errors found
- [ ] Read-aloud test passed
- [ ] Retention optimized

---

## PREVENTING COMMON ERRORS

### Error Type 1: Wrong Archive Reference
**Example:** HW 16/32 vs HW 16/23 (Fuentes error)

**Prevention:**
```markdown
# In 01-VERIFIED-RESEARCH.md:
### Reference 1: Höfle Telegram
**Exact Reference:** HW 16/23
**Common errors to avoid:** NOT HW 16/32
**Verified from:** UK National Archives catalogue
```

### Error Type 2: Wrong Numbers
**Example:** 8,000 vs 1,023 Italian Jews (Fuentes error)

**Prevention:**
```markdown
# In 01-VERIFIED-RESEARCH.md:
| Rome raid deportations | 1,023 | Höfle Telegram HW 16/23 | ✅ |
| NOT: | ❌ 8,000 | (unverified claim) | ❌ |
```

### Error Type 3: Paraphrased Quotes
**Example:** "Fulcher said something about blood" vs exact quote

**Prevention:**
```markdown
# In 01-VERIFIED-RESEARCH.md:
**Exact text:**
> "About ten thousand were beheaded. Not one of them was allowed to live."
**Verified:** ✅ Word-for-word exact (Krey 1921, Ryan 1969 cross-check)
```

---

## WORKFLOW COMMANDS

### Start new video:
```bash
/new-video
```

### Extract claims from YouTube video:
```bash
/extract-claims
[Paste transcript]
```

### Generate script:
```bash
/script
[Uses 02-SCRIPT-DRAFT-TEMPLATE.md]
```

### Run academic peer review:
```bash
/fact-check
[Uses ACADEMIC-PEER-REVIEW-PROTOCOL.md]
```

---

## TIME BREAKDOWN

### Old Workflow (9 hours):
- Research: 3 hours
- Write: 2 hours
- Fact-check: 2 hours
- Fix errors: 1 hour
- Re-check: 1 hour

### New Workflow (5.5 hours):
- Research + Verify: 4 hours (slower but thorough)
- Write from verified: 1 hour (faster - just assembly)
- Cross-check: 30 min (quick - just matching)

### Savings:
- **Time:** 3.5 hours per video
- **Rewrites:** 0 (vs 1-2 with old workflow)
- **Errors:** 0 (vs 2+ with old workflow)

---

## SOURCE TIER SYSTEM

Use this for `01-VERIFIED-RESEARCH.md`:

**Tier 1 (Best):**
- Primary documents (treaties, census, government archives)
- Peer-reviewed academic publications
- Expert historians specializing in topic

**Tier 2 (Good):**
- Respected historians (general)
- Peer-reviewed journals (related fields)
- University press books

**Tier 3 (Use with caution):**
- Respected journalists with expertise
- International organization reports
- Declassified documents (note potential bias)

**Tier 4-5 (Don't use):**
- Wikipedia
- Blogs
- YouTube videos
- Unverified sources

**Rule:** Every major claim needs 2+ Tier 1-2 sources

---

## FILE ORGANIZATION

### During Production:
```
video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/
  01-VERIFIED-RESEARCH.md
  02-SCRIPT-DRAFT.md
  03-FACT-CHECK-VERIFICATION.md
  PROJECT-STATUS.md
  _research/
    NOTEBOOKLM-SETUP.md
    [PDFs, source docs, etc.]
```

### After Filming:
```
video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/
  FINAL-SCRIPT.md (rename from 02-SCRIPT-DRAFT.md)
  FACT-CHECK-VERIFICATION.md (final version)
  B-ROLL-CHECKLIST.md
  YOUTUBE-METADATA.md
  _research/ (keep for reference)
```

### After Publishing:
```
Move to: video-projects/_ARCHIVED/[number]-[topic-slug-year]/
```

---

## CHECKLIST: AM I DOING THIS RIGHT?

**During Research:**
- [ ] I'm adding facts to 01-VERIFIED-RESEARCH.md AS I verify them
- [ ] Every claim has 2+ Tier 1-2 sources
- [ ] Quotes are word-for-word exact (not paraphrased)
- [ ] Numbers match source documents exactly
- [ ] I'm marking status: ✅ VERIFIED, ⏳ RESEARCHING, ❌ UNVERIFIABLE

**During Script Writing:**
- [ ] I'm writing from 01-VERIFIED-RESEARCH.md only
- [ ] Every fact references line # in research doc
- [ ] I haven't used any unverified facts
- [ ] If I need something not verified, I stopped and verified it first

**During Cross-Check:**
- [ ] I'm comparing script to 01-VERIFIED-RESEARCH.md line by line
- [ ] Quotes are exact word-for-word matches
- [ ] Numbers are exact matches
- [ ] Archive references are precise
- [ ] I found 0 errors (if >0, fix before filming)

---

## WHAT IF I FIND AN ERROR IN PHASE 3?

**Option A: Minor error (typo, formatting)**
- Fix in script immediately
- Mark ✅ VERIFIED in cross-check doc
- Continue verification

**Option B: Major error (wrong number, wrong ref)**
1. Go back to `01-VERIFIED-RESEARCH.md`
2. Verify correct fact
3. Update research doc
4. Update script
5. Re-run cross-check
6. Mark ✅ VERIFIED

**Option C: Unverified fact in script**
1. Verify the fact (add to research doc)
2. Update script with verified version
3. OR remove from script if unverifiable
4. Re-run cross-check

---

## KEY PRINCIPLES

### 1. Single Source of Truth
**One fact-check document:** 01-VERIFIED-RESEARCH.md
**Not multiple:** RESEARCH-SUMMARY.md + SCRIPT-FACT-CHECK.md + NOTEBOOKLM-OUTPUT.md

### 2. Verify First, Write Second
**Don't** write script then fact-check
**Do** verify facts then assemble script

### 3. No Placeholders
**Don't** use [QUOTE TK] or [DATA TK] in script
**Do** verify everything before writing

### 4. 90% Rule
**Don't** start writing at 50% verified
**Do** wait until 90%+ verified

### 5. 100% Cross-Check
**Don't** skip cross-check phase
**Do** verify every single claim before filming

---

## TROUBLESHOOTING

### "I'm 50% through research, can I start writing?"
**No.** Wait until 90%+ verified. You'll use unverified facts if you start too early.

### "I found a great quote while writing, can I add it?"
**Only if you verify it first.** Add to 01-VERIFIED-RESEARCH.md, then use in script.

### "The cross-check found 3 errors, should I film anyway?"
**No.** Fix all errors first. Filming with errors wastes time (you'll reshoot).

### "Do I need all 3 phases for a short video?"
**Yes.** Even 3-minute videos need verification. Short doesn't mean less accurate.

### "Can I use Wikipedia for preliminary research?"
**Yes for initial research, NO for script.** Use Wikipedia to find Tier 1-2 sources, then verify with those.

---

## TEMPLATES LOCATION

All templates in: `.claude/templates/`

- `01-VERIFIED-RESEARCH-TEMPLATE.md`
- `02-SCRIPT-DRAFT-TEMPLATE.md`
- `03-FACT-CHECK-VERIFICATION-TEMPLATE.md`

**Don't edit templates.** Copy them for each new video.

---

## REFERENCE DOCUMENTS

**Core workflow:**
- `.claude/CORE-WORKFLOW-SCRIPTWRITING-FACTCHECKING.md` (detailed 3-phase process)
- `VERIFIED-WORKFLOW-QUICK-REFERENCE.md` (this document)

**Quality control:**
- `.claude/ACADEMIC-PEER-REVIEW-PROTOCOL.md` (optional extra verification)
- `.claude/agents/fact-checker.md` (fact-checking agent rules)

**Project setup:**
- `.claude/commands/new-video.md` (project initialization)
- `.claude/FOLDER-STRUCTURE-GUIDE.md` (where files go)

---

## EXPECTED RESULTS

### After implementing this workflow:

**Quality:**
- ✅ Zero fact-check errors (no HW 16/32, no wrong numbers)
- ✅ All quotes word-for-word exact
- ✅ All claims verified with 2+ sources
- ✅ Academic-level accuracy

**Efficiency:**
- ✅ 3.5 hours saved per video
- ✅ No rewrites after fact-checking
- ✅ Script ready to film immediately
- ✅ Faster upload (no post-filming fixes)

**Confidence:**
- ✅ Know every fact is verified before filming
- ✅ No anxiety about errors in published videos
- ✅ Respond to corrections with confidence
- ✅ Build reputation for accuracy

---

## NEXT VIDEO: ACTION PLAN

1. **Run:** `/new-video`
2. **Open:** `01-VERIFIED-RESEARCH.md`
3. **Research:** Verify facts in NotebookLM, add to research doc as you go
4. **Check:** 90%+ verified? → Proceed to Phase 2
5. **Write:** `02-SCRIPT-DRAFT.md` from verified facts only
6. **Cross-check:** `03-FACT-CHECK-VERIFICATION.md` matches 100%
7. **Film:** Confident, error-free script

**Time:** 5.5 hours (vs 9 hours old way)
**Errors:** 0 (vs 2+ old way)
**Rewrites:** 0 (vs 1-2 old way)

---

**This workflow prevents Fuentes-type errors and makes production 40% faster.**
