# CTR Thumbnail Findings — visual audit of real thumbnails vs CTR (2026-06-27)

**Method:** pulled the actual published thumbnails (img.youtube.com by video_id) for the
6 highest- and 6 lowest-CTR videos and visually compared them against real Studio CTR.
Companion to `CTR-TITLE-FORMULA-2026-06.md`. Lifetime CTR is confounded by topic+title, so
treat these as STRONG hypotheses to confirm via native Test & Compare (per-variant CTR).

---

## ✅ FULL-56 VALIDATION (2026-06-27) — all thumbnails tagged, not just extremes

Tagged all 56 thumbnails (table `analytics.db.thumbnail_features`), CTR-by-feature on n=47:

| feature | median CTR delta | verdict |
|---|---:|---|
| document-as-focal-point | **−0.71** (2.41 vs 3.12) | CONFIRMED bad |
| clean map | **+0.65** (3.12 vs 2.47) | CONFIRMED good (largely a proxy for famous territorial topic) |
| busy / cluttered | **−0.52** | CONFIRMED bad |
| creator face: emoting vs blank | 3.62 vs 2.52 (n=2 vs 9) | holds, weak — blank face doesn't help |
| **red pop** | **−0.67** | ❌ **OVER-FIT, KILLED.** Claimed a winner from the 12 extremes; across all 56 it's NEGATIVE — red is on 29/47 thumbs (every declassified-stamp / red-arrow document flop), so it's confounded with the cluttered-document style, not a driver. Do NOT prescribe "add red." |

Confound caveat: map/document features partly proxy TOPIC FAME (famous disputes get clean
maps; obscure topics get cluttered documents). Image-craft rules that stand on their own:
**avoid document-as-focal, avoid clutter, keep it legible, emote if a face is shown.**
Causation still needs Test & Compare.

## Winners (high CTR) — shared recipe

JD Vance child sacrifice 9.37% · Guatemala-2 9.11% · Guatemala-1 7.62% · Selk'nam genocide
7.59% · KGB 7.40% · Crusades 5.48%.

1. **One focal point** — a face, a map, or a single object. Never cluttered.
2. **Recognizable or emotional element** — a famous/expressive face, OR a clean map with
   ONE red disputed slice, OR a meme.
3. **Red / high-contrast conflict pop** — disputed land in red, red "CLASSIFIED" stamp.
4. **2–4 words of big legible text**, white/yellow with heavy black stroke, ≤2 lines.
5. **Verdict / investigation language** — EXPOSED, ON TRIAL, FACT CHECKED, CLASSIFIED,
   "THE GENOCIDE NO ONE TALKS ABOUT."
6. **Readable in <1 second**, and coherent with the title.

## Losers (low CTR) — the kill-list

JD Vance human rights 1.48% · Medieval literacy 1.12% · Vichy 1.11% · Trade Wars 1.02% ·
USSR "3 men" 0.93% · $24 Manhattan 0.48%.

- **Clutter** — 3+ competing elements (Trade Wars: podium + newspaper + chart).
- **Document or chart as the focal point** — walls of unreadable small text (JD Vance human
  rights, Vichy "typed draft"), charts (Trade Wars). The forensic-document MOAT is poison
  as thumbnail material — show the *shock the document reveals*, not the document.
- **Blank faces** — Medieval literacy used the creator's face + "DEBUNKED!" (the exact
  MiniMinuteMan move) and got 1.12%. A neutral face adds nothing; only an EMOTING face works.
- **Dull / monochrome** — gray old maps (USSR), faded backgrounds.
- **Title↔thumbnail mismatch** — $24 Manhattan (thumb "PLAGIARIZED" over paintings vs title
  about Manhattan purchase), USSR (thumb "ILLEGAL BORDERS?" vs "3 men signed"), Medieval
  (thumb "Dark Ages" vs title "Literacy Boom"). Incoherent packaging = no click.
- **Nerdy archival hooks** — "TYPED DRAFT / HIS NOTES", arrows pointing at clauses,
  signatures. The auditor's-edge appeal does not survive at thumbnail size.
- **Typos** — "PROPGANDA" (Trade Wars). Reads amateur.

## Key reversals (don't repeat these mistakes)

- **"Put the creator's face on it" is NOT the lever.** Tested (Medieval, 1.12%) and failed.
  Faces work only when (a) famous OR (b) emoting hard, AND the topic carries stakes.
- **Documents/charts kill thumbnails** even though documents are the channel's content moat.
- **Title and thumbnail must tell ONE coherent story.** Mismatch is rampant in the losers.

## What's possible / data needed

- **Now:** audit all 56 thumbnails to confirm; encode findings into a thumbnail pre-flight
  checklist (focal point · legible 2–4 words · red conflict pop · coherent w/ title · no
  chart/document focal · face only if emoting); gate every new thumbnail before publish.
- **Going forward (only the creator can generate):** native **Test & Compare** per-variant
  CTR on the same video = clean causal data. Run 2–3 variants/upload, log per-variant CTR;
  after ~6–8 videos we have a real thumbnail-feature dataset and can weight the rubric.
