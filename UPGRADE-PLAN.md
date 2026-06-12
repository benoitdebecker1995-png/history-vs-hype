# UPGRADE-PLAN.md

> **Executable upgrade plan, 2026-06-12.** Produced by an interview + grill-with-docs session (plan: `~/.claude/plans/quizzical-gliding-goblet.md`). Successor to `docs/archive/REFACTOR-PLAN.md` (47/47 done). Run steps via `/refactor` (one step → one commit → stop) or by pasting a step's Prompt block into a fresh session.
>
> **Phase 0 (hygiene sweep) was executed inline on 2026-06-12** — root triage, worktree prune, CONTEXT.md slim-down, GRAPHIFY-OPS correction. Commits `2135938`..`959e5ce`. Not tracked here.

---

## Why this plan exists (context)

The previous improvement cycles are closed. The dominant remaining problem, per the user: **script drafts miss on all four axes — voice, structure, substance, and revision-cycle count. The goal is scripts that are engaging, clear, watchable, and SOUND LIKE HIM, with fewer passes to lock.** Phase 1 is the priority track; Phases 2–4 are supporting infrastructure.

**Pipeline sequencing (grill-locked 2026-06-12):**
- Panama #36 is the **next video after Kurdistan #58** (breakout-probability ordering: "Panama wins the board" per Fable Phase 4 rubric; H1/H2/H4 pre-registered).
- #59 I/P parks mid-draft (~1,672 words, v17) and resumes after Panama. It becomes a v17/v18 hybrid → **excluded from the KPI**.
- Phase 1 steps S1–S13 run **during Panama's Phase-2 NotebookLM research window** and must complete **before Panama scripting starts**.
- KPI: **passes-to-lock** (defined in `CONTEXT.md` § Production terms). #58 = v17 baseline (~2-3), Panama = first clean v18 test. Secondary: Panama's pre-registered H2 gate (first-28-day CTR ≥4%).

### Status legend
`[TODO]` not started · `[DOING]` in progress · `[DONE]` complete and committed · `[BLOCKED]` dependency unmet · `[INTERACTIVE]` requires the user live in session (don't run from phone /refactor unless you're present to answer)

---

## Status Tracker

**Last advanced:** 2026-06-12 (S14)
**Total steps:** 24
**Done:** 9

| Phase | Steps | Theme | Risk |
|-------|-------|-------|------|
| S — Script-accuracy calibration | S1–S14 | THE priority track | Medium |
| R — Research infrastructure | R1–R5 | quickest payoff first | Low |
| W — Workflow & command audit | W1–W3 | audit-report-first, user picks merges | Low |
| T — Production tooling | T1–T2 | leftovers from REFACTOR-PLAN era | Low |

## Dependency map

```
S1 ──> S2 ──> S8 ──> S9 ──┬──> S11 ──> S12 ──> S13
S3 ─────────┤      S10 ──┘
S4 ─────────┤
S5 ─────────┤
S6 ─────────┤
S7 ─────────┘
S14 (independent — wire any time after S1)

R1, R2 independent · R3 ──> R4 · R5 independent
W1 ──> W2 · W3 independent
T1, T2 independent
```

Hard ordering constraint: **S1–S13 before Panama `/script`.** R/W/T steps can interleave freely.

---

# PHASE S — Script-Accuracy Calibration

All corpus output accumulates in `channel-data/calibration/CALIBRATION-CORPUS.md`. Every delta entry is tagged with an axis: `[V]` voice · `[St]` structure · `[Su]` substance · `[P]` process/revision-economy. Source-tier rule: read-aloud corrections and locked-script diffs = validated signal; SRT deviations and retention mappings = **hypotheses only** (per `memory/feedback-postmortem-methodology.md`).

## S1 [DONE] Consolidate existing ad-hoc lesson artifacts

**Deps:** none

**Prompt:**
```
Create channel-data/calibration/CALIBRATION-CORPUS.md. Structure: header explaining axis tags + tier rule, then one section per source video (#56, #57, #58), then a cross-video "Recurring patterns" section (initially empty).
Consolidate — do NOT re-derive — every existing lesson artifact:
- #56 (video-projects/_ARCHIVED/published/56-no-lassos-atlantic-slave-trade-origin-2026/): REWRITE-PLAN-2026-05-25.md, PROSE-SCAN-2026-05-24.md, PROSE-SCAN-2026-05-25.md, READ-ALOUD-v3..v8 files, FIG-TREE-EDIT-PASS-*.md
- #57 (video-projects/_ARCHIVED/published/57-piri-reis-map-ottoman-2026/): WRITER-LESSONS.md, VOICE-FINGERPRINT.md, REVISION-BRIEF-v6.md
- #58 (video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/): VOICE-DRILL-RESUME.md + the lock-session lessons recorded in memory/58-kurdistan-production-state.md
Each lesson becomes one corpus entry: short rule statement, axis tag, source artifact path, validated/hypothesis tier. Dedupe against .claude/REFERENCE/VOICE-PROFILE.md — if a lesson is already canonical there, list it as a one-line cross-ref, not a duplicate entry.
```

**Verify:** `CALIBRATION-CORPUS.md` exists; contains ≥20 entries; every entry has an axis tag; zero entries duplicate VOICE-PROFILE rules verbatim.

**Commit:** `feat(calibration): S1 consolidate existing lesson artifacts into corpus`

## S2 [DONE] Mine draft-vs-locked version diffs

**Deps:** S1

**Prompt:**
```
Diff the in-folder script versions and extract every systematic edit pattern as a corpus delta:
- #56: 02-SCRIPT-DRAFT-v1-locked.md -> 02-SCRIPT-DRAFT.md (final)
- #57: SCRIPT-v2.md -> SCRIPT-v3.md -> SCRIPT-v4.md -> SCRIPT.md (locked)
Classify each recurring edit (not one-off content fixes): what did the lock version consistently do that the draft didn't? Sentence surgery, transition rewrites, concede-first insertions, attribution trims, beat moves, cut categories. Tag axis + tier (these are VALIDATED — he made these edits). Append to CALIBRATION-CORPUS.md under each video's section; update Recurring patterns for anything appearing in 2+ videos.
```

**Verify:** corpus gains ≥10 new entries sourced to version diffs; Recurring-patterns section non-empty.

**Commit:** `feat(calibration): S2 draft-vs-locked diff deltas`

## S3 [DONE] SRT-vs-script ad-lib deltas

**Deps:** S1

**Prompt:**
```
For each published video that has BOTH a locked script and a delivered SRT/subtitle file (search transcripts/, video-projects/_ARCHIVED/published/*/ for .srt; at minimum #56 and #57): align script to SRT and extract every place he deviated on camera — added connective tissue, dropped a line, rephrased into plainer speech, reordered. Each systematic deviation = a corpus entry tagged [V] or [St], tier HYPOTHESIS (per feedback-postmortem-methodology: SRT deltas are hypotheses, not validated rules). Where a deviation CONFIRMS an existing S1/S2 entry, upgrade that entry's confidence note instead of duplicating.
```

**Verify:** corpus gains SRT-delta section per video analyzed; all new entries marked HYPOTHESIS.

**Commit:** `feat(calibration): S3 SRT ad-lib deltas (hypotheses)`

## S4 [DONE] Retention-curve → beat mapping

**Deps:** S1

**Prompt:**
```
For each video with a POST-PUBLISH-ANALYSIS file (channel-data/analyses/ + archived project folders): map retention drop-off points to the script beat at that timestamp. Output per video: table of (timestamp %, beat description, drop severity, candidate cause). Tag entries [St] or [Su], tier HYPOTHESIS, and respect feedback-channel-data-too-small: individual-video retention is noise — only promote to Recurring patterns if the same beat-type drops in 3+ videos. Append to CALIBRATION-CORPUS.md.
```

**Verify:** mapping table exists for every video that has a post-publish report; no single-video pattern promoted to Recurring.

**Commit:** `feat(calibration): S4 retention-to-beat mapping (hypotheses)`

## S5 [DONE] Deep linguistic fingerprint of the unscripted gold standard

**Deps:** S1

**Prompt:**
```
Pull the transcript of yt:yMAWJcjo_ug (his first, unscripted video — VOICE-PROFILE gold standard) via tools/yt-dlp.exe --write-auto-sub or existing transcript in transcripts/. Produce channel-data/calibration/FINGERPRINT-UNSCRIPTED.md going BEYOND VOICE-PROFILE's top-level rules: sentence-length distribution (mean/median/histogram buckets), connector inventory with frequencies (so/which is why/and that meant/...), how he opens a thought, how he closes one, hedges he uses, idiolect phrases (recurring word choices unique to him), question frequency, self-correction patterns. Quantitative where possible (this feeds voice_lint thresholds later). Summarize the 10 strongest fingerprint markers as corpus entries [V], tier VALIDATED (it IS him).
```

**Verify:** FINGERPRINT-UNSCRIPTED.md exists with quantitative distributions; ≥10 fingerprint entries added to corpus.

**Commit:** `feat(calibration): S5 unscripted-video linguistic fingerprint`

## S6 [DONE] Reference-creator spoken-naturalness mine

**Deps:** S1

**Prompt:**
```
Positive refs per VOICE-PROFILE: Kraut, Alex O'Connor (anti-voice: RealLifeLore). Channel IDs in tools/intel/competitor_channels.json. Pull 3-4 high-retention transcripts per ref via tools/yt-dlp.exe, dispatch bulk digestion to Gemini Flash per .claude/commands/gemini.md. Extraction target: spoken-naturalness mechanics SPECIFICALLY (how they keep long explanations conversational, transition phrases, sentence rhythm around evidence, how they attribute sources aloud) — NOT retention/packaging patterns (the 85-transcript corpus covers that). Output channel-data/calibration/REFERENCE-CREATOR-NATURALNESS.md. Corpus entries tagged [V]/[St], tier IDEA (imported, must be tested — rules-hedge principle; they are HIS refs but not HIS voice).
```

**Verify:** digest file exists covering ≥2 creators; all corpus entries from this step marked IDEA.

**Commit:** `feat(calibration): S6 reference-creator naturalness digest`

## S7 [DONE] Internet craft-rules sweep

**Deps:** S1

**Prompt:**
```
WebSearch sweep: published craft guidance on writing for spoken delivery (broadcast-writing handbooks, speechwriting research, "write for the ear" literature, documentary VO practice). Curate HARD against generic YouTube-guru content. Output: channel-data/calibration/CRAFT-RULES-IMPORTED.md — each rule with source, one-line rationale, and a testable formulation. ALL entries tier IDEA (rules-hedge: imported rules are ideas to test, never mandates). Cap at ~15 rules; prefer rules that bear on the four axes and that CONFLICT with or sharpen current practice (those are the informative ones).
```

**Verify:** file exists, ≤15 rules, every rule has a source and tier IDEA.

**Commit:** `feat(calibration): S7 imported craft rules (hedged)`

## S8 [DONE] Contradiction + gap report → interview agenda

**Deps:** S1, S2, S3, S4, S5, S6, S7

**Prompt:**
```
Read the full CALIBRATION-CORPUS.md + the three side files (FINGERPRINT-UNSCRIPTED, REFERENCE-CREATOR-NATURALNESS, CRAFT-RULES-IMPORTED). Produce channel-data/calibration/INTERVIEW-AGENDA.md:
1. CONTRADICTIONS — places where two signals disagree (e.g. read-aloud note says tighter, SRT shows him expanding; imported rule conflicts with a validated delta). Each with both pieces of evidence cited.
2. GAPS — axes/situations no signal covers.
3. For every item: a draft grill question with 2-3 CONCRETE line variants from real scripts (feedback-grill-easier format — line variants in chat, never abstract rule-options).
Split the agenda into Session A (structure + substance) and Session B (process + revision economy). Voice contradictions route to the existing /voice grill cadence instead — list them in a handoff section, do not duplicate the voice truth source.
```

**Verify:** INTERVIEW-AGENDA.md exists; every item has cited evidence + concrete line variants; voice items in handoff section only.

**Commit:** `feat(calibration): S8 contradiction/gap report + interview agenda`

## S9 [TODO] [INTERACTIVE] Grill session A — structure + substance

**Deps:** S8

**Prompt:**
```
Run INTERVIEW-AGENDA.md Session A as a grill: one item at a time, concrete line variants in chat, he picks + annotates, you derive the rule and record it in CALIBRATION-CORPUS.md as VALIDATED (user-picked). Update INTERVIEW-AGENDA.md marking items resolved. Stop when agenda done or he calls time; unresolved items stay queued.
```

**Verify:** every Session-A item marked resolved or explicitly deferred; derived rules in corpus.

**Commit:** `feat(calibration): S9 grill session A resolutions`

## S10 [TODO] [INTERACTIVE] Grill session B — process + revision economy

**Deps:** S8

**Prompt:**
```
Same protocol as S9 for Session B (process + revision economy: what makes a draft converge in 2 rounds instead of 6 — ordering of passes, notebook-first timing, opener-decision timing, what he wants checked BEFORE he reads aloud).
```

**Verify:** every Session-B item resolved or deferred; derived rules in corpus.

**Commit:** `feat(calibration): S10 grill session B resolutions`

## S11 [TODO] Compile agent diff proposals

**Deps:** S9, S10

**Prompt:**
```
Compile CALIBRATION-CORPUS.md (now including grill resolutions) into channel-data/calibration/AGENT-DIFF-PROPOSALS.md, learn-from-paper format (proposals, NOT applied edits): proposed diffs for (a) .claude/agents/script-writer-v2.md -> v18, (b) .claude/agents/structure-checker-v2.md next wave, (c) tools/voice_lint.py new rules with thresholds from FINGERPRINT-UNSCRIPTED quantitative data, (d) .claude/commands/script.md flow changes targeting revision economy. Each diff cites its corpus entries. VALIDATED entries -> rule changes; HYPOTHESIS/IDEA entries -> at most WARN-level checks or A/B notes, never hard rules.
```

**Verify:** proposal file exists; every proposed diff cites corpus entries; no IDEA-tier entry became a hard rule.

**Commit:** `feat(calibration): S11 agent diff proposals (v18 candidate)`

## S12 [TODO] [INTERACTIVE] Apply approved diffs

**Deps:** S11

**Prompt:**
```
Walk AGENT-DIFF-PROPOSALS.md with the user; apply ONLY approved diffs. Bump versions (script-writer-v2 v18.0 etc.), run python tools/agent_contract_check.py if applicable, update memory/agent-versions.md with the new versions + one-line provenance. Rejected proposals stay in the file marked REJECTED with his reason (that's calibration data too — append to corpus).
```

**Verify:** approved diffs applied + version bumps consistent; agent-versions.md updated; rejections recorded.

**Commit:** `feat(agents): S12 script-writer v18 + checker/lint calibration diffs`

## S13 [TODO] Regression harness — in-sample sanity check

**Deps:** S12

**Prompt:**
```
Derive a scoring rubric from the corpus's VALIDATED entries (one checkable criterion each). Regenerate a draft from video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/01-VERIFIED-RESEARCH.md using script-writer-v2 v18 (full normal inputs: VOICE-PROFILE, WRITING-VOICE-AND-STYLE, structure refs). Score the regenerated draft vs the locked SCRIPT.md on the rubric. Record in channel-data/calibration/EVAL-BASELINE.md with the explicit caveat: IN-SAMPLE — v18 was trained on #58's deltas; a pass means "lessons encoded," NOT "generalizes." Real test = Panama passes-to-lock + H2 CTR gate. Do NOT touch the actual #58 production files.
```

**Verify:** EVAL-BASELINE.md exists with rubric, scores, and the in-sample caveat; #58 production files untouched (git status clean for that folder).

**Commit:** `feat(calibration): S13 in-sample regression baseline (v18 vs #58 lock)`

## S14 [DONE] Standing-loop wiring (reconcile-mirror)

**Deps:** S1

**Prompt:**
```
Wire the per-video calibration loop:
1. CLAUDE.md: add a conversational trigger rule next to the /reconcile trigger — when the user declares a script locked ("script locked", "lock it", T1-passed), IMMEDIATELY run the post-lock delta-mine: consolidate that video's read-aloud notes/version diffs/session corrections into CALIBRATION-CORPUS.md, append new contradictions to INTERVIEW-AGENDA.md, record the video's passes-to-lock count in EVAL-BASELINE.md.
2. .claude/commands/reconcile.md: add a backstop check — on each run, flag any SCRIPT.md-locked project whose deltas aren't in the corpus.
3. memory: update memory file(s) so the trigger survives sessions (feedback-project-reconciliation.md sibling entry or new feedback-calibration-loop.md).
```

**Verify:** CLAUDE.md trigger present; reconcile.md backstop present; memory file written.

**Commit:** `feat(calibration): S14 standing post-lock mining loop`

---

# PHASE R — Research Infrastructure

## R1 [TODO] Wire /greenlight NLM title validation

**Deps:** none

**Prompt:**
```
Read .claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md § Proposed/Backlog — the /greenlight title-validation prompt stub. Wire it into .claude/commands/greenlight.md as a step (packaging notebook query via notebook-researcher agent or direct mcp notebook_query), with a SKIP path when the packaging notebook is unreachable. Move the prompt from Proposed to Active in NOTEBOOKLM-RESEARCH-PROMPTS.md.
```

**Verify:** greenlight.md contains the step with skip path; prompt no longer listed as Proposed.

**Commit:** `feat(greenlight): R1 wire NLM title validation`

## R2 [TODO] Wire post-/script NLM structure comparison

**Deps:** none

**Prompt:**
```
Same pattern as R1 for the post-/script structure-comparison stub: wire into .claude/commands/script.md after the structure-checker auto-invoke, gated to run only when a project notebook exists. Move prompt to Active.
```

**Verify:** script.md contains the gated step; prompt moved to Active.

**Commit:** `feat(script): R2 wire NLM structure comparison`

## R3 [TODO] NLM coverage-notebook pilot (decides R4)

**Deps:** none

**Prompt:**
```
Create a NotebookLM notebook "HvH-coverage-corpus" with all 01-VERIFIED-RESEARCH.md files (archived + active projects). Run 10 representative coverage queries ("have we cited Mamdani", "which videos touch Treaty of Lausanne", ...) — compare answer quality + latency against mcp graphify-research query_graph on the same questions. Write verdict to .claude/REFERENCE/GRAPHIFY-OPS.md Open Work item 1: NOTEBOOK-SUFFICIENT (mark R4 [BLOCKED] with note) or GRAPH-STILL-NEEDED (R4 proceeds). Both paths are zero marginal cost — judge on quality only.
```

**Verify:** notebook exists with sources; 10-query comparison table written; GRAPHIFY-OPS verdict recorded; R4 status updated accordingly.

**Commit:** `feat(research-infra): R3 coverage-notebook pilot + verdict`

## R4 [TODO] Scope-A research-graph densification (conditional on R3)

**Deps:** R3

**Prompt:**
```
Only if R3 verdict = GRAPH-STILL-NEEDED. Extend tools/refresh-research-graph.py to ingest the full scope-A corpus (all 01-VERIFIED-RESEARCH.md + .brain/ quote threads + tools/benchmark/ playbooks) via Gemini Flash CLI, chunked; keep the balanced-brace JSON-truncation guard (known Flash duplication quirk, GRAPHIFY-OPS caveats). Re-verify citation attribution on a 20-sample against source files (known 2/20 error rate in markdown passes).
```

**Verify:** graph node count grows materially (baseline 169 entities); 20-sample attribution check ≥95% correct; mcp graphify-research returns ≥3 hits on 5 test coverage queries that previously fell back to file reads.

**Commit:** `feat(research-infra): R4 scope-A graph densification`

## R5 [TODO] Drive source library — next stage only

**Deps:** none

**Prompt:**
```
Read memory/project-drive-library.md for current stage of the ~2000-PDF consolidate/rename/mirror pipeline. Execute exactly the next stage (per feedback-metadata-extraction-order: cheap extraction before LLM). Update the memory file with the new state. Do not re-plan the pipeline.
```

**Verify:** memory file shows stage advanced; spot-check 10 processed files.

**Commit:** `feat(library): R5 drive-library next stage`

---

# PHASE W — Workflow & Command Audit

## W1 [TODO] Command/skill/agent audit report

**Deps:** none

**Prompt:**
```
Inventory all entries in .claude/commands/, .claude/skills/ (project + user-level relevant to this repo), .claude/agents/. For each: (1) static references (which docs/commands point at it), (2) invocation signal — grep the local session logs in ~/.claude/projects/D--History-vs-Hype/*.jsonl for skill/agent invocations, count per name (zero cost, local only), (3) approximate context cost (file size + files it instructs to read), (4) overlap candidates (commands whose procedures substantially intersect). Output docs/AUDIT-COMMANDS-2026-06.md: table + a shortlist of merge/retire candidates with rationale. DO NOT merge or delete anything — the user picks from the report (grill-locked: audit-report first, no silent consolidation).
```

**Verify:** report covers every command/skill/agent file; includes invocation counts; zero files modified besides the report.

**Commit:** `docs(audit): W1 command/skill/agent audit report`

## W2 [TODO] [INTERACTIVE] Execute approved merges

**Deps:** W1

**Prompt:**
```
Walk the W1 shortlist with the user. Execute ONLY approved merges/retirements; for each: update all referencing docs (ref-grep first), preserve removed content under .claude/_ARCHIVE/, note the change in docs/AUDIT-COMMANDS-2026-06.md decision log.
```

**Verify:** ref-greps clean for every removed name; decision log records every choice including rejections.

**Commit:** `refactor(commands): W2 approved consolidations`

## W3 [TODO] Routine health check

**Deps:** none

**Prompt:**
```
For routines 1-6 (tools/routines/ + .claude/routines/ + scheduled task definitions): verify each ran within its expected cadence (check output timestamps in .brain/_inbox/, channel-data/, logs/), outputs land where .brain/index.md says they land, and no routine references files moved by Phase 0 (ref-grep docs/archive moves against routine code). Output: short health table appended to docs/AUDIT-COMMANDS-2026-06.md (or standalone docs/ROUTINE-HEALTH-2026-06.md if W1 not yet run). Fix only broken PATHS (Phase-0 fallout); anything behavioral goes in the report as a finding.
```

**Verify:** all 6 routines assessed; any Phase-0 path breakage fixed and noted.

**Commit:** `chore(routines): W3 health check + path fixes`

---

# PHASE T — Production Tooling

## T1 [TODO] Resolve REFACTOR-PLAN F4 (database hardening leftover)

**Deps:** none

**Prompt:**
```
Read docs/archive/REFACTOR-PLAN.md step F4 (blocked: schema mismatch with audit). Inspect the actual schema (tools/youtube_analytics/analytics.db + relevant store modules) vs what F4's source audit (.planning/audits/52-database.md) assumed. Either: implement the corrected version of F4 against the real schema, or close it WONTFIX with a 3-sentence rationale appended to the archived plan's F4 section. Root-cause rule applies: no schema hacks to force-fit a stale audit.
```

**Verify:** F4 either implemented (tests in tests/ pass) or marked WONTFIX with rationale; no other steps touched.

**Commit:** `fix(db): T1 resolve REFACTOR-PLAN F4 (implement or wontfix)`

## T2 [TODO] Test-suite status + calibration-tool gaps

**Deps:** none

**Prompt:**
```
Run the full suite: python -m pytest tests/ tools/tests/ -q (and tools/youtube_analytics tests if separate). Record pass/fail. For the calibration-relevant tools (tools/voice_lint.py, tools/title_scorer.py, tools/script_checkers/) list which behaviors are untested. Output: docs/TEST-STATUS-2026-06.md. Fix any test broken by Phase-0 moves (feedback-behavior: never dismiss as pre-existing — but scope here is Phase-0 fallout + report; deeper gaps become findings, not silent fixes).
```

**Verify:** suite run recorded with counts; Phase-0-caused failures fixed; gap list present for the 3 calibration tools.

**Commit:** `test(tools): T2 suite status + calibration-tool gap report`

---

## Drift log

*(append-only; /refactor writes verify-failures and out-of-scope observations here)*

### Out-of-scope observation (S4, 2026-06-12)
`video-projects/_ARCHIVED/published/35-gibraltar-treaty-utrecht-2026/POST-PUBLISH-ANALYSIS.md` is misfiled: it analyzes video `TYNaIu28LeU` ("The 1922 Treaty Loophole That Ended the USSR" — Belavezha lane), not the Gibraltar video (`WZnCxVPNF7A` per project-map). Not fixed (off-step scope); S4 mapped it under zone labels with no Gibraltar chapter join.

### Out-of-scope observation (S6, 2026-06-12)
`transcripts/Kraut/` contains two non-Kraut files: `Why is Russia So DAMN BIG？.*` is a **RealLifeLore** video (the anti-voice — a first S6 digest pass was contaminated by it and re-run on genuine Kraut only) and `Tiedustelueverstin arvio Venäjästä….*` is a Finnish-language interview. Both excluded from S6; files left in place (off-step scope) — consider moving them out of the Kraut folder so future voice mining doesn't ingest the anti-voice as a positive ref.
