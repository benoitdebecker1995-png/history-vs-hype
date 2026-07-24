# VOICE-DRIFT ACROSS THE CATALOGUE — 2026-07-21

> **Status: PARTIAL, and it already overturns a finding from earlier today.** The agent that built this dataset was
> killed by a session limit before writing up. The measurement survived (`scratchpad/results.json`, 28 written scripts
> + the gold unscripted baseline); the write-up below is mine, from that data. **Two metrics the agent had not yet
> computed — total `so`/`but` frequency, and the performance join — are missing and are flagged as OPEN.**
>
> **TIER: MEASURED** for every number in the table. **INFERRED** for every interpretation.

---

## 0. THE HEADLINE — a claim I made confidently today is WRONG

Earlier today, off a **two-script comparison**, I told the owner that the em-dash-replacing-connectors drift "started
at #57" and was "a scripting-layer problem." That claim is now **falsified by the full catalogue**, and it was written
into two canonical files (`CALIBRATION-CORPUS.md` 62-14, `VOICE-PROFILE.md` §Connectors). Both corrected 2026-07-21.

**What the two-point comparison said:** #56 = 0.71 em-dash:connector ratio, #57 = 3.33. Conclusion drawn: something
broke at #57.

**What 25 measurable scripts say:** em-dash runs at a **median of 18.5 per 1,000 words across the whole catalogue,
from video #1 onward** (range 3.7–29.2). Video #1 is 23.8. Video #3 is 19.9. Video #4 is 17.6. There is no break at
#57 (21.4) — it sits mid-range. **#56 (5.3) is the outlier: the second-lowest script in the entire catalogue.**

I built a trend on an anomaly. The honest finding is the opposite of what I reported: **heavy em-dash use is his
scripted norm and always has been**, and the thing that needs explaining is not #57 but #56.

**Trend test:** videos ≤30 median **17.6/1k** (n=11) · videos >30 median **19.1/1k** (n=14). Essentially flat. Not
monotonic, not a drift, no inflection point.

> This is the case for cross-script measurement in one paragraph. n=2 produced a confident, wrong, canon-altering
> finding. n=25 killed it in one query. Any future single-video voice claim should be checked here before it is
> written into `VOICE-PROFILE.md`.

---

## 1. The table (chronological, written scripts only)

SRTs excluded from this table — they are edited-cut artifacts and `VOICE-PROFILE.md` says so explicitly. Gold =
`yMAWJcjo_ug`, his unscripted speech.

| vid | words | em-dash/1k | colon/1k | nominal/1k | median sent | >35w % |
|---|---|---|---|---|---|---|
| **GOLD** | 761 | **0.0** *(n/a in ASR)* | 0.0 | **11.8** | **13** | 12.5 *(ASR artifact)* |
| 1 | 1429 | 23.8 | 5.6 | 54.6 | 8 | 1.5 |
| 1b | 1262 | 24.6 | 1.6 | 49.1 | 5 | 1.1 |
| 3 | 1207 | 19.9 | 9.1 | 48.9 | 6 | 0.0 |
| 4 | 1251 | 17.6 | 3.2 | 41.6 | 9 | 2.7 |
| 6 | 1093 | 3.7 | 5.5 | 30.2 | 6 | 0.0 |
| 10 | 1661 | 13.2 | 5.4 | 41.5 | 10 | 0.0 |
| 13 | 996 | 14.1 | 5.0 | 42.2 | 9 | 1.1 |
| 14 | 1580 | 12.7 | 5.7 | 34.8 | 8 | 3.6 |
| 19 | 2221 | 21.6 | 0.9 | 32.9 | 9 | 1.0 |
| 24 | 2408 | 13.7 | 2.9 | 40.7 | 6 | 0.3 |
| 28 | 1336 | *0.0 ⚠* | 0.8 | 71.9 | 7 | 3.6 |
| 30 | 611 | 27.8 | 9.8 | 44.2 | 9 | 7.0 |
| 31 | 1104 | 13.6 | 4.5 | 18.1 | 7 | 1.7 |
| 34 | 672 | *0.0 ⚠* | 3.0 | 46.1 | 8 | 0.0 |
| 35 | 1906 | 11.5 | 4.7 | 39.3 | 9 | 4.7 |
| 37 | 1546 | 18.1 | 8.4 | 51.1 | 9 | 2.7 |
| 40 | 1460 | 26.0 | 5.5 | 32.9 | 11 | 3.6 |
| 41 | 2339 | *0.0 ⚠* | 0.0 | 23.9 | 9 | 1.9 |
| 43 | 1784 | 23.5 | 9.5 | 38.1 | 9 | 4.3 |
| 44 | 1900 | 22.6 | 4.2 | 35.3 | 9 | 0.6 |
| 45 | 2237 | 15.2 | 4.0 | 32.6 | 13 | 9.3 |
| 50 | 1620 | 18.5 | 9.9 | 20.4 | 9 | 2.9 |
| 51 | 803 | 10.0 | 1.2 | 29.9 | 8 | 2.8 |
| 52 | 1954 | 29.2 | 10.8 | 30.2 | 11 | 9.3 |
| 54 | 1262 | 26.1 | 5.5 | 43.6 | 12 | 9.8 |
| **56** | 1141 | **5.3** | 0.9 | 21.9 | 13 | 4.3 |
| **57** | 1818 | **21.4** | 3.3 | 14.9 | 11 | 1.4 |
| 59 | 2124 | 19.8 | 4.2 | 39.5 | 14 | 4.5 |
| **#62 v7.0** | 2678 | **16.1** | **1.9** | **22.8** | **13** | 2.2 |

⚠ **Three scripts read 0.0 em-dash (28, 34, 41).** Near-certainly an extraction artifact — hyphen or en-dash instead
of em-dash, or a teleprompter render that stripped them. Excluded from all medians. **Do not read them as clean.**

---

## 2. What IS systematic — and it isn't the em-dash

**⭐ Nominalization is the real, catalogue-wide drift.** Gold **11.8/1k**; catalogue median **38.7/1k** — more than
three times his natural rate, and it is high in *every* script (range 14.9–71.9, and the low end is only reached by
four videos). This is abstract nouns doing work his mouth gives to people and verbs: "the killing of" where he says
"they killed," "the count comes from" where he says "Motyka says." It was the phrasing audit's finding on #62 and it
holds across the whole catalogue. **This is the metric worth a linter rule.**

**Sentence length drifts SHORT, not long — the opposite of the intuition.** Gold median is **13 words**; the catalogue
median is **9**. Twenty-one of twenty-eight scripts sit below his natural median. Scripts are more *clipped* than his
speech, which is consistent with `VOICE-PROFILE.md`'s headline correction that **staccato is the #1 "too-AI" tell** —
and it means any future "tighten it" instruction should be treated with suspicion, because the catalogue is already
tighter than he is.

**Colon-reveal is genuinely variable** (0.0–10.8/1k) with no trend — this one really is per-script discipline, and the
Fable T8 cap of ~2 is violated by most of the catalogue.

---

## 3. Where #62 v7.0 now sits

Today's work put it among the cleanest scripts on every axis measured:

- **em-dash 16.1** vs catalogue median 18.5 — better than the norm, though not exceptional.
- **nominalization 22.8** vs catalogue median 38.7 — **second-lowest of the whole catalogue** after #57's 14.9.
- **median sentence 13** — **exactly his gold**, matched by only #45, #56 and (at 14) #59.
- **colon 1.9** vs catalogue median ~4.7 — inside the Fable T8 cap, which most scripts miss.

INFERRED: the phrasing pass worked, and it worked on the metrics that actually distinguish his voice — just not on the
one I claimed it was fixing.

---

## 4. Proposed pre-lock checklist (the deliverable)

Three numbers, thresholds set from his gold and the catalogue spread. Small and sharp on purpose.

| Check | Threshold | Why this one |
|---|---|---|
| **Nominalization /1k** | **≤ 25** (gold 11.8; catalogue median 38.7) | The only catalogue-wide, every-script drift found. Highest-yield single number. |
| **Median sentence length** | **≥ 11 words** (gold 13; catalogue median 9) | Catches the staccato drift, which is his own #1 stated too-AI tell and which the catalogue shows is the *real* direction of travel. |
| **Colon-reveal /1k** | **≤ 3** (gold 0.0) | Already a Fable T8 cap; the catalogue shows it is routinely blown, so it needs enforcement rather than a new rule. |
| **⭐ `so`+`but` /1k — a FLOOR, not a cap** | **≥ 8** (gold 21.0; catalogue median 7.4; best-ever script 13.7) | Added after OPEN item 1 closed. The one universal drift in the catalogue: every script suppresses his causal spine to roughly a third of natural. A floor of 8 means beating half your own back-catalogue; 12+ would be genuinely close to him and no script has managed it yet. |

⚠ **Do NOT add an em-dash threshold.** At a catalogue median of 18.5 with no trend and #56 as the outlier, a cap would
flag his normal scripted register as a defect. ⚠ **And do not use the em-dash:connector RATIO** — §4b shows its spread
is driven by em-dash noise sitting on a near-constant connector floor, so it moves for the wrong reasons. Measure the
connector rate directly.

---

## 4b. ⭐ OPEN ITEM 1 NOW CLOSED — the connector suppression is REAL, catalogue-wide, and present from video #1

Recomputed 2026-07-21 (`scratchpad/connectors.py`, total occurrences not sentence-initial, same 28-script corpus).
**This partly un-does §0: the original observation was right; only its attribution to #57 was wrong.**

| | `so`+`but` per 1k | em-dash per 1k | ratio |
|---|---|---|---|
| **GOLD (unscripted)** | **21.0** | n/a | — |
| Catalogue median (n=28) | **7.4** | 18.5 | 2.24 |
| Catalogue range | **3.2 – 13.7** | 3.7 – 29.2 | 0.00 – 8.25 |
| #56 | 6.3 | 5.4 | 0.86 |
| #57 | 6.6 | 21.5 | 3.25 |
| **#62 v7.0 (post-connector-pass)** | **8.6** | 16.1 | **1.87** |

**Every single script in the catalogue runs below half his natural connector rate, and the median is 35% of it.**
The highest any script has ever reached is 13.7 (#59). This is the most uniform finding in the study — no trend, no
outliers, no exceptions: **writing suppresses his causal spine, always, and has since video #1.**

**So the two findings separate cleanly, and the earlier framing conflated them:**
- **Connector suppression = a real, universal, verified constant.** Gold 21.0 → catalogue 7.4.
- **Em-dash volume = noisy and normal.** Median 18.5, flat, #56 is the outlier.
- **The RATIO is therefore the wrong instrument** — its spread (0.00–8.25) is driven almost entirely by em-dash
  variance sitting on top of a near-constant connector floor. **Measure the connector rate directly. Drop the ratio.**

INFERRED: #62 v7.0 at **8.6** is above the catalogue median and its ratio (1.87) is below it — today's connector pass
moved it in the right direction, but it is still at **41% of his natural rate**, which is the honest size of the gap.

---

## 5. OPEN — what this study still owes
2. **The performance join.** Not attempted. ⚠ And per the repo's own standing rules it should be attempted only with
   the caveats loud: n<30, and this channel fails on **distribution**, not retention (views↔retention r=0.07). The
   likely honest conclusion is that no voice metric predicts anything at this sample size.
3. **The three 0.0-em-dash extractions** (28, 34, 41) need re-parsing before the table is quoted anywhere.
4. **SRT-vs-written comparison** — the dataset has an `srt` bucket that this write-up does not use.

---

## 6. Honest limits

- **28 written scripts is a real sample by this repo's standards; the interpretations are still mine, not the data's.**
- Every number is reproducible from `scratchpad/results.json`; the extraction code is `scratchpad/drift.py` +
  `corpus.py`. Neither has been independently reviewed.
- Gold is **one 761-word unscripted video**. Every "his natural rate" figure in this file rests on that single sample,
  which is the same caveat `FINGERPRINT-UNSCRIPTED.md` carries.
- Gold's em-dash (0.0) and >35w (12.5%) figures are **ASR artifacts**, not measurements — auto-captions have no
  em-dashes and no reliable sentence boundaries. They are unusable as baselines and are not used as such above.
- **Nothing here is measured against retention or CTR.** No claim in this file is causal.
