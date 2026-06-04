---
name: Topic-selection rubric for sub-1K-sub channels
description: Empirically-grounded composite scoring framework for picking video topics at small channel size — replaces ad-hoc advocacy with reproducible math
type: feedback
originSessionId: 19d344f9-1eb5-43d1-b2b9-e9964c7bc06f
---
When greenlighting a new video topic at small channel size (sub-1K subs, search-anchored, no audience flywheel), use a transparent composite rubric grounded in published methodology — NOT hand-built vol×comp transforms.

**Why:** During 2026-05-08 weekend-test planning for a 5-min vibes test, I produced multiple topic flips (Donation of Constantine → Knights Templar/Chinon → Donation again) by introducing fabricated math (a "small-channel reach %" table I invented). User correctly identified this as advocacy wearing math clothing. Web research surfaced VidIQ's documented Overall Keyword Score (which already combines vol+comp per their published methodology) and Backlinko/TubeBuddy's empirical small-channel guidance (target comp <40, vol 1K-20K/mo). The rubric got rewritten using documented sources only.

**The empirically-grounded rubric (40% / 20% / 20% / 10% / 5% / 5%):**

| Weight | Dimension | Source |
|---|---|---|
| 40% | VidIQ Overall Keyword Score (0-100) | VidIQ direct — already a vol+comp composite per their methodology; appears as the prefix number in VidIQ keyword output (e.g., "67 edict of expulsion") |
| 20% | Title CTR (Format-specific, 0-100) | VidIQ Channel CTR score; if untested, use cross-batch format average flagged ESTIMATED |
| 20% | Top-3 English saturation on the specific topic | Gemini per-topic competitor scan: COVERED=0 / EMERGING=50 / EMPTY=100 |
| 10% | Small-channel rankability gate | Empirical: comp <40=100, 40-50=50, >50=0 (per Backlinko/TubeBuddy guidance) |
| 5% | Source verifiability + digital access | Manual: user's languages + PDF/epub availability |
| 5% | Foreign-audience validation bonus | Gemini Y/N on >100K-view foreign-language coverage — apply SYMMETRICALLY to all candidates |

**How to apply:**

1. **Tool role separation is mandatory.** VidIQ for keyword/search/title data only. Gemini for general web research / competitor scans / format saturation only. Manual for source/access/language. Mixing tools within a single decision criterion = the failure mode.

2. **Don't hand-build vol×comp transforms.** VidIQ already publishes the composite (Overall Score 0-100). Use it. Inventing your own reach % table at unverified percentages is fabrication — and fabrication will determine the winner in a tight race.

3. **Apply the foreign-audience bonus symmetrically.** Asking Gemini "does this candidate have foreign coverage?" for ONE candidate but not others rigs the comparison. Either query all candidates or drop the dimension.

4. **Tie-breaking rule:** if top score is within 10 points of #2, collect missing data (run additional VidIQ title scoring or saturation queries) before locking. Do NOT manually override the math.

5. **No advocacy in the score.** Once the rubric is locked and weights agreed, the composite IS the answer. Don't argue topic merits to nudge results. If you want a topic to score higher, find missing data that legitimately raises it (e.g., title-score it, query foreign coverage, check saturation).

**Verification of correct application:**
- The rubric should occasionally pick a topic the user did NOT initially favor — that's evidence the math isn't being gamed
- Two independent runs with the same data should produce the same ranking (reproducibility test)
- If a candidate's score depends on an ESTIMATED value, flag it explicitly and run the underlying VidIQ batch before lock

**When NOT to apply:** Topics where channel context dominates (commitment to a series, parked package being revisited, follow-up to a specific recent video). Those decisions live in the channel's editorial pipeline, not in greenlight scoring. The rubric is for FRESH topic selection, not pipeline execution.

**Origin:** 2026-05-08 weekend test plan, after 4 grill questions exposed fabricated rubric inputs and asymmetric data application.
