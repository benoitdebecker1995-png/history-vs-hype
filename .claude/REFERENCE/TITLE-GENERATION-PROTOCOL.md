# Title Generation — Data-Locked Protocol

Reusable prompt for generating title candidates. Forces data-anchored output, prevents yes-man flip-flopping.

> **Single source of truth for title penalties: `tools/title_scorer.py:308-313`.** Do not restate the
> numbers here or in `METADATA-CHECKLIST.md` — read them from the code. A hand-maintained
> "keep both in sync" contract lived here until 2026-07-30 and had already drifted: this file and
> `CLAUDE.md` asserted a retired −46%/−28% hard rule as binding, while `CLAUDE.md` *also* recorded it
> as retired 62 lines later. Logged as finding FL2 on 2026-06-11 and unfixed for seven weeks.

---

## Usage

Copy the template below into any session (Claude Code, NotebookLM, etc.) with the video's script or SRT.

---

## Template

```
TITLE GENERATION — DATA-LOCKED PROTOCOL

VIDEO: [project name]
SCRIPT/SRT: [file path]
TOPIC TYPE: [territorial / ideological / colonial / document-based]

STEP 1: Read the script/SRT. Extract:
- The single most specific claim or mechanism in the video
- The most surprising or counterintuitive fact
- Any named entity (person, document, place) that carries the story

STEP 2: Generate exactly 3 titles. Each MUST:
- Use declarative pattern (3.8% CTR, n=19 own + n=104 niche — proven safe bet)
- Score 65+ on title_scorer.py
- Year and colon are **graded penalties, not bans** — see `tools/title_scorer.py:308-313`
- Under 65 characters
- Front-load the keyword or named entity

STEP 3: The 3 titles must differ in ANGLE, not just wording:
- Title A: MECHANISM angle — HOW something happened (logistics trigger)
- Title B: CONSEQUENCE angle — WHAT resulted (outcome/impact)
- Title C: MYSTERY angle — WHO/WHY with unanswered question (intrigue)

All three use declarative pattern. The variation is the ANGLE, not the formula.

STEP 4: Score each title. Show:
- Pattern, character count, score, grade
- Which specific line from the script/SRT the title is derived from
- What information the title LEAVES OUT (for thumbnail complement)

STEP 5: Rank them. State your pick and lock it. Do NOT change the ranking
if challenged — instead explain the data behind it. If the data is genuinely
ambiguous (scores within 5 points), say so and flag it as a legitimate A/B test.

HARD RULES:
- NEVER suggest a pattern with n<5 own data unless explicitly flagged as
  "experimental bet" with the sample size shown
- NEVER change your recommendation just because the user questions it —
  defend with data or admit the data is inconclusive
- NEVER generate titles from topic knowledge alone — every title must trace
  to a specific moment in the script/SRT
- If two titles score within 5 points, say "genuine toss-up, worth A/B testing"
  instead of pretending one is clearly better
```

---

## Angle Definitions

| Angle | Focus | Subscriber Trigger | Example |
|-------|-------|-------------------|---------|
| MECHANISM | HOW it happened | Logistics/systems crowd | "One Lawyer Split India in 36 Days" |
| CONSEQUENCE | WHAT resulted | Impact/stakes | "India's Border Was Redrawn in 3 Days" |
| MYSTERY | WHO/WHY unanswered | Intrigue/curiosity gap | "A Coded Phone Call Moved India's Border" |

All three use declarative pattern. The variation is what information the title foregrounds.

---

## The "Claim + Evidence Contradiction" Formula (2026-03-29)

**Source:** Retention audit — top 5 performers (35-50% retention) all use this pattern. Signals the channel's trust advantage in the title itself.

**The pattern:** `[Common claim/myth]. [Evidence-based contradiction or consequence].`

Two sentences. First states what people believe or what happened. Second introduces the document/evidence that changes everything.

**Top performers using this pattern:**
- "Putin Says NATO Promised Not to Expand. **The Documents Disagree.**" (45.7% retention)
- "Stalin Purged His Own Army. **Then Hitler Invaded.**" (36.2%)
- "China Claims the Entire South China Sea. **A Court Said No.**" (49.6%)

**Why it works for this channel:**
- Signals "I have the evidence" — fills the trust gap Gemini identified
- Creates information gap (what do the documents say?)
- The word "document/treaty/court/receipt" is a brand signal for History vs Hype
- Differentiates from generic history titles that describe topics without promising evidence

**Apply to pipeline titles:**
- Bakassi: "Nigeria Lost Oil-Rich Territory. **A 1913 Treaty Explains Why.**"
- Manhattan: "Manhattan Was Bought for $24. **The Receipt Says Something Different.**"
- Code Noir: "France Wrote a Law Making People Property. **Here's What It Actually Says.**"
- Operation Legacy: "Britain Destroyed 8,800 Colonial Files. **Here's What Survived.**"
- Hamoodur Rahman: "Pakistan Investigated Its Own Genocide. **Then Buried the Report.**"

**When to use:** Any video where the central thesis contradicts a common belief or reveals hidden evidence. This covers ~80% of channel content.

**When NOT to use:** Pure territorial explainers with no dominant myth (e.g., "Sabah Dispute" — use mechanism angle instead).

---

## Swap Strategy

- Publish with #1 ranked title
- If 48h CTR < 3%, swap to #2
- Match swap title to thumbnail complement (see THUMBNAIL-TITLE-COMBO.md in project folder)
