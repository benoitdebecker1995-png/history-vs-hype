# Parties-with-mechanism title rule

**Date:** 2026-05-10
**Status:** accepted

At sub-1K subscriber count this channel is impression-starved (median long-form ~60 views, n=20). Audit of 2026's three above-median performers (Berlin Conference 439v, Tordesillas 788v, Somaliland 396v) and four sub-50 misses (Bakassi 10v, Tripoli 15v, Honduras 38v, Mexico Bermeja 12v) showed a clean split: winners led the title with a **mechanism word** ("split", "partition", "independence problem"); misses led with **named parties** the audience has no pre-loaded curiosity for ("Nigeria vs Cameroon", "Honduras...British Territory", "Treaty of Tripoli...").

**Rule:** country/treaty/named-party names are permitted in titles only when the rest of the title contains a mechanism word a non-specialist recognizes as the universal distortion. The audience doesn't search the parties — they search the mechanism. Bare party-vs-party titles are out until subscriber count grows the audience that pre-loads curiosity for specific geographies.

## Considered Options

- **Specificity-first** (the natural instinct from research): name the document, the year, the people. This works for an audience that already cares about the topic — i.e., what the channel will eventually have, not what it has now.
- **Universal-only**: drop named parties from titles entirely. Rejected because winners like "Somaliland's Legal Independence Problem" prove parties + mechanism can coexist, and dropping geography forfeits the channel's territorial-dispute lane.

The chosen rule is the synthesis: parties allowed iff a mechanism word carries the title alongside.

## Consequences

- All next-4 titles audited against this rule before lock. Hijab #52 passes (mechanism: "Forbidden to Wear" + "Mandatory"). Adwa #39 title OPEN — research + post-Slot-1 learning gate informs lock; "forged" candidate flagged as technically inaccurate per [Auditor's Edge — Primary > Scholar] (treaty wasn't forged; mechanism is *deliberate translation discrepancy + false-equivalence clause*). Haiti #21 stays locked despite weak explicit mechanism — sunk-cost protection on a 2026-03-12 approved title with VidIQ 92 and shipped newsletter alignment.
- Inquisition #54 exempt — VIBES TEST / Format C close-read experiment, not bound to channel-wide rules per memory rule [Vibes-Test Framing].
- Re-evaluate at n=10+ titles applying the rule. If outcome data refutes (mechanism-leading titles do not show impression lift), this ADR is superseded.

## Trial log

Append after each ship in plan `jiggly-sniffing-shamir.md`. Track: title, mechanism word(s), ADR exempt?, 28-day views + sub-conversion outcomes.

| Slot | # | Ship date | Title | Mechanism word(s) | ADR exempt? | 28d views | 28d sub-conv | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 54 | _pending_ | "The Spanish Inquisition Regulated Its Torture Methods. The Loophole Was in the Same Paragraph." | "regulated" / "loophole" | YES (vibes-test) | _pending_ | _pending_ | 8-min Format C close-read; first-test of mechanism rule at high abstraction |
| 2 | 52 | _pending_ | "The Veil Started as a Privilege Slaves Were Forbidden to Wear. Then It Became Mandatory for All Women." | "Forbidden to Wear" / "Mandatory" | NO | _pending_ | _pending_ | Native A/B rotation across 3 thumbnail variants |
| 3 | 21 | _pending_ | "Haiti Paid France for 122 Years. Here's Every Receipt." | "Paid" + scale signal "122" + specificity tail "Receipt" | NO (weak pass) | _pending_ | _pending_ | Locked since 2026-03-12; sunk-cost protected |
| 4 | 39 | _pending_ | _pending_ | _pending_ | NO | _pending_ | _pending_ | Title locks after research + post-Slot-1 gate |

**Refutation watch:** if 0 of slots 2/3/4 hit >500 views in 28 days, review this ADR. If 1+ hit >500, no claim — n still too small.
