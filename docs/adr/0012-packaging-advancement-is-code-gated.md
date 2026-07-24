# 0012 — Packaging advancement is code-gated, not instruction-gated

**Status:** Accepted (2026-07-01)

## Context

#62 (Volhynia) was locked "from /greenlight + VidIQ" and justified by a single confident number — **"VidIQ 95/100"** — with no record that `title_scorer`, `/curiosity`, or `thumbnail_checker` ever ran, and no thumbnail concept at all. Extends ADR 0007: the CTR audit that those tools encode is a set of **necessary-condition FILTERS** (confounded, "never auto-reject, learn via A/B"), not a clickability oracle — so the defect was **not** "ignored the audit." It was letting one confident enrichment number **stand in as the verdict without recording that the filters ran**.

The rule already existed in `greenlight.md` prose ("title MUST score ≥65 … thumbnail_checker in Step 3"). It didn't bind — a written step relies on the agent remembering to run it, and the agent skipped it. A written rule *about* the written rule (add a checklist line) has the same failure mode. Two latent bugs surfaced while building the gate: `has_search_anchor` didn't know "Zelensky" (a world-famous searchable figure, yet the recognizer false-FAILed the title), and the "clickbait brand gate" was **dead code** — the docstring promised `_apply_tone_filter` populated `hard_rejects`, but that function never existed, so clickbait titles scored clean.

## Decision

Packaging advancement is enforced by **code**, not by instructions:

- **`tools/preflight/packaging_lock.py`** runs the four **packaging filters** (search-anchor · clickbait brand-gate · title↔thumbnail curiosity gap · thumbnail conditions), records them plus the **enrichment** (title_scorer composite, /curiosity, VidIQ, NLM) in an `<!-- AUTO:packaging-lock -->` block in `PROJECT-STATUS.md`, and `--validate` returns BLOCKED unless every mechanical filter PASSES and the judgment field is filled. Enrichment can **never** upgrade a filter FAIL.
- **Model C (filters, not scores):** the `title_scorer` 65 and `/curiosity` 60 thresholds are **recorded enrichment with a REVIEW nudge**, not gates. No pre-publish number is a verdict except demand; live CTR is the only real one.
- **`/research` calls `--validate` before advancing a new project** and refuses if BLOCKED. `/reconcile` surfaces a **non-blocking flag** for grandfathered in-flight projects (created before 2026-07-01).
- **Root-cause fixes to `title_scorer.py`** (not worked around in the checker): the clickbait brand gate was restored (`detect_clickbait` populates `hard_rejects` → grade REJECTED); current world figures (Zelensky, Netanyahu, Bandera, …) added to the head-term recognizer.

## Consequences

- **Good:** the packaging discipline binds regardless of whether the agent remembers it; the clickbait guard is real (and doubles as the VidIQ-clickbait guard); a confident enrichment score can no longer masquerade as the verdict.
- **Cost:** a bit more machinery (a checker wired into two commands); the judgment fields (curiosity gap) still require a human/agent call — the gate enforces that the field is *filled*, not that the judgment is *correct*.
- **Reversible only by** demoting the gate back to prose — which is the exact failure this ADR exists to prevent.

See: ADR 0007, ADR 0009, CONTEXT.md (Packaging / thumbnail terms), `channel-data/CTR-TITLE-FORMULA-2026-06.md`, `memory/feedback-packaging-gate-authority.md`.
