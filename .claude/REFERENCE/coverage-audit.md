# Coverage Audit Reference

**Purpose:** Self-diagnosis system for detecting insufficient training material coverage.
**Behavior:** Non-blocking informational checkpoint. Never blocks output.

*Created: 2025-12-28*

---

## COVERAGE SUFFICIENCY DEFINITIONS

### Dimensions

| Dimension | Question | Measurement |
|-----------|----------|-------------|
| **Depth** | How thoroughly analyzed? | Techniques extracted vs. merely mentioned |
| **Breadth** | How many examples? | Transcript count per video type |
| **Variety** | How diverse? | Different creators covering same type |

### Sufficiency Levels

```
✅ SUFFICIENT
- ≥2 transcripts from different creators for this video type
- Techniques documented with "From Transcript:" examples
- Patterns integrated into Quick Reference tables
- "When to Use" guidance included

⚠️ MARGINAL
- 1 transcript only, OR
- Multiple transcripts but same creator, OR
- Techniques mentioned but not extracted with examples, OR
- Listed in style guide but missing from creator-techniques.md

❌ UNDERSPECIFIED
- 0 transcripts analyzed for this video type
- Creator referenced in passing only (no technique extraction)
- Video type requested but no model creator identified
- Novel narrative structure with no documented precedent
```

---

## COVERAGE MATRIX

| Video Type | Primary Model | Transcripts | Status | Gap |
|------------|---------------|-------------|--------|-----|
| **Territorial disputes** | RealLifeLore, Kraut | 4 | ✅ Sufficient | — |
| **Ideological myth-busting** | Kraut | 2 | ✅ Sufficient | — |
| **Person-centered debunking** | Shaun | 1 | ⚠️ Marginal | Need 1 more Shaun or similar |
| **Political fact-checks** | — | 0 | ❌ Underspecified | No model creator identified |
| **Historical period overview** | Fall of Civilizations | 1 | ⚠️ Marginal | Need broader creator sample |
| **Response/rebuttal videos** | Alex O'Connor | 1 | ⚠️ Marginal | Only 1 direct response analyzed |
| **Legal/treaty analysis** | — | 0 | ❌ Underspecified | No dedicated legal explainer model |

### Updating This Matrix

When a new transcript is analyzed:
1. Update transcript count
2. Change status if threshold crossed (⚠️ → ✅ requires 2+ different creators)
3. Remove from "Gap" column if filled
4. Add new video types as they emerge

---

## TRIGGER CONDITIONS

The checkpoint activates **only when ALL THREE conditions are met**:

1. **Task type is identified** — Script request has clear category
2. **Coverage is below ✅ Sufficient** — Matrix shows ⚠️ or ❌
3. **User has not explicitly acknowledged the gap** — Not a repeat request

### When Checkpoint Runs

- AFTER user provides topic/brief
- AFTER video type classification
- BEFORE outline generation begins

### When Checkpoint Does NOT Run

- During fact-checking
- During editing
- On small tasks (research, metadata, edits)
- When coverage is ✅ Sufficient (silent)

---

## CHECKPOINT BEHAVIOR

```
┌─────────────────────────────────────────────────────────────┐
│                    COVERAGE CHECKPOINT                       │
│                                                             │
│  ✅ Sufficient    → Produce NO output. Silent.              │
│  ⚠️ Marginal      → Note limitation, proceed with output    │
│  ❌ Underspecified → Flag gap, recommend additions, proceed │
│                                                             │
│  NEVER blocks output.                                       │
│  NEVER refuses task.                                        │
│  NEVER apologizes.                                          │
│  NEVER asks permission.                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## RECOMMENDATION TEMPLATES

### ⚠️ MARGINAL Coverage Template

```
**Coverage Note:** This [video type] draws primarily from [creator]'s techniques
(1 transcript analyzed). Structural patterns are documented but variety is limited.
To expand: [specific recommendation with creator + video title].
```

### ❌ UNDERSPECIFIED Coverage Template

```
**Coverage Gap:** No model creator analyzed for [video type]. Writing with general
techniques only—no proven structural template for this format.

Recommended additions:
- [Creator A]: "[Video Title]" — would provide [specific technique]
- [Creator B]: "[Video Title]" — would provide [specific technique]
- Estimated need: [1-2] transcripts ([length])
```

### Recommendation Specificity Requirements

Every recommendation MUST include:

| Element | Required | Example |
|---------|----------|---------|
| **Creator name** | Yes | "Shaun" |
| **Video title or type** | Yes | "The Bell Curve" |
| **What it would provide** | Yes | "Contemporary statistical debunking" |
| **Quantity needed** | Yes | "1-2 transcripts (30+ min)" |

**Forbidden phrases:**
- "Add more data"
- "Consider expanding training"
- "More examples would help"
- Any vague guidance

---

## SAMPLE COVERAGE AUDIT OUTPUTS

### Example 1: ⚠️ MARGINAL (Person-Centered Debunking)

```
**Coverage Note:** This person-centered debunk draws primarily from Shaun's
techniques (1 transcript: "Dropping the Bomb"). Structural patterns are
documented but variety is limited. To expand: Shaun's "The Bell Curve"
would add contemporary statistical debunking patterns.
```

### Example 2: ❌ UNDERSPECIFIED (Political Fact-Check)

```
**Coverage Gap:** No model creator analyzed for political fact-checks. Writing
with general techniques only—no proven structural template for this format.

Recommended additions:
- Shaun: Political response video — would provide current-event debunking structure
- Knowing Better: Political myth video — would provide fact-check narrative flow
- Estimated need: 1-2 transcripts (20+ min each)
```

### Example 3: ✅ SUFFICIENT (Territorial Dispute)

```
[NO OUTPUT — Checkpoint is silent when coverage is sufficient]
```

---

## VIDEO TYPE CLASSIFICATION

To determine which row of the Coverage Matrix applies:

| If the script involves... | Video Type |
|---------------------------|------------|
| Borders, maps, territorial claims, ICJ cases | Territorial disputes |
| Historical myths shaping modern beliefs | Ideological myth-busting |
| Debunking a specific person's claims | Person-centered debunking |
| Fact-checking a political figure/video | Political fact-checks |
| Explaining a historical era/civilization | Historical period overview |
| Responding directly to another video | Response/rebuttal videos |
| Explaining treaties, court rulings, legal mechanisms | Legal/treaty analysis |

If multiple types apply, use the PRIMARY type (the one driving the structure).

---

## NO-CONTAMINATION RULES

This checkpoint:
- Does NOT interact with Gates 0-3
- Does NOT modify evaluator behavior
- Does NOT change retention logic
- Does NOT add new techniques
- Does NOT modify creator-techniques.md
- Does NOT touch script-reviewer.md

It ONLY reports coverage status and recommendations.
