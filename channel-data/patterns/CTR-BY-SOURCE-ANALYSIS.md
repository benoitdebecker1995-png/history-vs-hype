# CTR by Traffic Source Analysis
**Generated:** 2026-03-21
**Videos with CTR data:** 39
**Videos with traffic data:** 51
**Videos with both:** 31

## Methodology Note

YouTube Analytics does not provide per-source CTR. Impressions are only available at the video level, not broken down by traffic source. This analysis correlates **overall video CTR** (from YouTube Studio, parsed from POST-PUBLISH-ANALYSIS files) with **traffic source view shares** (from YouTube Analytics API) to identify patterns.

The key question: do videos with higher CTR get their views from different sources than low-CTR videos?

## 1. CTR vs Traffic Source Correlation

**High CTR** (>=4.0%): 7 videos, avg 7.57%
**Mid CTR** (3.0-4.0%): 7 videos, avg 3.51%
**Low CTR** (<3.0%): 17 videos, avg 1.93%

| Source | High CTR (>=4.0%) | Mid CTR | Low CTR (<3.0%) | Delta (H-L) |
|--------|--------|--------|--------|--------|
| YouTube Search | 15.1% | 18.4% | 12.0% | +3.1pp |
| Suggested/Related | 27.0% | 13.8% | 32.1% | -5.2pp |
| Subscribers (Home) | 35.7% | 50.2% | 29.4% | +6.4pp |
| External URLs | 2.2% | 6.6% | 1.6% | +0.6pp |
| Notifications | 0.3% | 0.3% | 3.8% | -3.5pp |
| Channel Page | 10.9% | 5.2% | 9.2% | +1.7pp |
| Other | 13.3% | 8.4% | 18.6% | -5.3pp |

**Search % vs CTR correlation:** r=0.142 (weak, n=31)

## 2. Source Mix by Title Pattern

| Title Pattern | n | Avg CTR | Search % | Suggested % | Subscriber % | External % |
|--------|--------|--------|--------|--------|--------|--------|
| declarative | 24 (17 w/CTR) | 3.74% | 12.7% | 25.5% | 35.2% | 7.8% |
| versus | 11 (5 w/CTR) | 4.29% | 15.4% | 18.0% | 40.2% | 4.2% |
| how_why | 5 (5 w/CTR) | 3.31% | 26.4% | 21.4% | 33.8% | 1.7% |
| colon | 4 (2 w/CTR) | 2.05% | 24.4% | 30.7% | 13.5% | 3.7% |
| question | 2 (2 w/CTR) | 2.34% | 19.2% | 12.6% | 47.9% | 1.9% |

## 3. Source Mix by Topic Type

| Topic Type | n | Avg CTR | Search % | Suggested % | Subscriber % | External % |
|--------|--------|--------|--------|--------|--------|--------|
| territorial | 20 (14 w/CTR) | 2.96% | 12.8% | 24.7% | 41.9% | 4.6% |
| ideological | 11 (10 w/CTR) | 3.66% | 16.4% | 19.1% | 39.9% | 2.1% |
| general | 9 (6 w/CTR) | 5.06% | 20.6% | 20.1% | 23.9% | 10.8% |
| colonial | 4 (1 w/CTR) | 1.89% | 20.9% | 23.2% | 19.7% | 6.1% |
| legal | 1 (0 w/CTR) | n/a | n/a | 75.0% | 9.4% | 1.6% |
| factcheck | 1 (0 w/CTR) | n/a | 4.5% | 22.7% | 27.3% | 6.8% |

## 4. Source Mix by CTR Tier

Which traffic sources feed high-CTR videos vs low-CTR videos?

### Per-Video CTR + Source Breakdown

| Video | CTR | Search % | Suggested % | Subscriber % | Title Pattern |
|--------|--------|--------|--------|--------|--------|
| vikinghorde Title1 | 15.91% | 17.9% | 51.3% | 5.1% | declarative |
| JD Vance Claims Christians Found Child Sacrif | 9.49% | 3.4% | 6.4% | 83.3% | declarative |
| Debunking Begins! Why I Started ‘History vs H | 8.40% | 25.0% | n/a | 12.5% | versus |
| Primary Sources Destroy the 'Awesome Crusades | 5.42% | 2.5% | 0.9% | 89.7% | declarative |
| How the KGB Weaponized Palestinian Resistance | 5.31% | 47.3% | 13.4% | 9.9% | how_why |
| Venezuela vs Guyana: The Oil War Over Essequi | 4.31% | 1.4% | 68.7% | 24.9% | versus |
| The Hidden Pattern Behind the Armenia Conflic | 4.14% | 8.3% | 21.1% | 24.8% | declarative |
| Why Trump Walked Back the Armenian Genocide | 3.87% | 51.9% | 15.2% | 17.7% | how_why |
| 5 Big Myths About Israel and Palestine Busted | 3.80% | 1.1% | 39.4% | 43.5% | declarative |
| The Flat Earth Myth Was Invented in 1828. Her | 3.76% | 4.4% | 2.4% | 81.1% | declarative |
| Somaliland's Legal Independence Problem | 3.66% | 3.6% | 5.3% | 54.7% | declarative |
| India vs Pakistan. Britain Sold Kashmir for 7 | 3.20% | 3.1% | 18.8% | 67.9% | versus |
| Russia vs Georgia. The Rehearsal for Ukraine | 3.18% | 60.0% | 5.0% | 12.5% | versus |
| Why TURKEY and GREECE Can't Agree on these is | 3.10% | 4.7% | 10.7% | 73.8% | how_why |
| Putin Says NATO Promised Not to Expand. The D | 2.49% | 23.9% | 34.8% | 10.9% | declarative |
| Did Pagans Actually Copy Christmas? | 2.43% | 3.6% | 16.5% | 67.5% | question |
| The CIA Knew Cyprus Would Be Invaded. They Le | 2.40% | 14.1% | 34.3% | 22.2% | declarative |
| Why Egypt and Sudan Both Reject Bir Tawil | 2.38% | 13.0% | 15.9% | 49.3% | how_why |
| Spain vs Peru. 300 Years of Colonial Lies Exp | 2.35% | 17.4% | 8.7% | 17.4% | versus |
| Why a 1908 Map is Still Killing People: Thail | 2.28% | 29.6% | 22.2% | 14.8% | colon |
| Was Lagertha Real? DNA Says Female Viking War | 2.26% | 34.8% | 8.7% | 28.3% | question |
| Ancient Hatreds" in the Middle East Are a Mod | 2.16% | 3.2% | 28.0% | 34.4% | declarative |
| Morocco's 1,700-Mile Wall (And the Vote That  | 2.16% | 12.4% | 35.2% | 33.3% | declarative |
| Britain Promised the Same Land to Three Diffe | 2.01% | 5.2% | 17.7% | 40.6% | declarative |
| How 3 Coups Ended 60 Years of French Control  | 1.89% | 14.8% | 51.9% | 18.5% | how_why |
| China Claims the Entire South China Sea. A Co | 1.83% | n/a | 64.8% | 16.5% | declarative |
| Mexico's Missing Island: The Map Error That C | 1.83% | n/a | 9.1% | n/a | colon |
| Stalin Purged His Own Army. Then Hitler Invad | 1.55% | 1.7% | 27.5% | 53.3% | declarative |
| The "Dark Ages" Never Happened. Here's the Pr | 1.11% | 0.9% | 45.5% | 39.1% | declarative |
| The 200‑Year‑Old Tariff Myth That Drains Your | 1.01% | 1.0% | 59.0% | 20.0% | declarative |
| The 1922 Treaty Loophole That Ended the USSR | 0.66% | 4.2% | 66.7% | 4.2% | declarative |

## Interpreted Findings

- Search share is similar across CTR tiers (15.1% vs 12.0%). CTR differences are not driven by traffic source.
- High-CTR videos get 5.2pp less Suggested/Related traffic (27.0% vs 32.1%). Algorithm favoring low-CTR videos suggests subscriber base is driving views.
- High-CTR videos are 6.4pp more subscriber-dependent (35.7% vs 29.4%). High CTR may reflect subscriber loyalty, not packaging quality.
- 'how_why' titles have the highest Search traffic share (26.4%). Optimize evergreen topics with this pattern.
- Positive correlation between Search share and CTR (r=0.142, n=31). Videos that get found via Search tend to have better CTR — likely because search-optimized titles match user intent.

## Data Quality Notes

- CTR data from POST-PUBLISH-ANALYSIS files (39 videos). These are single-snapshot values manually entered from YouTube Studio.
- Traffic source data from YouTube Analytics API (51 videos).
- Only 31 videos have both CTR and traffic data for correlation.
- CTR tiers are arbitrary thresholds, not statistically derived clusters.
- Small sample sizes mean correlations should be treated as directional hypotheses, not proven rules.
