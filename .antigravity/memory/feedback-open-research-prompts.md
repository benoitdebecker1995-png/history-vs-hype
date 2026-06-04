---
name: Keep research-delegation prompts open — don't pre-load the candidate list
description: When routing landscape-scan research to an external agent (Gemini, NotebookLM, web search), the brief states the thesis + evaluation criteria but NOT a pre-selected candidate list. Pre-loading the list collapses the search into hypothesis-validation and filters out unknown stronger candidates.
type: feedback
originSessionId: 2026-05-12-asmongold-greenlight
---

# Open Research Prompts — Hypothesis in Criteria, Not in Candidate List

**Rule:** When delegating landscape-scan research (Gemini bulk read, NotebookLM exhibit search, WebSearch competitor scan, etc.), the prompt contains:

- The thesis or question being answered
- The evaluation criteria the answer must satisfy
- The output format

It does **NOT** contain a pre-selected candidate list of expected answers.

**Why:** Pre-loading candidates collapses the search from "find the strongest X" to "evaluate these 4 X's." The agent rank-orders my pre-list and skips the genuinely-stronger candidate I didn't think of. Born from #56 Phase 1 exhibit-selection prompt (2026-05-12) — initial Gemini prompt named four specific exhibits (Zurara, papal bulls, Thornton-cited letters, Slave Voyages data) for Gemini to evaluate. User flagged: *"why not keep the prompt as open as possible, for whatever is the strongest antidote against the right wing thesis."* Correct critique — Las Casas, Royal African Company charters, Hawkins's logs, Treaty of Alcáçovas, Casa da Guiné records etc. were all filtered out by the pre-load.

**How to apply:**

1. Write the thesis + criteria + output format. Stop there.
2. If you have hypothesis candidates, list them at the bottom as "starting points the researcher should NOT treat as constraints" — or omit entirely and let them appear if they survive open search.
3. The agent's first job is enumeration (what exists in this space), second job is ranking (which is strongest by your criteria), third job is shortlisting for downstream verification.
4. Trust the agent's enumeration. If 3 of your hypothesis candidates don't make the shortlist, that's a signal — not a prompt-broken signal.

**When NOT to apply:** Targeted lookups where you already know the document and want it located ("find the URL for the Beazley & Prestage 1896 Hakluyt edition on Internet Archive"). Those are retrieval, not landscape scan. Pre-load fine.

**Sibling rule:** [[feedback-topic-vs-angle-ordering]] — angle within a topic emerges from research before title locks. This rule is the same principle applied one level deeper: within the research phase, the specific exhibit / source / document emerges from the open scan, not from the pre-Phase-1 brief.

**Connects to:** [[feedback-tool-discovery]] (check what exists before proposing new); [[feedback-vibes-test-framing]] (don't pre-lock fallback topics for the user).
