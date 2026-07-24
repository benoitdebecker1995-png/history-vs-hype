# CTR bridge — pressure-test request for Codex
**2026-07-22. A fix is already applied and tested. This asks you to red-team the DESIGN and the WIRING, not to write code (you can read this repo but not write it — return findings in chat).**

## What was broken

`analytics.db.videos.ctr_percent` and `.impressions` were **0/NULL for all 58 videos**, so every consumer of that column — the performance markdown, growth dashboard, any packaging analysis — read zero. Two separate analyses this week concluded "the channel has no CTR data" from it.

The data was never missing. It lives in **`keywords.db.ctr_snapshots`** (1,171 rows, weekly refresh via `tools.youtube_analytics.ctr_tracker`, latest 2026-07-13). The Analytics API does **not** expose `videoThumbnailImpressions` for this channel — `growth_data.fetch_video_ctr_bulk`'s own docstring documents this and returns `{}`. `ctr_tracker` gets the numbers from the *Reporting* API instead and writes them to keywords.db. **Nothing bridged keywords.db → analytics.db.videos.** `growth_data --refresh` read the empty API path, stored empty, and moved on.

## What was applied

`tools/youtube_analytics/growth_data.py`:
- `fetch_ctr_from_snapshots(video_ids)` — latest `ctr_snapshots` row per video **where `impression_count > 0`**, returned in the exact `{vid: {impressions, ctr_percent}}` shape `store_videos` already consumes.
- `merge_ctr_with_snapshot_fallback(ctr_data, video_ids)` — API values win where present; snapshots fill the rest. Wired into the refresh at Step 3, so it runs inside the existing Routine 7 (`HvH-GrowthRefresh`, daily 07:45) with no new schedule.
- One-time backfill run against the live DB: **58/58 filled — 32 with CTR>0, 26 with a genuine 0% CTR on real impressions.**

Design choice already made and defended: I filter on `impression_count > 0`, **not** `ctr_percent > 0`. A real 0% CTR on real impressions is a true reading; the old (dead) `backfill_ctr_from_snapshots` filtered `ctr_percent>0` and would have substituted an older non-zero snapshot for a video whose latest reading is genuinely zero. Test `test_genuine_zero_ctr_with_impressions_is_kept` guards this.

Tests: `tests/unit/test_ctr_snapshot_fallback.py`, 7 cases against the real keywords.db. All green.

## What I want you to red-team

1. **Staleness ordering — RESOLVED, you were right and my "6 days" was wrong.** You found the real failure: `HvH-CtrTracker` **failed on 2026-07-20** (exit `0x8007010B` = ERROR_DIRECTORY) and `HvH-GrowthRefresh` was terminated (`0x41306`), so the newest snapshot sat at **2026-07-13 for ten days**, not six. My bridge would have copied that 10-day-old number every day with no signal. **Fixed:** schema v4 adds `videos.ctr_as_of` (the snapshot date each CTR came from — inspectable per video), and the bridge logs `CTR STALE` when the newest snapshot exceeds `CTR_STALE_AFTER_DAYS = 8` (one full weekly cycle). It still copies best-available (beats NULL) but staleness is now both stamped in the data and loud in the log. Tests: `TestFreshnessContract`. **Remaining question for you: is a log WARNING enough, or should a stale copy be surfaced somewhere a human actually looks** (channel-health snapshot, a gate)? The log alone is how the original failure went unnoticed. And separately: **the two task failures themselves are out of my scope — worth confirming ctr_tracker's ERROR_DIRECTORY is the known clean-cwd issue and not something new.**

2. **Is a denormalized copy the right call at all?** I copied CTR into `analytics.db.videos` because `AnalyticsStore` is deliberately scoped as a single seam over analytics.db and every reader already hits `videos.ctr_percent`. The alternative is readers `ATTACH keywords.db` and join `ctr_snapshots` live — one source of truth, no staleness, but it breaks the analytics.db seam and touches every reader. Which is the lesser evil for this repo? I chose the copy; argue the other side if it's stronger.

3. **`is_late_entry` / active thumbnail+title.** `ctr_snapshots` has `active_thumbnail_id`, `active_title_id`, `is_late_entry`. My bridge ignores them and takes the latest impression-bearing row. For a video mid-A/B-rotation, "latest CTR" blends variants. Does any downstream consumer need per-variant CTR, and if so does flattening to one number corrupt it? (The A/B rotation is native, all-combos — see the user's YouTube-AB memory.)

4. **The 314-vs-58 gap.** `ctr_snapshots` has 314 distinct video_ids; `videos` has 58. My join only fills the 58, which is correct for this table — but flag if any consumer expects CTR for the other ~256 (competitor/discovery tracking) and is silently getting nothing.

5. **Did I miss a consumer that writes `videos.ctr_percent`?** If some other path also writes that column, my refresh-time overwrite could fight it. `grep` for writers to `videos.*ctr_percent`. I checked `store_videos` and the dead `backfill_ctr_from_snapshots`; I did not exhaustively check.

Return a ranked list: what's wrong, what's fine, what's a latent trap. If (1) or (5) turns up a real ordering/collision bug, that's the one that matters — the rest is refinement.
