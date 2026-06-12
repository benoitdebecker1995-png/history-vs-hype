# Fable 5 Allocation Plan — Channel System Upgrade

## Context

Fable 5 access is rate-limited (Pro plan). Goal: spend it where it permanently upgrades the channel system — better videos, more views — leaving durable artifacts that keep paying off when running on Sonnet/Opus.

The system inventory shows mature tooling everywhere (title_scorer v4 corpus-driven, 95KB VOICE-PROFILE, script-writer-v2 v16.5, 5,600-bin retention DB, 47/47 refactor done). So the leverage is NOT building new tools. It's three weaknesses only a top-judgment model fixes well:

1. **The rules haven't produced breakouts.** Only 3/47 videos broke 2K views despite a sophisticated packaging engine. Either the rules are wrong, derived from noise (n<30 channel data), or optimizing the wrong variable.
2. **Voice authenticity risk.** User's explicit worry: scripts must sound like HIM, not generic AI. VOICE-PROFILE is fresh but built top-down from one discovery session; residual AI-tells need an adversarial hunt.
3. **Rule bloat without validation.** 134KB script agent + 95KB voice profile + 7,100-line style manual + 25 pattern files. Some rules contradict; many were never validated against retention/CTR data.

**Operating principle (every phase):** cheap models do bulk prep → ONE focused Fable session consumes pre-built digests and writes the durable artifact → Sonnet implements code changes Fable specifies. Fable never does bulk reads. Each phase is self-contained — stop after any phase and the value is banked.

## Model assignments

| Role | Model | What it does |
|---|---|---|
| Synthesis / adjudication / artifact lock | **Fable 5 (inline)** | The judgment work each phase exists for |
| Digest prep, corpus sweeps, SQL extracts | **Haiku agents / Gemini Flash** (`/gemini` for transcripts) | Build the input files Fable consumes |
| Code implementation of Fable's specs | **Sonnet agent** | Edit title_scorer.py, voice_lint.py per spec |
| Fallback if Fable quota exhausted mid-phase | **Opus 4.8** | Finish from Fable's partial notes |

## Phase 0 — Prep harness (NO Fable; Haiku/Gemini/Sonnet; can run any session)

**Step 0 — DATA REFRESH FIRST (gate for everything below).** All digests must be built from current data, not May snapshots:
- Refresh `analytics.db` via the `tools/youtube_analytics/` extraction pipeline (read-only YouTube API) — pulls in #56 slave-trade and #57 piri-reis, fresh retention curves, traffic, CTR for the whole catalog.
- Generate POST-PUBLISH-ANALYSIS files for any published video missing one (#56, #57) so the breakout dossier covers all uploads.
- Re-run live SERP scans (`serp_title_study.py` / `serp_thumb_study.py`) for fresh shelf snapshots — per corpus-refresh mechanics, live SERP beats the static intel corpus for currency.
- Record refresh date in each digest header so Fable knows data vintage.

Then build digest files into `channel-data/fable-digests/`:

- **D1 Breakout dossier:** for all 57 videos from `analytics.db` + the 26 POST-PUBLISH-ANALYSIS files: title, thumbnail concept, topic type, impressions, CTR, traffic mix, retention summary, views. Winners (3 breakouts + next tier) vs stalls, side by side. Include the existing scorer's score for each title (run `title_scorer.py` over the catalog) so Fable can measure predicted-vs-actual.
- **D2 Voice triad:** gold-standard unscripted transcript (yt:yMAWJcjo_ug) + 2 recent locked scripts (#56, #58) + 1 deliberately generic-AI-written sample on the same topic (Sonnet writes it). Aligned per-section for tell-hunting.
- **D3 Retention evidence pack:** per-video retention cliff/hold moments (from `retention_curves` table + `RETENTION-SCRIPT-CORRELATION.md` + `HOOK-RETENTION-CORRELATION.md`) mapped to the script lines at those timestamps. Plus n-size annotation for every quantitative rule currently cited in script-writer-v2.md and PACKAGING_MANDATE.md.
- **D4 Whitespace scan:** SERP study outputs (`serp_title_study.py`, `serp_thumb_study.py`) + competitor transcript corpus topic map (18 dirs, via Gemini) → "what the niche over-serves vs under-serves."

## Phase 1 — Packaging breakout forensics (Fable, ~1 session) — #1 PRIORITY

Input: D1, D4. Fable adversarially audits the packaging rule-set against the evidence:

- Why exactly did 3 break out and 44 stall? Impressions problem vs CTR problem vs topic-demand problem — per video, not aggregate (channel traffic is one-video-driven; cite distribution).
- Which title_scorer rules are validated, which are n<5 noise dressed as hard rules? (Year penalty n=5; "the X that Y" pattern, etc.)
- What do the breakouts share that no current rule captures?

**Durable artifacts:**
- `tools/PACKAGING_MANDATE.md` revised — rules re-tiered VALIDATED / HEDGE / RETIRED with n-sizes (per the rules-hedge-not-prescribe principle)
- `channel-data/BREAKOUT-HYPOTHESES.md` — ranked, testable predictions for the next 5 uploads (each = one A/B test)
- title_scorer.py change spec → Sonnet implements; regression: predicted-vs-actual CTR error rate must not worsen vs the current 17%
- Back-catalog retitle shortlist (top 5 candidates with proposed titles) → feeds existing `/retitle`

## Phase 2 — Voice authenticity adversarial pass (Fable, ~1 session)

Input: D2. Fable hunts the residual AI-tells the profile misses — rhythm, hedging patterns, transition tissue, paragraph shape, enumeration habits — by contrasting gold-standard unscripted vs locked scripts vs the generic-AI control. Direction matters: find where locked scripts drift TOWARD the AI control and AWAY from the unscripted gold.

**Durable artifacts:**
- `VOICE-PROFILE.md` delta — new tells section + any corrections (append, don't rewrite; profile is canonical)
- voice_lint.py new pattern spec → Sonnet implements; acceptance: gold transcript passes clean, AI control sample triggers ≥5 HARD flags, #58 locked script stays 0 HARD
- A "generic-AI tell list" Fable writes from introspection — what models like itself default to — added to script-writer-v2's anti-pattern section

## Phase 3 — Engagement/retention rule validation (Fable, ~1 session)

Input: D3. Fable cross-examines every retention/engagement rule in script-writer-v2.md + structure-checker-v2 against actual retention curves:

- Which patterns demonstrably hold viewers at the timestamps where they appear? Which rules have zero evidential support?
- Prune/re-tier: VALIDATED (keep, promote) / HEDGE (n<30, mark as idea not mandate) / NOISE (retire). Target: a leaner agent file that's MORE reliable, not a longer one.
- Add any newly-discovered engagement patterns from breakout retention curves (what held viewers in the 3 winners).

**Durable artifacts:**
- script-writer-v2.md v17 — re-tiered rules, retention-validated engagement section, generic-AI anti-patterns from Phase 2
- structure-checker-v2 updated to check the validated tier hard, hedge tier soft
- CHANGELOG entry with evidence citations per change

## Phase 4 — Topic/uniqueness strategy (Fable, ~1 session) — stretch

Input: D4 + Phase 1 findings. Codify "genuinely fills a need": upgrade the small-channel topic rubric (40/20/20/10/5/5) with a uniqueness/whitespace dimension — what can this channel say that the SERP shelf doesn't already serve. Refresh `channel-data/TOPIC-PIPELINE.md` ranking through the upgraded rubric.

**Durable artifacts:** upgraded rubric in the greenlight path + re-ranked topic pipeline with whitespace rationale per topic.

## Phase 5 — Coherence sweep (Opus, NOT Fable) — stretch

After phases 1–3 mutate the rule corpus: contradiction/staleness sweep across VOICE-PROFILE ↔ WRITING-VOICE-AND-STYLE ↔ script-writer-v2 ↔ PACKAGING_MANDATE. Mechanical cross-checking — Opus-grade, don't spend Fable.

## Sequencing & quota discipline

- Order: 0 → 1 → 2 → 3 → (4) → (5). Phase 0 runs on cheap models anytime, including while Fable quota recovers.
- Each Fable phase opens with ONLY its digest files in context — no exploratory reads. If quota dies mid-phase, Fable's partial notes go to a `PHASE-N-NOTES.md` and Opus finishes.
- Current production (#58 film prep, #59 pilot) continues on the normal Sonnet/Opus pipeline — EXCEPT #59's script lock, which should wait for Phase 2+3 artifacts if timing allows (pilot of a new series deserves the upgraded system).

## Verification

- **Phase 1:** title_scorer regression over the 57-video corpus — predicted-vs-actual CTR error ≤ current 17%. Breakout hypotheses falsifiable: each names the metric and threshold that confirms/kills it on upcoming uploads.
- **Phase 2:** three-way lint test (gold passes / AI control fails / #58 stays clean) + user read-aloud spot-check of one Fable-flagged passage rewritten per the new rules (read-aloud is the T1 gate).
- **Phase 3:** every rule change in v17 cites its evidence (video ID + timestamp range or pattern-file source). Rules with no citation can only be HEDGE tier.
- **System-level (slow):** next 5 uploads are the real test — packaging A/B per BREAKOUT-HYPOTHESES, retention vs 28.1% median baseline.
