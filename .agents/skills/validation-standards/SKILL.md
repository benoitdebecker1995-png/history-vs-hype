---
name: validation-standards
description: How work gets VALIDATED in D:\History vs Hype — exact pytest commands and the collection traps, the test-suite map (module → test file, what has zero coverage), conftest fixture + DB-pin patterns, the real-data verification rule (synthetic fixtures alone are never "verified"), the filters-not-predictors gate philosophy, and per-artifact definition of done. Use when: running tests or interpreting test results; deciding whether a change is "done" or "verified"; writing or modifying a checker, gate, or score; claiming a result from data (views, CTR, retention, traffic); adding tests for new code. NOT for locating code or seams (→ codebase-atlas), how to route a change (→ extending-safely), or DB schemas/query recipes (→ data-stores).
---

# Validation Standards

Repo root: `D:\History vs Hype`. Run everything from there; Python 3.12.2 as `python`.
Provenance: file-level facts (pytest config, conftest, every test file's existence, phantom module) verified by direct read 2026-07-02. Collection counts and command runs were live-verified 2026-07-01 (Wave-1 code inventory); anything not re-run since is dated or marked [UNVERIFIED].

## Running tests

Two non-negotiable mechanics, then the commands:

1. **Always run from repo root with `python -m pytest`** — tests use absolute `tools.` imports.
2. **Always pass `-p no:cacheprovider`** — `.pytest_cache/` is not writable on this machine (WinError 5); without the flag every run warns and `tools/youtube_analytics/.pytest_cache` breaks filesystem walks.

| What | Command |
|---|---|
| Default suite (`tests/` only — 649 tests, 0 collection errors as of 2026-07-01) | `python -m pytest -p no:cacheprovider -q` |
| Full suite (adds the repo-side pin files pytest skips by default) | `python -m pytest tests/ tools/tests/ tools/script_checkers/tests/ -p no:cacheprovider -q` |
| One file | `python -m pytest tests/test_status_doc.py -p no:cacheprovider -q` |
| One test | `python -m pytest tests/unit/test_pacing.py -k <name> -p no:cacheprovider -q` (collect-verified 2026-07-03) |
| Collect-only sanity check (fast, safe, no test executes) | `python -m pytest --collect-only -q -p no:cacheprovider` |
| Repo-side pins only | `python -m pytest tools/tests/ -p no:cacheprovider -q` |

The full run is SLOW (8m29s on 2026-06-12) — don't run it casually; scope to the files covering your change, then full-suite before declaring done.

### Collection traps (each one has bitten a session)

| Trap | Fact | Consequence if ignored |
|---|---|---|
| Default collects ONLY `tests/` | `pyproject.toml` `[tool.pytest.ini_options] testpaths = ["tests"]` | "All tests pass" while `tools/tests/` (scorer regression, swap ledger, thumbnail-filter pins, title-fallback parity) and `tools/research/test_opener_diagnostic.py` never executed. Pass their paths explicitly. |
| `tools/youtube_analytics/` is pytest-poison | 6 in-package `test_*.py` files use bare imports (`from transcript_analyzer import …`) → 3 error at collection; run from inside the dir, module-level `except ImportError: sys.exit(1)` guards can kill the collector with INTERNALERROR | **Never include `tools/youtube_analytics/` in a pytest path.** Working twins of those tests live in `tests/unit/` (test_pattern_synthesizer_v2, test_transcript_analyzer, test_retention_mapper, test_section_diagnostics). |
| Phantom module `retention_scorer` | `tests/unit/test_retention_scorer.py` imports `tools.youtube_analytics.retention_scorer`, which **does not exist** (confirmed 2026-07-02) — a TDD leftover; its tests `skipUnless`-skip forever (part of the recorded 13 skips) | "Fixing" the import un-skips tests for unimplemented behavior. Leave it, or implement the module first. |
| `tools/script_checkers/tests/` is now empty | Contains only `__init__.py` (2026-07-02); its `test_pacing.py` was deleted — live pacing tests are `tests/unit/test_pacing.py` | Keeping the path in the full-suite command is harmless; expecting tests there is stale. |
| Explicit-path collection errors are EXPECTED for one dir only | 2026-07-01: `tools/tests tools/script_checkers/tests tools/youtube_analytics` → 78 collected + 3 errors, all three from `tools/youtube_analytics/test_*.py` | Any collection error OUTSIDE that dir is a real regression you introduced. |

### Interpreting results — and the standing doc

`docs/TEST-STATUS-2026-06.md` is the standing status doc (2026-06-12 full run: 18 failed / 539 passed / 13 skipped). Read it before triaging reds, but know its staleness: **§A (8 title_scorer failures) was fixed 2026-06-25** (ADR-0009 re-baseline, "131 passed"); **§B (9 pacing failures) is historical** — the pacing checker was reworked (contract is now "one `all_sections` entry per parsed section — always", unstructured input returns a SKIPPED verdict; confirmed by reading `tools/script_checkers/checkers/pacing.py` 2026-07-02) and its tests relocated to `tests/unit/test_pacing.py`; **§C (youtube_analytics conftest fix) and §D (coverage gaps) remain live and unapplied.** Current full-run pass/fail state [UNVERIFIED — collection-only checked since].

**When tests fail:** fix ALL failures, not just the ones your change caused — "pre-existing" is never a reason to ship red (hard rule; the user once had to manually order the fix of 6 failures dismissed that way). Missing dependency = `pip install`, never a mock, skip decorator, or sys.modules injection. Escalate to the user only when the fix would be destructive or is a calibration decision (e.g. "what SHOULD a year-title grade now?" — the §A fix waited on the calibration owner, and that scoping was explicit, not assumed).

## Test-suite map (module → test file)

All mappings import-verified. Files under `tools/tests/` need an explicit path (trap above).

| Covered code | Test file(s) |
|---|---|
| `AnalyticsStore` (analytics.db seam, ADR-0004) | `tests/test_analytics_store.py` |
| `PostPublishStore` (ADR-0005) | `tests/test_post_publish_store.py` |
| `VideoProjectRepo` (ADR-0008) | `tests/test_video_projects.py` |
| `title_features` (ADR-0009) | `tests/test_title_features.py` + `tools/tests/test_preflight_title_fallback.py` (parity pin) |
| `subtitles` SRT parser (ADR-0010) | `tests/test_subtitles.py` |
| `analyze.run_analysis` + `AnalysisSource` (ADR-0011) | `tests/test_analyze.py` — 13 tests, ALL offline via `InMemoryAnalysisSource` |
| `packaging_lock` gate (ADR-0012) | `tests/test_packaging_lock.py` |
| `StatusDoc`/`AutoZone` (ADR-0014) | `tests/test_status_doc.py` |
| reconcile folder moves | `tests/test_reconcile_mover.py` |
| discovery `KeywordDB`/`KeywordStore` | `tests/test_database_pin.py` (THE DB-pin suite), `tests/test_keywords_migration.py`, `tests/test_discovery.py`, `tests/test_discovery_scanner.py` |
| intel `KBStore` | `tests/test_intel.py`, `tests/test_intel_migration.py` |
| `title_scorer` v5 | `tests/unit/test_title_scorer_db.py`, `tests/unit/test_title_scorer_niche.py` (re-baselined 2026-06-25), `tools/tests/test_scorer_regression.py` |
| `benchmark_store` / `title_ctr_store` | `tests/unit/test_benchmark_store.py` / `tests/unit/test_title_ctr_store.py` |
| `swap_ledger` + `packaging_intel` | `tools/tests/test_swap_ledger.py` |
| preflight thumbnail filters (ADR-0007) | `tools/tests/test_thumbnail_filters.py` (calibration pins) |
| script_checkers CLI + registry | `tests/test_script_checkers.py` (subprocess pins), `tests/test_checker_registry.py` |
| pacing checker | `tests/unit/test_pacing.py` |
| youtube_analytics backfill / retention / ctr_tracker | `tests/test_analytics.py` / `tests/test_retention_pipeline.py` + `tests/unit/test_retention_mapper.py` / `tests/youtube_analytics/test_ctr_tracker.py` |
| pattern_synthesizer_v2, transcript_analyzer, section_diagnostics | `tests/unit/` twins (same names) |
| production parser/entities/metadata/title_generator | `tests/test_production.py`, `tests/unit/test_metadata_bundle.py`, `tests/unit/test_title_generator.py` |
| translation, hook_scorer, ctr_ingest, logging_config | `tests/test_translation.py`, `tests/unit/test_hook_scorer.py`, `tests/integration/test_ctr_ingest.py`, `tests/test_logging_config.py` |
| opener_diagnostic | `tools/research/test_opener_diagnostic.py` (in-package but proper `tools.` imports — collects fine via explicit path) |

**Known zero-coverage (don't assume a net exists):**
- `tools/voice_lint.py` — **ZERO automated tests** (9 public scanners; the highest-priority gap per TEST-STATUS §D). It also carries the channel's one holdout-surviving HARD gate (`cta-too-early`), so a silent regression here corrupts every script lint.
- 4 of 5 script checkers (`flow`, `repetition`, `scaffolding`, `stumble`) — only subprocess smoke-pins (exit code + non-empty output), no behavior tests.
- Most of `tools/youtube_analytics/`'s 60 modules (e.g. `patterns.py`, 1,955 lines) — untested orchestration. ADR-0011's "net first, no rearranging" stance applies: do not restructure untested code before adding a net.

## Fixtures and the DB-pin pattern

`tests/conftest.py` (the only conftest) provides four fixtures; data lives in `tests/fixtures/`:

- `keyword_db` — in-memory `KeywordDB(db_path=":memory:")`, schema auto-initialized.
- `intel_store` — `KBStore(db_path=tmp_path/"test_intel.db")`. **Deliberately a temp FILE, never `:memory:`**: KBStore opens per-call connections, so an in-memory DB silently vanishes between calls and every read returns empty.
- `tmp_script` / `tmp_post_publish` — copy `tests/fixtures/test_script.md` / build a real-shaped `video-projects/_IN_PRODUCTION/test-video-2026/POST-PUBLISH-ANALYSIS.md` tree under tmp_path.

**What the pattern protects:** the three live SQLite DBs (`tools/youtube_analytics/analytics.db`, `tools/discovery/keywords.db`, `tools/intel/intel.db`) are committed and sit dirty in the working tree — a test that touches them corrupts real channel data and dirties git. Tests route through `:memory:`/tmp_path, no exceptions.

**DB-pin pattern** (`tests/test_database_pin.py`): before refactoring a store, pin every public method's exact return shape — including the `{'error': ...}` dict contracts — with one realistic-args call each (48/48 public methods covered there). The pin suite is written FIRST, so the refactor has a behavior-preservation check instead of hope. Copy this shape when touching any store. Sibling pattern: `tests/test_script_checkers.py` pins CLI behavior via subprocess (sets `PYTHONIOENCODING=utf-8` — required for Unicode checker output captured on Windows).

### Test-writing rules (independent-value + vertical-slice)

Three rules that keep a *green* test meaningful (harvested from the `tdd` skill, adapted):

- **Independent expected values.** The assertion's expected value must come from an *independent* source of truth — a known-good literal, a worked example, the spec — never recomputed the way the code computes it. A test that recomputes is **tautological** (`assert add(a,b) == a+b`): it passes by construction and can never disagree with the code. The DB-pins obey this (each pins a hand-verified return shape, not a re-derived one); hold new tests to the same bar.
- **Test at public seams, not internals.** Verify behaviour through the public interface. A test that mocks internal collaborators, reads private state, or queries the DB behind the interface breaks on refactor while behaviour is unchanged — false red. (The `youtube_analytics` bare-import twins exist because tests reached inside the package.)
- **Vertical slices, not horizontal.** One seam → one test → one minimal implementation → repeat. Writing all tests first pins *imagined* shape, goes insensitive to real behaviour, and commits to structure before the implementation is understood.

## What "verified" means here (the real-data rule)

**Synthetic fixtures prove the code runs. Only real data proves behavior is preserved.** Green tests on fixtures alone do NOT make a change "verified" — this is a recorded owner rule (2026-07-01, while approving architecture work: "remember that you have good csv data and vidiq integration as well"; `memory/feedback-verify-with-real-data.md`).

After migrating or refactoring a tool, run it against the live surfaces and confirm a **known-true fact**:

| Real surface | Path |
|---|---|
| Channel analytics DB | `tools/youtube_analytics/analytics.db` (read via `AnalyticsStore`; `mode=ro` URI for inspection) |
| Discovery/packaging DB | `tools/discovery/keywords.db` |
| Competitor KB | `tools/intel/intel.db` |
| YouTube Studio + VidIQ CSV exports | `channel-data/*.csv`, `channel-data/analytics-exports/*.csv` |
| Post-publish corpus | `POST-PUBLISH-ANALYSIS.md` files via `PostPublishStore` |
| VidIQ MCP (live) | enrichment only, below gates |

Worked example of the standard (2026-07-01): after migrating `find_project_folder`, 6 published video IDs were pulled from `analytics.db` and all 6 confirmed to resolve to `_ARCHIVED/published/` — the old glob found 0; the StatusDoc refactor was byte-parity-checked against the real #62/#58 `PROJECT-STATUS.md` files. That is the bar: a real record, a known answer, an exact match.

Corollary (no fabrication): never claim anything about data or visuals you haven't actually read — performance claims check `analytics.db`/post-publish reports first; image claims require Reading the file. And the local stores outrank dashboards: YT Studio and VidIQ numbers confabulate (a VidIQ "1.4%" was really 13.2%) — cross-check against the owning store (views/retention/traffic → `analytics.db`; CTR → keywords.db `ctr_snapshots`; → data-stores) before citing.

## Gates philosophy: filters, not predictors

Doctrine (ADR-0007, ADR-0012 — read both before touching any checker): **pre-publish tools verify NECESSARY CONDITIONS, pass/fail. Scores are recorded enrichment — never verdicts.** There is no pre-publish clickability oracle; the only clickability verdicts are LIVE (reach-window `ctr_snapshots` CTR trend; native Test & Compare — of which 0 have ever actually run on this channel).

Two incidents define the failure modes:
- **CLIP 100/100 (ADR-0007):** the image audit's "differentiation" score rated two visibly-weak Kurdistan thumbnail drafts 100/100 "STRONG" — a low-information blob is trivially *unlike* the shelf. A predictive score manufactured false confidence. Fix: verdict now driven by feed-size legibility (computable) + tech compliance; CLIP demoted to informational.
- **#62 "VidIQ 95/100" (ADR-0012):** Volhynia's packaging was locked on one confident ENRICHMENT number, with no record that `title_scorer`, `/curiosity`, or `thumbnail_checker` ever ran, and no thumbnail concept. The prose rule existed and didn't bind. Fix: `tools/preflight/packaging_lock.py` — four mechanical filters + recorded enrichment in an `<!-- AUTO:packaging-lock -->` zone; `--validate` BLOCKS unless every filter PASSES and the judgment field is filled.

If you are building or modifying a checker, these bind:
1. New check = a pass/fail **necessary condition**. A predictive "this will work" score is the forbidden failure mode (ADR-0007 is "reversible only by re-introducing" one).
2. **Enrichment can never upgrade a filter FAIL**; a low enrichment value emits a REVIEW nudge, never a block.
3. A packaging rule that must BIND goes in `packaging_lock.py` as code — prose in a command file demonstrably does not bind (that's how #62 happened).
4. Root-cause fixes go upstream: when the gate build exposed title_scorer's dead clickbait gate (docstring promised `_apply_tone_filter` populated `hard_rejects`; the function never existed), it was fixed IN `title_scorer.py`, not patched around in the checker.
5. Calibrate on the real corpus and pin it (`tools/tests/test_thumbnail_filters.py`) so recalibration is deliberate.
6. At this channel's traffic, learning happens via SINGLE-VARIABLE before/after swaps (title OR thumbnail, never both), judged on new-viewer CTR — a checker must not claim what only a live swap can show.

## Definition of done, per artifact (digest)

**Code change:** root cause fixed, not worked around · all tests green including previously-red ones (deps installed, not mocked) · real-data check passed with a known-true fact · commit + secret-guard discipline honored (details → extending-safely) · communicated in outcome terms (the owner is a non-engineer).
**Research file (`01-VERIFIED-RESEARCH.md`):** every fact ✅/⏳/❌, 90%+ ✅ before scripting · Phase 2 NotebookLM verification never skipped · tier tags (T1/T2/T3) applied · verbatim quotes with page numbers · load-bearing quotes read from RAW `nlm source content`, never `notebook_query` synthesis (it fabricates verbatim+pages) · unverifiable claims excluded or flagged, never included on plausibility.
**Script:** written ONLY from verified facts · `03-FACT-CHECK-VERIFICATION.md` 100% cross-checked, ✅ APPROVED before filming · `voice_lint` `cta-too-early` hard gate passes · locked = the user's T1 read-aloud passed (his declaration, never yours) → lock immediately triggers the calibration delta-mine.
**Packaging:** demand gate first (hard stop) · four filters PASS recorded by `packaging_lock.py`, `--validate` exits clean · enrichment recorded, never deciding · rendered thumbnail passes `thumbnail_image_audit.py` legibility+tech gate · 48h swap protocol armed before publish.
**Analysis/report:** distribution cited when one row can dominate, not just aggregates · every number carries n + confidence + source file · HYPOTHESIS vs VERIFIED tagged (subagent- and extremes-derived findings are hypotheses until primary-source/holdout checked) · channel n<30 numbers info-only, never constraints · numbers cross-checked against `analytics.db` · `/analyze` long-form only, never Shorts.

## The refusal list — what is never "done"

The judgment layer. Refuse to call work finished when you see:
- **Green tests, synthetic-only.** No run against `analytics.db`/CSVs/real project files = not verified, just plausible.
- **A data or visual claim nobody checked.** "I believe it was our 3rd best performer" (actual: ~11 views) is a recorded incident, not a hypothetical.
- **Aggregates hiding a distribution.** One video (Guatemala vs Belize, 23,727 subscriber views) = 51% of ALL long-form traffic; "73% subscriber-driven" collapses to ~42% without it. Report distribution/concentration, or report nothing.
- **A score treated as a verdict.** VidIQ/NLM/title_scorer/curiosity numbers are enrichment. The moment a confident number substitutes for the filters having run, you are re-creating #62.
- **"Pre-existing failure" as an excuse**, or a mock standing in for `pip install`.
- **An n<30 channel-specific number wired in as a constraint** (year -46%, colon -28% were exactly this — topic-confounded noise, later retired).
- **A pattern derived from best/worst extremes, unwired from holdout.** All four 2026-06 opening-formula candidates died out-of-sample; extremes-derived = hypothesis until holdout-tested.

## Related skills

- **extending-safely** — you're about to CHANGE code: which seam to route through, which tests must stay green, commit/secret-guard rules.
- **codebase-atlas** — you need to find the module, its entry point, or its exact run command before you can test it.
- **data-stores** — you need schemas, table→owner routing, or safe read-only query recipes for the three DBs used in real-data checks.
- **debugging-playbook** — a test or tool fails for infrastructure reasons (stale DB, dead task, MCP auth) rather than code you changed.
