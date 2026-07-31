# NEXT-VIDEO CANDIDATES — first gap-hunter run

**Date:** 2026-07-29
**Method:** `channel-data/NEXT-VIDEO-DISCOVERY-HANDOFF.md` §5, Stages 1–4, executed end to end.
**Store:** `intel.db.comment_signals` (3,343 rows) · view: `channel-data/gap-hunter/HARVEST-DIGEST.md`

## How to execute this doc

Read §4. If you agree with the recommendation, run `/greenlight` on the recommended candidate.
Nothing here is locked — §4 explains exactly why not.

---

## 1. What was swept

170 videos across 15 tracked competitor channels, **33,532 comments**, **3,343 tagged signals**
(unmet-supply / pocket / repeated-question). Roughly 20× the corpus that found the Panama pocket.

**Finding about the instrument, not the topics:** the tracked competitor set is misaligned with this
channel's lane. Metatron, ReligionForBreakfast and Alex O'Connor produced 1,397 of the 3,343 signals —
antiquity and religion, not treaties and borders. Only 61 signals in the whole corpus contain
treaty/border/court/referendum vocabulary. **The harvest is thinner in our lane than the raw count
suggests.** Fix before the next run: add CaspianReport, Geopolitics Explained, Casual Scholar,
Atun-Shei, and TLDR-style law/border channels to `tools/intel/competitor_channels.json`, then re-sync.

---

## 2. The two candidates that survived all four stages

Both pass **G0 identity** and **G1 demand floor**. Data collected symmetrically per TOPIC-RUBRIC rule 3.

### A — West Papua: the 1969 "Act of Free Choice"

**The claim on screen:** the UN supervised a self-determination vote in which Indonesia selected
**1,025 men** to speak for a population of roughly 800,000, and the General Assembly then "took note"
of the result in Resolution 2504 — which remains the legal basis for Indonesian sovereignty today.

| stage | evidence |
|---|---|
| **Demand** (S1) | Pocket comments under RealLifeLore's New Guinea video — *"As an Indonesian… the government restricts access to avoid international scrutiny. Papua… has been exploited heavily"* (2,774 likes) · *"As a West Papuan I appreciate your take on my homeland"* (204) · a Papua New Guinean voice in the same thread. The comments arrived under a video about **geology and mining** — the audience showed up for a question the video wasn't answering. |
| **Supply** (S3) | `channel-data/serp-studies/titles/west-papua-act-free-choice-2026-07-29.md` — top 12 is **Al Jazeera (74,070), SBS, ABC News, and four uploads by the West Papua advocacy org itself**. Zero explainer channels. Evidence-promise 0/12. Two-sentence Claim.Evidence. 0/12. **No quality English long-form exists.** |
| **Identity** (S4) | Documents are showable: New York Agreement 1962 (UNTS), UN doc **A/7723** — Ortiz-Sanz's own report on how the act was conducted — and GA Res 2504. Matters in 10 years regardless of who governs Jakarta. |
| **Cold parse** (S4) | *"1,025 people voted for 800,000. The UN called it free."* Parses with zero prior knowledge. This is the property the handoff calls the only structural thing Guatemala/Belize had. |
| **Topicality** | **Live, verified 2026:** Indonesia's national human-rights body logged 26 violent incidents Jan–Apr 2026; OPM claimed an airstrip attack in Boven Digoel in Feb 2026; Prabowo's transmigration expansion is the current flashpoint. ⚠ The 2019 Constitutional Court judicial review of the Act is **not** live — it was rejected in 2020. Do not cite it as a current case. |
| **VidIQ** | `west papua conflict` **5,267/mo**, overall **56.85**, competition **41.2** · `west papua` 3,908/mo, overall 50.77 |
| **Sources** | Dutch-language Netherlands New Guinea archives — **a language the owner reads**. Genuine channel-specific advantage. |

**POCKET flag: YES** (English-reading Papuan/Indonesian/Australian audience · near-zero English SERP · active dispute).

### B — Myanmar: the 1947 Panglong Agreement

**The claim on screen:** Burma's founding agreement with the Shan, Kachin and Chin promised autonomy,
and the 1947 constitution written alongside it carried a right of secession after ten years. Neither
survived contact with the state that followed.

| stage | evidence |
|---|---|
| **Demand** (S1) | The strongest pocket density in the whole corpus — *"most people don't know Burma/Myanmar even exists"* (914 likes), *"we never got attention"* (101), plus six more self-identified Burmese voices. |
| **Supply** (S3) | `channel-data/serp-studies/titles/panglong-agreement-1947-2026-07-29.md` — the shelf is **entirely Burmese-language**, plus British Pathé newsreel and AP Archive. No English explainer at any length. |
| **Identity** (S4) | Panglong text is short, signed, and showable; the 1947 constitution's secession clause is the second document. Passes. |
| **Cold parse** (S4) | **Weaker.** Understanding the stake requires knowing what Burma's ethnic states are. |
| **Topicality** | **Live, verified 2026:** junta losing the five-year war as of July 2026; Min Aung Hlaing installed as president April 2026 after Dec-25/Jan-26 controlled elections. |
| **VidIQ** | `panglong agreement` **4,662/mo**, overall **58.34**, competition **36.3** (best rankability of any candidate) |
| **Sources** | English-signed agreement, but the scholarship is largely Burmese — outside the owner's languages. |

**POCKET flag: YES, but recently served.** RealLifeLore's hour-long *Why Myanmar is Dying* is where
those comments came from. The pocket got its attention three months ago; that is the opposite of the
Panama situation.

---

## 3. Composite scores (TOPIC-RUBRIC v2)

| dimension | weight | **A — West Papua** | **B — Panglong** |
|---|---:|---:|---:|
| VidIQ overall | 30% | 56.85 → 17.06 | 58.34 → 17.50 |
| Topicality (verified live) | 20% | 100 → 20.00 | 100 → 20.00 |
| Whitespace (shelf × angle) | 25% | 100 → 25.00 | 100 → 25.00 |
| Title CTR format fit | 10% | **ESTIMATED** | **ESTIMATED** |
| Small-channel rankability | 10% | 41.2 → 50 → 5.00 | 36.3 → 100 → 10.00 |
| Source verifiability + access | 5% | 100 → 5.00 | 50 → 2.50 |
| **Composite (ex title-fit)** | | **72.06** | **75.00** |

**The composite favours B by 2.94 points — inside the 10-point tie-break band.** Per TOPIC-RUBRIC
rule 4 that means *collect the missing data before locking*, and the missing datum is the same for
both: the title-format-fit VidIQ batch, which needs candidate titles that don't exist yet.

**Neither candidate is locked.** The composite is not being overridden here.

---

## 4. Recommendation

**Recommended: A — West Papua**, and here is the honest basis, since the composite marginally prefers B.

The two things that separate them are **deliberately outside the composite**, by the rubric's own design:

1. **The POCKET flag is recorded, not scored.** Both flag YES, but A's pocket is *unserved* and B's was
   served by a 1M-subscriber channel in the last quarter. The whole point of the comment-mining method
   is demand *minus* supply, and B's supply just arrived.
2. **The cold-parse test.** The handoff (§1.4) calls stranger-legibility the only structural property
   the channel's single breakout had. A has it outright; B needs the viewer to already know what
   Burma's ethnic states are.

B stays live as the alternate, and its rankability advantage (competition 36.3) is real.

### Three things that are NOT this recommendation

- **Do not put this ahead of the shipping queue.** `BREAKOUT-MECHANICS-2026-07.md` §6.2 is explicit —
  five script-ready videos beat deepening one dossier. #36 Panama and #58 Kurdistan ship first.
- **The H3 pocket-raid slot is already filled by #36 Panama.** A second pocket raid before Panama's
  first-28-day numbers land would burn the read on H3. Greenlight this; queue it behind the Panama result.
- **This finds candidates, not winners.** Serve size is not predictable from anything in this repo
  (four predictors tested and killed, 2026-07-28). Nothing above changes that.

### One free shot the sweep found by accident

The corpus contains an **812-like comment** under Johnny Harris: *"Please do an episode about the
ongoing Cambodia-Thailand border clashes."* The channel **already made that video** —
*"38 Dead Over 4.6 Square Kilometers. Both Sides Blame One Map"* (2025-10-03, 33 views, ~807 lifetime
impressions) — and **its title names neither Thailand nor Cambodia.** That is the exact H6 pocket-unnamed
failure shape as Chagos and Sapodilla. Meanwhile the live SERP for that query carries Firstpost at
**303,735 views** on *"How a 1907 Map Has Sparked Thailand-Cambodia Clashes"* — the same 1907 map the
video is about.

⚠ **Temper the expectation:** VidIQ now returns **volume 0** on `thailand cambodia border` (search decayed
after the Dec-2025 ceasefire), and the video's problem was serve, not click — a retitle cannot manufacture
impressions. It costs nothing and it is a correctly-diagnosed defect, so run `/retitle` on it; do not
expect it to move the channel.

---

## 5. What to do next, in order

1. `/retitle` the Thailand–Cambodia video so the title names both countries. (Minutes, near-zero cost.)
2. Ship #36 Panama and #58 Kurdistan. Nothing here jumps that queue.
3. When the Panama H3 numbers land, `/greenlight` **West Papua — Act of Free Choice**.
4. Before the next sweep: widen `tools/intel/competitor_channels.json` toward the borders/treaties lane
   (§1), re-sync, then `python -m tools.discovery.gap_hunter --sweep --digest`.
