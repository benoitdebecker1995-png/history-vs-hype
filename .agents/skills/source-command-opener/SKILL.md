---
name: source-command-opener
description: "Cold-open decision system — generates 3 candidate 30-second openers from the project artifacts, scores them on 4 dimensions, and writes a ranked verdict. Use when: the first 30 seconds need deciding, a script needs its hook, or first-minute retention is the problem (31.6pp of the audience leaves there)."
---

> **Codex note.** This is the Codex port of `.claude/commands/opener.md`, which stays canonical.
> The procedure below is that file verbatim. While running here: a `/name` reference is the
> `source-command-name` skill in `.agents/skills/`; "the Task tool" means spawning a Codex agent
> from `.codex/agents/`; "Claude" means you.

# /opener — Cold-Open Decision System

**Purpose:** Generate and rank 3 candidate cold-opens (first 30 seconds) for a video project. Uses external/niche-wide data only (no channel-internal performance anchors). Returns a ranked verdict the user locks.

**Workflow slot:** After `/research` + comment-mining + P11.2 angle-discovery. Before `/script`.

**Scope:** First 30 seconds only. Beyond 30s = `script-writer-v2` domain. The 30-second window covers Rule 19's paradox beat (0:00-0:05) + exhibit reveal (0:05-0:30). After 30s, retention is a script-architecture problem.

## Usage

```
/opener                                          # Run on current/active project
/opener --project 56-no-lassos-...               # Run on specific project folder
/opener --refresh                                # Re-run if /opener was already locked (overwrites OPENER-DECISION.md)
```

---

## INPUTS REQUIRED

Before running, /opener reads these artifacts from the target project folder:

1. **Locked title** — from `YOUTUBE-METADATA.md` or `METADATA-DRAFT.md`
2. **Locked thumbnail concept** — from `YOUTUBE-METADATA.md` (description, not image)
3. **Locked thesis** — from `01-VERIFIED-RESEARCH.md` (working thesis OR P11.1b-locked mechanism word)
4. **Comment-mining synthesis** — from `_research/comment-mining/SIGNAL-ANALYSIS*.md`
5. **P11.2 CANDIDATE ANGLES** — from `01-VERIFIED-RESEARCH.md` section
6. **Topic type tag** — from `viability-check-*.md` or YOUTUBE-METADATA

### Precondition handling

| Missing input | Action |
|---|---|
| Locked title OR locked thesis | **HARD BLOCK** — output: `[PRECONDITION] /opener requires locked title + locked thesis. Run /greenlight + /research first.` |
| P11.2 CANDIDATE ANGLES section | **WARN** — output: `[WARNING] P11.2 missing — assembling candidates from primary-source material in 01-VERIFIED-RESEARCH.md only. For better candidate diversity, run P11.2 first via /research --apply-review.` Continue with degraded inputs. |
| Comment-mining SIGNAL-ANALYSIS | **DEGRADE** — dimension (b) audience-language-fit returns `N/A — comment-mining not run`. Other dimensions still score. |
| Thumbnail concept | **WARN** — Bridge Test reduces to title-vs-hook text comparison only. |

---

## VOICE GUARD (Live-Read from Style Doc)

Before any candidate is scored, run a forbidden-phrase check. Read live from `G:\History vs Hype\.claude\REFERENCE\WRITING-VOICE-AND-STYLE-P1-CORE-VOICE.md` (§1.3 forbidden phrases). Reject candidates containing:

**Forbidden phrases:**
- "Buckle up" / "Strap in" / "Hold on tight"
- "Let me show you" / "Let me tell you"
- "What I'm about to" / "You won't believe"
- "It's wild" / "It's crazy" / "Mind-blowing"
- Any exclamation point in narration
- Second-person commands ("Listen.", "Look at this.")
- No-contraction phrasing ("it is" instead of "it's" — Calm Prosecutor uses contractions)

If a candidate fails the voice guard: regenerate that candidate; do not score. If 3+ regenerations fail for the same archetype, surface to user with `[VOICE GUARD] Could not generate clean candidate for archetype [X]. Skipping; consider rewriting raw material in P11.2.`

---

## FIREWALL (Channel Data Isolation)

`/opener` MUST NOT cite or pull from:

- The 35-video channel performance table (`channel-data/POST-PUBLISH-ANALYSIS/`)
- Any HvH video's individual retention/CTR data
- Channel-specific hook-type ranking (myth_contradiction 36.7% etc., n<42)
- Notebook `98973069` (Packaging Intelligence) — for HvH-specific entries only
- Notebook `8d9e459b` (Thumbnail Outliers) — for HvH-specific entries only

The Opener Outliers notebook (`5287616d-7790-492b-bf52-0bbe880db71a`) contains ZERO HvH videos by design. All evidence dimensions pull from there exclusively.

If a firewall violation is attempted: output `[FIREWALL] Refused to cite [channel-internal data]. Per memory/feedback-channel-data-too-small.md.` and proceed with the violation removed.

---

## STEP 1 — ASSEMBLE 3 CANDIDATES (Hybrid Model)

**Sources of raw material (in priority order):**

1. **P11.2 CANDIDATE ANGLES section** in `01-VERIFIED-RESEARCH.md` — primary-source quotes, named documents, surprising facts already round-tripped through the project's NotebookLM notebook.
2. **Audience-validated language inventory** from comment-mining SIGNAL-ANALYSIS (the verbatim phrases that recurred in competitor video comments with high engagement).
3. **Locked thesis verb** (P11.1b) — the candidate must lead toward this verb without spoiling the body of the script.

**Assembly rule:** Each candidate must be built around a DISTINCT archetype from the `HOOK-PATTERN-LIBRARY.md` taxonomy:
- `cold_fact` — opens with specific number/date/measurement
- `specificity_bomb` — opens with hyper-specific named detail (person + document + date)
- `myth_contradiction` — states the standard belief then immediately contradicts
- `contextual_opening` — broad philosophical question that narrows
- `authority_challenge` — names an authority and promises to show why incomplete

Do NOT invent material outside P11.2 + comment-mining + thesis. If raw material is insufficient for a 3rd distinct archetype, output 2 candidates and flag the gap.

**Candidate structure (each):**

```
ARCHETYPE: [name from taxonomy]

0:00-0:05 — PARADOX BEAT (verbatim, ~15-25 words):
[Paradox statement: Specific Subject + Common Belief + Contradiction Word]

0:05-0:30 — EXHIBIT/DOCUMENT REVEAL (verbatim, ~50-75 words):
[Names what the script will show. First-person ownership ("I read...", "I pulled..."). 
References specific primary source from P11.2.]

STAKES/PROMISE PRESENT? [yes/no — required for Rule 19 pass]

RAW MATERIAL SOURCE (P11.2 line/section):
[Cite which P11.2 candidate entry was used.]

AUDIENCE-LANGUAGE PHRASES USED:
[List verbatim phrases pulled from comment-mining SIGNAL-ANALYSIS, with cite.]
```

---

## STEP 2 — SCORE EACH CANDIDATE (4 Dimensions)

### Dimension (a) — Rule 19 4-beat compliance (HARD GATE)

Source of truth: `G:\History vs Hype\.claude\REFERENCE\OPENING-HOOK-TEMPLATES.md` Rule 19 spec.

| Beat | Check | PASS/FAIL |
|---|---|---|
| Paradox in 0:00-0:05 | Contains Specific Subject + Common Belief + Contradiction Word | |
| Exhibit reveal in 0:05-0:30 | Names specific primary source / document / quote with first-person ownership | |
| Stakes/payoff promise | Promises what the script will deliver (specific, not vague) | |

ALL THREE must PASS. Any FAIL → candidate is auto-rejected with no further scoring.

### Dimension (b) — Audience-language fit (TIEBREAKER)

Source: `_research/comment-mining/SIGNAL-ANALYSIS*.md` validated audience language inventory.

Count occurrences of audience-validated phrases in the 30s draft. Cite each match verbatim. Score = N matches (integer).

If comment-mining missing: dimension returns `N/A`.

### Dimension (c) — Opener Outliers nearest analog (PRIMARY SIGNAL)

Query the Opener Outliers notebook (`5287616d-7790-492b-bf52-0bbe880db71a`):

```
For each candidate's archetype + topic-type combination, what is the nearest 
analog cold-open in this corpus? Cite the channel, sub-tier, view-multiplier, 
and the specific verbatim opener that matches.
```

Return per-candidate analog evidence with NLM citation `[N]`. This is the most-trusted signal until the channel builds more wins.

### Dimension (d) — hook_scorer.py deterministic score (SUPPLEMENT)

Tool: `G:\History vs Hype\tools\research\hook_scorer.py`

API:
```python
from tools.research.hook_scorer import score_hook
result = score_hook(hook_text, title=LOCKED_TITLE, topic_type=TOPIC_TYPE)
# Returns dict with overall_score (0-100) + per-dimension breakdown
```

Run for each candidate. Display the score and the top 2 weaknesses the tool flags.

---

## STEP 3 — BRIDGE TEST (Text-Only Consistency Check)

Source of truth: `OPENING-HOOK-TEMPLATES.md` Title-Content Alignment Matrix.

For each candidate, compare:
- **Title TEXT** (what does it promise? — modern relevance / mystery / mechanism / historical evidence)
- **Thumbnail concept TEXT** (what does the description say is depicted?)
- **Candidate first-5s TEXT** (what does the paradox beat say?)

| Result | Action |
|---|---|
| TIGHT — all three align to same concept | Keep as primary candidate |
| ADEQUATE — two of three align, third connects within 30s | Keep as rotation candidate |
| GAP — thumbnail/title connect to script minute 2+ but not the candidate hook | **HARD BLOCK** — reject candidate |
| NO BRIDGE — thumbnail concept doesn't appear in candidate at all | **HARD BLOCK** — reject candidate |

Output the test result per candidate with 1-sentence reasoning.

---

## STEP 4 — VERDICT

**Ranking logic:**

1. **Auto-reject:** any candidate that FAILS dimension (a) Rule 19 OR Bridge Test GAP/NO BRIDGE.
2. **Among surviving candidates:** primary ranking weight = dimension (c) Opener Outliers analog quality (channel-tier + view-multiplier of the nearest analog).
3. **Tiebreaker:** dimension (b) audience-language match count.
4. **Secondary tiebreaker:** dimension (d) hook_scorer overall_score.

If all 3 candidates auto-reject: output `[FAILURE] All candidates failed Rule 19 or Bridge Test. Re-run with adjusted P11.2 raw material or revised title.`

---

## STEP 5 — WRITE OPENER-DECISION.md

Output path: `<project_folder>/OPENER-DECISION.md`

Structure (use this template verbatim):

```markdown
# Opener Decision — <Project Name>

**Date:** YYYY-MM-DD
**Locked title:** ...
**Locked thumbnail concept:** ...
**Locked thesis:** ...

## Decision-log prior (from past /opener runs)

[1-paragraph synthesis read from .claude/REFERENCE/OPENER-DECISION-LOG.md, 
filtered to this project's topic_type. Skip section if log is empty or no 
matching entries.]

## Candidates evaluated (30s scope)

### Candidate 1 — [Archetype name]

**0:00-0:05 paradox beat:**
> [verbatim]

**0:05-0:30 exhibit reveal:**
> [verbatim]

**Raw material source:** P11.2 CANDIDATE ANGLES — [which quote/document/payoff]

**(a) Rule 19 compliance:**
- Paradox 0:00-0:05: PASS/FAIL
- Exhibit reveal 0:05-0:30: PASS/FAIL  
- Stakes/payoff present: PASS/FAIL

**(b) Audience-language fit:** [N matches: "phrase 1" / "phrase 2" / ...]

**(c) Opener Outliers analog:** [Channel name] / [tier] / [view-multiplier]x — [NLM citation]

**(d) hook_scorer.py:** N/100 — top weaknesses: [w1, w2]

**Bridge Test:** TIGHT/ADEQUATE/GAP — [1-sentence reasoning]

**Why this works:** [≤2 sentences]
**Why this might fail:** [≤2 sentences]

[Candidates 2, 3 same structure]

## Verdict

**Recommended:** Candidate N. Rationale: [1-2 sentences citing dim (c) primarily, dim (a) as gate, dim (b)+(d) as tiebreakers].

**Rejected:** Candidate K — [reason: Rule 19 FAIL or Bridge Test GAP].

## Lock decision (user-completed)

- [ ] LOCKED to Candidate N by [user] on YYYY-MM-DD
- [ ] Iterate — user wants different angle. Notes: ___

**Lock rationale (1-2 sentences from user, required to lock):** ___
```

---

## STEP 6 — APPEND TO DECISION LOG (After User Locks)

When user marks `LOCKED to Candidate N` on the OPENER-DECISION.md file, append to:

**File:** `G:\History vs Hype\.claude\REFERENCE\OPENER-DECISION-LOG.md`

Entry format:

```markdown
## YYYY-MM-DD — Video #N: <slug>
- **Locked:** Candidate [N] — [archetype] — [1-sentence rationale from user]
- **Rejected:** Candidate [M] — [archetype] — [why rejected]
- **Rejected:** Candidate [K] — [archetype] — [why rejected]
- **Topic type:** [territorial / ideological / myth-busting / mechanism]
- **What surprised user:** [optional — user-supplied note]
```

This log is queried by future `/opener` runs at the top of Step 5 to surface user-preference patterns.

---

## INTEGRATION

- `/greenlight` → GO → `/research --new` → P11.2 angle-discovery → **`/opener`** ← HERE → `/script`
- After user locks: `/script` reads OPENER-DECISION.md and uses the locked candidate as the cold-open scaffold
- After 3-4 locks: review OPENER-DECISION-LOG.md for emerging patterns; consider Phase D opener-critic agent if user judgment consistently overrides system verdicts

---

## OUT OF SCOPE

- Generation beyond 30s (script-writer-v2's domain)
- Full script generation (use /script after lock)
- Thumbnail or title changes (those must be locked before /opener runs)
- Channel-internal performance pattern matching (blocked by firewall)

---

*This skill is built per `C:\Users\Benoi\.claude\plans\fuzzy-pondering-puddle.md`. Opener Outliers notebook: `5287616d-7790-492b-bf52-0bbe880db71a`.*
