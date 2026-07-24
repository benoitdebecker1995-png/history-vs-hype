# Canonical valid-latest CTR read (ctr_reads)

**Date:** 2026-07-23
**Status:** accepted

Peer to ADR-0004 (the analytics/keywords store split). This ADR exists because
"the latest CTR observation for a video" was re-implemented six times against
`keywords.db` `ctr_snapshots`, and the copies had **diverged**. A 2026-07-23
read-only audit (Codex/GPT-5.6) found the divergence was actively corrupting
title-pattern scoring.

## The defect

`ctr_snapshots` gained `is_valid`/`invalid_reason` on 2026-07-22 so the collector
double-count rows (2026-07-13/07-23) could be **quarantined without deletion**.
But only `growth_data`'s CTR fallback actually filtered `is_valid = 1` and
de-duplicated to one row per video (tie-break `ORDER BY snapshot_date DESC, id
DESC`). The other five readers did neither, so:

- an **invalid** 2026-07-23 double-count row won `MAX(snapshot_date)` over a
  video's valid 2026-07-10 row and its bad CTR became the scored value;
- videos with multiple snapshot rows on the same date were **counted multiple
  times** in pattern averages.

Measured on the live DB before the fix: the title-scoring query returned **509
rows for 275 distinct videos**, of which **36 were `is_valid=0`**. After: **276
rows / 276 videos**, freshness `2026-07-10` (not the quarantined `07-23`).

## What the seam is

`tools/discovery/ctr_reads.py` — one place that encodes "current valid CTR per
video" (`is_valid = 1`, exactly one row per video). Read-only, stdlib `sqlite3`,
never raises (returns `{}`/`None`), matching the read-side error contract.

- `latest_valid_ctr_by_video(conn, *, require_ctr=False, require_impressions=False)`
  → `{video_id: {ctr_percent, impression_count, view_count, snapshot_date}}`.
- `latest_valid_ctr_for(conn, video_id, *, after_date=None, require_ctr=True, ...)`
  → one dict or `None` (keeps the swap-ledger's on/after-swap-date semantics).
- `latest_valid_snapshot_date(conn, *, require_ctr=True)` → newest valid date,
  so a quarantined later date never reports as fresh.

The column guards are fixed literals chosen by booleans — no caller-supplied SQL
is interpolated. `require_ctr` vs `require_impressions` preserves the one real
semantic difference: `growth_data` keeps a genuine 0.00% CTR on real impressions
(so it filters impressions, not CTR); the title/packaging readers want CTR > 0.

## Decision — extract the one correct query, route every consumer through it

This is an **extract-and-route**, not a new invention: the correct logic already
existed inline in `growth_data`. It was factored out and the six consumers now
call the seam — `title_ctr_store` (pattern scoring + freshness),
`packaging_autopilot`, `swap_ledger`, `growth_data` (the origin, now unified),
and the per-date readers in `ctr_tracker` + freshness/attribution in `benchmarks`
(which keep their all-videos-on-a-date shape but gained the `is_valid = 1`
predicate).

Deletion test: removing `ctr_reads` re-spreads the `is_valid` + dedup logic back
across six callers — exactly the divergence that caused the bug. It earns its place.

## Consequences

- **Test surface.** `tests/unit/test_ctr_reads.py` pins the seam (invalid
  exclusion, same-date dedup to highest id, freshness, after-date); a
  consumer-level pin in `tests/unit/test_title_ctr_store.py` proves a quarantined
  99% snapshot cannot move a pattern score. Three fixtures were corrected to
  model the real schema (they had omitted `is_valid` or `view_count`).
- **No public-shape change.** Consumers return the same shapes as before; only
  the rows selected changed (valid + de-duplicated). Verified against the live
  keywords.db copy.
- **Re-litigation guard.** A future reader tempted to hand-roll another
  "latest CTR" `SELECT` against `ctr_snapshots` should call `ctr_reads` instead.
  Adding a new column guard = a new boolean on the seam, not a new query.
