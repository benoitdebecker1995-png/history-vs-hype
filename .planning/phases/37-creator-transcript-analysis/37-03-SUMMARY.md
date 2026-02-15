---
phase: 37-creator-transcript-analysis
plan: 03
subsystem: Script-Writer Integration
tags: [agent-integration, workflow-automation, creator-techniques, part8-application]
dependency_graph:
  requires: [Plan 37-02 Part 8 generation, STYLE-GUIDE.md Part 8, script-writer-v2 agent]
  provides: [Rule 17 technique application, /script Part 8 integration, creator technique workflow]
  affects: [Script generation workflow, /script command, script-writer-v2 behavior]
tech_stack:
  added: [Agent rule framework, command documentation]
  patterns: [Rule-based agent behavior, optional technique application, graceful fallback]
key_files:
  modified:
    - .claude/agents/script-writer-v2.md (+37 LOC - Rule 17)
    - .claude/commands/script.md (+4 LOC - Part 8 reference)
decisions:
  - "Rule 17 positioned after Rule 15 (retention playbook) and before REASONING FRAMEWORK"
  - "Part 8 techniques optional, not mandatory (graceful fallback to Parts 1-7)"
  - "HTML comments for technique tracking: <!-- Part 8.1: Visual Contrast Hook -->"
  - "Selection priority: creator_count → topic match → natural fit (no force-fitting)"
  - "Part 8 cross-referenced with Part 6 to avoid duplication"
  - "Pattern synthesizer update command documented in /script reference"
metrics:
  duration_minutes: 3
  tasks_completed: 1
  files_modified: 2
  rules_added: 1
  completed_date: "2026-02-15"
---

# Phase 37 Plan 03: Script-Writer Integration Summary

**One-liner:** Rule 17 wires Part 8 creator technique library into script-writer-v2 with optional application and graceful fallback to core principles.

## What Was Built

### Rule 17: Creator Technique Library (script-writer-v2.md)
**Purpose:** Enable script-writer-v2 agent to leverage Part 8 creator-validated techniques during script generation.

**Location:** Added after Rule 15 (Retention Playbook) at line 537, before REASONING FRAMEWORK section.

**Core capabilities:**

1. **Part 8 Section Reference:**
   - 8.1: Opening hooks (visual contrast, fact-check declaration, escalation timeline, question hooks)
   - 8.2: Transitions (causal chains, temporal jumps, pivots, contrast shifts)
   - 8.3: Evidence presentation (direct quotes, source citations, document reveals)
   - 8.4: Pacing & rhythm (question density, paragraph length variation)
   - 8.5: Part 6 cross-references (maps Part 8 examples to existing Part 6 patterns)

2. **Application Workflow:**
   ```
   Step 1: Identify section type (intro, transition, evidence, conclusion)
   Step 2: Check Part 8 for matching techniques
   Step 3: Select 1-2 relevant techniques
   Step 4: If Part 6 cross-ref exists, check Part 6 for core pattern
   Step 5: Adapt formula to current topic
   Step 6: Add HTML comment: <!-- Part 8.1: Visual Contrast Hook -->
   ```

3. **Selection Priority:**
   - Highest `creator_count` first (most validated across creators)
   - Topic match (territorial → map hooks, ideological → fact-check hooks)
   - Natural fit (do NOT force-fit when no technique applies)

4. **Example Application (Territorial Dispute Opening):**
   - Section type: intro
   - Topic: territorial
   - Part 8.1 match: Visual Contrast Hook (Kraut, History vs Hype, RealLifeLore)
   - Formula: [Show visual A] → [Show visual B] → [State tension]
   - Applied: "Open a map of [region], you see [Country A]. Now open [Country B]'s map. [Territory] disappears."

5. **Relationship to Other Rules:**
   - **Rule 14 (Part 6):** Core voice patterns — use ALWAYS
   - **Rule 15 (Part 9):** Retention playbook — use ALWAYS
   - **Rule 17 (Part 8):** Creator techniques — use when relevant, skip when forced

**Key design decision:** Part 8 techniques are OPTIONAL. If no technique naturally fits, agent falls back to Parts 1-7 core principles. This prevents force-fitting patterns that don't serve the script.

### /script Command Updates (.claude/commands/script.md)
**Purpose:** Document Part 8 availability and update workflow in user-facing command.

**Changes:**

1. **STYLE-GUIDE.md Reference Expanded:**
   - Added Part 6, 8, 9 breakdown with descriptions
   - Part 6: Voice patterns (proven History vs Hype patterns)
   - Part 8: Creator technique library (cross-validated from 80+ transcripts)
   - Part 9: Retention playbook (data-driven retention rules)

2. **Update Command Documented:**
   - `python tools/youtube-analytics/pattern_synthesizer_v2.py --update` for Part 8
   - `python tools/youtube-analytics/playbook_synthesizer.py --update` for Part 9
   - Users can regenerate sections after adding transcripts or performance data

3. **Reference Files Section:**
   - Part 8 positioned alongside Parts 6 and 9 in workflow documentation
   - Auto-update capability highlighted for both synthesizers

## Deviations from Plan

None. Plan executed exactly as written.

## Verification Results

### Task 1 Verification

```bash
# 1. Rule 17 exists
$ grep -c "RULE 17" .claude/agents/script-writer-v2.md
1

# 2. Part 8 referenced in script command
$ grep -c "Part 8" .claude/commands/script.md
1

# 3. Existing Rules 14-15 unchanged
$ grep "RULE 1[45]" .claude/agents/script-writer-v2.md
### RULE 14: VOICE PATTERN APPLICATION (Added 2026-02-10)
### RULE 15: RETENTION PLAYBOOK APPLICATION
```

All checks passed. Rule 17 added successfully without modifying existing rules.

## Technical Decisions

### 1. Rule 17 Positioning After Rule 15
**Decision:** Placed Rule 17 immediately after Rule 15 (Retention Playbook) and before REASONING FRAMEWORK section.

**Reasoning:**
- Logical grouping: Rules 14-17 all reference STYLE-GUIDE.md sections (Parts 6, 9, 8)
- Reading order: Part 6 (core patterns) → Part 9 (retention data) → Part 8 (creator examples)
- Rule 16 reserved for Phase 38 (adaptive scriptwriter intelligence)

**Alternative considered:** Place after Rule 14 (rejected - breaks Part 6 → Part 9 → Part 8 flow).

### 2. Optional Technique Application (Not Mandatory)
**Decision:** Part 8 techniques are optional. Agent can skip when no technique naturally fits.

**Reasoning:**
- Part 8 contains examples, not rules (unlike Part 6 core patterns)
- Force-fitting techniques degrades script quality
- Fallback to Parts 1-7 ensures script always has foundation
- Creator techniques supplement, don't replace, core principles

**Implementation:** "If no Part 8 technique naturally fits, use Parts 1-7 core principles (do NOT force-fit)"

**Trade-off:** Reduces Part 8 usage in early adoption, but ensures quality over quantity.

### 3. HTML Comment Tracking
**Decision:** Add HTML comments to mark technique source: `<!-- Part 8.1: Visual Contrast Hook -->`

**Reasoning:**
- Enables post-generation analysis (which techniques were used)
- Allows user to verify technique application
- Supports future analytics on technique effectiveness
- Non-intrusive (comments don't appear in final output)

**Alternative considered:** Metadata section in script frontmatter (rejected - less granular, harder to track per-section).

### 4. Selection Priority by creator_count
**Decision:** Prioritize techniques by `creator_count` (how many creators use it).

**Reasoning:**
- 3+ creators = universal pattern (cross-validated)
- Higher count = more proven across different styles
- Reduces risk of idiosyncratic patterns from single creator
- Aligns with Part 8 synthesis threshold (3+ creators)

**Implementation:** "Part 8 techniques with highest creator_count first (most validated)"

### 5. Part 6 Cross-Reference Integration
**Decision:** When Part 8 technique has Part 6 cross-reference, check both sections.

**Reasoning:**
- Part 6 contains the core pattern definition
- Part 8 provides creator-validated examples
- Cross-referencing ensures agent understands both theory and practice
- Prevents applying examples without understanding underlying pattern

**Example:** Visual Contrast Hook in Part 8.1 cross-references Part 6.1 Visual Contrast Hook pattern.

### 6. Pattern Synthesizer Update Command in /script Docs
**Decision:** Document pattern_synthesizer_v2.py update command in /script workflow.

**Reasoning:**
- Users need to know Part 8 is auto-generated (not static)
- Update command allows refreshing after adding transcripts
- Aligns with playbook_synthesizer.py pattern (Part 9 updates)
- Encourages iterative improvement of technique library

**Location:** Reference files section, alongside STYLE-GUIDE.md reference.

## Integration Points

### Data Flow:
1. **transcript_analyzer.py** → Analyzes 83 transcripts → Extracts patterns
2. **technique_library.py** → Stores patterns in keywords.db → Returns technique counts
3. **pattern_synthesizer_v2.py** → Synthesizes universal patterns → Generates Part 8 markdown
4. **STYLE-GUIDE.md Part 8** → Written at line 1077 → Auto-updated with `--update`
5. **script-writer-v2 Rule 17** → Reads Part 8 → Applies techniques during generation
6. **script.md /script command** → Documents Part 8 → Users know how to refresh

### Rule Integration:
- **Rule 14 (Part 6):** Core voice patterns — ALWAYS apply
- **Rule 15 (Part 9):** Retention playbook — ALWAYS apply
- **Rule 17 (Part 8):** Creator techniques — OPTIONAL application

Rule 17 sits alongside Rules 14-15 as the third STYLE-GUIDE.md reference rule, completing the trinity:
- Part 6 = proven channel patterns
- Part 9 = data-driven retention lessons
- Part 8 = cross-creator validation

### Workflow Integration:

**Before script generation:**
1. Read STYLE-GUIDE.md (includes Parts 6, 8, 9)
2. Surface pre-script insights (from feedback_queries.py)
3. Determine topic type (territorial, ideological, etc.)

**During script generation:**
1. Apply Rule 14 (Part 6 voice patterns) — mandatory
2. Apply Rule 15 (Part 9 retention rules) — mandatory
3. Apply Rule 17 (Part 8 creator techniques) — when relevant

**After script generation:**
1. Run retention_scorer.py (identify high-risk sections)
2. Display retention warnings to user
3. Suggest revisions before filming

## Known Limitations

1. **No Automatic Technique Selection:**
   - Agent manually selects techniques per section
   - Could be automated with section type classification
   - Future: Auto-suggest techniques based on section_type field

2. **No Technique Effectiveness Tracking:**
   - HTML comments mark technique usage
   - No automatic correlation with retention data yet
   - Future: Track which Part 8 techniques correlate with high retention

3. **Limited Topic Type Matching:**
   - Topic matching relies on manual classification (territorial, ideological)
   - No semantic matching between technique and topic
   - Future: NLP-based technique recommendation

4. **No Pattern Conflict Detection:**
   - If Part 6 and Part 8 patterns conflict, agent decides manually
   - No automated conflict resolution
   - Mitigation: Part 8.5 cross-references flag overlaps

5. **Creator Count Threshold Fixed at 3:**
   - Threshold doesn't adapt to corpus size
   - 3 creators from 11 (27%) vs. 3 from 50 (6%) have different confidence
   - Future: Dynamic threshold based on total creator count

## Next Steps

**Phase 38 (Adaptive Scriptwriter Intelligence):**
- Context-aware technique recommendations (auto-select based on section type)
- Script comparison against creator baselines (pattern density analysis)
- Improvement suggestions: "Consider using causal_chain transitions (9 creators use this)"
- Technique effectiveness ranking (combine creator_count + retention data)

**Potential Enhancements:**
- Auto-select techniques by section type (intro → opening hooks, body → transitions)
- Track technique effectiveness (correlate HTML comments with retention drops)
- Dynamic creator count threshold (scale with corpus size)
- Semantic similarity matching (beyond regex pattern matching)
- Technique conflict detection (warn when Part 6 and Part 8 overlap)

## Self-Check

### Files modified:
```bash
$ ls -lh .claude/agents/script-writer-v2.md
-rw-r--r-- 1 user user 61K Feb 15 01:50 .claude/agents/script-writer-v2.md

$ ls -lh .claude/commands/script.md
-rw-r--r-- 1 user user 19K Feb 15 01:50 .claude/commands/script.md
```

### Commit exists:
```bash
$ git log --oneline --all | grep "37-03"
cddc2f6 feat(37-03): wire Part 8 creator techniques into script generation workflow
```

### Rule 17 verification:
```bash
$ grep "### RULE 17" .claude/agents/script-writer-v2.md
### RULE 17: CREATOR TECHNIQUE LIBRARY (Added 2026-02-14)

$ grep "Part 8" .claude/agents/script-writer-v2.md | head -3
**Before writing each section, consult STYLE-GUIDE.md Part 8 for creator-validated techniques.**
Part 8 contains structural techniques extracted from 80+ creator transcripts and validated across 3+ successful creators:
- **Part 8.1:** Opening hooks (visual contrast, fact-check declaration, escalation timeline, question hooks)
```

### Part 8 reference in command:
```bash
$ grep "Part 8" .claude/commands/script.md
  - **Part 8:** Creator technique library (cross-validated patterns from 80+ transcripts) — auto-updated with `python tools/youtube-analytics/pattern_synthesizer_v2.py --update`
```

## Self-Check: PASSED

All files modified, commit verified, Rule 17 added successfully, Part 8 referenced in command documentation.

---

**Completion time:** 3 minutes
**Commit:** cddc2f6
**Status:** ✅ Complete - Phase 37 Complete (All 3 plans shipped)
