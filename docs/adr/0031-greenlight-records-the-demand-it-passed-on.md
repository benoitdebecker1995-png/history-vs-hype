# ADR-0031: Greenlight records the demand it passed on

**Status:** Accepted — 2026-08-27
**Extends:** ADR-0028 (recommendation ledger), ADR-0029 (validate or label)

## Context

`.claude/commands/greenlight.md` Step 1 gates topic selection on measured search demand:
**GO ≥1,000/mo · CAUTION 500–999 · STOP <500**, with a verified live news hook overriding a STOP.

That threshold has never been checked against outcomes, and — unlike the `title_scorer` composite in
ADR-0029 — **it currently cannot be**, because the record needed to check it was never kept.

Attempting the check on 27 August 2026: of the 47 published videos with ≥1,000 impressions in the
Studio export, only **two** could be matched to a search volume recorded in `keywords.db`. The table
holds 138 keywords, last updated 3 August. Nothing links a greenlit video to the demand figure it was
greenlit on.

The two that could be matched both cleared the gate comfortably and underperformed:

| Video | Search volume | Views | CTR |
|---|---:|---:|---:|
| Berlin Conference | 11,648 | 443 | 3.66% |
| Operation Condor | 2,000 | 52 | 1.53% |

**n=2 proves nothing about the threshold.** It demonstrates the gap: the validation cannot be run at
all. That is the finding this ADR exists to fix.

**The conceptual limit matters as much as the missing data.** The demand gate answers *"will YouTube
serve this?"* Berlin Conference shows it working — 9,485 impressions, the audience was found. It
converted 3.66%. The gate cannot answer *"will anyone click?"*, and ADR-0029 establishes that the
click is the binding constraint. A passing demand score is a necessary condition, never a forecast.

## Decision

**Greenlight writes its decision to the existing `recommendation_ledger` before research begins.**

No new table. `recommendation_ledger` (keywords.db, added by ADR-0028) already has the right shape —
prediction fields recorded before the outcome is known, outcome fields completed later. It currently
holds **one row**. It was built for exactly this and has gone unused.

A greenlight record uses `decision_kind = 'topic_greenlight'` and the project slug, and must carry:

- **the measured volume and the term it was measured on**, in `rationale` — not "demand looks good";
  the number, the anchor term, and the date it was measured;
- **which band it fell in** (GO / CAUTION / STOP) and whether a news-hook override was applied, in
  `recommendation`;
- **what is expected to follow**, in `expected_observation` — the traffic mode and a first-week range
  worth betting on;
- **what this evidence cannot tell you**, in `evidence_limitations` — at minimum, that measured demand
  predicts serving, not clicking.

The 7- and 28-day review completes `outcome`, `outcome_as_of` and `revised_confidence` — including
the honest verdict **"uninformative"** when impressions were too low to read.

**The threshold stays where it is in the meantime.** ≥1,000/mo is not being changed on the strength of
two data points. It is being made *answerable*, so that after a handful of uploads there is something
to check it against. Until then it carries the same status ADR-0029 gives any unvalidated number: use
it as a filter, never report it as a forecast.

## Consequences

Validation is several videos away, not immediate. That is the cost of a record that was never kept,
and there is no shortcut — the same conclusion ADR-0030 reached about testing titles on the back
catalogue.

`tools/discovery/performance_tracker.py` and `schema_manager.py` already touch this table; the write
belongs on the existing seam rather than in a new module.

**Also recorded, so it is not rediscovered:** `intel.db` is stale — competitor videos last refreshed
10 August, comment signals 29 July — and nothing refreshes it on a schedule. Competitor-gap and
comment-demand work runs on month-old data unless refreshed first. That is a separate gap from this
one and is not fixed here.
