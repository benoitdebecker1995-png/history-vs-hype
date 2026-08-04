---
name: production-map
description: 'Routing layer for content-production work in the History vs Hype repo — pipeline-phase→command map, the packaging gate authority model (filters decide, scores inform), mandatory conversational triggers, artifact done-standards, and decision epistemics for content decisions. Use when: working on a video project or any video-projects/ path; deciding which command comes next in the pipeline; the user says "uploaded"/"published"/"is live"/"script locked"/"lock it"/"T1 passed"; any packaging, gate, greenlight, or title/thumbnail-advancement question; citing channel performance data in a recommendation; unsure which reference doc or skill owns a content question. DORMANT for pure code/engineering work (→ codebase-atlas, extending-safely).'
---

# Production Map

ROUTER skill. It tells you WHERE to go and WHAT must fire — it never contains the procedure.
CLAUDE.md (always loaded) has the pipeline summary; this skill adds the decision map, the gate
authority model, and the judgment that isn't written there. If you find yourself explaining HOW
to write a script or do research, you have left this skill's lane — jump to the routed surface.

## Pipeline spine (idea → published)

One row per phase. Commands live in `G:\History vs Hype\.claude\commands\<name>.md`.

| # | Command | What it does | Artifact produced | Gate it enforces |
|---|---|---|---|---|
| 1 | `/greenlight` | Pre-work viability gate: demand, title candidates, thumbnail concept — BEFORE any research | Greenlight verdict + packaging candidates | Demand gate (V1, `tools/PACKAGING_MANDATE.md`) — the ONLY pre-publish verdict |
| 2 | `/research` | Start project / conduct topic research (Phase 1+2, NotebookLM) | `01-VERIFIED-RESEARCH.md` | Runs `packaging_lock.py --validate` before advancing; refuses if BLOCKED |
| 3 | `/script` | Write / revise / review / export scripts | `02-SCRIPT-DRAFT.md` | Voice + structure gates (voice_lint, structure-checker-v2); CTA-in-final-5% hard gate |
| 4 | `/verify` | Fact-check script, extract claims, detect simplifications | `03-FACT-CHECK-VERIFICATION.md` | 100% cross-checked, verdict ✅ APPROVED before filming |
| 5 | `/prep` | Filming preparation: edit guides, B-roll planning, assets | Prep docs in project folder | — |
| 6 | `/thumbnail` | 3 ranked thumbnail concepts from outlier corpus + playbook | Thumbnail concept doc | Thumbnail locked before filming (2-stage gate) |
| — | *(film)* | User records; script must be LOCKED first (see Script lock below) | Rough cut | — |
| 7 | `/editing-guide` | Segment-by-segment editing playbook from rough-cut SRT | Editing guide | — |
| 8 | `/fix` | Fix subtitle errors from auto-transcription | Corrected SRT | — |
| 9 | `/publish` | YouTube metadata, title testing, clip suggestions | `YOUTUBE-METADATA.md` | `/preflight` scorecard before upload; arm the 48h swap protocol BEFORE publish (V5: CTR <2% @48h on >500 impressions → swap title+thumb; 2–4% → swap title; >4% → hold; always to a different pattern) |
| 10 | `/engage` | Comment responses, corrections, feedback management | — | — |
| 11 | `/reconcile` | Sync folder lifecycle, AUTO blocks, derived docs | Updated PROJECT-STATUS + registry | MANDATORY on publish utterance (below) |
| 12 | `/analyze` | Complete post-publish analysis | Post-publish report | Long-form ONLY — NEVER run on Shorts |

Supporting commands (route, don't guess): `/status` next-action + project state · `/next` ranked
topic recs · `/opener` cold-open decision · `/polish` final AI-pattern pass on a locked script ·
`/preflight` full pre-upload scorecard · `/verify-flow-nlm` + `/script-research-pass` deeper
verification passes `/verify` skips for context-economy · `/comment-mine` audience demand (cmd outdated — yt-dlp bot-walled; use the OAuth data-API fallback, see MEMORY) ·
`/curiosity` title psychology (enrichment) · `/retitle` underperformer retitling · `/patterns`,
`/growth` analytics · `/voice`, `/voice-readthrough`, `/voice-clickdrill` voice calibration.

## Gate authority model (packaging model C) — get this exactly right

Authority: `docs/adr/0012-packaging-advancement-is-code-gated.md` + `CONTEXT.md` § Packaging / thumbnail terms.

- **FILTERS decide (pass/fail, all four must PASS):** (1) search-anchor in title
  (`title_scorer.has_search_anchor` — a curated head term OR a verified ≥1,000/mo volume;
  a FAIL on a famous term means "unmeasured", so record it rather than rewriting the title, ADR-0023),
  (2) clickbait brand-gate (no `title_scorer` hard_rejects),
  (3) title↔thumbnail curiosity gap — a judgment field the gate requires be FILLED, (4) thumbnail
  conditions (`thumbnail_checker`; may be PENDING at lock, checked before publish).
- **ENRICHMENT informs, never decides:** `title_scorer` composite (65), `/curiosity` (60), VidIQ
  MCP score, NLM P5. Low value = a REVIEW nudge ("eyeball it"). Enrichment can NEVER upgrade a
  filter FAIL. VidIQ "tends to prioritize clickbaity shit" — its generation suite is REJECT.
- **The record:** `tools/preflight/packaging_lock.py` runs the filters and writes the
  `<!-- AUTO:packaging-lock -->` block in the project's `PROJECT-STATUS.md`. Only that
  checker-owned block counts — a freeform "Locked Packaging" prose note is NOT a lock.
  `--validate` returns BLOCKED unless every mechanical filter passes and the judgment field is
  filled; `/research` refuses to advance on BLOCKED.
- **Verdicts:** no pre-publish number is a verdict except demand (Gate 1). Live CTR is the only
  real clickability verdict (Gate 2). Pre-publish tools are filters-not-predictors (ADR-0007).

**The incident this model exists to prevent (#62 Volhynia):** packaging was "locked" on a single
confident enrichment number — "VidIQ 95/100" — with no record that title_scorer, /curiosity, or
thumbnail_checker ever ran, and no thumbnail concept at all. A confident score is never the verdict.

**Never-do:** treat any score as a packaging verdict · advance via prose note instead of the AUTO
block · let enrichment override a filter FAIL · hand-edit inside any `<!-- AUTO:* -->` zone
(→ data-stores skill for zone rules) · re-introduce a predictive pre-publish score.

**Stale-doc trap:** `tools/PACKAGING_MANDATE.md` V4 still calls title_scorer 65+ a "gate/floor".
ADR-0012 (newer) demoted 65 to recorded enrichment. ADR-0012 + CONTEXT.md win. Two more:
CLAUDE.md's "<1K/mo = hard stop" demand line is stale — the LIVE gate (greenlight.md) is graded:
GO >= 1,000 / CAUTION 500-999 (passes the V1 floor, warn) / STOP < 500 unless a verifiable news
hook; answer demand questions by RUNNING /greenlight, not from the CLAUDE.md number. And
CLAUDE.md's quick-start still lists /sources and /intel — neither exists any more.

## Conversational triggers (MANDATORY — fire regardless of what else is happening)

| User says | You MUST immediately | Why |
|---|---|---|
| "I uploaded / released / published X" / "X is live" / "X went up" | Run `/reconcile <X>`. Do NOT just look up the video; do NOT assume project files are current. Ambiguous X → ask once, then proceed | The utterance IS the write trigger; stale state files were the loudest recorded workflow failure (2026-05-12) |
| "script locked" / "lock it" / "T1 passed" / read-aloud passed top-to-bottom | Run the post-lock delta-mine: (1) consolidate read-aloud notes + version diffs + session corrections into `channel-data/calibration/CALIBRATION-CORPUS.md` (axis-tagged, tiered); (2) append new contradictions to `channel-data/calibration/INTERVIEW-AGENDA.md`; (3) record passes-to-lock in `channel-data/calibration/EVAL-BASELINE.md` | Lock-session deltas are the highest-tier calibration signal and evaporate fast; #56/#57 lessons had to be archaeologically reconstructed |
| Any pushback or correction | Save the derived rule to memory/wiki immediately (project analog: `video-projects/_CORRECTIONS-LOG.md` + affected agent files) — not just an acknowledgment | Global hard rule 1; "I'll remember" is not a process fix |
| "save this idea somewhere" | Create `PROJECT-BRIEF.md` in a new NUMBERED folder under `video-projects/_BACKLOG/` (parked concept — pull to `_IN_PRODUCTION/` when work starts; NEVER a loose folder in `video-projects/` root) with the claim being fact-checked + preliminary findings, status "CONCEPT SAVED" | `.claude/USER-PREFERENCES.md` § COMMENT-DRIVEN RESEARCH |
| `/prompt-mini` request | Save the result as `.claude/commands/<slug>.md`, not chat-only | User wants artifacts, not ephemera (MEMORY.md hard rule) |

Backstops exist (Routine 6 auto-archives missed publishes; `/reconcile` flags un-mined locked
scripts) but backstops are for MISSES — the conversational trigger is the contract.

## Artifact standards (what "done" means)

**`01-VERIFIED-RESEARCH.md` is done when:** every fact marked ✅/⏳/❌ with 90%+ ✅ before any
script writing; Phase-2 NotebookLM verification completed (never skipped — it's the channel's
competitive advantage); every claim tier-tagged; verbatim quotes with page numbers, load-bearing
ones verified against RAW `nlm source content` (never `notebook_query` synthesis — it fabricates);
unverifiable claims excluded or flagged, never included on plausibility. Enforcement rules
(NLM-anchor, tier discipline, stop-flags) live in the **historian skill** — read it before filing
any claim.

**"Script locked" means:** the USER's T1 read-aloud passed top-to-bottom. Only the user declares
a lock — never infer or self-declare it. Lock fires the delta-mine trigger (table above). After
lock: teleprompter is a derived render of the locked SCRIPT.md, never hand-edited; changes go
through the script file. `03-FACT-CHECK-VERIFICATION.md` must be ✅ APPROVED before filming.

**Lifecycle folders (the 5 lines that matter):**
1. `_IN_PRODUCTION/` → `_READY_TO_FILM/` → `_ARCHIVED/published/` — never loose folders in `video-projects/` root.
2. Folder location is DERIVED: filesystem + `tools/youtube_analytics/analytics.db` decide; `/reconcile` moves folders — you don't move them by hand mid-conversation.
3. `_BACKLOG/` is OUTSIDE the lifecycle: parked work, invisible to all scanners; pull back to `_IN_PRODUCTION/` to resume; never for filmed/published work.
4. Per-folder `PROJECT-STATUS.md`: AUTO block at top is machine-owned; hand-written narrative lives below `<!-- /AUTO:reconcile -->`.
5. Before creating any file: read root `video-projects/PROJECT_STATUS.md` → Glob for an existing folder → confirm lifecycle stage.

## Decision epistemics for content decisions

The owner is scientific: data-backed, test-and-measure. These rules gate every recommendation:

- **n<30 channel data = noise.** Never cite channel-specific CTR/pattern numbers as constraints
  (~57 videos, most patterns n<10). Use niche-wide corpora (n=85+) for decisions; channel numbers
  are info-only. Source: `MEM:feedback-channel-data-too-small.md`.
- **Distribution, not aggregates.** One video (Guatemala) = 51% of all long-form traffic; any
  channel-wide aggregate can be one-row-driven. Report distribution/concentration, not just means.
- **Holdout discipline.** Any pattern derived from best/worst subsets is a HYPOTHESIS until tested
  on the rest of the distribution — four opening formulas ALL died out-of-sample (2026-06-26).
  Never wire an extremes-derived pattern into tools or advice without a holdout pass.
- **Single-variable swaps.** At current traffic, learn via before/after swaps changing title OR
  thumbnail — never both (re-blends CTR, teaches nothing). Judge on new-viewer CTR.
- **Famous-gate.** Before any "you've been taught wrong" myth framing, verify the audience
  actually HOLDS the belief; otherwise use assumption-first framing. Packaging pays only once the
  topic is famous (FAME = #1 validated CTR driver).
- **Whitespace = watch deep results.** "Nobody covers X" is a hypothesis until you've actually
  watched/read the top deep results (and non-English framings). Comment-demand on a shallow video
  lies; a competitor-gap agent's claim was disproven by pulling the actual transcript.
- **Tools confabulate; the local stores are ground truth.** Verify every YT-Studio/VidIQ number
  against the store that owns it — views/retention/traffic → `analytics.db`; CTR → keywords.db
  `ctr_snapshots` (analytics.db's API CTR field is NULL) — before citing it (→ data-stores skill).

## Which surface handles X (router)

| Question is about | Go to | Note |
|---|---|---|
| How to write the script — voice, style, structure, delivery | `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` index (routes to PARTS 1-5 sibling files) + `.claude/REFERENCE/VOICE-PROFILE.md` | VOICE-PROFILE.md is CANONICAL — it wins on any conflict |
| Research discipline — filing claims, quotes, tiers, NLM, stop-flags | **historian skill** (`.claude/skills/historian/SKILL.md`) | Owns all research-mode rules; dormant only during project mechanics |
| Titles / thumbnails — rules, patterns, protocols | `tools/PACKAGING_MANDATE.md` + `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md` | Read with the ADR-0012 correction above (65 = enrichment) |
| Gate/advancement mechanics | `tools/preflight/packaging_lock.py` + `docs/adr/0012-packaging-advancement-is-code-gated.md` | This skill's Gate section is the digest; the ADR is authority |
| Per-video state — where is project X, what's next for it | that folder's `PROJECT-STATUS.md` + `/status` | Never trust a stale registry line over the folder + `analytics.db` |
| Channel performance numbers, staleness, which table holds what | **data-stores skill** | analytics.db / keywords.db / intel.db live there |
| Topic selection / what to make next | `channel-data/TOPIC-PIPELINE.md` + `tools/TOPIC-RUBRIC.md` + `/next` | Rubric v2 is canonical for scoring |
| Opening hooks / thesis throughline | `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` / `.claude/REFERENCE/THESIS-DISCIPLINE.md` | Remember: no opening formula survived holdout — templates are craft, not predictors |

## Related skills

- **project-onboarding** — you're new to the repo entirely, or need the two-surface map (channel ops vs engineering) and the read-order for a task type.
- **data-stores** — before querying or citing any number from analytics.db / keywords.db / intel.db, or touching anything near an `<!-- AUTO: -->` block.
- **historian** (`.claude/skills/historian/SKILL.md`) — the moment you act as a researcher: NLM queries, `_IN_PRODUCTION/` folders, editing `01-VERIFIED-RESEARCH.md`, any `/research` subcommand.
