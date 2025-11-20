# Agent Update Plan - January 2025

**Reason:** New performance analysis shows 6-8 min videos outperform 10-12 min (JD Vance: 11.21% CTR, 42.6% retention at 6:16)

**New approach:** Experimentation framework over formula repetition, with travel/improvised production support

---

## UPDATES REQUIRED

### 1. script-writer-v2.md - CRITICAL
**Current:** Targets 8-9 minutes
**Update to:**
- **Default:** 6-8 minutes (650-880 words @ 110 wpm)
- **Optional:** 8-9 minutes for complex topics
- **Travel mode:** Key points format (250 words written + improvisation)

**Changes needed:**
- Line 22: "Create 6-8 minute educational scripts..." (default)
- Line 46: "Planning retention engineering across 6-8 minute scripts"
- Line 613: "PHASE 3: SCRIPT STRUCTURE (6-8 MINUTES)"
- Add: TRAVEL MODE option (key points only, not full script)
- Add: Reference to performance-analyzer insights

---

### 2. video-orchestrator.md - CRITICAL
**Current:** No performance analysis integration, no experimentation framework
**Update to:**
- Add `performance-analyzer` to worker registry
- Add experimentation workflow (score topics before production)
- Add travel mode coordination
- Update length expectations

**Changes needed:**
- Worker registry: Add performance-analyzer agent description
- Phase 0 (NEW): Topic validation using scorecard (before research)
- Phase 1: Research integrates with topic testing
- Phase 2: Script writer uses performance insights
- Monitor: 650-880 words (6-8 min) default, 850-1000 optional

---

### 3. research-organizer.md - MEDIUM
**Current:** Target length (8-12 minutes)
**Update to:**
- Target length (6-8 minutes default, 8-10 optional)
- Add topic testing scorecard reference
- Add experimentation value assessment

**Changes needed:**
- Line 36: "Target length (6-8 minutes)"
- Add: Topic testing scorecard integration
- Add: Novelty assessment (has this angle been tested?)

---

### 4. structure-checker-v2.md - LOW
**Current:** Expects 8-9 minutes
**Update to:**
- Check for 6-8 min default
- Validate against JD Vance retention pattern
- Flag if >8 min without justification

**Changes needed:**
- Line 137: "Length: [X minutes] (Expected: 6-8 minutes, 8-10 for complex topics)"
- Add: JD Vance benchmark comparison (11.21% CTR, 42.6% retention)

---

### 5. vidiq-optimizer.md - LOW
**Current:** Works but doesn't reference new defaults
**Update to:**
- Note 6-8 min as compression target
- Reference JD Vance efficiency metrics

**Changes needed:**
- Compression recommendations: Target 6-8 min (not 10-12)
- Add: JD Vance case study as optimization benchmark

---

## NEW INTEGRATIONS NEEDED

### Integration 1: performance-analyzer → research-organizer
**Flow:**
- Research-organizer checks: "Has this topic type been tested?"
- If tested: Reference performance-analyzer patterns
- If untested: Flag as high experimentation value

**Implementation:**
- Research-organizer reads: `video-projects/_ANALYTICS/TOPIC-TESTING-SCORECARD.md`
- Scores topic using scorecard framework
- Outputs: Experimentation score + expected performance range

---

### Integration 2: performance-analyzer → script-writer-v2
**Flow:**
- Script-writer checks similar tested topics
- Adapts length/structure based on performance data
- Example: "Political fact-check detected → Use JD Vance 6-min format"

**Implementation:**
- Script-writer reads: `video-projects/_ANALYTICS/LENGTH-PERFORMANCE-ANALYSIS.md`
- Applies validated patterns (territorial disputes, fact-checks)
- Justifies length choice based on data

---

### Integration 3: topic-testing-scorecard → video-orchestrator
**Flow:**
- Phase 0 (NEW): Orchestrator scores topic before delegating research
- Only proceeds if score >60 (YELLOW LIGHT minimum)
- Recommends redesign if <60

**Implementation:**
- Orchestrator uses scorecard template
- Scores: Experimentation (40) + Breakout (30) + Risk (30) = 100
- Decision: GREEN (80+) / YELLOW (60-79) / RED (<60)

---

## TRAVEL MODE ADDITIONS

### script-writer-v2.md
**Add new mode:** "Travel/Improvised Production"

**When activated:**
- Output: Key points format (not full script)
- Structure: 250 words written + improvisation guidance
- Quotes: On cards (verbatim reading)
- Target: 6-8 minutes
- Example: TRAVEL-VERSION-KEY-POINTS.md (Crusades)

---

### video-orchestrator.md
**Add travel workflow:**

**Phase 2a: Travel Script Mode**
- Delegates to script-writer-v2 with `mode: travel`
- Outputs: Key points, quote cards, timing checkpoints
- Skips: Full script development, detailed B-roll cues
- Focuses: Accuracy of quotes, structure clarity

---

## PRIORITY ORDER

### Immediate (Before next video):
1. ✅ Create performance-analyzer.md (DONE)
2. ✅ Create topic-testing-scorecard.md (DONE)
3. ✅ Create travel-version template (DONE - Crusades example)
4. ⏳ Update script-writer-v2.md (6-8 min default, travel mode)
5. ⏳ Update video-orchestrator.md (add performance-analyzer, Phase 0 scoring)

### Soon (Before traveling):
6. ⏳ Update research-organizer.md (topic scoring integration)
7. ⏳ Update structure-checker-v2.md (6-8 min expectations)

### Later (After travel test):
8. ⏳ Update vidiq-optimizer.md (6-8 min compression targets)
9. ⏳ Create workflow examples with new integrations

---

## BACKWARD COMPATIBILITY

**Question:** Should we keep 8-9 min option?

**Answer:** YES - Make it optional, not removed

**Rationale:**
- Some topics need deeper explanation
- Complex historical events (Israel-Palestine 11:58 got 586 views)
- User preference for specific videos

**Implementation:**
- Default: 6-8 min (based on JD Vance performance)
- Optional flag: `length: extended` → 8-10 min
- User can override: "Make this one 10 minutes"

---

## VALIDATION AFTER UPDATES

### Test workflow:
1. User says: "New video idea: [topic]"
2. Orchestrator scores with topic-testing-scorecard
3. If GREEN: Delegate to research-organizer
4. Research-organizer checks performance-analyzer for similar topics
5. Script-writer-v2 defaults to 6-8 min (unless user specifies longer)
6. Structure-checker validates against 6-8 min target
7. Output: Optimized for engagement, validated by data

### Test travel mode:
1. User says: "Crusades video, travel mode"
2. Orchestrator delegates to script-writer-v2 with `mode: travel`
3. Script-writer outputs key points format
4. Structure-checker validates structure (looser requirements)
5. Output: Filming guide, not full script

---

## FILES TO UPDATE

### Critical Updates (Do Now):
1. `.claude/agents/script-writer-v2.md`
2. `.claude/agents/video-orchestrator.md`

### Medium Priority:
3. `.claude/agents/research-organizer.md`
4. `.claude/agents/structure-checker-v2.md`

### Low Priority:
5. `.claude/agents/vidiq-optimizer.md`
6. `.claude/agents/script-writer.md` (legacy agent, less critical)

### Documentation Updates:
7. `CLAUDE.md` - Update target length from 8-12 min → 6-8 min
8. `START-HERE.md` - Reference new analytics files
9. `.claude/README.md` - Note performance-analyzer integration

---

## ESTIMATED TIME

**Agent updates:** 2-3 hours total
- script-writer-v2: 45 min
- video-orchestrator: 1 hour
- research-organizer: 30 min
- structure-checker-v2: 20 min
- vidiq-optimizer: 15 min
- documentation: 30 min

**Testing:** 1 hour
- Run through workflow with Crusades video
- Validate integrations work
- Check backward compatibility

**Total: 3-4 hours before travel**

---

## DECISION POINT

**Do you want me to:**

**A)** Update all critical agents now (script-writer-v2, video-orchestrator) before you travel

**B)** Just update script-writer-v2 for travel mode (minimum viable)

**C)** Review/approve the update plan first, then I'll execute

**My recommendation:** Option A
- 2-3 hours of updates
- Gets full integration working
- You have performance-driven workflow before traveling
- Crusades video uses optimized system

**Minimum (Option B):**
- 45 min update to script-writer-v2 only
- Add travel mode
- Change default to 6-8 min
- Other agents stay as-is (manual override)

Your call?
