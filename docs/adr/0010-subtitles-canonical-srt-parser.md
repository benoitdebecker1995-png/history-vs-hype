# subtitles: one canonical SRT parser

**Date:** 2026-06-25
**Status:** accepted

Peer to ADR-0008 (`VideoProjectRepo`) and ADR-0009 (`title_features`). This ADR exists because parsing an `.srt` file was implemented **five times** across the codebase — three hand-rolled regex parsers returning three different dict shapes, one using a third-party library, and one in `title_generator` — and a `/improve-codebase-architecture` pass (2026-06-25) surfaced it. Future runs that re-find scattered `parse_srt` functions should be answered with this ADR.

## What the seam is

`tools/subtitles.py` — stdlib only.

- **`Cue`** — frozen dataclass: `start`/`end` (seconds), `text` (tag-stripped, whitespace-normalized), `index`, and `raw_start`/`raw_end`/`raw_text` so a rewriter can round-trip.
- **`SubtitleTrack`** — the parsed track plus the read projections the callers needed: `text()`, `sentences()` (terminal-punctuation grouping), `window(center, half)`, `at(t)`.
- **`parse(path, *, fix_hour_offset=False)`** / **`parse_text(content, ...)`** — never raises on a decode error (encoding ladder + lossy fallback). `fix_hour_offset` applies the +1h export-bug correction when the first cue starts near 3600s (the legacy retention behavior).

## Engine — hand-rolled union, not a library (corrected mid-design)

The design grill first chose the `srt` third-party library *on the stated premise that it was already an installed dependency* (it is imported by `corpus_builder`). Verification before building showed that premise was **false**: `srt` is not installed and not declared in any requirements/pyproject, so `corpus_builder` could not even be imported. With the premise corrected, the choice was remade: a **hand-rolled, stdlib-only** engine — matching the project's stdlib-only posture (e.g. `project_scanner` advertises "All stdlib — no external dependencies") and avoiding a new declared dependency in every environment/CI.

The engine is the union of the three regex parsers' robustness:

- **4-encoding ladder** (utf-8-sig, utf-8, cp1252, latin-1) + lossy fallback (from `auto_srt_fixer`),
- **positional `-->` detection** — finds the timestamp line anywhere in a block, so it handles indexed *and* unindexed cues (from `retention_analysis`; stricter parsers required `lines[1]`),
- **tag stripping + whitespace normalization** (all three),
- **opt-in +1h-offset correction** (from `retention_analysis`).

It also fixes a latent bug while consolidating: the fractional-seconds field is interpreted as `int(frac) / 10**len(frac)`, so a non-3-digit fraction (`,40`) reads as 0.4s rather than the legacy `int(frac)/1000` = 0.04s. Real YouTube SRTs are always 3-digit, so no behavior change in practice.

## Side effect — fixes a broken module

`corpus_builder.parse_srt_to_text` imported `srt` at module top; with `srt` absent, the whole `corpus_builder` module raised `ModuleNotFoundError` on import. Migrating it to the seam removed that import. The module is importable again — a bug found and fixed by the consolidation, not a regression introduced by it.

## Migration — staged

First cohort (2026-06-25), the read-only consumers, each now a thin dict-adapter over the seam so their existing callers' field shapes are untouched:

- `retention_analysis.parse_srt` → `{start_seconds,end_seconds,text}`, with `fix_hour_offset=True` (preserves the offset correction `pacing_analysis` and `retention_by_topic` depend on). Dead `_parse_srt_timestamp` removed.
- `script_srt_deviation.parse_srt` → `{text,start_sec,end_sec}`. `srt_to_sentences` left in place (operates on that dict shape; `SubtitleTrack.sentences()` supersedes it for new callers).
- `corpus_builder.parse_srt_to_text` → `SubtitleTrack.text()`; `import srt` removed.

**Deferred** (recorded so a future run doesn't think they were missed):

- `auto_srt_fixer.parse_srt` — the **writer**. It needs round-trip fidelity (which the seam's `raw_*` fields now support) but it *rewrites* `.srt` files; migrating the write path is riskier and is its own pass. House pattern: defer the dangerous writer (cf. reconcile's mover in ADR-0008).
- `title_generator.extract_from_srt` (and its twin at line ~813) — two sites in the title-generation path; migrate when that module is next touched.

## Considered alternatives

- **`srt` library engine.** Rejected once the "already installed" premise proved false — it would add the project's first parse dependency. The library's `compose()` would help the deferred `auto_srt_fixer` rewrite path; revisit only if that migration motivates adding the dep, as an explicit dependency decision.
- **Canonical `list[dict]` instead of a typed `Cue`.** Rejected — typed cues end the four-field-name drift (`start_sec` vs `start_seconds` vs …) and give the projections a home. Adapters preserve the old dict shapes at the call sites for now.

## Consequences

- **Test surface.** `tests/test_subtitles.py` (15 tests) — the five parsers shared no tests. Covers indexed/unindexed cues, tag stripping, encoding fallback, variable fractional digits, all four projections, and the offset correction.
- **Behavior preserved.** Adapters return byte-identical dict shapes; `retention_pipeline`, `script_checkers`, and unit `pacing` suites pass; offset correction verified (`3605 → 5.0`).
- **Unrelated pre-existing failures.** `tools/script_checkers/tests/test_pacing.py` has 10 failures (PacingChecker returns empty `all_sections`). Verified by stash to fail **identically without this change** — a separate bug in `tools.script_checkers.checkers.pacing`, out of scope here.
- **Re-litigation guard.** Future `/improve-codebase-architecture` runs surfacing "merge the SRT parsers" should be answered with this ADR, including the deferred writer and the stdlib-only engine decision. If the deferred items need doing, supersede rather than re-fork.
