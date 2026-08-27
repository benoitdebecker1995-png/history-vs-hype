# Python conventions (`tools/`)

Applies to everything under `tools/`. Distilled from the `extending-safely` skill — read that skill
for the full seam catalogue and the extend-don't-add acceptance test. Canonical source:
`.claude/rules/python-tools.md`.

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
  CLI behaviour → subprocess pin with `PYTHONIOENCODING=utf-8`. See `tests/AGENTS.md`.
- **A change is not done on synthetic fixtures alone** — run it against the live tree and confirm a
  known-true fact.

The repo root path contains a space (`G:\History vs Hype`) — quote it in every shell command that
uses an absolute path.
