# Phase 3 — Retention Rule Adjudication (Fable, 2026-06-11)

**Input:** D3-retention-evidence.md (build 2026-06-11; analytics.db refresh 2026-06-10; RETENTION-SCRIPT-CORRELATION n=42; HOOK-RETENTION-CORRELATION n=17; 15-video cliff/hold dataset).
**Scope:** every retention/engagement rule in `script-writer-v2.md` (v16.6) + `structure-checker-v2.md` (Wave 10). Packaging rules (D3 inventory #30–41, #50) are Phase 1 jurisdiction — already re-tiered in `tools/PACKAGING_MANDATE.md` (commit fb53b97). Not re-adjudicated here.
**Tier definitions:**
- **VALIDATED** — own-channel retention evidence directly supports the claim at usable n; checker enforces HARD.
- **HEDGE** — directional, plausible, or niche-wide views-based; per [rules-hedge-not-prescribe], an idea not a mandate; checker flags SOFT (WARNING/SUGGESTION/INFO).
- **RETIRED** — number or mandate contradicted, confounded beyond use, or distortion-driven; the number is removed from rule text (the underlying craft practice may survive as HEDGE).

Verification standard (FABLE-PLAN §Phase 3): every change cites video ID + timestamp range or pattern-file source. No citation → HEDGE ceiling.

---

## 1. Headline findings (what the evidence actually says)

**F1 — The opening cliff is structural, not content-driven.** All 15 videos lose 24.6–91.4pp by 10% elapsed; in 11/15 the single largest step-drop sits at 2–5% elapsed. The cliff hits the strongest hook material in the dataset (GuL9PtXEjN0 Somaliland: dual −17.5pp cliffs at 00:06–00:20 ON "35 countries recognized then forgot" + "12% of global trade") exactly as it hits the weakest. **Implication:** rules claiming a specific opening tactic *prevents* the 2–4% drop are unfalsifiable from this data; the script-side lever in the cliff zone is limited to not parking the worst-measured content type there (F2). The real lever for the 10%-checkpoint level is click-intent match — packaging/topic (Phase 1's jurisdiction): winners enter 10% at 50.0–56.4% (Y21EjQ0v9W4, XbGl1Kcspt4, UH2PddfaaR8); losers at 25.7–38.3% (LuLZYZWMiU4, WgE2FLsDhfk, lFGs5NHMxMw).

**F2 — Early-zone personal-authority is the one content-type×position cell with validated damage.** personal_authority in the first ~13%: avg delta −0.051 (n=88 points); mid-video: −0.0001 (n=10 — the natural control). Direct hits: LO_fUeX9IEQ (Vance) −12.5pp at 00:15–00:18 landing ON "I went to the Vatican archives, I pulled up papal documents"; LuLZYZWMiU4 (Flat Earth) −25.2pp at 00:21–00:32 on the authority-classified beat (#3 worst single drop in the 42-video set). **Contradiction caught:** script-writer Rule 17 *mandates* an authority signal ("So I read/checked/found...") inside the hook — i.e., the rule-set required placing the worst-measured content type in the worst-measured zone. Fixed in v17.

**F3 — The myth-first "30.3% vs 22.4%" structure claim is the topic table relabeled.** Retention by topic: ideological 30.3% / colonial 22.4%. Retention by structure: myth-first 30.3% / chronological-colonial 22.4%. Identical numbers — because ideological videos are myth-first and colonial videos were chronological, the comparison cannot separate structure from topic. The structure *mandate* (Constraint U CRITICAL) rested on a confound. Myth-first stays the default for ideological topics (niche-wide corpus support, 85 transcripts), but the 8pp number is retired and the checker severity drops to WARNING.

**F4 — Statistics are the strongest validated content type; late-video statistics gain viewers.** 61% positive-rate (n=354 points); late-zone stats +0.001 avg delta (n=114). Genuine mid-video recoveries are rare and cluster on evidence/statistic beats (7fpBz6uo504 +0.4pp twice at ~25%/~34%; lFGs5NHMxMw +0.7pp/+0.5pp at ~21%/~29%). Promoted: a hard number in the final 20% becomes a checked default.

**F5 — Modern-relevance frequency mandate has negative evidence.** modern_relevance content type: −0.010 avg delta (n=577) — worse than plain narration (−0.005, n=1,654). The "every 90 seconds" rule had no stated n and the measured direction is mildly negative for *standalone* bridges. Retired as a frequency mandate; survives as "weave into narration, never standalone" (HEDGE).

**F6 — Late-quarter collapse is a distinct failure mode the rule-set never addressed.** 7fpBz6uo504 (I/P myths) −12.3pp across 75→100%; UH2PddfaaR8 (KGB) −15.1pp across 75→100%; _N_08zn95FY (Turkey islands) −7.2pp at 98–99%. Diagnostic from the 15-video set: absolute retention <20% at the 75% checkpoint predicts final-quarter collapse. New soft constraint (BF) + closing-third statistic default (F4). Observational, n=15 → HEDGE.

**F7 — Duration cap is the strongest surviving own-channel rule.** r=−0.455 (n=47), and the D3 top-15 corroborates: the three over-cap videos (WgE2FLsDhfk 12:49 → 16.86%; l8abBf4aMv8 14:39 → 23.09%; LuLZYZWMiU4 17:50 → 12.84%) rank 3rd, 13th, 15th worst. Confound acknowledged (long videos may be weaker topics) but signal is consistent across both datasets. Stays VALIDATED / HARD.

---

## 2. Verdict table (D3 Part-2 inventory numbering)

| # | Rule (short) | Verdict | Evidence basis | Action |
|---|---|---|---|---|
| 1 | Ad-lib retains +10% (0.351 vs 0.250) | HEDGE | n unstated; workflow benefit user-validated independently | Keep two-tier philosophy; tag number as unverified |
| 2–4, 21–22 | Duration r=−0.455; 8–12 sweet spot; 12–20 penalty | **VALIDATED** | n=47 + D3 corroboration (F7: WgE2FLsDhfk/l8abBf4aMv8/LuLZYZWMiU4) | Keep HARD (Rule 10, Constraint T CRITICAL) |
| 5 | 60/10 rhythm "validated across 39 videos" | HEDGE | No surviving methodology; retention curves can't resolve sentence-level effects | Keep as craft default; strike "validated" claim |
| 6 | First quote ≤90s "loses 15–25% and never recovers" | HEDGE | Confounded by F1 — ALL 15 videos lose 13–25%+ at 2–4% regardless | Keep early-evidence default (channel identity); rewrite evidence note; Constraint A CRITICAL→WARNING |
| 7–11, 45 | Hook-type retention hierarchy (36.7% → 24.6%) | HEDGE | Per-cell n: myth_contradiction n=4, contextual n=15, cold_fact n=19, specificity n=2 (Constraint I table); HOOK-CORR n=17 self-labels "directional" | Keep routing direction; annotate per-cell n; numbers no longer citable as hard data |
| 12 | Turn 15–25% = 3.2x; 25–35% dead zone | HEDGE | Niche-wide views (n=85; cells n=20/n=9); own-channel cross-validation (n=40, 2026-03-24) found NO 25–35% retention penalty | Rule 16 text aligned to Constraint E's hedge |
| 13, 42 | Myth-first 30.3% vs chronological 22.4% | **RETIRED (number)** / HEDGE (structure default) | F3 — identical to topic table; structure⊗topic confound | Strip the 8pp claim; Constraint U CRITICAL→WARNING; default survives on niche-corpus support |
| 14–15 | Territorial 2,449 avg views; ideological 179 / 2.31% sub rate | **RETIRED (views numbers)** / HEDGE (sub-rates) | Guatemala one-video distortion — Y21EjQ0v9W4 = 51% of channel traffic ([channel-traffic-distortion]) | Replace with distribution-aware note in Rule 14 |
| 16–17, 49 | WPM calibration (A/B 200, C 150) | HEDGE (working constant) | n=1 (#54 measured delivery) — a calibration measurement, not an inference | Keep operative; re-measure next Format C; n stays visible |
| 18 | Long quotes >30 words don't survive recording | HEDGE | n=2 (#45, #51/#52) | Already correctly marked; no change |
| 19 | 44% script survival (Constraint AV / Phase 4.5) | **RETIRED (stale)** | User-flagged 2026-06-11: predates two-tier scripting; v16+ two-tier target is 80%+ survival. Same root as the 1.80x filming buffer in Constraint T / STEP 0 — both replaced with the 1.20x two-tier formula (~3,600 words = 12 min Format A/B; Format C → Constraint BD budgets) | Removed from checker text |
| 19b | +10pp ad-lib retention (Constraint AV) | HEDGE | n unstated | Tagged in checker |
| 20 | First number by 101s | HEDGE | Niche-wide n=85 top/bottom split; BUT D3 counter-texture: lPilDVSAeEM −16.5pp at 00:18–00:25 ON Ferozepur canal-headworks hyper-detail; lFGs5NHMxMw −20.6pp at 00:16–00:21 ON "229 ethnic groups" stat-barrage | Keep SUGGESTION; add "one anchor number ≠ stats-dense barrage in the cliff zone" |
| 23–25 | 2026 trend (median 24.0%; chrono-colonial 16.7%; ideological 12.1%) | HEDGE | n=10 / subsets n<10 | Informational only (already Constraint V); tag n |
| 26 | 8+ "you" = overuse | HEDGE | No evidence cited | Already INFO; no change |
| 27 | 4+ consecutive ~25-word sentences = monotone | HEDGE | No evidence cited | Stays craft ISSUE; no severity change |
| 28 | Modern relevance every 90s | **RETIRED (frequency mandate)** / HEDGE (weave-don't-standalone) | F5: modern_relevance −0.010 (n=577) vs narration −0.005 | Checker "CRITICAL RULE" header demoted to guideline; woven-vs-standalone check stays |
| 29 | Document reveals spaced 30–70%; 3-min gap flag | HEDGE | No direct retention evidence; weakly consistent with F4 recovery texture | Stays SUGGESTION |
| 30–41, 50 | Packaging rules (years, colons, CTR, scoring gate) | — | Phase 1 jurisdiction | Already re-tiered in PACKAGING_MANDATE (fb53b97) |
| 43 | 2–4% = where 13–25% leave | **VALIDATED (as fact)** / RETIRED (as bridge-lever) | F1: universal in 15/15; bridge presence does not prevent it | Reframed as zone discipline; Constraint B CRITICAL→WARNING |
| 44 | Topic retention table (ideological 30.3 > territorial 28.5 > general 26.4 > colonial 22.4) | HEDGE | n<30 per cell; source of the F3 conflation | Annotate; never cite as structure evidence |
| 46 | Myth-narration skip (famous myths) | HEDGE | n=2, correctly marked | No change |
| 47 | Evidence-anchored close | HEDGE | n=2, user-confirmed preference | No change |
| 48 | Debunk-the-mechanism dominant in niche corpus | HEDGE (strong default) | Niche-wide qualitative (KB/RFB corpus) | No change |

## 3. New rules added (v17)

| New | Rule | Tier | Evidence |
|---|---|---|---|
| N1 | **Early-zone authority ban:** no personal_authority content ("I went/read/checked/pulled", credential chains beyond one clause) in the first ~90s; the "So I read it" pivot lands after the cliff zone | VALIDATED-directional | F2: −0.051 early (n=88) vs −0.0001 mid (n=10); LO_fUeX9IEQ 00:15–00:18; LuLZYZWMiU4 00:21–00:32. Mid-video authority is fine — this is placement, not voice |
| N2 | **Closing-third statistic:** at least one hard number in the final 20% | VALIDATED-directional | F4: late stats +0.001 (n=114); stats 61% positive (n=354) |
| N3 | **Late-quarter collapse audit:** 75% checkpoint diagnostic; final quarter gets evidence density, not wind-down padding | HEDGE | F6: 7fpBz6uo504 / UH2PddfaaR8 / _N_08zn95FY late crashes |
| N4 | **Cliff-zone humility:** first-30s text micro-optimization has no measurable retention payoff; spend that effort on packaging/topic instead | VALIDATED (observation) | F1: GuL9PtXEjN0 strongest-hook cliffs; cross-video universality |

## 4. Checker severity map (validated=hard / hedge=soft)

| Constraint | Was | Now | Why |
|---|---|---|---|
| A (first evidence 0:90) | CRITICAL | WARNING | #6 — confounded evidence; craft default survives |
| B (transition bridge) | CRITICAL | WARNING | #43 — universal hemorrhage; bridge ≠ proven lever |
| T (duration cap) | CRITICAL | **CRITICAL (unchanged)** | F7 — validated |
| U (myth-first for non-territorial) | CRITICAL | WARNING | F3 — topic-confounded numbers |
| BD (word budget) | BLOCK | BLOCK (unchanged) | Calibration constant; budget discipline feeds Constraint T |
| Content-type table "stat in first 10s" | WARNING | INFO | F1 + lFGs5NHMxMw early stat-barrage cliff |
| Content-type table "I read... in 1:00–3:00" | CAUTION | WARNING (new BE) | F2 — the validated-directional finding |
| Modern relevance 90s header | "CRITICAL RULE" | guideline (HEDGE) | F5 |
| NEW BE (early-zone personal-authority scan) | — | WARNING | N1 |
| NEW BF (late-quarter collapse audit) | — | SUGGESTION | N2/N3 |
| T / STEP 0 duration formula | words ÷ 250 ÷ 1.80 (~5,400-word cap) | words ÷ 250 ÷ 1.20 (~3,600-word cap, Format C → BD) | #19 — 1.80x buffer encoded the stale 56%-cut assumption |
| AV "44% survival" / Phase 4.5 "44% (not 77%)" | cited as fact | RETIRED (stale) | #19 — user-flagged 2026-06-11 |
| Constraint B bridge pattern "To understand how, you need to see..." | recommended | removed from examples | conflicts with Rule 13.7 HARD lint (tour-guide tissue, Phase 2) |

## 5. What this does NOT change

- Voice register, two-tier scripting, claims-ledger, citation-grounding gates — out of scope, untouched.
- Niche-wide structural toolkits (turn types, rebuttal architecture, closing taxonomy) — qualitative corpus rules, already correctly framed as Tier-3 "consider."
- The 12-minute cap and Format-C word budgets — enforced harder, not softer.
- Generic-AI anti-patterns (Rule 13.7) — Phase 2 artifact, carried into v17 unchanged.

**Quota note:** adjudication + v17 edits completed in one Fable session per plan. If anything below diverges from the edited files, the files win.
