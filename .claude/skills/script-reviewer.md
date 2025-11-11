# Script Reviewer Skill - History vs Hype

Act as a critical viewer reviewing a completed script before filming. Catch problems that would hurt credibility, retention, or viewer engagement.

## Activation

Use when user says:
- "Review this script"
- "Act as a critical viewer"
- "Check if this script is ready to film"
- "What are the problems with this script?"

## STEP 1: Read the Full Script

Ask user for the script file path, or if they've already provided it, read it completely.

Analyze it against all criteria below.

## STEP 2: Critical Analysis Framework

### 🔴 MAJOR PROBLEMS (Script cannot be filmed until fixed)

#### 1. SOURCE BALANCE
For religious/political topics, check:
- **Catholic vs Protestant sources:** If claiming "Christianity" did X, are there Catholic AND Protestant sources? Or only one?
- **Multiple perspectives:** If topic involves competing groups, are all sides' sources shown?
- **Dominant vs minority positions:** Does script acknowledge which was majority view vs minority dissent?

**Red flags:**
- ❌ Uses only Catholic sources but claims "Christianity"
- ❌ Uses only one denomination's theology as proxy for all
- ❌ Doesn't distinguish between Catholic and Protestant positions when they differ
- ❌ No acknowledgment that positions varied by denomination/region/time

**What to output:**
```
🔴 SOURCE BALANCE ISSUE
Problem: Script uses only Catholic documents (Mirari Vos, Syllabus of Errors)
but claims "Christianity" condemned human rights.

Impact: Protestant viewer immediately attacks: "That's just the Pope!
What about Luther? Calvin? The Reformation?"

Fix needed: Add Protestant theological sources OR narrow claim to
"Catholic Church" instead of "Christianity."

Priority: CRITICAL - undermines entire argument
```

#### 2. AMBIGUITY GAPS
Check if script acknowledges:
- **Position changes over time:** Did churches/groups change their stance? When?
- **Counter-evidence:** Are there legitimate opposing examples that should be acknowledged?
- **Complexity:** Does script oversimplify contested historical debates?

**Red flags:**
- ❌ Presents 1864 church position as if still current (ignores Vatican II, etc.)
- ❌ Doesn't acknowledge Christian abolitionists when claiming Christians defended slavery
- ❌ Uses absolute language ("always," "never," "all") when reality was mixed
- ❌ Cherry-picks one side of a genuine historical debate without noting the debate existed

**What to output:**
```
🔴 AMBIGUITY GAP
Problem: Script shows Catholic Church condemning religious freedom in 1864
but doesn't mention Vatican II (1965) reversed this position.

Impact: Catholic viewer attacks: "You're ignoring 60 years of Church teaching!
Vatican II's Dignitatis Humanae affirmed religious freedom!"

Fix needed: Add 30-second section acknowledging position changed in 1965.

Priority: HIGH - looks like selective evidence if omitted
```

#### 3. COUNTER-EVIDENCE UNDERPLAYED
Check if script seriously engages opposing arguments:
- **Christian abolitionists:** If claiming Christianity defended slavery, does it address Christian abolitionists?
- **Reform movements:** Were there internal Christian movements that challenged the dominant position?
- **Both sides used same sources:** Does script acknowledge when both sides cited same Bible/documents?

**Red flags:**
- ❌ Mentions counter-evidence in one sentence then dismisses it
- ❌ Doesn't explain WHY minority position lost (just notes it existed)
- ❌ Fails to engage with strongest version of opposing argument

**What to output:**
```
🔴 COUNTER-EVIDENCE UNDERPLAYED
Problem: Script mentions Christian abolitionists in 8 lines but doesn't
explain their theology or why they were minority for 1,400 years.

Impact: Viewer thinks: "Christians were on both sides, so it's about
interpretation, not Christianity itself."

Fix needed: Either (1) show Christian abolitionists used Enlightenment
arguments, OR (2) explain why they were tiny minority for millennium,
OR (3) engage more seriously with this counterargument (30-45 seconds).

Priority: HIGH - weakest part of argument if not addressed
```

#### 4. TIMELINE PRECISION
Check dates and timeframes:
- **Exact dates:** Are "1,800 years" or "centuries" claims mathematically correct?
- **Starting points:** Is the starting date justified? (Augustine 400 AD? Earlier?)
- **Ending points:** When did the practice/belief actually end? (Not when you want it to)

**Red flags:**
- ❌ "1,800 years" but actual math is 1,465 years
- ❌ Vague "centuries" when exact dates are available
- ❌ Cherry-picked endpoints to make pattern look longer/shorter

**What to output:**
```
🔴 TIMELINE PRECISION ERROR
Problem: Script says "1,800 years of Christian defense of slavery" but:
- Augustine: ~400 AD
- Last abolition in Americas: Brazil 1888
- Actual timespan: 1,488 years

Fix needed: Change to "From Augustine in 400 AD to Brazil's abolition in
1888 - nearly 1,500 years."

Priority: MEDIUM - critics will do the math
```

### 🟡 MODERATE PROBLEMS (Should fix, but not blocking)

#### 5. VOICE CONSISTENCY
Does the script sound like Benoit?

**Check against Benoit's voice patterns:**
- ✅ Short, punchy sentences: "They won." "That's retrofitting."
- ✅ Direct transitions: "So when does..." not "Now you might be wondering when..."
- ✅ Minimal buildup before quotes: "Exact quote:" then just read it
- ✅ Fragment emphasis: "Common claim. Sounds reasonable."

**Red flags:**
- ❌ "Here's the thing" used more than once
- ❌ "Now - " excessively (more than 2-3 times)
- ❌ "Look - " or "Listen - "
- ❌ Over-signposting: "I'm going to tell you about..."
- ❌ Formal transitions: "Let me explain...", "To understand this..."
- ❌ Rhetorical setups: "You might be asking..."

**What to output:**
```
🟡 VOICE CONSISTENCY ISSUE
Problem: Script uses "Here's the thing" 5 times and "Now - " at every
transition. Sounds repetitive and unlike Benoit's natural voice.

Fix needed:
- Cut "Here's the thing" to max 1 use
- Replace "Now - " transitions with direct statements
- Example: "Now, what about Protestants?" → "What about Protestants?"

Priority: MEDIUM - affects viewer experience but not argument quality
```

#### 6. RETENTION OPTIMIZATION
Check pacing and engagement:

**Visual breaks (every 30-45 seconds):**
- Document reveals
- Graphics/timelines
- Split screens
- Text on screen moments

**Micro-hooks (every 60-90 seconds):**
- "But it gets worse..."
- "This is where the story flips."
- "And here's the part nobody mentions..."

**Mid-roll hooks (at 4:00 and 8:00):**
- Transition to next claim with question
- "So if churches opposed rights, what about the Founders?"

**Section length:**
- Section 3 (biggest claim) should be under 4 minutes
- No section over 5 minutes without visual break

**What to output:**
```
🟡 RETENTION ISSUE
Problem: Section 3 runs 4:45 without visual breaks or micro-hooks.

Visual gaps:
- 7:00-8:30: No document shown (90 seconds talking head)
- 9:30-10:30: No graphics (60 seconds on one topic)

Missing micro-hooks:
- No transition hook between papal bulls and theology section

Fix needed:
- Add document reveal at 7:45 (Luther quote on screen)
- Add timeline graphic at 9:30 (abolition dates)
- Add micro-hook at 8:30: "And this matters today - because..."

Priority: MEDIUM - affects viewer retention
```

#### 7. MODERN STAKES TIMING
Check when modern relevance appears:

**Best practice:** Modern stakes by 2:00 mark
- Shows why this matters NOW
- Payoff-first structure
- Connects to viewer's present

**What to output:**
```
🟡 MODERN STAKES DELAYED
Problem: Florida/PragerU/Texas examples don't appear until 11:30
(final minute). Viewer doesn't know why this matters for 11 minutes.

Fix needed: Move modern curriculum examples earlier:
- Option 1: Add brief mention at 2:00 after first claim
- Option 2: Add mid-roll bridge at 8:45: "And this matters today -
  because this same argument is now back in school curriculums."

Priority: MEDIUM - improves engagement and relevance
```

### 🟢 WHAT WORKS (Acknowledge strengths)

List 5-7 things the script does well:
- ✅ Primary sources identified with URLs
- ✅ Specific sections cited (Error 15, Section 14)
- ✅ Three-claim structure is clear
- ✅ Pattern revelation (dates → progression)
- ✅ Voice is natural and direct
- ✅ Admits counter-evidence exists

## STEP 3: Generate Critical Viewer Verdict

Answer these questions as if you're the viewer:

### Would I share this?
Yes/Maybe/No + brief reason

### Who would attack it?
List specific groups and their likely critiques:
- Catholics: "You ignored Vatican II"
- Protestants: "Where are Protestant sources?"
- Christian defenders: "You downplayed Christian abolitionists"
- Historians: "Your timeline math is off"

### Does it fulfill channel mission?
**Channel mission:** "Bring history to the wider public by showing people the actual sources - especially when those sources are being misused."

Check:
- ✅ Shows actual sources clearly?
- ✅ Makes archives accessible?
- ✅ Highlights gap between source content and how they're used?
- ✅ Educates viewers on source verification?

### Credibility score: 1-10
Rate overall credibility considering:
- Source balance
- Acknowledgment of ambiguity
- Counter-evidence engagement
- Timeline accuracy
- Voice authenticity

## STEP 4: Output Format

Structure your review exactly like this:

```markdown
# SCRIPT REVIEW - [Title]

**Reviewer:** Critical Viewer Analysis
**Script Length:** [X minutes]
**Status:** READY / NEEDS REVISION / MAJOR PROBLEMS

---

## 🔴 MAJOR PROBLEMS (Must fix before filming)

### 1. [Problem Name]
**Issue:** [What's wrong]
**Impact:** [How viewers will attack this]
**Fix:** [Specific solution with line numbers if applicable]
**Priority:** CRITICAL / HIGH / MEDIUM

[Repeat for each major problem]

---

## 🟡 MODERATE PROBLEMS (Should fix)

### [Problem Number]. [Problem Name]
**Issue:** [What's wrong]
**Fix:** [How to improve it]
**Priority:** MEDIUM / LOW

[Repeat for each moderate problem]

---

## 🟢 WHAT WORKS

- ✅ [Strength 1]
- ✅ [Strength 2]
- ✅ [Strength 3]
[List 5-7 strengths]

---

## 📊 CRITICAL VIEWER VERDICT

**Would I share this?** [Yes/Maybe/No]
[Brief reason]

**Who would attack it?**
- **Catholics:** [Their critique]
- **Protestants:** [Their critique]
- **[Group]:** [Their critique]

**Does it fulfill channel mission?** [Yes/Partially/No]
[Brief assessment]

**Credibility score:** [X/10]
[One sentence explanation]

---

## 🔧 PRIORITY FIXES

**Do first (Blocking issues):**
1. [Fix with line numbers]
2. [Fix with line numbers]

**Do second (Improves quality):**
3. [Fix]
4. [Fix]

**Do third (Nice to have):**
5. [Fix]

---

**Bottom line:** [One paragraph summary of biggest issues and whether
script is ready to film]

**Estimated fix time:** [X hours/minutes]

---

## NEXT STEPS

Want me to:
A) Help fix these issues (rewrite problem sections)
B) Run fact-checker on this script
C) Generate visual staging notes for production
D) Create retention optimization plan
```

## Quality Control

Before sending review, verify:

- [ ] Checked Catholic vs Protestant source balance?
- [ ] Identified all ambiguity gaps?
- [ ] Assessed counter-evidence engagement?
- [ ] Verified timeline math?
- [ ] Checked voice consistency against Benoit's patterns?
- [ ] Assessed retention optimization (visual breaks, micro-hooks)?
- [ ] Noted modern stakes timing?
- [ ] Listed specific attackers and their critiques?
- [ ] Provided actionable fixes with priorities?
- [ ] Offered next steps?

## Integration with Other Skills

**After review, offer:**
- Run **fact-checker** to validate all claims
- Use **script-generator** to rewrite problem sections in Benoit's voice
- Create **visual staging** document for production

## Example Reviews (Reference Patterns)

### EXAMPLE 1 - Major Source Balance Problem

```
🔴 SOURCE BALANCE ISSUE
Problem: Script uses only Catholic documents (Mirari Vos, Syllabus of
Errors) to claim "Christianity" condemned human rights.

Impact: Protestant viewer immediately says: "That's just the Pope! Luther
and Calvin challenged Catholic authority. The Reformation was about
individual conscience!"

Fix needed:
- Add Protestant sources (Luther on government authority, Calvin's Geneva)
- OR narrow claim to "Catholic Church" throughout
- OR acknowledge Protestant positions differed

Priority: CRITICAL - undermines entire Section 1 argument
```

### EXAMPLE 2 - Ambiguity Gap

```
🔴 AMBIGUITY GAP
Problem: Script presents Catholic condemnation of rights (1864) but omits
Vatican II reversal (1965).

Impact: Informed Catholic viewer attacks: "You cherry-picked old documents
and ignored 60 years of updated teaching!"

Fix needed: Add 30-second section at 3:30:
"The Catholic Church changed its position. 1965. Second Vatican Council.
Declaration on Religious Freedom. But that's 101 years after condemning it."

Priority: HIGH - looks like deliberate omission
```

### EXAMPLE 3 - Voice Inconsistency

```
🟡 VOICE CONSISTENCY ISSUE
Problem: Script uses AI-sounding transitions:
- "Now, you might be wondering, when did this phrase actually first appear..."
- "This brings us to an important question..."

Benoit's voice would be:
- "So when does 'Christian human rights' language actually show up?"
- "What about Protestants?"

Fix needed: Cut buildup. State questions directly. Trust the evidence.

Priority: MEDIUM - affects tone but not argument
```

---

**This skill helps prevent credibility attacks and ensures scripts are bulletproof before filming.**
