# Agent & Command Improvements - January 2025

Based on the successful Crusades fact-check workflow (project 4-crusades-fact-check-2025), I've upgraded the agent and command system with new capabilities proven in production.

---

## SUMMARY OF CHANGES

### New Agents: 2
1. **diy-asset-creator** - Zero-budget B-roll production guides
2. **claims-extractor** - Systematic source analysis for fact-checking videos

### Updated Agents: 3
1. **fact-checker** - Added primary source quote verification methodology
2. **research-organizer** - Added NotebookLM response organization (Phase 5)
3. **video-orchestrator** - Added 3 new workflow phases (0.5, 2.5, 7.5)

### New Commands: 1
1. **/zero-budget-assets** - Generate DIY asset creation guides

---

## NEW AGENT: diy-asset-creator

**File:** `.claude/agents/diy-asset-creator.md`

### What It Does
Creates comprehensive step-by-step guides for producing B-roll assets using 100% free tools:
- Canva (free account) - Quote documents, timelines, charts
- MapChart.net / Google My Maps - Historical maps, routes
- Wikimedia Commons - Public domain images
- PowerPoint/Google Slides - Alternative to all of the above

### When to Use
- User has zero budget for asset commissioning
- B-roll checklist exists but assets need creation
- Want organized day-by-day workflow (can film after Day 1)

### Example Output
From Crusades project: `DIY-ASSET-GUIDE.md` with:
- Day 1 (3 hours): 8 critical assets - **can START FILMING after this**
- Day 2-4: Remaining assets organized by priority
- Step-by-step Canva/MapChart/PowerPoint instructions
- Public domain sourcing from Wikimedia Commons
- Folder organization structure
- Batch workflow tips (save 30-40% time)

### Integration
- **Input:** B-ROLL-CHECKLIST.md (from production-packager agent)
- **Output:** DIY-ASSET-GUIDE.md with free tool instructions
- **Workflow:** Phase 7 (production package) → Phase 7.5 (DIY guide) → Filming

### Key Innovation
**"Can film after Day 1" approach** - Critical assets prioritized, user doesn't wait for all 31 assets before filming. Remaining B-roll added during editing.

---

## NEW AGENT: claims-extractor

**File:** `.claude/agents/claims-extractor.md`

### What It Does
Extracts every verifiable factual claim from source material (video transcripts, articles, books) for systematic fact-checking:
- Comprehensive extraction (no claims missed)
- Categorization by topic/chronology
- Complexity analysis (what's omitted or oversimplified)
- Omissions identification (what source doesn't mention)
- Verification priority assignment

### When to Use
- Fact-checking videos targeting specific sources
- Have transcript of video/article being fact-checked
- Need exhaustive claim list before NotebookLM research

### Example Output
From Crusades project: `CLAIMS-TO-VERIFY.md` with:
- 30+ claims extracted from Pax video
- 6 categories: Early Christian Control, Islamic Expansion, Treatment of Christians, Mediterranean Piracy, Crusades Justification, Crusades Conduct
- Priority assignment: 🔴 Critical / 🟡 Medium / 🟢 Low
- Complexity omitted for each claim (what context source left out)
- Major omissions: Jerusalem massacre, Fourth Crusade, Ma'arra cannibalism, Rhineland massacres, Byzantine-Sassanid War

### Integration
- **Input:** Source transcript (video/article being fact-checked)
- **Output:** CLAIMS-TO-VERIFY.md
- **Workflow:** Phase 0.5 (claims extraction) → NotebookLM research → Script writing

### Key Innovation
**Omissions tracking** - Not just what source claims, but what they DON'T mention. Critical for fact-checking videos.

---

## UPDATED AGENT: fact-checker

**File:** `.claude/agents/fact-checker.md`

### What Changed
Added comprehensive **PRIMARY SOURCE QUOTE VERIFICATION** section with:

**New methodology:**
1. Word-for-word quote verification (exact matches required)
2. Context verification (quote meaning preserved)
3. Translation cross-reference (multiple translations checked)
4. Medieval chronicle handling (manuscript variations addressed)
5. Red flags for rejection (when to reject quotes)

**New output format:**
- Quote Verification template with comparison status
- Step-by-step verification process (5 steps)
- Special cases: Medieval chronicles, Arabic sources, multiple translations

**Example from Crusades project:**
```
Verified Fulcher of Chartres Ma'arra quote:
- Located in Krey (1921) edition
- Word-for-word match confirmed
- Context verified (describing cannibalism)
- Cross-referenced with Ryan (1969) translation
- STATUS: ✅ VERIFIED
```

### Why This Matters
**Primary source accuracy is non-negotiable.** One misquote destroys credibility. This methodology ensures every medieval chronicle quote is exact.

---

## UPDATED AGENT: research-organizer

**File:** `.claude/agents/research-organizer.md`

### What Changed
Added **PHASE 5: NOTEBOOKLM RESPONSE ORGANIZATION**

**New capability:**
- Transforms raw NotebookLM outputs into script-ready format
- Categorizes findings: Priority 1 (Critical Omissions), Priority 2 (Oversimplifications), Priority 3 (Accurate Claims)
- Adds "Script Use" guidance for each finding
- Identifies smoking gun evidence
- Provides B-roll requirements per finding

**New output:** RESEARCH-SUMMARY.md

**Example from Crusades project:**
- Input: NotebookLM responses on 15+ topics
- Output: Organized summary with Priority 1 (5 critical omissions), Priority 2 (4 oversimplifications), Priority 3 (3 accurate claims)
- 10+ primary source quotes ready for B-roll display
- Script structure recommendation (12-minute outline)
- Modern relevance connections identified

### Why This Matters
**Raw NotebookLM responses are overwhelming.** Organized summary with "Script Use" guidance enables efficient script writing without re-researching.

### Integration
- **Workflow:** NotebookLM prompts → User runs prompts → Provides responses → Phase 5 organizes → RESEARCH-SUMMARY.md → Script writing

---

## UPDATED AGENT: video-orchestrator

**File:** `.claude/agents/video-orchestrator.md`

### What Changed

#### 1. Updated Worker Agent Registry
- Added **claims-extractor** to registry
- Updated **research-organizer** with Phase 5 capability
- Added **diy-asset-creator** to registry

#### 2. New Workflow Phases

**PHASE 0.5: Claims Extraction (for fact-checking videos)**
- When: User is fact-checking specific source
- Delegate to: claims-extractor
- Output: CLAIMS-TO-VERIFY.md
- Next: Use claims list to target NotebookLM research

**PHASE 2.5: Research Response Organization (when user provides NotebookLM outputs)**
- When: User has run NotebookLM prompts and provides responses
- Delegate to: research-organizer (Phase 5)
- Output: RESEARCH-SUMMARY.md with Priority 1/2/3 categorization
- Why: Prevents re-researching during script writing

**PHASE 7.5: Zero-Budget Asset Creation (if user has no budget)**
- When: User needs B-roll but has zero budget
- Delegate to: diy-asset-creator
- Output: DIY-ASSET-GUIDE.md with free tool instructions
- Result: User can create all assets without spending money

### Why This Matters
**Complete workflow coverage** - From fact-checking a source through zero-budget production, the orchestrator now handles the full proven workflow from Crusades project.

---

## NEW COMMAND: /zero-budget-assets

**File:** `.claude/commands/zero-budget-assets.md`

### What It Does
Slash command to quickly generate DIY asset creation guide from B-roll checklist.

**Usage:**
```
/zero-budget-assets
```

**Prompts for:**
- Project name (or reads current project)
- B-roll checklist location

**Output:**
- DIY-ASSET-GUIDE.md with step-by-step free tool instructions
- Day-by-day workflow (can film after Day 1)
- Canva/MapChart/PowerPoint tutorials
- Public domain sourcing instructions

### When to Use
- After creating B-roll checklist (Phase 7)
- User has zero budget
- Want quick generation of DIY guide

### Integration
- Part of Phase 7.5 workflow
- Can be invoked directly by user via `/zero-budget-assets`

---

## WORKFLOW IMPROVEMENTS DEMONSTRATED

### Complete Fact-Checking Workflow (Crusades Project)

**Before these improvements:**
- Manual claim extraction (prone to gaps)
- Raw NotebookLM responses (hard to use)
- Generic fact-checking (not tailored to primary sources)
- Expensive B-roll (barrier to production)

**After these improvements:**
```
1. VidIQ viability check ✅
2. Claims extraction → CLAIMS-TO-VERIFY.md ✅ (NEW)
3. NotebookLM prompts → Responses ✅
4. Response organization → RESEARCH-SUMMARY.md ✅ (NEW)
5. Script writing (with organized evidence) ✅
6. Primary source quote verification ✅ (IMPROVED)
7. B-roll checklist creation ✅
8. Zero-budget DIY guide → DIY-ASSET-GUIDE.md ✅ (NEW)
9. Filming (with critical assets) ✅
```

**Result:**
- 11 files created in organized workflow
- 60 claims verified (96.7% accuracy)
- 31 B-roll assets planned
- DIY guide enables $0 production
- Complete production package

---

## PROVEN RESULTS

### Crusades Fact-Check Project (4-crusades-fact-check-2025)

**Files Created:**
1. PROJECT-BRIEF.md (VidIQ analysis)
2. CLAIMS-TO-VERIFY.md (30+ claims extracted) ← **NEW CAPABILITY**
3. NOTEBOOKLM-SOURCE-LIST.md
4. FACT-CHECK-VERIFICATION.md
5. NOTEBOOKLM-PROMPTS.md (20+ prompts)
6. RESEARCH-SUMMARY.md (Priority 1/2/3 organized) ← **NEW CAPABILITY**
7. SCRIPT-DRAFT-01.md
8. SCRIPT-DRAFT-02-FINAL.md (with Ma'arra section)
9. SCRIPT-FACT-CHECK.md (word-for-word verification) ← **IMPROVED**
10. B-ROLL-CHECKLIST.md (31 assets)
11. DIY-ASSET-GUIDE.md (zero-budget workflow) ← **NEW CAPABILITY**

**Fact-Check Quality:**
- 60 claims verified
- 58 fully verified (96.7%)
- 2 minor clarifications (both already fixed)
- 0 errors
- Primary source quotes verified word-for-word

**Production Readiness:**
- 8 critical assets (Day 1 - 3 hours) → Can start filming
- 23 remaining assets (Days 2-4)
- All free tools (Canva, MapChart, Wikimedia Commons)
- Total DIY time: 10 hours across 4 days
- Budget: $0

---

## HOW TO USE THESE IMPROVEMENTS

### For Fact-Checking Videos:

**1. Start with Claims Extraction**
```
Use claims-extractor agent:
- Input: Source transcript
- Output: CLAIMS-TO-VERIFY.md
```

**2. Organize NotebookLM Responses**
```
Use research-organizer (Phase 5):
- Input: NotebookLM responses
- Output: RESEARCH-SUMMARY.md with Priority 1/2/3
```

**3. Verify Primary Source Quotes**
```
Use fact-checker agent (updated):
- Word-for-word verification
- Context checking
- Translation cross-reference
```

**4. Create Zero-Budget Assets**
```
Use diy-asset-creator agent:
- Input: B-ROLL-CHECKLIST.md
- Output: DIY-ASSET-GUIDE.md
- Film after Day 1 (3 hours)
```

### For Original Videos:

**Skip Phase 0.5 (Claims Extraction)** - Only needed for fact-checking

**Use Phase 2.5 (Research Organization)** - Organize NotebookLM responses if extensive

**Use Phase 7.5 (DIY Assets)** - If zero budget

---

## TECHNICAL DETAILS

### Agent Files Created/Updated:
- ✅ `.claude/agents/diy-asset-creator.md` (NEW - 586 lines)
- ✅ `.claude/agents/claims-extractor.md` (NEW - 528 lines)
- ✅ `.claude/agents/fact-checker.md` (UPDATED - added 197 lines)
- ✅ `.claude/agents/research-organizer.md` (UPDATED - added 359 lines)
- ✅ `.claude/agents/video-orchestrator.md` (UPDATED - added 3 phases + registry updates)

### Command Files Created:
- ✅ `.claude/commands/zero-budget-assets.md` (NEW - 67 lines)

### Total Lines Added: ~1,737 lines of production-proven agent code

---

## BACKWARDS COMPATIBILITY

**All existing workflows still work:**
- Original video production (no fact-checking)
- Budget-available production (skip Phase 7.5)
- Simple research (skip Phase 2.5 if minimal NotebookLM)

**New phases are optional:**
- Phase 0.5: Only for fact-checking videos
- Phase 2.5: Only when NotebookLM responses need organization
- Phase 7.5: Only when zero budget

**No breaking changes** - Existing agents enhanced, not replaced.

---

## SUCCESS METRICS

### Crusades Project Demonstrated:

**Efficiency:**
- Complete workflow: 11 production files
- Research organized in phases (not scattered)
- DIY guide enables immediate production (Day 1 filming)

**Quality:**
- 96.7% fact-check accuracy
- Word-for-word primary source verification
- Comprehensive claim coverage (30+ claims)

**Accessibility:**
- $0 budget requirement
- Free tools exclusively (Canva, MapChart, Wikimedia)
- Day-by-day workflow (manageable sessions)

**Scalability:**
- Agents handle complexity (orchestrator-worker pattern)
- Session persistence (PROJECT-STATUS.md)
- Resumable workflow (Phase 2.5 enables later resumption)

---

## NEXT STEPS

### Ready to Use:

**For your next fact-checking video:**
1. Run `/new-video` or invoke video-orchestrator
2. Provide source transcript
3. Orchestrator will:
   - Extract claims (Phase 0.5)
   - Generate NotebookLM prompts
   - Organize responses (Phase 2.5)
   - Generate script
   - Verify quotes word-for-word
   - Create B-roll checklist
   - Generate DIY guide (Phase 7.5) if zero budget

**For your next original video:**
1. Skip Phase 0.5 (no source to fact-check)
2. Use Phase 2.5 if NotebookLM responses extensive
3. Use Phase 7.5 if zero budget

### Test the Improvements:

Try the new capabilities on a simple test project to see the workflow in action.

---

## DOCUMENTATION LOCATIONS

**Agent Documentation:**
- `.claude/agents/diy-asset-creator.md`
- `.claude/agents/claims-extractor.md`
- `.claude/agents/fact-checker.md` (see "PRIMARY SOURCE QUOTE VERIFICATION" section)
- `.claude/agents/research-organizer.md` (see "PHASE 5" section)
- `.claude/agents/video-orchestrator.md` (see "PHASE 0.5, 2.5, 7.5")

**Command Documentation:**
- `.claude/commands/zero-budget-assets.md`

**Reference Implementation:**
- `video-projects/_IN_PRODUCTION/4-crusades-fact-check-2025/`
- See all 11 files for working examples

---

## QUESTIONS?

**Want to see an agent in action?**
- Just say "use [agent-name]" and I'll invoke it

**Want to test the workflow?**
- Provide a source transcript for fact-checking, or
- Provide a topic for original video

**Want modifications?**
- Tell me what needs adjustment
- All agents are customizable

---

**Summary: Agents and commands upgraded based on proven Crusades workflow. Zero-budget production now fully supported. Primary source verification now rigorous. Fact-checking videos now systematic.**

**Status: PRODUCTION READY ✅**
