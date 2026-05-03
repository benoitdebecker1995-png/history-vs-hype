# Wave 2 Competitor Script Analysis — Continuation Prompt

Paste this into a new context window to continue extraction.

---

## Context

I just completed a competitor script structure analysis pipeline. Here's what was done:

1. **Rules 41-46 encoded** into `.claude/agents/script-writer-v2.md` (now v10.0) — source uncertainty hierarchy, steelmanning mechanics, forward causal connectors, visual staging cues, modern relevance bridge phrases, post-quote analysis (7 patterns)
2. **Constraints AA-AF added** to `.claude/agents/structure-checker-v2.md`
3. **NotebookLM notebook created** — "Competitor Script Structure Analysis — Wave 2" (ID: `438186cd-045e-40b1-ae67-9ecf25fcb415`) with 21 competitor video transcripts + 3 prior analysis docs
4. **3 scripts audited** — Thermopylae, Bakassi, Brazil. Biggest systemic gap: modern relevance bridges (7-min and 6-min gaps in middle acts)

## Task: Continue NotebookLM Extraction

The notebook has 7 analysis prompts saved as a note (title: "Analysis Prompts — Wave 2 Structural Extraction"). I ran Prompts 1 and 2 (post-quote analysis + uncertainty/causal chains/gaps). 

**Run the remaining 5 prompts against the notebook:**

- **Prompt 3:** Steelmanning mechanics — intro phrases, duration, transition phrases
- **Prompt 4:** Causal chain connectors — full inventory, longest chain, missing connectors  
- **Prompt 5:** Visual staging cues — verbal patterns triggering visuals, missing patterns
- **Prompt 6:** Modern relevance bridges — exact phrases, spacing, techniques for ancient history
- **Prompt 7:** Gap analysis — what competitor patterns are NOT covered by Rules 41-46?

**For each query result:**
1. Extract any NEW patterns not already in Rules 41-46
2. If new patterns found, add them to the relevant rule in `script-writer-v2.md`
3. Update corresponding constraint in `structure-checker-v2.md` if needed

**Then:** Write the consolidated Wave 2 findings to `tools/benchmark/WAVE-2-STRUCTURAL-FINDINGS.md` in the same format as `NOTEBOOKLM-STRUCTURAL-FINDINGS.md`.

**NotebookLM notebook ID:** `438186cd-045e-40b1-ae67-9ecf25fcb415`

**Key files:**
- Script-writer agent: `.claude/agents/script-writer-v2.md` (Rules 41-46 at the end, before REASONING FRAMEWORK)
- Structure-checker: `.claude/agents/structure-checker-v2.md` (Constraints AA-AF in the summary block)
- Prior findings: `tools/benchmark/NOTEBOOKLM-STRUCTURAL-FINDINGS.md` (45-video, sections 1-17)
- Prior findings: `tools/benchmark/TRANSCRIPT-STRUCTURE-ANALYSIS.md` (85-video quantitative)
- Prior findings: `tools/benchmark/SCRIPT-PATTERN-ANALYSIS.md` (15-transcript qualitative)

**What Prompts 1-2 already found (don't duplicate):**
- 3 new post-quote patterns added to Rule 46: narrative continuation, emotional mirroring, single-word decode
- Uncertainty phrases confirmed matching Rule 41 hierarchy
- HC and FoC make uncertainty interesting; Three Arrows uses it as disclaimer (apologetic)
- Longest causal chain: OverSimplified Emu War (10-step economic collapse)
- No major structural gaps found beyond existing rules — but Prompts 3-7 haven't run yet
