# More findings like the retention one
**2026-07-23, for Codex. You read this repo but can't write it — return findings in chat; each one verifiable so the main thread can re-check before the creator acts.**

## What made the last finding worth having (the template — match it)

The retention finding — "the winner/loser gap is decided by 20%, and the recurring seam is the 5–10% post-hook handoff" — was valuable because it was **(a)** mined from an untapped source (`retention_curves`), **(b)** it overturned a standing assumption ("intro drop is universal and unfixable"), **(c)** it *located* the problem (a specific band, not a vibe), and **(d)** it was reproducible from the data. It was verified independently and held (r20 quartiles 48.7 vs 27.8).

Find **more of that class.** Not more of the same topic — the same *quality*: non-obvious, data-grounded, assumption-challenging, and actionable. A finding that overturns something the channel currently believes is worth more than one that confirms it.

## The seed — a real puzzle already on the table

Retention does **not** predict distribution. Spearman(avg_view_percentage, impressions) ≈ **0.0** across 58 videos. So holding viewers better doesn't get you pushed more — yet distribution is the channel's documented #1 bottleneck (only 3/47 ever broke 2K views; 27/56 die not-clicked; `memory/analytics-distribution-not-retention`). **So what DOES predict getting pushed?** That is the highest-value question on the channel and nobody has answered it with the clean data. Even a rigorous null is useful.

## Untapped data (real columns — mine these, don't guess)

- **`subscribed_status`** (115 rows: video_id, status, views, watch_time_minutes, **avg_view_percentage**) — retention split by subscriber vs non-subscriber. **The freshest high-value angle:** do NON-subscribers (the people you convert) drop earlier/harder than loyal subs? If the 5–10% seam is worse for non-subs, that beat is costing you *new audience* specifically — a sharper, more strategic version of the retention finding.
- **`search_terms`** (153 rows: video_id, term, views) — what searches actually bring people. Which topics pull search vs none; demand the channel ranks for but under-serves; whether search-heavy videos share a title trait.
- **`traffic_sources`** (528 rows: source_type per video) — browse vs suggested vs search share. Cross with CTR and retention: does the bottleneck differ by *how* a video is found? (A browse-fed video and a search-fed video may need different fixes.)
- **`opener_retention`** (21: hook_archetype, first_30s_retention, intro_drop_30s) and **`thumbnail_features`** (47: doc/cf/em/map/busy/red) — already partly mined; only go here if you find something the CTR/opener runs missed.
- **CTR now clean** — `studio_ctr_rows` (lifetime, July-23) + `videos` cache. Safe to correlate.

## What to produce

3–6 findings, each in this shape:
- **The claim**, one sentence.
- **The evidence** — the exact query/metric and the numbers, so it can be re-run and verified.
- **What assumption it challenges or confirms** (challenging is more valuable).
- **The action it implies** — single-variable, or "measure X before deciding."
- **`n` and `CONFIRMED` / `HYPOTHESIS`** — CONFIRMED only if the sample supports it and it survives an obvious confound check.

Prioritize: (1) anything that explains **distribution** (what gets a video pushed), (2) the **subscriber-vs-non-subscriber** retention split, (3) **search discoverability** patterns.

## Guardrails (non-negotiable — a finding that ignores these is worse than none)
- **The Guatemala distortion is everywhere.** One video is ~49% of all impressions and a huge share of views. Any channel-level aggregate is dominated by it — report with-and-without Guatemala, or use medians, or you'll "discover" Guatemala wearing a different hat. This is the #1 trap; the last run's impression bucket totals already got skewed by it.
- **n < 30 = directional; n < 10 = anecdote.** Tag honestly. Prefer niche-wide evidence where the channel n is thin.
- **Correlation is not a lever.** With 58 videos and heavy topic confounds, everything is correlational — say so, and frame actions as tests, not verdicts (filters decide, scores inform, ADR-0012).
- **Distinguish "holds viewers" from "gets pushed" from "gets clicked"** — three different outcomes with three different fixes. The retention finding is a HOLD lever and does not touch distribution (ρ=0.0). Don't let a distribution finding masquerade as a retention one.
- **Don't re-derive** the CTR §2 program, the opener scan, or the retention-curve bottleneck table — build past them.
- **Verifiable or it doesn't count** — every number must come with the query that produced it.

## Out of scope
- #62 (film-ready, hands-off).
- No new data pulls — everything is already in the two DBs.

Return the findings ranked by (leverage × how much they'd change what the creator believes).
