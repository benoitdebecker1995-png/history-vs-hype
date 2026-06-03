# .brain/index.md — Master Knowledge Catalog

*Auto-maintained by Routine 5 (brain hygiene, nightly). Last updated: 2026-05-05*

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
| Workflow audit findings (2026-04-14) | `memory/workflow-audit.md`, `WORKFLOW-AUDIT-2026-04-14.md` |
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
| `56-no-lassos-atlantic-slave-trade-origin-2026` | `_READY_TO_FILM` | filmed | 2026-06-03 |
| `59-israel-palestine-partition-offer-2026` | `_IN_PRODUCTION` | fact-checked | 2026-06-03 |
| `58-kurdistan-statelessness-2026` | `_READY_TO_FILM` | filming-ready | 2026-06-03 |
| `57-piri-reis-map-ottoman-2026` | `_READY_TO_FILM` | filmed | 2026-06-03 |
| `1-sykes-picot-2025` | `_READY_TO_FILM` | filmed | 2026-05-11 |

---

## 4. Recently Added / Changed (last 14 days)
<!-- AUTO:routine-5 — prepend new entries; entries older than 14 days are dropped -->

- 2026-05-05 — 5 daily routines live: Routines 1-2 (Cloud), 3-5 (Desktop Task Scheduler, State: Ready)
- 2026-05-05 — Gemini retrofit complete: wiki-researcher, claims-extractor, competitor-gap, research-organizer, fact-checker all dispatch bulk reads to Gemini
- 2026-05-05 — Schema contracts locked: all 5 retrofitted agents have `.contract.md` + harness at `tools/agent_contract_check.py`
- 2026-05-05 — Model routing applied: structure-checker-v2 → Opus; all other agents confirmed per matrix
- 2026-05-05 — `.brain/` skeleton created: `README.md`, `index.md`, `methodology/`
- 2026-05-05 — `.brain/methodology/gemini-routing.md` — model routing matrix (Opus/Sonnet/Haiku/Gemini per agent)
- 2026-05-05 — `.brain/methodology/handoff-playbook.md` — Gemini↔Claude handoff recipes
- 2026-05-05 — `.brain/methodology/brain-map.md` — multi-root knowledge architecture
- 2026-05-05 — `.claude/commands/gemini.md` — Gemini headless dispatch command (4 task types)
- 2026-05-05 — `~/llm-brain/wiki/concepts/gemini-claude-routing.md` — cross-project routing doc added

---

## 5. Health Signals
<!-- AUTO:routine-5 — populated by nightly brain-lint pass -->

```
LAST LINT: not yet run
Stale items (>90d unverified):  —
Orphan pages (no inbound links): —
Open contradictions:             —
Next lint scheduled:             tonight 22:00 local (Routine 5 Desktop task)
```

---

## 6. Cross-Root Links
<!-- AUTO:routine-5 — wiki concepts referenced by current projects -->

**Treaty of Tripoli (active project):**
- `~/llm-brain/wiki/entities/treaty-of-tripoli.md`
- `~/llm-brain/wiki/entities/article-11-treaty-of-tripoli.md`
- `~/llm-brain/wiki/entities/joel-barlow.md`
- `~/llm-brain/wiki/entities/snouck-hurgronje.md`
- `~/llm-brain/wiki/concepts/article-11-arabic-discrepancy.md`

**Berlin Conference (prior project, archive crossref):**
- `~/llm-brain/wiki/entities/berlin-conference-1884.md`
- `~/llm-brain/wiki/entities/leopold-ii.md`
- `~/llm-brain/wiki/entities/roger-casement.md`
- `~/llm-brain/wiki/concepts/effective-occupation.md`
- `~/llm-brain/wiki/concepts/ethnic-partition-of-africa.md`

**Chagos Islands (prior project, archive crossref):**
- `~/llm-brain/wiki/entities/chagos-archipelago.md`
- `~/llm-brain/wiki/concepts/double-betrayal-chagos.md`
- `~/llm-brain/wiki/concepts/strategic-island-concept.md`

**Active methodology (all projects):**
- `~/llm-brain/wiki/concepts/gemini-claude-routing.md`
- `~/llm-brain/wiki/concepts/llm-wiki-pattern.md`
- `~/llm-brain/wiki/concepts/rag-vs-wiki.md`
