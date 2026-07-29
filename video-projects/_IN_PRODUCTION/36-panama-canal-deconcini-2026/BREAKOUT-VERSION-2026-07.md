# #36 Panama — the BREAKOUT version

**Date:** 2026-07-28 · **Input:** `SCRIPT.md` v2 (fact-check APPROVED, not locked) + today's findings in
`channel-data/BREAKOUT-MECHANICS-2026-07.md` and `_research/COMP-AND-POCKET-REFRESH-2026-07.md`.

**The script is already good.** Cold open is a genuine specificity bomb, the debunk loop is properly
built, the Ancon Hill close earns its emotion. **This is not a rewrite.** Three changes, each tied to a
specific finding, and one honest limit at the end.

---

## CHANGE 1 — The title must signal the POCKET, not just the topic

**Why.** H3's own kill note says the Sapodilla sequel died partly because *"the title never named Belize
or Sapodilla — so the pocket was never signaled."* Guatemala's title named Belize. If the Panamanian
audience is the mechanism (23 self-identified voices, 1 Spanish comment in 1,711), **the title has to
tell them this is their story.**

**And it should answer their actual request.** The pocket's two highest-liked comments, on two different
channels, ~2,800 likes combined, ask the same thing: **"how the panamanian got the control of the
canal."** The current locked title doesn't promise that — it promises a grievance.

| | title | pocket signal | promises the ask |
|---|---|---|---|
| current A | "Panama Canal Explained. No Panamanian Signed the Treaty." | weak — "Explained" is neutral/US-framed | ✗ ends on grievance |
| **LEAD** | **"America Took the Panama Canal With a Treaty. Panama Took It Back."** | **strong — names Panama twice, frames it as Panama's win** | **✓** |
| **ARM B** | "A Frenchman Signed Away the Panama Canal. Panama Took It Back." | strong | ✓ |

**Lead rationale:** it *is* the script's own thesis ("They took Panama with a treaty — and signed away the
right to take it back"), it's a mirror structure that's easy to remember, and — the Guatemala property —
**a total stranger parses it with zero prior knowledge.** 65 chars, two-sentence formula, anchor in the
first 40. All eight candidates scored 73 on `title_scorer`; the composite could not discriminate, so this
is decided on the pocket evidence, per ADR-0012 (scores are enrichment).

**A/B is single-variable** (H4-compatible): same second sentence, first half swaps mechanism ↔ specificity.

## CHANGE 2 — The cold open must point at the RESTORATION, not stop at the theft

**Why.** The title now promises "Panama took it back." The channel's one confirmed at-creation retention
lever is that the beat after the cold open bleeds ~12.7 points — so the promise has to be set *inside*
the first 30 seconds or the video reads as a grievance piece and the pocket's question stays unanswered
until 5:50 (55% in).

**Keep the cold open exactly as written** — the Frenchman, the two hours, the man nearly fainting on the
platform. It's the best 30 seconds in the project. **Change only the last line.**

> **Now:** "The treaty that gave away their canal — not one Panamanian ever signed it."
> **Breakout version:** "The treaty that gave away their canal — not one Panamanian ever signed it.
> **And seventy-six years later, they took it back the same way. With a document.**"

That single sentence converts the video from *how it was stolen* into *how they won it back* — which is
what the pocket asked for, what the title now promises, and what makes a stranger stay. **Nothing else in
the structure moves.** Acts 1–4 remain the setup; Act 5 now pays off a promise instead of arriving cold.

## CHANGE 3 — The thumbnail. This is where 2026 is actually losing.

**Why.** One video above 4% CTR in twelve this year; no ≥7% image since JD Vance, November. Feature
checklists can't fix it — Guatemala and the India–Pakistan video share identical tags (map + red) and
score 7.66% vs 1.61%. The four images that cleared 7% share four properties (full workings at
`BREAKOUT-MECHANICS-2026-07.md` §9):

1. **Flat fill, not line** — big blocks of colour, readable as a *shape*. Never a detailed reference map.
2. **Famous face or no face** — an unknown person is worse than nobody. (The creator's own face is on the
   channel's single worst performer at 1.11%.)
3. **Two text registers** — subject on top, stake beneath in yellow. Heavy sans, thick outline.
4. **One or two focal objects.** Not four.

### The spec

> **Image:** Panama in solid flat green. The Canal Zone as **one solid red stripe cutting the country
> clean in half**, ocean to ocean. Nothing else — no photos, no faces, no document, no ships. Two flat
> colours and a shape.
> **Top register:** `A COUNTRY CUT IN HALF` — black on white, heavy, thick outline.
> **Bottom register:** `IN PERPETUITY` — yellow, heavy outline.

**Why this and not the document.** The metadata currently specifies a *"Signed by a Frenchman."* overlay
and the script note already says the thumbnail *"needs regen off document-focal."* Correct —
**document-as-focal-point is the channel's CTR floor** (−0.71 overall, −2.11 on famous topics). The
signature belongs in the video, not the thumbnail.

**Why the strip works.** It's the literal story — a foreign strip through the middle of a country — it's
two flat fills, and it needs **zero prior knowledge**. That is the one structural property Guatemala had
that nothing else on the channel has had.

**Curiosity gap (required by the packaging lock):** the title says Panama took the canal back; the
thumbnail says the grant was **in perpetuity** — *forever*. The overlay never restates the title, and it
raises the question the title doesn't answer: **how do you undo forever?** That's Act 6.

---

## What does NOT change

- The whole 1903 → 1978 spine, all six acts, the Ancon Hill close. It's fact-check APPROVED.
- The DeConcini debunk as the payoff — the 8,500-like top comment is still the corpus's most-endorsed,
  unsourced and wrong in detail. That's the wedge.
- The 2026 ICC arbitration stays a **closing rhyme only**. Identity guard: if a beat explains present-day
  US–China politics for its own sake, cut it.

## ~~Still gating, carried from June~~ — **CLOSED 2026-07-28**

✅ The DeConcini characterisation has been verified **character-exact against the treaty text as deposited
with the United Nations** (UNTS Vol. 1161 I-18342, Condition (b)(1)). Flagged 2026-06-11, closed
2026-07-28. See `01-VERIFIED-RESEARCH.md` **Layer 9**.

⚠ **But the payoff changes shape.** The unelided US reservation (UNTS Vol. 1280 I-21086) shows the
non-intervention limit binds only action taken *"to assure that the Canal shall remain open, neutral,
secure, and accessible"* — **not US action on some other asserted basis, which is exactly what 1989 relied
on.** The honest verdict is a mechanism, not a slogan. **Act 7 needs rewriting to Layer 9's shape before
filming.**

## The honest limit

**None of this buys a serve.** Four predictors were tested today and all four failed; the escalation
event is not predictable from any data available (§5b). What these three changes do is maximise every
controllable: the pocket gets signalled, the promise matches the demand, and the image is built to the
only pattern that has ever converted on this channel.

If it gets served, this converts. Whether it gets served is the experiment — which is why #36 is the
pre-registered H3 slot, and why the geography check afterwards matters more than the view count.
