# Fig Tree Edit Pass — Predictions for #52 Hijab

**Date written:** 2026-05-18 (BEFORE filming — pre-registered to prevent hindsight bias)
**Script version under test:** v3.2 (`SCRIPT.md`) — Fig Tree edit pass applied
**Baseline comparison:** v3.1 (`SCRIPT-v3.1-locked.md`)
**Channel median retention baseline:** 28.1% (n=47 long-form)

---

## 1. Hypothesis

Spatial-pointer document reveals, stay-on-face quote performances, and stinger-free verbal transitions will improve retention vs. how the same content would have performed under v3.1's editing rhythm. Effects should be visible at specific timestamps where v3.2 diverges from v3.1.

**Null hypothesis:** No measurable improvement at any divergence point. Edits are noise at this channel size (n=527 subs, packaging-first bottleneck per memory `feedback-channel-data-too-small.md` + `feedback-starting-channel-search-anchored.md`).

**Skeptical prior:** Packaging is the channel's #1 bottleneck. CTR and title-thumbnail matching the search anchor matter more than editing rhythm at this stage. Edits may produce a real but invisibly-small effect dwarfed by packaging variance.

---

## 2. Falsifiable predictions

### Retention-curve predictions (where to look in YouTube Studio)

| Timestamp | v3.1 expected | v3.2 prediction | What to check |
|---|---|---|---|
| **0:00–0:30** | Cold start retention dip — paradox card → tablet immediately | Slightly LATER first dip — face holds longer on "Most people start this debate in 7th-century Arabia" before the cut | Earn-the-cut prediction |
| **0:30–1:00** | One flat hold on MAL 40 law block VO | **3 micro-bumps** at "The first… The second… The third…" pointer beats | Spatial-pointer prediction (highest-leverage edit) |
| **2:10–2:15** | Music stinger on chapter card | Silent card — should NOT cause a dip; if anything, less interruption | Stinger-free chapter card |
| **4:00–4:20** | Whip-quote delivered as B-roll on Musannaf citation | **Face-hold during the quote performance.** Bump or no dip predicted. If retention DIPS here, face-hold is wrong for this content. | Stay-on-face quote performance |
| **5:00–5:30** | Ibn al-Jawzi reasoning paraphrased | **Spatial pointer on "attenuating the visual distinction"** — primary-source phrase on screen. Should HOLD attention through the legal jargon, not lose it. | Document-treatment prediction |
| **5:50–6:40** | Document-first delivery, rhetorical question buried | **Question-first delivery** — face poses "If the veil was really about modesty, what would a plague decree look like?" then cuts to al-Maqrizi. Predict the question-on-face beat reduces drop-off at the 6:00 minute mark (common falloff point per channel data). | Question-first sequencing |
| **6:40–7:00** | Aisha quote on B-roll | **Face-hold for Aisha's rank-claim quote.** Predict comments mentioning her specifically (high-emotional-weight moment). | Stay-on-face prediction (second instance) |
| **7:25–7:30** | Music stinger on §VIII chapter card | Silent card | Stinger-free (second instance) |
| **10:30–11:00** | Side-by-side reveal without spatial language | **"On the left — Mesopotamia, 1200 BCE. On the right — Afghanistan, 2026."** Predict highest comment-density moment of the video. The thesis-document moment. | Closing-spatial-pointer prediction |

### Aggregate predictions

- **Median retention ≥ 28.1%** (channel baseline) — soft win threshold
- **Median retention ≥ 33%** — hard win threshold (5pts above baseline)
- **No catastrophic dip** at any v3.2-specific edit timestamp (catastrophic = >5pts drop in <15 seconds)
- **Average view duration ≥ 4:00** (~35% of 11:30 runtime) — strong signal

### Comment signal predictions

Watch for comments mentioning:
- "The Assyrian law / 1200 BCE" — §I MAL 40 pointer landed
- "Ibn al-Jawzi / attenuating the visual distinction" — §V indictment landed
- "The plague test / If it was really about modesty" — §VI question-first landed
- "Aisha / 'God has honored me'" — §VII face-hold landed
- "Mesopotamia to Afghanistan / 3,200 years" — §VIII closer landed
- "The pattern is class" / "It's about state control" — overall thesis landed

If 2+ of these signals appear in top 20 comments → Fig Tree treatment is doing audience-readable work.

---

## 3. Failure modes that would falsify the framework

| Observation | Conclusion |
|---|---|
| Retention DIPS at spatial-pointer beats (0:30–1:00 or 5:00–5:30 or 10:30–11:00) | Pointer language adds cognitive load without payoff. Roll back. |
| Retention DIPS during face-hold quote performances (4:00–4:20 or 6:40–7:00) | Calm Prosecutor delivery doesn't carry the performance like Fig Tree's does. Cut back to B-roll for quotes. |
| Comments mention "boring document" / "too slow" / "felt like a lecture" | Pacing slowed too much. Calibrate. |
| Median retention < 25% | Below baseline. Either edits hurt OR packaging wasn't enough OR topic underperformed regardless. Confounded — need #56 to disambiguate. |
| Median retention 25–28% | No effect. Treat as null. Re-examine at #56. |
| Median retention 28–33% | Mild positive. Encouraging; wait for #56 confirmation. |
| Median retention ≥ 33% | Strong positive. If #56 confirms, promote rules. |

---

## 4. Confounds to acknowledge

- **Packaging variance dominates.** A bad title/thumbnail will tank retention regardless of script edits. Compare retention only if impressions get the video past the cold-start floor (~500 views).
- **Topic loading.** Hijab is a higher-controversy topic than typical channel fare. Comment volume will be elevated regardless of script quality. Quality signal needs comment *content* not count.
- **Single-video N.** This is n=1. #56 doubles N. Even both = n=2, well below the 30+ needed for channel data to be actionable per memory `feedback-channel-data-too-small.md`. Treat as soft signals only.
- **Filming + delivery variance.** v3.2 edits change the script; they don't guarantee the on-camera execution matches the design. If the spatial-pointer beats are read flatly instead of pointedly, the test isn't of the edit — it's of the delivery.

---

## 5. Decision rules

**At T+14 days post-publish, run `/analyze` and update this file with results.**

| Outcome | Decision |
|---|---|
| Strong positive on both #52 AND #56 (≥33% median + 2+ comment signals each) | **Promote Rules 43–46** to `script-writer-v2` v16.0 + `WRITING-VOICE-AND-STYLE.md` PART 4 |
| Mild positive on both (28–33% median + 1+ comment signal each) | **Extend test** — apply to #45 Monroe Doctrine (next in pipeline). 3rd video before promotion. |
| Mixed: one strong, one null | **Investigate confound** — was the null video's packaging the bottleneck? If yes, extend test. If no, framework is topic-dependent, narrow the rules. |
| Both null or negative | **Reject framework** — Fig Tree's editing rhythm doesn't transfer to Calm Prosecutor voice at this channel size. Document why and move on. |

---

## 6. Where to check the data

- **Retention curve:** YouTube Studio → Audience retention tab (need at least 500 views for stable curve)
- **Comments:** `/engage` skill OR raw scroll of top 20 comments by likes
- **Analytics summary:** `tools/youtube_analytics/analytics.db` after `/reconcile` archives the published video → run `/analyze` for full report
- **Comparison artifact:** `_ARCHIVED/published/52-hijab-women-rights-2026/POST-PUBLISH-ANALYSIS.md` (generated by `/analyze`)

---

## 7. Result section (TO FILL IN POST-PUBLISH)

*Filled in at T+14 days after upload.*

**Upload date:** TBD
**T+14 analysis date:** TBD
**Retention summary:** TBD
**Specific timestamps observed:** TBD
**Comment signals observed:** TBD
**Decision triggered:** TBD
