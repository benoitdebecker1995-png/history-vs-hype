# AnalysisSource: a test seam for run_analysis

**Date:** 2026-06-25
**Status:** accepted

Peer to ADR-0008/0009/0010. This ADR exists because `analyze.run_analysis` — the engine behind `/analyze`, which writes every video's post-publish report — had **zero tests**. It fetched live YouTube-API and database data directly, so there was no way to feed it known input and check the report it produced. A silently wrong number or a dropped data source had no safety net. A `/improve-codebase-architecture` pass (2026-06-25) surfaced it.

## What the seam is

`tools/youtube_analytics/analysis_source.py` — one interface over the six external fetches `run_analysis` depends on, with two implementations:

- **`AnalysisSource`** (Protocol): `video_report`, `comments`, `channel_averages`, `video_metrics` (YouTube API) + `variant_data`, `ctr_analysis` (keywords.db). The four API methods may raise; `run_analysis` owns the try/except and error collection. The two DB methods return `None` when their optional subsystem is unavailable or has no data.
- **`LiveAnalysisSource`** — production default; calls the real functions with lazy imports, so the optional subsystems degrade to `None` exactly as the old `_AVAILABLE` import-gating did.
- **`InMemoryAnalysisSource`** — fed canned results (or a `raises={'comments': RuntimeError(...)}` map) so tests drive `run_analysis` and every partial-failure branch with no network.

`run_analysis(video_id_or_url, manual_ctr=None, source=None)` — `source` defaults to `LiveAnalysisSource`, so the one real caller (the CLI `main`) is unchanged.

## Decision — net first, no rearranging (per the user)

The user (non-engineer) asked for two things explicitly: **cover all the data sources** (so every part of the report is checked, not just the headline numbers), and **add the safety net without rearranging the existing code** (since there was no test net, restructuring first is how you silently break things).

Both honored:

- **All six external fetches** go behind the port — including the two optional DB-backed ones — so every fetch and its failure branch is reachable from a fake. (`diagnose_discovery` and `generate_lessons` are pure synthesis on already-fetched data, not data sources; they stay as direct calls and were already testable.)
- **Only the fetch calls moved.** The assembly, the manual-CTR override, the comparison fallback, and all the `errors.append(...)` partial-failure handling stay exactly where and how they were. No `synthesize()` was extracted — that deeper split is deferred until the test net has proven itself.

## What was deliberately left alone

- `analyze.py` still carries its module-level optional imports (`VARIANTS_AVAILABLE`, `BENCHMARKS_AVAILABLE`, `compare_variants_for_video`, `get_benchmarks_report`). Three are now unused by `run_analysis` (their logic moved into `LiveAnalysisSource`), but other functions in the file still use the variant ones, and removing the benchmarks imports is exactly the kind of rearranging the user asked to defer. Tidy in a later pass.
- `find_project_folder` (analyze.py) globs the lifecycle folders by hand — a future candidate for `VideoProjectRepo` (ADR-0008), not touched here.

## Considered alternatives

- **Core 4 fetches only** (leave variants/benchmarks inline). Rejected — "cover all the data sources" means the optional branches must be testable too.
- **Also split fetch / synthesize** in this pass. Rejected — restructuring 1200 lines of untested orchestration before any net exists is the risk the user named. Inject-source first; split later if wanted.

## Consequences

- **Test surface.** `tests/test_analyze.py` (13 tests) — the first tests of `run_analysis`: happy-path assembly, manual-CTR override, video-report error propagation, and each partial-failure branch (comments, channel-averages, variant fetch raising, ctr-analysis raising, and the no-variants short-circuit), all offline.
- **No behavior change.** `LiveAnalysisSource` reproduces the old inline calls (including connection cleanup, now in a `finally`). The CLI path is unchanged. Module imports verified.
- **Re-litigation guard.** Future runs surfacing "run_analysis is untestable / a god-function" should be answered with this ADR. The next step (extracting a pure `synthesize`) is recorded as deferred, not missed — supersede rather than re-derive.
