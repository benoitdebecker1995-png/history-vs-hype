# CODE-MAP.md — Project Code Structure (from graphify)

Distilled from `graphify-out/GRAPH_REPORT.md` (built from commit `562996b1`, 2026-05-25). AST-only — no semantic extraction of doc content. Load this instead of grepping the whole tree when answering "where does X live" or "what depends on Y."

## Graph caveats (read first)
- **AST-only run** — code-structure accurate, doc-content blind. Token cost was 0; semantic LLM pass never ran.
- **Worktree duplication** — every real community has a twin from `.claude/worktrees/bridge-cse_012ehbZ45qGePLbtARZ4qoxP/`. Twins listed below as `(#N / #M)`. Treat as one cluster.
- **Communities are unlabeled** — graphify Step 5 was skipped, so all 7,288 communities are named `"Community N"`. This file is the human-readable label set.
- **65% of nodes (60,952) are isolated singletons** — language codes, primitive type stubs (`str`, `int`, `bool`), filename fragments. Ignore unless following a specific edge.
- **Total: 93,914 nodes / 97,994 edges across 3,843 files.**

## God Nodes (real, de-noised)

The report's god-node list has `automatic_captions` duplicated 7× (YouTube API caption registries from 7 channel extractions). Real load-bearing abstractions:

| Node | Edges | Role |
|---|---|---|
| `KeywordDB` | 302 | Central SQLite store in `tools/discovery/database.py`. 220 of those edges are INFERRED — `Path`/`bool`/`Any` signature noise, not real coupling. |
| `canonical_map` | 267 | Author/publisher canonicalization registry (Community #0). Drives the source library renamer. |
| `ScriptParser` | (high betweenness 0.002) | Bridges code communities to doc/research clusters — touched by anything that reads SCRIPT.md. |
| `open()` | (high betweenness 0.004) | File-IO bridge; not interesting on its own but appears as the connector in cross-community paths. |

## Real code communities

Cohesion ≥ 0.05 and substantive node lists. Worktree twin in parens.

### Discovery / keyword pipeline
- **#17, #20** (twins) — `KeywordDB`/keyword discovery surface; tools/discovery/database.py + intent_classifier.py
- **#22** — Discovery pipeline orchestrator (autocomplete + competitor-gap + trends → ranked candidates → `DISCOVERY-FEED.md`)
- **#23** — Channel extraction / outlier hooks backfill
- **#24** (cohesion 0.05) — `IntentClassifier` (Phase H5 refactor of database.py)
- **#48** (cohesion 0.08) — `KeywordStore` (Phase H4 refactor, single-responsibility store)
- **#50** — `PerformanceTracker` (Phase H4 refactor — stores POST-PUBLISH-ANALYSIS feedback)
- **#67** — Keyword classification / trends populator (`classify_keyword`, `populate_keyword_intents`)
- **#68** — Algorithm snapshots + competitor video registry

### Analytics / publishing
- **#49** (cohesion 0.07) — `AnalyticsStore` / database connection layer (the ADR-0004 refactor work)
- **#58, #33** (twins) — `PostPublishReport` + pattern aggregation (`aggregate_by_pattern/thumbnail/title_structure/topic`)
- **#25** — Video assessment + retitle swap-candidate generation
- **#29** (cohesion 0.06) — Folder ↔ YouTube video matcher (`MatchCandidate`, reconcile pipeline)
- **#62, #63** (twins, cohesion 0.08) — Schema migrations + technique DB (script_choices logging, v29)
- **#69** (cohesion 0.09 — highest) — Content classification: `_classify_hook_type`, `_classify_specificity`, `_classify_duration_bucket`
- **#64** — Hook/close analysis (`classify_hook`, `count_documents_mentioned`, `count_source_citations`)
- **#59** — Title classification + schema (`classify_title`, `ensure_schema`)

### Script & quality
- **#18** — `EditGuideGenerator` + `Section`/`Entity` parsing
- **#19** — Retention scorer tests (voice patterns, modern-relevance gap, evidence markers)
- **#21, #42** (twins) — Description/metadata generator + citation extraction (CLICKBAIT consolidation, `_extract_citations`)
- **#54, #55** (twins) — `PacingChecker` tests (sentence variance, entity density, fleshiness)
- **#57** — AI-slop detector (`_check_ai_slop`, `_check_em_dashes`, `_check_metadiscourse`, `_check_qualifiers`, `_check_rhythm_flatlines`, `_check_axiom_anchors`)
- **#65** — Material builder / versus-signal detection (`_build_material`, `_count_conflict_hits`, `detect_versus_signal`)
- **#1** — Title generator tests + contradiction extraction
- **#70** — `benchmark_store` tests (niche-score VPS conversion)
- **#74, #87** (twins) — `hook_scorer` Phase 69 upgrade tests (Document Reveal framework)

### Specialized
- **#35** — Pétain annotated draft PDF builder (`AnnotatedDraftPDF` — Untranslated Evidence series)
- **#53** — Translation pipeline (`CrossChecker`, clause-by-clause via Claude)

### Source/publisher registry
- **#0** — `canonical_map` cluster: 267 publisher/scholar nodes (ACLS-Humanities, Cambridge UP, Adonis & Abbey, AnnaArchive, etc.) — drives source-library rename + author normalization
- **#28** — `slug_renames` table for the same registry

## Per-video research clusters (doc content as bag-of-headings)

Each video's research markdown got bag-extracted into a community. Useful as a content-presence index, NOT as a knowledge graph — no edges to scholars, claims, or cross-cutting concepts (because semantic step never ran).

| Twin pair | Topic / Video |
|---|---|
| #73, #86 | Guatemala–Belize ICJ case (#48 series) |
| #75, #88 | Viking sagas / Grágás (blood feud / compensation) |
| #76, #89 | Christmas date origins (De Pascha Computus, Early Christian imagery) |
| #77, #90 | 5-act structure dump (likely Christmas or Vikings script) |
| #78, #91 | Flat earth / medieval cosmology (Bede, Sacrobosco, conflict thesis) |
| #79, #92 | Flat-earth bibliography (Bede, Sacrobosco, Isidore, Aquinas, Irving, Draper, White, Cormack) |
| #80, #93 | Manifest Destiny / Vance Ole Miss / Mirari Vos / Dum Diversas / Florida 2023 curriculum |
| #81, #94 | Autonomous research final report — high-demand underserved ideas |
| #82, #95 | British mandate promises (Hussein-McMahon, Sykes-Picot, Balfour, San Remo) |
| #83 | PDF source library (filenames + dedup actions) |
| #71, #84 | Phase milestones / roadmap (Phase 10-25+) |
| #72, #85 | Architecture code examples — `PATTERN_SCORES`, `title_ctr_store`, `score_title` |
| #96 | Article-Writer v5.5 anti-patterns + first-person integration |

## Noise communities (ignore)

Whole-cluster duplicates from registry data:
- **#2–#15** (14 copies) — `automatic_captions` × ISO 639 language codes (`aa, ab, af, ak, am, ar, as`...). YouTube channel-data caption availability. Skip.
- **#26, #27, #30–32, #34, #36–41, #44–47** — yt-dlp video-info field schemas (`acodec, age_limit, aspect_ratio, asr, audio_channels, audio_ext, availability...`). Skip.
- **#43** — `subtitles` × language codes. Skip.
- **#51, #56, #61** — YouTube video ID strings (`2RQWu-cyO90, 499YLd1BHZ4...`). Skip.
- **#52, #60** — numeric string tokens (`"1", "10", "11"...`). Skip.

These all have cohesion 0.03 and identical node-list prefixes — easy to spot.

## How to query

- **"Where is X defined?"** — find X in god nodes / communities table above; if not there, grep directly (faster than loading graph).
- **"What depends on KeywordDB?"** — caution: 220 of its 302 edges are AST signature noise (INFERRED). Use the explicit caller list in tools/discovery/database.py imports, not the graph.
- **"What's in Community N?"** — `sed -n '/^### Community N - /,/^### Community/p' graphify-out/GRAPH_REPORT.md` (PowerShell equivalent via Bash tool).
- **Deep traversal** — `/graphify query "<question>"` runs BFS against `graph.json` externally; no Claude tokens. Use for cross-cutting questions only — for "where does X live" this file is faster.

## What's missing (semantic gap)

The 22.5M words of doc/research content were detected but never LLM-extracted. So the graph cannot answer:
- "Which scholars do I cite most?"
- "Which arguments appear in multiple videos?"
- "What's the relationship between Pope Nicholas V and the Atlantic Slave Trade across my research files?"

For that, dispatch `/gemini ingest` against `video-projects/_ARCHIVED/published/*/01-VERIFIED-RESEARCH.md` (cheap, Flash, single bulk call), or accept the cost of re-running graphify with the semantic step enabled.

## Refresh

- Graph commit: `562996b1` — run `git rev-parse HEAD` and compare.
- After code refactors: `graphify --update .` (AST re-extracts changed files, no LLM cost).
- After deleting the worktree: re-run from scratch to lose the duplicates.
