# ADR-0024 — Analytics CTR reads carry their grain

**Status:** Accepted · **Date:** 2026-08-03
**Extends:** ADR-0017 (canonical valid-latest-CTR read) to the second store.
**Applies:** ADR-0020 (strategy claims carry the same evidentiary burden as on-screen claims) to
instrument output.
**Supersedes nothing.** ADR-0004 (two-store split) stands — this adds a seam *inside* `analytics.db`.

## Context

`analytics.db` holds two answers to "how many impressions did this video get", and they differ by
roughly fifty times:

| | source | grain | stamped with |
|---|---|---|---|
| `videos.impressions` / `.ctr_percent` | collector | **trailing snapshot** | `videos.ctr_as_of` |
| `studio_ctr_rows.impressions` / `.ctr_percent` | Studio CSV export | **lifetime** | `studio_ctr_imports.exported_at` |

On 2026-08-03 a packaging analysis for project #67 read the first as the second. Measured live:

- snapshot median **56** impressions, `ctr_as_of = 2026-07-28` on 57 of 58 rows
- lifetime median **2,923** impressions, `exported_at = 2026-07-23`, 16 of 57 videos over 5,000
- the channel breakout reads **3,915 @ 11.03%** in the snapshot and **292,398 @ 7.66%** lifetime

Three strategy conclusions were published off the error and written into decision documents: that the
binding constraint was impressions ("only one video of 58 was ever served"); that CTR on this channel
is bimodal at 11% or 2% with nothing between; and that `title_scorer` is anti-predictive (r = −0.053
against snapshot views — actually **r ≈ +0.155** against lifetime CTR, n=35). A title was locked on
the third. **All three were caught by the channel owner, none by a gate.**

### Why the existing safeguards did not catch it

Nothing was missing. **`AnalyticsStore.latest_studio_lifetime()` already existed and was correct** —
it filters `window_kind = 'lifetime'` and returns `exported_at`. `AnalyticsStore.videos()` already
returned `ctr_as_of` in the same row as `impressions`. The failure was that:

1. **The correct method was named and documented as niche.** "latest_studio_lifetime … *Used by the
   CTR validator*" does not read as *the* answer to "how did this video do". It had **one** production
   caller in the whole repo (`ctr_tracker.py`). Nobody in the packaging path used it.
2. **The seam was bypassed entirely.** At least twelve modules open `analytics.db` with
   `sqlite3.connect()` and hand-rolled SQL. `.claude/rules/python-tools.md` already says *"route
   through the seam, don't re-implement it"*; ADR-0017 exists because five of six consumers
   hand-rolling one read got it wrong. **The same failure recurred in the other store.**
3. **Provenance was available but optional.** `ctr_as_of` sat in the returned row and was ignored,
   because nothing made carrying it a condition of using the number.
4. ⛔ **`PACKAGING_MANDATE.md` actively misdirected.** Its "Data vintage upgrade" paragraph stated
   that *"real per-video Studio impressions+CTR for ALL 56 long-form [are] now in `analytics.db`
   (`videos.impressions/ctr_percent`)"* — conflating the Studio lifetime export with the collector
   snapshot columns. The same document's 2026-07-23 section correctly names `studio_ctr_rows` as
   "the freshest CTR truth", so the file contradicted itself and the wrong half was read first.
   **Corrected in place as part of this ADR.**

## Decision

**A CTR/impressions read from `analytics.db` returns its grain, its as-of and its source table, or it
is not a read.**

Two methods on `AnalyticsStore`, named for what they mean rather than where they came from:

- **`lifetime_ctr_by_video()`** — the canonical "how did this video actually do". Peer to
  `tools.discovery.ctr_reads.latest_valid_ctr_by_video` (ADR-0017), which does the same job for
  `keywords.db`.
- **`snapshot_ctr_by_video()`** — the trailing window, when that is genuinely what is wanted.

Both stamp **every row** with `grain` (`"lifetime" | "snapshot"`), `as_of` and `source_table`. Neither
can hand back a number stripped of its provenance. `latest_studio_lifetime()` is retained unchanged —
`ctr_tracker` depends on it — and `lifetime_ctr_by_video()` delegates to it.

`videos()` keeps returning the snapshot columns (callers legitimately want the rest of the row), but
its docstring now states the grain and points at the lifetime method.

## Consequences

- **The wrong read is still reachable** — `videos()[...]["impressions"]` still works. This ADR makes
  the right one discoverable and the wrong one documented, not impossible. Hard-blocking would break
  legitimate callers for a mistake that documentation and naming can carry.
- ✅ **The packaging path is migrated (2026-08-03).** The "twelve modules hand-roll" figure in the
  first draft of this ADR counted every module that *opens* `analytics.db`; only **two** actually read
  the snapshot CTR columns, and both are now on the lifetime seam:

  | Module | Was | Damage measured on the live tree |
  |---|---|---|
  | `packaging_autopilot.py` (channel-health block) | `AVG(ctr_percent) FROM videos`, `impressions > 500` | **Swap candidates reported 2; true answer 42.** The >500 reliability test is nearly unsatisfiable against a column whose median is 56, so the detector was silently reporting almost nothing to fix. Avg CTR read **5.45%** vs a true **3.20%** |
  | `packaging_intel.py` (`_get_own_channel_signal`) | `SELECT … ctr_percent FROM videos` | Understated the catalogue's CTR on every topic-similarity lookup |

  `candidate_preflight`, `retitle_gen` and `outlier_title_dissector` open `analytics.db` but **never
  read these columns** — no change needed. The remaining `ctr_percent` readers in `tools/` are against
  `keywords.db` / `ctr_snapshots`, which is ADR-0017's seam and already correct.

  Pinned by `tests/test_packaging_ctr_grain.py`, which builds a fixture where the two grains disagree
  in the same direction as the live data and asserts the packaging path picks lifetime.
- **Any document quoting an impressions or CTR figure is now expected to name its grain.**
  `.claude/rules/research-verification.md` carries the rule; `PACKAGING_MANDATE.md` figures sourced
  from the snapshot columns need auditing against it.
- **Tests pin the distinction** (`tests/unit/test_studio_import.py::TestCtrGrainSeparation`): the two
  grains must disagree, every row must carry `grain`/`as_of`/`source_table`, and a missing lifetime
  import returns `{}` rather than raising.

## Alternatives considered

- **Delete or rename `videos.impressions`.** Rejected: the collector legitimately produces a trailing
  window, and other consumers want it. The grain is real; the ambiguity was the defect.
- **A new `tools/youtube_analytics/ctr_reads.py` module** mirroring the `discovery` one. Rejected on
  extend-don't-add: `AnalyticsStore` is the sanctioned seam for this store per ADR-0004, and a second
  entry point would recreate the ambiguity one layer up.
