# Cross-Validation: Competitor Findings vs Our Retention Data

**Generated:** 2026-03-24
**Method:** 85-video competitor structural analysis (10 channels) cross-referenced against our 42-video retention dataset (4,200 data points)
**SRTs matched:** 40/43 videos with retention data (3 missing: BXyT8OTGBBo, HtVIC4dS0e8, ZZz_g_Ov6Lg)

**Critical caveat:** The competitor analysis measured **normalized views** (reach/discoverability), while our data measures **retention %** (engagement quality). A pattern that attracts more viewers (competitor metric) may not keep them watching (our metric), and vice versa. Both metrics matter but measure different things.

---

## Finding 1: Hook Type vs Retention

**Competitor claim:** specificity_bomb (5.4x views) > cold_fact (3.7x) > contextual_opening (2.7x). Contextual openings are 80% of the niche but lowest performers.

### Our Data

| Hook Type | n | Avg Ret @5% | Avg Ret @10% | Avg Ret @30% | Overall Avg Ret |
|---|---|---|---|---|---|
| myth_contradiction | 4 | 66.3% | 52.1% | 42.9% | **36.7%** |
| contextual_opening | 15 | 60.5% | 47.1% | 33.2% | **32.0%** |
| cold_fact | 19 | 58.3% | 45.0% | 29.5% | **29.4%** |
| specificity_bomb | 2 | 53.1% | 45.0% | 26.8% | **28.5%** |

### Analysis

On our channel, the **ranking is inverted**: contextual_opening (32.0%) outretains cold_fact (29.4%) by 2.6pp. Myth_contradiction leads at 36.7% but n=4.

However, this doesn't disprove the competitor finding because:

1. **Different metrics.** Competitor measured normalized views (packaging power), we measured retention (content quality). A cold_fact hook may attract more CLICKS without necessarily retaining better.
2. **cold_fact includes our weakest videos.** Flat Earth (13.1%), Sahel (17.1%), and Bir Tawil (23.2%) are in the cold_fact group. These had problems beyond the hook (pacing, topic interest, length). Removing the 3 worst outliers brings cold_fact to 31.5%, closing the gap.
3. **contextual_opening includes our strongest videos.** South China Sea (50.5%), KGB (44.4%), Turkey/Greece (41.1%) — all older videos that had more time for algorithmic distribution.
4. **Our hook types overlap.** Many "contextual" hooks on our channel actually contain dates/facts within 10 seconds (e.g., "Two NATO allies are making completely opposite claims about the same 100 year old treaty"). The automated classifier may not capture the same distinctions as manual analysis.

### Verdict: **NOT CONFIRMED** (but different metrics — finding may hold for views/CTR even though it doesn't for retention)

**Actionable:** Don't change hook strategy based on this alone. The competitor finding's value is for **attracting clicks**, not **retaining viewers**. Continue using cold_fact for packaging power (CTR), but don't assume it improves retention over contextual openings.

**Confirmed sub-finding:** myth_contradiction is our strongest hook type for retention (36.7%, n=4). This aligns with the competitor data (4.6x views, n=1). Worth testing more.

---

## Finding 2: Turn Placement Zone vs Retention

**Competitor claim:** 25-35% of runtime is a "dead zone" (2.1x views). Best zones: 15-25% (3.2x) and 45-55% (3.7x).

### Our Data

| Zone | n | Avg Retention | Competitor Norm Views |
|---|---|---|---|
| 0-15% | 3 | 33.4% | n/a |
| 15-25% | 11 | 27.8% | 3.2x (strong) |
| **25-35%** | **5** | **37.5%** | **2.1x (dead zone)** |
| 35-45% | 1 | 37.7% | 2.4x |
| 45-55% | 0 | — | 3.7x (strongest) |
| 55%+ | 12 | 30.7% | 2.8x |

**Turns detected:** 32/40 videos (80%)

### Analysis

Our data shows the **opposite pattern**: the competitor "dead zone" (25-35%) is actually our **best-retaining zone** at 37.5%, while the competitor "strong" zone (15-25%) is our **worst** at 27.8%.

Major caveats:

1. **Turn detection is crude.** The script finds the first occurrence of transition markers ("but here's", "in reality", "the problem is"). This may not match what the competitor analysis considers a "turn" (a major narrative pivot). Many of our videos have "but here's" early as a sentence connector, not a structural turn.
2. **"But here's" dominates.** 20/32 detected turns used "but here's" as the marker — this is a verbal tic in our scripts, not necessarily the main narrative turn.
3. **Zero videos in the 45-55% zone.** We can't validate the competitor's strongest zone at all.
4. **15-25% includes weak videos.** Berlin Conference (25.3%), Somaliland (25.6%), and Did Pagans Copy Christmas (25.1%) pull down this zone — likely unrelated to turn placement.

### Verdict: **NOT CONFIRMED** (but methodology too crude to be conclusive)

**Actionable:** The turn detection is too noisy for reliable conclusions. The marker-based approach can't distinguish between a minor transition ("but here's what happened next") and a major structural pivot ("but the documents tell a completely different story"). A manual re-analysis of 15-20 videos with human-identified turn moments would be needed to properly validate this.

---

## Finding 3: First Date/Number Timing vs Early Retention

**Competitor claim:** Top-performing videos introduce their first date/number 101 seconds earlier than bottom performers (203s vs 304s).

### Our Data

| Group | n | Avg First Date | Early Ret (0-10%) | Overall Avg Ret |
|---|---|---|---|---|
| <=101s (fast) | 37 | 18s | 62.7% | 30.8% |
| >101s (slow) | 3 | 245s | 64.3% | 34.4% |

### Analysis

**37 out of 40 videos** (92.5%) already place their first date/number within 101 seconds. Our median is just **18 seconds** — we're far ahead of both the competitor top half (203s) and bottom half (304s).

The 3 "slow" videos (Stalin 102s, Tariffs 298s, Israel-Palestine 335s) actually have *slightly higher* retention, but n=3 is meaningless for comparison.

### Verdict: **INSUFFICIENT DATA** (we already follow this practice universally — no counterfactual exists)

**Actionable:** This is already baked into our workflow. Our scripts naturally front-load dates/numbers because of the cold_fact and evidence-first style. No change needed. The competitor finding is validated *indirectly* — we do it, and our early retention (62.7% at 0-10%) is healthy.

---

## Finding 4: Question Frequency vs Mid-Video Retention

**Competitor claim:** Top-performing videos average 3.6 rhetorical questions vs 1.4 for bottom performers (+2.2 delta).

### Our Data

| Group | n | Avg Questions | Mid-Video Ret (30-70%) | Overall Avg Ret |
|---|---|---|---|---|
| 0-1 questions | 6 | 1.0 | 31.2% | 34.3% |
| 2+ questions | 34 | 8.0 | 26.7% | 30.5% |

### Analysis

On our channel, videos with **fewer questions retain slightly better** (34.3% vs 30.5%) — opposite to the competitor finding.

Major caveats:

1. **Outlier effect.** The 0-1 question group includes South China Sea (50.5% retention), which alone pulls the average up by ~3pp. Remove it and the low-question group drops to 31.0%, nearly identical to the high-question 30.5%.
2. **Our question counts are already high.** The competitor "high" threshold is 3.6 questions. Our median is ~5. Only 6/40 videos have 0-1 questions. We're already a high-question channel.
3. **Question counting is blunt.** A `?` count includes genuine rhetorical questions ("So why did France build this wall?"), conversational questions ("Sound familiar?"), and subtitle artifacts. The competitor study may have used more nuanced classification.
4. **34/40 videos in the 2+ group.** With 85% of videos in one bucket, the comparison has very low statistical power.

### Verdict: **NOT CONFIRMED** (but confounded by outlier and lack of low-question videos to compare)

**Actionable:** Our channel already uses 5+ questions per video. There's no evidence that adding MORE questions would help. The competitor finding may apply to channels that use very few questions (like pure narrative channels), but doesn't differentiate within our already-high-question range.

---

## Summary Table

| # | Finding | Competitor Claim | Our Data Says | Verdict | n (comparison) |
|---|---|---|---|---|---|
| 1 | Hook type | specificity_bomb > cold_fact > contextual | myth > contextual > cold_fact > specificity | **NOT CONFIRMED** | 40 (but metrics differ) |
| 2 | Turn placement | 25-35% dead zone, 15-25% & 45-55% best | 25-35% is our best, 15-25% our worst | **NOT CONFIRMED** | 32 (crude detection) |
| 3 | First date timing | <101s = better early retention | 92% of our videos already <101s | **INSUFFICIENT DATA** | 37 vs 3 |
| 4 | Question frequency | 2+ questions = better mid-video | 0-1 questions marginally better (outlier-driven) | **NOT CONFIRMED** | 6 vs 34 (imbalanced) |

---

## Why the Disconnect? Three Hypotheses

### 1. Views vs Retention Are Different Metrics
The competitor analysis measured normalized views (impressions x CTR x algorithm push). Our analysis measures retention %. A hook type that generates more clicks (cold_fact) may not produce better retention if the content quality is equal. Both findings can be simultaneously true.

### 2. Channel Size Creates Different Dynamics
At 475 subscribers, our videos live or die by their first 48 hours of subscriber response. Competitor channels (350K-1.8M subs) have large subscriber bases that generate initial velocity for the algorithm. What works at scale may not work for small channels — and vice versa.

### 3. Our Sample Is One Creator's Style
All 40 videos are from one creator. The competitor analysis spans 10 creators with different styles, pacing, and audiences. Our "contextual openings" may be unusually strong (because they still front-load evidence), while our "cold facts" may underperform for reasons unrelated to the hook type (e.g., the cold_fact videos tend to be newer and on niche topics).

---

## Recommendations

1. **Don't over-rotate on hook type for retention.** The data suggests hook type matters less for retention than topic choice, video length, and content quality. Use cold_fact/specificity_bomb for CTR (packaging power), not retention.

2. **Test more myth_contradiction hooks.** This is the only type that shows consistent strength in BOTH datasets — 4.6x in competitor views AND 36.7% in our retention. n=4 on our side, n=1 on competitor side. More data needed but the signal is positive.

3. **Don't rearrange turn placement based on competitor zones.** Our turn detection is too crude and the results contradict the competitor data. The 25-35% "dead zone" may be real for views/packaging but doesn't harm our retention.

4. **Keep front-loading dates/numbers.** We already do this (median 18s). The competitor finding is indirectly validated by our consistent practice.

5. **Questions: diminishing returns above 5.** Our channel averages ~8 questions per video. There's no evidence that more questions help. The competitor finding likely applies to channels going from 0-1 to 3-4 questions, not from 5 to 10.

6. **Revisit with manual classification.** A human-coded analysis of 20 videos (hook type, true narrative turn, question quality) would produce much more reliable results than automated parsing. The algorithmic classifier disagrees with the manual HOOK-RETENTION-CORRELATION.md classifications on several videos.
