---
name: rule-research-verification
description: "How facts get verified and filed here — the two-phase method (never skip NotebookLM), source tiers, red flags, graded claim status, and the rule that a database figure carries its table, grain and as-of or is not quoted. Use when: opening or editing any 01-VERIFIED-RESEARCH.md, 03-FACT-CHECK-*.md, anything under _research/ or research/; filing a claim; quoting a source or a number from analytics.db; or asserting that something does not exist. Load it BEFORE filing. Does NOT cover script voice (→ rule-script-writing)."
---

> **Codex note.** Port of `.claude/rules/research-verification.md`, which stays canonical. On Claude
> Code this loads automatically whenever a research or fact-check file is opened. Codex has no
> glob-scoped auto-load, so **load this yourself before filing a claim or quoting a figure**.
> Governs: `**/01-VERIFIED-RESEARCH.md`, `**/03-FACT-CHECK-*.md`, `**/_research/**`, `research/**`.

# Research and fact-checking

## Two-phase approach (CRITICAL)

**Phase 1: Internet research** — map landscape, identify claims to verify (Wikipedia, news, Google Scholar). All findings marked ❓. Free, 2-4 hours.

**Phase 2: NotebookLM academic verification** — university press books ONLY (Cambridge, Oxford, etc.), top scholars, critical editions. Budget UNLIMITED. Upload 10-20 sources, use citation grounding for exact page numbers. Output: verified quotes ready for script.

**NEVER skip Phase 2.** That's the competitive advantage. See: `.claude/REFERENCE/NOTEBOOKLM-SOURCE-STANDARDS.md`

## Source hierarchy

See `.claude/REFERENCE/fact-checking-protocol.md`
- Tier 1: Primary documents, peer-reviewed (2010+), expert historians
- Tier 2: Journalists, intl org reports, declassified docs
- Tier 3: News sources (verify multiple), documentary evidence

**Red flags requiring immediate verification:**
- "The court ruled X..." → Which paragraph? Exact quote?
- "The treaty says..." → Which article? Exact language?
- Any quote without page number → Verify with primary source

**NEVER include unverified claims.** If you can't verify: don't include it, flag it, or ask user for source.

See: `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md` for 8 anti-oversimplification rules

## Claim status is graded, not binary

`ASSERTED → SOURCED → INSPECTED → CORROBORATED/CONTESTED → SETTLED`. Verdict words
(REFUTED/PROVEN/RESOLVED) only at CORROBORATED+. Check with
`python -m tools.preflight.claim_status <file.md>`; `--frontier` says whether research is actually
finished. ADR-0021.

**Never assert absence without a direct check.** A search returning nothing proves nothing. If an ID
or URL was supplied, query THAT. ADR-0020.

**A figure quoted from a database carries its table, its grain and its as-of — or it is not quoted.**
The same evidentiary burden, applied to instruments. "Median impressions is 56" is not a fact; "median
impressions is 56 in `videos`, a trailing snapshot stamped `ctr_as_of = 2026-07-28`" is. Lifetime and
snapshot answers to the same question differ by ~50× on this channel.

- **Route through the seam.** `AnalyticsStore.lifetime_ctr_by_video()` for how a video actually did;
  `snapshot_ctr_by_video()` for the recent window. Both stamp every row with `grain`, `as_of` and
  `source_table`. Hand-rolled SQL against `analytics.db` is how this goes wrong — ADR-0017 exists
  because six consumers each re-implemented one read and five got it wrong.
- **Check the ADRs before deriving a metric.** ADR-0018 (impressions grain), ADR-0017 (canonical CTR
  read), ADR-0012 (filters decide, scores inform). The principle you need has usually already been
  written down.
- **A score is not evidence until it is calibrated.** `title_scorer`'s composite correlates with
  lifetime CTR at r ≈ +0.155. Quote the number if useful; do not treat a high one as validation.

*Origin: 2026-08-03. Three strategy conclusions — a 56-impression median, a "bimodal CTR" shape test,
and "the title scorer is anti-predictive" — were published off the snapshot column read as lifetime,
and were caught by the channel owner rather than by any gate.*

**Intellectual honesty** — acknowledge what the opposing side gets right. Single source of truth is
`01-VERIFIED-RESEARCH.md`. Gate: 90% verified before writing; 100% cross-checked before filming.
