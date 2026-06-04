---
name: Pre-Build During External Waits
description: When an external dependency blocks part of the work (Gemini, NotebookLM, user manual step, long bash), build everything that doesn't depend on the blocker in parallel. Don't sit idle.
type: feedback
originSessionId: acf6893b-dd34-4e58-89e9-9290f916aa55
---

# Pre-Build During External Waits

## The rule

When an external dependency blocks one part of the work, identify what doesn't depend on that blocker and build it in parallel. Don't sit idle waiting for the unblock.

## Why

2026-05-11 — while building `/editing-guide` for #54, hit Gemini Flash quota. User said *"give me the prompt, I will run it manually"* and offered to run Gemini themselves. I offered to pre-build the other 8 sections of the editing guide while they ran Gemini. User approved. Both finished in parallel; no idle wait. Final guide came together in one assembly step once Gemini output landed.

If I had waited for Gemini output before starting any composition, the user would have been idle while I sat ready to start, OR I would have been idle waiting for user to paste back. Either way, ~10 minutes of wasted wall time.

## How to apply

**Triggers when:** an external dependency blocks one part of the work. Common cases:

- Gemini Flash batched call (quota, rate limit, slow response)
- NotebookLM query (latency, auth refresh, rate limit)
- User manual step (*"I'll run that and paste back"*, fetch a PDF, verify a quote on a paywalled site)
- Long-running bash (build, fetch, large file processing)
- Background agent task

**Action:**

1. **Identify the blocker scope.** What specifically depends on the blocker's output? (Often only 1-2 sections of the final artifact.)
2. **Identify what doesn't depend on it.** Headers, structure, frontmatter, sections built from already-loaded inputs, analysis that can use current context.
3. **Offer to pre-build** in parallel — and propose specifically what (*"want me to pre-build sections 1, 2, 3, 5, 6, 7, 8, 9 while you run Gemini?"*).
4. **When the blocker resolves**, slot the result into the pre-built scaffold. Don't rebuild.

**Marker for blocker-dependent sections:** use a placeholder like `[GEMINI FILL — pending]` or `[USER OUTPUT — pending]` so the slot is obvious when integration happens.

## Counter-examples (when NOT to fire)

- The downstream work genuinely depends on the blocker (you can't pre-build a fact-check before the facts arrive)
- The blocker is fast (<30 seconds — wait for it, parallelism adds complexity for no gain)
- The pre-built sections would need to be rewritten depending on the blocker output (premature work, will be wasted)

The rule is about **identifying TRUE independence** — sections that can land cleanly once the blocker resolves, not sections that depend on the blocker's content shape.
