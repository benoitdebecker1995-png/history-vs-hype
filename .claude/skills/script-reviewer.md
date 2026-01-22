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

#### 3b. ALEX O'CONNOR INTELLECTUAL HONESTY CHECK (Added 2025-12-28)

**Does script use concession-before-rebuttal pattern?**
- ✅ "That's fair. But..." or "They're right about X. Where they go wrong is Y."
- ❌ Jumps straight to criticism without acknowledging valid points

**Does script admit uncertainty where appropriate?**
- ✅ "I'm not entirely sure about this..." when genuinely uncertain
- ❌ False confidence on contested claims

**Does script flag expertise limits?**
- ✅ "I'm probably not the best person to ask about..." when out of lane
- ❌ Presents opinions on specialized topics as expert analysis

**Does script use parallel reasoning to test logic?**
- ✅ "Imagine if [different group] used this same logic..."
- ❌ Critiques logic without demonstrating its inconsistency

**Red flags:**
- ❌ No concessions anywhere in script (appears one-sided)
- ❌ Absolute certainty on genuinely contested claims
- ❌ Logic critiqued but not tested with parallel examples

**What to output:**
```
🟡 INTELLECTUAL HONESTY ISSUE
Problem: Script critiques [position] without conceding any valid points.
No use of "That's fair. But..." or "They're right about..." pattern.

Impact: Viewer with nuanced view thinks: "This person isn't being fair.
They're not acknowledging what I know to be true about the other side."

Fix needed: Add 1-2 concessions before major rebuttals:
- "To be fair, [valid point from other side]. But..."
- "They're right that [concession]. Where they go wrong is..."

Priority: MEDIUM - affects perceived fairness and credibility
```

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

#### 4. KRAUT DEPTH CHECK (Updated 2025-12-29)

**This is the most common script weakness.** Scripts explain WHAT happened but not WHY.

**Acceptable Causal Connectors (≥3 required):**
"consequently," "as a consequence," "thereby," "by doing so," "which meant that," "meaning that," "as a result," "the result was," "this produced," "this created," "because of this," "for this reason," "the effect was," "the outcome was"

**Check for:**
- **Causal connectors:** Does script use connectors from the list above? (Need ≥3 VALID ones)
- **Comparative analysis:** Is there at least one "While in X... in Y" comparison with explanation of WHY different?
- **Mechanism explanation:** Does script show HOW things worked, not just THAT they happened?
- **Opening framework:** Does opening use Pattern→Exception OR Both-Extremes-Wrong?
- **Modern echoes:** Are there modern relevance callbacks every 2-3 minutes?

**CAUSAL VALIDITY TEST (Apply to each connector):**
Ask: "If I remove the previous sentence, does the connector still make sense?"
- YES = cosmetic connector (does NOT count toward ≥3) → FAIL
- NO = genuine causal link (counts toward ≥3) → PASS

**CAUSAL DEPTH CHECK (Apply to connectors that pass Validity Test) - Added 2025-12-29:**
Ask: "Does the surrounding text explain HOW the cause produced the effect, or just THAT it did?"
- THAT only (motive → outcome, no transmission) → ⚠️ SHALLOW CAUSATION
- HOW explained (motive → action → intermediate effect → outcome) → PASS

**Requirement:** ≥1 mechanism-level explanation per major argument section
**Enforcement:** SOFT-BLOCKING (proceeds with warning, must resolve before filming)

| Level | Pattern | Example |
|-------|---------|---------|
| **Assertion** (shallow) | "They needed X, so they did Y" | "The Ptolemies needed legitimacy. Consequently, they invested in culture." |
| **Mechanism** (deep) | "They needed X. To achieve this, they [action] which [effect], thereby Y" | "The Ptolemies needed legitimacy. To achieve this, they funded scholars who produced authoritative texts, which positioned Alexandria as the intellectual center—thereby attracting more scholars and reinforcing their cultural authority." |

**Red flags:**
- ❌ "X happened. Then Y happened." (no causal connection)
- ❌ "Consequently" used but previous sentence doesn't explain WHY (cosmetic)
- ❌ No comparisons to similar cases
- ❌ States effects without explaining mechanisms
- ❌ Opening goes straight to content without framing extremes
- ❌ Modern relevance only appears at end

**What to output:**
```
🔴 KRAUT DEPTH FAILURE
Problem: Script explains WHAT happened (Mongols invaded, Russia changed)
but not WHY the outcome was different from other conquests.

Missing:
- Causal connectors: Found 2 uses but only 1 passes Causal Validity Test
  - Line 45: "Consequently, Russia changed" ← COSMETIC (previous sentence doesn't explain cause)
  - Line 78: "As a result of the Mongol tax system" ← VALID (cause stated)
- No comparative analysis (doesn't compare to Magyar/Seljuk/Ottoman conquests)
- No mechanism (says "peasants were controlled" but not HOW vodka did this)

Causal Depth Issues:
- ⚠️ SHALLOW CAUSATION at Line 78: "The Mongols needed control, so they taxed vodka"
  → Motive stated but transmission path missing
  → Fix: "The Mongols needed control. They granted monopoly licenses to loyal nobles,
     who then controlled village access to vodka, thereby making peasant communities
     dependent on state-approved distribution."

Impact: Script feels shallow. Viewer doesn't understand the WHY,
just memorizes facts. Lower retention, less shareability.

Fix needed:
1. Add causal chain with valid connectors: "Because X, and because Y, consequently Z"
2. Add comparison: "While in Europe [opposite outcome], in [subject]..."
3. Add mechanism: Show step-by-step HOW the process worked
4. Expand ≥1 shallow causation per section into full mechanism

Priority: CRITICAL - This is the primary quality differentiator
```

See: `.claude/REFERENCE/causal-chain-examples.md` for patterns
See: `.claude/REFERENCE/creator-techniques.md` → KRAUT section

#### 4b. MAP FRAMING CHECK (TERRITORIAL VIDEOS ONLY - Added 2025-12-29)

**Apply if video type = TERRITORIAL (border disputes, sovereignty claims, geographic anomalies)**

**Check for:**
- **Geographic hook:** Does script open with "zoom in and things get strange" or similar geographic reveal in first 30 seconds?
- **Strategic implications:** Are ≥3 strategic implications stacked before 2:00 mark?
- **"How did this happen?" transition:** Is there explicit pivot from current situation to historical cause?
- **Specific measurements:** Are there ≥5 specific numbers (distances, populations, dates, percentages)?

**Red flags:**
- ❌ Opens with historical background instead of current map oddity
- ❌ No specific measurements in first 90 seconds
- ❌ Strategic implications stated but not stacked (only 1-2 reasons why territory matters)
- ❌ "How did this happen?" transition missing or weak
- ❌ Numbers are vague ("hundreds of years" instead of "684 years")

**What to output:**
```
🔴 MAP FRAMING FAILURE
Problem: Territorial dispute video doesn't establish geographic stakes early.

Missing:
- No geographic hook in first 30 seconds (opens with 1859 treaty background)
- Only 2 strategic implications (needs ≥3)
- "How did this happen?" transition at 3:45 (too late, should be ~2:00)
- Only 3 specific measurements (needs ≥5)

Impact: Viewer doesn't feel the geographic tension. Drops off before
understanding why this territory matters.

Fix needed:
1. Open with map showing the anomaly before explaining history
2. Stack strategic implications: military, economic, political stakes
3. Move historical transition earlier (~2:00)
4. Add specific numbers: distances, populations, exact dates

Priority: CRITICAL for territorial videos - this is the hook structure
```

See: `.claude/REFERENCE/map-framing-checklist.md` for full checklist
See: `.claude/REFERENCE/map-narration-patterns.md` for copy-paste templates

#### 4c. THESIS ADVANCEMENT CHECK (ALL VIDEOS - Added 2025-12-29)

**Check for:**
- **Section purpose:** Does every section either support thesis, address counterargument, or provide necessary context?
- **No bloat:** Is there any section >90 seconds that doesn't advance the argument?
- **Necessity test:** If you removed any section, would the argument be weaker?

**Red flags:**
- ❌ Interesting historical tangent that doesn't connect to thesis
- ❌ Section exists because research found it, not because argument needs it
- ❌ Over-explaining context that viewer doesn't need for the argument
- ❌ Repetition of points already made

**What to output:**
```
🟡 THESIS ADVANCEMENT ISSUE
Problem: Section at 4:30-6:00 provides interesting context but doesn't
advance the main argument.

Analysis:
- Section topic: Byzantine trade routes
- Thesis: "Colonial borders still cause modern conflicts"
- Connection: None clear

Impact: Viewer may find it interesting but loses narrative momentum.
Runtime inflated without improving argument strength.

Fix needed:
- Option A: Cut section entirely (saves 90 seconds)
- Option B: Add explicit connection: "And this matters because..."
- Option C: Move to research notes for future video

Priority: MEDIUM - affects pacing but not argument validity
```

#### 4d. ATTRIBUTION VERIFICATION CHECK (REVISIONS ONLY - Added 2025-12-29)

**Trigger:** Any of the following added AFTER initial draft:
- Named scholar/historian
- Specific publication year
- Page number citation
- Claim about scholarly consensus ("historians agree," "mainstream since X")

**For each triggered item, check:**
1. Is this in `01-VERIFIED-RESEARCH.md`?
   - YES → PASS
   - NO → 🔴 UNVERIFIED REVISION ATTRIBUTION

2. Does claim assert scholarly consensus without named source?
   - YES → ⚠️ CONSENSUS CLAIM UNANCHORED

**Enforcement:** SOFT-BLOCKING (script can proceed to review, filming gate blocks until resolved)

**What to output:**
```
🔴 UNVERIFIED REVISION ATTRIBUTION
Problem: Revision added citations not in VERIFIED-RESEARCH.md

Flagged items:
- Line 145: "Bagnall's quantitative analyses in the 1990s..."
  → Scholar + decade cited, not in research doc
  → Action: VERIFY exact publication OR REMOVE
- Line 203: "historians moved on from this debate by 2005"
  → Consensus claim with specific date, not sourced
  → Action: CITE specific historian OR SOFTEN to "recent scholarship suggests"

⚠️ CONSENSUS CLAIM UNANCHORED
- Line 89: "Among classicists, this is settled"
  → No named scholar anchoring the claim
  → Action: Add "As [Name] argues in [Work]..." OR remove consensus framing

Impact: Plausible-sounding citations may be misremembered.
Informed viewer or commenter will check.

Fix options:
1. Verify against primary source and add to VERIFIED-RESEARCH.md
2. Remove unverified attribution and use softer language
3. Flag for pre-filming verification (add to B-ROLL-CHECKLIST.md)

Priority: HIGH - Must resolve before filming
```

**Scope limitation:** This check ONLY applies to revisions. Initial draft citations are covered by Phase 1 verification.

---

#### 5. TIMELINE PRECISION
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

**Alex O'Connor Intellectual Honesty Checks (Added 2025-12-28):**
- [ ] Script uses concession-before-rebuttal pattern at least once?
- [ ] Script admits uncertainty where genuinely uncertain?
- [ ] Script flags expertise limits when appropriate?
- [ ] Script uses parallel reasoning to test logical consistency?
- [ ] No strawmanning (engages strongest version of opposing argument)?

**Kraut Depth Check with Causal Validity + Depth Tests (Updated 2025-12-29):**
- [ ] ≥3 causal connectors that pass Causal Validity Test (not cosmetic)?
- [ ] ≥1 mechanism-level explanation per major argument section (Causal Depth Check)?
- [ ] All ⚠️ SHALLOW CAUSATION flags resolved or acknowledged?
- [ ] ≥1 comparative analysis with explanation of WHY different?
- [ ] ≥1 mechanism explanation (HOW, not just WHAT)?
- [ ] Opening uses Pattern→Exception OR Both-Extremes-Wrong?
- [ ] Modern echoes every 2-3 minutes?

**Attribution Verification Check (REVISIONS ONLY - Added 2025-12-29):**
- [ ] All named scholars added in revision verified against VERIFIED-RESEARCH.md?
- [ ] All publication years/page numbers added in revision verified?
- [ ] All consensus claims ("historians agree") anchored with named source?
- [ ] No 🔴 UNVERIFIED REVISION ATTRIBUTION flags unresolved?
- [ ] No ⚠️ CONSENSUS CLAIM UNANCHORED flags unresolved?

**Map Framing Check (TERRITORIAL VIDEOS ONLY - Added 2025-12-29):**
- [ ] Geographic hook in first 30 seconds?
- [ ] ≥3 strategic implications stacked before 2:00?
- [ ] "How did this happen?" transition exists?
- [ ] ≥5 specific measurements throughout?

**Thesis Advancement Check (ALL VIDEOS - Added 2025-12-29):**
- [ ] Every section advances thesis, addresses counterargument, or provides necessary context?
- [ ] No section >90 seconds that doesn't advance argument?
- [ ] If removing any section wouldn't weaken argument → flagged for cutting?

## Integration with Other Skills

**Before script-reviewer:**
- Run **voice check** (`tools/prompt_evaluation.py` channel_voice_check) to verify style patterns

**After review, offer:**
- Run **fact-checker** to validate all claims
- Use **script-generator** (`.claude/skills/script-generator.md`) to rewrite problem sections
- Create **visual staging** document for production
- When all issues fixed → Move project to `_READY_TO_FILM/`

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
