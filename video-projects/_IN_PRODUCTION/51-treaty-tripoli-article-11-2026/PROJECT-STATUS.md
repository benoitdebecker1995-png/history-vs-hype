# Project 51 — Treaty of Tripoli, Article 11

**Created:** 2026-04-24
**Lifecycle:** `_IN_PRODUCTION`
**Format:** Correction / Document-First (first test of this format)
**Target runtime:** 5-6 minutes (compressed from VidIQ's 7-min draft)
**Status:** Research phase — preliminary notes assembled, NLM notebook created, sources pending upload

**NotebookLM:** [#51 Treaty of Tripoli Article 11 (1797) — Hunter Miller / Arabic Discrepancy](https://notebooklm.google.com/notebook/b05813fc-0a59-4b93-ac34-dd63b9d60114)
**Notebook ID:** `b05813fc-0a59-4b93-ac34-dd63b9d60114`

---

## One-line pitch

The Senate ratified Article 11 in 1797 saying the US government is "not in any sense founded on the Christian religion." The Arabic original of the treaty does not contain that article at all — and Hunter Miller flagged this in a 1931 State Department publication almost nobody reads.

---

## Why this video (decision trail)

- VidIQ STC: 74,718 vol / 30.9 comp = **2,417 ratio** (best in the format research pool)
- Gemini Prompt A ranked it #7 of 25; Prompt B flagged it as politically combustible but verifiable; Prompt C validated the 5-7 min document-first format.
- Competitor scan: 2 existing YouTube videos on Article 11, neither forensically treats the Hunter Miller / Arabic discrepancy. **The gap is the 1931 citation.**
- User override: chose Tripoli over my Radcliffe Line recommendation. Reasoning: full production package already drafted, document is spectacular, wants to test keyword-dominant topic once.

See: `channel-data/FORMAT-EXPERIMENTS/SYNTHESIS-decision.md` for the full cross-filter.

---

## Political heat — flagged ONCE, then stop

This is a live US culture-war topic ("Christian nation" debate). Comment section will trend combative. Mitigation baked into the structure:

1. **Frame as document forensics, not political argument.** Voice: we are reading 1797 ink. That's it.
2. **Preempt the obvious objection in-script.** Acknowledge early that most 1797 Americans were Christian — the claim is about the *legal framing of the government*, which is what Article 11 literally addresses. Do not steelman either side; just read the document.
3. **Close on the forensic mystery, not the modern fight.** End with "why does the Arabic version not contain this article?" — it's historical curiosity, not ammunition.
4. **No modern political figures.** No 2024/2026 references. If comments drag it there, moderate hard.

Don't re-flag this in script review. Assume the mitigation works and test it.

---

## Deliverables checklist

- [x] Project folder created
- [x] PROJECT-STATUS.md
- [x] `_research/01-PRELIMINARY-RESEARCH.md` (Gemini + VidIQ integrated)
- [x] `_research/02-NOTEBOOKLM-PROMPTS.md` (verification prompts)
- [x] `_research/03-COMPETITOR-GAP.md` (YouTube comp scan + gap)
- [x] `ROUGH-STRUCTURE.md` (5-6 min, restructured 2026-04-24 for 1:30 reveal mandate)
- [x] NotebookLM round (Hunter Miller 1931 Tripoli passage, Senate Journal page 244, Crane 2020, Haselby 2015 — all uploaded and verbatim-verified)
- [x] `01-VERIFIED-RESEARCH.md` — 100% verified, 14 verified facts (F1–F14), all primary-source citations locked
- [x] Title scoring via `title_scorer.py` + VidIQ cross-check — initial title locked (later expanded to 3-slot rotation)
- [x] Thumbnail concept locked (single hero — split-screen English/Arabic, "MISSING IN ARABIC" overlay; later expanded to 3-slot rotation paired to titles)
- [x] `02-SCRIPT-DRAFT.md` — v5-FINAL written, 6 beats, ~6:00 runtime, NLM source_id `33c1a052-104b-4214-8614-83a97c0e6b4a`
- [x] `03-FACT-CHECK-VERIFICATION.md` — FACT-CHECK CLEAR after 2 blocking fixes (B1, B2 applied). 4 advisory items (A1–A4); only A4 needs visual asset fix in edit
- [x] `YOUTUBE-METADATA.md` — drafted 2026-04-25. 3-slot title + thumbnail rotation locked from competitor notebook data (Wave 2 + Packaging Intelligence). Description, tags, on-screen overlays, comment moderation + pinned comment all drafted. Open items: end-screen target pick, A4 visual asset confirmation, pinned comment final review.

---

## Production load estimate

- **Filming:** LIGHT — talking head + document reveals. No map work. ~1 day.
- **Editing:** LIGHT — document zooms, text overlays, one period illustration. No complex B-roll. ~1 day.
- **Research:** MEDIUM — the primary-source chain is clear (Hunter Miller → Barlow → Senate Journal), but the NLM round needs careful source selection (university press only on Early Republic / Barbary).
- **Total:** 4-5 days if research stays tight.

---

## Locked thesis (2026-04-27)

**Thesis (≤12 words, Rule 36 — script-writer-v2 v14.4):** *Historical texts remain dormant until domestic culture wars require new ammunition.*
**Thesis Type:** invisible-until-named.
**Walk-Away Test:** PASSED — same sentence universally captions the Second Amendment individual-rights interpretation, 14th Amendment incorporation doctrine, Magna Carta's 17th-century rediscovery, Commerce Clause activation post-1937.

**Locked closing VO (post-rough-cut pickup):**
> *"But Article 11 meant almost nothing until nineteenth-century activists started arguing over the public funding of Christian clergy. The text itself didn't change, but the country did, and we simply projected our new cultural divides onto an old piece of paper."*

**Closing structure:** rough-cut tape kept through "Today this English text is wielded as the ultimate weapon in a modern culture war." (video time 6:19.5). Hard cut to `assets/timeline-133-years.html`. New VO over graphic with Crane lower-third super. Final cut at 6:41.5. See `EDIT-PLAN-THESIS-LOCK.md` for the full edit sheet.

**Decision trail:** see `THESIS-CANDIDATES-NLM.md` (round 1, 5 thesis candidates), `CLOSING-LINE-CANDIDATES-NLM.md` (round 2, voice-failed), `CLOSING-LINE-CANDIDATES-NLM-R3.md` (round 3, locked Candidate 4).

---

## Locked packaging (2026-04-24)

### Title — LOCKED
**"The Treaty Of Tripoli's Most Famous Line Isn't In The Original Arabic"**
- 68 chars. Head-term anchor + forensic punchline. Niche-optimized (user override of channel's year-in-title penalty — disregarded for this video to test against broader niche patterns).
- Local title_scorer.py: edge case (no year, no colon, no "X That Y" pattern, but lower specific-number bonus — score parity with VidIQ's 4th-title proposal)
- VidIQ niche assessment: head-term anchored, no ideology, works for both engaged debaters and curious newcomers

### Title decision trail
| # | Candidate | Local | VidIQ | Outcome |
|---|---|---|---|---|
| A | "The 1797 Treaty That Ends the Christian Nation Argument" | 0/100 REJECTED | 85 | Rejected — channel-data wins on year + "X That Y" penalty |
| B | "Article 11. John Adams Signed It. They Never Taught You This." | 75 | 78 | Rejected — "They Never Taught You This" conspiracy-adjacent fights channel positioning |
| C | "The Document Where America Declared It Wasn't Christian" | 55 | 81 | Rejected — weakest local score |
| D | "One Treaty. Two Versions. One Line Was Never There." (VidIQ proposed) | 70 | unscored | Strong runner-up |
| **LOCKED** | **"The Treaty Of Tripoli's Most Famous Line Isn't In The Original Arabic"** | — | — | **Selected by user — niche-optimized override** |

### Thumbnail — LOCKED concept
**Split-screen, document-as-evidence:**
- LEFT: English Article 11 in period 1790s typography
- RIGHT: Arabic manuscript page with the empty/blank space where Article 11 should be visually highlighted
- TEXT OVERLAY: **"MISSING IN ARABIC"** (3 words, ~28pt)
- No face, no presenter
- VidIQ-projected CTR: 3.0–3.5% (vs 2.0–2.8% for single-document close-up). Channel avg 3.0%.

### Keyword strategy (post-VidIQ verification 2026-04-24)
**Head term (use in title — VidIQ-confirmed current data):**
- treaty of tripoli — 3,722/mo, 20.6 competition (down 29% from snapshot 5,241; still well above 1K floor)

**Description SEO targets (high-leverage adjacents from VidIQ Task 2):**
- religious history — 25,215/mo, STC 638 🚨
- american history documentary — 22,991/mo, STC 582 🚨
- john adams — 17,569/mo, STC 423 🚨
- thomas paine — 12,368/mo, STC 331 🚨
- deism — 9,194/mo, STC 335 🚨
- article 11 — 4,854/mo, STC 158

**DO NOT chase as title bait — zero search demand:**
- treaty of tripoli article 11 (0/mo)
- founding fathers religion primary source (0/mo)
- christian nation debate history (0/mo)
- john adams religion (0/mo)
- joel barlow, senate ratification 1797, founding fathers islam, barbary pirates history (all 0/mo)

**Outlier check:** No competing videos broke out on this exact topic in the past 180 days. Field is clear. Clean entry window.

---

## Risks

- **Comment war tanking retention curve** — mitigation above. Also: enable auto-hold on politically charged comments, moderate first 48 hours hard.
- **Sub-conversion ceiling** — political topics convert subs worse than forensic/mechanism topics. Accept this as the tradeoff of testing the keyword-dominant angle.
- **Running over 6 min** — VidIQ draft is 7 min. Cut the "modern implications" section entirely; let the document do that work off-screen.
