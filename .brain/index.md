# .brain/index.md — Master Knowledge Catalog

*Auto-maintained by Routine 5 (brain hygiene, nightly). Last updated: 2026-06-13*

---

## 1. Multi-Root Map
<!-- MANUAL — update when structure changes -->

| Root | Path | Scope | Owner-of-Truth | Freshness |
|------|------|-------|----------------|-----------|
| `channel-data/` | `D:\History vs Hype\channel-data\` | Channel analytics, CTR baselines, competitor tracking, POST-PUBLISH-ANALYSIS, topic pipeline, CHANNEL_ANALYTICS_MASTER | Daily routines (1-3) | Live |
| `tools/benchmark/` | `D:\History vs Hype\tools\benchmark\` | Title/thumbnail/hook playbooks, WAVE analyses (1-8), outlier corpus, structural findings | Research sprints | Versioned |
| `.brain/` | `D:\History vs Hype\.brain\` | Verified quotes/sources, cross-source threads, methodology, routine inbox | Routine 5 nightly | Nightly |
| `~/llm-brain/wiki/` | `C:\Users\Benoi\llm-brain\wiki\` | Cross-project entities, concepts, quotes by book, global methodology | Per-project ingestion | Per-session |
| `memory/` | `C:\Users\Benoi\.claude\projects\D--History-vs-Hype\memory\` | User behavior rules, feedback patterns, channel stats, workflow notes | Per-session capture | Per-session |

---

## 2. Knowledge-by-Question
<!-- AUTO:routine-5 — appended when new artifact types appear -->

| I want to know... | Look in... |
|-------------------|-----------|
| Title CTR patterns (niche-wide, n=388) | `channel-data/COMPETITOR-TITLE-DATABASE.md`, `tools/benchmark/SCRIPT-PATTERN-ANALYSIS.md` |
| Channel CTR baselines (my videos) | `channel-data/analyses/POST-PUBLISH-ANALYSIS-*.md` (per-video), `channel-data/CHANNEL_ANALYTICS_MASTER.md` |
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
| Anti-oversimplification rules | `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` |
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
| `59-israel-palestine-partition-offer-2026` | `_IN_PRODUCTION` | fact-checked | 2026-06-08 |
| `58-kurdistan-statelessness-2026` | `_READY_TO_FILM` | fact-checked | 2026-06-07 |
| `1-sykes-picot-2025` | `_READY_TO_FILM` | filmed | 2026-05-11 |

---

## 4. Recently Added / Changed (last 14 days)
<!-- AUTO:routine-5 — prepend new entries; entries older than 14 days are dropped -->

- 2026-06-13 — `video-projects/_IN_PRODUCTION/60-guadalupe-hidalgo-dispossession-2026/` — new project scaffolded (01-VERIFIED-RESEARCH, SCRIPT, 03-FACT-CHECK, PROJECT-STATUS, _research preliminary brief + NotebookLM source list + Gemini wiki cache)
- 2026-06-13 — `channel-data/serp-studies/titles/guadalupe-hidalgo-2026-06-13.{json,md}` — SERP title shelf study for Guadalupe Hidalgo
- 2026-06-13 — `.claude/routines/reconcile-daily.md` + `run-reconcile.ps1` — Routine 6 registered as claude-driven `HvH-Reconcile` task (auto-publish-only backstop)
- 2026-06-13 — `.claude/routines/{brain-hygiene,channel-health-snapshot,stale-project-nudge}.md` — Routine 7 `HvH-GrowthRefresh` analytics.db refresh wiring + channel-health query repair
- 2026-06-13 — `CLAUDE.md` — Routine 6/7 backstop chain documented (07:45 refresh → 08:00 health → 08:30 reconcile)
- 2026-06-11 — `.claude/agents/script-writer-v2.md` — v17.0: Fable Phase 3 retention re-tier (VALIDATED/HEDGE/RETIRED), +Rule 47 retention-zone discipline
- 2026-06-11 — `.claude/agents/script-writer-v2-CHANGELOG.md` — v17.0 changelog entry
- 2026-06-11 — `.claude/agents/structure-checker-v2.md` — Wave 11: +BE early-zone authority, +BF late-quarter; A/B/U demoted to WARNING
- 2026-06-11 — `.claude/commands/greenlight.md` — wired to TOPIC-RUBRIC v2 scoring
- 2026-06-11 — `.claude/commands/publish.md` — Fable-pass updates
- 2026-06-11 — `.claude/REFERENCE/VOICE-PROFILE.md` — voice fingerprint refinements (Phase 2 lint alignment)
- 2026-06-11 — `channel-data/BREAKOUT-HYPOTHESES.md` — H1/H2/H4 pre-registered for Panama + #59
- 2026-06-11 — `channel-data/fable-digests/PHASE-2-VOICE-LINT-SPEC.md` — voice-lint mechanization spec
- 2026-06-11 — `channel-data/fable-digests/PHASE-3-RETENTION-ADJUDICATION.md` — retention rule adjudication digest
- 2026-06-11 — `channel-data/fable-digests/PHASE-5-COHERENCE-REPORT-2026-06-11.md` — Opus coherence sweep; corpus coherent for #59 + Panama
- 2026-06-11 — `channel-data/patterns/TRAFFIC-SOURCE-ANALYSIS.md` — one-video-distortion banner added (Guatemala 51%)
- 2026-06-11 — `channel-data/serp-studies/titles/` — 5 SERP title studies: adwa-wuchale, brest-litovsk, panama-canal, suez-1956, unequal-treaties
- 2026-06-11 — `channel-data/TOPIC-PIPELINE.md` — pipeline re-ranked under TOPIC-RUBRIC v2
- 2026-06-11 — `channel-data/youtube-intelligence.md` — intelligence refresh
- 2026-06-11 — `CLAUDE.md` — Critical Reminder 13 softened (years/colons = hedge, not ban)
- 2026-06-11 — `tools/benchmark/outlier_title_dissector.py` — title scorer v5 adjudication
- 2026-06-11 — `tools/PACKAGING_MANDATE.md` — Fable Phase 1 re-tiered mandate
- 2026-06-11 — `tools/TOPIC-RUBRIC.md` — v2 canonical small-channel topic rubric (gates + 30/20/25/10/10/5 weights + POCKET flag)
- 2026-06-11 — `tools/voice_lint.py` + `tools/tests/voice-fixtures/` — voice linter + gold/control fixtures
- 2026-06-11 — `video-projects/_IN_PRODUCTION/36-panama-canal-deconcini-2026/` — pulled from _BACKLOG, greenlit; SCRIPT.md, RESEARCH-VIABILITY.md, 03-FACT-CHECK-VERIFICATION.md, PROJECT-STATUS.md, _research/00-PRELIMINARY-BRIEF.md touched
- 2026-06-11 — `graphify-out/` — 3 new graph reports + 5 converted research docs (generated artifacts)

---

## 5. Health Signals
<!-- AUTO:routine-5 — populated by nightly brain-lint pass -->

```
LAST LINT: 2026-06-13 22:00
Stale items (>90d unverified):  0
Orphan pages (no inbound links): 0 (sources/ + threads/ empty)
Open contradictions:             0 (wiki/contradictions/ absent — skipped)
Next lint scheduled:             tomorrow 22:00 local (Routine 5)
```

---

## 6. Cross-Root Links
<!-- AUTO:routine-5 — wiki concepts referenced by current projects -->

**Active projects (59-israel-palestine-partition-offer-2026, 36-panama-canal-deconcini-2026, 60-guadalupe-hidalgo-dispossession-2026):**
- No `~/llm-brain/` wiki references in any active project's `01-VERIFIED-RESEARCH.md` yet

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
