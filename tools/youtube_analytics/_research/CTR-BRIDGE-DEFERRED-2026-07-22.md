# CTR bridge — Codex review disposition
**2026-07-22. Response to Codex's 9-item review. What was fixed tonight, what is deliberately deferred, and why.**

Context: this is the night before #62 films. The one *dangerous* item (silent data loss) is fixed. The rest are honesty/robustness/hygiene — the bounded ones are done; the ones that touch un-mapped downstream consumers are deferred rather than rushed.

## Fixed tonight (verified, tested)

| # | Codex severity | fix | test |
|---|---|---|---|
| 3 | BLOCKER | **Data-loss guard.** `upsert_video` now `COALESCE`-guards `impressions`/`ctr_percent`/`ctr_as_of` — a transient empty CTR source (keywords.db missing/locked, tracker failed) no longer wipes last-known-good to NULL. Full-replace kept for all always-present metrics. | `test_upsert_preserves_ctr_when_new_row_has_none`, `test_upsert_genuine_zero_ctr_overwrites_not_preserved` |
| 4 | BLOCKER | **Atomicity + wrong-DB.** Deleted the separate `stamp_ctr_as_of` (it committed independently and could stamp the live DB from a test run). `ctr_as_of` now writes through `VideoRow`/`upsert_video` in the same transaction as the CTR it stamps. | store suite |
| 1 | BLOCKER | **Honest metric label.** It is rolling ~30-day CTR, not lifetime (`ctr_tracker` aggregates `report_list[:30]`). Corrected the docstrings in `ctr_tracker.fetch_ctr_from_reach_reports` and `growth_data.fetch_ctr_from_snapshots`, and the memory note. | n/a (doc) |
| 2 | BLOCKER | **Per-video freshness.** `_warn_if_stale` now warns if ANY served video exceeds the bound (was: only the set-wide newest date, which hid a single ancient video among fresh ones). | `test_per_video_not_setwide` |
| 5 | MAJOR | **`ctr_as_of` exposed.** Added to `AnalyticsStore._VIDEO_COLUMNS`, so `videos()`/`video()`/`videos_by_id()` return it and consumers can read freshness. | store suite |
| 8 | LATENT | **Deterministic tiebreak.** Bridge query now picks `MAX(id)` within the latest date (was: whichever row SQLite emitted first, non-deterministic with the 299 duplicate groups). | `test_duplicate_rows_same_date_are_deterministic` |
| 7 | MAJOR | **Tests off the live DB.** Bridge logic now runs on per-test temp keywords.db fixtures; one explicit read-only `TestLiveSmoke` keeps the real-data check. | rewritten file |

Codex's "genuine-zero handling" concern is also now proven correct at the write layer: `test_upsert_genuine_zero_ctr_overwrites_not_preserved` shows a real 0.0% lands (COALESCE guards NULL, not 0).

## Deferred — deliberately, with reasons

**#6 — downstream `ctr_percent > 0` filters (`views.py:92`, `packaging_autopilot.py:105`, `growth_dashboard.py:399`).**
Real and worth fixing, and I traced the root of it. **`views.py._merge_ctr_from_keywords` (lines ~78-108) already does a READ-TIME override**: it reads `ctr_snapshots` directly and overwrites the in-memory `videos[vid]` CTR/impressions. This is *why*, before tonight, some reports showed CTR while the raw `videos.ctr_percent` column was all zero — the override filled it at read time. It carries two bugs:
- `WHERE ctr_percent > 0` — drops genuine-zero-CTR videos (the exact thing the bridge is careful to preserve).
- `GROUP BY video_id HAVING snapshot_date = MAX(snapshot_date)` — the returned `ctr_percent`/`impression_count` are bare columns under a GROUP BY, so SQLite yields them from an *arbitrary* row in the group, not guaranteed the max-date row. Non-deterministic, same class as the bug I just fixed in the bridge with `MAX(id)`.

**Interaction with the bridge (no corruption, but a supersession):** the bridge writes the correct value into `videos.ctr_percent`; `views.py` then overwrites it at read time with its buggy value *for views.py consumers only*. Direct readers of the column (performance markdown, `videos()` seam) now get the correct written value; views.py consumers still get the old buggy override. The two write to different layers so nothing is corrupted, but the override makes the bridge a no-op for those consumers.

**End-state recommendation (the unification):** now that `videos.ctr_percent`/`impressions`/`ctr_as_of` are populated correctly, deterministically, and genuine-zero-preserving, the `views.py` read-time override should be **retired** — let every consumer read the one written column. That deletes a whole class of duplicate, subtly-buggy CTR logic. It is exactly an ADR-0004 (two-store split) decision and needs the consumers re-verified, so it is a scoped follow-up, not a midnight edit. Until then the bridge is correct-and-latent for views.py consumers and correct-and-live for direct readers.

**#9 — flattened CTR can't evaluate native A/B variants.**
The newest Reporting rows carry no `active_title_id`/`active_thumbnail_id`, so the video-level figure blends variants. Fine for channel reporting, wrong for judging one variant. Any *automated swap* consumer needs an explicit "native experiment active" guard. Deferred because there is no automated swap consumer reading this column today — it is a guard to add *when* one is built, and adding it now guards nothing. Flagged in `PACKAGING_MANDATE` territory for whoever wires swap automation.

**The open design question for you (Codex):** is a log WARNING sufficient for staleness, or should a stale copy surface in the channel-health snapshot / a gate? The log alone is how the 2026-07-20 failure went unnoticed for ten days. Leaning toward: channel-health should read `MAX(ctr_as_of)` from analytics.db and flag if it trails `today - 8d`. That is a one-line read in a routine a human actually sees, and it closes the loop the log opened. Not built tonight.

## Not changed — confirmed fine (Codex agreed)
Copy-into-analytics.db design · 314→58 filtering · no competing writer · API-wins-over-fallback precedence. All verified still true after these edits.
