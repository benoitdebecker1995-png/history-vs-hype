---
name: Research Deep Audit Method
description: Systematic pre-filming research audit — 4 vulnerability categories, targeted NLM prompts, human verification flags. Developed after Bakassi gaps.
type: feedback
originSessionId: ecb6fa6a-5beb-40b9-a747-90a2d77bdb76
---
Before filming, run a deep audit on verified research using 4 vulnerability categories learned from Bakassi:

1. **Single-source claims** — any fact resting on ONE secondary author. Find a second source or hedge it
2. **Citation chain risks** — quote chains (Script → Author A → Original). Verify the original exists and says what Author A claims. The Bakassi Macdonald Aug 1894 problem
3. **Framing/logic risks** — fact is correct but framing oversimplifies (e.g., projecting 1649 trade goods onto 1626, using Western legal terms for non-Western systems)
4. **Missing context** — things a knowledgeable viewer would raise that the script doesn't address

5. **Primary accessibility** — claim is verified via secondary source (Kamen p. X, Hassner p. X) but the original primary document was never acquired. These CANNOT go as [ON SCREEN] evidence — they're secondary-sourced. Options: add primary to notebook, reframe as VO with scholar attribution, substitute procedurally-equivalent primary (see `feedback-auditors-edge.md` — source substitution discipline), or cut. Inquisition #54 failure: converso writer quote (only in Kamen, not the 1538 Toledo document), María de Carvajal trial records, Díaz de Cáceres records — all shipped without primary document acquisition. They appeared in edited video as secondary-sourced content, weakening the auditor's edge.

**Why:** Bakassi had 5 corrections needed after NLM audit (unverified quote, misdated deed, misframed war, logic gap). The fact-check passed on paper but real scrutiny found holes. The deep audit catches what the standard fact-check misses.

**How to apply:** After 03-FACT-CHECK-VERIFICATION.md passes, create RESEARCH-DEEP-AUDIT.md with targeted NLM prompts for each vulnerability. Prioritize: closing quotes (highest embarrassment risk) and central claims (highest impact if wrong). Include human verification flags for things NLM can't check (book existence, exhibition dates, original publications).

**Source tier tagging (added 2026-05-14):** In 03-FACT-CHECK-VERIFICATION.md, every claim must carry a source tier tag alongside the ✅/⏳/❌ status:
- **[P]** — primary document accessible, verbatim quote in notebook. Can go [ON SCREEN].
- **[S]** — verified via secondary source only. Primary document NOT acquired. Cannot go [ON SCREEN]. Must appear as VO with scholar attribution, use source substitution, or be cut.
- **[S→P]** — secondary source points to a named primary document; document not yet acquired. Action item: add to notebook before filming.

Any [S] or [S→P] tagged claim that appears as [ON SCREEN] in the script is a hard fail at the fact-check gate — flag it before filming, not during editing.

**Output:** 5 copy-paste NLM prompts (prioritized) + human verification checklist + source-tier tag audit. Run Priority 1 prompts before filming.
