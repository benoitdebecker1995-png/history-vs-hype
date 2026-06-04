---
name: Topic-first packaging, angle-first research
description: The channel's packaging-first workflow applies to TOPIC selection only. Within a locked topic, the specific ANGLE must emerge from research before title/thumbnail.
type: feedback
originSessionId: 19d344f9-1eb5-43d1-b2b9-e9964c7bc06f
---
The channel's documented Packaging-First Workflow (CLAUDE.md) — search demand → title generation → thumbnail concept → THEN research — applies to **topic selection**, not to within-topic angle selection.

Once a topic is locked via composite scoring (the small-channel rubric), the **specific angle** inside that topic must emerge from primary-source research BEFORE title and thumbnail are locked. Pre-locking an angle (e.g., "There Was a Time Limit" for Spanish Inquisition) before reading the actual primary documents risks:
- Forcing facts to fit the pre-locked narrative (violates Earn-Your-Inclusion Rule)
- Missing a stronger single-document forensic case in research
- Writing a title the script can't deliver on (thumbnail-mismatch retention failure pattern)

**The split:**

| Decision | Order | Why |
|---|---|---|
| Topic | Packaging-first (search demand → title concept → /greenlight → research) | Search-anchored channel needs head-term keyword anchor; can't tell if research investment is worth it without packaging viability |
| Angle within topic | Research-first (Phase 1 → Phase 2 → thesis emerges → title) | Thesis Discipline procedure requires the ≤12-word throughline to be derived from sources, not imposed on them |

**Operational rule:** when scoring rubric produces a winning topic, run a VidIQ unicorn-finder on sub-niches WITHIN the topic to inform research priorities — but do NOT lock the specific angle title until Phase 2 NotebookLM round-trips through primary documents.

**Origin:** 2026-05-08 weekend test, post-rubric-lock. Spanish Inquisition won the composite. User flagged that pre-locking the within-topic angle (e.g., "Torture Time Limit") before reading Torquemada's Instrucciones in primary research would invert the proper ordering. Confirmed: thesis must emerge from research per existing Thesis Discipline canonical procedure.

**When NOT to apply:** Pure follow-up videos in an established series where the angle is fixed by series convention (e.g., Untranslated Evidence series — angle is always "the document English-language coverage doesn't translate"). For one-off topic tests, research-first on angle.

## Minimum gate stack for title lock (added 2026-05-10)

The existing rule says angle must emerge from research before title locks. The minimum gate stack that satisfies this:

1. `/comment-mine` on top 3-4 competitor videos — validates audience-demand alignment for the angle
2. VidIQ keyword research — confirms a search anchor exists for the title
3. NotebookLM citation grounding — the title's mechanism word must be grounded against primary documents in the project notebook (LOW confidence = soften the word or pause for source acquisition)

All three gates must clear before title locks. Comment-mine alone is insufficient — it validates demand but not documentary support. NotebookLM alone is insufficient — it validates sourcing but not search viability.

**Failure example — Adwa #39 (2026-05-10):** Title locked to "Italy Forged the Ethiopia Treaty" from a grill hypothesis. User demanded research gates. Phase 1 NotebookLM grounding showed "forged" (document fabrication) was technically inaccurate — the actual mechanism is deliberate translation discrepancy + false-equivalence clause. Even the softened "Italy Rigged" + "Empress Taytu Caught It" claims were unsupported in current Phase 1 sources (McLachlan documents the discrepancy as "unclear cause"; does not credit Taytu with discovery). Running the gate stack first would have caught this before the grill spent time on a technically wrong title candidate.
