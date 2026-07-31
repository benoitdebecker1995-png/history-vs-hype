# ADR-0021 — Research claims carry a graded status, not a binary "verified"

**Date:** 2026-07-30
**Status:** Accepted
**Extends:** ADR-0020 (strategy claims carry the same evidentiary burden as on-screen claims)
**Related:** ADR-0012 (a rule that must bind goes in code, not prose) · ADR-0007 (filters, not scores)

## Context

Project #66 (Churchill / Bengal famine) produced an unusually strong primary-source haul in a single
session — six documents, the full War Cabinet decision chain, 25 rendered exhibits. It also produced
**seven reversals in that same session**:

1. R1 marked **REFUTED**, then qualified when contrary evidence appeared in a later volume.
2. A source declared to have **"no text layer"** — actually a path bug on our side; the file was
   never opened.
3. A duration finding ("cut to under 8 minutes") published, then **retracted** when the underlying
   bucket turned out to be contaminated by a channel-intro video and five zero-conversion entries.
4. "Three purchases remain" → **seven**, once the list was ranked by *what the video could get wrong*
   rather than *what finishes the project*.
5. A source marked **FREE** from a search hit; its metadata said `access-restricted-item: true`.
6. "The hinge no longer blocks scripting" — **withdrawn**; it contradicted the project's own
   academic-sourcing standard.
7. The research "hinge" declared **RESOLVED** using one commission's supply tables to adjudicate a
   dispute *about the reliability of that commission's supply tables*. Circular.

None of these were dishonest; each was corrected in the open. But the aggregate behaviour is a
research process that oscillates, and the owner named it: *"you are all over the place and not acting
like a real research team."*

**The root cause is vocabulary, not diligence.** The repo's verification marks were binary —
`✅ VERIFIED` / `⏳ PENDING` / `❌ FAILED` (see `.claude/templates/03-FACT-CHECK-VERIFICATION-TEMPLATE.md`,
where ✅ and ❌ account for 72 of the 90 status marks). A binary vocabulary has no rung for *"I have
read this in one source and it is not yet corroborated"* — which is the true state of most findings
at the moment of discovery. Faced with ✅ or ⏳, a researcher who has genuinely just read a document
marks ✅. The retraction is then structurally guaranteed.

Notably, the *most valuable* state in this project — **CONTESTED**, where good historians disagree —
had no representation at all in a ✅/❌ scheme. That is the state this channel exists to portray.

## Decision

**Research claims carry a graded status with a defined evidence threshold at each rung, enforced in
code.**

```
ASSERTED      someone says it; no verification (a model's output, a comment, a summary)
SOURCED       traced to a named source WITH a locator — not yet opened by us
INSPECTED     we opened the source and read the passage; locator + date recorded
CORROBORATED  INSPECTED + a SECOND INDEPENDENT source agrees
CONTESTED     INSPECTED + a named source disagrees — a status, NOT a failure
SETTLED       CORROBORATED + the strongest opposing case has been read and answered
```

`CONTESTED` and `CORROBORATED` carry **equal evidential weight**. A contested claim is strong; it is
simply not closed.

**Five binding rules**, implemented in `tools/preflight/claim_status.py`:

| Rule | Requirement | The #66 failure it catches |
|---|---|---|
| **R1** | Verdict words (REFUTED/PROVEN/RESOLVED/DISPROVED/CONFIRMED/ESTABLISHED/SETTLED) only at CORROBORATED+ | #1, #6, #7 |
| **R2** | A claim whose only support is the body whose reliability is in dispute (`circular:`) caps at INSPECTED | #7 |
| **R3** | INSPECTED and above require a locator — page, section, archive ref, or identifier | #2, #5 |
| **R4** | SETTLED requires a named opposing case (`opposed-by:`) and where it was read | — |
| **R5** | Nothing below CORROBORATED goes on screen | (script gate) |

Run: `python -m tools.preflight.claim_status <file.md>` — exits non-zero on violation.
`--ladder` prints the vocabulary.

## Consequences

- **The vocabulary makes the honest state expressible.** A researcher who has read one document can
  now mark INSPECTED and move on, instead of choosing between overclaiming and understating.
- **Verdict language becomes expensive**, which is the intent. Writing REFUTED now requires naming a
  second independent source.
- **Circularity becomes declarable.** `circular:` is a first-class annotation rather than an error
  someone notices three days later.
- **`03-FACT-CHECK-VERIFICATION-TEMPLATE.md`'s binary marks are superseded for research files.** The
  fact-check stage (script line vs verified research) may keep ✅/❌ — it is a different question,
  asked after the research is settled. **Do not migrate the template silently**; that is a separate
  change with its own ADR if pursued.
- **Migration cost is real and deliberate.** #66's `01-VERIFIED-RESEARCH.md` currently uses ✅/⏳ and
  scores `claims: 0` under the new checker. Existing research files are *not* retro-tagged wholesale;
  they are tagged when next edited. The checker still catches untagged verdict words — on first run
  against #66 it independently flagged *"THE HINGE — RESOLVED"*, the exact claim that had to be
  retracted.
## Amendment, same day — the two process failures, also closed in code

The first version of this ADR named two failures it did **not** fix and left them open. Both
recurred in the same session, so both are now enforced.

### A. "Why did you stop?" — a checkable definition of done

Research was reported finished twice while obtainable sources remained unread; the owner had to ask
twice. There was no definition of "done" to violate.

**Decision:** a research phase is **not finished while any claim below CORROBORATED still has an
available, untried route to raise it.** Claims below CORROBORATED carry `next: <action>`, or
`next: none — <reason>` to declare the thread genuinely closed.

`python -m tools.preflight.claim_status --frontier <file.md>` reports:
- **UNTRACKED** — below CORROBORATED with no `next:` at all (the silent-abandonment case)
- **OPEN THREADS** — with the action that would raise them
- **CLOSED** — declared `next: none`

Verdict `OPEN` exits non-zero: *"research is NOT finished. Do not report completion."*
Claims at CORROBORATED or above are excluded — they are not frontier items.

### B. Collision checks move from prose to code

`.claude/PROMPTS/blind-next-video-discovery.md` has mandated a collision check against published
titles and project folders since it was written. On 2026-07-30 it was ignored twice: a *"NATO
promised not to expand"* video was proposed and screened at length before the owner pointed out it
was **already published** (`499YLd1BHZ4`, 2025-09-10, 52 views).

**Decision:** `tools/preflight/candidate_preflight.py`. Checks `analytics.db` titles plus all four
lifecycle folders including `_BACKLOG/`.

- **PUBLISHED match → `COLLISION`**, exit non-zero. Hard stop absent an explicit override.
- **Project-folder match → `FLAG`**, exit zero. Per the discovery brief an existing project is
  eligible on merit — but the proposal must say so.
- Matching requires **≥2 content words** to co-occur (stopwords dropped), so a single shared word is
  not a false positive.

Verified against the actual failure: the NATO topic returns `COLLISION` with the video ID and date.

**Run it before proposing a candidate, not after.**

### C. Idea provenance — `--origin`

Four candidates were generated from the assistant's own recall, screened against each other, and a
winner announced; the self-generated shortlist was never disclosed. The owner named it:
*"keep an open mind pls."*

**Decision:** `candidate_preflight --origin {frame|catalogue|audience|data|owner|recall}`.
`recall` is **not forbidden — it is required to be stated**, so the reader can discount it, and it
prints: *"SELF-GENERATED… A shortlist you invented and then judged is not a screen."* Same principle
as `circular:` in R2: make the weak state declarable rather than invisible.

### D. Hyperbole — `--tone`

*"Everything is the next best thing or the strongest find."* Chat cannot be linted; **written
deliverables can**, and those are the half that persists in the repo.

**Decision:** `claim_status --tone <file.md>` counts three families — superlative, awe, intensifier —
against a house budget of **one superlative claim per project** (CLAUDE.md § Calibration).

Run against the file that prompted this: **10 superlatives, 5 intensifiers, verdict OVER**, with
`"strongest"` used five times for five different things.

⚠ **Signal, not a gate.** Quoted source material inflates it — two of those ten were quotations from
the Cabinet minute and from Wavell. Read the hit list, do not just read the count.

### Still not covered

None of this addresses *judgement* — proposing a candidate that is unwise rather than duplicated,
choosing the wrong hinge question, or hyperbole in conversation as opposed to in files. These
enforce that cheap mechanical checks actually run, and make weak states declarable. **They are not a
substitute for the owner saying "you are all over the place."** That remains the only signal that
caught most of this.

### Wiring (the part that was nearly missed)

Building the tools and invoking them from nothing would have repeated the exact failure they exist
to prevent — the collision rule sat unenforced in prose for months. They are therefore wired in:

- **`/greenlight` Step −1** — `candidate_preflight`, before demand, on every invocation.
- **`/research` completion gate** — `claim_status --frontier` before reporting research finished.

## Alternatives considered

- **"Be more careful."** Not implementable, not testable, and demonstrably already the intent.
- **Extend `packaging_lock.py`.** Rejected: that gate is title/thumbnail-specific and its filters
  answer a different question. Per the extend-don't-add test, no existing surface carries
  responsibility for research-claim evidence thresholds — `verify.md` checks script lines against
  settled research, and the fact-check template assumes the research is already done.
- **Ratings rather than a ladder** (e.g. confidence 0–100). Rejected under ADR-0007: a score invites
  averaging and advocacy. These are necessary conditions, so they are filters.
