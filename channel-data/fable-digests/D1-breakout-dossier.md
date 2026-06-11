# D1 — Breakout Forensics Dossier

**Build date:** 2026-06-11  
**Data vintage:** analytics.db fetched through 2026-06-10; POST-PUBLISH-ANALYSIS files current as of 2026-06-10; title_scorer v-current  
**Videos in DB:** 57 (includes Shorts and one legacy 2014 video)  
**Long-form videos with CTR data:** 22 (from POST-PUBLISH files; all dated to 2026-02-23 snapshot)  
**Videos with POST-PUBLISH files:** 27 (47% of DB); no POST-PUBLISH files exist for 30 videos including top 2 (#1 Guatemala, #2 Guatemala ICJ)

> **Note on impressions/CTR in DB:** `impressions` and `ctr_percent` columns are NULL for all 57 rows. All CTR and impression figures in this dossier come from POST-PUBLISH-ANALYSIS markdown files.

---

## 1. MASTER TABLE

Sorted by views descending. Duration in minutes (rounded). Top traffic source shown as `TYPE (N views, X%)` where N = raw views from that source and X% = share of all tracked traffic for that video. Scorer score uses the title as published; REJECTED = hard-reject flag triggered (colon, year, or "The X That Y" pattern).

| Title | Published | Dur (min) | Views | Impressions | CTR% | Avg Watch% | Top Traffic Source | Subs Gained | Topic | Scorer | Scorer Flags |
|-------|-----------|-----------|-------|-------------|------|------------|-------------------|-------------|-------|--------|-------------|
| The Country That Might Disappear: Guatemala vs Belize | 2025-10-27 | 10.95 | 29,713 | n/a | n/a | 35.3% | SUBSCRIBER (23,741 / 80%) | 147 | territorial | REJECTED (50) | HARD REJECT: Colon in title |
| Guatemala vs Belize Dispute: What 3 ICJ Cases Show | 2025-12-04 | 11.13 | 5,355 | n/a | n/a | 38.7% | SUBSCRIBER (3,671 / 69%) | 51 | territorial | 75 / B | — |
| Venezuela vs Guyana: The Oil War Over Essequibo | 2025-10-19 | 10.55 | 1,966 | 36,129 | 4.31% | 34.6% | RELATED_VIDEO (1,348 / 69%) | 19 | territorial | REJECTED (80) | HARD REJECT: Colon in title |
| JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence. | 2025-11-04 | 6.27 | 1,147 | n/a | n/a | 26.5% | SUBSCRIBER (941 / 82%) | 16 | territorial | 75 / B | — |
| Turkey Claims 152 Greek Islands. Here's Why. | 2025-08-27 | 9.13 | 963 | n/a | n/a | 39.1% | SUBSCRIBER (682 / 71%) | 14 | territorial | 100 / A | — |
| Two Countries Split a Continent They Had Never Mapped | 2026-03-18 | 12.82 | 793 | n/a | n/a | 16.9% | SUBSCRIBER (745 / 94%) | 5 | territorial | 70 / B | — |
| Primary Sources Destroy the 'Awesome Crusades' Narrative | 2025-11-27 | 10.58 | 689 | n/a | n/a | 26.9% | SUBSCRIBER (603 / 88%) | 7 | ideological | 80 / B | — |
| 5 Big Myths About Israel and Palestine Busted! | 2025-07-29 | 11.97 | 640 | 11,331 | 3.80% | 31.2% | SUBSCRIBER (273 / 43%) | 11 | ideological | 95 / A | — |
| How the KGB Weaponized Palestinian Resistance | 2025-09-25 | 10.10 | 457 | 3,176 | 5.41% | 40.5% | YT_SEARCH (270 / 59%) | 24 | ideological | 55 / D | — |
| The Berlin Conference: How Colonial Borders Still Fuel Conflict in Africa | 2026-03-12 | 9.12 | 440 | n/a | n/a | 24.7% | SUBSCRIBER (395 / 90%) | 7 | territorial | REJECTED (0) | HARD REJECT: Colon; Too long (73 chars) |
| Somaliland's Legal Independence Problem | 2026-01-01 | 11.22 | 405 | n/a | n/a | 24.0% | SUBSCRIBER (216 / 53%) | 5 | territorial | 55 / C | — |
| China vs Taiwan. 4 Historical Claims Exposed by Scholars | 2025-08-23 | 9.58 | 257 | n/a | n/a | 27.8% | SUBSCRIBER (195 / 76%) | 2 | territorial | 100 / A | — |
| India vs Pakistan. Britain Sold Kashmir for 7.5 Million Rupees | 2025-08-14 | 10.48 | 228 | 5,543 | 3.20% | 19.6% | SUBSCRIBER (153 / 67%) | 2 | territorial | 100 / A | — |
| Why The Sol Invictus Story Is Completely Wrong | 2025-12-25 | 14.65 | 214 | n/a | n/a | 23.1% | SUBSCRIBER (131 / 61%) | 6 | ideological | 45 / D | — |
| The Flat Earth Myth Was Invented in 1828. Here's Who Did It. | 2026-01-15 | 17.83 | 213 | n/a | n/a | 12.8% | SUBSCRIBER (167 / 78%) | 2 | ideological | 70 / B | — |
| Why Trump Walked Back the Armenian Genocide | 2025-09-01 | 12.55 | 193 | n/a | n/a | 24.8% | YT_SEARCH (114 / 59%) | 4 | general | 75 / B | — |
| Fact-Checking Nick Fuentes: Why His Claims Are Dangerous | 2025-11-20 | 10.42 | 184 | n/a | n/a | 25.2% | YT_SEARCH (67 / 36%) | 0 | territorial | REJECTED (0) | HARD REJECT: Colon; low demand (-10) |
| The Piri Reis Map Cites Columbus. Hancock Calls It 12,000 Years Old | 2026-06-04 | 10.47 | 145 | n/a | n/a | 30.3% | SUBSCRIBER (107 / 74%) | 1 | territorial | 80 / A | — |
| London's Stock Exchange Funded a Genocide | 2025-09-12 | 9.32 | 137 | n/a | n/a | 30.1% | YT_SEARCH (53 / 39%) | 5 | colonial | 65 / B | — |
| 7 Million Landmines Guard a Wall Nobody Talks About | 2025-10-16 | 11.12 | 128 | 3,073 | 2.16% | 25.5% | RELATED_VIDEO (37 / 29%) | 2 | territorial | 75 / B | — |
| Stalin Purged His Own Army. Then Hitler Invaded | 2025-07-19 | 10.03 | 122 | 5,538 | 1.55% | 36.0% | SUBSCRIBER (64 / 52%) | 5 | ideological | 65 / C | — |
| The 1947 Partition Map Didn't Follow Religion | 2026-03-29 | 10.65 | 119 | n/a | n/a | 20.2% | RELATED_VIDEO (47 / 39%) | 0 | territorial | REJECTED (15) | HARD REJECT: Year in title |
| Medieval Europe's Hidden Literacy Boom \| What Historians Got Wrong | 2025-12-18 | 10.75 | 115 | n/a | n/a | 30.2% | RELATED_VIDEO (50 / 43%) | 2 | general | 70 / B | — |
| The Hidden Pattern Behind the Armenia Conflict | 2025-09-08 | 14.03 | 115 | 1,347 | 4.11% | 29.8% | SUBSCRIBER (27 / 23%) | 0 | general | 85 / A | — |
| The Historical Pattern Nobody Wants to Admit About Trade Wars | 2025-08-07 | 11.53 | 106 | n/a | n/a | 28.1% | RELATED_VIDEO (62 / 58%) | 2 | general | 70 / B | — |
| Britain Promised the Same Land to Three Different Groups | 2025-11-13 | 11.10 | 102 | 3,204 | 2.01% | 35.0% | SUBSCRIBER (39 / 38%) | 3 | general | 65 / C | — |
| Cyprus Is Still Divided. Both Sides Blame the Other | 2025-09-21 | 9.27 | 102 | 2,758 | 2.40% | 33.5% | RELATED_VIDEO (34 / 33%) | 2 | territorial | 90 / A | — |
| "Ancient Hatreds" in the Middle East Are a Modern Invention | 2025-07-24 | 9.47 | 95 | 2,970 | 2.16% | 29.0% | SUBSCRIBER (32 / 34%) | 1 | general | 65 / C | — |
| China Claims the Entire South China Sea. A Court Said No | 2025-08-20 | 4.70 | 91 | 3,007 | 1.83% | 49.6% | RELATED_VIDEO (59 / 65%) | 2 | territorial | 90 / A | — |
| 1,000 Years of Ukraine: The History Putin Erased | 2025-07-10 | 9.92 | 89 | n/a | n/a | 24.5% | YT_CHANNEL (26 / 29%) | 4 | territorial | REJECTED (0) | HARD REJECT: Colon in title |
| Vichy France: The Anti-Jewish Law Nobody Translated | 2026-03-05 | 10.60 | 82 | n/a | n/a | 29.5% | RELATED_VIDEO (48 / 59%) | 3 | legal | REJECTED (0) | HARD REJECT: Colon in title |
| The Myths of Thermopylae: Fake Quotes & Missing Soldiers | 2026-04-11 | 11.17 | 80 | n/a | n/a | 25.8% | SUBSCRIBER (62 / 78%) | 0 | ideological | REJECTED (0) | HARD REJECT: Colon; low demand (-10) |
| The Hijab Wasn't Modesty. It Was a Property Law | 2026-05-20 | 11.48 | 79 | n/a | n/a | 28.6% | RELATED_VIDEO (47 / 59%) | 4 | general | 70 / B | — |
| Yes Slavery Existed In Africa. Then Europe Took Over | 2026-05-28 | 11.12 | 76 | n/a | n/a | 25.6% | RELATED_VIDEO (52 / 68%) | 2 | general | 70 / B | — |
| Why Egypt and Sudan Both Reject Bir Tawil | 2025-12-11 | 8.90 | 73 | n/a | n/a | 22.0% | SUBSCRIBER (34 / 47%) | 0 | territorial | 55 / C | — |
| Iran vs Its Own Democracy. 120 Years of Failed Revolutions | 2026-02-05 | 13.73 | 72 | n/a | n/a | 24.7% | SUBSCRIBER (27 / 38%) | 0 | general | 80 / B | — |
| "Putin Copied Serbia's Playbook. Here's the Original | 2025-09-18 | 12.18 | 67 | n/a | n/a | 30.7% | YT_SEARCH (35 / 52%) | 1 | ideological | 80 / B | — |
| Was Lagertha Real? DNA Says Female Viking Warriors Existed | 2025-10-24 | 10.10 | 55 | n/a | n/a | 28.1% | YT_SEARCH (24 / 44%) | 1 | general | 70 / B | — |
| 34,000 People Can't Decide Their Future. One Clause Trapped Them | 2026-02-26 | 14.08 | 54 | n/a | n/a | 28.1% | YT_SEARCH (22 / 41%) | 0 | legal | 70 / B | — |
| Putin Says NATO Promised Not to Expand. The Documents Disagree. | 2025-09-10 | 5.70 | 51 | 1,214 | 2.48% | 44.5% | RELATED_VIDEO (16 / 31%) | 3 | ideological | 75 / B | — |
| The CIA Document That Proved Operation Condor | 2026-02-12 | 4.78 | 50 | n/a | n/a | 29.6% | SUBSCRIBER (13 / 27%) | 0 | colonial | REJECTED (0) | HARD REJECT: The X That Y pattern |
| The Colonial Structures Killing Peruvian Protesters in 2023 | 2025-10-10 | 12.57 | 50 | n/a | n/a | 33.8% | SHORTS_CONTENT_LINKS (15 / 30%) | 1 | colonial | REJECTED (15) | HARD REJECT: Year in title |
| JD Vance vs History: Who Invented Human Rights? | 2025-11-08 | 11.42 | 49 | n/a | n/a | 35.7% | YT_CHANNEL (15 / 31%) | 0 | factcheck | 80 / B | — |
| Honduras Called These Islands British Territory. Then Claimed Them | 2026-03-30 | 10.88 | 47 | n/a | n/a | 41.5% | YT_SEARCH (16 / 34%) | 0 | territorial | 80 / A | — |
| Debunking Begins! Why I Started 'History vs Hype' | 2025-06-27 | 7.97 | 43 | n/a | n/a | 26.1% | YT_CHANNEL (14 / 33%) | 2 | ideological | 80 / B | — |
| Iran vs the CIA. Two Coups the West Wants You to Forget | 2026-01-27 | 20.27 | 40 | n/a | n/a | 19.7% | YT_SEARCH (14 / 35%) | 1 | colonial | 90 / A | — |
| Putin Invaded Georgia Before Ukraine. Nobody Stopped Him | 2025-07-16 | 6.00 | 40 | 892 | 3.22% | 22.5% | YT_SEARCH (24 / 60%) | 0 | territorial | 85 / A | — |
| vikinghorde Title1 | 2014-05-06 | 28.72 | 39 | 44 | 15.91% | 18.8% | RELATED_VIDEO (20 / 51%) | 0 | general | 50 / D | — |
| 3 Men Signed 1 Document. The Soviet Union Ceased to Exist | 2026-01-29 | 4.85 | 38 | n/a | n/a | 38.6% | RELATED_VIDEO (16 / 42%) | 0 | general | 80 / B | — |
| Treaty of Tripoli: The Most-Cited Line Isn't in the Arabic Text | 2026-04-30 | 6.63 | 36 | n/a | n/a | 45.1% | YT_SEARCH (16 / 44%) | 1 | territorial | REJECTED (0) | HARD REJECT: Colon in title |
| The Spanish Inquisition Documented Its Torture Methods. Most People Skip the Documents | 2026-05-14 | 7.82 | 36 | n/a | n/a | 32.1% | RELATED_VIDEO (19 / 53%) | 0 | general | 70 / B | — |
| 38 Dead Over 4.6 Square Kilometers. Both Sides Blame One Map | 2025-10-03 | 7.37 | 32 | 668 | 2.34% | 24.0% | YT_SEARCH (12 / 38%) | 0 | territorial | 80 / A | — |
| How 3 Coups Ended 60 Years of French Control in Africa | 2025-10-01 | 13.53 | 30 | 1,068 | 1.88% | 15.7% | RELATED_VIDEO (14 / 47%) | 1 | colonial | 65 / B | — |
| Britain Expelled 2,000 Islanders. The Memo Proves It | 2026-01-08 | 10.62 | 29 | n/a | n/a | 30.4% | YT_SEARCH (13 / 45%) | 0 | general | 70 / B | — |
| The Lenape Never Sold Manhattan. Every Piece Was Forged | 2026-05-08 | 10.02 | 18 | n/a | n/a | 27.0% | RELATED_VIDEO (10 / 56%) | 0 | general | 75 / B | — |
| Nigeria vs Cameroon. The Court Chose Paper Over People | 2026-04-16 | 11.38 | 17 | n/a | n/a | 26.8% | YT_OTHER_PAGE (6 / 35%) | 0 | legal | 70 / B | — |
| Mexico's Missing Island: The Map Error That Cost $22 Billion | 2026-02-19 | 8.25 | 13 | n/a | n/a | 32.4% | SHORTS_CONTENT_LINKS (7 / 54%) | 0 | territorial | REJECTED (0) | HARD REJECT: Colon in title |

---

## 2. BREAKOUT PROFILES

Videos with >1,000 views. Note: #1 and #2 have no POST-PUBLISH files; all discovery data comes from traffic_sources and search_terms tables.

---

### VIDEO B1 — The Country That Might Disappear: Guatemala vs Belize
**Video ID:** Y21EjQ0v9W4 | **Published:** 2025-10-27 | **Duration:** 10m 57s  
**Views:** 29,713 | **Impressions:** n/a | **CTR:** n/a | **Avg Watch%:** 35.3% | **Subs Gained:** 147  
**Topic:** territorial | **Scorer:** REJECTED (50) — hard reject: colon in title

**Discovery (traffic sources):**

| Source | Views | % of tracked |
|--------|-------|--------------|
| SUBSCRIBER | 23,741 | 80% |
| RELATED_VIDEO | 2,657 | 9% |
| EXT_URL | 1,232 | 4% |
| YT_SEARCH | 1,082 | 4% |
| NO_LINK_OTHER | 603 | 2% |
| YT_OTHER_PAGE | 264 | 1% |
| PLAYLIST | 51 | <1% |
| END_SCREEN | 45 | <1% |
| YT_CHANNEL | 32 | <1% |

**Diagnosis:** No POST-PUBLISH file. Traffic dominated by SUBSCRIBER (80%) — this video benefited from the channel's subscriber base at a time when another video (XbGl1Kcspt4, the related ICJ follow-up) was receiving algorithmic push. Chicken-and-egg likely: the follow-up's subscriber spike retroactively boosted this video in recommendations.

**Search terms driving views:**

| Term | Views |
|------|-------|
| belize | 74 |
| guatemala history | 23 |
| history of belize | 20 |
| belize guatemala dispute | 13 |
| history of guatemala | 13 |
| belize country | 11 |
| belize history | 9 |
| belize vs guatemala | 4 |
| guatemala | 4 |
| guatemala vs belize | 4 |

**Retention (sampled from curve):**

| Position | Audience Ratio |
|----------|---------------|
| 25% | 39.7% |
| 50% | 32.0% |
| 75% | 28.2% |
| 100% | 24.6% |

Retention shape: standard steep drop in first 5%, then gradual linear decay — no catastrophic cliff, strong floor at 24.6% completion.

---

### VIDEO B2 — Guatemala vs Belize Dispute: What 3 ICJ Cases Show
**Video ID:** XbGl1Kcspt4 | **Published:** 2025-12-04 | **Duration:** 11m 8s  
**Views:** 5,355 | **Impressions:** n/a | **CTR:** n/a | **Avg Watch%:** 38.7% | **Subs Gained:** 51  
**Topic:** territorial | **Scorer:** 75 / B

**Discovery (traffic sources):**

| Source | Views | % of tracked |
|--------|-------|--------------|
| SUBSCRIBER | 3,671 | 69% |
| RELATED_VIDEO | 869 | 16% |
| EXT_URL | 308 | 6% |
| YT_SEARCH | 233 | 4% |
| NO_LINK_OTHER | 110 | 2% |
| YT_OTHER_PAGE | 51 | 1% |
| END_SCREEN | 38 | <1% |
| YT_CHANNEL | 34 | <1% |
| NOTIFICATION | 29 | <1% |

**Diagnosis:** No POST-PUBLISH file. Strong subscriber pull (69%) combined with meaningful related-video spread (16%) and EXT_URL referral (6%) — possibly a Reddit or forum link. Follow-up to B1; benefited from audience already primed on the topic.

**Search terms driving views:**

| Term | Views |
|------|-------|
| belize | 9 |
| guatemala | 6 |
| icj belize and guatemala | 6 |
| guatemala city | 2 |
| belize guatemala dispute | 1 |
| belize real estate | 1 |

**Retention (sampled):**

| Position | Audience Ratio |
|----------|---------------|
| 25% | 44.4% |
| 50% | 34.3% |
| 75% | 31.1% |
| 100% | 28.3% |

Strongest completion rate of any video on the channel (28.3% at 100%). Elevated 25%-mark retention (44.4%) vs channel pattern.

---

### VIDEO B3 — Venezuela vs Guyana: The Oil War Over Essequibo
**Video ID:** oDK52GwjTIo | **Published:** 2025-10-19 | **Duration:** 10m 33s  
**Views:** 1,966 | **Impressions:** 36,129 | **CTR:** 4.31% | **Avg Watch%:** 34.6% | **Subs Gained:** 19  
**Topic:** territorial | **Scorer:** REJECTED (80) — hard reject: colon in title

**Discovery:** POST-PUBLISH diagnosis = "Discovery performing at or above benchmarks." RELATED_VIDEO was top source (1,348 / 69%) — this video broke out via algorithmic recommendation, not subscribers or search. EXT_URL also meaningful (19 views / 1%). Likely surfaced alongside Guatemala content given the territorial Latin America overlap.

**Traffic sources:**

| Source | Views | % of tracked |
|--------|-------|--------------|
| RELATED_VIDEO | 1,348 | 69% |
| SUBSCRIBER | 489 | 25% |
| NO_LINK_OTHER | 34 | 2% |
| YT_SEARCH | 28 | 1% |
| YT_OTHER_PAGE | 22 | 1% |
| YT_CHANNEL | 20 | 1% |

**Search terms driving views:**

| Term | Views |
|------|-------|
| documentaries | 2 |
| guyana venezuela | 2 |
| you did not break me | 2 |

Note: Very low search-term data — most discovery via recommendations not search.

**Retention (sampled):**

| Position | Audience Ratio |
|----------|---------------|
| 25% | 42.5% |
| 50% | 31.1% |
| 75% | 24.2% |
| 100% | 20.4% |

---

### VIDEO B4 — JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence.
**Video ID:** LO_fUeX9IEQ | **Published:** 2025-11-04 | **Duration:** 6m 16s  
**Views:** 1,147 | **Impressions:** n/a | **CTR:** n/a | **Avg Watch%:** 26.5% | **Subs Gained:** 16  
**Topic:** territorial | **Scorer:** 75 / B

**Discovery:** No POST-PUBLISH file. SUBSCRIBER dominant (941 / 82%). This was published one week after B1 (Guatemala); suggests the subscriber surge from B1 was still feeding the channel's notification reach. Short format (6m 16s) relative to channel norm.

**Traffic sources:**

| Source | Views | % of tracked |
|--------|-------|--------------|
| SUBSCRIBER | 941 | 82% |
| RELATED_VIDEO | 72 | 6% |
| YT_SEARCH | 44 | 4% |
| EXT_URL | 23 | 2% |
| NO_LINK_OTHER | 21 | 2% |
| YT_CHANNEL | 20 | 2% |
| YT_OTHER_PAGE | 13 | 1% |
| SHORTS_CONTENT_LINKS | 9 | 1% |

**Search terms driving views:**

| Term | Views |
|------|-------|
| jd vance child sacrifice | 3 |
| jd vance children | 1 |

**Retention (sampled):**

| Position | Audience Ratio |
|----------|---------------|
| 25% | 31.0% |
| 50% | 22.3% |
| 75% | 17.1% |
| 100% | 11.7% |

Retention weaker than B1/B2/B3 despite high views — reflects subscriber delivery + early drop-off, not sustained engagement.

---

## 3. STALL PATTERN SAMPLE

The 10 lowest-view videos (long-form only; excludes Shorts). Note: these are all recent uploads (2026), suggesting the channel's ability to surface new videos organically has weakened significantly.

---

### STALL S1 — Mexico's Missing Island: The Map Error That Cost $22 Billion
**Video ID:** P6yalauLDic | **Views:** 13 | **Published:** 2026-02-19 | **Duration:** 8m 15s  
**Avg Watch%:** 32.4% | **Subs Gained:** 0 | **CTR:** n/a | **Impressions:** n/a  
**Scorer:** REJECTED (0) — hard reject: colon in title  
**Top Source:** SHORTS_CONTENT_LINKS (7 / 54%)  
**Retention:** 25%=0.333, 50%=0.250, 75%=0.333, 100%=0.250  
**Discovery:** No POST-PUBLISH file. Traffic almost entirely from Shorts links — no organic search, no subscriber reach. Retention numbers erratic (n too small to trust).

---

### STALL S2 — Nigeria vs Cameroon. The Court Chose Paper Over People
**Video ID:** MXvTuHXSf3o | **Views:** 17 | **Published:** 2026-04-16 | **Duration:** 11m 23s  
**Avg Watch%:** 26.8% | **Subs Gained:** 0 | **CTR:** n/a | **Impressions:** n/a  
**Scorer:** 70 / B  
**Top Source:** YT_OTHER_PAGE (6 / 35%)  
**Retention:** 25%=0.267, 50%=0.267, 75%=0.467, 100%=0.200  
**Discovery:** No POST-PUBLISH file. Retention curve anomalous (75% higher than 50% — small n artifact). No search traction, no subscriber pull.

---

### STALL S3 — The Lenape Never Sold Manhattan. Every Piece Was Forged
**Video ID:** mg6ujk6rDVE | **Views:** 18 | **Published:** 2026-05-08 | **Duration:** 10m 1s  
**Avg Watch%:** 27.0% | **Subs Gained:** 0 | **CTR:** n/a | **Impressions:** n/a  
**Scorer:** 75 / B  
**Top Source:** RELATED_VIDEO (10 / 56%)  
**Retention:** 25%=0.389, 50%=0.222, 75%=0.222, 100%=0.167  
**Discovery:** No POST-PUBLISH file. RELATED_VIDEO = 56% but absolute count is 10 — essentially noise. Scorer rated it B but the title has no keyword hook that could pull search traffic.

---

### STALL S4 — The Colonial Structures Killing Peruvian Protesters in 2023
**Video ID:** 6GybGd_q25w | **Views:** 50 | **Published:** 2025-10-10 | **Duration:** 12m 34s  
**Avg Watch%:** 33.8% | **Subs Gained:** 1 | **CTR:** n/a | **Impressions:** n/a  
**Scorer:** REJECTED (15) — hard reject: year in title  
**Top Source:** SHORTS_CONTENT_LINKS (15 / 30%)  
**Retention:** 25%=0.367, 50%=0.347, 75%=0.306, 100%=0.184  
**Discovery:** No POST-PUBLISH file. "2023" in title = hard-reject year penalty. Good retention profile but no discovery mechanism.

---

### STALL S5 — The CIA Document That Proved Operation Condor
**Video ID:** Q5Pfv_dPubU | **Views:** 50 | **Published:** 2026-02-12 | **Duration:** 4m 47s  
**Avg Watch%:** 29.6% | **Subs Gained:** 0 | **CTR:** n/a | **Impressions:** n/a  
**Scorer:** REJECTED (0) — hard reject: "The X That Y" pattern  
**Top Source:** SUBSCRIBER (13 / 27%)  
**Retention:** 25%=0.354, 50%=0.312, 75%=0.229, 100%=0.188  
**Discovery:** No POST-PUBLISH file. Short format (4m 47s). Nearly equal split across subscriber, search, and related — no channel pulling hard in any direction. Low retention floor despite short duration.

---

### STALL S6 — How 3 Coups Ended 60 Years of French Control in Africa
**Video ID:** jLZngVFKWVg | **Views:** 30 | **Published:** 2025-10-01 | **Duration:** 13m 32s  
**Avg Watch%:** 15.7% | **Subs Gained:** 1 | **CTR:** 1.88% | **Impressions:** 1,068  
**Scorer:** 65 / B  
**Top Source:** RELATED_VIDEO (14 / 47%)  
**Retention:** 25%=0.133, 50%=0.100, 75%=0.067, 100%=0.033  
**Discovery:** POST-PUBLISH diagnosis = LOW_IMPRESSIONS (HIGH severity). Worst retention curve on channel — 15.7% avg, 3.3% completion. Title scores B but "How 3 Coups" is a weak opener pattern vs declarative alternatives.

---

### STALL S7 — Britain Expelled 2,000 Islanders. The Memo Proves It
**Video ID:** ZZz_g_Ov6Lg | **Views:** 29 | **Published:** 2026-01-08 | **Duration:** 10m 37s  
**Avg Watch%:** 30.4% | **Subs Gained:** 0 | **CTR:** n/a | **Impressions:** n/a  
**Scorer:** 70 / B  
**Top Source:** YT_SEARCH (13 / 45%)  
**Retention:** 25%=0.310, 50%=0.241, 75%=0.241, 100%=0.241  
**Discovery:** No POST-PUBLISH file. Search-led (45%) but views still minimal — low search volume on Chagos topic. Search terms: "british indian ocean territory," "chagos," "chagos deal," "chagos islands," "diego garcia" (all 1 view each). Flat retention from 50%–100% (0.241) = unusual; viewers who make it past the midpoint don't leave — completion floor is surprisingly high.

---

### STALL S8 — The Lenape Never Sold Manhattan (already listed as S3 above)

### STALL S8 — 38 Dead Over 4.6 Square Kilometers. Both Sides Blame One Map
**Video ID:** xODFE2Pyubo | **Views:** 32 | **Published:** 2025-10-03 | **Duration:** 7m 22s  
**Avg Watch%:** 24.0% | **Subs Gained:** 0 | **CTR:** 2.34% | **Impressions:** 668  
**Scorer:** 80 / A  
**Top Source:** YT_SEARCH (12 / 38%)  
**Retention:** 25%=0.281, 50%=0.344, 75%=0.156, 100%=0.156  
**Discovery:** POST-PUBLISH diagnosis = LOW_IMPRESSIONS (MEDIUM severity). Notable mismatch: scorer A, 0 subs, 32 views. CTR decent (2.34%) but impressions catastrophically low (668). YouTube simply did not surface this video. Retention curve anomalous — 50% higher than 25% (likely small-n artifact or re-watch spike at midpoint).

---

### STALL S9 — Putin Says NATO Promised Not to Expand. The Documents Disagree.
**Video ID:** 499YLd1BHZ4 | **Views:** 51 | **Published:** 2025-09-10 | **Duration:** 5m 42s  
**Avg Watch%:** 44.5% | **Subs Gained:** 3 | **CTR:** 2.48% | **Impressions:** 1,214  
**Scorer:** 75 / B  
**Top Source:** RELATED_VIDEO (16 / 31%)  
**Retention:** 25%=0.529, 50%=0.412, 75%=0.392, 100%=0.216  
**Discovery:** POST-PUBLISH diagnosis = LOW_IMPRESSIONS (HIGH severity). Strongest retention profile outside the top breakouts — 44.5% avg, 21.6% completion — but died on discovery. Only 1,214 impressions ever. Good content, invisible distribution. Search terms: "ukraine war" (2), "sweden nato" (1) — misaligned with actual content.

---

### STALL S10 — The Myths of Thermopylae: Fake Quotes & Missing Soldiers
**Video ID:** yetYD9_VcmM | **Views:** 80 | **Published:** 2026-04-11 | **Duration:** 11m 10s  
**Avg Watch%:** 25.8% | **Subs Gained:** 0 | **CTR:** n/a | **Impressions:** n/a  
**Scorer:** REJECTED (0) — hard reject: colon in title; low demand penalty  
**Top Source:** SUBSCRIBER (62 / 78%)  
**Retention:** 25%=0.317, 50%=0.253, 75%=0.203, 100%=0.165  
**Discovery:** No POST-PUBLISH file. High subscriber share (78%) but low absolute count — subscriber pool was small when this published. Colon in title, low-demand topic flag.

---

## 4. PREDICTED-VS-ACTUAL

CTR data available for 22 videos (from POST-PUBLISH files). Views used for "actual result." Mispredictions flagged where score vs outcome diverges significantly.

| Video ID | Title (truncated) | Scorer Score | Scorer Grade | CTR% | Views | Misprediction Flag |
|----------|-------------------|-------------|-------------|------|-------|-------------------|
| Y21EjQ0v9W4 | The Country That Might Disappear... | REJECTED (50) | REJECTED | n/a | 29,713 | **HIGH-SCORE/HIGH-RESULT + SCORER WRONG WAY** — biggest video on channel; scorer rejected it |
| XbGl1Kcspt4 | Guatemala vs Belize Dispute... | 75 / B | B | n/a | 5,355 | Normal |
| oDK52GwjTIo | Venezuela vs Guyana: The Oil War... | REJECTED (80) | REJECTED | 4.31% | 1,966 | **SCORER WRONG WAY** — rejected title, 4.31% CTR, 1,966 views |
| LO_fUeX9IEQ | JD Vance Claims Christians... | 75 / B | B | n/a | 1,147 | Normal |
| _N_08zn95FY | Turkey Claims 152 Greek Islands... | 100 / A | A | n/a | 963 | Normal (best scored, good result) |
| WgE2FLsDhfk | Two Countries Split a Continent... | 70 / B | B | n/a | 793 | — |
| VyPv2n4mii8 | Primary Sources Destroy the Crusades... | 80 / B | B | n/a | 689 | — |
| 7fpBz6uo504 | 5 Big Myths About Israel and Palestine | 95 / A | A | 3.80% | 640 | Normal — high score, decent result |
| UH2PddfaaR8 | How the KGB Weaponized... | 55 / D | D | 5.41% | 457 | **LOW SCORE / HIGH CTR** — scorer D, actual CTR 5.41% (highest on channel with CTR data); views limited by impressions not CTR |
| lFGs5NHMxMw | The Berlin Conference: How Colonial... | REJECTED (0) | REJECTED | n/a | 440 | **SCORER WRONG WAY** — rejected, still 440 views |
| GuL9PtXEjN0 | Somaliland's Legal Independence Problem | 55 / C | C | n/a | 405 | — |
| LCze9B2xpOI | China vs Taiwan. 4 Historical Claims... | 100 / A | A | n/a | 257 | **HIGH SCORE / LOW RESULT** — perfect score, only 257 views |
| lPilDVSAeEM | India vs Pakistan. Britain Sold Kashmir... | 100 / A | A | 3.20% | 228 | **HIGH SCORE / LOW RESULT** — perfect score, 228 views |
| l8abBf4aMv8 | Why The Sol Invictus Story Is Wrong | 45 / D | D | n/a | 214 | — |
| Oc7oq292HkM | Why Trump Walked Back... | 75 / B | B | n/a | 193 | — |
| BNEEAD--Y3c | Fact-Checking Nick Fuentes... | REJECTED (0) | REJECTED | n/a | 184 | — |
| UxsXdUj0EhU | The Hidden Pattern Behind Armenia | 85 / A | A | 4.11% | 115 | **HIGH SCORE / LOW RESULT** — A grade, 4.11% CTR, only 115 views (impressions only 1,347; supply not demand failure) |
| n-CUSE4bDvg | Cyprus Is Still Divided... | 90 / A | A | 2.40% | 102 | **HIGH SCORE / LOW RESULT** — A grade, 2.40% CTR, 102 views |
| LrthC_8Hb2Y | China Claims the South China Sea... | 90 / A | A | 1.83% | 91 | **HIGH SCORE / LOW CTR + LOW RESULT** — A grade, but 1.83% CTR is below channel avg |
| Yx5oywZs-rk | Stalin Purged His Own Army... | 65 / C | C | 1.55% | 122 | — |
| 499YLd1BHZ4 | Putin Says NATO Promised Not to Expand | 75 / B | B | 2.48% | 51 | — |
| xODFE2Pyubo | 38 Dead Over 4.6 Square Kilometers | 80 / A | A | 2.34% | 32 | **HIGH SCORE / LOW RESULT** — A grade, impressions starved (668) |

**Biggest mispredictions summary:**

- **Scorer wrong, video succeeded:** Y21EjQ0v9W4 (REJECTED → 29,713 views), oDK52GwjTIo (REJECTED → 1,966 views / 4.31% CTR), lFGs5NHMxMw (REJECTED → 440 views). All three were rejected on colon penalty — the colon rule is systematically over-penalizing.
- **Low score, high CTR:** UH2PddfaaR8 (D grade → 5.41% CTR, channel's highest recorded CTR). Scorer undervalues "How the X did Y" curiosity-gap titles on ideological topics.
- **High score, low result (impressions-starved):** LCze9B2xpOI (100/A → 257 views), lPilDVSAeEM (100/A → 228 views), UxsXdUj0EhU (85/A → 115 views), n-CUSE4bDvg (90/A → 102 views), xODFE2Pyubo (80/A → 32 views). These videos had acceptable-to-good CTR where measured but YouTube simply did not distribute them. The scorer correctly assessed title quality; the failure mode is distribution, not packaging.

---

## 5. DISTRIBUTION FACTS

| Metric | Value |
|--------|-------|
| Total channel views (all 57 videos) | 46,619 |
| Share held by top 1 video (Guatemala vs Belize) | 63.7% (29,713 views) |
| Share held by top 3 videos | 79.4% (37,034 views) |
| Share held by top 5 videos | 84.0% (39,168 views) |
| Median views (57 videos) | 91 |
| Median CTR (22 videos with CTR data) | 2.48% |
| Channel avg CTR (as reported in POST-PUBLISH files) | 2.36% |
| Videos above 1,000 views | 4 |
| Videos above 500 views | 9 |
| Videos with 0 subscribers gained | 22 |

**Concentration note:** The distribution is extreme. The top 1 video (Guatemala vs Belize) holds 64% of all channel views. Remove the top 5 and the remaining 52 videos share 16% of total views (average 143 views each). The channel is functionally a one-video channel in terms of reach.

**CTR range (22 videos):** 1.55% (Stalin Purged His Army) to 5.41% (KGB Weaponized Palestinian Resistance). Legacy 2014 video (ejkC0ecYyxk) shows 15.91% CTR on 44 impressions — not meaningful.

---

*End of D1 Dossier*

---

## FRESH CTR SNAPSHOT — 2026-06-10 (YouTube Reporting API via ctr_tracker; supersedes the 2026-02-23 POST-PUBLISH CTR above)

NOTE: impression_count is the Reporting-API reach window, not lifetime impressions — compare videos against each other within this snapshot, not against lifetime view totals.

| video_id | title | CTR % | impressions | views |
|---|---|---|---|---|
| UH2PddfaaR8 | How the KGB Weaponized Palestinian Resistance | 18.41 | 315 | 463 |
| XbGl1Kcspt4 | Guatemala vs Belize Dispute: What 3 ICJ Cases Show | 12.11 | 512 | 5356 |
| LO_fUeX9IEQ | JD Vance Claims Christians Found Child Sacrifice. Here' | 10.0 | 60 | 1147 |
| Oc7oq292HkM | Why Trump Walked Back the Armenian Genocide | 9.72 | 72 | 193 |
| Y21EjQ0v9W4 | The Country That Might Disappear: Guatemala vs Belize | 8.49 | 1850 | 29723 |
| WZnCxVPNF7A | 34,000 People Can't Decide Their Future. One Clause Tra | 8.33 | 48 | 54 |
| _N_08zn95FY | Turkey Claims 152 Greek Islands. Here's Why. | 8.26 | 121 | 964 |
| d1Bx3uptNuo | "Putin Copied Serbia's Playbook. Here's the Original | 7.41 | 27 | 68 |
| QgDJSu0Y5K0 | 7 Million Landmines Guard a Wall Nobody Talks About | 6.98 | 86 | 128 |
| HtVIC4dS0e8 | Iran vs Its Own Democracy. 120 Years of Failed Revoluti | 6.58 | 76 | 72 |
| xODFE2Pyubo | 38 Dead Over 4.6 Square Kilometers. Both Sides Blame On | 5.71 | 35 | 32 |
| l8abBf4aMv8 | Why The Sol Invictus Story Is Completely Wrong | 5.62 | 89 | 215 |
| Q5Pfv_dPubU | The CIA Document That Proved Operation Condor | 4.91 | 163 | 49 |
| MXvTuHXSf3o | Nigeria vs Cameroon. The Court Chose Paper Over People | 4.82 | 83 | 17 |
| WgE2FLsDhfk | Two Countries Split a Continent They Had Never Mapped | 4.76 | 42 | 793 |
| BXyT8OTGBBo | Britain Promised the Same Land to Three Different Group | 4.76 | 42 | 102 |
| VyPv2n4mii8 | Primary Sources Destroy the 'Awesome Crusades' Narrativ | 4.69 | 64 | 689 |
| GuL9PtXEjN0 | Somaliland's Legal Independence Problem | 4.17 | 48 | 405 |
| zt7VntgauC8 | The Piri Reis Map Cites Columbus. Hancock Calls It 12,0 | 3.81 | 3097 | 147 |
| liW4BSh46DU | Treaty of Tripoli: The Most-Cited Line Isn’t in the Ara | 3.67 | 109 | 37 |
| yetYD9_VcmM | The Myths of Thermopylae: Fake Quotes & Missing Soldier | 3.57 | 56 | 80 |
| -kg30uRUY1M | The 1947 Partition Map Didn't Follow Religion | 3.33 | 60 | 120 |
| X0dO-aJx-aQ | London's Stock Exchange Funded a Genocide | 2.94 | 34 | 137 |
| FvqALriDCv4 | JD Vance vs History: Who Invented Human Rights? | 2.86 | 35 | 49 |
| rbsdtveYvv0 | The Spanish Inquisition Documented Its Torture Methods. | 2.56 | 313 | 37 |
| sXadwOj8VoA | Honduras Called These Islands British Territory. Then C | 2.44 | 82 | 47 |
| 2RQWu-cyO90 | Was Lagertha Real? DNA Says Female Viking Warriors Exis | 2.38 | 84 | 55 |
| aSfZtrgGjwA | Yes Slavery Existed In Africa. Then Europe Took Over | 1.91 | 5188 | 77 |
| BNEEAD--Y3c | Fact-Checking Nick Fuentes: Why His Claims Are Dangerou | 1.54 | 65 | 186 |
| mCR5f_ZcB5k | The Hijab Wasn't Modesty. It Was a Property Law | 1.48 | 1759 | 80 |
| mg6ujk6rDVE | The Lenape Never Sold Manhattan. Every Piece Was Forged | 0.0 | 101 | 18 |
| lFGs5NHMxMw | The Berlin Conference: How Colonial Borders Still Fuel  | 0.0 | 59 | 440 |
| imPn_OxLYlk | Vichy France: The Anti-Jewish Law Nobody Translated | 0.0 | 93 | 82 |
| P6yalauLDic | Mexico's Missing Island: The Map Error That Cost $22 Bi | 0.0 | 43 | 13 |
| TYNaIu28LeU | 3 Men Signed 1 Document. The Soviet Union Ceased to Exi | 0.0 | 81 | 40 |
| L5ZIP24-36s | Iran vs the CIA. Two Coups the West Wants You to Forget | 0.0 | 52 | 40 |
| LuLZYZWMiU4 | The Flat Earth Myth Was Invented in 1828. Here's Who Di | 0.0 | 42 | 213 |
| ZZz_g_Ov6Lg | Britain Expelled 2,000 Islanders. The Memo Proves It | 0.0 | 32 | 29 |
| -QG8trhNsoM | Medieval Europe's Hidden Literacy Boom / What Historian | 0.0 | 58 | 115 |
| XKAqt_ZLHGo | Why Egypt and Sudan Both Reject Bir Tawil | 0.0 | 48 | 73 |
| oDK52GwjTIo | Venezuela vs Guyana: The Oil War Over Essequibo | 0.0 | 22 | 1966 |
| 6GybGd_q25w | The Colonial Structures Killing Peruvian Protesters in  | 0.0 | 28 | 50 |
| jLZngVFKWVg | How 3 Coups Ended 60 Years of French Control in Africa | 0.0 | 21 | 30 |
| n-CUSE4bDvg | Cyprus Is Still Divided. Both Sides Blame the Other | 0.0 | 18 | 102 |
| 499YLd1BHZ4 | Putin Says NATO Promised Not to Expand. The Documents D | 0.0 | 30 | 51 |
| UxsXdUj0EhU | The Hidden Pattern Behind the Armenia Conflict | 0.0 | 27 | 115 |
| LCze9B2xpOI | China vs Taiwan. 4 Historical Claims Exposed by Scholar | 0.0 | 12 | 257 |
| LrthC_8Hb2Y | China Claims the Entire South China Sea. A Court Said N | 0.0 | 11 | 91 |
| lPilDVSAeEM | India vs Pakistan. Britain Sold Kashmir for 7.5 Million | 0.0 | 18 | 228 |
| JkH4XIHfnJU | The Historical Pattern Nobody Wants to Admit About Trad | 0.0 | 9 | 106 |
| 7fpBz6uo504 | 5 Big Myths About Israel and Palestine Busted! | 0.0 | 33 | 640 |
| Ac-k2p9Gvj4 | "Ancient Hatreds" in the Middle East Are a Modern Inven | 0.0 | 12 | 95 |
| Yx5oywZs-rk | Stalin Purged His Own Army. Then Hitler Invaded | 0.0 | 20 | 122 |
| 71xY0Pt4T-M | Putin Invaded Georgia Before Ukraine. Nobody Stopped Hi | 0.0 | 26 | 40 |
| 6SdfqTYPviQ | 1,000 Years of Ukraine: The History Putin Erased | 0.0 | 33 | 89 |
| yMAWJcjo_ug | Debunking Begins! Why I Started ‘History vs Hype’ | 0.0 | 9 | 43 |
| ejkC0ecYyxk | vikinghorde Title1 | 0.0 | 0 | 39 |
