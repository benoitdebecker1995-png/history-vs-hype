# PHASE 5 — COHERENCE SWEEP REPORT

**Date:** 2026-06-11 | **Model:** Opus 4.8 (NOT Fable, per FABLE-PLAN.md L81-83)
**Scope:** Contradiction/staleness cross-check across the rule corpus mutated by Fable Phases 1–4 (packaging re-tier, voice adversarial pass, retention re-tier, topic rubric v2).

## Files swept (line counts)

| File | Lines | Role |
|---|---|---|
| `tools/PACKAGING_MANDATE.md` | 146 | Packaging authority (2026-06-10, re-tiered) — **precedence rule 1** |
| `channel-data/BREAKOUT-HYPOTHESES.md` | 77 | A/B hypotheses |
| `tools/TOPIC-RUBRIC.md` | 68 | Topic rubric v2 (2026-06-11) — **precedence rule 4** |
| `channel-data/TOPIC-PIPELINE.md` | 83 | Ranked pipeline (rubric v2) |
| `.claude/commands/greenlight.md` | 377 | Greenlight gate |
| `.claude/REFERENCE/VOICE-PROFILE.md` | 474 | Canonical voice — **precedence rule 2** |
| `.claude/REFERENCE/WRITING-VOICE-AND-STYLE.md` | 3016 | Craft manual (callout-deferred to profile) |
| `.claude/agents/script-writer-v2.md` | 1933 | v17 retention tiers — **precedence rule 3** |
| `.claude/agents/structure-checker-v2.md` | 2552 | Checker (re-tiered v17) |
| `docs/adr/0006-...md` | 13 | Voice precedence ADR |
| `channel-data/patterns/TRAFFIC-SOURCE-ANALYSIS.md` | 210 | Source data (reinterpreted by mandate) |

**Method:** Read each read_first file in full (paginated where >cap). Grepped the repo for retired-rule fingerprints (`auto-REJECT`, `-46%`/`-28%`, `73% subscriber`, `26x`, `26.4% search`, `42% subscriber`, `VOICE-PROFILE.md`, `but guess what`, `40/20/20/10/5/5`). Verified `title_scorer.py` actual behavior against the mandate's claims. Applied only unambiguous mechanical citation fixes where a superseding artifact is explicit + named; everything else flagged. **Out-of-corpus excluded by design:** `.antigravity/`, `_toolkit_release/`, `.planning/`, `.claude/_ARCHIVE/`, `.claude/worktrees/`, `WORKFLOW-AUDIT-*.md`, published `video-projects/` — none are active rule files; the Phase 5 spec scopes the live corpus only.

---

## Section 1 — FIXED (mechanical edits applied)

| # | File:line | Before → After | Precedence |
|---|---|---|---|
| F1 | `.claude/commands/publish.md:305` | "No years, colons, or 'The X That Y' (auto-REJECTED by scorer)" → "graded style penalties, NOT auto-rejects" + named mandate Tier 2 HEDGE | Rule 1 |
| F2 | `.claude/agents/structure-checker-v2.md:32,39-42` | Removed `VOICE-PROFILE.md` from the "do NOT read deprecated files" list; added it as **reference 0 (canonical, read FIRST)** with ADR-0006 pointer; demoted WRITING-VOICE-AND-STYLE.md from "SINGLE SOURCE OF TRUTH" → "PRIMARY craft manual (canonical EXCEPT where VOICE-PROFILE.md overrides)" | Rule 2 |

**F1 verification:** `title_scorer.py` v5 (lines 47-59, 204-213, 650, 727-756) confirms year/colon/the-x-that are graded penalties (-15/-10/-15), auto-REJECT survives ONLY for clickbait tone, and `--strict` is opt-in v4-regression mode. `publish.md` was factually describing pre-v5 behavior. Unambiguous.

**F2 verification:** ADR-0006 declares VOICE-PROFILE.md canonical on any conflict and states `script-writer-v2` already reads it first. The checker was the ONLY agent still treating it as deprecated — a hard contradiction with the ADR, and the most consequential staleness in the corpus (the structure checker would skip the canonical voice file entirely). The "deprecated VOICE-PROFILE.md" of the 2026-05-02 consolidation note refers to the OLD file; the current one was re-created 2026-06-05. Edit preserves the genuinely-deprecated list and disambiguates.

---

## Section 2 — FLAGGED contradictions (user decision required)

| # | File:line | Issue | Precedence | Severity |
|---|---|---|---|---|
| FL1 | `greenlight.md:214-217` | Stale "Traffic-optimized title selection" block | Rule 1 | HIGH |
| FL2 | `CLAUDE.md:158, 192` | Item 13 + step 2 cite -46%/-28% as binding | Rule 1 | MED (no-edit file) |
| FL3 | `WORKSPACE_RULES.md:28` | "No year tokens (–46% CTR), no colons (–28%)" as a rule | Rule 1 | MED |
| FL4 | `research-organizer.md:64-68` | Guatemala-distorted avg views + -46%/-28% as title data | Rule 1 + 3 | MED |
| FL5 | `tools/PACKAGING-NOTEBOOK-GUIDE.md:83-84,103` | Notebook prompt source-text restates retired rules | Rule 1 | HIGH (gated) |
| FL6 | `TRAFFIC-SOURCE-ANALYSIS.md` (whole) | No staleness banner; mandate says "re-read through Funnel lens" | Rule 1 | HIGH |
| FL7 | `structure-checker-v2.md:49` | "TITLE-PATTERNS.md (versus=5.5%, colon=2.6%)" stale n<30 | Rule 1 + 5 | LOW |
| FL8 | `structure-checker-v2.md:32` residual | "PRIMARY craft manual" still implies sole authority for some rule classes | Rule 2 | LOW (F2 partial) |

### FL1 — greenlight.md stale traffic block (HIGH)
`greenlight.md:214-217` still instructs:
> **Traffic-optimized title selection (from TRAFFIC-SOURCE-ANALYSIS.md):**
> - Search-optimized topics … Prefer How/Why … gets 26.4% search traffic (2x declarative)
> - Territorial topics are 42% subscriber-dependent…

The mandate's Funnel Model (PACKAGING_MANDATE.md:24) reinterprets the SUBSCRIBER bucket as largely homepage/Browse and says TRAFFIC-SOURCE-ANALYSIS.md conclusions "should be re-read through this lens." The "42% subscriber-dependent" framing presupposes the misread subscriber-loyalty interpretation the mandate RETIRED (L76). The 26.4%/2x How-Why claim is also a HEDGE in the mandate (Tier 2, n=5). **Not a mechanical fix** — How/Why guidance survives as a HEDGE, so this isn't pure deletion; it needs the user to decide whether to reframe (Browse-not-loyalty) or cut. NOTE: greenlight.md's Step 2 title rules (L211) were ALREADY correctly updated to the re-tiered mandate — only this one downstream block lagged. **Recommended:** replace the block with a Funnel-Model-consistent note (subscriber bucket ≈ Browse; How/Why is a HEDGE for evergreen-search topics).

### FL2 — CLAUDE.md item 13 + step 2 (MED, do NOT edit)
`CLAUDE.md:158` ("No years (-46% CTR), no colons (-28%)") and `CLAUDE.md:192` (item 13, same) state retired causal claims as binding. Per mandate L75 these are confounded correlations, now HEDGE. **Per spec, CLAUDE.md is user-facing and I did not edit it.** **Recommended:** user softens both to "graded style penalties (HEDGE) — see PACKAGING_MANDATE.md; the channel's #1/#3 videos both use colons."

### FL3 — WORKSPACE_RULES.md:28 (MED)
> 8. **Title rules.** No year tokens (–46% CTR, n=47), no colons (–28%).

Same retired causal claims, stated as hard rules ("No year tokens"). Not edited because it's a top-level workspace-rules charter (user-facing register like CLAUDE.md) and the precise rewrite is a judgment call. **Recommended:** user softens to HEDGE + names the mandate.

### FL4 — research-organizer.md:64-68 (MED)
Line 64: "Territorial: 965 avg views, 30.9% retention" and line 68: "colon=-28% penalty, year=-46% penalty." The avg-views figures carry the Guatemala traffic distortion that script-writer-v2 v17 explicitly RETIRED (Rule 14: "old territorial = 2,449 avg views figure is RETIRED — it was the Guatemala breakout…"). The -46%/-28% are retired causal claims. **Recommended:** re-tier to HEDGE / cite retention not avg-views, mirroring script-writer-v2 Rule 14.

### FL5 — PACKAGING-NOTEBOOK-GUIDE.md + the gated notebook (HIGH, gated)
`PACKAGING-NOTEBOOK-GUIDE.md:83-84` ("Colon structure: -28% CTR / Years in title: -46% CTR") and :103 ("Traffic: 42% subscriber-dependent") are the **source text uploaded into the Packaging Intelligence NotebookLM notebook.** The guide file itself can be edited (recommended), but **the live notebook already contains these retired rules and CANNOT be edited by an agent** — it needs a gated notebook-patch (re-upload corrected source). This is the highest-leverage stale artifact because `/greenlight` Step 0B queries this notebook for packaging angles. **Recommended:** (a) edit the guide's title-pattern + traffic blocks to the re-tiered mandate; (b) flag a gated notebook source re-upload for user approval.

### FL6 — TRAFFIC-SOURCE-ANALYSIS.md carries no staleness banner (HIGH)
The mandate (L24) names this file and says its conclusions "should be re-read through this [Funnel] lens," but the file itself (all 210 lines, esp. §1 L25 "Subscribers (Home) drives 73%", §9 L181 "73% subscriber-driven… YouTube isn't suppressing the channel") has **no banner** warning the reader the 73%/42% subscriber-loyalty interpretation was reinterpreted as Browse. Anyone reading it cold inherits the retired interpretation. **Not a mechanical fix** (adding an interpretive banner is authored content, not a citation correction). **Recommended:** user adds a top-of-file banner: "⚠️ 2026-06-10 REINTERPRETATION — the SUBSCRIBER bucket is largely homepage/Browse, not loyalty; see PACKAGING_MANDATE.md Funnel Model. The 73%/42% subscriber framing below is superseded."

### FL7 — structure-checker-v2.md:49 stale title-pattern numbers (LOW)
Reference 5: "TITLE-PATTERNS.md - Title pattern CTR data (versus=5.5%, colon=2.6%)." These are channel n<30 figures presented without a HEDGE tag; the mandate's colon row (n=9 vs 26, confounded) supersedes the implied colon penalty. Low severity (it's a reference pointer, not an enforced constraint). **Recommended:** annotate as HEDGE / n<30 or point to the mandate Tier 2 table.

### FL8 — residual "PRIMARY craft manual" wording (LOW, partially fixed by F2)
F2 demoted WRITING-VOICE-AND-STYLE.md from "SINGLE SOURCE OF TRUTH" to "PRIMARY craft manual (canonical EXCEPT where VOICE-PROFILE.md overrides)." This is now ADR-consistent, but a reader could still over-weight the manual on a voice call. The manual's own inline callouts (verified present: §1.1 L100, §1.4 L300, §2.3 L673) already defer correctly, so this is cosmetic. **Recommended:** no further action needed; logged for completeness.

---

## Section 3 — STALE-BUT-HARMLESS (correctly framed as superseded — no action)

- **PACKAGING_MANDATE.md:62-77** — the mandate itself lists -46%/-28%, the 73% interpretation, the 26x multiplier, and the hard-reject policy in its RETIRED/HEDGE tiers, correctly framed as superseded. This is the source of truth doing its job. ✅
- **BREAKOUT-HYPOTHESES.md:58,62** — cites "-28% penalty was topic-confounded" and "restore -25 penalty" inside hypothesis H5, correctly as a falsifiable A/B claim, not a binding rule. ✅
- **script-writer-v2.md Rule 14 (L620), Rule 11 (L296), Rule 12 (L304), Rule 15 (L630), Rule 16 (L650), Constraints in checker (BE/T/U/AV)** — every retired retention number is explicitly tagged RETIRED/HEDGE with the confound named. The v17 re-tier is internally coherent and the checker mirrors it (CONSTRAINT T VALIDATED-hard, U/A/B HEDGE-demoted, BE/BF new). ✅
- **TITLE-RUBRIC v2 (TOPIC-RUBRIC.md)** — explicitly "Supersedes: feedback-small-channel-rubric.md v1 (40/20/20/10/5/5)" in its header; TOPIC-PIPELINE.md + greenlight.md Step 1b both reference v2. The old 40/20/20/10/5/5 survives only in the memory file it supersedes (out of corpus). ✅
- **WRITING-VOICE-AND-STYLE.md correction-callouts** — the manual's self-contradicting inline callouts (retired tics "but guess what"/"guess who" at L253, plain-numbers override §2.3, staccato-demotion §1.4) are intentional-by-design per ADR-0006 ("carries self-contradicting correction-callouts by design… the callouts defer to VOICE-PROFILE.md"). Verified they all point to the profile. ✅ NOT rot.
- **serp-studies/titles/*-2026-06-11.md** — Suez + Brest-Litovsk studies mention "dodges the -46% year penalty." Borderline, but these are dated per-topic scan artifacts (snapshots, not rules) and the observation (years saturate the shelf → yearless differentiates) is independently true regardless of the penalty's tier. No action.

---

## Section 4 — Dead / orphan cross-references

- **structure-checker-v2.md:39 (pre-fix)** — pointed agents to NOT read VOICE-PROFILE.md, which is now the canonical file script-writer-v2 reads first. Orphaned by the 2026-06-05 ADR; **fixed in F2.**
- **No broken file-path references found** among the read_first set — all named files (`PHASE-1-SCORER-SPEC.md`, `PHASE-3-RETENTION-ADJUDICATION.md`, `D1-breakout-dossier.md`, `D4-competitor-topic-map.md`, `SWAP-PROTOCOL.md`, `RETITLE-SHORTLIST.md`) referenced by the mandate/agents resolve to real paths (spot-checked the digests dir + tools dir).
- **greenlight.md Step 3b "FORMAT-TEMPLATES.md"** and **Audience-Segment table (L267-274)** cite sub-conversion %s (Correctionist 2.31%, etc.) that are the same n<30 channel figures the corpus elsewhere HEDGEs — not a dead ref, but a latent FL-class staleness (logged under FL4's family; not separately actioned).
- **PACKAGING-NOTEBOOK-GUIDE.md** is referenced as live setup by both greenlight.md (L98, L106) and MEMORY — its stale source text (FL5) is reachable through an active workflow path, which is why FL5 is HIGH not LOW.

---

## Section 5 — Verdict

**The corpus is coherent enough for #59 script lock and Panama production to proceed — with two caveats the user should clear first.** The two load-bearing systems for those tasks are internally consistent: (1) the **voice corpus** (VOICE-PROFILE.md ↔ WRITING-VOICE-AND-STYLE.md ↔ script-writer-v2 v17 ↔ ADR-0006) is now fully ADR-consistent after F2 — the one hard contradiction (the structure checker treating the canonical voice file as deprecated) is fixed, and the manual's self-contradictions are intentional-by-design and correctly deferred; (2) the **retention corpus** (script-writer-v2 v17 ↔ structure-checker-v2 re-tier) is coherent, every number tagged with its evidence tier, checker severities mirroring the agent tiers. The **packaging corpus** is coherent at its source of truth (PACKAGING_MANDATE.md + TOPIC-RUBRIC v2 + BREAKOUT-HYPOTHESES + greenlight Step 2 title rules), and Panama is already greenlit through rubric v2 with H4 arms pre-registered. The residual staleness is all **downstream restatement lag** (FL1-FL7): older files still phrasing retired CTR penalties as binding rules. None of it blocks the two named tasks, because #59 and Panama route through the already-corrected primary files. **Clear before relying on the system at scale:** FL6 (TRAFFIC-SOURCE-ANALYSIS banner) and FL5 (the gated packaging-notebook re-upload) — those are the two places a future `/greenlight` could re-inherit the retired subscriber-loyalty interpretation. FL2/FL3 (CLAUDE.md, WORKSPACE_RULES) are user-facing charter edits left for the user by policy.
