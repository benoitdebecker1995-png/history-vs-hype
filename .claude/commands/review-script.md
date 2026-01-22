---
description: Act as a critical viewer and review the script for credibility, retention, and engagement issues.
---

# /review-script - Comprehensive Script Analysis

Analyze a script for structure, voice authenticity, narrative flow, and retention issues before filming.

## Reference Files (MANDATORY)

Read before reviewing:
- `.claude/REFERENCE/NARRATIVE-FLOW-RULES.md` - 10 structural rules
- `.claude/REFERENCE/USER-VOICE-PROFILE.md` - Forbidden/approved phrases
- `.claude/REFERENCE/SCRIPTWRITING-QUICK-REFERENCE.md` - Copy-paste alternatives
- `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md` - Opening templates (first 60 sec)
- `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md` - Closing templates (final 60-90 sec)
- `.claude/REFERENCE/CREATOR-PHRASE-LIBRARY.md` - Natural phrases from Kraut, Knowing Better, Shaun, Alex O'Connor
- `.claude/REFERENCE/scriptwriting-style.md` - Voice patterns
- `.claude/REFERENCE/retention-mechanics.md` - Retention triggers

---

## PART 1: FORBIDDEN PHRASE SCAN (Do First)

**Run grep for these patterns:**
```
(Let me show you|Here's where it gets interesting|And that's the key insight|Buckle up|Stay with me here|Here's the thing|You won't believe|SHOCKING)
```

**If found → Flag as 🔴 CRITICAL and provide rewrite using approved alternatives.**

### Forbidden Phrases
| Phrase | Replacement |
|--------|-------------|
| "Let me show you" | "Here's how..." / "As you can see..." |
| "Here's the thing" | "The reality is..." |
| "Buckle up" | (just cut it) |
| "Here's where it gets interesting" | "And that's when..." |
| "And that's the key insight" | "This is crucial." |
| "Stay with me here" | (just cut it) |

---

## PART 2: NARRATIVE FLOW CHECK

### Rule 1: Term Introduction
**Scan for terms used before introduction.**

Flag these patterns:
- Names dropped without context (who is this person?)
- Acronyms without expansion (IRGC, AU, CIC)
- Historical terms without definition (bast, estoppel, bonyads)
- Treaties/laws without explanation

**For each violation:**
```
🔴 Line [X]: "[Term]" used without introduction
   Fix: "[Term] — [plain language definition]"
```

### Rule 2: Bridge Transitions
**Check every section transition.**

Does each section change have a "why are we talking about this now" sentence?

**Flag:**
```
🟡 Transition at [timestamp]: [Section A] → [Section B]
   Missing bridge. Add: "[Suggested bridge sentence]"
```

### Rule 3: Quote Integration
**Check every quote follows the pattern: Setup → Quote → Implication**

**Flag:**
```
🟡 Line [X]: Quote dropped without setup
   Current: > "[Quote]" That's from [Source].
   Fix: [Setup claim first] → [Quote] → [Implication]
```

### Rule 4: Implications
**After major facts, is there a "why does this matter?" follow-up?**

**Flag facts without implications:**
```
🟡 Line [X]: Fact stated, no implication
   Add: "That's how [X] was." / "Which meant..." / "Do you see what this means?"
```

### Rule 5: Meta-Commentary Count
**Count instances of meta-commentary:**
- "Let me show you" (should be 0)
- "Here's what most people miss" (max 1-2)
- "I'm going to explain" (should be 0)

**If over budget → Flag and suggest cuts**

### Rule 6: Repetition
**Flag same fact stated twice in different words.**

---

## PART 3: VOICE PROFILE CHECK

### Approved Phrases (Verify Usage)
Check script uses natural phrases:
- [ ] "The reality is..." (for emphasis)
- [ ] "This is crucial" (for key points)
- [ ] "If we are being fair..." (for steelman)
- [ ] "As you can see..." (for documents)
- [ ] "please subscribe" (for CTA)

### Formal Language (FLAG these)
- "Furthermore," "Moreover" → use "On top of that," "And"
- "In conclusion," → use "To summarize," "If you take away one thing..."
- "It is evident that" → just state the fact
- Academic passive voice → first person active

### Register Check
**Should sound like:** Educated casual (passionate tutor explaining to friend)
**Should NOT sound like:** Academic paper, news anchor, hype YouTuber

### Read-Aloud Test
- [ ] Every sentence under 25 words
- [ ] Contractions used (it's, they're, wasn't)
- [ ] Dates conversational ("On June 16th, 2014" not "June 16, 2014")
- [ ] No tongue-twisters or awkward consonant clusters

---

## PART 4: STRUCTURE CHECK

### Opening (0:00-1:00)
- [ ] Concrete detail in first 10 seconds (date, place, document)
- [ ] Modern hook (2024-2026 relevance)
- [ ] BOTH extreme narratives framed
- [ ] Stakes established ("people are dying/paying")
- [ ] NO forbidden phrases

**See:** `.claude/REFERENCE/OPENING-HOOK-TEMPLATES.md`

### Closing (Final 60-90 seconds)
- [ ] Returns to opening premise (both extremes, document, question)
- [ ] Answers "so what?" explicitly
- [ ] Modern relevance restated or implied
- [ ] Universal pattern extracted (if applicable)
- [ ] CTA is polite and natural ("please subscribe")
- [ ] NO forbidden phrases
- [ ] Ends with concrete takeaway, not vague sentiment

**See:** `.claude/REFERENCE/CLOSING-SYNTHESIS-TEMPLATES.md`

### Modern Relevance Map
Track every modern connection. **Flag gaps over 90 seconds.**

| Timestamp | Type | Content |
|-----------|------|---------|
| 0:15 | Hook | [Event] |
| [GAP] | ⚠️ RISK | No modern connection for X seconds |

### Both Extremes Pattern
**Opening:**
- [ ] Extreme A framed with who believes it
- [ ] Extreme B framed with who believes it
- [ ] "Both wrong" or "Both oversimplify" stated

**Ending:**
- [ ] Returns to both extremes
- [ ] Explains danger/limitation of each
- [ ] Nuanced reality with evidence

### Steelman Check
- [ ] "If we are being fair..." or equivalent present
- [ ] Opposing side's BEST argument presented
- [ ] Not strawmanned or dismissed

---

## PART 5: RETENTION PREDICTION

### Danger Zones
| Zone | Risk | Mitigation |
|------|------|------------|
| 0:00-0:08 | Highest dropout | Must hook immediately with concrete detail |
| 1:00-1:30 | "Is this worth my time?" | Must have stakes + promise |
| 3:00-4:00 | First fatigue point | Need pattern interrupt |
| Any 90+ sec without modern relevance | Drift risk | Add connection to present |
| 5+ dates in one section | Overload | Condense or visualize |

### Predicted Curve
| Time | Retention | Reason |
|------|-----------|--------|
| 0:00 | 100% | Start |
| 0:30 | [%] | Hook strength |
| 2:00 | [%] | Stakes clarity |
| 5:00 | [%] | Evidence engagement |
| End | [%] | Synthesis payoff |

**Channel benchmark: 35% average retention**

---

## PART 6: TERMS CHECKLIST GENERATOR

**List all terms that need introduction (auto-generate for script):**

### People
| Name | Introduced? | Introduction Needed |
|------|-------------|---------------------|
| [Name] | ❌/✅ | "[Name] — [role], [context]" |

### Organizations/Groups
| Term | Introduced? | Introduction Needed |
|------|-------------|---------------------|
| [Term] | ❌/✅ | "[Term] — [definition]" |

### Historical Terms
| Term | Introduced? | Introduction Needed |
|------|-------------|---------------------|
| [Term] | ❌/✅ | "[Term] — [definition]" |

---

## OUTPUT FORMAT

### QUICK SUMMARY

**Forbidden Phrases:** [X found / Clean]
**Narrative Flow:** [X/10]
**Voice Match:** [X/10]
**Structure:** [Both Extremes / Other]
**Retention Risk:** [Low / Medium / High]

**VERDICT:** [✅ Ready to film / 🟡 Needs revision / 🔴 Major issues]

---

### 🔴 CRITICAL ISSUES (Must Fix)

1. **Line [X]:** [Forbidden phrase / Unintroduced term / etc.]
   > "[Quote from script]"

   **Fix:**
   > "[Corrected version]"

---

### 🟡 IMPORTANT ISSUES (Should Fix)

1. **[Timestamp]:** [Issue type]
   **Problem:** [Description]
   **Fix:** [Suggestion]

---

### ✅ WHAT WORKS

- [Strength 1]
- [Strength 2]
- [Strength 3]

---

### TERMS NEEDING INTRODUCTION

| Term | Line | Suggested Introduction |
|------|------|------------------------|
| [Term] | [X] | "[Term] — [definition]" |

---

### MISSING BRIDGES

| Transition | Line | Suggested Bridge |
|------------|------|------------------|
| [A] → [B] | [X] | "[Bridge sentence]" |

---

### QUOTES NEEDING SETUP/IMPLICATION

| Quote | Line | Missing |
|-------|------|---------|
| "[Quote]" | [X] | Setup / Implication |

---

## Script to Analyze

$ARGUMENTS
