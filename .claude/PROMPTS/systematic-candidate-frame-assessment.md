# Can candidate discovery be made systematic? — assessment brief

## The question

History vs Hype needs weaponised historical claims that lack a public referee. Four independent
discovery passes ran on 2026-07-29/30 (one interactive, one GPT Deep Research, two blind cold agents).

**Measured result:** 45 distinct candidates surfaced. Capture-recapture (Chapman estimator) on the two
largest samples (n=26, n=19, overlap 4) gives **N̂ ≈ 107**; pooled prior-three against the last blind
pass gives **N̂ ≈ 85**. So roughly **half the space has been found, and the space is on the order of
100 candidates — finite and tractable, not unbounded.**

Both known biases push that estimate upward: the passes shared a brief (not fully independent), and
famous claims are more catchable than obscure ones. Treat ~100 as a floor.

**Screening is cheap; generation is the bottleneck.** Testing a named candidate costs ~5 minutes
(vidIQ demand + `serp_title_study` referee sweep + full-catalogue check of likely referees). Every pass
so far generated candidates ad hoc — from a model's own recall, or from open-web searches that return
commentary rather than enumerable lists.

## Your task

Determine whether candidate generation can be made **systematic** — driven by enumerable sampling
frames rather than recall — and if so, specify the pipeline.

### 1. Find the sampling frames

Identify concrete, enumerable corpora where weaponised historical claims are already listed, indexed
or catalogued by someone else. For each, establish:

- **What it is** and who maintains it
- **Size** — how many discrete claims it contains
- **Access** — API, scrape, purchase, manual; blocked or open
- **Hit-rate estimate** — what fraction would plausibly meet the brief (live weaponisation + referee
  gap + auditable exhibit), with your reasoning
- **Overlap** with the 45 already found, where you can tell
- **Cost per 100 claims screened**

Hunting grounds worth assessing, non-exhaustively: edited scholarly volumes that debunk political
myths by chapter; historiographical-controversy reference works and companions; fact-checking
organisations' history verticals; academic literature on public memory, negationism and history
textbook disputes; parliamentary and congressional hearing records where historians testify;
university public-history "myth" series; encyclopaedia list-articles of historical controversies;
partisan media series that make serial historical claims (each episode = one indexed claim); and
retraction/erratum literature where a widely-cited historical estimate was later disputed.

Assess each honestly. If a frame is inaccessible, unreliable or low-yield, say so and drop it.

### 2. Answer the feasibility question directly

Is systematic enumeration achievable, or is this space inherently sample-based? Give a yes/no with
reasoning. **A clear "no, keep sampling, here is the best sampling strategy" is an acceptable and
valuable answer** — do not manufacture a pipeline that won't work.

### 3. If yes, specify the pipeline

- Ordered stages from frame → shortlist, with the kill criterion at each stage
- What is automatable versus what needs judgement
- Expected yield: how many frame entries produce one greenlight-grade candidate
- Total cost to screen the estimated remaining ~55
- Where it would break

### 4. Say when to stop

Given N̂ ≈ 85–107 and ~45 found, at what point does further discovery stop paying? Marginal new
candidates per pass will fall as overlap rises. Name the stopping rule.

## Constraints

- **Verify claims about sources.** If you assert a corpus has N entries or is API-accessible, check it.
  Do not assert absence without naming the instrument — a search returning nothing proves nothing
  (see `docs/adr/0020-*`).
- Do not propose anything requiring paid data the channel doesn't have. Budget for academic *sources*
  is unlimited; budget for tooling and data subscriptions is not.
- Available: WebSearch/WebFetch, YouTube Data API, vidIQ MCP, `serp_title_study`, local SQLite.
- Be adversarial about your own recommendation. The failure mode is an elegant pipeline nobody runs.

## Deliver

1. **Verdict** — systematic, semi-systematic, or sample-only, with reasoning
2. **Ranked frames table** — the fields from §1, best first
3. **The pipeline** if warranted, or the best sampling strategy if not
4. **Stopping rule**
5. **What you could not verify**, named explicitly

Write to `G:\History vs Hype\research\active\CANDIDATE-FRAME-ASSESSMENT-2026-07-30.md`.
Reply ≤200 words. Final line exactly: `OUTPUT: <absolute path>`
