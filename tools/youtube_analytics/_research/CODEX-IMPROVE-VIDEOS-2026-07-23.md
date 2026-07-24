# Find what to improve about our videos — whole-funnel scan
**2026-07-23, for Codex. Runs while the creator films. You read this repo but can't write it — return a ranked findings list in chat; the creator reviews it after filming.**

## The point of this run

"Find stuff to improve about our videos." Broad on purpose — but grounded in the now-trustworthy data and, critically, **not a repeat of what you already found.** Three prior runs stand; build on them, don't re-derive:
- CTR / packaging red-team + the §2 experiment program — `_research/CODEX-CTR-FIX-PROGRAM-2026-07-22.md`, `CODEX-CTR-IMPROVE-BRIEF-2026-07-22.md`. The #59 title test and the doctrine corrections are already captured. Don't restate them.
- Opener/cold-open craft scan — `channel-data/OPENER-CRAFT-SCAN-2026-07-22.md`.
- The CTR data is now fixed (bridge, quarantine, validator, Studio importer). Trust it.

**Your new angle: the WHOLE funnel per video, especially the half nobody has mined yet — `retention_curves`.**

## The data you now have (all trustworthy, all in analytics.db unless noted)

- **`retention_curves`** — 5,800 rows, ~100 points × 58 videos. `elapsed_ratio` (0→1) vs `audience_watch_ratio`. **This is the untapped goldmine** — it shows exactly WHERE each video loses people, which no prior run used.
- **`videos`** — cached rolling CTR + `ctr_as_of`, `avg_view_percentage` (retention), views, topic_type, duration.
- **`studio_ctr_rows`** (via `AnalyticsStore.latest_studio_lifetime()`) — lifetime CTR ground truth, July-23, 57 videos, #59 = 1.60%.
- **`traffic_sources`** — where each video's views come from (browse/suggested/search).
- **`opener_retention`** (21 videos) — first-30s retention + hook archetype, already classified.
- **`thumbnail_features`** (47), **`search_terms`** (153).
- ⚠ `surface_ctr` is Feb-2026 stale — directional only.

## What to produce

### 1. Per-video bottleneck diagnosis (the core)
For each video with **≥500 lifetime impressions** (starved videos can't be diagnosed — list them separately and drop them), classify the SINGLE biggest leak using the funnel:

- **CLICK problem** — gets impressions, low CTR vs the channel median (2.58% overall from the fixed data). Fix = packaging. Cross-ref the §2 program; don't re-propose what's already there.
- **EARLY-DROP problem** — CTR is fine but `retention_curves` shows a steep loss in the first ~15–30% (the cold open isn't holding). Fix = opener. Give the exact `elapsed_ratio` where the cliff is.
- **MID-DROP problem** — holds the open but bleeds in the middle (pacing/structure/a dead stretch). Fix = editing/structure. Name the `elapsed_ratio` band where it sags.
- **HEALTHY** — no single dominant leak; leave it alone.

Output a table: video · impressions · CTR · avg retention · **bottleneck** · the specific evidence (the drop-point ratio or the CTR gap) · one concrete single-variable fix.

### 2. Cross-video patterns (hypotheses, not verdicts)
What do the retention winners do that the losers don't — measured off the curves, not vibes? e.g. do videos that survive the 10–20% mark share an opener archetype (`opener_retention.hook_archetype`)? Do long videos (>12 min) drop faster in a specific band? Every pattern is a HYPOTHESIS with its n, tagged for a future single-variable test. Flag anything that contradicts the existing retention notes in `channel-data/`.

### 3. The three highest-leverage fixes on the whole channel
Rank by (affected views or impressions) × (confidence). One of these should be the single change that, if the creator did nothing else, moves the most. Say why.

## Guardrails (channel rules — non-negotiable)
- **CTR and retention are different levers** — packaging fixes clicks, opener/editing fixes holds. Never prescribe a packaging change for a retention problem or vice-versa. The per-video diagnosis must pick the RIGHT lever.
- **n < 30 = directional.** 58 videos, most impression-starved. Every cross-video finding is a hypothesis until a live single-variable test confirms it. Prefer niche-wide evidence where channel n is thin.
- **Single variable per proposed fix.** No bundled title+thumbnail+edit changes.
- **Filters decide, scores inform** (ADR-0012). Propose tests; don't declare winners from correlations.
- **Don't re-litigate the CTR §2 program or the opener scan** — cite them, extend them, but the value here is the retention-curve diagnosis and the whole-funnel per-video picture nobody has assembled yet.
- **Evergreen identity holds** — improvements must keep the channel "history with modern relevance," not chase timely hooks (see `CLAUDE.md` channel DNA).

## Out of scope
- #62 (Volhynia) — it's mid-production and film-ready; do not touch its script or packaging.
- Anything requiring a new data pull the creator can't do while filming.

Return: the per-video bottleneck table (§1), the ranked cross-video hypotheses (§2), and the top-3 leverage fixes (§3). Every fix single-variable, every cross-video claim tagged with its n and CONFIRMED/HYPOTHESIS.
