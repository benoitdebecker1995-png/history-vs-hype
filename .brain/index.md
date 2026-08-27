# .brain/index.md — Master Knowledge Catalog

*Auto-maintained by Routine 5 (brain hygiene, nightly). Last updated: 2026-08-27*

---

## 1. Multi-Root Map
<!-- MANUAL — update when structure changes -->

| Root | Path | Scope | Owner-of-Truth | Freshness |
|------|------|-------|----------------|-----------|
| `channel-data/` | `G:\History vs Hype\channel-data\` | Channel analytics, CTR baselines, competitor tracking, POST-PUBLISH-ANALYSIS, topic pipeline, CHANNEL_ANALYTICS_MASTER | Daily routines (1-3) | Live |
| `tools/benchmark/` | `G:\History vs Hype\tools\benchmark\` | Title/thumbnail/hook playbooks, WAVE analyses (1-8), outlier corpus, structural findings | Research sprints | Versioned |
| `.brain/` | `G:\History vs Hype\.brain\` | Verified quotes/sources, cross-source threads, methodology, routine inbox | Routine 5 nightly | Nightly |
| `~/llm-brain/wiki/` | `C:\Users\Benoi\llm-brain\wiki\` | Cross-project entities, concepts, quotes by book, global methodology | Per-project ingestion | Per-session |
| `memory/` | `C:\Users\Benoi\.claude\projects\G--History-vs-Hype\memory\` | User behavior rules, feedback patterns, channel stats, workflow notes | Per-session capture | Per-session |

---

## 2. Knowledge-by-Question
<!-- AUTO:routine-5 — appended when new artifact types appear -->

> **Precedence (added 2026-08-27).** `AGENTS.md` is the active operating contract; `CHANNEL.md` is
> active channel state; `channel-data/creator-model/OPERATING-MODEL.md` is active creator authority.
> Per `channel-data/README.md`, most top-level `channel-data/` files below are historical laboratory —
> analyses, generated feeds, experiment records — and **their presence here is not current
> instruction.** Old channel laws, fixed thresholds, and composite opportunity/title/thumbnail/
> retention scores must not be read as verdicts. Per `CLAUDE.md`, `.claude/` is migration history and
> is not loaded during normal work; rows pointing into it are archival routing only.

| I want to know... | Look in... |
|-------------------|-----------|
| **Active operating contract** | `AGENTS.md` (+ `CLAUDE.md` adapter) |
| **Active channel state** | `CHANNEL.md` |
| **Active creator authority (v3)** | `channel-data/creator-model/OPERATING-MODEL.md`; evidence in `READTHROUGH-PATCH-2026-08-17.md`, `VOICE-CALIBRATION-JUNE-2026.md` |
| Raw creator speech (query-only voice evidence, NOT factual evidence) | `channel-data/creator-model/VOICE-EVIDENCE.md`, `creator-model/SOURCE.md` |
| Why packaging is the binding constraint (not frequency, not writing) | `channel-data/PACKAGING-DIAGNOSIS-2026-08-26.md` |
| Who is actually watching (two non-overlapping audiences) | `channel-data/audience/AUDIENCE-2026-08-24.md` |
| Corrections viewers raised in comments | `channel-data/audience/CORRECTIONS-2026-08-24.md`, `audience/VERIFICATION-2026-08-26.md` |
| Architecture decisions (why a seam is shaped as it is) | `docs/adr/` (0001–0028) |
| Channel-data boundary — what is laboratory vs instruction | `channel-data/README.md` |
| Front-room evidence packets (source, grain, as-of date) | `tools/front_room.py` |
| Title CTR patterns (niche-wide, n=388) | `channel-data/COMPETITOR-TITLE-DATABASE.md`, `tools/benchmark/SCRIPT-PATTERN-ANALYSIS.md` |
| Per-topic SERP shelf structure (what the top 12 on a query actually look like) | `channel-data/serp-studies/titles/` (75 studies) + `channel-data/serp-studies/` (topic-level). ⚠ Each study carries its own "what this cannot tell you" block: top-12 on a handful of queries **never** establishes that a competitor does not exist — verify by video ID before claiming absence |
| Channel CTR baselines (my videos) | `channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md` (per-video), `channel-data/CHANNEL_ANALYTICS_MASTER.md` |
| Per-video retention curves (raw, n=57) | `channel-data/CHANNEL-PERFORMANCE-DATA-2026-06.md` (first30/body, traffic, drop-points — directional) |
| Why long-form underperforms (holdout-tested) | `channel-data/LONGFORM-FAILURE-DIAGNOSIS-2026-06.md`, `channel-data/calibration/OPENER-RETENTION-DIAGNOSIS.md` |
| CTR title + thumbnail formula (derived, my data, n=56) | `channel-data/CTR-TITLE-FORMULA-2026-06.md`, `channel-data/CTR-THUMBNAIL-FINDINGS-2026-06.md` |
| Causal A/B + traffic-source CTR split, per-video funnel autopsy | `channel-data/AB-TEST-AND-TRAFFIC-CTR-2026-06.md`, `channel-data/FLOP-AUTOPSY-TABLE.md` |
| Thumbnail formulas for this niche | `tools/benchmark/THUMBNAIL-NICHE-ANALYSIS.md`, `tools/benchmark/PER-CHANNEL-THUMBNAIL-PLAYBOOK.md` |
| Thumbnail overlay operation map | `tools/benchmark/TITLE-TO-OVERLAY-OPERATION-MAP.md` |
| Outlier thumbnail corpus | `tools/benchmark/OUTLIER-THUMBNAIL-CORPUS.md` |
| Competitor outlier findings (what breaks out) | `channel-data/COMPETITION-ANALYSIS-TOP5-2026-03.md`, `memory/competitor-findings.md` |
| Today's competitor uploads | `.brain/_inbox/competitor-drops-YYYY-MM-DD.md` (Routine 1 output) |
| Modern relevance hooks for active projects | `.brain/_inbox/modern-relevance-YYYY-MM-DD.md` (Routine 2 output) |
| Verified quotes — Treaty of Tripoli | `~/llm-brain/wiki/entities/treaty-of-tripoli.md`, `~/llm-brain/wiki/entities/article-11-treaty-of-tripoli.md` |
| Verified quotes — Berlin Conference | `~/llm-brain/wiki/entities/berlin-conference-1884.md`, `~/llm-brain/wiki/quotes/` |
| Verified quotes — Chagos | `~/llm-brain/wiki/entities/chagos-archipelago.md`, `~/llm-brain/wiki/concepts/double-betrayal-chagos.md` |
| Writing voice and script rules | `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` (authoritative, read before ANY script) |
| Hook patterns and formulas | `tools/benchmark/WAVE-8-SCRIPT-TECHNIQUES.md`, `memory/data-patterns.md` |
| Hook type performance (specificity_bomb vs cold_fact) | `memory/competitor-findings.md` (85-video corpus) |
| Script structure patterns (WAVE analyses) | `tools/benchmark/WAVE-2-STRUCTURAL-FINDINGS.md`, `tools/benchmark/TRANSCRIPT-STRUCTURE-ANALYSIS.md` |
| Retention curve benchmarks | `memory/analytics-findings.md`, `memory/data-patterns.md` |
| Fact-checking protocol and source hierarchy | `.claude/REFERENCE/fact-checking-protocol.md` |
| Anti-oversimplification rules | `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md` |
| NotebookLM source standards | `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md` |
| Which Claude model to use for which task | `.brain/methodology/gemini-routing.md` |
| Gemini headless dispatch | `.claude/commands/gemini.md` |
| Topic pipeline / greenlight queue | `channel-data/TOPIC-PIPELINE.md` |
| Greenlight protocol | `tools/PACKAGING_MANDATE.md`, `channel-data/PACKAGING-REFRESH.md` |
| A/B testing log | `channel-data/AB-TESTING-LOG.md` |
| User behavior rules (feedback) | `memory/feedback-behavior.md`, `memory/feedback-content.md` |
| Article-writer rules (v5.3) | `.claude/agents/article-writer.md` |
| Newsletter rules | `memory/feedback-newsletter.md` |
| Workflow audit findings (2026-04-14) | `memory/workflow-audit.md`, `docs/archive/WORKFLOW-AUDIT-2026-04-14.md` |
| Thesis discipline methodology | `.claude/REFERENCE/THESIS-DISCIPLINE.md` |
| Channel health anomalies | `.brain/_inbox/channel-health-YYYY-MM-DD.md` (Routine 3 output) |
| Stale in-production projects | `.brain/_inbox/stale-projects-YYYY-MM-DD.md` (Routine 4 output) |
| Script technique log | `channel-data/TECHNIQUE-USAGE-LOG.md` |
| Format experiment results | `channel-data/FORMAT-EXPERIMENTS/` |
| Brain health status | `.brain/index.md §5 Health Signals` (this file) |

---

## 3. Active Topics
<!-- MANUAL — auto-refreshed by Routine 4 (stale projects, daily) -->

| Topic | Lifecycle | Phase | Last Touched |
|-------|-----------|-------|--------------|
| `62-volhynia-massacre-untranslated-2026` | `_IN_PRODUCTION` | editing (committed next upload) | 2026-08-27 |
| `37-untranslated-vichy-statut-juifs-2026` | `_IN_PRODUCTION` | ⚠ unknown — no status file, `_research/` only | 2026-08-17 |
| `67-donation-constantine-forgery-2026` | `_IN_PRODUCTION` | script v4 (not locked; 15 `[CL]` open) | 2026-08-14 |
| `65-enigma-polish-cipher-bureau-2026` | `_IN_PRODUCTION` | pre-research (title lock pending owner) | 2026-07-30 |
| `64-ancient-dna-aryan-weaponised-2026` | `_IN_PRODUCTION` | pre-research (NLM auth blocked) | 2026-07-29 |
| `36-panama-canal-deconcini-2026` | `_IN_PRODUCTION` | script v2 (fact-check approved, not locked) | 2026-07-28 |
| `55-falklands-malvinas-2026` | `_IN_PRODUCTION` | research (Stage A locked, B pending) | 2026-07-28 |
| `Tariffs` | `_IN_PRODUCTION` | thumbnail assets only — archive candidate | 2026-07-25 |
| `35-gibraltar-treaty-utrecht-2026` | `_IN_PRODUCTION` | thumbnail assets only — archive candidate | 2026-07-25 |
| `27-peru-2025` | `_IN_PRODUCTION` | thumbnail assets only — archive candidate | 2026-07-25 |
| `23-christmas-origins-2025` | `_IN_PRODUCTION` | thumbnail assets only — archive candidate | 2026-07-25 |
| `10-dark-ages-2025` | `_IN_PRODUCTION` | thumbnail assets only — archive candidate | 2026-07-25 |
| `60-guadalupe-hidalgo-dispossession-2026` | `_IN_PRODUCTION` | script draft (not locked, awaiting T1) | 2026-07-22 |
| `61-spanish-colonization-black-legend-2026` | `_IN_PRODUCTION` | research complete (title lock pending) | 2026-07-22 |
| `63-leopold-congo-cobalt-2026` | `_IN_PRODUCTION` | pre-research (NLM auth blocked) | 2026-07-22 |
| `58-kurdistan-statelessness-2026` | `_READY_TO_FILM` | fact-checked | 2026-06-14 |
| `6-bir-tawil-2025` | `_ARCHIVED/published` | published | 2026-05-12 |
| `30-belavezha-accords-2025` | `_ARCHIVED/published` | published | 2026-05-12 |
| `28-vance-part-2-review-2025` | `_ARCHIVED/published` | published | 2026-05-12 |
| `24-iran-1953-coup-2025` | `_ARCHIVED/published` | published | 2026-05-12 |
| `19-flat-earth-medieval-2025` | `_ARCHIVED/published` | published | 2026-05-12 |
| `14-chagos-islands-2025` | `_ARCHIVED/published` | published | 2026-05-12 |
| `1-somaliland-2025` | `_ARCHIVED/published` | published | 2026-05-12 |

---

## 4. Recently Added / Changed (last 14 days)
<!-- AUTO:routine-5 — prepend new entries; entries older than 14 days are dropped -->

*Dates are the artifact's own as-of date. The August architecture work was authored across 14–26 Aug
and landed in git on 2026-08-27, which is when hygiene first saw it (the run before that was
2026-07-29). ⚠ Because bullets are keyed to the artifact's date and not the day this routine noticed
them, entries can age out of the 14-day window within a day or two of first appearing — see the
note at the end of `_inbox/brain-hygiene-2026-08-27.md`.*

- 2026-08-27 — `AGENTS.md` / `CLAUDE.md` / `CHANNEL.md` — the contract layer replaced the command-driven Claude workflow: `AGENTS.md` is the shared operating contract, `CHANNEL.md` the active channel state, `CLAUDE.md` now a thin adapter pointing at both
- 2026-08-27 — `channel-data/README.md` — declares the channel-data boundary: most top-level files are historical laboratory, not current instruction; old laws/thresholds/composite scores must not be used as verdicts
- 2026-08-27 — `tools/front_room.py` + `tools/sqlite_access.py`, `packaging_intel.py`, `packaging_autopilot.py`, `title_scorer.py`, `voice_lint.py`, `preflight/*` — the August tooling architecture (front-room evidence packets carrying source, grain, and as-of date)
- 2026-08-27 — `docs/adr/0023`–`0028` — six new ADRs: search-anchor fame is measured not listed; analytics/CTR reads carry their grain; read-only SQLite on lockless workspace drives; package history is chronological observation; creator-model v3 is query-routed and routes strategy + learning
- 2026-08-26 — `channel-data/PACKAGING-DIAGNOSIS-2026-08-26.md` — the evidence that packaging, not frequency and not writing, is the binding constraint; sourced to the Studio impressions/CTR export (Jul 2025–Jul 2026) plus Analytics-API retention
- 2026-08-26 — `channel-data/audience/VERIFICATION-2026-08-26.md` — verification pass over the comment-derived corrections
- 2026-08-24 — `channel-data/audience/AUDIENCE-2026-08-24.md` — first read of the channel's own comments (~600–700 across ten videos); finds there is no single audience but two that don't overlap
- 2026-08-24 — `channel-data/audience/CORRECTIONS-2026-08-24.md` — corrections viewers raised, extracted from the same comment read
- 2026-08-14 — `channel-data/creator-model/OPERATING-MODEL.md` — creator operating model v3 imported from the v3 docx; active creator authority, amended 2026-08-26 with the 17 Aug read-through patch (V1–V4, B1–B8)
- 2026-08-14 — `docs/audits/CREATOR-MODEL-V3-WHOLE-PROJECT-AUDIT-2026-08-14.md` — whole-project audit accompanying the v3 import

*Pruned 2026-08-27 (22:00 run): the 2026-08-01 `serp-studies/titles/` entry aged out of the 14-day
window. It was not dropped — the corpus now has a permanent §2 row, which is where a standing
lookup belongs; §4 is only the recency feed.*

---

## 5. Health Signals
<!-- AUTO:routine-5 — populated by nightly brain-lint pass -->

```
LAST LINT: 2026-08-27 22:00  (second run today; a 15:44 run preceded it)
Queue:                           0 items in .brain/_queue/
Stale items (>90d unverified):   0 real (12 grep hits are this routine's own _inbox reports
                                 quoting its own template)
Orphan pages (no inbound links): 0 — re-verified this run, not inherited. sources/ = 228 notes,
                                 every slug mentioned from topics/ (78); threads/ still empty (0)
Open contradictions:             UNKNOWN — ~/llm-brain/wiki/contradictions/ is outside the working
                                 directory; the sandbox refuses the read. NOT recorded as zero.
Dead links:                      0 external (no URLs exist in .brain/**/*.md at all — the check is
                                 vacuous here, not passing)
                                 0 internal — all 32 §2 targets re-resolved this run
Open lint findings:              2 needing a human, all carried from the 15:44 run, none fixable
                                 from inside this routine's write scope:
                                 - §1 `~/llm-brain/wiki/` root does not exist on disk
                                   (MANUAL section; planned or abandoned?)
                                 - STEP 3c glob misses migrated projects (see §6)
Next lint scheduled:             tomorrow 22:00 local (Routine 5)
```

---

## 6. Cross-Root Links
<!-- AUTO:routine-5 — wiki concepts referenced by current projects -->

**Active projects with a research file (7):**

Old shape — `01-VERIFIED-RESEARCH.md` (5): `36-panama-canal-deconcini-2026`,
`55-falklands-malvinas-2026`, `60-guadalupe-hidalgo-dispossession-2026`,
`61-spanish-colonization-black-legend-2026`, `63-leopold-congo-cobalt-2026`

Three-file shape — `RESEARCH.md` (2): `62-volhynia-massacre-untranslated-2026`,
`67-donation-constantine-forgery-2026`

- **Zero `~/llm-brain/` references anywhere in `_IN_PRODUCTION/`.** Verified by grepping every file
  under the tree, not only the research files — so §6's premise holds more broadly than it claims.
  The wiki crossref layer is, in practice, dormant for current work. *Re-checked 2026-08-27 22:00:
  still zero; 15 projects in `_IN_PRODUCTION`, 7 with a research file, 8 with none.*
- ⚠ **The routine's own STEP 3c glob is stale.** It targets `01-VERIFIED-RESEARCH.md` only, so it
  silently misses the two migrated projects (#62, #67) and would keep missing every project that
  migrates next. The routine spec in `.claude/routines/brain-hygiene.md` needs amending to glob both
  names. Logged, not fixed — editing the routine spec is outside this run's write scope.
- Remaining `_IN_PRODUCTION` projects carry no research file at all.
- *55-falklands-malvinas-2026 resumed from `_BACKLOG` 2026-07-25 — now carried in the active set.*
- *59-israel-palestine-partition-offer-2026 published 2026-07-05 (yt:OHWq4jY8iAY) — left `_IN_PRODUCTION`; no wiki crossrefs to archive.*

**Prior projects (archive crossref):**

*Treaty of Tripoli:*
- `~/llm-brain/wiki/entities/treaty-of-tripoli.md`
- `~/llm-brain/wiki/entities/article-11-treaty-of-tripoli.md`
- `~/llm-brain/wiki/entities/joel-barlow.md`
- `~/llm-brain/wiki/entities/snouck-hurgronje.md`
- `~/llm-brain/wiki/concepts/article-11-arabic-discrepancy.md`

*Berlin Conference:*
- `~/llm-brain/wiki/entities/berlin-conference-1884.md`
- `~/llm-brain/wiki/entities/leopold-ii.md`
- `~/llm-brain/wiki/entities/roger-casement.md`
- `~/llm-brain/wiki/concepts/effective-occupation.md`
- `~/llm-brain/wiki/concepts/ethnic-partition-of-africa.md`

*Chagos Islands:*
- `~/llm-brain/wiki/entities/chagos-archipelago.md`
- `~/llm-brain/wiki/concepts/double-betrayal-chagos.md`
- `~/llm-brain/wiki/concepts/strategic-island-concept.md`

**Active methodology (all projects):**
- `~/llm-brain/wiki/concepts/gemini-claude-routing.md`
- `~/llm-brain/wiki/concepts/llm-wiki-pattern.md`
- `~/llm-brain/wiki/concepts/rag-vs-wiki.md`
