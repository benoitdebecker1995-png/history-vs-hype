---
description: Start new video with 3-phase verified workflow (research → script → fact-check)
---

# New Video - Verified Workflow

You are setting up a new History vs Hype video project using the **3-phase verified workflow** that prevents fact-check errors.

## WORKFLOW OVERVIEW

**Phase 1:** Research + Verify simultaneously → `01-VERIFIED-RESEARCH.md`
**Phase 2:** Write script from verified facts only → `02-SCRIPT-DRAFT.md`
**Phase 3:** Cross-check script against research → `03-FACT-CHECK-VERIFICATION.md`

**Goal:** Zero fact-check errors (like Fuentes HW 16/32, 8,000 Italian Jews)

---

## YOUR TASK

### Step 1: Gather Project Information

Ask the user:
1. **Topic:** What's the video about?
2. **Opponent (if applicable):** Who are you fact-checking? (Pax Tube, Nick Fuentes, etc.)
3. **Modern hook:** What current event makes this relevant? (2024-2025 news)
4. **Project number:** What number is this? (Check existing projects in `_IN_PRODUCTION/`)

### Step 2: Check Claims Database for Existing Verified Facts

Before creating the project folder, search for relevant verified claims:

1. **Read:** `.claude/VERIFIED-CLAIMS-DATABASE.md`
2. **Search for:** Topic keywords, related subjects, overlapping time periods
3. **If claims found:**
   - Note which claims are already verified
   - These can be used directly in 01-VERIFIED-RESEARCH.md
   - Mark as "Previously verified: [date], [video]"
   - Only research claims NOT already in database
4. **If no claims found:** Proceed with full research

This step prevents duplicate research and ensures consistency across videos.

### Step 3: Create Project Folder

**Location:** `video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/`

**Example:** `video-projects/_IN_PRODUCTION/5-french-colonialism-2025/`

**Create folder structure:**
```
[number]-[topic-slug-year]/
  01-VERIFIED-RESEARCH.md
  02-SCRIPT-DRAFT.md (placeholder for Phase 2)
  03-FACT-CHECK-VERIFICATION.md (placeholder for Phase 3)
  _research/ (for NotebookLM outputs, source PDFs, etc.)
```

### Step 4: Initialize 01-VERIFIED-RESEARCH.md

**Copy from:** `.claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md`

**Fill in:**
- Project name
- Date started
- Topic categories (based on what user described)

**Leave blank:**
- Claims (user will fill as they research)
- Verification stats (will update during research)

### Step 5: Create Placeholder Files

**02-SCRIPT-DRAFT.md:**
```markdown
# Script Draft - [Topic]

**Status:** ⏸️ WAITING FOR PHASE 1 COMPLETION

Do not write script until 01-VERIFIED-RESEARCH.md is 90%+ verified.

**Next step:** Complete research phase first.
```

**03-FACT-CHECK-VERIFICATION.md:**
```markdown
# Final Fact-Check - [Topic]

**Status:** ⏸️ WAITING FOR PHASE 2 COMPLETION

This file will be used to cross-check the script after Phase 2.

**Next step:** Complete script phase first.
```

### Step 6: Create Research Folder

**Create:** `_research/` subfolder

**Add:** `NOTEBOOKLM-SETUP.md` with:
```markdown
# NotebookLM Setup for [Topic]

## Sources to Load

**Primary Sources:**
- [ ] [List key primary documents to find]

**Academic Sources:**
- [ ] [List expert historians' books]

**Modern Context:**
- [ ] [List 2024-2025 news articles]

## Research Questions

1. [What specific claims need verification?]
2. [What statistics need sources?]
3. [What quotes need exact wording?]

## Next Steps

1. Load sources into NotebookLM
2. Use research prompts from Master Project Template
3. As you verify each fact, add to 01-VERIFIED-RESEARCH.md
4. Don't start writing until 90%+ verified
```

### Step 7: Create PROJECT-STATUS.md

```markdown
# Project Status: [Topic]

**Created:** [Date]
**Current Phase:** 1 - Research + Verification
**Target Completion:** [Date]

---

## Phase 1: Research + Verification ⏳

**File:** 01-VERIFIED-RESEARCH.md
**Status:** 0% complete

**Tasks:**
- [ ] Load NotebookLM sources
- [ ] Identify all claims to verify
- [ ] Verify 90%+ of major claims
- [ ] All quotes word-for-word exact
- [ ] All numbers have 2+ sources
- [ ] Ready to write script

**Blocked by:** Nothing - start researching!

---

## Phase 2: Script Writing ⏸️

**File:** 02-SCRIPT-DRAFT.md
**Status:** Not started

**Waiting for:** Phase 1 to reach 90% verification

**Tasks:**
- [ ] Write script from verified facts only
- [ ] Every claim references research doc
- [ ] No unverified facts
- [ ] Read-aloud test
- [ ] Retention optimized

---

## Phase 3: Final Verification ⏸️

**File:** 03-FACT-CHECK-VERIFICATION.md
**Status:** Not started

**Waiting for:** Phase 2 script completion

**Tasks:**
- [ ] Cross-check every claim
- [ ] Verify all quotes word-for-word
- [ ] Verify all numbers exact
- [ ] Check archival references
- [ ] 100% match → Approve for filming

---

## Production Ready? ❌

**Script approved for filming:** NO
**Next step:** Complete Phase 1 research
```

---

## Step 8: Provide User Instructions

Tell the user:

```
✅ New video project created: [Project name]

📁 Location: video-projects/_IN_PRODUCTION/[folder-name]/

📋 Files created:
  - 01-VERIFIED-RESEARCH.md (START HERE)
  - 02-SCRIPT-DRAFT.md (placeholder - don't use yet)
  - 03-FACT-CHECK-VERIFICATION.md (placeholder)
  - PROJECT-STATUS.md (track progress)
  - _research/NOTEBOOKLM-SETUP.md (source checklist)

---

🎯 NEXT STEPS:

**Phase 1: Research + Verification** (Your focus now)

1. Open _research/NOTEBOOKLM-SETUP.md
2. Load sources into NotebookLM
3. As you research each claim:
   - Verify with 2+ sources
   - Get exact quotes word-for-word
   - Add to 01-VERIFIED-RESEARCH.md
   - Mark ✅ VERIFIED or ⏳ RESEARCHING

4. Don't start writing until 90%+ claims verified

**Why this workflow?**
- Prevents Fuentes-type errors (wrong refs, wrong numbers)
- Saves 3.5 hours per video (no rewriting after fact-check)
- Script is pre-verified, ready to film immediately

---

📚 Reference Documents:
- .claude/REFERENCE/workflow.md (full workflow)
- .claude/templates/ (all 3 templates)

**Questions?** Update PROJECT-STATUS.md as you progress through phases.
```

---

**After Video Completion (Post-Filming):**

When the video is complete, update VERIFIED-CLAIMS-DATABASE.md:
1. Extract reusable claims from 01-VERIFIED-RESEARCH.md
2. Add to appropriate topic cluster (or create new cluster)
3. Include: video title, verification date, tier, full sources
4. Flag any claims that may become outdated

This ensures facts verified for this video are available for future videos.

---

## IMPORTANT REMINDERS

**For the AI:**
1. ✅ Create all files in lifecycle folder (`_IN_PRODUCTION/`)
2. ✅ Use templates from `.claude/templates/`
3. ✅ Don't skip Phase 1 - verify first, write second
4. ✅ Keep placeholders empty until phase is ready
5. ✅ Update PROJECT-STATUS.md to show current phase

**For the user:**
1. ❌ Don't write script until research 90%+ verified
2. ❌ Don't use unverified facts "just for now"
3. ❌ Don't skip cross-check phase
4. ✅ One fact-check doc only (no RESEARCH-SUMMARY.md + SCRIPT-FACT-CHECK.md)
5. ✅ Mark verification status as you go (✅ / ⏳ / ❌)

---

## WORKFLOW QUALITY GATES

**Gate 1: Research → Script**
Can't proceed to Phase 2 until:
- [ ] 90%+ claims verified
- [ ] All major quotes word-for-word exact
- [ ] All archival refs precise
- [ ] All numbers have 2+ sources
- [ ] 01-VERIFIED-RESEARCH.md status: "READY TO WRITE SCRIPT"

**Gate 2: Script → Filming**
Can't film until:
- [ ] Script cross-checked against research doc
- [ ] 100% of claims match verified research
- [ ] 0 errors found
- [ ] 03-FACT-CHECK-VERIFICATION.md status: "APPROVED FOR FILMING"

**Gate 3: Video Complete → Database Update**
After filming and publishing:
- [ ] Reusable claims extracted from 01-VERIFIED-RESEARCH.md
- [ ] Claims added to VERIFIED-CLAIMS-DATABASE.md
- [ ] Topic cluster created or updated

---

**This command sets up the workflow that prevents fact-check errors and saves 3.5 hours per video.**
