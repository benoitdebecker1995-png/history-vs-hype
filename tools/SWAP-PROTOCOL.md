# 48-Hour Swap Protocol

**Purpose:** Systematic reaction to underperforming videos within the critical first 48 hours.

**Trigger:** Run at 48 hours post-publish for EVERY video. Use `/analyze [video-id]` to get performance data, then apply this protocol.

---

## Important: 48h Velocity Does NOT Predict Lifetime Views

**Source:** VELOCITY-ANALYSIS.md (2026-03-21, n=48 videos)
**Finding:** Pearson r=0.163 — no meaningful correlation between 48h views and lifetime views.
Delayed-push videos average 1,917 lifetime views vs 544 for front-loaded (3.5x).
"The Country That Might Disappear" got only 73 views in 48h but reached 29,011 lifetime (397x).

**Implication:** The 48h swap trigger should focus on **CTR and impressions**, not raw view count. A video with low views but decent CTR (>4%) may simply be waiting for an algorithm push. Only swap when CTR is poor (<2%) WITH sufficient impressions (>500), confirming YouTube tested and viewers rejected the packaging.

## Step 1: Pull Metrics

From YouTube Studio (manual) or `/analyze`:
- **New-viewer CTR** — the metric to judge on. 98% of views are non-subscribers and
  new-viewer CTR (~3%) runs well below returning-viewer CTR (~7%); blended CTR hides
  the cold-audience gap the packaging must win. Use new-viewer CTR where Studio breaks
  it out; fall back to blended only if it doesn't.
- **Impressions** (how many times YouTube showed the thumbnail)
- **Dominant traffic surface** (Suggested / Browse / Search) — this picks the lever (Step 3)
- **AVD** (average view duration), **Views**

## Step 2: Diagnose (V5 thresholds, 2026-06-14 live data)

The algorithm throttles fast — inferred ~1.3% first-48h CTR is the "keep getting pushed"
floor; sub-1% plateaus within 24-48h. Judge on **new-viewer CTR**.

| New-viewer CTR | Impressions | Diagnosis | Action |
|----------------|-------------|-----------|--------|
| <1.3% | >500 | **Throttling now** — tested and rejected | SWAP **one lever** immediately |
| 1.3-4% | >500 | **Below potential** | SWAP **one lever** to lift |
| <1.3-4% | <500 | **Early or suppressed** — check search volume | Wait / re-check at 7 days |
| >=4% | Any | **Working** | HOLD — don't fix it |

## Step 3: Pick ONE lever (single-variable doctrine)

**Change the thumbnail OR the title, never both.** CTR is one blended number
(title + thumbnail + topic); if you change two things you can't attribute the move, so
you learn nothing. The surface tells you which lever:

- **Suggested / Browse-dominant** → swap the **thumbnail** (thumbnail-dominant surface).
- **Search-dominant** → swap the **title** (keyword/title-dominant surface).
- A thumbnail swap read on a Search-heavy video (or vice-versa) reads dirty — match the
  lever to the surface.

**Log the swap before you wait** so the before/after delta is tracked, not lost to prose:

```
python -m tools.swap_ledger open --video <id> --variable thumbnail \
    --baseline-ctr 1.91 --baseline-impr 2672 --surface Suggested --read-in 21d \
    --old "<old>" --new "<new>" --note "<why>"
```

## Step 3b: Generate the alternative arm

Generate ONLY the lever you picked in Step 3 — leave the other untouched.

**If swapping the TITLE** (Search-dominant):
1. Run the existing title through `title_scorer.py --db` — see why it underperforms.
2. Score backups in YOUTUBE-METADATA.md; generate new candidates.
3. Pick the highest-scoring candidate that (a) anchors the primary search keyword in
   the first ~40 chars, (b) uses a **different pattern** than the failing title (so it's
   a real alternative arm), (c) scores 65+. Note: colon/year/the-X-that are HEDGE flags,
   not disqualifiers — don't "remove the colon," change the pattern.
4. If the title changes, update the first 3 lines of the description to match.

**If swapping the THUMBNAIL** (Suggested/Browse-dominant):
1. Build the new thumbnail to `.claude/REFERENCE/THUMBNAIL-CRAFT-RECIPE.md` (cut-out +
   saturation pop + ONE red accent at the focal point + ≤3 huge words + REAL subject —
   no AI-generated figure).
2. Gate the rendered PNG through `python -m tools.preflight.thumbnail_image_audit` —
   it must pass the **feed-size legibility** check (the one image-computable failure).
   CLIP differentiation is informational only (ADR 0007).
3. Run the concept through `thumbnail_checker.py` for the curiosity-gap filter (the
   overlay must not duplicate the title). Don't leave the title unchanged AND make the
   overlay restate it.

## Step 3c: Native A/B (Test & Compare) — PARKED at current traffic

YouTube's Test & Compare is the only verdict that truly isolates the thumbnail, but it
needs more impressions than this channel's uploads currently get to reach significance
(0 of the last 12 uploads ever ran one). **Until traffic grows, learn via the
single-variable before/after swap above**, not A/B. When a video does pull enough reach,
prefer Test & Compare over a manual swap. (See ADR 0007 + the packaging-overhaul plan.)

## Step 4: Execute + log

1. Change the one lever in YouTube Studio (title OR thumbnail).
2. **Log it in the swap ledger** (this is the system of record — not a prose SWAP LOG):
   ```
   python -m tools.swap_ledger open --video <id> --variable thumbnail \
       --baseline-ctr <pre> --baseline-impr <pre> --surface <Suggested|Search|Browse> \
       --read-in 21d --old "<old>" --new "<new>" --note "<why>"
   ```
3. The ledger regenerates `channel-data/SWAP-LEDGER.md` automatically.

## Step 5: Read the result + learn

When the experiment comes due (`python -m tools.swap_ledger list` flags it **DUE TO
READ**), pull the post-swap **new-viewer CTR** from Studio and close the loop in one step:

```
python -m tools.ctr_quick_add "<title>" --ctr <new> --views <v> --impressions <i> --swap-read <experiment_id>
```

This ingests the CTR datapoint AND computes the experiment's delta + verdict
(LIFT ≥ +0.5pp / FLAT / DROP). On a **LIFT**, it prints a paste-ready line for the
proven-recipes appendix in `THUMBNAIL-CRAFT-RECIPE.md` so the win compounds into the
operation priors. A FLAT/DROP means the problem is likely deeper (topic demand,
retention) — don't keep swapping the same lever.

---

## SWAP SCHEDULE

| Timing | Action |
|--------|--------|
| Publish | Monitor first 2 hours for obvious issues |
| 48 hours | Diagnose (Step 2) on new-viewer CTR; if <1.3% on >500 imp, swap ONE lever now |
| At swap | Log the experiment in `swap_ledger` |
| ~21 days | `swap_ledger list` flags it DUE; read with `ctr_quick_add --swap-read` |
| 30 days | Bulk review (`packaging_autopilot`) — back-catalog single-lever swaps |

---

## NEVER SWAP

- Videos performing >4% CTR (don't fix what's working)
- Videos less than 24h old (insufficient data)
- Videos during a current-events spike (wait for organic to settle)

---

*This protocol replaces "hope and wait." Every video gets a 48h checkpoint.*
