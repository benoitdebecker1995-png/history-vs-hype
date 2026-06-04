---
name: Vibes-test framing for format experiments
description: When user proposes a new video format experiment, default to vibes-test framing with soft signals — not hard retention gates with controlled-experiment design
type: feedback
originSessionId: 19d344f9-1eb5-43d1-b2b9-e9964c7bc06f
---
When the user proposes an experimental new video format (compressed length, new structure, new opening pattern, etc.), they prefer **vibes-test framing** over controlled retention experiments.

**Why:** During 2026-05-07 weekend-test planning, user pushed back twice on rule-strict framing. (1) Q1 picked "vibes test at 5 min" over "controlled retention test at 6 min." (2) Q6 said "we can be a bit crazy with this video. its experiemental. more vibe bases" when asked whether the channel-wide 90s modern-relevance rule applied. Pattern: format experiments are for *feeling whether the format is sustainable*, not for proving statistical retention claims.

**How to apply:**
- Frame format experiments as VIBES TEST, not controlled experiment — don't insist on holding variables constant for clean inference
- Use **soft signals** (informative, not gates) for retention/CTR thresholds. Final call is user judgment after watching the cut + reviewing analytics, not auto-decided by a number.
- Channel-wide rules (modern relevance every 90s, pattern interrupt every 2-3 min, etc.) can be RELAXED for an experimental video if they fight the format being tested — flag the relaxation as a deliberate one-off, don't quietly drop the rule
- Don't pre-lock fallback topics for the user — if a planning gate fails, user picks at runtime, doesn't auto-default
- Don't write retention-threshold gates that auto-archive a format on a single test result — confound problems are common in vibes tests, give the user judgment latitude

**When NOT to apply:** Production decisions for already-validated formats (the existing 8-10 min Pilot Episode template, the Untranslated Evidence series). Those are operating under known constraints and the channel-wide rules apply normally.

## Test-reframe-on-divergence (added 2026-05-10)

When production results diverge >30% from test design parameters (runtime, length, format scope), update the test classification BEFORE shipping — not after.

A "5-min Format C compression test" that ships at 7:48 (+56% overshoot) is an **"8-min Format C close-read test."** These are different experiments with different lessons. Shipping under the original classification files the evidence incorrectly: future analytics on the video would be treated as "5-min compression evidence" when it's actually "8-min close-read evidence."

**How to apply:** When a video's final runtime diverges >30% from target, rewrite the test classification in PROJECT-STATUS.md and the post-mortem before upload. The lesson learned changes accordingly — don't let stale labels corrupt the data.

**Origin:** Inquisition #54 (2026-05-09) — shipped at 7:48 vs 5:00 target. Caught in 2026-05-10 grill. PROJECT-STATUS.md updated to "8-min Format C close-read test" before ship.
