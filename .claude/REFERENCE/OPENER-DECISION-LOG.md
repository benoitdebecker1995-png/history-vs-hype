# Opener Decision Log

**Purpose:** Append-only log of locked /opener decisions. Read by future /opener runs to surface accumulating user-preference patterns without inferring from channel performance metrics.

**Rule:** Captures user's stated reasoning (qualitative), not aggregate statistics. After 10-15 entries, the log may surface signals like "user has locked specificity_bomb 8/10 times for myth-busting topics" — that's a real preference signal, not channel-data noise inference.

**Firewall:** This log captures USER STYLE DECISIONS, not CHANNEL PERFORMANCE INFERENCES. Per [Channel Data Not Actionable], it's the right category of data to learn from.

---

## Entries

<!-- Append entries below. Most recent at bottom. -->

---

### 2026-05-24 — Video #56 (Atlantic Slave Trade Origin Debunk)

- **Locked title:** Yes Slavery Existed In Africa. Then Europe Industrialized It.
- **Topic type:** myth-busting / ideological
- **Locked archetype:** specificity_bomb / document-first (Zurara 1444 chronicle)
- **Locked candidate:** B-tight (v3 micro-refinement of Candidate B)
- **Clip slot:** 0:30 pivot (2-4s streamer-foil insert post-document-authority, pre-refutation)
- **Run history:** v1 ad-hoc (myth_contradiction "Three viral claims") → v2 choice-ignorant n=36 (specificity_bomb B Zurara) → v3 choice-ignorant n=44 (B confirmed + clip slot resolved)
- **Corpus state at lock:** 44 sources (36 baseline + 8 user-directed adds: Hbomberguy ×2, Folding Ideas ×2, Shaun "Bell Curve", Atun-Shei ×2, "How Johnny Harris Rewrites History"). Notebook id `5287616d-7790-492b-bf52-0bbe880db71a`.
- **Peer-tier specificity_bomb analogs at v3:** Historia Civilis "Longest Year 46 BCE" (3.7x mega), Atun-Shei Revolutionary War (10.9x peer), Shaun "Bell Curve" (3.5x mega, document-first read from source), Atun-Shei "Cornerstone of Johnny Reb" (primary-source-frame), TikHistory Southport (8.7x peer)
- **Clip-slot decision precedent:** 0/6 corpus clip-led debunks open cold with foil clip; closest stylistic twin "How Johnny Harris Rewrites History" drops first foil clip at 0:38
- **User rationale:** v3 choice-ignorant rerun against expanded corpus confirmed v2 verdict and resolved clip-slot gap simultaneously; B-tight over B-v2 for tighter Rule 19 / Sub-rule B compliance; "this is how i want research to be done for everything"
- **Memory linkage:** `feedback-corpus-expansion-loop.md` (new, derived from this run); strengthens `feedback-choice-ignorant-rerun.md`
- **System health signal:** Adding 8 sources did NOT flip the verdict — desired behavior. Verdict-holds-under-expansion = corpus trustworthy.
- **POST-GRILL AMENDMENT 2026-05-24:** Same-day grill-with-docs session reclassified this run as **WEAK SIGNAL** under the newly-added disconfirmation sub-rule. 5/8 expansion sources were verdict-confirming (document-first / primary-source-frame analogs); a truly disconfirming expansion would have included successful narrative-first or scene-first historians to test whether specificity_bomb verdict survives antagonistic additions. The B verdict is probably correct, but the methodology as run didn't *prove* it. Future /opener runs must include ≥1/3 disconfirming sources per amended `feedback-corpus-expansion-loop.md`.
- **Also via grill:** title was iterating not locked → 3-title rotation locked instead (see `YOUTUBE-METADATA.md`); cold-open Auditor's Edge red flag (mothers/children wording mis-attribution) resolved via Option B Beazley verbatim rewrite; Dum Diversas 1452 integrated as ~15s mention into Romanus Pontifex beat (same operative Latin phrase as 1455 — strengthens iterative-legal-architecture claim).
