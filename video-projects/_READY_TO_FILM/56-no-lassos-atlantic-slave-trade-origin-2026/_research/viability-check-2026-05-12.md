# Viability Check — 2026-05-12

**Conducted:** During grill session that produced `C:\Users\Benoi\.claude\plans\i-have-a-video-joyful-wolf.md`
**Gate verdict:** PROCEED

This file preserves the live-scouting findings for post-mortem reference. It is the pre-greenlight context, not the greenlight verdict itself. `/greenlight` runs separately at Phase 0 with comment-mine + VidIQ + competitor-gap + title_scorer + thumbnail_checker.

---

## Finding 1 — The original spine premise was wrong

**The assumption:** Dosunmu (Oba of Lagos, 1853–1885) inherited from his anti-slavery father Akitoye, and the viral comment's "the Oba was a slave trafficker" framing would collapse against the documents.

**What the sources actually say:** Dosunmu briefly revived the slave trade after Akitoye's 1853 death. Wikipedia and corroborating sources: *"Under Dosunmu, the slave trade was revived briefly until the British convinced him to exchange the ports of Lagos for a yearly pension of 1,200 cowries (equivalent to £1,000)."* Kosoko (the pro-slavery deposed Oba) continued raiding from Epe with hundreds of warriors after 1853, contributing to the survival-pressure context.

**Implication:** Asmongold's amplified comment has **partial empirical purchase**. The video's job is no longer "falsify the comment" — it's "provide the causal chain the comment omits." Beat 1 concedes the easy fact, then deploys the harder context.

**Status:** Reframe accepted. Reframed plan reuses Rule 40 (Baseline-Before-Exception) twice — once in Beat 1, once in Beat 2. The concede-then-deploy structure IS Rule 40 applied.

**Next step:** Phase 1 NotebookLM grounding must verify each link of the 8-year causal chain (Akitoye 1851 → bombardment → Kosoko continuing raids → Dosunmu inheritance → brief revival → palm oil + abolitionist + strategic British leverage → Bedingfield threat → 1861 Treaty). T1 and T2 in the pivot protocol cover what happens if links break.

---

## Finding 2 — Competitor space partly saturated

**Existing coverage on YouTube + adjacent media:**

| Item | Type | Coverage |
|---|---|---|
| "Africans Sold Their Own: What Really Happened" | YouTube video | Dedicated debunk of the general claim |
| "The Day Lagos Was Taken: Oba Dosunmu and the British Betrayal (1861)" | YouTube video (Nigerian-history channel) | Covers the exact 1861 event |
| Hasanabi reaction to "Asmongold's INSANELY RACIST RANT On Africans" | Streamer reaction | Streamer-reaction window partly occupied |
| Dr. Obadele Kambon's Black Trauma Podcast | Podcast | Debunks "Africans sold their own" claim |
| Multiple university-blog write-ups | Essays | Same debunk angle |

**Implication:** Pure debunk is **saturated**. *Document-deployment* (the primary-source layer in shareable form) is **not**. The differentiation is clearer when framed this way.

**Status:** Frame accepted as the differentiation hook for greenlight. Per `feedback-single-word-focus-when-competitor-scatters.md` — when competitors scatter across exhibits, our edge is single-exhibit depth. The 1861 Treaty + Zurara *Crónica* are the two single-exhibit moments.

**Next step:** Refresh competitor-gap scan at Phase 0 via the `competitor-gap` agent. If the closest competitor's documents overlap >50% with our plan, pivot to their gap. <50%, proceed and reference their work in description.

---

## Reaction-format prior base rate

Pulled from `tools/youtube_analytics/analytics.db` (2026-05-12):

| Video | Views | Ret% | Subs | Title pattern |
|---|---|---|---|---|
| Vance Pt 1 | 1,142 | 26.3 | 16 | **Name + specific claim + evidence-promise** |
| Vance Pt 2 | 48 | 34.4 | 0 | Name + abstract question |
| Fuentes | 179 | 25.7 | 0 | Name + judgment + colon |
| Crusades | 682 | 27.0 | 7 | No-name + framing verb |

**Channel median (n=55):** 833 views, 28.5% retention, 6 subs gained.
**Reaction-format average:** ~512 views — **62% of channel median.**

**Implication:** Reaction format underperforms channel median historically. Only Vance Pt 1 cleared median — and it used the claim-led-with-evidence-promise title shape.

**Rule for #56:** Title must be claim-led with evidence promise (Vance-Pt-1 shape). Streamer name allowed; claim must lead. No colons. No years.

---

## Gate verdict

**PROCEED.** Three reasons:

1. The shaky spine premise is **resolved** by the reframe (concede + context, not falsify). Rule 40 applied twice.
2. The saturated debunk space is **dodged** by the document-layer positioning.
3. The reaction-format 62%-of-median base rate **remains a risk**, but algorithmic juice from Asmongold + Destiny + the 1861 Treaty primary source raises the ceiling. Title shape (Vance-Pt-1) is the lever for clearing the median.

**Conditions for proceed:**
- `/greenlight` must PASS on demand (≥1K/mo on at least one keyword cluster) — hard stop per `PACKAGING_MANDATE.md` if all <1K/mo
- competitor-gap refresh must not surface a closer document-layer competitor
- title locks via title_scorer.py + memory rule `feedback-topic-vs-angle-ordering.md` minimum gate stack (comment-mine + VidIQ + NotebookLM mechanism-word grounding)

---

## Grill decisions (7 locked Qs, 2026-05-12)

| Q | Decision | Why |
|---|---|---|
| Q1 | Thesis working (unlocked) — *"Concede the easy fact. Deploy the harder document."* | Final lock at `/thesis-discovery` post-Phase 1 |
| Q2 | Scope expanded to 2 beats (1861 Lagos + 1453 Zurara) | Asmongold made both a specific (1861) and a general ("no lasso") claim; both have documents |
| Q3 | Spine flipped to 1861 Lagos | After viability check found Dosunmu did briefly revive the trade |
| Q4 | Destiny = framing not beat | Destiny is in cold open + closing beat, not a dedicated middle beat |
| Q5 | Tooling visible in closing beat (Option B) | "Destiny was structurally right. He just didn't have the receipts. Now you do." |
| Q6 | Keep streamer clip + pivot to hard docs | Reaction-clip cold open + Format C close-read body |
| Q7 | One-video frame with signal-tracking (Option A) | This is a vibes test; channel-level repositioning requires 2+ data points |
