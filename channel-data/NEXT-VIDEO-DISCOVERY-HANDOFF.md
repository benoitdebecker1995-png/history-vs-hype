# HANDOFF — building a way to find the next video: real demand, nobody serving it

**Written 2026-07-28.** Pick this up by saying something like *"continue building a way to figure out the
best possible next video that is original and try something there is a demand for but nobody does on
YouTube."*

**Read these first, in order:** this file → `channel-data/BREAKOUT-MECHANICS-2026-07.md` →
`channel-data/BREAKOUT-HYPOTHESES.md` → `tools/TOPIC-RUBRIC.md`. Then `.claude/skills/production-map`.

---

## 1. The problem, stated precisely

Find a topic where **all four** hold:

1. **Demand exists** — an audience is actively asking about it *now*.
2. **Supply doesn't** — no good English coverage answers the actual question.
3. **It's ours** — history with a mechanism, modern relevance as a closing rhyme, not a geopolitics
   explainer. Test: *"will this matter in 10 years regardless of who's in power?"*
4. **A stranger parses it cold** — no prior knowledge required to understand why the title matters.

Point 4 is not decoration. It is the **only structural property** the channel's single breakout
(Guatemala/Belize, 292K impressions at 7.66%) had that nothing else has had. Every other video asks the
viewer to already care about a named dispute.

---

## 2. What we know that constrains the search

**Serve size, not click-through, is the constraint.** 63.5% of all browse impressions in channel history
went to one video. 15 of 56 were ever served ≥2,000 browse impressions; **41 were never meaningfully
tested.** Great packaging on a small pool stays small. Full workings in `BREAKOUT-MECHANICS-2026-07.md`.

**There are TWO failure modes and they need opposite fixes.** This was only understood on 2026-07-28:

- *Never served* — no pool. Bir Tawil 2.5k, Nigeria/Cameroon 369, Honduras 138. Packaging could not have
  saved these.
- *Served once, then cut* — **#59 (I/P Palestine) took 9,626 impressions on day one, 88% of its lifetime,
  then collapsed to ~44/day by day three.** YouTube ran a test batch, it didn't convert, serve stopped.
  **A total-impressions threshold cannot tell these apart** — #59 would have "passed" the pre-registered
  9,000 bar while being a total failure.

**Search is ~5% of this channel's traffic.** So *search volume is the wrong demand proxy.* The channel
lives on Browse. The right question is **"do comparable-size channels get large views on this exact topic
right now?"** — a competitor/comment question, not a keyword-tool question.

**Four candidate predictors were tested and all four failed** (CTR, retention, thumbnail feature tags, peer
coverage). Escalation is not predictable from any data we hold. Anything claiming otherwise is overfitting.

---

## 3. The insight to build on

**The Panama pocket was found by comment-mining, not by search volume.**

Mining 1,711 comments across 16 competitor videos surfaced **23 self-identified Panamanian voices and
exactly one Spanish-language comment** — proving the national audience watches this topic *in English*.
Their two highest-liked comments, on two different channels, ~2,800 likes combined, asked the same
question: *how did Panama get the canal back?* That became the title.

Comment sections are the only demand signal that is simultaneously:
- **evidence an audience exists** (likes on the question),
- **evidence supply is missing** ("he skips some important facts", "this lacks a lot of background"),
- **pocket-identifying** ("as a Panamanian I never expected…").

Search tools give you (a) only. **Systematising this mining is the highest-value thing to build.**

---

## 4. What already exists (don't rebuild it)

| tool | what it answers | limits |
|---|---|---|
| `/greenlight --scan` (`tools/discovery/discovery_scanner.py`) | autocomplete demand + competitor gaps + Trends, ranked | search-anchored; ~90–120s; scores a *space*, not a gap |
| `tools/packaging_intel.py` → `get_topic_viability()` | competitor outlier count + demand proxy + own coverage | needs a candidate topic as input |
| `tools/preflight/serp_title_study.py` / `serp_thumb_study.py` | **live** SERP: which title/thumbnail operations are absent | needs a query; run per-candidate |
| `/comment-mine` | audience demand from competitor comment sections | manual invocation, one topic at a time |
| `tools/TOPIC-RUBRIC.md` v2 | scored comparison of 2+ fresh candidates | comparison, not generation |
| `tools/intel/intel.db` | 1,801 competitor videos, outlier flags | **views only — no impressions, no CTR**; stale 2026-07-13 |

**The gap:** every one of these **scores a candidate you already have.** Nothing *generates* candidates by
sweeping for demand-without-supply. That inversion is the build.

---

## 5. The build

A **gap-hunter** that sweeps and ranks, rather than scoring one input at a time.

**Stage 1 — harvest.** For the tracked competitor set (`channel-data/competitor-channels.yaml`, 20
channels), pull recent high-performing videos and mine their comment sections at scale for three patterns:
- *unmet-supply*: "skips", "lacks", "didn't mention", "nobody talks about", "wish someone covered"
- *pocket*: "as a [nationality]", "I'm from", "my country", "rare to see videos about"
- *repeated question*: the same question asked by many people under different videos

**Stage 2 — cluster** the harvested questions into topic candidates. Rank by likes-weighted volume, number
of distinct source videos (a question recurring across channels is stronger than one thread), and pocket
density.

**Stage 3 — supply check.** For the top candidates, run the existing `serp_title_study.py` to confirm the
question really is unanswered on the live shelf. This is where an existing tool slots straight in.

**Stage 4 — identity gate.** Apply the channel DNA test and the cold-parse test (§1.3, §1.4) by judgment.
**Do not automate this into a score** — per ADR-0012, filters decide and scores inform.

**Reuse, don't rebuild:** `tools/youtube_analytics/comments.py` for fetching (yt-dlp is bot-walled — see
`reference-comment-transcript-data-api-fallback`), `serp_title_study.py` for supply, `packaging_intel.py`
for the competitor side, and the `intel.db` schema for storage. Route new code through the seams in
`.claude/skills/extending-safely`.

**Honesty guard:** this finds *candidates*, not winners. It cannot predict serve — nothing can. It narrows
the field to topics that have a pool and an unanswered question. That is all it should ever claim.

---

## 6. State of the measurement work (context you'll need)

Rebuilt 2026-07-28 because the instrument couldn't answer the pre-registered question.

- `ctr_snapshots.impression_count` is a **sliding ~30-day sum ending ~D−3** — it cannot answer "first-28-day
  impressions". Left alone (six consumers, ADR-0017).
- **`impressions_daily`** added — per-video per-day grain, PK `(video_id, metric_date)`, upsert on newer
  `report_create_time`. Ingest is idempotent, so a missed run self-heals.
- `HvH-CtrTracker` was **weekly (Mondays)** — that's why #59's launch window was lost. Now daily.
- **The Analytics API has no `impressions` metric** (verified: HTTP 400). Only
  `channel_reach_basic_a1` carries thumbnail impressions, with a `date` column — cumulative must be summed.
- **Reporting API retention is ~60 days.** Only **two** complete 28-day windows are reconstructable
  (2,422 and 3,088). The 9,000/4,500 thresholds rest on **n=2** — say so whenever you cite them.
- Manual Studio Advanced-mode exports (`tools/youtube_analytics/studio_import.py`, `--surface browse
  --start --end`) are the **only** route to older history. ~16 exports would give a real baseline. Needs no
  code — it's data entry, and it's still outstanding.

**Open:** `channel_reach_combined_a1` job was created to test whether **browse-only** impressions are
obtainable. H3 is framed on browse; the running job gives total across all surfaces. **Check its columns
once reports generate** — if it carries `traffic_source_type`, add that dimension to `impressions_daily`.

---

## 7. Known-bad in the evidence base — fix before trusting it

1. **Thumbnail rules are computed on unserved videos.** 38 of 56 have <1,000 lifetime browse impressions,
   so the feature deltas in `CTR-THUMBNAIL-FINDINGS-2026-06.md` (−0.71 doc, +0.65 map, −0.52 busy) are
   medians over three-digit-impression noise. **Recompute restricted to served-only (n≈18).**
2. **That file contradicts itself.** Its validation table kills "red pop" (−0.67, "OVER-FIT, KILLED") and
   forty lines below prescribes red as winner-recipe item #3; `THUMBNAIL-CRAFT-RECIPE.md` [T2] rule 5 still
   calls it the channel's look-here signal. **Any agent reading top-to-bottom gets the killed rule.**
3. **5 swap experiments sit PENDING and unread** in `keywords.db.swap_experiments` (from June, one on a
   19,388-impression video). **This is the channel's only within-video causal evidence.** Harvest it.
4. **`thumbnail_features` is frozen** — 47 of 58 rows, six booleans, no writer script, no *operation*
   column. The generator's core decision variable (the operation taxonomy) has never been tested on this
   channel's own data.

---

## 8. Immediate state / blockers

- **`claude` CLI auth: FIXED** 2026-07-28 23:30 (`claude auth login --claudeai`; the desktop app and the
  CLI are separate logins). A pre-flight now fails with **exit 78** and an actionable message instead of
  four silent `1`s — `.claude/routines/_lib-preflight.ps1`, dot-sourced by all seven wrappers.
- **Current routine failures are a usage session limit**, not auth. Different cause, benign.
- **`HvH-GrowthRefresh` still fails**: takes ~42 min against a PT30M task limit, killed almost daily since
  2026-07-12. Root cause is serial per-video API calls with 500-retries in `growth_data.py`. **Do not just
  raise the limit** — the standing rule is root cause over workaround.
- **Reconcile hasn't archived publishes since 2026-07-23.** First successful run should catch up.
- **VidIQ CSV export is 8 months stale** (2025-11-19). Manual pull; unused for anything load-bearing.

## 9. The video in flight

**#36 Panama** — research CLOSED at 123 claims, 6 primary documents local, brief at
`video-projects/_IN_PRODUCTION/36-panama-canal-deconcini-2026/RESEARCH-BRIEF-2026-07-28.md`.
Remaining: Act 5 rewrite (the Security Council chair detail), Act 7 reshape, the creator's read-aloud, and
**the thumbnail — the binding constraint** (one video above 4% CTR in twelve this year).

**Before it publishes:** add a *shape* criterion to H3 in `BREAKOUT-HYPOTHESES.md`, dated — e.g. day-1
share below ~60%, or a floor on days 8–28. #59 proved a total-only threshold can't distinguish a demand
pocket from a failed test batch. **Do not retune the 9,000/4,500 numbers** — that would be post-hoc.
