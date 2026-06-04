---
name: Competitor Findings
description: Competitor analysis — outlier patterns, growth paths, transcript structure, channel positioning, applicable lessons
type: reference
---

## Competitor Outlier Patterns (from: competitor-lessons.md)

**Source:** Intel DB (870 videos, 9 channels), analyzed 2026-03-05

### Kraut (604K subs, closest style match)
- Outliers: Trump's Biggest Failure (9.3x), How Vodka ruined Russia (8.3x), Turkish Century (5.6x)
- SHORT videos (9-10min) with cultural hooks outperform epics per-minute
- "How Vodka ruined Russia" = 2nd most-viewed at only 9 minutes

### Knowing Better (952K subs)
- Outliers: Wannabe States (9.8x), Neoslavery (9.4x), Japan Revisionism (7.9x)
- EVERY outlier uses `[Provocative Hook] | [Academic Topic]` pipe format
- Hook side is NEVER academic — short, provocative, movie-tagline style

### Shaun (760K subs)
- One/two-word titles for biggest hits. "Harry Potter." "The Bell Curve."
- Only works with established brand recognition — NOT replicable at <1K subs

### Fall of Civilizations (1.46M subs)
- Numbered series + civilization name + subtitle. Ultra-long (2-4h). Series numbers drive completionism.
- NOT replicable at <1K subs — 2-3h format needs established audiobook-style fanbase

## Growth Patterns
- **0-10K:** All started with short, consistent uploads. Shaun rode response video wave.
- **10K-100K:** ALL pivoted to longer, deeper content once they had a base.
- **Breakout:** Every competitor had ONE video that 3-10x'd their channel. None were "core" format — topic-first outliers that went viral, audience stayed for deep dives.

## Applicable Lessons for HvH
1. **Title:** Use declarative or `[Hook] | [Topic]` format (from Knowing Better)
2. **Duration:** 10-min sweet spot confirmed (Kraut's short outliers outperform)
3. **Cultural Hook > Academic Precision:** "How Vodka ruined Russia" 2.6x > "Origins of Russian Authoritarianism"
4. **Breakout formula:** Active dispute + specific framing + visual storytelling (your Belize video)
5. **DON'T copy:** FoC 2-3h format, Shaun one-word titles, K&G war content

## Shorts-First Growth Channels
- Reed Schultz Geo: 553K in <3 years (geography Shorts → long-form)
- Map Lad: 91K subs, 120M views (1,319 views/sub — extreme Shorts leverage)
- Shorts-first works for geography/map but funnel to deep-dive unproven at quality level

## AI Slop Context
- AI history channels earn $40-60K/month from ~$60/video
- YouTube July 2025: renamed "repetitious content" → "inauthentic content," terminated 11 channels
- On-camera + document methodology = exact opposite positioning

## Niche Format Data (870 videos)
- Average duration: 31.7 min (median: 21.8 min). Your 10-min is BELOW niche avg.
- Title formula: "other" (55%), "how/why" (24%), "colon_split" (14%)
- Trending topics: war (39%), ideological (23%), colonial (12%), territorial (9%)

---

## Competitor Transcript Structure (85 videos, 10 channels, 2026-03-23) (from: competitor-script-patterns.md)

**Source:** 85 transcripts from Atun-Shei Films, CaspianReport, FoC, Historia Civilis, Knowing Better, Kraut, Shaun, Three Arrows, TikHistory, WonderWhy.
**Full analysis:** `tools/benchmark/TRANSCRIPT-STRUCTURE-ANALYSIS.md`
**Tool:** `transcript_structure_analyzer.py` (--fetch, --analyze, --report)

### Hook Type Performance (Normalized Views)
- specificity_bomb: 5.4x (n=5, LOW confidence)
- myth_contradiction: 4.6x (n=1, VERY LOW)
- cold_fact: 3.7x (n=11, MEDIUM confidence)
- contextual_opening: 2.7x (n=68, HIGH confidence but LOWEST performance)
- **Implication:** contextual_opening = 80% of niche but underperforms. Prefer cold_fact/specificity_bomb.

### Turn Placement Zones (58 videos)
- 15-25%: 3.2x (STRONG — early turn)
- 25-35%: 2.1x (DEAD ZONE — avoid)
- 35-45%: 2.4x
- 45-55%: 3.7x (STRONGEST — mid turn)
- 55%+: 2.8x

### First Date/Number Timing
- Top half: 203s vs bottom half: 304s (101s delta). Niche median: 101s.

### Other Signals
- Top half: +2.2 more rhetorical questions, +0.9 more documents mentioned
- 92% chronological structure, WPM median 165 (no correlation with views)
- Max structural correlation: r=+0.208 — packaging > structure confirmed
- CTA rate: 52% across niche

### Channel Positioning
HvH closest to Shaun (document-first, quotes) + Kraut (causal chains) + Alex O'Connor (intellectual honesty). Competitive advantage: page numbers + academic sources + steelmanning.

### Tool Updates Made (2026-03-23)
- `script-writer-v2.md` → Rules 26-27 updated from 85-video data
- `structure-checker-v2.md` → Constraints D-I updated
- `HOOK-PATTERN-LIBRARY.md` → 85 hooks, 10 channels, performance table
- `hook_scorer.py` → cold_fact/specificity_bomb +3, contextual_opening -3

---

## Wave 2 NotebookLM Extraction (21 videos, 2026-04-04)

**Source:** 21 competitor transcripts + 3 prior analysis docs via NotebookLM notebook `438186cd-045e-40b1-ae67-9ecf25fcb415`
**Full analysis:** `tools/benchmark/WAVE-2-STRUCTURAL-FINDINGS.md`

### Rules Refined
- Rule 42: +2 steelman intro phrases (Vox investigative, Kraut historiographical), +1 transition pivot (expert refutation)
- Rule 43: +5 causal connector types (thereby, meaning that, paves the way for, stepping stone to, ripple effects/domino/vicious cycle)
- Rule 44: +Tier 4 hypothetical visualization ("imagine..."), +tactile border verbs, +geological origin stories
- Rule 45: +Bridge Type 4 "Just Like" analogy, +systemic continuum, +explicit bridge intro phrases
- Rule 46: +3 post-quote patterns (narrative continuation, emotional mirroring, single-word decode)

### Constraints Updated
- AB: +expert refutation pivot, +intro phrase specificity check
- AC: +5 connectors to valid list, +systemic terms for simultaneous crises
- AD: +Tier 4 check for ancient topics, +tactile verb check
- AE: +"Just Like" analogy type, rotation across 4 types

### Gap Patterns (documented, not encoded)
- "Everything is a System" conceptual frame (Kraut/CGP Grey) — full-video framing, not rule-level
- Professional vulnerability ethos — requires voice profile change
- Hook-and-eye paragraph transitions — partially covered by Rules 35+43
- Loop-back reward planting — long-form technique, 12-min cap limits payoff

### Agent Versions
- `script-writer-v2.md` v10.1 (2026-04-04)
- `structure-checker-v2.md` Constraints AA-AF refined (2026-04-04)

---

## Wave 3 NotebookLM Extraction (51 sources, 2026-04-04)

**Source:** Expanded corpus (44 YouTube + 3 analysis docs). +23 videos added (Shaun 5, WonderWhy 5, Three Arrows 3, Knowing Better 3, Atun-Shei 2, CaspianReport 2, TikHistory 1, HC 1, FoC 1)
**Full analysis:** `tools/benchmark/WAVE-2-STRUCTURAL-FINDINGS.md` (Sections 12-17)

### Per-Channel Deep Dives
- **Shaun:** 5 techniques — Credential Chain, Investigative Contradiction, Self-Condemnation, Weaponizing opponent's sources, Sarcastic understatement. HvH's on-screen docs = visual version of Shaun's verbal credential chains.
- **WonderWhy:** 4 techniques — Cold Fact + Question hook (<15s), clean chronological, de jure vs de facto separation, treaties as mechanical pivots. BEST model for HvH territorial topics at current size.

### Unique Channel Signatures (1 per channel)
- Shaun: weaponizes opponent's own cited sources. Knowing Better: thematic pun CTAs. Kraut: non-historical conceptual frame. Three Arrows: hypothetical gut-punch trap. CaspianReport: cynical maxim. Atun-Shei: narrative inversion. FoC: deep-time geological scaling. HC: absurdist understatement. TikHistory: epistemological genealogy mapping.

### Failure Patterns to Avoid (5)
1. Disclaimer Dump — never apologize for runtime
2. Russian Nesting Doll tangents — weave mechanisms into causal chain, never announce tangents
3. Meta-framing gimmicks — clean evidence hand-offs only
4. Broadcasting ignorance mid-script — FATAL for Calm Prosecutor
5. Burying the lede — topic keyword in first 30s (WonderWhy model)

### Top 5 Techniques for HvH (ranked by retention impact)
1. Standard Myth Subversion (0:00-1:00) — 2.31% sub conversion
2. Early turn at 15-25% (1:30-2:30 in 10min video) — 3.2x views
3. Credential Chain before every major quote
4. Modern relevance bridges every 90s
5. Hook-and-eye micro-transitions between paragraphs

---

## Wave 4 NotebookLM Extraction (55 sources, 2026-04-04)

**Source:** Same 55-source corpus. 3 gap-filling prompts: closings, emotional arc, mid-video recovery.
**Full analysis:** `tools/benchmark/WAVE-2-STRUCTURAL-FINDINGS.md` (Sections 22-24)

### Closing Mechanics (5 types)
- Philosophical Synthesis (Shaun, KB), Geopolitical Warning (WonderWhy, Kraut), Pattern Synthesis (KB), Atmospheric Lament (FoC), Cynical Maxim (CaspianReport)
- **Loop-back structure:** Best closings return to opening hook/image with new meaning
- **CTA placement:** RIGID boundary — always AFTER final narrative point, never during
- **Register:** Final sentence = declarative verdict (≤12 words), not summary paragraph

### Emotional Arc — Oscillating (not linear)
- 3 zones: Hook+Turn (0-25%), Evidence Oscillation (25-75%), Climax+Close (75-100%)
- Valley-before-peak: deliberate calm before most devastating evidence (FoC peaceful city → siege; Shaun dry history → meeting notes)
- Post-turn: oscillate intensity, don't stay maxed. Breathing room every ~90s.
- Strongest evidence at 70-85%, not earlier

### Mid-Video Recovery (30-70% zone)
- Escalation phrases: "And it gets worse" / "strap in" / "Are you starting to understand why...?"
- Memory callbacks: "Did you forget about her?" (KB)
- Empathy checks: force viewer to actively process, not passively listen
- HvH-adapted: "But here's where the evidence gets damning." (Calm Prosecutor tone)

### Agent Versions
- `script-writer-v2.md` v10.3 (2026-04-04)
- `structure-checker-v2.md` Constraints AK-AM (2026-04-04)

---

## Wave 7 Structural Research (64 sources, 2026-04-05)

**Source:** 64-source NotebookLM corpus (`438186cd`) + HvH 47-video retention data + SRT deviation analysis
**Full analysis:** `tools/benchmark/WAVE-7-STRUCTURAL-RESEARCH.md`
**Triggered by:** User identified over-reliance on AI-generated scripts. 44% survival rate = 56% cut during filming.

### Core Finding: Top Performers ≠ Rule-Followers
Top quartile videos use **inductive reasoning** (evidence → verdict last), not deductive (thesis → prove it). They sequence evidence by **escalating impact**, not chronology. They sound human through **strategic inconsistency** — research moments, honest reactions, evidence-limit concessions.

### Argument Structures (4 types encoded in Rule 52)
- **Inductive:** Evidence → verdict last (Kraut, Shaun). Default for HvH.
- **Elimination:** Steelman → dismantle premises (KB, Shaun, Three Arrows). For debunking.
- **Accumulation:** Multiplier stack, 5 simultaneous factors (HC Bronze Age). For colonial/systemic.
- **Parallel Comparison:** Map unfamiliar → familiar (Kraut prison→China). For mechanism/how.

### Human Texture (5 markers encoded in Rule 53)
1. Research moments ("So I went and checked")
2. Honest reactions to evidence ("He's getting the wrong answer very carefully")
3. Concessions about evidence limits ("We're left with a gap")
4. Terse personal verdicts ("Britain never built it")
5. Beat gaps for ad-libs (ad-libs retain +10pp better)

### Evidence Impact Sequencing (Rule 54)
Setup evidence (25-40%) → Complicating evidence (40-60%) → Devastating evidence (70-85%) → Verdict evidence (85-100%)

### Agent Versions
- `script-writer-v2.md` v11.0 (2026-04-05): +Rule 52, 53, 54
- `structure-checker-v2.md` Constraints AU-AW (2026-04-05)
