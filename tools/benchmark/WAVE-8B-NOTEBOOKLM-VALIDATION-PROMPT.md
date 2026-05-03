# Wave 8B: NotebookLM Validation Prompt

**Copy-paste this into a new Claude Code conversation to validate Wave 8 findings across the full transcript corpus.**

---

## Prompt

I just completed Wave 8 competitor analysis (`tools/benchmark/WAVE-8-SCRIPT-TECHNIQUES.md`) — 20 transcripts from 6 channels, producing 5 new rules (55-59) and 3 constraints (AX-AZ). Now I need to validate and deepen these findings using NotebookLM's semantic search across the full transcript corpus.

You have a NotebookLM MCP server connected. Use `mcp__notebooklm__notebook_list` to find the transcript/benchmark notebooks, then run these queries with `mcp__notebooklm__notebook_query` or `mcp__notebooklm__cross_notebook_query`:

### Query Set 1: Validate Rule 55 (Rebuttal Architecture)

1. "Find every instance where a creator reads their opponent's own cited source against them. Extract the exact phrasing used to introduce the source-flip move."
2. "Find every instance of a hypothetical concession — where the creator grants the opponent's premise then shows the conclusion still fails. What phrases signal the concession?"
3. "Find all passages where anomalies or problems are listed sequentially to build overwhelming weight. How many items before the creator states the conclusion?"

### Query Set 2: Validate Rule 56 (Mid-Video Second Hook)

4. "Identify structural restarts or second beginnings that occur between 30-60% of total runtime. What signals the restart — new character, new location, new question, or topic shift?"
5. "Find all instances of hypothetical scenarios that are later revealed to be real historical events. How long is the hypothetical section before the reveal?"

### Query Set 3: Validate Rule 57 (Character Introduction)

6. "How do creators introduce historical figures for the first time? Find introductions that use career trajectory, personality traits, or modern comparisons rather than Wikipedia-style biographical data."
7. "Find all instances of deadpan humor or deflation immediately after introducing a historical figure's accomplishments."

### Query Set 4: Validate Rule 58 (Data Delivery)

8. "Find every statistic or number that is immediately followed by a comparison, analogy, or 'so what' explanation. What connector phrases bridge the number to its meaning?"
9. "Find statistics presented WITHOUT comparison or context. Are these in higher or lower performing videos?"

### Query Set 5: Validate Rule 59 (Pre-Teaching Frame)

10. "Find all video openings where the creator discusses a seemingly unrelated topic before revealing the actual subject. How long is the pre-teaching section? What connects the frame to the real topic?"

### Query Set 6: New Extractions (Gaps Wave 8 Agents May Have Missed)

11. "What phrases do creators use to transition from historical narration to modern relevance? Extract the exact bridge sentences."
12. "Find all instances where a creator explicitly acknowledges the limits of their own knowledge or expresses genuine uncertainty. What effect does this have on the surrounding argument?"
13. "How do the highest-view videos handle their final 2 minutes differently from average videos? Extract closing patterns from the top 5 videos by views."

### Output

Write findings to `tools/benchmark/WAVE-8B-NOTEBOOKLM-VALIDATION.md`. For each query:
- Confirm or challenge the Wave 8 finding
- Add new examples not found by the agents
- Note any patterns that contradict the proposed rules
- Extract specific phrases that should be added to the style guide

Then update `WAVE-8-SCRIPT-TECHNIQUES.md` with any corrections or additions. If a rule needs modification based on the validation, note what changed and why.
