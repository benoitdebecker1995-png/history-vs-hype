# Cold-open craft scan — 2026-07-22

**Hypothesis generation, not a model.** Ten videos, far below this channel's n≥30 threshold. Nothing here is a finding; every item is a swap that could be tested. Analysis by Codex (GPT-5.x) from `channel-data/CHANNEL-PERFORMANCE-DATA-2026-06.md`; CTR layer and re-scoping added by the main thread from `analytics.db`.

---

## ⚠ Read this before the craft section — the opener is probably not the binding constraint

The scan ranked ten videos by retention at 0:30 and asked what the best three do that the worst three don't. That question is only worth asking about videos people actually clicked. **They mostly didn't.**

Click data exists in **two** places, neither of them the markdown export (where `ctr_percent` and `impressions` are zero for all 58 videos — the reason the original scan reported "no usable CTR data"):

- **`tools/discovery/keywords.db` → `ctr_snapshots`** — 1,171 rows, latest **2026-07-13**, lifetime `impression_count` + `ctr_percent` per video, weekly Monday refresh via `tools.youtube_analytics.ctr_tracker`. **This is the authoritative live source.**
- **`analytics.db` → `surface_ctr`** — 56 rows, browse vs suggested split. Useful for *where* the clicks come from, but its impression totals disagree with `ctr_snapshots` (different pull windows), so don't mix the two in one number.

| video | views | browse impr | browse CTR | sugg impr | sugg CTR | opener rank |
|---|---:|---:|---:|---:|---:|---:|
| #57 Piri Reis | 155 | 1,414 | **6.72%** | 1,496 | 1.40% | 3 |
| #54 Inquisition | 53 | 50 | 4.00% | 1,570 | 0.76% | 9 |
| #50 Thermopylae | 80 | 1,593 | 2.95% | 739 | 0.95% | 6 |
| #56 slave trade | 87 | 516 | 2.52% | 1,845 | 1.68% | 4 |
| #43 India–Pakistan | 124 | **11** | *36.36%* | 2,627 | 1.33% | 8 |
| #45 Manhattan | 18 | 108 | **0.93%** | 1,342 | 0.52% | 7 |

Channel-wide: browse CTR median **4.30%**, and **33 of 56 videos got under 500 browse impressions.**

**Three consequences for how to read the craft section below.**

1. **#45 Manhattan is not an opener problem.** It sits mid-table on opener retention (55.6%) and has the worst click-through in the set — 0.93% browse, 0.52% suggested, on ~1,450 impressions. Rewriting its cold open cannot fix a video almost nobody opens. It is a title/thumbnail job.
2. **#43's 36.36% browse CTR is noise, not a triumph** — it is 4 clicks on 11 impressions. Its real signal is 2,627 suggested impressions converting at 1.33%. The scan ranked it a bottom-three opener; the click data says its problem is upstream of the opener too.
3. **#57 Piri Reis is the only unambiguous winner here** — best browse CTR in the set *and* third-best opener retention. It is clicked and it is held. If any video in this set is worth copying, it is this one, and for both halves of the funnel.

This is the channel's already-documented shape (views↔retention r=0.07, views↔CTR r=0.62, 27/56 dying not-clicked) showing up again. **Treat everything below as craft worth testing when a video is getting impressions — not as an explanation of why these ten underperformed.**

---

## The craft observations (Codex, unedited in substance)

Ranked by retention at 0:30: #44 Bakassi 78.8% · #51 Tripoli 70.7% · #57 Piri Reis 67.1% · #56 slave trade 63.4% · #52 Veil 63.0% · #50 Thermopylae 56.0% · #45 Manhattan 55.6% · #43 India–Pakistan 51.4% · #54 Inquisition 48.6% · #41 Tordesillas 47.3%. ⚠ #44's 78.8% comes from 18 views — ignore it.

**1. The best make one unresolved document conflict legible before explaining the subject.** Tripoli: a named scholar reads a specific Arabic treaty and the State Department cannot explain what he found. Piri Reis: the decisive evidence is a paragraph physically visible on the map that almost nobody has read. Bakassi: one legible treaty paradox — protection versus ownership.

The weaker three have equally good evidence and reach its cleanest form later. #54 establishes the familiar Inquisition stereotype before Paragraph Fifteen. #43 describes Ferozepore densely before delivering the two-word order "Eliminate salient." #41 opens on an economics paper, census figures and an unexplained "different empire" before the treaty line.

**The difference is not "proof first"** — that formula already failed out of sample on this channel. It is **how fast the viewer can name the unresolved problem.**

**2. The best give one object and one contradiction.** The weaker openers ask the ear to hold several unfamiliar elements at once — #43 carries date, draft map, Viceroy, Punjab governor, Ferozepore, religious majority, canal headworks and irrigation stakes before the payload. **Specificity helps only when the details converge on one question; a specificity pile is still setup.**

**3. The best immediately resemble the promise that earned the click.** #41 is the clearest negative: packaging promised two countries splitting a continent they had never mapped, and the opener began with a 2023 economics study and Brazilian census numbers.

---

## Ranked swaps, each single-variable

**1. Put the packaged artifact and its contradiction in the first sentence.** Cheapest possible change — reorder existing verified lines, add no claims. Candidates: #54 open on Paragraph Fifteen and the loophole, then the myth · #43 open on "Eliminate salient," then the map · #41 open on the treaty line splitting unmapped territory, then the modern measurement.
*Falsified if* the reorder doesn't improve 0:15–0:30 under a sufficiently exposed native test, **or** if it improves entry but creates a new drop when the postponed context arrives.

**2. Strip secondary names and numbers from the first 90 words.** One object, one consequential fact, one open question; supporting figures move to the next beat. Clearest candidate #43.
*Falsified if* early abandonment doesn't fall, or if comments show the removed specificity was the credibility hook.

**3. Replace generic myth setup with the script's unique mechanism.** #54's "Everyone thinks they know…" is accurate and could open almost any Inquisition video; its exclusive asset is a procedural manual whose rule and loophole sit in the same paragraph. Same material, reversed order.
*Falsified if* mechanism-first loses viewers faster — i.e. the audience needed the stereotype as orientation before the document meant anything.

⚠ **Run these only on videos that get impressions.** On #45 and #43 the swap is untestable as written, because the retention signal is built on 18 and 124 views.

---

## Bottom line

> Early retention may improve when the opener makes one unresolved document conflict immediately legible and visibly delivers the packaging promise.

Not a wording formula — a description of the viewer's state: they know what object they are looking at, why it is strange, and what question the video will settle.

## Side findings

- **CTR source order: `keywords.db → ctr_snapshots` first** (live, weekly, lifetime), `analytics.db → surface_ctr` for the browse-vs-suggested split. Never `videos.ctr_percent` (zero for all 58) and never the markdown export. Two independent analyses have now concluded "the channel has no CTR data" from that empty export.
- **⚠ #59 is the loudest packaging signal on the channel and it is not in this scan.** `OHWq4jY8iAY`, published 2026-07-05: **21,498 lifetime impressions at 1.48% CTR, 283 views.** YouTube pushed it roughly forty times harder than anything else in this set and almost nobody clicked. Every other video here is starved of impressions; #59 got them and converted at a third of the channel's browse median. It is the pilot of the claims-on-trial series, so this is worth a dedicated look before the next episode is packaged — and it is a title/thumbnail question, not an opener one.
- **#59's `PROJECT-STATUS.md` still says "not published."** The scan excluded it on that basis — correctly by luck, since it postdates the retention export. Worth a `/reconcile`.
