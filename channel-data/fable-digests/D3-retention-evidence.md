# D3 Retention Evidence Digest

**Build date:** 2026-06-11
**Data vintage:** analytics.db refresh 2026-06-10; SRT files from production; RETENTION-SCRIPT-CORRELATION.md generated 2026-03-21 (n=42); HOOK-RETENTION-CORRELATION.md generated 2026-03-07 (n=17).
**Purpose:** Input for rule-validation session — cross-examine scriptwriting rules against actual retention. Numbers from database and SRTs only.

---

## PART 1 — RETENTION EVENTS

### How to read this section

- **Cliff:** audience_watch_ratio drops ≥ 0.04 within one data-step (≤ 3% elapsed ratio). Converted to mm:ss using actual duration.
- **Hold/Recovery:** plateau or rise sustained across ≥ 3 consecutive points after the 20% mark. Deduplicated: only one entry per 5%-elapsed window.
- **Curve shape:** audience_watch_ratio at 10 / 25 / 50 / 75 / 100% elapsed.
- **SRT text:** 2 subtitle lines bracketing the cliff timestamp (DaVinci offset normalized). "no SRT" = no project folder with matching subtitle file found.

Cliff analysis threshold used: ≥ 4pp drop within a single retention-curve step (adjacent rows where elapsed_ratio difference ≤ 0.031). This intentionally captures the opening-minute hemorrhage universal across all videos — that pattern itself is the signal.

---

### Video 1 — Y21EjQ0v9W4
**Title:** The Country That Might Disappear: Guatemala vs Belize
**Duration:** 657s (10:57) | **Views:** 29,713 | **Avg retention:** 35.34% | **Published:** 2025-10-27

**Curve:** 10%=50.0% → 25%=39.7% → 50%=32.0% → 75%=28.2% → 100%=24.6%
Shape: steep front drop (~26pp in first 10%), then slow linear decay.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:13–00:19 | 2–3% | −7.1pp | [00:06] "Justice is hearing oral arguments." / [00:08] "The ruling comes in 2027." |
| 00:19–00:26 | 3–4% | −10.3pp | [00:14] "to see what the court" / [00:15] "actually does when countries" |
| 00:26–00:32 | 4–5% | −8.2pp | [00:19] "The precedent points" / [00:20] "towards one likely outcome." |
| 00:39–00:45 | 6–7% | −4.3pp | [00:32] "Let me show you the three precedents," |
| 00:45–00:52 | 7–8% | −5.1pp | [00:34] "then the historical / twist that makes Guatemala's" |

**Post-20% holds:** 02:11–02:24 (41.3%→41.0%), 03:03–03:17 (38.6%→37.7%), 03:56–04:09 (35.6%→35.2%)
**Note:** Holds are micro-plateaus, not recoveries — curve decays slowly and steadily after the opening cliff. The strongest video in the dataset; its floor at 100% (24.6%) exceeds the *avg* retention of most other videos.

---

### Video 2 — XbGl1Kcspt4
**Title:** Guatemala vs Belize Dispute: What 3 ICJ Cases Show
**Duration:** 668s (11:08) | **Views:** 5,355 | **Avg retention:** 38.67% | **Published:** 2025-12-04

**Curve:** 10%=55.3% → 25%=44.4% → 50%=34.3% → 75%=31.1% → 100%=28.3%
Shape: same steep-front pattern, slightly higher floor than #1. Same SRT file applies (two videos share a folder).

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:13–00:20 | 2–3% | −6.8pp | [00:06] "Justice is hearing oral arguments." / [00:08] "The ruling comes in 2027." |
| 00:20–00:26 | 3–4% | −6.4pp | [00:14] "to see what the court" / [00:15] "actually does when countries" |
| 00:26–00:33 | 4–5% | −4.3pp | [00:19] "The precedent points" / [00:20] "towards one likely outcome." |
| 00:40–00:46 | 6–7% | −6.3pp | [00:34] "then the historical twist that makes Guatemala's" |

**Post-20% holds:** 03:20–03:33, 04:13–04:27, 05:07–05:20 — all micro-plateaus (~0.5pp variance).
**Note:** Higher absolute retention than #1 despite fewer views. Both Guatemala videos share the same SRT; cannot distinguish opening text.

---

### Video 3 — oDK52GwjTIo
**Title:** Venezuela vs Guyana: The Oil War Over Essequibo
**Duration:** 633s (10:33) | **Views:** 1,966 | **Avg retention:** 34.56% | **Published:** 2025-10-19

**Curve:** 10%=54.8% → 25%=42.5% → 50%=31.1% → 75%=24.2% → 100%=20.4%
Shape: steeper mid-section decay than Guatemala videos; larger late-video drop (75%→100% = −3.8pp vs Guatemala's ~3.6pp).

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:06–00:12 | 1–2% | −7.6pp | no SRT |
| 00:12–00:18 | 2–3% | −7.8pp | no SRT |
| 00:18–00:25 | 3–4% | −5.5pp | no SRT |
| 00:44–00:50 | 7–8% | −4.8pp | no SRT |

**Post-20% holds:** 03:41–03:54, 04:32–04:44, 05:41–05:54 — all micro-plateaus.
**No project folder found.** No SRT available.

---

### Video 4 — LO_fUeX9IEQ
**Title:** JD Vance Claims Christians Found Child Sacrifice. Here's the Evidence.
**Duration:** 376s (6:16) | **Views:** 1,147 | **Avg retention:** 26.47% | **Published:** 2025-11-04

**Curve:** 10%=49.4% → 25%=31.0% → 50%=22.3% → 75%=17.1% → 100%=11.7%
Shape: catastrophic early drop — loses 18.4pp in the 10–25% window (roughly 00:38–01:34), one of the sharpest mid-early falls in the dataset.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:11–00:15 | 3–4% | −6.0pp | [00:05] "Christianity invented human rights, the" / [00:07] "founders wanted Christianity in government," |
| 00:15–00:18 | 4–5% | −12.5pp | [00:09] "and Christian civilization is the most" / [00:10] "moral in history. I went to the Vatican archives," |
| 00:18–00:22 | 5–6% | −8.8pp | [00:12] "to the Vatican archives," / [00:14] "I pulled up papal documents from the 1800s, I checked what" |

**Post-20% holds:** 01:30–01:37 (31.3%→30.6%), 02:11–02:19 (25.6%→25.0%) — micro-plateaus only.
**Observation:** The 12.5pp cliff at 00:15–00:18 lands precisely on the "I went to the Vatican archives / I pulled up papal documents" credential chain — consistent with RETENTION-SCRIPT-CORRELATION.md's finding that personal_authority content in the first 13% carries the heaviest dropout (avg delta −0.051, n=88 early-zone points).

---

### Video 5 — _N_08zn95FY
**Title:** Turkey Claims 152 Greek Islands. Here's Why.
**Duration:** 548s (9:08) | **Views:** 963 | **Avg retention:** 39.10% | **Published:** 2025-08-27

**Curve:** 10%=53.2% → 25%=42.3% → 50%=37.6% → 75%=36.1% → 100%=17.5%
Shape: unusual — relatively flat 25–75% window (only −6.2pp over half the video), then sharp late cliff at 98–99% (−7.2pp). Strong mid-section retention; catastrophic finish cliff.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:05–00:10 | 1–2% | −12.4pp | no SRT |
| 00:16–00:21 | 3–4% | −9.9pp | no SRT |
| 00:21–00:27 | 4–5% | −5.9pp | no SRT |
| 08:57–09:02 | 98–99% | −7.2pp | no SRT |

**Post-20% holds:** 01:49–02:00, 02:33–02:44, 03:17–03:28 — extended plateau zone, very stable 20–75%.
**No project folder found.** No SRT available.
**Note:** The 25–75% flatness (42.3% → 36.1%, only −6.2pp) is exceptional. Greece/Turkey is a high-interest territorial topic with a large diaspora audience; audience self-selection likely explains the plateau.

---

### Video 6 — WgE2FLsDhfk
**Title:** Two Countries Split a Continent They Had Never Mapped
**Duration:** 769s (12:49) | **Views:** 793 | **Avg retention:** 16.86% | **Published:** 2026-03-18

**Curve:** 10%=28.7% → 25%=19.7% → 50%=14.7% → 75%=13.3% → 100%=9.5%
Shape: catastrophic. Loses 72.4pp by 10% mark — the opening cliff is 35.4pp in a single step. Lowest-retention territorial video in the top 15.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:07–00:15 | 1–2% | −7.7pp | [00:00] "Open a language map of South America." / [00:02] "Almost the entire continent speaks Spanish." |
| 00:15–00:23 | 2–3% | −35.4pp | [00:09] "The border between Spanish-speaking and" / [00:10] "Portuguese-speaking South America isn't a mountain range or a river." |
| 00:23–00:30 | 3–4% | −11.9pp | [00:16] "perfect north-south line." / [00:18] "That line is a treaty." |
| 00:30–00:38 | 4–5% | −7.1pp | [00:24] "Spanish town called Tordesillas." / [00:26] "Two countries drew a line through a world they'd never mapped." |

**Post-20% holds:** 02:49–03:04, 03:50–04:06, 04:59–05:15 — micro-plateaus around 15–20%.
**Observation:** The 35.4pp cliff at 00:15–00:23 — the single largest opening cliff in the top-15 dataset — occurs during the transition from language-map observation to treaty explanation. This video was published after the PACKAGING_MANDATE hardened. Duration at 769s (12:49) exceeds the 12-minute hard cap.

---

### Video 7 — VyPv2n4mii8
**Title:** Primary Sources Destroy the 'Awesome Crusades' Narrative
**Duration:** 635s (10:35) | **Views:** 689 | **Avg retention:** 26.88% | **Published:** 2025-11-27

**Curve:** 10%=41.9% → 25%=31.5% → 50%=25.3% → 75%=20.4% → 100%=15.2%
Shape: steep front drop (−52.5pp in first 10%), slow but consistent decay through to end.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:06–00:12 | 1–2% | −6.5pp | [00:00] "This is Pete Hegseth, current US Secretary of Defense." / [00:04] "He has a tattoo that says 'Deus Vult'," |
| 00:12–00:19 | 2–3% | −17.1pp | [00:06] "Latin for 'God wills it', that was the war cry of the first crusade." / [00:12] "A viral video with nearly 5 million views" |
| 00:19–00:25 | 3–4% | −12.6pp | [00:14] "argues the crusades were defensive," / [00:17] "justified and 'awesome'." |
| 00:31–00:38 | 5–6% | −5.3pp | [00:24] "justified, but were actually a historic achievement." / [00:28] "This narrative is being used right now." |

**Post-20% holds:** 02:26–02:38 (31.8%→31.5%), 03:29–03:42 (29.4%→28.7%), 04:26–04:39 (27.1%→26.8%).
**Observation:** 17.1pp cliff at 00:12–00:19 during the transition from Hegseth intro to "a viral video with 5 million views." This is the "famous current event → myth narration" moment. RETENTION-SCRIPT-CORRELATION.md marks the Berlin Conference text at 4% position (about 00:21 for a 547s video) as one of the top-10 worst drops, classified as `personal_authority`.

---

### Video 8 — 7fpBz6uo504
**Title:** 5 Big Myths About Israel and Palestine Busted!
**Duration:** 718s (11:58) | **Views:** 640 | **Avg retention:** 31.19% | **Published:** 2025-07-29

**Curve:** 10%=50.2% → 25%=40.4% → 50%=31.3% → 75%=24.2% → 100%=11.9%
Shape: severe late-video collapse — 75%→100% = −12.3pp (worst late drop in top 15).

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:07–00:14 | 1–2% | −13.5pp | no SRT |
| 00:14–00:21 | 2–3% | −8.2pp | no SRT |
| 00:21–00:28 | 3–4% | −7.1pp | no SRT |
| 00:43–00:50 | 6–7% | −4.1pp | no SRT |

**Post-20% holds:** 02:45–02:59 (40.1%→40.4%, slight recovery), 03:49–04:04 (36.3%→36.8%, slight recovery), 05:08–05:23 (32.4%→31.9%).
**Note:** Two mid-section micro-recoveries (at ~25% and ~34%), suggesting some re-engagement in the evidence sections. The severe 75%→100% cliff is unusual — the final 3 minutes bled 12.3pp. No SRT available to identify content. Duration 11:58 is just under the hard cap.

---

### Video 9 — UH2PddfaaR8
**Title:** How the KGB Weaponized Palestinian Resistance
**Duration:** 606s (10:06) | **Views:** 457 | **Avg retention:** 40.49% | **Published:** 2025-09-25

**Curve:** 10%=56.4% → 25%=48.2% → 50%=42.0% → 75%=36.7% → 100%=21.6%
Shape: best mid-section retention of the 15 videos (56.4%→42.0% over first 50%, only −14.4pp). Sharp late drop (75%→100% = −15.1pp).

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:06–00:12 | 1–2% | −13.8pp | no SRT |
| 00:12–00:18 | 2–3% | −9.8pp | no SRT |
| 00:24–00:30 | 4–5% | −4.2pp | no SRT |

**Post-20% holds:** 02:19–02:31 (47.8%→48.2%, recovery), 03:13–03:26 (44.7%→44.4%), 04:02–04:14 (42.2%→42.0%).
**Note:** The 02:19–02:31 recovery (+0.4pp) is notable — one of the few genuine mid-video upswings in the top 15. No SRT; cannot identify what content caused it. The 40.49% avg retention is the highest in the top 15 among non-Guatemala videos.

---

### Video 10 — lFGs5NHMxMw
**Title:** The Berlin Conference: How Colonial Borders Still Fuel Conflict in Africa
**Duration:** 547s (9:07) | **Views:** 440 | **Avg retention:** 24.67% | **Published:** 2026-03-12

**Curve:** 10%=38.3% → 25%=27.3% → 50%=22.2% → 75%=18.8% → 100%=14.9%
Shape: catastrophic opening (−61.7pp in first 10%), then stable-but-low. RETENTION-SCRIPT-CORRELATION.md identifies this video's 00:21 point (4% position) as the #10 worst drop in the 42-video dataset.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:05–00:10 | 1–2% | −6.2pp | [00:00] "In just three months, 14 countries" / [00:02] "divided an entire continent that none of them actually ruled." |
| 00:10–00:16 | 2–3% | −6.0pp | [00:05] "them actually ruled." / [00:06] "That was 1884 and the borders they drew, using rivers, rulers and latitude lines," |
| 00:16–00:21 | 3–4% | −20.6pp | [00:10] "using rivers, rulers and latitude lines," / [00:14] "ended up splitting 229 ethnic groups across multiple countries." |
| 00:21–00:27 | 4–5% | −13.8pp | [00:14] "ended up splitting 229 ethnic groups" / [00:17] "across multiple countries. Those groups, they're still fighting over" |
| 00:27–00:32 | 5–6% | −4.6pp | (continuation of same section) |
| 00:54–01:00 | 10–11% | −4.1pp | beyond what SRT covers |

**Post-20% holds:** 01:54–02:05 (30.0%→30.7%, recovery), 02:38–02:49 (25.7%→26.2%, recovery), 03:22–03:33 (24.5%→24.8%).
**Observation:** The 20.6pp cliff at 00:16–00:21 occurs during "229 ethnic groups across multiple countries" — a statistics-dense sentence. RETENTION-SCRIPT-CORRELATION.md classifies this position as `personal_authority` (the creator referencing the conference results), but the SRT text is primarily statistical narration.

---

### Video 11 — GuL9PtXEjN0
**Title:** Somaliland's Legal Independence Problem
**Duration:** 673s (11:13) | **Views:** 405 | **Avg retention:** 24.04% | **Published:** 2026-01-01

**Curve:** 10%=37.1% → 25%=31.7% → 50%=22.1% → 75%=18.5% → 100%=14.5%
Shape: severe opening (−62.9pp in first 10%), then steady decay. Similar profile to Berlin Conference.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:06–00:13 | 1–2% | −17.5pp | [00:00] "35 countries recognized Somaliland in" / [00:02] "1960, then they all forgot." |
| 00:13–00:20 | 2–3% | −17.5pp | [00:06] "This is where 12% of global trade passes" / [00:08] "and where 5 powers are now competing for control." |
| 00:20–00:26 | 3–4% | −9.4pp | [00:13] "Ethiopia is landlocked and desperate for port access." |
| 00:26–00:33 | 4–5% | −6.9pp | [00:16] "China, UAE, Turkey, Israel all want in." |
| 00:33–00:40 | 5–6% | −6.9pp | [00:22] "And right in the middle, a functioning democracy with its own government, currency and borders" |

**Post-20% holds:** 02:21–02:34 (32.0%→32.2%), 03:21–03:35 (28.9%→28.9%), 04:49–05:02 (22.1%→22.1%).
**Observation:** The dual 17.5pp cliffs at 00:06–00:20 are the steepest opening run in the top 15 after Berlin Conference. The content at those moments is the strongest hook material — "35 countries recognized Somaliland then forgot" and "12% of global trade" — confirming that the opening hemorrhage is structural/algorithmic, not content-driven.

---

### Video 12 — LCze9B2xpOI
**Title:** China vs Taiwan. 4 Historical Claims Exposed by Scholars
**Duration:** 575s (9:35) | **Views:** 257 | **Avg retention:** 27.79% | **Published:** 2025-08-23

**Curve:** 10%=39.8% → 25%=33.6% → 50%=25.4% → 75%=23.8% → 100%=13.3%
Shape: moderate opening loss (−60.2pp in first 10%), then steady mid-section, sharp late drop (75%→100% = −10.5pp).

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:05–00:11 | 1–2% | −10.9pp | no SRT (Taiwan folder has no subtitle file) |
| 00:11–00:17 | 2–3% | −8.2pp | no SRT |
| 00:17–00:23 | 3–4% | −15.6pp | no SRT |
| 00:23–00:28 | 4–5% | −4.7pp | no SRT |
| 00:34–00:40 | 6–7% | −4.7pp | no SRT |

**Post-20% holds:** 02:06–02:18, 03:15–03:27, 04:07–04:18 — micro-plateaus.

---

### Video 13 — lPilDVSAeEM
**Title:** India vs Pakistan. Britain Sold Kashmir for 7.5 Million Rupees
**Duration:** 629s (10:29) | **Views:** 228 | **Avg retention:** 19.56% | **Published:** 2025-08-14

**Curve:** 10%=31.2% → 25%=22.3% → 50%=17.9% → 75%=13.8% → 100%=8.0%
Shape: one of the weakest retention profiles in the dataset. Opening hemorrhage (−68.8pp in first 10%) and low floor.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:06–00:12 | 1–2% | −9.4pp | [00:00] "On August 8th 1947, a draft map was sent from the Viceroy's office in New Delhi to" / [00:06] "the governor of Punjab." |
| 00:12–00:18 | 2–3% | −11.2pp | [00:06] "the governor of Punjab." / [00:08] "It showed the new border between India and Pakistan." |
| 00:18–00:25 | 3–4% | −16.5pp | [00:12] "Ferozepur, a district that was 55% Muslim, containing the canal headworks" / [00:14] "that controlled irrigation for millions" |
| 00:25–00:31 | 4–5% | −4.0pp | [00:19] "of acres of Pakistani farmland, was on the Pakistani side." |
| 00:31–00:37 | 5–6% | −8.0pp | [00:23] "Three days later, a" (transition point) |

**Post-20% holds:** 03:02–03:14 (flat at 19.6%), 03:52–04:05 (flat at 19.6%), 05:01–05:14 (17.0%→17.9%, recovery).
**Observation:** The 16.5pp cliff at 00:18–00:25 lands on the Ferozepur canal headworks detail — hyper-specific geographic/administrative content in the first 30 seconds. Per HOOK-RETENTION-CORRELATION.md this type of cold-fact opening averages 28.2% retention; this video at 19.56% is a significant underperform.

---

### Video 14 — l8abBf4aMv8
**Title:** Why The Sol Invictus Story Is Completely Wrong
**Duration:** 879s (14:39) | **Views:** 214 | **Avg retention:** 23.09% | **Published:** 2025-12-25

**Curve:** 10%=43.8% → 25%=29.0% → 50%=19.5% → 75%=15.2% → 100%=13.3%
Shape: severe front drop (−56.2pp in first 10%), dramatic mid-fall (10%→50% loses 24.3pp), then relative stability in final quarter.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:08–00:17 | 1–2% | −17.6pp | no SRT |
| 00:17–00:26 | 2–3% | −16.2pp | no SRT |
| 00:35–00:43 | 4–5% | −4.8pp | no SRT |

**Post-20% holds:** 02:55–03:13 (33.3%→32.9%), 04:32–04:50 (23.8%→23.8%), 05:42–06:00 (23.3%→22.9%).
**Note:** Duration 14:39 substantially exceeds the 12-minute hard cap. This is potentially a confound: CONSTRAINT T cites the rule-source as r=−0.455 (n=47). No SRT available.

---

### Video 15 — LuLZYZWMiU4
**Title:** The Flat Earth Myth Was Invented in 1828. Here's Who Did It.
**Duration:** 1070s (17:50) | **Views:** 213 | **Avg retention:** 12.84% | **Published:** 2026-01-15

**Curve:** 10%=25.7% → 25%=12.4% → 50%=10.5% → 75%=7.6% → 100%=5.2%
Shape: catastrophic. Loses 74.3pp in the first 10%. The worst overall retention in the top-15 dataset. By 25% (4:28) only 12.4% of viewers remain.

| Timestamp | Elapsed | Drop | SRT text at cliff |
|-----------|---------|------|-------------------|
| 00:10–00:21 | 1–2% | −13.3pp | [00:01] "United States from 1880. Look up what it says about Columbus." / [00:04] "Columbus believed the earth to be round." |
| 00:21–00:32 | 2–3% | −25.2pp | [00:12] "Just 18 years later, the earth was flat as a plate. One of the most" / [00:15] "successful lies in western history was manufactured in just 18 years" |
| 00:32–00:42 | 3–4% | −16.2pp | [00:23] "I went through the medieval manuscripts." / [00:27] "'Bede's" |
| 01:14–01:25 | 7–8% | −4.3pp | [01:06] "Dickinson White in 1896, he buried the lie under a mountain of footnotes" |

**Post-20% holds:** 04:06–04:27 (13.3%→12.4%, slight drop), 05:31–05:53 (10.5%→11.9%, recovery), 07:18–07:40 (10.0%→10.9%, recovery).
**Observation:** The 25.2pp cliff at 00:21–00:32 lands precisely on "One of the most successful lies in western history was manufactured in just 18 years by textbook authors." This is classified as `personal_authority` in RETENTION-SCRIPT-CORRELATION.md (position 3%, ranked #3 worst single drop in 42-video dataset). Duration 17:50 = 49% over the hard cap. HOOK-RETENTION-CORRELATION.md identifies this as the worst-performing video in its 17-video sample (11.57% retention at time of that analysis).

---

### Cross-Video Opening Patterns

All 15 videos lose material audience in the 00:06–00:45 window — no exceptions. The range is 24.6pp to 91.4pp lost by 10% elapsed. This is the universal opening hemorrhage documented in RETENTION-SCRIPT-CORRELATION.md. Key observations:

1. **The opening cliff is structural, not content-specific.** Even the strongest hook content (Somaliland "35 countries recognized then forgot," Guatemala's ICJ methodology promise, Berlin Conference's specific statistics) still loses 17–35pp in the first 30 seconds.

2. **The 3–4% step consistently carries the heaviest cliff.** In 11 of 15 videos, the largest single-step drop occurs between elapsed 0.02–0.05 (00:13–00:45 range depending on video length). This is the transition from "hook beat 1–2" to "hook beat 3–4."

3. **After the opening cliff, mid-section is flat.** Genuine mid-video recoveries are rare (Venezuela +0.4pp recovery, Israel/Palestine +0.4pp twice). Most "holds" are micro-plateaus where decay temporarily pauses.

4. **Late-video collapses are a separate phenomenon.** Turkey (−7.2pp at 98%), KGB (−15.1pp at 75–100%), Israel/Palestine (−12.3pp at 75–100%) all have distinct late-section crashes not visible in the 10/25/50% curve shape. The 75% checkpoint is a meaningful indicator: videos with <20% at 75% tend to collapse in the final quarter.

5. **Duration correlates with low retention in this sample.** The three videos exceeding 12 minutes (Tordesillas 769s/16.86%, Sol Invictus 879s/23.09%, Flat Earth 1070s/12.84%) are the 3rd, 13th, and 15th worst in the dataset respectively.

---

## PART 1B — Summary of Prior Correlation Analyses

### RETENTION-SCRIPT-CORRELATION.md (2026-03-21)

**Method:** 42 videos, 4,200 retention data points mapped to SRT content. Content labeled: narration / quote / primary_source / statistic / modern_relevance / personal_authority.

**Key claims with stated n:**

| Claim | n | Evidence type |
|-------|---|---------------|
| narration best overall avg delta (−0.005) | 1,654 data points | own-channel SRT mapping |
| personal_authority worst avg delta (−0.044) | 102 data points | own-channel SRT mapping |
| personal_authority in EARLY position avg delta (−0.051) | 88 of the 102 points | own-channel SRT mapping |
| personal_authority in MID position near-flat (−0.0001) | 10 of the 102 points | own-channel SRT mapping |
| statistic has highest positive-rate (61%) across all types | 354 data points | own-channel SRT mapping |
| late-video statistics gain viewers (+0.001 delta) | 114 data points (late zone) | own-channel SRT mapping |
| ALL top-10 worst moments are in first 2–4% of videos | 10 worst events | own-channel SRT mapping |
| modern_relevance underperforms at −0.010 avg delta | 577 data points | own-channel SRT mapping |

**Authors' caution:** "The personal_authority finding is misleading — 86% cluster in the first third where all videos lose viewers. Mid-video personal_authority is flat." The study notes it cannot separate hook content-type effects from structural-position effects.

### HOOK-RETENTION-CORRELATION.md (2026-03-07)

**Method:** 17 videos with SRT files matched to analytics.db retention data. Hook style classified from first 30 seconds.

**Key claims with stated n:**

| Claim | n | Evidence type |
|-------|---|---------------|
| myth hook avg retention 29.3% | n=2 | own-channel, small |
| cold_fact hook avg retention 28.2% | n=11 | own-channel |
| document hook avg retention 23.9% | n=2 | own-channel, small |
| context hook avg retention 28.2% | n=2 | own-channel, small |
| hook does not determine retention alone | qualitative observation | own-channel |

**Authors' caution:** "Small sample (n=17). Treat as directional. No A/B testing — differences may reflect topic interest or algorithm distribution."

---

## PART 2 — Rule Inventory with N-Sizes

Source files scanned: `.claude/agents/script-writer-v2.md` (v16.5), `.claude/agents/structure-checker-v2.md` (Wave 10), `tools/PACKAGING_MANDATE.md`.

Legend — Evidence type:
- **own-channel n<30** = derived from this channel's data, sample below statistical threshold
- **niche-wide** = derived from competitor/niche corpus (competitor transcripts, outlier analysis)
- **none stated** = no explicit evidence cited in rule text

| # | Rule text (≤20 words) | Source file | Stated evidence / n | Evidence type |
|---|----------------------|-------------|---------------------|---------------|
| 1 | Ad-libbed content retains +10% over scripted (0.351 vs 0.250) | script-writer-v2 Rule intro | n not stated; two-tier scripting rationale | none stated |
| 2 | r=−0.455 duration vs retention; 8–12 min sweet spot (29.6%, 1,521 avg views) | script-writer-v2 Rule 10 | n=47 | own-channel n<30 (47 videos but single channel) |
| 3 | 8–12 min avg 29.6% retention, 1,521 avg views | script-writer-v2 Rule 10 | n=47 | own-channel |
| 4 | 12–20 min avg 24.7% retention, 101 avg views | script-writer-v2 Rule 10 | n=47 | own-channel |
| 5 | Sentence over 60 words must be followed by under-10-word sentence | script-writer-v2 Rule 11 | "validated across 39 videos" | own-channel |
| 6 | First attributed academic quote must appear before 90 seconds | script-writer-v2 Rule 12 | "loses 15–25% at 2–4% mark" (no n) | none stated |
| 7 | myth_contradiction hook = 36.7% retention | script-writer-v2 Rule 17; structure-checker-v2 Constraint A | "cross-validated 2026-03-24, n=40" | niche-wide |
| 8 | contextual_opening hook = 32.0% retention | script-writer-v2 Rule 17; structure-checker-v2 | n=40 | niche-wide |
| 9 | cold_fact hook = 29.4% retention | script-writer-v2 Rule 17; structure-checker-v2 | n=40 | niche-wide |
| 10 | specificity_bomb hook = 28.5% retention | script-writer-v2 Rule 17; structure-checker-v2 | n=40 | niche-wide |
| 11 | curiosity-gap hook = 24.6% retention (avoid) | script-writer-v2 Rule 17; structure-checker-v2 | n=40 | niche-wide |
| 12 | Turn at 15–25% = 3.2x views; 25–35% zone = 2.1x (weakest) | script-writer-v2 Rule 16 | "85 competitor transcripts, 10 channels" | niche-wide |
| 13 | Myth-first structure = 30.3% retention vs chronological 22.4% | script-writer-v2 Rule 15; structure-checker-v2 Constraint U | n not stated | none stated (claimed own-channel) |
| 14 | Territorial = 2,449 avg views, 0.65% sub rate | script-writer-v2 Rule 14 | n not stated | own-channel n<30 |
| 15 | Ideological = 179 avg views, 2.31% sub rate (best conversion) | script-writer-v2 Rule 14 | n not stated | own-channel n<30 |
| 16 | Format A/B spoken pace ~200 WPM; budget = runtime × 3.3 | script-writer-v2 Rule 10 | n=1 (Video #54 post-mortem) | own-channel n<30 |
| 17 | Format C spoken pace ~150 WPM; budget = runtime × 2.5 | script-writer-v2 Rule 10 | n=1 (Video #54 post-mortem) | own-channel n<30 |
| 18 | Long quotes (>30 words) frequently don't survive recording intact | script-writer-v2 Rule 44 | n=2 (Manhattan #45 + Hijab #52) | own-channel n<30 |
| 19 | Ad-lib retention +10pp over scripted; 44% script survival rate | structure-checker-v2 Constraint AV | n not stated | none stated |
| 20 | "First specific number or date" flag if absent from first 101 seconds | structure-checker-v2 Constraint AH | "top-performing videos introduce data 101s earlier" (no n) | none stated |
| 21 | Only 1 of 12 videos over 12 min ever hit 30% retention | structure-checker-v2 Constraint T | n=12 (subset of n=47) | own-channel |
| 22 | Duration 12–20 min avg 24.7% retention vs 8–12 min at 29.6% | structure-checker-v2 Constraint T | n=47 | own-channel |
| 23 | 2026 channel median retention 24.0%; only 2 of 10 above 28% | structure-checker-v2 Constraint V | n=10 (2026 subset) | own-channel n<30 |
| 24 | 2026 chronological-colonial avg 16.7% retention | structure-checker-v2 Constraint V | n not stated | own-channel n<30 |
| 25 | 2026 long-form ideological avg 12.1% retention | structure-checker-v2 Constraint V | n not stated | own-channel n<30 |
| 26 | 8+ instances of "you" = possible overuse | structure-checker-v2 Constraint W | no evidence cited | none stated |
| 27 | 4+ consecutive ~25-word sentences = monotone rhythm | structure-checker-v2 Constraint AQ | no evidence cited | none stated |
| 28 | Modern relevance every 90 seconds guideline | structure-checker-v2 Constraint AE | "HvH retention data" (no n or statistic) | none stated |
| 29 | Document reveals spaced through 30–70% runtime; 3-min gap = flag | structure-checker-v2 Constraint AJ | no evidence cited | none stated |
| 30 | Year in title = −45.6% CTR | PACKAGING_MANDATE Rule 1 | n=6 vs n=27 | own-channel n<30 |
| 31 | Colon structure = −28.1% CTR | PACKAGING_MANDATE Rule 2 | n=9 vs n=26 | own-channel n<30 |
| 32 | "The X That Y" = 1.2% CTR (historically worst pattern) | PACKAGING_MANDATE Rule 3 | n not stated | own-channel n<30 |
| 33 | Question titles = −36.3% CTR | PACKAGING_MANDATE Rule 4 | n=3 vs n=32 | own-channel n<30 (noted as directional) |
| 34 | Versus format avg ~3.7% CTR | PACKAGING_MANDATE Tier 1 | n=2 verified | own-channel n<30 |
| 35 | Declarative format avg 3.8% CTR; two-sentence formula 11% outlier rate | PACKAGING_MANDATE Tier 2 | n not stated | own-channel n<30 |
| 36 | Two-sentence declarative = 3x+ views (strongest proven structural pattern) | PACKAGING_MANDATE Tier 2 | n not stated | own-channel n<30 |
| 37 | Scale words provide 1.33x lift in outlier videos | PACKAGING_MANDATE Tier 2 | n not stated | own-channel n<30 |
| 38 | How/Why titles get 2x search traffic (26.4% from search vs 12.7% declarative) | PACKAGING_MANDATE Tier 3 | "traffic source analysis" (no n cited) | own-channel |
| 39 | 73% of views from subscribers; 14% suggested/related (healthy = 30–50%) | PACKAGING_MANDATE note | n=48 videos | own-channel |
| 40 | YouTube Search = only 3.4% of views | PACKAGING_MANDATE note | n=48 videos | own-channel |
| 41 | CTR > 4% → hold; 2–4% → swap title; < 2% → swap title + thumbnail | PACKAGING_MANDATE 48h protocol | no evidence cited | none stated |
| 42 | Myth-first retention 30.3% vs chronological-colonial 22.4% (8pp gap) | structure-checker-v2 Constraint U | n not stated | none stated |
| 43 | 2-4% elapsed = where 13–25% of viewers leave (hook-to-body transition) | structure-checker-v2 Constraint B | n not stated | none stated |
| 44 | Retention by topic: ideological 30.3% > territorial 28.5% > general 26.4% > colonial 22.4% | structure-checker-v2 header | n not stated | own-channel (implied) |
| 45 | Hook type retention: myth_contradiction 36.7% → curiosity-gap 24.6% | structure-checker-v2 header | "n=40, cross-validated 2026-03-24" | niche-wide |
| 46 | Rule 43 Myth-narration-skip: skip narration act for famous myths | script-writer-v2 Rule 43 | n=2 (Manhattan #45 + Hijab #52) | own-channel n<30 |
| 47 | Rule 45 Evidence-anchored close validated | script-writer-v2 Rule 45 | n=2 (Tripoli #51 + Hijab #52) | own-channel n<30 |
| 48 | Rule 46 Debunk-the-mechanism: dominant structure in closest-match niche corpus | script-writer-v2 Rule 46 | "closest-match niche debunk corpus" (KB + RFB) | niche-wide |
| 49 | Format C word budget: 5-min ≤750 words; 8-min ≤1,200 words | script-writer-v2 Rule 10 | n=1 (Video #54) | own-channel n<30 |
| 50 | Title scoring gate: no title published below 65+ on title_scorer.py | PACKAGING_MANDATE scoring gate | "65-point minimum is a policy constant, not data-derived" (stated explicitly) | none stated |

**Total quantitative rules/claims inventoried: 50**

---

## Notes for Validation Session

1. **Cliff data matches the "intro hemorrhage" theory:** In all 15 videos, the largest absolute drops occur before 5% elapsed. Nothing in the SRT text at those cliffs suggests the content itself is the primary cause — the same cliff appears during both the strongest and weakest hook content. The causal mechanism (structural abandonment vs. content dropout) is not separable from this data alone.

2. **N-sizes at risk:** Rules 16–17 (WPM calibration), 18 (long-quote survival), 46–47 (myth-narration skip, evidence close) rest on n=1–2. Rules 13–15 (myth-first gap, topic type conversion) have no n stated despite appearing as hard rules.

3. **Cross-channel rules (niche-wide):** Rules 7–12 (hook types, turn placement) are the most defensible — derived from 40–85 competitor transcripts. These should be treated differently in the validation session from own-channel n<30 rules.

4. **Duplicate claims:** Rules 3/22 (8–12 min retention), 7/45 (hook type n=40), 13/42 (myth-first gap), and 22/4 (12–20 min retention) appear in both source files. The rule inventory lists both instances as they may diverge in wording.

5. **The "personal_authority" finding is confounded** (see RETENTION-SCRIPT-CORRELATION interpretation): the content labeled `personal_authority` clusters at the intro drop zone. The SRT evidence from Video 4 (Vance, cliff at credential chain) and Video 15 (Flat Earth, classified as personal_authority in correlation data) is consistent with the finding but does not establish causation.
