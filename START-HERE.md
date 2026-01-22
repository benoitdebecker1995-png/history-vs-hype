# History vs Hype - Start Here

**Last Updated:** 2026-01-06

## CHANGELOG

**2026-01-06 - Documentation Hierarchy & Workflow Clarity**
- Added Documentation Hierarchy (Tier 1-3 authority system for reference files)
- Added Command vs Skill vs Agent Decision Tree (clarifies when to use each)
- Integrated VERIFIED-CLAIMS-DATABASE into Phase 1 workflow (saves 2-4 hours/video)
- All Tier 1 & 2 enforcement mechanisms now live in workflow.md
**Your current system:** Verified Workflow (3-phase, zero-error scriptwriting)

---

## QUICK START: NEXT VIDEO

```bash
/new-video
```

This starts the 3-phase workflow that prevents fact-check errors:
1. **Research + Verify** (4 hours) → 01-VERIFIED-RESEARCH.md
2. **Choose Format Template** (5 min) → NEW! See format templates below
3. **Write Script** (1 hour) → 02-SCRIPT-DRAFT.md
4. **Cross-Check** (30 min) → 03-FACT-CHECK-VERIFICATION.md

**Result:** 5.5 hours, 0 errors, ready to film

---

## NEW: FORMAT TEMPLATES (2026-01-04)

**5 signature series structures** that differentiate your channel:

**⭐ BOTH EXTREMES ARE WRONG** (Primary Series)
- Use when: Two polarized online claims about same history
- Next video: Medieval Flat Earth (Episode 2)
- Structure: False binary → Debunk A → Debunk B → Real story
- See: `.claude/REFERENCE/FORMAT-TEMPLATES.md`

**Other Templates:**
- DOCUMENT SHOWDOWN (side-by-side source comparison)
- TREATY AUTOPSY (legal document line-by-line)
- THE MAP THEY IGNORED (alternative borders from real documents)
- SAME DAY DIFFERENT WAR (multiple theaters, same date)

**Full details:** `video-projects/_IN_PRODUCTION/research-session-autonomous/FORMAT-TEMPLATES-FINAL.md`

---

## YOUR WORKFLOW SYSTEM

### Main Documentation

**📘 Quick Reference** (start here)
- `VERIFIED-WORKFLOW-QUICK-REFERENCE.md` - One-page workflow guide with checklists

**📗 Complete Guide** (detailed explanation)
- `.claude/REFERENCE/workflow.md` - Full 3-phase process

### Advanced Features

**📺 YouTube Claim Extraction**
- `.claude/tools/YOUTUBE-TRANSCRIPT-SETUP.md` - Extract claims from competitor videos
- Command: `/extract-claims`

---

## TEMPLATES (Your Starting Points)

**Location:** `.claude/templates/`

**Phase 1:** `01-VERIFIED-RESEARCH-TEMPLATE.md`
- Single source of truth for verified facts
- Used during NotebookLM research
- Tracks: ✅ VERIFIED, ⏳ RESEARCHING, ❌ UNVERIFIABLE

**Phase 2:** `02-SCRIPT-DRAFT-TEMPLATE.md`
- Production-ready script structure
- Write ONLY from verified facts
- Self-check before calling "final"

**Phase 3:** `03-FACT-CHECK-VERIFICATION-TEMPLATE.md`
- Final quality gate before filming
- Cross-checks script vs research
- Output: ✅ APPROVED or ❌ NEEDS REVISION

**Note:** `/new-video` automatically sets these up for you

---

## COMMANDS CHEAT SHEET

### Video Production
```bash
/new-video    # Start new video (3-phase workflow)
/script                # Generate script from research
/fact-check            # Run academic peer review
```

### Content Tools
```bash
/extract-claims        # Extract claims from YouTube transcript
/youtube-metadata      # Generate optimized metadata
/zero-budget-assets    # Create DIY B-roll guide
/fix-subtitles         # Fix auto-transcription errors
```

### Analysis
```bash
/analyze-interview     # Build production docs from interview
/edit-guide            # Generate shot-by-shot visual guide
```

---

## PROJECT STRUCTURE

### Active Projects
```
video-projects/_IN_PRODUCTION/
  [number]-[topic-slug-year]/
    01-VERIFIED-RESEARCH.md      ← Research phase
    02-SCRIPT-DRAFT.md            ← Writing phase
    03-FACT-CHECK-VERIFICATION.md ← Quality gate
    PROJECT-STATUS.md             ← Track progress
    _research/                    ← Source materials
```

### Workflow Stages
- **_IN_PRODUCTION/** - Active research and scripting
- **_READY_TO_FILM/** - Scripts approved, ready to record
- **_ARCHIVED/** - Published or cancelled videos

---

## CORE PRINCIPLES

### 1. Verify First, Write Second
**Old way:** Research → Write → Fact-check → Find errors → Rewrite
**New way:** Research + Verify → Write from verified facts → Quick check

**Why:** Prevents Fuentes-type errors (HW 16/32, wrong numbers)

### 2. Single Source of Truth
**One document:** 01-VERIFIED-RESEARCH.md (updated as you research)
**Not multiple:** RESEARCH-SUMMARY.md + SCRIPT-FACT-CHECK.md + NOTEBOOKLM-OUTPUT.md

**Why:** Prevents conflicting fact-check documents

### 3. Quality Gates
**Gate 1:** Can't write script until 90%+ claims verified
**Gate 2:** Can't film until 100% cross-checked

**Why:** Catches errors before filming (saves reshoot time)

### 4. 2+ Source Standard
**Every major claim:** Requires 2+ independent Tier 1-2 sources
- Tier 1: Primary documents, peer-reviewed publications, expert historians
- Tier 2: University press books, respected journalists
- Don't use: Wikipedia, blogs, YouTube (for final verification)

**Why:** Academic-level accuracy

### 5. Word-for-Word Verification
**Quotes:** Exact text from primary sources (no paraphrasing)
**Numbers:** Match source documents exactly
**Archive refs:** Precise catalogue numbers (HW 16/23, not HW 16/32)

**Why:** Prevents subtle errors that damage credibility

---

## DOCUMENTATION HIERARCHY

**When reference files conflict, this is the order of authority:**

### Tier 1: Authoritative (NEVER contradict these)
1. **`.claude/REFERENCE/workflow.md`** - Workflow steps, quality gates, enforcement rules
2. **`.claude/REFERENCE/channel-values.md`** - Brand DNA, non-negotiables, documentary tone
3. **`.claude/USER-PREFERENCES.md`** - Your natural speaking patterns, delivery preferences

### Tier 2: Operational (Must align with Tier 1)
4. **`.claude/agents/*.md`** - Agent execution instructions
5. **`.claude/commands/*.md`** - Command entry points
6. **`.claude/templates/*.md`** - Starting structures for projects

### Tier 3: Reference (Useful but not authoritative)
7. **All other `.claude/REFERENCE/*.md` files** - Examples, techniques, patterns

**Maintenance Rule:**
- When updating Tier 1: Review Tier 2 files for alignment
- When updating Tier 2: No need to update Tier 3 (reference only)
- **If Tier 3 contradicts Tier 1: Tier 1 wins, update Tier 3**

**Why this matters:** You have 30+ reference files. This hierarchy prevents confusion and ensures consistency when documents disagree.

---

## COMMAND VS SKILL VS AGENT: DECISION TREE

**Confused about when to use `/command`, a skill, or call an agent directly? Use this guide:**

### Use COMMAND when:
- ✅ You want the standard workflow for a task
- ✅ You're following the verified 3-phase system
- ✅ Commands auto-invoke the right agents/skills for you

**Examples:**
- "I want to start a new video" → `/new-video` (handles project setup, templates, workflow)
- "I want to fact-check a script" → `/fact-check` (runs fact-checker agent with full protocol)
- "I want to generate metadata" → `/youtube-metadata` (runs optimizer with channel DNA filter)

### Use SKILL directly when:
- ✅ You want a specific sub-task without full workflow
- ✅ You're customizing or skipping workflow steps
- ✅ You need just one component of a larger process

**Examples:**
- "I just want the voice consistency check" → Use `script-reviewer` skill (not full review)
- "I just need NotebookLM prompts" → Use `notebooklm-prompt-generator` skill
- "I just want clip suggestions" → Use `clip-suggestions` skill

### Call AGENT directly when:
- ✅ You need advanced customization
- ✅ You're running experimental/non-standard workflows
- ✅ Command doesn't exist for your use case

**Examples:**
- "I want to test a new scriptwriting approach" → Call `script-writer-v2` agent with custom parameters
- "I want non-standard fact-checking criteria" → Call `fact-checker` agent with specific instructions
- "I need deep codebase exploration" → Call Task tool with `subagent_type=Explore`

**Quick Reference:**
- `/new-video` = Full workflow (command)
- `script-reviewer` = Just voice check (skill)
- `script-writer-v2` = Custom script generation (agent)

**Why this matters:** Reduces confusion, speeds up task completion, prevents invoking wrong tool.

---

## TIME COMPARISON

### Old Workflow (Fuentes Video)
- Research: 3 hours
- Write: 2 hours
- Fact-check: 2 hours
- Fix errors: 1 hour
- Re-check: 1 hour
- **Total: 9 hours, 2 errors**

### New Workflow (Next Video)
- Research + Verify: 4 hours
- Write from verified: 1 hour
- Cross-check: 30 min
- **Total: 5.5 hours, 0 errors**

**Savings: 3.5 hours per video (39% faster)**

---

## TYPICAL VIDEO PRODUCTION FLOW

### Day 1: Research Phase
```bash
/new-video
```
1. Open `01-VERIFIED-RESEARCH.md`
2. Load sources into NotebookLM
3. As you verify each claim:
   - Add to research doc
   - Mark ✅ VERIFIED or ⏳ RESEARCHING
   - Get exact quotes, precise numbers
4. Don't proceed until 90%+ verified

### Day 2: Script Phase
1. Open `02-SCRIPT-DRAFT.md`
2. Write from `01-VERIFIED-RESEARCH.md` ONLY
3. Every claim references line # in research doc
4. If you need unverified fact → STOP → Verify first
5. Self-check passes? → Proceed to Phase 3

### Day 3: Quality Gate
1. Open `03-FACT-CHECK-VERIFICATION.md`
2. Cross-check every claim vs research doc
3. Verify: quotes exact, numbers match, refs precise
4. Result: ✅ APPROVED FOR FILMING
5. Create B-ROLL-CHECKLIST.md and YOUTUBE-METADATA.md

### Day 4: Film
- Confident (every fact verified)
- No anxiety (script is pre-checked)
- Ready to publish (no post-filming fixes)

---

## WHEN TO USE WHAT

### Standard Video (10-12 minutes)
- Use 3-phase verified workflow
- Time: 5.5 hours
- Commands: `/new-video` → `/youtube-metadata`

### Fact-Checking Video (debunking Pax Tube, Nick Fuentes, etc.)
1. Get transcript: `YOUTUBE-TRANSCRIPT-SETUP.md` (manual extract)
2. Extract claims: `/extract-claims`
3. Verify claims: 3-phase workflow
4. Write script: `/script`
5. Quality gate: `/fact-check` (academic peer review)

### High-Stakes Topic (Holocaust, genocide, sensitive)
- Use 3-phase workflow + academic peer review
- Add: `/fact-check` (3-reviewer system)
- Time: Add 1-2 hours for peer review
- Result: Journal-publication-level accuracy

### Rapid Response (trending topic, <24 hours)
1. Extract claims: `/extract-claims`
2. Quick verify (top 3-5 claims only)
3. Write short script (3-5 minutes)
4. Fast cross-check
5. Film same day
- Note: Still verify facts, just fewer of them

---

## FOLDER NAVIGATION

### Documentation
- Root: Workflow guides, upgrade summaries
- `.claude/`: Agent configs, command definitions, templates
- `.claude/agents/`: Specialized AI agents
- `.claude/commands/`: Slash command definitions
- `.claude/templates/`: Reusable templates for projects

### Production
- `video-projects/_IN_PRODUCTION/`: Active projects
- `video-projects/_READY_TO_FILM/`: Approved scripts
- `video-projects/_ARCHIVED/`: Published videos

### Research
- `library/`: Books, PDFs organized by topic
- Per-project `_research/` folders: NotebookLM sources, transcripts

---

## AGENT SYSTEM

### video-orchestrator
**Purpose:** Coordinates full workflow from topic to finished script
**When to use:** Complex multi-phase videos
**Command:** Invoke via Task tool with subagent_type="video-orchestrator"

### script-writer-v2
**Purpose:** Writes retention-optimized scripts with viral hooks
**When to use:** After research phase complete
**Command:** `/script`

### structure-checker-v2
**Purpose:** Analyzes scripts for retention issues before filming
**When to use:** Review draft scripts
**Features:** Predicts dropout points, suggests fixes

### fact-checker
**Purpose:** Verifies sources and claims using tier-based system
**When to use:** Automatically runs during fact-check phase
**Rules:** Single source of truth, 2+ sources required, word-for-word quotes

### claims-extractor
**Purpose:** Extracts factual claims from transcripts for systematic fact-checking
**When to use:** Fact-checking competitor videos
**Command:** `/extract-claims`

### diy-asset-creator
**Purpose:** Creates zero-budget DIY guides for B-roll assets
**When to use:** After script complete, need B-roll on budget
**Command:** `/zero-budget-assets`

---

## TROUBLESHOOTING

### "Where do I start?"
→ Run `/new-video` and open `01-VERIFIED-RESEARCH.md`

### "The templates are overwhelming"
→ Start with `VERIFIED-WORKFLOW-QUICK-REFERENCE.md` (simpler)

### "I'm not sure if my research is verified enough"
→ Check: Do you have 2+ Tier 1-2 sources for each major claim?

### "Can I skip Phase 3?"
→ No. Fuentes video was careful, still had 2 errors

### "My script has [TK] placeholders"
→ Go back to Phase 1, verify those facts first

### "I found an error in the published video"
→ Update `01-VERIFIED-RESEARCH.md` for next video, note the error type

---

## KEY FILES TO BOOKMARK

### Daily Use:
1. `VERIFIED-WORKFLOW-QUICK-REFERENCE.md` - Workflow checklist
2. `.claude/templates/` - Starting templates
3. `.claude/tools/get-transcript.py` - Get competitor transcripts

### Reference:
4. `.claude/REFERENCE/workflow.md` - Complete workflow
5. `.claude/REFERENCE/scriptwriting-style.md` - Voice and style guide
6. `.claude/REFERENCE/retention-mechanics.md` - Engagement triggers

---

## SUCCESS METRICS

**Track for next 3 videos:**

### Quality (Goal: 100%)
- [ ] Fact-check errors: 0
- [ ] Rewrites required: 0
- [ ] Claims verified before writing: 90%+

### Efficiency (Goal: <6 hours)
- [ ] Total time per video: ___ hours
- [ ] Time saved vs old workflow: ___ hours
- [ ] Same-day filming after approval: Yes/No

### Confidence (Goal: High)
- [ ] Felt confident filming: Yes/No
- [ ] Worried about errors: No/Yes
- [ ] Corrections needed after publishing: 0

---

## WHAT MAKES THIS SYSTEM WORK

### Prevention Over Correction
- Verify facts BEFORE writing (not after)
- Quality gates prevent progression with errors
- Single source of truth (no conflicting docs)

### Academic Standards, YouTube Speed
- 2+ source requirement (like academic papers)
- Word-for-word quote verification (like peer review)
- 5.5 hour turnaround (unlike academic publishing)

### Built for Your Workflow
- NotebookLM integration (your primary research tool)
- Fact-checking focus (your competitive advantage)
- Evidence-based approach (your channel mission)

---

## NEXT STEPS

### Right Now:
```bash
/new-video
```

### This Week:
1. Use verified workflow for next video
2. Track time spent in each phase
3. Note any template improvements needed

### This Month:
1. Build muscle memory (use for 2-3 videos)
2. Refine templates based on experience
3. Measure: time saved, errors prevented

### Ongoing:
1. Update templates as you learn
2. Build library of verified facts
3. Scale the system (topic-specific templates)

---

## HELP & SUPPORT

### Documentation Issues:
- Check `VERIFIED-WORKFLOW-QUICK-REFERENCE.md` first
- Then `.claude/CORE-WORKFLOW-SCRIPTWRITING-FACTCHECKING.md`
- Still stuck? Check troubleshooting sections

### Workflow Questions:
- "Am I doing this right?" → Check workflow checklists
- "Can I skip this step?" → Check quality gates (usually no)
- "Is this verified enough?" → Check 2+ source standard

### System Improvements:
- Note issues in PROJECT-STATUS.md
- Update templates as needed
- Document learnings for next video

---

**Welcome to the verified workflow system. Start your next video with `/new-video` and experience zero-error scriptwriting.**
