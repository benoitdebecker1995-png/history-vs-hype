# Domain Pitfalls: v3.0 Adaptive Scriptwriter

**Domain:** Adding adaptive learning features to existing YouTube scriptwriting system
**Researched:** 2026-02-12
**Confidence:** HIGH

**Context:** Adding learning/adaptation to a working script-writer-v2 agent (1284-line prompt, 14 rules). Solo creator, no team. Any friction kills adoption.

---

## Executive Summary

The biggest risk isn't building bad features — it's breaking what works. script-writer-v2 already generates usable scripts. The V4→V5 editing pattern is working. The danger: making the system MORE complex without making the output measurably BETTER.

**Critical insight from project history:** v1.2 built voice fingerprinting. It requires manual `--rebuild-voice` setup. The user never ran it. Patterns remain empty. **Tools that require setup don't get used.**

---

## Pitfall 1: Prompt Bloat

**Risk:** script-writer-v2 is already 1,284 lines with 14 rules. Adding Rules 15-17 plus technique references plus retention playbook could push it past Claude's effective instruction-following threshold.

**Warning signs:**
- Agent starts ignoring earlier rules in favor of newer ones
- Script quality degrades after adding more instructions
- Agent takes longer to generate (more context = more thinking)
- New rules conflict with existing rules

**Prevention:**
- **Measure before adding:** Test script quality with current agent FIRST, then compare after adding rules
- **Consolidate, don't accumulate:** When adding Rule 15 (preferences), simplify or merge existing rules. Rule 13 (auto-capture) can be absorbed into Rule 15.
- **Move reference material OUT of agent prompt:** Techniques and retention rules go in STYLE-GUIDE.md parts (which agent reads), not in the agent definition file
- **Budget:** Target max 1,500 lines for agent prompt (currently 1,284 + ~200 new = 1,484)

**Phase to address:** All phases — monitor prompt size at every change.

---

## Pitfall 2: Learning From Noise

**Risk:** Not all edits are preferences. User changes "geologists were saying" to "Mexican senators were estimating" because the FACT was wrong, not because they prefer a different tone. Treating accuracy fixes as voice preferences pollutes the model.

**Warning signs:**
- Preferences.json fills with one-off corrections that aren't generalizable
- System starts "learning" from content-specific changes
- Preferences conflict with each other (because they were extracted from different contexts)

**Prevention:**
- **Classify edits before learning:** Use Claude API to categorize each edit as: accuracy_fix (don't learn), voice_preference (learn), structural (learn cautiously), content_specific (don't learn)
- **Require 3+ consistent edits** before promoting to confirmed preference. One edit = candidate only.
- **Human confirmation:** Show user what system "learned" periodically. Let them reject bad inferences.
- **Separate fact corrections from voice corrections:** If the edit changes a factual claim (name, date, source), it's NOT a voice preference.

**Phase to address:** Phase 39 (Edit Learning Loop) — classification logic is critical.

---

## Pitfall 3: Setup Friction = Non-Adoption

**Risk:** Voice fingerprinting (v1.2) required user to run `--rebuild-voice`. They never did. If transcript analysis requires manual steps, it won't happen either.

**Warning signs:**
- Features require multi-step setup before providing value
- User has to remember to run commands after editing
- System requires specific file naming or organization that user doesn't follow

**Prevention:**
- **Zero-setup principle:** Transcript analysis should work on existing transcripts/ folder as-is. No renaming, no reorganization.
- **Automatic edit tracking:** When user types "here's my edited version" or saves a new draft, the system should detect it automatically, not require a separate `/track-edits` command.
- **Progressive value:** System provides value from day 1 (retention science rules), more value at day 30 (accumulated preferences), full value at day 90 (rich technique library + learned voice).
- **Batch analysis over setup:** Analyze all 80+ transcripts in one command (`python tools/script-analysis/transcript_analyzer.py --all`), not require per-file processing.

**Phase to address:** Phase 37 (Transcript Analysis) and Phase 39 (Edit Learning) — design for zero-friction.

---

## Pitfall 4: Variant Fatigue

**Risk:** Offering too many options creates decision paralysis. The creator wants BETTER first drafts, not MORE first drafts to choose between.

**Warning signs:**
- User stops using `--variants` because it's slower
- User always picks the first option (not actually evaluating)
- Variant generation doubles the time before getting a script

**Prevention:**
- **Max 3 options** per category (hooks, structure). Never more.
- **Recommend one:** Always highlight which variant the system recommends and why. "Based on your territorial dispute preference pattern, I recommend Hook A."
- **Make it optional:** `--variants` flag, not default behavior. Default behavior: pick best option automatically based on learned preferences.
- **Quick format:** Variants should be 2-3 sentences each, not full paragraphs. User should be able to choose in 30 seconds.

**Phase to address:** Phase 38 (Choice Architecture) — keep it lightweight.

---

## Pitfall 5: Retention Science Becomes Formulaic

**Risk:** Baking retention rules too rigidly makes every video feel the same. "Pattern interrupt at 2:30, modern relevance at 4:00, evidence reveal at 5:30" = predictable and boring.

**Warning signs:**
- Every script has identical pacing structure
- Retention rules override creative choices
- Scripts feel like they were generated by algorithm

**Prevention:**
- **Guidelines, not rules:** Frame retention patterns as recommendations, not hard constraints. "Consider a pattern interrupt near the 3-minute mark" not "INSERT PATTERN INTERRUPT AT 3:00."
- **Score, don't block:** Flag sections that might have retention issues, but don't refuse to generate them. Let creator decide.
- **Preserve the Part 6 approach:** Current voice patterns are a LIBRARY to choose from, not a checklist to complete. Retention playbook should work the same way.
- **Creative override:** If creator says "I want a slow build here," the system should respect that even if it contradicts retention heuristics.

**Phase to address:** Phase 36 (Retention Science) — write as playbook, not rulebook.

---

## Pitfall 6: Preference Model Conflicts with Quality Rules

**Risk:** User's preferences might conflict with quality rules. Example: user might prefer shorter closings (preference), but the channel's best-performing videos have substantive 60-second closings (quality data).

**Warning signs:**
- Learned preferences contradict retention data
- Preferences from early videos (when channel was finding its voice) conflict with current successful patterns
- System applies outdated preferences to new content types

**Prevention:**
- **Quality rules (Rules 1-14) always override preferences (Rule 15)**
- **Timestamp preferences:** Track when preferences were learned. Older preferences get lower confidence over time.
- **Context-aware preferences:** A preference learned from a fact-check video might not apply to a territorial dispute video. Tag preferences with video type.
- **Periodic review:** Every 5 videos, surface preferences for user review. "You learned these 8 preferences over the last 5 videos. Still accurate?"

**Phase to address:** Phase 39 (Edit Learning) — priority hierarchy is critical.

---

## Pitfall 7: Analysis Paralysis Before First Script

**Risk:** Building the entire analysis pipeline (80+ transcripts, preference model, retention playbook) before the scriptwriter generates a single improved script.

**Warning signs:**
- Weeks of "infrastructure" before any script improvement
- User loses interest waiting for the system to be "ready"
- Over-engineering the analysis at expense of quick wins

**Prevention:**
- **Quick win first:** Phase 36 (Retention Science) should produce an improved STYLE-GUIDE.md Part 9 within one session. Scriptwriter immediately reads it. Instant improvement.
- **Progressive enrichment:** Each phase adds value independently. Don't wait for all 4 phases to complete.
- **Ship the retention playbook before analyzing transcripts.** The creator can feel the improvement on their next video.

**Phase to address:** Build order design — retention science FIRST because it's immediate value with no new code.

---

## Summary: Risk Mitigation by Phase

| Phase | Top Risk | Mitigation |
|-------|----------|------------|
| 36: Retention Science | Formulaic scripts | Write as playbook, not rulebook |
| 37: Creator Analysis | Setup friction | Zero-setup, batch processing |
| 38: Choice Architecture | Variant fatigue | Max 3 options, recommend best, make optional |
| 39: Edit Learning | Learning from noise | Classify edits, 3+ threshold, human confirmation |
| All phases | Prompt bloat | Budget 1,500 lines max, consolidate rules |

---

*Researched: 2026-02-12 for v3.0 Adaptive Scriptwriter milestone*
