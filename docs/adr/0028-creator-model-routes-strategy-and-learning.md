# ADR-0028: The creator model routes strategy and learning

**Status:** Accepted — 2026-08-14

## Context

The imported creator model correctly described editorial identity, voice, decisions, growth,
packaging and business viability. The historical front room already implemented its research and
voice requirements, but opportunity, packaging, business and performance requests fell through to
the historical claim-safety packet. The project also preserved package chronology without preserving
the recommendation, predicted mechanism or later confidence revision that made an experiment
learnable.

Older composite opportunity and packaging scores remain in the repository. They are useful migration
evidence, but conflict with the creator model when treated as verdicts.

## Decision

`channel-data/creator-model/OPERATING-MODEL.md` is the active strategy and collaboration authority.
`tools.front_room` now routes:

- opportunity to relevant creator criteria, dated matching market evidence and the recommendation
  ledger;
- packaging to the current script, creator criteria, chronological package history, the ledger and
  dated matching market evidence;
- business viability to creator criteria, dated channel evidence and the ledger;
- performance to the pre-publication reasoning, chronological package history, attributable dated
  metrics and a small same-topic cohort.

Add `recommendation_ledger` to the existing keyword database. Channel-wide recommendations use the
reserved internal scope `__channel__`; video-specific recommendations use the project slug. This
prevents workflow or business choices from being silently attached to whichever video happens to be
active. A record stores the recommendation,
rationale, predicted mechanism, expected observation, decision status and evidence limitations before
the outcome is known. The later outcome, observation date and revised confidence complete the chain.
It stores prose and provenance, not a score.

Composite scores and superseded strategy outputs remain preserved but are excluded from normal
front-room packets. Missing evidence remains visible instead of being replaced by a score.

## Consequences

- The creator model changes live behavior rather than merely documenting preferences.
- Channel strategy remains distinct from current-video state.
- Strategy recommendations can be audited against what was actually predicted.
- One result can revise confidence without becoming an automatic channel law.
- Performance claims cannot silently detach from the title and thumbnail viewers encountered.
- Legacy tools remain recoverable during migration but cannot become normal decision evidence through
  the conversational front room.
