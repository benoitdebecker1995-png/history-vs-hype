---
name: Channel-specific data is not actionable at this scale
description: At 47 long-form videos, channel-specific CTR/outlier patterns (n<30) are NOT actionable. Only use niche-wide / large-corpus competitor data when making packaging decisions.
type: feedback
originSessionId: 42a2f8a3-b852-43b8-b1e0-c47ba3be594c
---
# Don't apply channel-specific data — sample size too small to be actionable

**Rule:** When making title, thumbnail, hook, or packaging decisions, do NOT cite channel-specific CTR data, outlier rates, or pattern penalties. The channel has 47 long-form videos — every channel-specific pattern is at n<30, often n<10. That's noise, not signal.

**Why:** At this scale, channel-specific patterns are dominated by execution variance, topic variance, seasonality, and small-n statistical noise. Examples of patterns I've previously cited that are NOT actionable:
- Year-in-title penalty -46% (n=8) → 8 mediocre executions could fully explain this
- Colon penalty -28% (n=10) → same problem
- Question penalty -36.3% (n=3) → labeled "directional only" in source data, but I treated as constraint
- Versus pattern 3.7% CTR (n=2) → cannot extract a pattern from n=2
- Face-rate 0% on thumbs → topic-confounded (territorial videos use maps, not faces)

User explicitly: "we are too small to have actionable data" (2026-04-25, project 51 Treaty of Tripoli title rotation).

**How to apply:**
- DO use: niche-wide patterns from competitor notebooks at large n (Wave 2: n=138 scale signals, n=85 video corpus, 388-title dataset, 650-thumbnail dataset). Outlier patterns from Wave 2 (two-sentence declarative 11% rate n=9 outliers from outlier corpus, specificity bomb 5.4x lift n=5, scale signal 1.33x n=138, authority 1.34x n=42).
- DO use: specific named outlier examples with view counts (Atun-Shei "Civil War Was A Slave Revolt" 482K, Historia Civilis "(46 B.C.E.)" 7.2M, Knowing Better "Part of History You've Always Skipped" 6.0M).
- DO NOT use: any channel-specific n<30 number as a CONSTRAINT or penalty.
- DO NOT cite: "channel-rule violation" / "channel-rule stress test" framing when the rule is just channel n<30.
- WHEN n>30 channel-specific eventually exists: treat as directional, not deterministic. Combine with niche-wide patterns.

**Stops:** Do not engineer titles to "deliberately violate channel rules" as a stress test. There are no reliable channel rules to violate yet. Engineer titles to match niche outlier patterns; that's the only signal that's actionable at 515 subs / 47 videos.

**Connection to existing rules:** Extends [Rules Hedge, Not Prescribe](feedback-rules-hedging.md) — that rule said competitor patterns are IDEAS not mandates. This rule says channel patterns aren't even ideas yet at this scale.
