# Breakout Mechanics — why one video broke out and nine mimics didn't

**Date:** 2026-07-28
**Method:** `analytics.db` — `studio_ctr_rows` (Studio export, 2026-07-23, lifetime, authoritative),
`surface_ctr` (browse/suggested split), `traffic_sources`, `thumbnail_features`; plus
`keywords.db.ctr_snapshots` (1,287 rows, 2026-02→07). All long-form (>180s), n=56.
**Trigger:** creator: *"I want to find the next breakout video. I tried mimicking the Guatemala Belize
video a couple of times but it didn't work."*

> ⚠ **`videos.impressions` is garbage** (shows 5,611 views on 1,558 impressions). Every impression
> figure here comes from `studio_ctr_rows` or `surface_ctr`. Do not use `videos.impressions`.

---

## 1. The thing that actually varies is the SERVE, not the click

63.5% of every browse impression in channel history went to one video. **15 of 56 long-form videos
were ever served ≥2,000 browse impressions. 41 were never meaningfully tested.**

Search is irrelevant to this channel: 4.4% of the breakout's traffic, 1–8% everywhere else. This
channel gets home-feed traffic or it gets nothing. **Optimising search anchors is optimising ~5% of
the funnel.**

⚠ Note on the API: `traffic_sources.source_type = 'SUBSCRIBER'` does **not** mean subscriber views —
it maps to Studio's **Browse features**. 23,858 "subscriber" views on a 527-sub channel is the tell.

## 2. Escalation tiers, and the two anomalies that break the simple theory

| tier | n | videos |
|---|---|---|
| **A — 100k+** | 1 | Guatemala vs Belize (292,398 imp, 7.66%) |
| **B — 15–100k** | 4 | Guatemala-ICJ (44k, 9.18%) · Venezuela/Guyana (36k, 4.30%) · Turkey/Greece (22k, 3.20%) · Brazil (20k, 3.12%) |
| **C — 5–15k** | 9 | incl. JD Vance (10.0k, **9.41%**) · Israel/Palestine 2026 (21k rolling, **1.59%**) |
| **D — 1.5–5k** | 20 | incl. KGB (4.8k, **7.90%**) |
| **E — <1.5k** | 17 | never tested |

**Anomaly 1 — high CTR does not buy escalation.** KGB hit **7.90%** and got 4,760 impressions (tier D).
JD Vance hit **9.41%** and got 9,969 (tier C). Both out-clicked Guatemala's 7.66% and got 30–60× fewer
impressions.

**Anomaly 2 — mediocre CTR can still be escalated.** Brazil got 19,894 impressions at **3.12%** (tier B),
four times KGB's serve on less than half the CTR.

→ **CTR does not determine the serve.** Something upstream does.

## 3. The two-factor model — ⚠ DESCRIPTIVE ONLY, see §5b

> ⚠ **This model describes the outcomes but it is NOT predictive.** "Topic pool" fits every data point
> retrospectively and **cannot be measured before publishing** — four attempts failed (§5b). Treat this
> section as a way of *sorting past failures*, never as a way of picking the next video.

```
    serve size   ≈  how big an audience YouTube has to show it to   (TOPIC POOL)
    views        ≈  serve size  ×  CTR                              (PACKAGING)
    escalation   ≈  both, and it needs both
```

Every video on the channel fails on one axis or the other — except one:

| | large topic pool | small topic pool |
|---|---|---|
| **CTR ≥7%** | ✅ **Guatemala** — 292k × 7.66% = 30,416 views | ❌ **KGB** 4.8k×7.9% · **JD Vance** 10k×9.41% — great packaging, nobody to show it to |
| **CTR <4%** | ❌ **Brazil** 20k×3.12% · **Turkey/Greece** 22k×3.2% · **Israel/Palestine** 21k×1.59% — got the shot, missed | ❌ **Bir Tawil · Nigeria/Cameroon · Honduras · Mexico's island · Thailand/Cambodia · Gibraltar** — dead on both |

**This is why mimicking failed, and the two failures are different failures:**
- **Bir Tawil (2.5k), Nigeria/Cameroon (369), Honduras (138), Mexico's island (459), Thailand/Cambodia
  (807), Gibraltar (2.3k)** — copied the *format*, picked topics with no browse pool. Perfect packaging
  could not have saved a 369-impression test.
- **Turkey/Greece (22k @ 3.2%), China/Taiwan (7.3k @ 2.71%), Brazil (20k @ 3.12%), Berlin (9.5k @ 3.66%)**
  — the pool was there and YouTube served them. **They lost at the click.**

And the cleanest single case: **Israel/Palestine (published 2026-07-05) was served 21,498 impressions in
its first week — a genuine shot — and converted at 1.59%.** That video got what Guatemala got, in
miniature, and the packaging wasted it.

## 4. What does NOT explain it — three dead ends, killed here

1. **Copying the winner's format.** The direct sequel (*What 3 ICJ Cases Show*) beat the original on
   **browse CTR (9.83 vs 8.44)** *and* **retention (38.5 vs 35.4)** and got **7.6× fewer impressions**.
   Packaging was never the missing ingredient in that pair. A sequel also competes for the same slot and
   the same viewers — the pool had already been served.
2. **Retention.** Turkey/Greece (39.1%) and Guatemala-ICJ (38.5%) both beat Guatemala (35.4%). Neither
   escalated. Retention is not the escalation trigger.
3. **Thumbnail feature tags.** `thumbnail_features` cannot explain the gap: **Guatemala and "Britain Drew
   the India–Pakistan Border" carry identical tags (map=1, red=1) and score 7.66% vs 1.61% CTR.**
   One real filter does survive — **no video with a creator face (`cf=1`) has ever cleared 4%** (max 3.83%,
   n=8; all eight >4% videos are `cf=0`) — but it is **necessary, not sufficient**: the 2026 cohort is
   mostly faceless and still tops out at 4.06%.

## 5. The 2026 problem, stated precisely

Medians are flat (2025: 2.94% · 2026: 2.60%). **The ceiling is what disappeared.**

- 2025: **7 of 22** videos cleared 4% CTR. Three cleared 7.6%.
- 2026: **1 of 12** cleared 4% (Somaliland, 4.06%). **Nothing has cleared 4.1% all year.**

Escalation appears to need ~4% to move up a tier and ~7%+ to move up two. The channel has not built a
≥7% thumbnail since **JD Vance (2025-11-04)**.

## 5b. 🛑 FOUR PREDICTORS TESTED 2026-07-28. ALL FOUR FAILED. Gate 1 below is WITHDRAWN.

I tried to build a pre-publish pool metric. Every attempt died. Recording them so nobody rebuilds them:

| attempted predictor | instrument | result |
|---|---|---|
| Topic interest = small channels doing big views | `vidiq_outliers(keyword=…)` | ❌ **Measures the wrong thing.** `belize` returns travel vlogs, resort tours and hip-hop. A bare topic keyword measures interest in a *place*, not in the dispute. |
| Peer coverage in the overlapping audience | `intel.db`, 1,801 videos / 20 peer channels, `outlier_ratio` | ❌ **No discriminating power — and it vetoes the winner.** **Guatemala/Belize has ZERO peer coverage.** So does Turkey/Greece. So do all five dead topics. The breakout sits in the same bucket as the failures. |
| Channel-level algorithmic state (was the channel demoted after the hit?) | serve size by publish month | ❌ **No.** Median serve is flat: pre-Oct-2025 **2,889** · Oct–Dec 2025 **3,478** · 2026 **2,258**. |
| Topic type | `videos.topic_type` | ❌ territorial median is **155 views**; 16 of 21 under 500. |

**And the decisive observation:** in **October 2025** the median video got **1,573** impressions and one got
**292,398** — a **186× spread inside a single month, on the same channel.**

→ 🛑 **Gate 1 as written in §6 is WITHDRAWN.** "If nothing on the topic clears 50k from anyone, don't make
it" would have killed Guatemala/Belize, the channel's only breakout, which no peer had ever covered.
**Do not apply it.**

→ **Honest state of knowledge: with the data available, the escalation event is not predictable.** Every
measurable predictor — CTR, retention, thumbnail features, peer coverage, search volume, channel state,
topic type — has been eliminated. Anyone offering a breakout formula from this dataset is guessing.

## 6. What to do — REVISED, and it is a portfolio answer not a picking answer

Since the winner cannot be picked, the only rational strategy is to **buy more tickets and stop wasting
the ones that win.** Two controllables, in priority order:

**1. NEVER WASTE A SERVE.** This is the only loss category that is unambiguously the channel's own fault
and unambiguously fixable. **Israel/Palestine was served 21,498 impressions in week one and converted at
1.59%.** Brazil got 19,894 at 3.12%. Turkey/Greece 22,034 at 3.20%. Those three serves, converted at
Guatemala's 7.66%, would have been ~4,800 views instead of ~2,060.
- The bar is **~4% to move up a tier, ~7% to move up two.**
- **2026 has cleared 4% once in twelve videos** (Somaliland 4.06%). No ≥7% thumbnail since JD Vance,
  2025-11-04.
- **Study the four images that cleared 7%** — Guatemala ×2, JD Vance, KGB — not the title formats.
  Feature tags cannot do this for you (Guatemala and India–Pakistan share map+red: 7.66% vs 1.61%),
  so it has to be a visual comparison.

**2. MORE SHOTS, CHEAPER.** A 186× serve spread with no predictable cause is a lottery, and the response
to a lottery is ticket volume — not a bigger bet per ticket. #55 currently carries **50 claims and five
research passes**. That is an enormous stake on one draw. The channel already has **five script-ready
videos** and a stated production (not research) bottleneck — shipping those is strictly better than
deepening one dossier.

**3. INSTRUMENT THE LAUNCHES — the one thing that converts this from guessing to knowing.**
`ctr_snapshots` begins 2026-02-23, so **not a single launch push in channel history is observable.** Snapshot
impressions + CTR **weekly from publish day**. After 6–8 videos there is a real launch-window dataset and
the escalation question becomes testable instead of speculative. **Start with #62 Volhynia.**

**And keep the two failure modes apart.** "It didn't work" has meant *never served* (41 of 56 videos) far
more often than *served and not clicked* (4 videos). Only the second is a packaging problem.

## 7. Open questions this data cannot answer

- **What made Guatemala's pool so large?** n=1. The only structural difference I can find is that every
  other video asks the viewer to already care about a named dispute, while Guatemala asked nothing —
  *a country might disappear*, legible to a stranger with zero prior knowledge. **That is a hypothesis
  from one data point, not a finding.**
- **Was Guatemala's push immediate or delayed?** Unanswerable — `ctr_snapshots` begins 2026-02-23, four
  months after it published. From Feb→Jul it added only ~1,570 views, so the push was long over. **To
  answer this for future videos, snapshot weekly from day one.**
- **Causation on any thumbnail rule** — needs native Test & Compare per-variant CTR, not lifetime CTR.

## 8. Consequences for #55 Falklands (greenlight passed 2026-07-28)

Gate 1 is genuinely uncertain and the earlier read was too optimistic. The "open distribution window"
recorded on 2026-07-25 was a **football-controversy window** (World Cup banner row, 16–24 July):
the 1.12M video was a banner reaction; the fan-clash clips did 36k/18k/12k. **The substantive sovereignty
video published into that same window by a 7,830-sub GB channel — "Britain's Falklands Oil Is Worth
£3 Billion" — got 1,454 views.** Falkland Islands TV gets ~1,500. Topic velocity has decayed under
10 views/hour.

→ **Falklands passes Gate 1 for football reaction content and probably not for an 11-minute document
video.** Ship #55 as a solid channel video — the research is the best on the channel and the packaging
lock is valid — but **do not file it as the breakout attempt.**


---

## 9. The five images that cleared 5% — visual comparison (2026-07-28)

Feature *tags* can't explain CTR (§4.3). So I pulled the actual images and looked at them.
**Winners:** JD Vance 9.41% · Guatemala-ICJ 9.18% · KGB 7.90% · Guatemala-1 7.66% · Crusades 5.47%.
**Losers (≥3,000 impressions):** Medieval Literacy 1.11% · India–Pakistan 1.61% · South China Sea 1.78%.

### What actually separates them — four differences, all executable

**1. FILL, NOT LINE. This is the biggest single difference.**
Both Guatemala thumbnails are large flat colour areas — solid green country, solid red contested strip,
readable as a *shape* at any size. The two map losers use fine linework: India–Pakistan is a sepia
archival map with hairline district borders and ~6pt place names; South China Sea is a dark satellite
map with a thin red dashed line. **At feed size the winners are shapes and the losers are grey mush.**
→ Rule: a map must read as **two or three flat blocks of colour**. If it has legible place names, it has
too much detail.

**2. THE SUBJECT IS INSTANTLY RECOGNISABLE — OR THERE IS NO SUBJECT.**
Winners show JD Vance (globally recognisable), Arafat + a Soviet officer (recognisable), or **no person
at all** (both Guatemalas). Losers show Cyril Radcliffe (a stranger in glasses) and **the creator's own
face** (the single worst performer, 1.11%).
→ Rule: famous face, or no face. **A photograph of an unknown person is worse than no photograph.**

**3. TWO TEXT REGISTERS, TOP AND BOTTOM — subject on top, stake underneath in yellow.**
- Guatemala-1: `GUATEMALA VS BELIZE` (top, black on white outline) + `BORDER ON TRIAL` (bottom, yellow)
- Guatemala-ICJ: `ICJ 2027` (top) + `3 CASES ANALYZED` (yellow)
- JD Vance: `3 HISTORICAL CLAIMS / FACT CHECKED`
- KGB: `KGB EXPOSED` + a red `CLASSIFIED` stamp
Every winner uses **heavy sans with a thick contrasting outline**. The 1.78% loser puts a single thin,
un-outlined white word (`ILLEGAL`) centred over a dark map — it vanishes.
→ Rule: heavy weight, thick outline, 2–4 words per line, top and/or bottom. **Never thin. Never centred
over detail.**

**4. ONE OR TWO FOCAL OBJECTS. NOT FOUR.**
Winners: map+text, or two faces+stamp. The 1.11% loser carries stained glass + a village illustration +
the creator's face + three lines of text + an exclamation mark.
→ Rule: if you can name more than two things in the image, cut one.

### What this means for #62 Volhynia (in edit now)
Fits the winner pattern: **clean two-fill map** (the Volhynia region as one solid block against Poland
and Ukraine), **no face**, two text registers — subject on top, stake in yellow beneath. **Do not make
the document the hero** — document-as-focal-point is the channel's CTR floor (−0.71 overall, −2.11 on
famous topics), and the untranslated page belongs *inside* the video, not on the thumbnail.

### Next-video fit on the same test
- **#58 Kurdistan** — `kurdistan map` is the top keyword (**4,414/mo, VidIQ 64, competition 16.4** — the
  lowest of any candidate). People are literally searching for the map, and a 4-country flat-fill map is
  the exact winner treatment. **Script locked, awaiting camera.**
- **#36 Panama Canal** — `panama canal history` **8,995/mo, VidIQ 63**; globally recognisable name and an
  iconic shape. Fact-checked, script exists. ⚠ Its "topicality 100" rating was web-verified **2026-06-11**
  and is now ~7 weeks old — **re-verify the live legal drama before counting the hook.**
