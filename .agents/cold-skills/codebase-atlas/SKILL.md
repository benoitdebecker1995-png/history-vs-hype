---
name: codebase-atlas
description: 'Map of the Python code surface in G:\History vs Hype — package map of tools/, runnable entry points with exact commands, the ADR seam catalog (which file owns what, where to route a change), and navigation recipes (graphify-code MCP vs CODE-MAP.md vs grep). Use when: asking "where does X live", "what depends on Y", "which file implements Z", "how do I run tool X", when adding or modifying anything under tools/, or when deciding which seam a change routes through. Does NOT cover DB schemas or query recipes (→ data-stores skill) or how to run tests (→ validation-standards skill).'
---

# Codebase Atlas

Everything below was live-verified 2026-07-01 (commands actually run, files read). Repo root: `G:\History vs Hype`. Python 3.12.2, invoked as `python` (system install, no venv in use).

## Rule zero — how to run anything

**Always `python -m tools.<pkg>.<module>` from repo root.** (The repo path contains a SPACE — `G:\History vs Hype` — quote it in every shell command that uses an absolute path.) Direct-script invocation fails for most modules: `python tools/title_scorer.py --help` dies with `ModuleNotFoundError: No module named 'tools'` (no sys.path bootstrap in the file), while `python -m tools.title_scorer --help` works. A few entry modules (reconcile, session_context, news_scanner) carry a bootstrap and survive direct invocation — don't rely on it; `-m` is the universal convention.

One exception that CANNOT use `-m`: `tools/refresh-research-graph.py` (hyphen in filename). Run it as `python tools/refresh-research-graph.py --skip-gemini` (omitting `--skip-gemini` makes a live Gemini call).

## Package map (`tools/`)

241 Python files under `tools/`. Purposes below from live docstring extraction.

| Package / module | What it is |
|---|---|
| `tools/title_scorer.py` | Title Scorer v5 — the packaging workhorse (~47KB). Clickbait brand gate + search-anchor recognizer live here (ADR-0012; the recognizer accepts a curated term OR a verified ≥1,000/mo search volume from keywords.db — ADR-0023). `--strict` restores old hard-rejects; default is graded penalties. |
| `tools/title_features.py` | ADR-0009 seam: pure `str → features`, 6-class `pattern()` taxonomy + predicates. No DB, no I/O. Topic classification deliberately excluded. |
| `tools/subtitles.py` | ADR-0010 seam: THE one SRT parser (`parse()`, typed `Cue`/`SubtitleTrack`, encoding ladder, opt-in `fix_hour_offset`). |
| `tools/benchmark_store.py` | Reader for `channel-data/niche_benchmark.json` (niche scores, topic thresholds). Never raises. Its docstring falsely says colon is a hard reject — behavior is right, comment lies. |
| `tools/title_ctr_store.py` | DB-backed pattern-CTR lookup for the scorer (reads keywords.db). Never raises. |
| `tools/topic_pipeline.py` | Ranks future topics (volume × fit × gap); writes `channel-data/TOPIC-PIPELINE.md` with `--save`. |
| `tools/swap_ledger.py` | Single-variable packaging-swap ledger: DB row is truth, regenerates `channel-data/SWAP-LEDGER.md`. |
| `tools/voice_lint.py` | v18 deterministic voice scanner; rules derived FROM `.claude/REFERENCE/VOICE-PROFILE.md` (ADR-0006: never edit lint first). Zero automated tests — top coverage gap. |
| `tools/retitle_audit.py` / `retitle_gen.py` | Find underperforming titles / generate retitle candidates. `retitle_gen` has no argparse (manual `--script-only` check). |
| `tools/packaging_intel.py`, `packaging_autopilot.py`, `ctr_ingest.py`, `ctr_quick_add.py` | Packaging feedback loop: competitor/demand signals → scoring; CTR ingestion into keywords.db. |
| `tools/logging_config.py` | Shared logging (`setup_logging` once in main, `get_logger(__name__)` per module) + `check_db_freshness()`. |
| `tools/discovery/` | Keyword/topic discovery; owns `keywords.db`. NOTE: `database.py` is a shim — real `KeywordDB` code is in `schema_manager.py`; domain store is `keyword_store.py`. Also: news_scanner, recommender, autocomplete, trends, intent classifiers. |
| `tools/youtube_analytics/` | Largest package (~60 modules); owns `analytics.db`. Foundation: `auth.py` (OAuth), `store.py` (`AnalyticsStore` — ADR-0004 seam), `growth_data.py` (API→DB refresh writer), `backfill.py`. Analysis: `analyze.py` (/analyze orchestrator), `analysis_source.py` (ADR-0011 test seam), retention_* modules, `patterns.py`, traffic/CTR modules. |
| `tools/intel/` | Competitor/algorithm KB; owns `intel.db` via `kb_store.py` (`KBStore` — per-call connections). `topic_vocabulary.py` = single source of truth for topic classification. `refresh.py` is a library, NO main guard. `vidiq_competitor_sync.py` (ADR-0013). |
| `tools/preflight/` | Pre-publish gates (ADR-0007/0012: filters, not predictors). `packaging_lock.py` = the code-enforced packaging gate; `thumbnail_checker.py`, `thumbnail_image_audit.py`, `demand_checker.py`, `audio_loudness.py` (needs ffmpeg via winget), `scorer.py` (composite scorecard, no argparse). |
| `tools/production/` | Script-side artifact generation: `parser.py` (`ScriptParser` — the SCRIPT.md parser everything composes), entities, metadata, title_generator, editguide, broll. |
| `tools/reconcile/` | THE dangerous writer: `reconcile.py` owns lifecycle folder moves, AUTO:reconcile zones, derived root docs, reversible diffs + `--undo`. `match.py` = folder↔video matcher. Truth: filesystem + analytics.db (never calls YouTube API itself). |
| `tools/video_projects/` | ADR-0008/0014 seams: `repo.py` (`VideoProjectRepo` — read-only project/lifecycle resolver) + `status_doc.py` (`StatusDoc`/`AutoZone` — the one AUTO-fence implementation). |
| `tools/post_publish/` | ADR-0005 seam: `PostPublishStore`/`PostPublishReport` over POST-PUBLISH-ANALYSIS.md files (retention stored as PERCENT). |
| `tools/script_checkers/` | Script QA: `cli.py`, `registry.py`, `checkers/` (flow, repetition, stumble, scaffolding, pacing), `voice/` (corpus_builder etc.). |
| `tools/research/` | competitor_gap, hook_scorer, nlm_ingest, opener_diagnostic (+ its in-package tests, which DO collect). |
| `tools/routines/` | Scheduled-task workloads: competitor_drop_scan, keyword_trends_daily, modern_relevance_scan, retention_audit_weekly. Scheduling itself → automation-ops skill. |
| `tools/hooks/` | Claude Code harness hooks: `session_context.py` (SessionStart), `locked_asset_guard.py` (PreToolUse). |
| `tools/dashboard/project_scanner.py` | The ONE home of `detect_phase` + `extract_topic_slug`; VideoProjectRepo and reconcile import from it. Reuse, don't relocate. |
| `tools/benchmark/` | One-shot competitor-corpus builders (n=85 corpus). Many hit the network (yt-dlp/YouTube) — do not run casually. |
| `tools/newsletter/` | article_scorer, subject_line_scorer. |
| `tools/translation/`, `tools/document_discovery/`, `tools/thumbnail/` | Untranslated Evidence pipeline; translation-gap checkers; thumbnail render templates. |
| `tools/tests/` | Repo-side regression pins (scorer, swap ledger, thumbnail filters, preflight fallback). NOT collected by default pytest — see validation-standards skill. |
| `tools/history-clip-tool/` | Self-contained FastAPI clipping app (own requirements.txt, own src tree, `run.py` → uvicorn on 127.0.0.1:8000). NOT in the `tools.*` namespace — treat as an embedded standalone app. [UNVERIFIED: never launched.] |

## Entry points — exact commands

All from repo root. Every command below exited 0 printing real argparse help on 2026-07-01.

| Command | Key args / output |
|---|---|
| `python -m tools.reconcile.reconcile --help` | `[project] --dry-run --migrate --auto-publish-only --undo --apply` |
| `python -m tools.youtube_analytics.growth_data --help` | `--refresh --video ID` → writes analytics.db (Routine 7's tool) |
| `python -m tools.youtube_analytics.backfill --help` | `--force --insights-only --json-only` |
| `python -m tools.youtube_analytics.analyze --help` | `VIDEO_ID_OR_URL --markdown --ctr V --save --output PATH --script PATH` |
| `python -m tools.title_scorer --help` | `titles... --file --db --topic --ingest --experimental --strict` |
| `python -m tools.preflight.packaging_lock --help` | `--project P [enrichment flags] --write --validate` |
| `python -m tools.preflight.thumbnail_checker --help` | `[project] --text --title --person-focused --territorial` |
| `python -m tools.preflight.demand_checker --help` | positional `topic`; emits a harmless runpy RuntimeWarning — ignore it |
| `python -m tools.script_checkers.cli --help` | `script_path --flow/--repetition/--stumble/--scaffolding/--pacing/--all --json` |
| `python -m tools.voice_lint --help` | `paths... --no-transitions --quiet` |
| `python -m tools.topic_pipeline --help` | `--top N --save --type T` |
| `python -m tools.newsletter.article_scorer --help` | `[file] --all --json` |
| `python -m tools.swap_ledger --help` | subcommands `open` / `read` / `list` |
| `python -m tools.routines.competitor_drop_scan --help` | `--lookback-hours N` |
| `python -m tools.retitle_audit --help` | `--top --min-impressions --save` |

Documented-but-not-executed (invocation read from `__main__` blocks): `python -m tools.preflight.scorer <project_path>` (no argparse, prints usage without arg); `python -m tools.intel.query` (read-only staleness print); `python -m tools.retitle_gen [--script-only]`; `python tools/refresh-research-graph.py [--skip-gemini]`.

**Do-not-run-casually** (network, API writes, or money): anything in `tools/benchmark/` (scrapes), `growth_data`/`backfill` without `--help` (writes analytics.db), `tools/notebooklm_bridge.py` (Anthropic API), `refresh-research-graph.py` without `--skip-gemini` (Gemini), `tools/intel/refresh` (bulk fetch), `tools/preflight/serp_thumb_study.py` / `serp_title_study.py` (live SERP). Also: the three live SQLite DBs are committed in the working tree — any run that writes them dirties git status.

## Seam catalog (ADR → files → when to route through it)

Full ADRs in `docs/adr/` (0001–0003 and 0006 are content-side decisions, not code seams). The table below covers the seam ADRs; it is **not** an index of every ADR — `ls docs/adr/` is. One-line takeaways only — read the ADR before arguing with it. Every code ADR is a re-litigation guard: **supersede with a new ADR rather than silently restructure.**

| ADR | Seam | Files | Route your change through this when… |
|---|---|---|---|
| 0004 | Two-store split: analytics.db vs keywords.db — never consolidate | `tools/youtube_analytics/store.py` (`AnalyticsStore`), `tools/discovery/{schema_manager,keyword_store}.py`, `tools/youtube_analytics/views.py` (cross-store joins) | Any read/write of analytics.db → `AnalyticsStore.open()`. Cross-store join → `views.py`. Proposing a merge = answered by the ADR: no. |
| 0005 | Post-publish markdown gets one typed seam | `tools/post_publish/` (`from tools.post_publish import PostPublishStore`) | Reading/writing POST-PUBLISH-ANALYSIS.md data. New fields go in `PostPublishReport` only when a second consumer needs them. |
| 0007 | Thumbnail tools are FILTERS, never clickability predictors | `tools/preflight/thumbnail_checker.py`, `thumbnail_image_audit.py`; pinned by `tools/tests/test_thumbnail_filters.py` | Adding any thumbnail check: must be pass/fail necessary-condition. A predictive pre-publish score is the forbidden failure mode. |
| 0008 | `VideoProjectRepo` = read-only resolver over the 3 lifecycle folders | `tools/video_projects/repo.py` | Any "find project folders / resolve slug / what phase" logic. NEVER add a mutation — folder moves stay in `tools/reconcile/`. `_BACKLOG` stays invisible. |
| 0009 | `title_features` = the one title-structure home | `tools/title_features.py` | Any title-structure question → import it. Broaden by enriching `pattern()` + re-baselining tests, never fork. Topic rules do NOT go here (they live in intent_mapper / topic_vocabulary / growth_data). |
| 0010 | `subtitles` = the one SRT parser (the `srt` pip lib was rejected) | `tools/subtitles.py` | Any SRT read → `tools.subtitles.parse()`. The SRT WRITER (`auto_srt_fixer`) is deliberately still outside the seam. |
| 0011 | `/analyze` data fetches behind `AnalysisSource` Protocol | `tools/youtube_analytics/analysis_source.py`, `analyze.py` | Adding/changing any external fetch in the analyze path → extend the Protocol + BOTH impls (Live + InMemory). |
| 0012 | Packaging advancement is CODE-gated (4 filters; enrichment never upgrades a FAIL) | `tools/preflight/packaging_lock.py`; root-cause fixes in `title_scorer.py` (packaging_lock IMPORTS `score_title`/`has_search_anchor` from it) | Any packaging rule that must BIND → add as a filter in packaging_lock (code), never prose in a command file. Scores stay non-binding nudges. The search-anchor recognizer itself is governed by ADR-0023. A title_scorer semantic change → re-run `tests/test_packaging_lock.py` + `tools/tests/test_scorer_regression.py` (explicit path). |
| 0013 | VidIQ MCP = enrichment-only; repo JSON is the canonical competitor set | `tools/intel/vidiq_competitor_sync.py`, `tools/intel/competitor_channels.json` | Changing competitors → edit the repo JSON, then run the sync. VidIQ generation tools on-channel require a new ADR. |
| 0023 | Search-anchor fame is MEASURED, not listed (curated set is a fast path only) | `tools/title_scorer.py` (`find_search_anchor`, `ANCHOR_VOLUME_FLOOR`, `record_anchor_volume`); pinned by `tests/unit/test_search_anchor.py` | A title fails the anchor filter on a term you believe is famous → do NOT add it to `HEAD_TERMS`. Record its verified volume: `python -m tools.title_scorer --record-anchor "<term>" --volume <n> --anchor-source vidiq-YYYY-MM-DD`. Three symptomatic list patches in eight weeks is what this ADR ended. |
| 0014 | `status_doc` owns AUTO-zone fence grammar (3 registered zones) | `tools/video_projects/status_doc.py` (`AutoZone`, `StatusDoc`) | Any new managed block in PROJECT-STATUS.md → register a new `AutoZone`; never hand-roll `<!-- AUTO:* -->` markers or edit inside a zone. |

Two seams deliberately NOT extracted yet ("defer the dangerous writer" house pattern): the folder mover (`tools/reconcile/reconcile.py`) and the SRT rewriter (`tools/youtube_analytics/auto_srt_fixer.py`). Do not "helpfully" wrap them. Full extend-vs-add judgment → extending-safely skill.

## Navigation recipes — which tool wins when

| Question | Use | Why |
|---|---|---|
| "Where is class/function X defined?" | Grep for `def X\|class X` (or `.claude/REFERENCE/CODE-MAP.md` god-node/community tables first) | Fastest; graph adds nothing for point lookups. |
| "Where does capability X live / which package?" | The package map above, then `.claude/REFERENCE/CODE-MAP.md` | CODE-MAP is the human-labeled community index. |
| "What depends on Y / blast radius of changing Y?" | `mcp__graphify-code__get_neighbors` / `query_graph`; cross-check with Grep for real import sites | Graph is dense and reliable for structure — but see the noise caveats below. |
| "How does A connect to B across packages?" | `mcp__graphify-code__shortest_path` | The one thing grep can't do. |
| "Most-connected hubs?" | `mcp__graphify-code__god_nodes` — or just read the de-noised list below | Report list is pre-cleaned. |
| "Have we covered scholar/treaty/topic Z across videos?" | NotebookLM notebook `HvH-coverage-corpus` (id → automation-ops § MCP servers) via `notebook_query` — NOT the research graph | Head-to-head test 2026-06-12: notebook 10/10, graph 0/10. `mcp__graphify-research__*` is sparse; fine for a quick entity ping, fall back on <3 hits. |
| Graph feels broken / needs rebuild | `.claude/REFERENCE/GRAPHIFY-OPS.md` | Health checks, refresh, and rollback commands live there. |

**God nodes (de-noised, from `.claude/REFERENCE/CODE-MAP.md`):**
- `KeywordDB` (302 edges) — resolves to `tools/discovery/database.py`, which is a shim; real code is `schema_manager.py`. **220 of those edges are AST signature noise** (`Path`/`bool`/`Any`), not coupling — for real dependents, grep import sites instead.
- `canonical_map` (267 edges) — publisher/scholar canonicalization registry driving the source-library renamer.
- `ScriptParser` (`tools/production/parser.py`) — highest betweenness; touched by anything that reads SCRIPT.md.
- 65% of graph nodes are isolated singletons (language codes, type stubs) — ignore.

**Graph staleness caveat:** the code graph was built at commit `562996b1` (2026-05-25), AST-only. The ADR-0012/0013/0014 seams post-date it — treat graph/CODE-MAP community labels as a label set, not ground truth for HEAD. A post-commit git hook rebuilds the AST graph in the background (log: `~/.cache/graphify-rebuild.log`), but CODE-MAP.md itself is a frozen distillation. When graph and current code disagree, current code wins; verify with Grep before asserting.

## Gotchas (atlas scope)

| Symptom | Cause → fix |
|---|---|
| `ModuleNotFoundError: No module named 'tools'` | Direct-script invocation → run `python -m tools....` from `G:\History vs Hype`. |
| Grep finds `KeywordDB` in `tools/discovery/database.py` but the code looks empty | It's the backward-compat shim → real implementation in `tools/discovery/schema_manager.py`. |
| `python -m tools.refresh-research-graph` fails | Hyphenated filename can't be a module → `python tools/refresh-research-graph.py --skip-gemini`. |
| Filesystem walk / `find` dies with Permission denied | `tools/youtube_analytics/.pytest_cache` is unwritable (WinError 5) → exclude that dir from walks. |
| `tools/youtube_analytics/test_*.py` files look like the tests for a module | 6 of them use broken bare imports; the WORKING twins live in `tests/unit/`. Also `tests/unit/test_retention_scorer.py` targets `retention_scorer.py`, which does not exist (TDD leftover, permanently skipped) — don't "fix" the import. Test procedure → validation-standards skill. |
| git status shows the `.db` files modified after a tool run | The live SQLite DBs are committed in-tree; tool runs dirty them. Expected — schemas and handling → data-stores skill. |
| A docstring contradicts observed behavior (e.g. `benchmark_store.py` "colon is a HARD REJECT") | Stale comment; behavior follows the v5 re-tier (graded penalty, hard-reject only under `--strict`). Trust tests + ADRs over docstrings. |

## Related skills

- **data-stores** — the moment your question is about what's IN analytics.db / keywords.db / intel.db (schemas, refresh chains, staleness, safe queries) rather than which module owns them.
- **extending-safely** — before writing NEW code: extend-don't-add test, conventions (logging, imports, error contracts), where new modules go.
- **validation-standards** — to run tests or decide whether a change is actually done (exact pytest commands, real-data verification rule).
- **debugging-playbook** — when a tool from this map fails at runtime and you need the evidence-first diagnostic path (which log/lock/timestamp to check).
