---
name: Analytics Findings
description: All analytics analysis results — retention, pacing, traffic, descriptions, comments, velocity, geography, curves, deviations, end screens
type: project
---

## Retention Audit (2026-03-29, 47 videos) (from: retention-audit-2026-03-29.md)

Full channel retention audit. 47 long-form videos analyzed with retention curves.

**Key findings:**
- Duration-retention correlation r=-0.455 (n=47). Strongest predictor of retention.
- 8-12 min sweet spot: 29.6% avg retention, 1,521 avg views (n=27). 44% hit 30%+.
- 12-20 min: 24.7% avg retention, 101 avg views (n=9). Only 1 of 12 ever hit 30%.
- 20+ min: 17.8% avg (n=3). Catastrophic.
- Myth-first structure: 30.3% retention vs 22.4% for chronological colonial. Gap = 8pp.
- Turn placement: channel avg at 42% of runtime. Competitors' best zone: 15-25% (3.2x views).
- 2026 trend: median 24.0% retention, only 2 of 10 above 28%. Not improving.
- Top 5 (35-50%): all 8-11 min, territorial or ideological, active disputes.
- Bottom 5 (12-20%): avg 15.1 min, colonial/narrative, no active modern stakes.
- Intro NOT the main problem: TOP intro drop 14.9% vs BOT 18.9% (only 4pp gap). Divergence happens at 10% mark: TOP=54%, BOT=40%.

**How to apply:**
- Hard 12-min cap implemented in script-writer-v2 Rule 32, structure-checker Constraint T, preflight scorer
- Myth-first mandatory for non-territorial implemented in Rule 33, Constraint U
- Turn at 15-25% enforced in quality checklist
- All changes in script-writer-v2 v8.0 (2026-03-29)

## Retention-to-Script Content Analysis (2026-03-20, 42 videos, 4200 data points) (from: retention-script-findings.md)

**Source:** `retention_analysis.py` — maps retention curves to SRT timestamps and classifies content type.
**Full report:** `channel-data/patterns/RETENTION-SCRIPT-CORRELATION.md`

1. **Statistics keep viewers** — 61% positive retention rate, highest of all types. Late-video stats actually GAIN viewers.
2. **Narration is safest** — -0.005 avg delta (best of all types). Causal chain narration holds viewers.
3. **"I read..." is fine mid-video** — personal_authority looks terrible (-0.044) but 86% clusters in intro drop zone (confound). Mid-video: -0.0001 (flat).
4. **Modern relevance bridges may disrupt flow** — -0.010 avg delta. Weave modern stakes INTO narration.
5. **All worst drops are intros** — Top 10 worst moments all at 2-4% position.
6. **Recovery happens mid-late with narration + stats** — Serbia video gains viewers 3 times during narration.

**How to apply:** Front-load a number in first 10 seconds. Weave modern stakes into narration (don't interrupt). Save strongest statistic for closing. Keep "I read..." for hook and mid-video only.

## Pacing Analysis (2026-03-21, 42 videos, 4096 data points) (from: pacing-analysis-findings.md)

**Key Finding: Pacing Is NOT a Retention Driver**

1. **WPM: non-significant** (r=-0.019, p=0.18).
2. **Sentence length: non-significant** (r=-0.018, p=0.21).
3. **Pause density: tiny negative** (r=-0.04, p=0.009). Negligible.
4. **Word complexity: tiny positive** (r=+0.048, p=0.002). Academic vocabulary slightly helps.
5. **No position-dependent effects.**

**Optimal WPM:** ~131 WPM (best bin), user's natural pace is ~138. Close enough.

**How to apply:** Don't add pacing rules to any tool. Content type placement matters far more.
**Tool:** `pacing_analysis.py` — `python -m tools.youtube_analytics.pacing_analysis --cached --report`

## Traffic Source Analysis (2026-03-21, 48 videos) (from: traffic-source-findings.md)

**Full report:** `channel-data/patterns/TRAFFIC-SOURCE-ANALYSIS.md`

1. **73% subscriber-driven.** Healthy channels get 30-50% from Suggested.
2. **Suggested/Related only 14%.** Packaging (CTR + AVD) is the trigger.
3. **YouTube Search only 3.4%.** Despite search-optimized topics.
4. **How/Why titles get 2x search traffic** (26.4% from search vs 12.7% for declarative).
5. **Territorial topics are most subscriber-dependent** (42%) despite highest views.
6. **Short videos (<5m) get 42% Suggested** vs 25% for 10-15m.
7. **Playlists = highest engagement** (5.8 min/view). End screens = 5.4 min/view. Both underused (<1% traffic).
8. **9 videos are search-driven** (>30% from YT Search). Evergreen assets.

**How to apply:**
- Search-optimized topics: prefer How/Why title pattern
- Browse-optimized: prefer Declarative (highest CTR)
- Territorial: optimize description first 2 lines for geographic keywords
- Add end screens to every video. Create playlists by topic type.
**Tool:** `traffic_analysis.py` — `python -m tools.youtube_analytics.traffic_analysis --report`

## Description SEO Benchmark (2026-03-20, 150 competitor + 45 own) (from: description-seo-findings.md)

**Full report:** `channel-data/patterns/DESCRIPTION-SEO-ANALYSIS.md`

1. **Our length is on target** — 2,011 chars vs 2,030 niche avg.
2. **We lead on timestamps** — 84% vs 29% niche. Keep doing this.
3. **We lead on sources** — 73% vs 43% niche. Competitive advantage.
4. **CTA is our gap** — 44% vs 94% niche. Add subscribe line to every description.
5. **First line should be thesis/hook** — not generic topic summary.
6. **Hashtags go at END** — YouTube shows first 3 hashtags above title if placed in first lines.

**Description formula:**
LINE 1: Thesis or strongest claim → LINE 2: Unique angle → 2-4 sentence summary (keyword 2-3x) → TIMESTAMPS → SOURCES → Subscribe CTA → #3-5 hashtags at end

**Tool:** `description_analyzer.py` — `python -m tools.benchmark.description_analyzer --report`

## Comment Text Mining (2026-03-21, 45 videos, 220 comments) (from: comment-analysis-findings.md)

- Channel average: 15.34 comments/1K views
- **Ideological topics generate 2.3x more comments** per view than territorial (27.80 vs 11.94)
- 4 topic requests found in comments (demand signals)
- 42 viewer questions found (FAQ material)
- 2 loyal commenters (3+ videos): @RidiculousObserver (5), @purcitron (4)
- Guatemala/Belize videos dominate comment volume (118 of 220)
- `auth.py` now includes `youtube.force-ssl` scope for real comment fetching

**Tool:** `comment_analysis.py` — `python -m tools.youtube_analytics.comment_analysis --fetch --report`

## Script-to-SRT Deviation (2026-03-21, 20 project pairs) (from: script-srt-deviation-findings.md)

- Average script survival rate: **44%** (56% cut/replaced during filming)
- Ad-lib rate: **32%** of final video content is improvised
- Ad-libs have **+0.102 higher retention** than scripted content (0.351 vs 0.250)
- Most faithful: Brazil (88%). Most divergent: Operation Condor (0%)
- General topics survive best (70%), ideological diverge most (36%)

**How to apply:**
- Script-writer-v2 Rule 21: 1.80x buffer, ad-lib retention data
- Mark more content as EXPENDABLE — survival is only 44%
- Leave more beat gaps for natural ad-libs (+10% retention advantage)
**Tool:** `script_srt_deviation.py` — `python -m tools.youtube_analytics.script_srt_deviation --report`

## Deep Analytics (2026-03-21, 48 videos) (from: deep-analytics-findings.md)

### Geography
- Core: US 39%, UK 13%, Belize 12% (outlier from viral video)
- 36% non-anglophone — content resonates internationally
- International audience correlates with LOWER retention (r=-0.25)
- Territorial topics = most international (60% non-anglophone)

### Search Terms (24 videos, 105 terms)
- "belize" is #1 search driver (72 views, 3.3 min/view)
- 9 title-search mismatches detected
- Highest-value: "belize guatemala dispute" (6.1 min/view)
- Run search term check before publishing

### Retention Curve Shapes
- bump: 40% (mid-video recovery, avg +6.4%)
- other: 36% (highest views 742 avg, best Suggested traffic 26.3%)
- cliff: 21% (sharp early drop, 67.8% subscriber-driven, territorial dominant)

### Velocity
- 48h velocity does NOT predict lifetime views (r=0.163). Evergreen search > launch spikes.
- 38% of videos get delayed algorithm push (day 3-7 spike) — 6.2x more lifetime views
- 48h benchmark: median 17, mean 135. >34 = outperformer
- Don't panic about slow starts.

### CTR by Source (31 videos)
- Weak correlation between Search % and CTR (r=0.142)
- High-CTR videos are MORE subscriber-dependent (+6.4pp)
- Low-confidence findings. Don't optimize differently for Search vs Browse.

### End Screens (43 videos)
- Only 0.2% of traffic. Below typical 2-5% benchmark.
- Low priority but free improvement.

### Tools Built
- `geography_analysis.py`, `search_term_analysis.py`, `comment_analysis.py`, `curve_shape_analysis.py`, `velocity_analysis.py`, `ctr_by_source_analysis.py`, `endscreen_analysis.py`
- All under `tools/youtube_analytics/`, run with `python -m tools.youtube_analytics.<name> --report`
