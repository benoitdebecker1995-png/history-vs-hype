# Fix our CTR problem — the program
**2026-07-22, for Codex. You diagnosed it and red-teamed it; now turn it into an executable plan. You read this repo but can't write it — return the program in chat, I implement the code/doc changes.**

## Where things stand (so you build on the right base)

- **The measurement bug you found is fixed in code.** `ctr_tracker._dedup_reports_by_interval` now collapses YouTube's regenerated reach reports to one per interval before the 30-day window, so the double-count (#59 rolling 20,919 > lifetime 10,925) can't recur. Tested. ⚠ The *existing* snapshots (07-13, 07-23) are still polluted until the next authenticated `ctr_tracker` run overwrites them — so for this program, **CTR ground truth = the fresh Studio CSV** (`channel-data/analytics-exports/`, 2026-07-23, 57 videos), never the current rolling snapshots.
- Your Phase 2 findings, the #59 teardown, and the doctrine corrections are the raw material below. Don't re-derive them; build the program.

## What "fix our CTR problem" means here

Two halves, both in scope:
- **A. Make CTR reliably measurable going forward** — so we can actually tell if a packaging change worked. Part done (dedup). You spec the rest.
- **B. A prioritized, single-variable improvement program** — the packaging changes most likely to recover clicks, in order, each independently testable.

## Deliver these

### 1. Finish the measurement fix (spec, I implement)
Your Phase 1 gave four validation steps; step 1 (dedup) is done. Specify the rest precisely enough to code:
- The rolling≤lifetime assertion — where should it live (a guard in `ctr_tracker` after aggregation? a test?), and what does it compare against, given lifetime only exists in the Studio CSV?
- The `views.py` redundant-override retirement: exact change, which consumers to re-verify, and how to prove no regression. Confirm the traffic-source merge stays.
- Whether the Studio CSV should get a real importer + timestamped table (so "is CTR fresh" is checkable and surface_ctr stops silently rotting), or stay a conversational read. Recommend one.

### 2. The improvement program (the core deliverable)
A ranked list of packaging experiments. For each, exactly:
- **Target**: which video(s) / which future-video rule.
- **Single variable**: the one thing that changes (title OR thumbnail element, never both).
- **Hypothesis**: grounded in your fresh-data findings, stated as a prediction.
- **Priority**: recoverable clicks (impressions × CTR gap) × your confidence. Starved videos (<500 lifetime impressions) are ineligible — they can't be measured.
- **Measurement**: Studio impressions post-change, the ≥500-impression threshold, and roughly how long to wait.

Lead with the #59 title test you already designed (`Israel vs Palestine. The 1947 UN Plan Wasn't Legally Binding.`, thumbnail held constant) — that's experiment #1.

### 3. Doctrine reconciliation (as doc-change proposals I apply)
The fresh data contradicts parts of `tools/PACKAGING_MANDATE.md` and memory `reference-ctr-packaging-playbook`. Turn each into a proposed edit, marked `CONFIRMED` (fresh data supports, adequate n) or `HYPOTHESIS` (directional, n<30 — needs a live single-variable test before it changes doctrine). Your findings to reconcile:
- **Evidence-promise in title** +3.91% vs 2.41% (n=8) — strongest title lever. Keep/strengthen.
- **Document-as-thumbnail-focal-point NEGATIVE** (2.39% vs 3.12%) — directly contradicts the mandate's "document focal point." ⚠ Separate this cleanly from "evidence promise in the *title*" (positive) — they are different variables and the mandate conflates them.
- **Busy thumbnail negative; red-emphasis not a reliable lever** — retire "red pop" as a universal prescription; "reduce elements before adding a device."
- **Maps positive but confounded** (topic-correlated) — don't prescribe.
- **Colons/years**: fresh data shows colon titles slightly beat declaratives and the year sample is n=2 — reinforces "graded penalty, not ban" (already Tier-2 in the mandate, but state it's now channel-data-supported).
- **`surface_ctr` is Feb-2026-stale and missing #59** — the mandate cites it as current surface data. Factual fix: flag its vintage everywhere it's cited.
- **Named-entity ≠ fame**: the weak named-entity signal doesn't validate OR falsify the "famous parent keyword" doctrine — the feature is a poor proxy. Say so; don't overclaim either way.

### 4. Guardrails the program must respect (channel rules, non-negotiable)
- **Single variable per test** — your own doctrine correction flagged that bundling a title+thumbnail swap below 2% breaks causal learning. Enforce it.
- **Filters decide, scores inform** (ADR-0012) — the program proposes tests, it doesn't declare winners from correlations.
- **n<30 = directional** — every channel-only finding is a hypothesis until a live single-variable test confirms it. Prefer niche-wide evidence where the channel n is too thin.
- **CTR is title+thumbnail only** — retention/opener is a separate lever, out of scope here.

Return: the measurement-fix spec (§1), the ranked experiment program (§2), the doctrine edits (§3). Keep every experiment to one variable and every doctrine change tagged CONFIRMED/HYPOTHESIS.
