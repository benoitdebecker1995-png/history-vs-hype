---
paths:
  - "tools/**/*.py"
  - "tests/**/*.py"
---

# Python conventions

Loaded only when Python files are open. Distilled from the `extending-safely` skill — read that skill
for the full seam catalogue and the extend-don't-add acceptance test.

- **Absolute `tools.` imports only.** Bare imports are the known collection-breaker. Design for
  `python -m tools.<pkg>.<module>` from the repo root.
- **Error contract:** read-side helpers never raise — return `None`/defaults or `{'error': msg}`.
  Strict single-item `load()` may raise typed exceptions; bulk discovery logs and skips. Typed
  returns are frozen dataclasses.
- **Logging** via `tools/logging_config.py`: `logger = get_logger(__name__)` at module top. CLI mains
  call `setup_logging(...)` once. Never `print()` diagnostics, never `logging.basicConfig()`.
- **Path anchoring:** `Path(__file__).resolve().parents[N]` — never cwd-relative (ADR-0008).
- **CLI shape:** argparse, mutually-exclusive `--verbose/-v` and `--quiet/-q`, epilog with worked
  `-m` examples.
- **Route through the seam**, don't re-implement it: `AnalyticsStore` (analytics.db), `KeywordStore`
  (keywords.db), `KBStore` (intel.db — needs a tmp FILE in tests, never `:memory:`),
  `VideoProjectRepo` (read-only), `tools.subtitles.parse()`, `AutoZone` (managed markdown blocks).
- **Tests land with the change.** Bug fix → regression test first. New seam → suite lands with it.
  CLI behaviour → subprocess pin with `PYTHONIOENCODING=utf-8`.
- **Tests never touch the three live DBs** — `:memory:` or `tmp_path` only.
- **No network in tests.** An autouse socket guard in `tests/conftest.py` blocks it; a test that
  genuinely needs it must be marked `@pytest.mark.network`. Four tests reached the live API for
  months while their docstrings claimed otherwise — that is the failure this prevents.
- **Fix ALL red tests, not just yours.** A missing dependency means `pip install`, never a mock,
  skip decorator, or `sys.modules` injection.
- **A change is not done on synthetic fixtures alone** — run it against the live tree and confirm a
  known-true fact.
- **A scorer is not done until it is correlated against outcomes (ADR-0029).** Any tool emitting a
  number a human reads to make a decision must either be checked against what actually happened, or
  ship with a non-predictive label. `title_scorer`'s composite ran for about a year unchecked; when
  finally measured against `channel-data/analytics-exports/Table data.csv` it scored **+0.173**
  Spearman against real CTR, and the titles it rated **100 averaged 2.67% CTR against a 3.05% channel
  mean** — its strongest recommendation was its worst advice. An unvalidated number in a guidance
  document is worse than no number, because it displaces judgement.
- **Degrade loudly, never silently.** A checker that drops a component must say so in its result, not
  return a plausible default. `_calculate_flesch` returning `0.0` on a corpus failure would read as
  "maximally complex" on every section and invent readability cliffs — so it returns `None` and every
  result path carries a `READABILITY NOT MEASURED` advisory. Silence and a wrong number are the same
  failure; only the wrong number is harder to catch.
