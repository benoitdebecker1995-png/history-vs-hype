# CTR improvement — the original question, now that the data is trustworthy
**2026-07-22, for Codex. You can read this repo but not write it — return findings in chat; I apply any code fix.**

The original ask was "how do we improve CTR on our videos." Answering it surfaced that the CTR data was unreadable (all zeros in `analytics.db.videos`), which spawned the bridge work in `CTR-BRIDGE-DEFERRED-2026-07-22.md`. This brief closes the loop: **Phase 1 — confirm the numbers are now accurate. Phase 2 — the improvement analysis.** Do Phase 1 first and report it before Phase 2; if the data still can't be trusted, Phase 2 is worthless.

---

## Phase 1 — verify the CTR numbers are accurate

What was fixed (see the deferred doc for detail): `analytics.db.videos.ctr_percent`/`impressions`/`ctr_as_of` are now populated from `keywords.db.ctr_snapshots` via the growth_data bridge, deterministically, preserving genuine-zero, with a freshness stamp and a staleness warning. The metric is **rolling ~30-day, not lifetime** (`ctr_tracker` aggregates `report_list[:30]`).

Verify, and tell me the answer to each:

1. **Which number should the analysis trust?** Three surfaces exist and can disagree:
   - `keywords.db.ctr_snapshots` — the source of truth (rolling 30-day, video-level, per snapshot_date).
   - `analytics.db.surface_ctr` — the browse-vs-suggested split (**the most useful lever for improvement**, because browse and suggested CTR are different fixes). ⚠ **But it has NO API writer — it is a manual YouTube Studio CSV import and is STALE (last export ~2026-02-23).** The API cannot pull per-source CTR at all (the traffic-source query returns only views + watch time). So treat surface_ctr as directional/old, not live; if the browse-vs-suggested split is load-bearing for a recommendation, say so and I'll ask the user to refresh the Studio CSV export.
   - `analytics.db.videos.ctr_percent` — now a stamped cache of the first, but **`views.py._merge_ctr_from_keywords` overrides it at read time with a buggy query** (`WHERE ctr_percent>0` drops genuine-zero; bare columns under `GROUP BY … HAVING MAX` return an arbitrary row). So a consumer going through views.py may see a *different, wrong* number than the column holds.
   **Decide: for CTR-improvement analysis, read `surface_ctr` + `ctr_snapshots` directly and ignore the views.py path. Confirm that's right, or argue otherwise.**

2. **Is the views.py override worth retiring now** (the deferred unification), or does anything depend on its exact current behavior? If retiring is safe, give me the precise change and the consumers to re-verify and I'll apply it.

3. **Spot-check 5 videos** end to end: `ctr_snapshots` latest row → `surface_ctr` browse/suggested → what a report actually displays. Flag any mismatch. If they reconcile, say so plainly — that's the green light for Phase 2.

---

## Phase 2 — how to improve CTR, grounded in the now-trusted data

### ⭐ Primary data source for Phase 2: a FRESH Studio CSV export

The user is exporting current **lifetime** per-video CTR from YouTube Studio (the API cannot pull it — see Phase 1). Use it as the ground truth for CTR, not the rolling-30-day snapshots.

- **Location:** newest `*.csv` in `channel-data/analytics-exports/` dated on/after 2026-07-22. If none newer than 2026-02 exists, STOP and tell me the export hasn't landed — do not fall back to the stale surface_ctr and present it as current.
- **Columns you'll get** (Studio "Table data" format, confirmed): `Content` (= video_id, matches `analytics.db.videos.video_id`), `Video title`, `Impressions`, `Impressions click-through rate (%)`, `Views`, plus others. The first row is `Total` — skip it.
- **This is lifetime OVERALL CTR per video** (not split by surface). For browse-vs-suggested, the stale `surface_ctr` is the only split we have; if a recommendation hinges on the split, say so and I'll ask for the traffic-source export too.
- Join `Content` → `videos` for topic_type/retention/duration; join `title_features` for title structure. Cross-check the CSV's Impressions against `ctr_snapshots` (rolling) to sanity-check the two sources agree in direction.


**Read these first** — the channel's packaging doctrine is already written and CTR is its #1 stated bottleneck:
- `tools/PACKAGING_MANDATE.md` (the gate philosophy; years/colons are graded penalties not bans)
- `.claude/REFERENCE/TITLE-GENERATION-PROTOCOL.md` and `tools/title_scorer.py` / `title_features.py`
- `tools/preflight/thumbnail_checker.py` (text-overlay mandatory, no-face, maps for territorial)
- memory `reference-ctr-packaging-playbook.md` — title = Recognition×Stakes×Curiosity−Abstraction; thumbnail = one focal + red pop + legible verdict
- the opener scan `channel-data/OPENER-CRAFT-SCAN-2026-07-22.md` (already found the biggest signal — see below)
- `CLAUDE.md` "Packaging-First Workflow" and the channel DNA

**Hard constraints on the analysis — do not violate these, they are established channel rules:**
- **CTR is a title+thumbnail problem, not a content or opener problem.** Opener retention is a *hold* lever; CTR is a *click* lever. Keep them separate.
- **n < 30 per video = directional only.** This channel has ~58 videos, most impression-starved (33/56 under 500 browse impressions). Do not build a "finding" on one video's CTR. Where you can, compare against niche-wide patterns, not just this channel. See memory `feedback-channel-data-too-small`.
- **Browse CTR ≠ suggested CTR.** They are different algorithms and different fixes. Split every claim by surface. A video can have great suggested CTR and dead browse CTR (or vice versa) and the packaging implication differs.
- **Filters decide, scores inform.** title_scorer/VidIQ are enrichment, not verdicts (ADR-0012). Don't present a score as a ruling.
- **The biggest known signal is #59** (`OHWq4jY8iAY`): ~21K browse impressions at ~1.5% CTR — YouTube pushed it ~40× harder than anything else and almost nobody clicked. That is the single most informative packaging failure on the channel; a video that gets impressions and doesn't convert is worth more analysis than fifty starved ones.

**What I want back (ranked, single-variable, testable — the channel A/B-tests packaging natively, all combos):**
1. **The impression-bearing set only.** List the videos actually getting shown (browse and suggested separately), their CTR, and rank by *impressions × (channel-median-CTR − their-CTR)* — i.e. where the most clicks are being left on the table. Starved videos can't be improved by packaging; drop them.
2. **Title patterns** that separate the channel's higher-CTR from lower-CTR videos *within the impression-bearing set* — as hypotheses, grounded in title_features, cross-checked against the niche where the channel n is too small. Each as a single-variable swap.
3. **Thumbnail patterns**, same discipline, against thumbnail_checker's dimensions and the outlier corpus.
4. **The #59 teardown** specifically: given 21K impressions and 1.5% CTR, what is the highest-probability single-variable title/thumbnail swap, and what does the live SERP it competes in look like (packaging-adversary style — scroll-past hypotheses, not a score).
5. **Anything the data says that contradicts the written doctrine** — if the now-accurate numbers falsify a PACKAGING_MANDATE rule, that's the most valuable thing you can find. Flag it with the evidence.

Return Phase 1 as a short verdict (trustworthy / not, and why), then Phase 2 as the ranked list. Keep every improvement claim to a single testable variable — the channel can only learn from one-variable swaps.
