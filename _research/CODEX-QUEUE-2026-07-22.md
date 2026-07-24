# CODEX WORK QUEUE — post-#62, 2026-07-22

Three independent jobs. **Run them one at a time, each as its own session**, and read `video-projects/_IN_PRODUCTION/62-volhynia-massacre-untranslated-2026/_research/CODEX-COLLAB-BRIEF-2026-07-22.md` §2–§4 first — the constraints there (add no facts, never strip an attribution, never supply a missing actor from inference, no numeric targets) apply to all three.

Two other queued items are already done and are **not** yours: the hedge counter is fixed (`tools/voice_lint.py`, `_hedges_in`, tests in `tests/unit/test_voice_lint_hedge.py`) and the locked-line sweep has been run — see the closing note.

---

## JOB A — open-question ledger audit of the four other in-production scripts

**Why now:** V1–V5 violations are cheapest to fix before research and filming money is spent. #62 needed seven read-alouds partly because these went undetected until his mouth found them.

**Targets**, in this order:
1. `video-projects/_IN_PRODUCTION/63-leopold-congo-cobalt-2026/`
2. `video-projects/_IN_PRODUCTION/61-spanish-colonization-black-legend-2026/`
3. `video-projects/_IN_PRODUCTION/60-guadalupe-hidalgo-dispossession-2026/`
4. `video-projects/_IN_PRODUCTION/36-panama-canal-deconcini-2026/`

For each, find the most advanced script artifact (`SCRIPT.md`, `02-SCRIPT-DRAFT.md`, or a `VO-*.md`) and audit **only** the ledger, using the definitions in `HUMANIZE-PROMPT.md` §5:

- **V1** term/name/claim used before it is introduced
- **V2** answering a question the viewer never asked
- **V3** raising a question and never answering it
- **V4** re-answering a closed question — ⚠ **but check what a restatement's POSITION is doing before calling it repetition.** #62 deliberately states the death toll twice so scale lands before the honoring is explained. A previous pass cut that as V4 and broke the guard.
- **V5** breaking a promise the script made earlier

**Do not rewrite anything.** Output one file per project at `<project>/_research/LEDGER-AUDIT-2026-07-22.md`: a table of `type · location · the open question · the violation · suggested fix`, plus a note on any violation that cannot be fixed without a fact the project doesn't have. Flag those loudest — they are research tasks, not writing tasks.

---

## ⚠ CORRECTION FROM JOB A — read before B and C

Job A's audits were **accurate on the defects and wrong on every classification.** All four items filed as "LOUD — research-dependent, requires a fact" were **already verified, sourced facts sitting in that project's own `01-VERIFIED-RESEARCH.md`**, unread:

| flagged as needing research | actually in the ledger |
|---|---|
| #36 who coined "titular sovereignty" | **John Hay, 1904** — C29, ✅ LaFeber/Jorden T1 |
| #36 "the investigation" | the **OAS** investigation — line 174, ✅ Jorden/LaFeber |
| #36 Maier's legal reasoning | the Leadership Amendment + Panama's counter-reservation fence the DeConcini clause; it "gives and takes away with the same hand" — lines 17–18 |
| #60 why the Senate deleted Article X | **Ebright p.32 argues** it was to avoid being bound by *Percheman*'s pro-grantee precedent — line 93, SUPPORTED |

**The rule this establishes: never classify a gap as research-dependent without reading `01-VERIFIED-RESEARCH.md` first.** An audit of a script in isolation can find that a question is unanswered; it cannot find whether the answer exists. Getting this backwards is expensive in the wrong direction — it sends verified work to the research queue.

It also surfaced a real pattern worth carrying: **these scripts are vaguer than their own research.** "They coined a phrase" for a documented person, "the investigation" for the OAS. That is the opposite of the usual failure, and it costs this channel specifically, because named agents and named mechanisms are its conversion trigger.

**For Jobs B and C: read the project ledger before calling anything missing.**

## JOB B — implement the V2–V5 checkers

`tools/script_checkers/checkers/told_so_far.py` implements **V1 only** (the antecedent case). V2–V5 have been unimplemented since 2026-07-20 and you have just applied all five by hand across a whole script, so the working definitions are fresh.

**Read first:** `.claude/skills/extending-safely/SKILL.md` and `.claude/skills/validation-standards/SKILL.md`. This repo has a seam discipline and a test-first expectation; extend the existing checker, do not add a parallel one.

**Be honest about what is mechanizable.** My read: **V1 and V5 are tractable** (V1 is first-mention-vs-definition, already half-built; V5 is a promise-pattern — "would have left three things behind", "we'll come back to" — followed by a satisfaction check). **V4 is partly tractable** as near-duplicate detection between paragraphs, and must ship with the position-guard as a REVIEW-level flag, never a WARN. **V2 and V3 are probably not mechanizable** — they need a model of what the viewer is currently asking.

**So: build what is real and say plainly what is not.** A checker that emits confident nonsense on V2/V3 is worse than no checker, because this project gates on `0 HARD`. Anything uncertain lands at REVIEW. Tests required, real fixtures from `#62` and `#56`, not synthetic strings.

---

## JOB C — the cold open, against retention

27 of 56 videos on this channel die not-clicked or not-held, and the growth bottleneck is packaging, not content. The first 30 seconds is the most expensive real estate in the catalogue.

Read the **first 30 seconds only** (~90 words) of the last ten published scripts under `video-projects/_ARCHIVED/published/`, and the per-video retention and CTR in `channel-data/CHANNEL-PERFORMANCE-DATA-2026-06.md` (n=57, real numbers — use these, not aggregates).

**Two hard constraints, both learned expensively here:**
1. **n<30 on this channel is noise.** Do not report a correlation across ten openers as a finding. The honest output is *hypotheses ranked by how cheaply they could be A/B tested*, not a model.
2. **Formulas derived within a video do not survive out of sample** on this channel — that has been tested and written up. So: describe **craft** (what the opener does to the viewer, in what order), never a runtime template.

Output `channel-data/OPENER-CRAFT-SCAN-2026-07-22.md`: what the three best-retained openers do that the three worst don't, stated as testable single-variable swaps. Name what would falsify each.

---

## Closing note — the sweep is done, and it changed the voice canon

The catalogue-wide locked-line sweep **cannot** be run: only #62 and #56 have read-aloud records, and #56's are the render he was handed, not a log of his changes. So there is no reference set for the other videos.

What ran instead was better. #56 is published, so its page could be diffed against **what he actually said on camera**:

| #56 | words | `so` | `but` | ratio | `so`+`but` | `very` |
|---|---|---|---|---|---|---|
| page handed to him | 1,725 | 4.6 | 7.0 | 0.67 | 11.6 | 0.6 |
| delivered, published | 1,589 | 3.1 | 6.3 | **0.50** | **9.4** | **0.0** |

**At the microphone he strips connectors and says `very` zero times.** The long-held belief that these markers "close at the mic" is false in the direction it assumed. Consequences you inherit: **no numeric connector target, no ratio target, and never add a marker on the theory he will say it anyway.** Full entry: `CALIBRATION-CORPUS.md` 62-21.
