# LLM-CRAFT-UPGRADE-PLAN.md

> **Executable upgrade plan, 2026-07-19.** Produced by an interview + research session (plan: `~/.claude/plans/write-a-plan-to-peppy-sunset.md`). **Sibling, not successor**, to `UPGRADE-PLAN.md` (23/24 done, root-level, drives `/refactor`) — this doc's steps become `/refactor`-runnable once `UPGRADE-PLAN.md` reaches 24/24: at that point archive the older plan to `docs/archive/` and promote this file's steps into the root `UPGRADE-PLAN.md`. Until then, run a step by pasting its Prompt block into a fresh session, same as any `UPGRADE-PLAN.md` step.

## Why this plan exists

The repo has genuinely advanced LLM-craft infrastructure — a calibration corpus with evidence tiers (`channel-data/calibration/CALIBRATION-CORPUS.md`), filters-not-predictors packaging gates (ADR-0007/0012), a voice fingerprint with an adversarial drift audit (`.claude/REFERENCE/VOICE-PROFILE.md`), and its own authoring-skills doctrine explicitly lineaged to Matt Pocock's `writing-great-skills` (`.claude/skills/authoring-skills/SKILL.md`). This plan does not re-invent any of that. It closes six specific, self-documented gaps found by cross-reading the repo's own audit files against six external practitioner sources (Karpathy, Anthropic engineering, Hamel Husain, Matt Pocock, Simon Willison — full citations below).

**What we are NOT changing:** the packaging gate philosophy, the calibration-corpus discipline, the `/voice grill` loop, and the 2026-07-15 talk-first pipeline flip (VOICE-PROFILE.md ~line 499, "the pipeline flip") are already at or ahead of published practice. This plan builds the missing scaffolding around them — it does not touch their logic.

## Sources

- **Karpathy — context engineering.** "Context engineering is the delicate art and science of filling the context window with just the right information for the next step." Four failure modes (poisoning, distraction, confusion, clash) map to four moves: **write, select, compress, isolate**. [x.com/karpathy/status/1937902205765607626](https://x.com/karpathy/status/1937902205765607626)
- **Anthropic — Effective context engineering for AI agents.** Context is the bottleneck, not intelligence; hybrid strategy of small always-loaded files + just-in-time retrieval; sub-agents return condensed summaries, not raw dumps. [anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Anthropic — Equipping agents for the real world with Agent Skills.** Progressive disclosure (metadata → SKILL.md → linked files); code for deterministic operations; **evaluation-first development** — run on representative tasks, observe failures, then build the skill. [anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Hamel Husain — Your AI Product Needs Evals.** Three levels (unit-test assertions → human + LLM-judge with measured agreement → A/B); build test cases from error analysis of real failures; start with binary good/bad labels; **a judge is only trustworthy once its agreement with a human is measured**, not assumed. [hamel.dev/blog/posts/evals](https://hamel.dev/blog/posts/evals/)
- **Matt Pocock — evalite.** Evals run like tests in the dev loop: local, cheap, per-case scored, on every change. (This repo is Python — the transferable principle is pytest-native evals, not the TS tool itself.) [github.com/mattpocock/evalite](https://github.com/mattpocock/evalite)
- **Simon Willison — plan-first workflow.** For non-trivial changes, write the plan, iterate on it as a "meta program," then execute step by step — the working method this very document follows. [simonwillison.net/series/using-llms](https://simonwillison.net/series/using-llms/)

---

## The six gaps

1. **Eval loop is manual, one-shot, in-sample.** `channel-data/calibration/EVAL-BASELINE.md` is a real golden-set regen eval — script-writer-v2 v18 blind-regenerated a #58 draft, scored PASS/PARTIAL/FAIL against the human lock on 24 criteria (R01–R24) sourced from CALIBRATION-CORPUS VALIDATED entries. It was run once, by hand, on the same video whose deltas trained the prompt — its own header says so: *"a pass means 'lessons encoded,' NOT 'generalizes.'"*
2. **Prompt changes fire no regression signal.** `.claude/agents/script-writer-v2.md` (1,965 lines / 154 KB) carries 48 dated rules layered in over time. A commit to it triggers nothing. `tests/unit/` tests the checker *code* (pacing, title scorer), never generated script text.
3. **LLM-as-judge is inline and unlogged.** `/script`'s Step 3a packaging-coherence check and `/verify`'s Steps 7.5–7.9 attribution passes are genuine Claude-native judge calls — but they re-run ad hoc each session with no persisted verdict ledger and no measured agreement against what the creator actually approves at read-aloud.
4. **`tools/voice_lint.py` has drifted from its own source of truth.** Its docstring says it's hand-transcribed from `VOICE-PROFILE.md` ("update RULES here when the profile changes"). The profile (line ~505) has staged two corrections since 2026-07-15 (demote T7 "to understand X we have to go back" from HARD to WARN-with-exception; add a "Now," relevance-scaffold exception) explicitly marked "not yet applied to voice_lint.py." No test catches this drift.
5. **The single largest read-aloud failure class is prose, not a tool.** VOICE-PROFILE.md line 512 (2026-07-16, T1–T3 read-alouds): ~30 of the creator's flags reduced to one failure — the script rebutting or calling back to a claim never stated on screen yet. Codified as *"a rebuttal is a referent too — its antecedent claim must exist on screen first"* and flagged **mechanizable** ("any AI pre-read must keep a running told-so-far ledger") — but no checker implements it.
6. **Context bloat violates the repo's own standard.** `authoring-skills/SKILL.md` caps SKILL.md at ~250 lines and preaches progressive disclosure. `script-writer-v2.md` is 154 KB, `structure-checker-v2.md` is 114 KB, `WRITING-VOICE-AND-STYLE.md` is 3,016 lines, and voice rules are restated across five surfaces (`/script`, script-writer-v2, structure-checker-v2, VOICE-PROFILE, WRITING-VOICE-AND-STYLE) rather than routed. `docs/AUDIT-COMMANDS-2026-06.md` flagged the two agent sizes without a remediation decision.

**Sequencing spine:** Phase E (eval harness) lands before Phase C (compaction) — the eval scores are what make it safe to compact 154 KB of accreted prompt without silently regressing R01–R24.

### Status legend
`[TODO]` not started · `[DOING]` in progress · `[DONE]` complete and committed · `[BLOCKED]` dependency unmet · `[INTERACTIVE]` requires the user live in session

## Status Tracker

**Total steps:** 15
**Done:** 11 (E1-E5, D1-D3, C1-C3 — E/D executed 2026-07-19/committed 2026-07-20 `12f54e8`..`173b829`; C1 `96b1e14`; C2 `bbec442`; C3 `c086865`)
**Blocked:** 1 (L3 — investigated 2026-07-19/20: Phase 75a is still "Not started" in `.planning/ROADMAP.md`, so the worked-example prerequisite is unmet)

**C1 finding worth flagging for C3/C4:** the plan's premise (48 dated rules = sediment) didn't hold uniformly. script-writer-v2.md (C1) was already well-consolidated — small yield (~1.6%), but caught a stale voice section actively contradicting VOICE-PROFILE.md. structure-checker-v2.md (C2) was the opposite: a whole parallel checklist system from an old iteration (dated 2025-01-16/2025-12-03, referencing a stale agent version) sat undetected alongside the current lettered Constraint system — real 17.8%-line reduction, and multiple sections were actively teaching the OPPOSITE of validated current rules (staccato mandate again, an 8-10-authority-marker target contradicting Constraint BE, a retention-fabrication instruction contradicting the file's own stated rule). The lesson holding across both: **don't assume sediment volume from file size — cross-read against the canonical docs (VOICE-PROFILE.md) and the file's own stated rules to find contradictions, not just duplication.** C3/WRITING-VOICE-AND-STYLE.md should get the same treatment.

| Phase | Steps | Theme | Risk |
|-------|-------|-------|------|
| E — Standing eval harness | E1–E5 | keystone; everything else depends on this existing | Medium |
| D — Deterministic checkers from error analysis | D1–D3 | mechanize documented, already-solved findings | Low |
| C — Context compaction | C1–C4 | BLOCKED until E5; guarded by the harness | Medium |
| L — Close open loops | L1–L3 | leftovers already tracked elsewhere in the repo | Low |

## Dependency map

```
E1 ──> E2 ──> E3 ──> E4 ──> E5
D1, D2, D3 independent (may run any time, but D1 should land before C1 touches voice rules)
C1 ──> C2 ──> C3 ──> C4     (all BLOCKED until E5 — need eval scores as a pre/post guard)
L1, L2, L3 independent
```

Hard ordering constraint: **E5 before any C step.** D and L steps may interleave freely.

---

# PHASE E — Standing Eval Harness

The keystone phase. Turns `EVAL-BASELINE.md`'s one-shot regen eval into a repeatable, versioned check that fires on prompt changes — the missing piece Hamel Husain's methodology and Pocock's evalite both center on.

## E1 [DONE] Extract the rubric into a versioned, runnable file

**Deps:** none

**Prompt:**
```
Read channel-data/calibration/EVAL-BASELINE.md in full. Extract its 24-criterion rubric (R01-R24) into a new file channel-data/calibration/EVAL-RUBRIC.md: one row per criterion with a stable ID, a binary checkable statement (not a paragraph), its CALIBRATION-CORPUS source citation, and the axis tag [V]/[St]/[Su]/[P]. Do NOT re-derive or reword the criteria — this is an extraction, not a rewrite. Then add new criteria for the failure class documented in .claude/REFERENCE/VOICE-PROFILE.md around line 512 (2026-07-16 T1-T3 read-alouds): "a rebuttal is a referent too - its antecedent claim must exist on screen first." Tag these [St], source-cite the VOICE-PROFILE line, tier VALIDATED (the creator's own read-aloud catches, not a hypothesis).
```

**Verify:** `EVAL-RUBRIC.md` exists with all 24 original criteria intact (spot-check R01, R22, R24 against EVAL-BASELINE.md) plus at least 2 new told-so-far criteria; every row has a source citation.

**Commit:** `feat(calibration): E1 extract EVAL-BASELINE rubric into versioned EVAL-RUBRIC`

## E2 [DONE] Define the golden set (fix the in-sample caveat)

**Deps:** E1

**Prompt:**
```
Read EVAL-BASELINE.md's IN-SAMPLE CAVEAT and channel-data/calibration/EVAL-RUBRIC.md (from E1). Create channel-data/calibration/EVAL-GOLDEN-SET.md listing, with exact paths:
- Positives: every locked SCRIPT.md under video-projects/_ARCHIVED/published/ for videos #56-#62 that has a corresponding CALIBRATION-CORPUS section.
- Negatives: channel-data/calibration/REGEN-58-V18-DRAFT.md and any generic-AI control sample referenced in the VOICE-PROFILE.md adversarial drift audit (Fable Phase 2, search "AI control").
- Voice-gold reference (outranks derived rules per the creator's own directive, VOICE-PROFILE.md ~line 499): the _adlib/ transcripts under video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026/_adlib/.
- One HELD-OUT locked script: pick the most recently locked video NOT yet mined into CALIBRATION-CORPUS.md (check which #-numbered video has the newest lock date with no corpus section). Mark it explicitly excluded from all future rule-mining until a future eval run consumes it — this is what fixes the in-sample caveat. If every locked script has already been mined, flag this as a blocker in the doc rather than picking one to un-mine.
```

**Verify:** `EVAL-GOLDEN-SET.md` exists; every listed path is confirmed to exist on disk; exactly one script is marked held-out with a stated exclusion date.

**Commit:** `feat(calibration): E2 define golden set with held-out script`

## E3 [DONE] LLM-as-judge protocol with measured agreement

**Deps:** E2

**Prompt:**
```
Design and document channel-data/calibration/EVAL-JUDGE-PROTOCOL.md: a Claude-native judge procedure that scores a draft script against every EVAL-RUBRIC.md criterion (PASS/PARTIAL/FAIL, matching EVAL-BASELINE.md's existing scale), citing the specific line(s) that earned each verdict - same evidentiary discipline as the existing R01-R24 table. Critically, per Hamel Husain's alignment rule: the judge is not trusted until its agreement with the creator's actual read-aloud verdicts is measured. Add a calibration step: run the judge against the LOCKED script for the held-out video from E2 (pre-lock draft if available, otherwise the lock itself) and compare its verdicts against what's already recorded in CALIBRATION-CORPUS.md / the video's read-aloud notes for that video. Record percent agreement per criterion in EVAL-JUDGE-PROTOCOL.md. State explicitly, per ADR-0007/0012 filters-not-predictors: the judge's output informs revision, it never gates lock - only the creator's read-aloud gates lock.
```

**Verify:** `EVAL-JUDGE-PROTOCOL.md` exists with a stated agreement percentage from a real calibration run (not a placeholder); the filters-not-predictors constraint is stated verbatim.

**Commit:** `feat(calibration): E3 LLM-judge protocol with measured human agreement`

## E4 [DONE] Runnable entry point

**Deps:** E3

**Prompt:**
```
Add tests/unit/test_eval_harness.py per this repo's validation-standards conventions (check tests/unit/ for the existing fixture/conftest pattern before writing). It should: (1) run the tools/script_checkers/ registry checkers (build_default_registry() from tools/script_checkers/registry.py) plus tools/voice_lint.py against every script in EVAL-GOLDEN-SET.md's positives and negatives, asserting positives score better than negatives on each deterministic checker; (2) provide a documented (not necessarily auto-run, since it needs a live Claude judge call) entry point - a script or pytest marker - for running the E3 judge protocol over the golden set and writing results to a dated file in channel-data/calibration/. Document both entry points at the top of the test file and in this plan's step. Do not attempt to automate the LLM-judge call inside pytest if that requires infrastructure this repo doesn't have (e.g. API keys in CI) - a documented manual/CLI trigger is acceptable, matching how EVAL-BASELINE.md itself was produced.
```

**Verify:** `pytest tests/unit/test_eval_harness.py` runs and passes the deterministic-checker assertions; the judge-protocol entry point is documented and was test-invoked at least once against the golden set.

**Commit:** `feat(calibration): E4 runnable eval harness entry point`

## E5 [DONE] Wire the regression trigger

**Deps:** E4

**Prompt:**
```
Extend the existing regen-regression guard (see memory/feedback-talk-first-scripting.md for the current informal version) into a written procedure: any version bump to .claude/agents/script-writer-v2.md, .claude/agents/structure-checker-v2.md, or .claude/REFERENCE/VOICE-PROFILE.md's HARD rules must run the E4 harness against the golden set BEFORE the new version is treated as adopted, and the result gets appended to channel-data/calibration/EVAL-BASELINE.md's ledger (new dated row, same format as the existing v18 entry) alongside the existing passes-to-lock KPI table. Document this as a step in the relevant agent/skill files' own changelogs (script-writer-v2.md and structure-checker-v2.md both have version/changelog frontmatter already - add one line there pointing to this procedure). This step is what unblocks Phase C.
```

**Verify:** The regression-trigger procedure is documented in `EVAL-BASELINE.md` and referenced from both agent files' changelog sections; re-read the dependency map above and confirm C1 is no longer BLOCKED.

**Commit:** `feat(calibration): E5 wire eval regression trigger, unblock Phase C`

---

# PHASE D — Deterministic Checkers From Error Analysis

Mechanizes findings the repo has already made and documented but not yet coded — the Anthropic "code for deterministic operations" principle applied to failures that are already solved in prose.

## D1 [DONE] Sync voice_lint.py to VOICE-PROFILE's staged corrections

**Deps:** none

**Prompt:**
```
Read .claude/REFERENCE/VOICE-PROFILE.md around line 505 ("LINT-RULE CORRECTIONS from the generative corpus") in full. Apply both staged corrections to tools/voice_lint.py: (1) demote the T7 "to understand X, we have to go back"-shaped rule from HARD_LITERALS/HARD_REGEXES to a WARN-tier rule that only fires when NOT followed by a walked causal chain (the profile gives two exception examples - use them as test cases); (2) add an exception to the "Now," opener ban so it doesn't fire on a relevance-scaffold usage like "Now, it is important to mention..." but still fires on the empty camera-turn "Now -". Then add a parity test (tests/unit/test_voice_lint_parity.py or similar, matching this repo's existing test file conventions) that fails loudly if voice_lint.py's HARD_LITERALS/HARD_REGEXES diverge from what VOICE-PROFILE.md currently stages as HARD - so this specific drift (documented-but-uncoded) can't silently recur.
```

**Verify:** `tools/voice_lint.py` no longer HARD-flags the two documented exception cases from VOICE-PROFILE.md line 505; the new parity test exists and passes; run `voice_lint.py` against the #58 gold script and confirm it still reports 0 HARD (the acceptance target cited in `channel-data/fable-digests/PHASE-2-VOICE-LINT-SPEC.md`).

**Commit:** `fix(voice-lint): D1 apply staged VOICE-PROFILE corrections, add parity test`

## D2 [DONE] Build the told-so-far ledger checker

**Deps:** none

**Prompt:**
```
Read .claude/REFERENCE/VOICE-PROFILE.md line 512 in full (the "READ-ALOUD'S REAL AXIS IS ARGUMENT-STATE" finding) and tools/script_checkers/registry.py's Checker protocol. Build a new checker at tools/script_checkers/checkers/told_so_far.py implementing that protocol: parse a script into beats/paragraphs, maintain a running set of claims/facts stated so far (a simple heuristic is fine for v1 - e.g. flag sentences containing negation-of-a-prior-claim markers, "callback," pronoun-only references to an unnamed antecedent, or rebuttal connectives like "but," "however," "isn't whole either" appearing before any positive statement of the thing being rebutted), and flag any rebuttal/callback whose apparent antecedent doesn't appear earlier in the same document. False positives are acceptable for v1 (this mirrors the other checkers' heuristic nature, e.g. scaffolding.py's proportional-threshold approach) - the goal is a first pass that surfaces candidates for the human read-aloud, not a perfect detector. Register it in build_default_registry() in registry.py. Add a unit test using at least one real example from VOICE-PROFILE.md line 512's own catalogue (the "which massacre?", "what case?" examples) as a known-flag case.
```

**Verify:** `told_so_far.py` checker registered and runnable via `tools/script_checkers/cli.py`; unit test passes against the VOICE-PROFILE.md-cited examples; run it against one locked script and confirm it doesn't produce an unusable volume of false positives (spot-check the output).

**Commit:** `feat(script-checkers): D2 told-so-far ledger checker mechanizes T1-T3 read-aloud finding`

## D3 [DONE] Persist inline judge verdicts

**Deps:** none

**Prompt:**
```
Read .claude/commands/script.md's Step 3a (Packaging Coherence Check) and .claude/commands/verify.md's Steps 7.5-7.9 (attribution/provenance judging). These are real LLM-as-judge calls that currently produce output only in the chat transcript. Add a lightweight append step to both commands: after the judge verdict is produced, append one line to a new channel-data/calibration/JUDGE-VERDICT-LOG.md (date, command, video slug, verdict summary, PASS/DRIFT/FAIL or equivalent). This is intentionally minimal - no new tooling, just a documented append-to-ledger instruction inside the existing command markdown, so verdict drift and (eventually, once enough entries exist) judge-to-creator agreement become measurable over time instead of evaporating each session.
```

**Verify:** `JUDGE-VERDICT-LOG.md` exists with a header explaining its schema; both `/script` Step 3a and `/verify` Steps 7.5–7.9 have an added append-to-ledger instruction; the instruction is stated as a completion criterion (per `authoring-skills`), not a no-op reminder.

**Commit:** `feat(calibration): D3 persist inline LLM-judge verdicts to a ledger`

---

# PHASE C — Context Compaction (BLOCKED until E5)

Applies Karpathy's write/select/compress/isolate and the repo's own `authoring-skills` progressive-disclosure standard to the two oversized agents and the largest reference doc — guarded by the Phase E eval scores so compaction can't silently regress R01–R24 or the told-so-far criteria.

## C1 [DONE] Compact script-writer-v2.md

**Deps:** E5

**Prompt:**
```
Run the Phase E harness (tests/unit/test_eval_harness.py + the E3 judge protocol) against the current .claude/agents/script-writer-v2.md and record baseline scores. Then read the full file (1,965 lines) and apply authoring-skills/SKILL.md's discipline: identify sediment (the 48 dated rules - which are superseded by a later dated rule on the same topic and can be cut, not just layered), duplication (voice rules that restate .claude/REFERENCE/VOICE-PROFILE.md instead of routing to it - per "skills route to the authoritative doc, never fork"), and no-op sentences. Consolidate superseded rules into their current form, move the historical dated-amendment trail into the file's changelog frontmatter instead of the body, and replace restated voice rules with pointers to VOICE-PROFILE.md sections. Re-run the Phase E harness against the compacted version. If any score regresses versus baseline, that criterion's supporting instruction was cut - restore it before committing.
```

**Verify:** Phase E harness score on the compacted file is equal to or better than the recorded baseline on every criterion; file size reduced (record before/after KB and line count in the commit message); no orphaned voice-rule restatements remain (spot-check against VOICE-PROFILE.md).

**Commit:** `refactor(agents): C1 compact script-writer-v2, eval-guarded`

## C2 [DONE] Compact structure-checker-v2.md

**Deps:** C1

**Prompt:**
```
Same method as C1, applied to .claude/agents/structure-checker-v2.md (2,582 lines / 114 KB). Baseline the Phase E harness first, apply the same sediment/duplication/no-op cleanup, re-run and confirm no regression before committing. Note from the repo survey: this file asserts "extended thinking mode... interleaved reasoning" in prose - verify whether this is a harness-level setting (frontmatter model/thinking config) or purely narrative instruction, and if narrative, either make it a real setting or cut the assertion (a no-op per authoring-skills: "does it change behaviour versus the default?").
```

**Verify:** Same eval-non-regression check as C1; the extended-thinking claim is either backed by a real config setting or removed.

**Commit:** `refactor(agents): C2 compact structure-checker-v2, eval-guarded`

## C3 [DONE] Progressive-disclosure the style manual

**Deps:** C2

**Prompt:**
```
Read .claude/REFERENCE/WRITING-VOICE-AND-STYLE.md (3,016 lines, PARTS 1-7) and every command/agent that currently instructs reading it whole or by PART (grep for its filename across .claude/commands/ and .claude/agents/). Apply authoring-skills' progressive-disclosure ladder: keep a lean core (the parts genuinely needed on every script run) and split the rest into named sibling files loaded only by the specific commands/agents that cite them, updating those citations to point at the split files instead of "read PARTS 1-5." Do not change any content - this is a structural split, not a rewrite. Run the Phase E harness after to confirm no citation was silently dropped (a criterion whose supporting instruction moved to a sibling file that nothing loads would regress the score).
```

**Verify:** No content lost (diff old-file line count against the sum of new files); every command/agent that referenced the old file now references the correct split file(s); Phase E harness shows no regression.

**Commit:** `refactor(reference): C3 progressive-disclosure WRITING-VOICE-AND-STYLE`

## C4 [TODO — deps: C3 done] Single-source voice rules

**Deps:** C3

**Prompt:**
```
Grep .claude/commands/script.md, .claude/agents/script-writer-v2.md, and .claude/agents/structure-checker-v2.md for voice-rule content that restates rather than routes to .claude/REFERENCE/VOICE-PROFILE.md (this should be largely done already if C1/C2 were thorough - this step is the cleanup pass and final verification). VOICE-PROFILE.md remains the single source of truth per ADR-0006. Replace any remaining restatement with a routing pointer. Run the Phase E harness one final time and record the full before/after comparison (original baseline from before C1 vs. final state) in EVAL-BASELINE.md as a dated entry.
```

**Verify:** No voice-rule duplication remains across the four surfaces (spot-check with grep for a few distinctive VOICE-PROFILE phrases); final Phase E harness comparison recorded in `EVAL-BASELINE.md`.

**Commit:** `refactor(reference): C4 single-source voice rules, record Phase C eval comparison`

---

# PHASE L — Close Open Loops

Items already tracked elsewhere in the repo that this plan surfaces but doesn't newly discover — included for completeness since they're part of the same LLM-craft picture.

## L1 [TODO] Fill the KPI ledger as data lands

**Deps:** none (data-dependent, not code-dependent)

**Prompt:**
```
Check channel-data/calibration/EVAL-BASELINE.md's "Passes-to-lock KPI ledger" table. When Panama (#36) locks, fill its "Passes to lock" cell and note the writer version used. When Panama publishes and 28 days of data exist, check the pre-registered H2 gate (first-28-day CTR >=4%) and record pass/fail. This is a standing reminder step, not a one-time task - re-run whenever a new video locks or crosses the 28-day mark.
```

**Verify:** The KPI ledger row for the most recently locked/published video is filled, not TBD.

**Commit:** `docs(calibration): L1 update passes-to-lock KPI ledger`

## L2 [TODO] Work the open voice contradictions

**Deps:** none

**Prompt:**
```
Read channel-data/calibration/INTERVIEW-AGENDA.md's "VOICE HANDOFF" section (H1-H9, all currently open). Run the standing /voice grill (per .claude/REFERENCE/voice-modes/grill.md) on 2-3 of these per session using the file's own line-variant format, until the list is empty or each remaining item is explicitly marked DEFERRED with a reason. Update INTERVIEW-AGENDA.md's resolution log the same way A1-A10/B1-B6 were recorded.
```

**Verify:** At least one H-item moves from OPEN to RESOLVED or DEFERRED with a logged reason; the resolution log gains a corresponding entry.

**Commit:** `docs(calibration): L2 resolve voice contradictions via /voice grill`

## L3 [BLOCKED — dep unmet: Phase 75a not started] Fill the AGENT-ORCHESTRATION worked-examples placeholder

**Deps:** none (depends on Phase 75a landing per the file's own note)

**Prompt:**
```
Check .claude/AGENT-ORCHESTRATION.md's "Worked Examples" section (currently a placeholder citing "Phase 75a"). Check .planning/ROADMAP.md for Phase 75a's status. If Phase 75a is complete, write the worked example per its success criterion #7 (cited in AGENT-ORCHESTRATION.md line 110): document the /research pilot's sequential retry pattern as a concrete example so later phases can cite "apply the 75a pattern." If Phase 75a is not yet complete, leave this step BLOCKED and note the dependency.
```

**Verify:** Either the Worked Examples section is filled with a concrete example, or the step is explicitly left BLOCKED with the Phase 75a status noted.

**Commit:** `docs(orchestration): L3 fill worked-examples section`
