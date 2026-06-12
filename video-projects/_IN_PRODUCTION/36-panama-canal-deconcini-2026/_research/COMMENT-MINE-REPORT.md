# Comment-Mine Report — #36 Panama Canal Treaties

**Date:** 2026-06-11 | **Method:** `/comment-mine` (yt-dlp, top-comments sort, ~200/video cap)
**Corpus:** 1,662 comments across 16 videos (6 fetched this pass + 10 recovered from prior-attempt cache). Raw data: `_research/comment-mining/` (`comments-extracted.txt`, per-angle `signals-*.txt`, `*.info.json`).

## Videos mined

| Video | Channel | Views | Comments |
|---|---|---:|---:|
| 6LNuRW9t4JA Modern Marvels: Construction | HISTORY | 2.87M | 200 |
| 0t2EE5JZP-M Why did the US give up the Panama Canal? | History Matters | 1.98M | 200 |
| uE_UuHRtXCY Demolition, disease, and death | TED-Ed | 1.56M | 200 |
| BrH66Phjjts How Trump Plans to 'Take Back' the Canal | WSJ | 577K | 200 |
| AyrfxG1Po-g Panama Kicks China & CK Hutchison Out | Valuetainment | 139K | 116 |
| NNJDeETKP78 China Fumes as Panama Ends Port Contracts | TaiwanPlus | 108K | 200 |
| + 10 cached: HISTORY-build, Geographics, Valuetainment-BlackRock, DW×2, NTD, CGSP, WION, Reuters, PBS | — | — | 546 |

---

## Per-angle demand scores

Signal = comment that asks a question the angle answers, asserts/corrects the angle's core fact, or explicitly requests the content. Like-weight = sum of likes on signal comments (audience endorsement, not just commenter count).

| # | Angle | Signals | Like-weight | Verdict |
|---|---|---:|---:|---|
| **2** | **DeConcini / "US still has a legal right"** | **~22** | **~8,800** | **WINNER — the claim is already viral, unsourced, and contested** |
| **1** | Treaty forensics / Bunau-Varilla | ~19 | ~3,400 | Strong #2 — the most-liked "you left this out" correction on every history video |
| 6 | Sovereignty arc (1903→1989→2026) | ~25 | ~2,600* | Strong as SPINE, not hook — "Carter gave it away" is the #1 recurring fight |
| 3 | 2026 ports dispute | ~40 | high but saturated | High demand, high supply — 8+ news videos already serve it; works as payoff beat only |
| 5 | 1989 invasion legality | 6 | ~70 | Explicit gap ("barely mentioned in any media") but small; mid-video beat / Part-2 seed |
| 4 | Engineering/build (baseline) | ~0 unmet | — | Confirmed saturated: build-video comments are nostalgia + appreciation, zero gap-asking |

*A6 like-weight excludes the 8,500-like comment, credited to A2 (it's the DeConcini claim verbatim).

### Headline finding — Angle 2

The single most-liked comment in the entire corpus — **8,500 likes, the TOP comment under History Matters' 1.98M-view video** — IS the DeConcini/Neutrality-Treaty claim, stated from memory, without the document, with the details wrong:

> [0t2E-1] (8,500 likes) "part of the treaty stipulates that the US is allowed to take complete control over it, the canal zone and remiliterize the canal at any point if there is a threat to US or Panamanian sovereignty... it has a return policy."

Zero of 1,662 comments name "DeConcini." Nobody cites the actual text. Meanwhile WSJ commenters fight over it blind:

> [BrH6-79] "They violated the US Panama treaty... according to that treaty, we can take any action, including military action... The treaty is quite clear on what happens if you violate."

> [BrH6-68] "So Chinese company running the port is violation of the treaty but American company running is neutral?"

The audience's most-endorsed "well actually" is an unverified treaty claim, and the comment sections are actively arguing about what the document permits. That is a document-on-screen wedge custom-built for this channel: *"The most-liked comment under the biggest Panama Canal video cites a treaty clause. Here's the actual page."*

### Angle 1 — treaty forensics (strong second / opening beat)

The Bunau-Varilla correction is the highest-liked substantive correction on every history video mined:

> [0t2E-200] "You left out the part where no Panamanian signed the agreement, a Frenchman signed for Panama... collected a large amount of money in the transaction, then split never returning to Panama."

**Modern Marvels check (task question):** Yes — one commenter picked up the "No Panamanians signed that agreement" thread:

> [6LNu-41] (14 likes) "They kinda left out the facts that the French engineer went behind the [Panamanian] peoples back and sold the project to the Americans and that is why no Panamanian people signed it."

Only ~3/200 Modern Marvels comments engage the treaty story (build-doc audience is there for construction nostalgia), but on History Matters and TED-Ed the Bunau-Varilla omission draws 10+ corrections each, several from self-identified Panamanians (0t2E-75 12L, uE_U-22 27L, uE_U-11 98L). Also note 0t2E-5 (1,800 likes) retells the Nicaragua-route/Spooner Act switch — Bunau-Varilla's lobbying story already has audience traction.

### Angle 6 — sovereignty arc (the spine)

The most-liked content request in the corpus:

> [uE_U-4] (1,000 likes, TED-Ed) "it would be interesting if you could talk about how the panamanian got the control of the canal"

Plus the "Carter gave it away" fight appears 15+ times across every video (Modern Marvels alone: 6 "Carter gave it away" comments), with corrections pushing back:

> [0t2E-59] (21 likes) "I love how the narrator didn't mention the campaign for the Panama Canal, the voting... and the congress decision in favor of it. Erroneously portraying it as just a Jimmy Carter decision."

### Angle 5 — 1989 invasion (explicit but small gap)

> [0t2E-41] (44 likes) "You should make a video about why the US invaded panama in 1989"

> [zCx7-47] "Does the video mention the 1989 US invasion of Panama? ... it's barely mentioned in any media."

Two explicit video requests (+ HY8Q-48 asking Warographics). Real whitespace, low volume. Fits as the arc's middle beat or a Part-2 seed, not the headline.

### Angle 3 — 2026 dispute (demand met by news, demand UNMET on history side)

News-video comment sections are partisan China/Trump shouting (low mine value). The usable signal is the current-events pull INTO history videos: 0t2E-4 "This video's gonna get an uptick" (2,200 likes), 6LNu-6 "How many people here hoping trump takes it" (116 likes) on a build documentary. And the best-liked Panamanian correction shows the misconception the 2026 beat must fix:

> [BrH6-5] (337 likes) "Panama canal is not operated by chinese, all workers are from Panama and can only be from Panama by law... the two ports are not in the canal but close to it."

---

## Recurring audience questions (→ script beats)

1. **"Can the US actually take it back — what does the treaty allow?"** (BrH6-79 vs BrH6-68/77/112 fight; zCx7-26; ~12 "we can/can't take it back" assertions) → the DeConcini document reveal.
2. **"How did Panama actually get control?"** (uE_U-4, 1,000L) → Torrijos–Carter mechanics, two treaties not one, Senate 68-32.
3. **"Why doesn't anyone mention the 1989 invasion?"** (0t2E-41 44L; zCx7-47; HY8Q-48) → invasion-legality beat; note DeConcini-era "right to intervene" was the claimed legal cover.
4. **"Who actually signed for Panama in 1903?"** (0t2E-193/200; uE_U-162) → Bunau-Varilla cold open.
5. **"Is the China ports thing a real treaty violation?"** (BrH6-64/68/112; Ayrf-42 noting the court case was about the contract, not China) → 2026 court-ruling payoff.

## Misconceptions to debunk (→ myth-contradiction fuel)

1. **"The treaty has a return policy / US can retake control at any time"** — 8,500-like top comment; DeConcini's actual text is narrower (force to keep the canal OPEN/neutral, expressly not a right to intervene in Panama's internal affairs or retake sovereignty — per the 1978 leadership amendments).
2. **"Carter gave it away"** (solo-decision myth) — ignores Senate ratification, Ford/Nixon-era negotiations, 1964 Martyrs' Day riots (0t2E-125, uE_U-55), Torrijos.
3. **"It was a 99-year lease that expired"** (0t2E-182) — Hong Kong contamination; Hay–Bunau-Varilla was *in perpetuity*, which is the scandal.
4. **"China operates/controls the canal"** (BrH6-5 337L correction; NNJD-1 308L) — ports ≠ canal; ACP runs it; workforce Panamanian by law.
5. **"Panama was forced to sign"** (0t2E-108) — sharper truth: NO Panamanian signed at all; a French shareholder did, two hours before the delegation arrived.
6. **"We built it, we own it"** (Z0m8-7 et al.; BrH6-2's Alaska/Brooklyn-Bridge counter at 775L) — the legal-precedent fight the video adjudicates with documents.

---

## VERDICT

```
ANGLE RECOMMENDED: 2 — DeConcini Reservation as spearhead, carried on the 6 sovereignty-arc spine,
                   opened with the 1 treaty-forensics cold open (Bunau-Varilla / "no Panamanian signed")
Signals: A2≈22 (like-weight ~8,800) | A1≈19 (~3,400) | A6≈25 (~2,600) | A3 saturated | A5=6 | A4≈0 unmet
Key signal: 8,500-like top comment on History Matters = the DeConcini claim, unsourced and wrong in detail
Reasoning: The audience already believes a half-true version of Angle 2 at viral scale and is fighting
about it in 2026-dispute comment sections with nobody citing the document. Angle 4 has zero unmet
demand; Angle 3 is news-saturated and works only as the modern-relevance payoff. The three winning
angles chain naturally: 1903 forged consent → what the 1977 treaty actually says (DeConcini) →
1989 use of the clause → 2026 court fight. That IS the sovereignty arc with a document at each beat.
```

Hedge (per channel rules): these are demand signals from competitor audiences, not a mandate — final angle lock is the user's call, and the DeConcini text characterization above must be verified against the actual treaty/amendment text in Phase 2 before any script line is written.

**Next step (methodology Step 6, on user lock):** add "Angle decision — LOCKED" to `01-VERIFIED-RESEARCH.md` with these counts + update production-state memory.
