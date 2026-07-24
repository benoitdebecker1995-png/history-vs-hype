# Opener-Principle Validation — Do the Borrowed Principles Predict OUR Retention?

**Generated:** 2026-06-26
**Scorer under test:** `tools/research/opener_diagnostic.py`
**Data:** `opener_retention` table (n=21 published long-form, joined to `videos.title`)
**Outcome variable:** `first_30s_retention` (range 0.511–0.715, mean 0.606)
**Method:** manual Spearman rank correlation (stdlib only, ties-averaged) of each
diagnostic signal vs `first_30s_retention`; binary signals also reported as
pass/fail group means + delta.

---

## ⚠️ READ THIS FIRST — what this is and is not

**n=21 is below the n<30 noise floor.** This is **DIRECTIONAL, not proof.** Per
`memory/feedback-channel-data-too-small.md`, a single-channel sample this small
cannot bless or kill a principle — niche-wide data does that. What this exercise
*does* do is set **how much authority each imported principle earns** when we wire
the scorer into `/opener`: a principle that shows the *right-direction* signal here
gets to speak with a slightly louder voice; one that shows *no* signal or the
*wrong* direction gets demoted to advisory / idea-generator and flagged for an
explicit A-B test before we ever weight it.

**Confounds (all push toward "directional only"):**
- These 21 are heavily territorial/geopolitical. The top retainers (Guatemala,
  Venezuela–Guyana, South China Sea) are **search-anchored** topics — 30s retention
  is plausibly driven more by topic/intent-match than opener craft.
- `first_30s_retention` is the **right** yardstick for first-30s mechanisms (anchor,
  gap-timing) but the **wrong** yardstick for whole-video sustain principles
  (macro-gap / slow-burn) — those are flagged accordingly below.
- Several binary signals have a pass-cell of n=3–5. A "correlation" off 3 videos is
  a rumor, not a result.

**Where a principle we "knew" was true shows no signal, this doc says so plainly and
does not massage it.** The biggest such finding is the headline below.

---

## HEADLINE FINDING

**The composite SUCCES score does NOT track our retention: Spearman rho = +0.005
(n=21) — flat.** It also fails to reduce intro-drop (SUCCES vs `intro_drop_30s`
rho = −0.034). The best-retaining video (Guatemala, 0.715) scores SUCCES 4; a
SUCCES-5 opener (Cyprus, 0.543) sits near the bottom while a SUCCES-2 opener
(Venezuela–Guyana, 0.713) sits near the top. **Do not weight the composite as a
predictor.**

**Exactly one principle earns its authority:** **anchor specificity** — a
named person/date/place in the first 10 words. rho = **+0.45**; openers that pass
average **0.647** retention (n=7) vs **0.586** for those that fail (n=14),
delta **+6.1 pts**. Its SUCCES sibling, *Concrete-in-sentence-1*, corroborates
(rho +0.38, delta +4.6 pts).

**The brief's #1-ranked Tier-1 levers — gap quality and gap-timing — show no
support here, and gap-timing points the wrong way.** This *inverts* the
OPENER-MASTERY-BRIEF §2 hierarchy (which ranked gap #1, anchor #2) on our own data.

---

## Signal table (Spearman vs first_30s_retention, n=21)

| Signal | type | rho | pass n / mean | fail n / mean | delta | Tag |
|---|---|---|---|---|---|---|
| **named-entity in first 10 words (ANCHOR)** | binary | **+0.45** | 7 / 0.647 | 14 / 0.586 | **+0.061** | **HOLDS** |
| Concrete-in-sentence-1 (SUCCES) | binary | +0.38 | 10 / 0.630 | 11 / 0.584 | +0.046 | HOLDS |
| framework anomaly+stakes+inciting | cont. | +0.23 | — | — | — | weak+ |
| sentence-1 word count (longer→) | cont. | +0.20 | — | — | — | wrong-way for "short" rule |
| prerequisite-knowledge *(heuristic)* | binary | +0.16 | 12 / 0.613 | 9 / 0.597 | +0.016 | INCONCLUSIVE |
| surprise-relates-to-argument *(heuristic)* | binary | +0.15 | 5 / 0.622 | 16 / 0.601 | +0.021 | INCONCLUSIVE |
| **composite SUCCES score (0-6)** | cont. | **+0.005** | — | — | — | **DOESN'T (flat)** |
| Unexpected / schema-break (SUCCES) | binary | −0.06 | 9 / 0.601 | 12 / 0.610 | −0.009 | DOESN'T (flat) |
| hockey-stick-risk (fulfillment) | binary | −0.12 | 17 / 0.602 | 4 / 0.622 | −0.020 | INCONCLUSIVE (no variance) |
| s1 ≤13 words | binary | −0.16 | 10 / 0.594 | 11 / 0.617 | −0.023 | DOESN'T (wrong dir) |
| gap-feels-painful *(heuristic)* | binary | −0.18 | 3 / 0.579 | 18 / 0.610 | −0.031 | INCONCLUSIVE (n=3) |
| sentence-1-parses-cleanly | binary | −0.20 | 17 / 0.599 | 4 / 0.634 | −0.035 | INCONCLUSIVE (no variance) |
| macro-gap-present (Eves slow-burn) | binary | −0.31 | 6 / 0.576 | 15 / 0.618 | −0.042 | INCONCLUSIVE (wrong metric) |
| **gap-by-sentence-3 (TIMING)** | binary | **−0.34** | 4 / 0.566 | 17 / 0.615 | −0.050 | **DOESN'T (wrong dir, n=4)** |

*Positive rho = signal-pass associates with HIGHER first-30s retention (the
expected direction for every principle here).*

---

## Per-principle verdicts

### 1. Composite SUCCES score (0-6) — **DOESN'T**
rho **+0.005**, n=21. Flat against retention and flat against intro-drop (−0.034).
Six independent necessary-conditions summed into one number washes out — the
strong signal (anchor) and the dead signals (gap-timing, schema-break) cancel.
**This is the principle we most "expected" to work, and it does not.** Said plainly:
the scorer's headline number is an idea-generator, not a predictor.
→ **Recommendation: advisory-only. Never display/rank by the composite as if it
forecasts retention.**

### 2. Anchor — named person/date/place in first 10 words — **HOLDS** (directional)
rho **+0.45**, the strongest signal in the set; +6.1-pt mean gap, n=7 vs 14, right
direction. Corroborated by Concrete-in-s1 (+0.38, +4.6 pts) and the continuous
framework-anomaly score (+0.23). Top three retainers all pass it. This matches the
channel's standing rule that every title needs a head-term keyword anchor
(`feedback-starting-channel-search-anchored.md`) — specificity up front is the
through-line.
→ **Recommendation: weight-in (lightly). This is the one opener lever the data
supports; foreground it in `/opener` output.**

### 3. Gap-opening timing — gap named by sentence 3 — **DOESN'T**
rho **−0.34**, *wrong direction*: the 4 openers that pass average 0.566 vs 0.615 for
the 17 that don't. Pass-cell is only n=4 (KGB, Thermopylae, Cyprus, India–Pakistan —
three below mean), so this is "no usable signal" more than "proven inverse." Either
the principle doesn't transfer to our search-anchored topics, or our best openers
win via a cold-fact/specificity mechanism the gap-by-3 detector doesn't credit.
Either reading says: **do not treat early-gap-timing as a retention lever here.**
This directly contradicts OPENER-CRAFT-BRIEF §3's "compression correlates with
retention" claim on our own sample.
→ **Recommendation: drop as a weighted lever; keep as craft advice; A-B-test going
forward (single-variable: gap@s2 vs gap@s6 on matched topics).**

### 4. Schema-break / Unexpected — **DOESN'T**
rho **−0.06**, delta −0.009 — flat. Whether the opener trips a schema-break marker
is uncorrelated with first-30s retention on our channel. A Tier-1 principle in the
brief, invisible in our data.
→ **Recommendation: advisory-only (it has genuine craft value); do not weight;
A-B-test.**

### 5. Sentence-1 mechanics (≤13 words / parses-cleanly) — **DOESN'T (≤13) / INCONCLUSIVE (clean)**
The "≤13 words" rule runs the *wrong* way: pass mean 0.594 vs fail 0.617 (rho −0.16),
and continuous word-count is mildly *positive* (+0.20) — our top openers have 16-,
21-, 23-word first sentences. "Parses-cleanly" can't be read: 17/21 pass, no
variance. The McKee/1of10 short-sentence-1 prescription does not hold here.
→ **Recommendation: drop the ≤13-word hard rule; keep read-aloud/stumble-test as
advisory only.**

### 6. Hook-archetype group means — **INCONCLUSIVE**
cold_fact 0.624 (n=10) · specificity_bomb 0.616 (n=5) · myth_contradiction 0.627
(n=1) · **unknown 0.555 (n=5)**. Per-cell n is tiny and myth=1, so the *ranking* is
unreadable — and per memory rule, archetype ranking is niche-wide's job, not ours.
The one suggestive note: openers the scorer **couldn't classify ("unknown")**
retain ~7 pts worse than classifiable ones. Directional only.
→ **Recommendation: advisory-only; defer archetype ranking to niche-wide data;
treat "unknown archetype" as a soft yellow flag, not a score.**

### 7. Drop pattern (`intro_drop_30s`) — **DOESN'T (vs composite)**
SUCCES vs intro-drop rho −0.034 (target: strongly negative). A higher composite does
not buy a smaller intro drop. Same verdict as #1, measured against the drop metric
instead of the retention level.
→ **Recommendation: advisory-only.**

### 8. Heuristic checks (gap-painful, prerequisite-knowledge, surprise-relates) — **INCONCLUSIVE**
These were honestly labelled `heuristic=True` in the scorer, and the data confirms
caution was right: gap-painful trips on only n=3 openers; prereq (+0.16) and
surprise-relates (+0.15) lean the right way but off pass-cells of 12 and 5 with
tiny deltas. No cell is big enough to read.
→ **Recommendation: advisory-only; keep the heuristic labels; revisit at n≥40.**

### 9. Eves macro-gap / slow-burn — **INCONCLUSIVE (wrong outcome metric)**
rho −0.31 against first-30s, but **this principle is about whole-video sustain, not
the first 30 seconds** — first_30s_retention is the wrong yardstick for it. The
negative sign here is expected noise, not a refutation.
→ **Recommendation: A-B-test against *full-curve / 50%-point* retention, never
first-30s. Do not judge it on this metric.**

### 10. Hockey-stick / title-fulfillment check — **INCONCLUSIVE (mis-calibrated)**
17 of 21 openers get flagged hockey-stick-risk → almost no variance, so it can't
correlate. The check (`_check_fulfillment`, first ~50 words) is likely too strict
for our keyword-heavy titles.
→ **Recommendation: advisory-only; recalibrate the fulfillment threshold before
trusting it; re-validate after recalibration.**

---

## One-line recommendations (for the `/opener` wiring decision)

| Principle | Verdict | Wiring recommendation |
|---|---|---|
| Anchor (named entity in first 10 words) | HOLDS | **weight-in** (lightly) — the one supported lever |
| Concrete-in-sentence-1 | HOLDS | weight-in (same family as anchor) |
| Composite SUCCES score | DOESN'T | advisory-only — never present as a forecast |
| Gap-opening timing (gap by s3) | DOESN'T | drop as a lever; A-B-test |
| Schema-break / Unexpected | DOESN'T | advisory-only; A-B-test |
| Sentence-1 ≤13 words | DOESN'T | drop the hard rule; read-aloud advisory |
| Hook-archetype ranking | INCONCLUSIVE | advisory-only; defer to niche-wide |
| Heuristics (painful/prereq/surprise) | INCONCLUSIVE | advisory-only |
| Eves macro-gap / slow-burn | INCONCLUSIVE | A-B-test vs full-curve retention, not 30s |
| Hockey-stick / fulfillment | INCONCLUSIVE | recalibrate, then re-validate |

**Net:** wire `opener_diagnostic` into `/opener` as an **idea-generator / advisory
lint**, with **only the anchor-specificity signal** earning a (light) weighted
voice. The composite score and the brief's gap-first hierarchy do **not** earn
predictive authority on our n=21 — surface them as craft prompts, and resolve them
the only honest way for a small channel: single-variable A-B tests going forward.

---

*Validation run 2026-06-26. Read-only over `analytics.db`. Spearman computed with a
stdlib ties-averaged implementation (no scipy/numpy). Per-row scoring and group
means reproducible via the scorer + `opener_rows()`/`video()`. Directional evidence
only — n=21 < the n<30 noise floor.*
