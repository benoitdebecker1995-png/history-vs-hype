# Phase 38 Plan 02: Variant Generation Summary

**One-liner:** Rule 16 in script-writer-v2 agent + --variants flag in /script command enables pre-script hook/structure variant generation with choice logging.

---

## Frontmatter

```yaml
phase: 38-structured-choice-architecture
plan: 02
subsystem: choice-architecture
tags: [script-workflow, agent-extension, variant-generation, cli]
completed: 2026-02-15

dependency_graph:
  requires:
    - phase: 38
      plan: 01
      artifact: technique_library.py (log_choice, get_recommendation, get_choice_summary_for_topic)
  provides:
    - artifact: script-writer-v2 Rule 16
      for: [user /script workflow]
    - artifact: /script --variants flag
      for: [user pre-script choices]
  affects:
    - component: .claude/agents/script-writer-v2.md
      impact: "Added Rule 16 (42 lines) for variant generation workflow"
    - component: .claude/commands/script.md
      impact: "Added --variants flag and VARIANT GENERATION section"

tech_stack:
  added: []
  patterns:
    - Sequential choice flow (hooks first, then structure)
    - Footnote-style technique attribution
    - Silent choice logging (no user confirmation)
    - Invisible friction pattern (skip "no data yet" messages)

key_files:
  created: []
  modified:
    - path: .claude/agents/script-writer-v2.md
      changes: "+42 lines (Rule 16 between Rules 15 and 17)"
      commit: 1e11c15
    - path: .claude/commands/script.md
      changes: "+29 lines (--variants flag, VARIANT GENERATION section, PRE-SCRIPT INTELLIGENCE update)"
      commit: 49fce11

decisions:
  - choice: "Sequential choice flow (hooks → structure, not parallel)"
    rationale: "Hooks set video tone, structure builds on chosen hook. Sequential prevents mismatched combinations."
    alternatives: ["Parallel selection (user picks both simultaneously)", "Structure-first flow"]
  - choice: "Footnote-style attribution (_Uses [technique] (Part 8.1)_)"
    rationale: "Unobtrusive, educational, doesn't interrupt variant text flow"
    alternatives: ["Inline attribution", "Post-variant table", "No attribution"]
  - choice: "Silent choice logging (no confirmation message)"
    rationale: "Invisible friction - user doesn't need to acknowledge DB writes"
    alternatives: ["Confirmation message", "Option to disable logging"]
  - choice: "Skip 'no data yet' message when no patterns exist"
    rationale: "Invisible friction - empty state is silence, not noise"
    alternatives: ["Show 'building pattern history' message", "Show Part 8 fallback info"]

metrics:
  duration: "~7 minutes"
  tasks_completed: 2
  files_modified: 2
  loc_added: 71
  tests_run: 2 (Rule 16 placement verification, --variants flag count)
```

---

## What Was Built

### Rule 16: Variant Generation & Choice Architecture

Added to `.claude/agents/script-writer-v2.md` between Rules 15 (Retention Playbook) and 17 (Creator Technique Library).

**A. Hook Variant Generation (CHO-01):**
- Generate 2-3 opening hook variants using Part 8 techniques
- Different technique per variant (e.g., Visual Contrast Hook, Fact-Check Declaration, Escalation Timeline)
- Each variant: 100-200 words of actual hook text (not outline)
- Label: Hook A, Hook B, Hook C
- Footnote-style attribution below each hook: "_Uses [technique_name] (Part 8.1)_"
- If recommendation exists: display recommended variant first with "(Recommended - [reason])"
- Present ALL variants, wait for user to pick by letter (A/B/C)
- NEVER auto-skip variants (user always chooses)

**B. Structure Variant Generation (CHO-02):**
- After hook selection, generate 2 structural approaches
- Each approach: 3-5 sentence summary explaining approach FOR THIS SPECIFIC TOPIC
- Template format: "[Approach name]: [Opening] -> [Middle structure] -> [Ending]. [Key benefit]. [Key risk]."
- Label: Structure 1, Structure 2
- If recommendation exists: rank recommended first with rationale
- Wait for user to pick (1/2)

**C. Choice Logging (CHO-03):**
- After each choice, call `technique_library.py log_choice()` with:
  - choice_type ('opening_hook' or 'structural_approach')
  - project_path (current video project path)
  - topic_type (territorial/ideological/factcheck from research docs)
  - selected_variant, selected_technique, all_variants
  - recommended_technique (what was recommended, if any)
- Logging is silent - no confirmation message to user
- Enables pattern recognition after 5+ choices

**D. Pre-Generation Summary:**
- Before showing variants, call `get_choice_summary_for_topic(topic_type)`
- If patterns exist: display "Past patterns for [topic_type] topics: You chose [technique] [X/Y] times"
- If no patterns: skip entirely (don't show "no data yet" - invisible friction pattern)

**Activation:** Only when `--variants` flag is set. Without flag, Rule 16 skipped entirely and script written normally.

**Size:** 42 lines (under 60-line target from plan).

---

### /script --variants Flag

Added to `.claude/commands/script.md` with complete workflow documentation.

**1. Flag table entry:**
```
| `--variants` | Generate hook and structure variants before full script | `/script --variants 35-gibraltar-treaty-utrecht-2026` |
```

**2. Usage examples:**
- `/script --variants [project]` - Standalone variant generation
- `/script --new --variants [project]` - Combined new script + variants

**3. VARIANT GENERATION section:**
- **Flow:** Past choice patterns → Hook variants (A/B/C) → User picks → Structure variants (1/2) → User picks → Full script
- **Choice Logging:** Automatic database logging for pattern recognition
- **Review Past Choices:** CLI commands documented:
  - `python tools/youtube-analytics/technique_library.py --choices`
  - `python tools/youtube-analytics/technique_library.py --choices territorial`
  - `python tools/youtube-analytics/technique_library.py --choice-stats`

**4. PRE-SCRIPT INTELLIGENCE update:**
- Added bullet: "Past hook and structure choice patterns for this topic type (from variant history)"
- Surfaces alongside existing topic performance and retention lessons

---

## Deviations from Plan

None - plan executed exactly as written.

---

## Implementation Notes

### Design Decisions

**Why sequential choice flow (hooks → structure)?**
- Hooks establish video tone and approach
- Structure builds on chosen hook (e.g., Visual Contrast Hook → map-heavy structure)
- Prevents mismatched combinations (e.g., conversational hook + document-heavy structure)
- Clear progression: narrow down tone first, then build framework

**Why footnote-style attribution?**
- Unobtrusive - doesn't interrupt reading the hook text
- Educational - user learns which Part 8 technique is being demonstrated
- Maintains flow - variant text readable as continuous passage
- Format: `_Uses Visual Contrast Hook (Part 8.1)_` on line below hook

**Why silent choice logging?**
- Invisible friction principle from Plan 38-01
- User doesn't need to acknowledge DB writes (implementation detail)
- Confirmation messages add noise without value
- Logging happens automatically in background after user selects variant

**Why skip "no data yet" message?**
- Empty state for new users is silence, not explanation
- First-time users see variants immediately without preamble
- Pattern summary only appears when data exists (value-add, not noise)
- Prevents "we're learning about you" messaging that creates friction

### Integration Points

**From Plan 38-01:**
- `log_choice()` - stores user's hook/structure selections
- `get_recommendation()` - provides recommended variant based on past patterns
- `get_choice_summary_for_topic()` - surfaces "You chose X 4/5 times" summary

**For future usage:**
- User runs `/script --variants 35-gibraltar-treaty-utrecht-2026`
- Agent reads Rule 16, calls get_choice_summary_for_topic('territorial')
- Displays past patterns if >=1 choice exists for territorial
- Generates Hook A/B/C with Part 8 technique attributions
- User picks Hook B
- Agent calls log_choice('opening_hook', ..., selected='B')
- Agent generates Structure 1/2
- User picks Structure 1
- Agent calls log_choice('structural_approach', ..., selected='1')
- Agent proceeds with full script using selected hook + structure

### Edge Cases Handled

1. **First-time user (no patterns):** Pre-generation summary skipped silently
2. **--variants without --new:** Works standalone (variant generation only)
3. **--new without --variants:** Works as before (no Rule 16 activation)
4. **Combined flags:** `--new --variants` triggers Rule 16 before script generation
5. **No recommendation available:** All variants shown without recommended ranking

---

## Verification Results

### Rule 16 Placement
```bash
$ grep -c "RULE 16" .claude/agents/script-writer-v2.md
1

$ grep -n "^### RULE 1[567]:" .claude/agents/script-writer-v2.md
502:### RULE 15: RETENTION PLAYBOOK APPLICATION
538:### RULE 16: VARIANT GENERATION & CHOICE ARCHITECTURE (Added 2026-02-15)
580:### RULE 17: CREATOR TECHNIQUE LIBRARY (Added 2026-02-14)
```
✓ Rule 16 exists between Rules 15 and 17

### Line Count
```bash
$ wc -l .claude/agents/script-writer-v2.md
1398 .claude/agents/script-writer-v2.md
```
✓ Added 42 lines (was 1356, now 1398)
✓ Under 60-line target

### --variants Flag Coverage
```bash
$ grep -c "\-\-variants" .claude/commands/script.md
4
```
✓ Flag appears in: table, usage examples, section header, workflow documentation

### Choice References
```bash
$ grep "choice" .claude/commands/script.md | head -5
- **Past hook and structure choice patterns** for this topic type (from variant history)
   - Use insights to inform structure, pacing, and pattern choices
1. Surface past choice patterns for topic type (if any exist)
After 5+ choices, the system recommends preferred options based on your past patterns.
python tools/youtube-analytics/technique_library.py --choices
```
✓ Choice logging documented
✓ CLI commands included
✓ PRE-SCRIPT INTELLIGENCE updated

---

## Self-Check: PASSED

**Files created:**
- .planning/phases/38-structured-choice-architecture/38-02-SUMMARY.md ✓

**Files modified:**
```bash
$ git diff --stat HEAD~2
 .claude/agents/script-writer-v2.md | 42 ++++++++++++++++++++++++++
 .claude/commands/script.md          | 29 +++++++++++++++++
 2 files changed, 71 insertions(+)
```
✓ script-writer-v2.md modified (+42 lines)
✓ script.md modified (+29 lines)

**Commits exist:**
```bash
$ git log --oneline -2
49fce11 feat(38-02): add --variants flag and choice surfacing to /script command
1e11c15 feat(38-02): add Rule 16 (variant generation) to script-writer-v2 agent
```
✓ Commit 1e11c15 (Task 1 - Rule 16)
✓ Commit 49fce11 (Task 2 - --variants flag)

**Rule 16 structure verified:**
✓ A. Hook Variant Generation exists
✓ B. Structure Variant Generation exists
✓ C. Choice Logging exists
✓ D. Pre-Generation Summary exists
✓ Activation condition documented (--variants flag only)
✓ Part 8 references included

**--variants flag verified:**
✓ Added to flag table
✓ Added to usage examples
✓ VARIANT GENERATION section created
✓ Sequential flow documented
✓ Choice logging explained
✓ CLI review commands included
✓ PRE-SCRIPT INTELLIGENCE updated

---

## Next Steps

**For Plan 38-03 (Agent Consolidation - OPTIONAL):**
- Review Rule 16 line count (currently 42 lines)
- Consider condensing with Part 8 references if needed
- Evaluate overlap between Rule 7 (Spoken Delivery) and Rule 13 (Preference Auto-Capture)
- Potential consolidation: merge Rules 7 + 13 into single "Delivery & Preferences" rule

**Note:** Plan 38-03 is optional per plan dependencies. v3.0 Adaptive Scriptwriter is complete after Plan 38-02 ships.

---

**Completion:** 2026-02-15 20:52 UTC
**Commits:** 1e11c15, 49fce11
**Status:** ✓ Plan 38-02 complete - variant generation integrated into /script workflow
