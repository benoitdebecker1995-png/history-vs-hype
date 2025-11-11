# Fact-Checker Skill - History vs Hype

Systematically verify every factual claim in a script using 3-tier fact-checking methodology. Output detailed verification reports identifying what's verified, what has errors, and what needs additional checking.

## Activation

Use when user says:
- "Fact-check this script"
- "Verify the claims in this script"
- "Run fact-checker on this"
- "Check if these facts are accurate"

## CRITICAL: Fact-Check VidIQ Angles Too

**IMPORTANT REMINDER:** When VidIQ or other optimization tools suggest "catchy angles" (like "It Was Never Used"), fact-check those angles FIRST before adopting them.

**Example:** VidIQ might suggest "Sykes-Picot Was Never Used" for clickability, but historically this oversimplifies - while the exact agreement was modified, it did influence the mandate system. Maintain historical integrity over clickability.

**Rule:** If a title claim would fail your fact-checking standards, don't use it - even if it has low competition.

---

## STEP 1: Read Script and Extract Claims

Ask user for script file path if not provided.

Extract all factual claims and categorize into 3 tiers:

### TIER 1: SMOKING GUN EVIDENCE (Must verify before filming)
These are the core claims the entire argument rests on:
- Primary document quotes (papal bulls, treaties, founding documents)
- Key statistics that drive the narrative
- Viral quotes from current figures
- Central historical events (dates, locations, participants)

### TIER 2: SUPPORTING CLAIMS (Need 2+ sources each)
These support the main argument:
- Historical event details (timelines, casualties, outcomes)
- Attribution claims (who said/wrote what)
- Cause-effect relationships
- Contextual statistics

### TIER 3: CONTEXTUAL (Should verify)
These add depth but aren't essential:
- Background information
- Comparative data
- Secondary quotes from scholars
- Academic interpretations

## STEP 2: Verification Methodology

For each claim, use available tools:

**1. WebSearch** for:
- Academic sources (Google Scholar results)
- Official archives (government websites, university presses)
- Primary source databases
- Reputable news verification

**2. WebFetch** for:
- Specific document verification (papal encyclicals, treaties)
- University press book descriptions
- Archive page content
- Official statements

**3. Cross-reference requirements:**
- Tier 1 claims need verification from authoritative source
- Tier 2 claims need 2+ sources or strong single authoritative source
- Tier 3 claims need at least plausibility check

## STEP 3: Document Verification Standards

### For PRIMARY DOCUMENTS (Papal bulls, treaties, letters):

**VERIFY:**
- ✅ Exact wording of quote
- ✅ Correct section/article number
- ✅ Correct date
- ✅ Correct attribution (who issued it)
- ✅ Accessible URL to source

**Common errors:**
- ❌ Paraphrased quote presented as exact
- ❌ Wrong section number
- ❌ Translation variations not noted
- ❌ Context omitted

**Output format:**
```
✅ VERIFIED: Mirari Vos Section 14
Exact quote: [full quote]
Source: papalencyclicals.net/greg16/g16mirar.htm
Match: EXACT (quote is verbatim from English translation)

Minor note: Latin original says [X], English translation says [Y].
Script uses English version - acceptable.
```

OR

```
❌ ERROR FOUND: Syllabus of Errors
Script says: "Error 15: 'Every man is free to embrace that religion
which he shall consider true.'"

Actual text: "Every man is free to embrace and profess that religion
which, guided by the light of reason, he shall consider true."

Issue: Missing "and profess" and "guided by the light of reason"
Priority: MEDIUM - substance correct but quote should be exact
Fix: Use complete quote
```

### For STATISTICS & NUMBERS:

**VERIFY:**
- ✅ Correct number
- ✅ Correct units (don't mix nautical miles and kilometers)
- ✅ Correct context (is "one-third of army" actually "one-fifth of frontier forces"?)
- ✅ Source attribution

**Common errors:**
- ❌ Rounded numbers presented as exact
- ❌ "One-third" when it's actually "one-fifth"
- ❌ Mixing different casualty counts from different sources
- ❌ Timeframe inflation ("1,800 years" when it's 1,465)

**Output format:**
```
❌ CRITICAL ERROR FOUND
Script claim: "President Buchanan sends one-third of the entire U.S.
Army to Utah"

Actual fact: Approximately one-fifth of regular frontier forces (~5,000
troops)

Source: Wikipedia - Utah War; BYU Special Collections
Issue: Incorrect fraction and incorrect base (not "entire army")
Priority: CRITICAL - factual error
Fix: "President Buchanan sends roughly one-fifth of the frontier forces
- about 5,000 troops - to Utah"
```

### For ACADEMIC CLAIMS (historian quotes, book citations):

**VERIFY:**
- ✅ Person exists and has claimed credentials
- ✅ Book/article exists
- ✅ Quote attribution is accurate (or at least plausible)
- ✅ Academic affiliation correct

**Common errors:**
- ❌ Wrong university (Samuel Moyn at Yale, not Harvard)
- ❌ Wrong affiliation (David Sehat not at Oxford - book published by Oxford UP)
- ❌ Quote not found in source (or paraphrased)

**Output format:**
```
✅ VERIFIED: Samuel Moyn claim
Person: Samuel Moyn, Professor at Yale Law School
Book: "Christian Human Rights" (University of Pennsylvania Press, 2015)
Core thesis verified: Human rights language "reinvented" in 1930s-1940s
by Christian thinkers

⚠️ MINOR CORRECTION NEEDED:
Script says: "historian at Harvard"
Correct: "historian at Yale"
Priority: LOW - substance correct, just wrong university
```

### For HISTORICAL EVENTS:

**VERIFY:**
- ✅ Correct date
- ✅ Correct location
- ✅ Correct participants
- ✅ Correct outcome/casualties
- ✅ Correct cause (if claimed)

**Output format:**
```
✅ VERIFIED: 1844 Philadelphia riots
Date: May 6-8 and July 6-7, 1844 ✅
Cause: Bible controversy (Catholic Douay-Rheims vs Protestant KJV) ✅
Military response: Over 4,000 troops deployed ✅
Casualties: At least 20 dead ✅

Script says: "They call in martial law"
Actual: Military force deployed, but not technically "martial law"
Priority: LOW - close enough, but "military force" more accurate
```

## STEP 4: Generate Tier Reports

Create three separate reports:

### TIER 1 REPORT

```markdown
# TIER 1 FACT-CHECK RESULTS - [Script Title]

**Date:** [Date]
**Status:** [TIER 1 COMPLETE - X ITEMS VERIFIED]

---

## SUMMARY OF FINDINGS

**✅ VERIFIED (X items):** [List]
**❌ ERROR (X items):** [List with severity]
**⚠️ COULD NOT VERIFY (X items):** [List with reason]

---

## 1. [CLAIM NAME] - [✅ VERIFIED / ❌ ERROR / ⚠️ UNCERTAIN]

### Script Claims (Lines X-Y):
> [Exact quote from script]

### ACTUAL FINDINGS:

[What you found in sources]

**Source:** [URL or citation]

### [✅/❌/⚠️] ASSESSMENT:
[Your verdict on accuracy]

### [✅/⚠️/❌] RECOMMENDATION:
[Keep as-is / Minor correction / Major rewrite needed]

**Corrected text (if needed):**
```
[Exact corrected wording]
```

**Priority:** [CRITICAL / HIGH / MEDIUM / LOW]

---

[Repeat for each Tier 1 claim]

---

## TIER 1 VERDICT

**Can you film with current script (TIER 1 items only)?** [✅ YES / ⚠️ WITH CORRECTIONS / ❌ NO]

**Critical errors found:** [Number]
**Minor corrections needed:** [Number]

**Estimated time to fix:** [X minutes/hours]

---
```

### TIER 2 & TIER 3 REPORTS

Use same format structure as Tier 1.

## STEP 5: Combined Summary Report

After all three tiers, create summary:

```markdown
# COMBINED FACT-CHECK VERDICT - [Script Title]

**Date:** [Date]
**Total Claims Checked:** [Number across all tiers]

---

## OVERALL FINDINGS

**✅ Verified:** X/Y claims (Z%)
**❌ Errors found:** X claims
**⚠️ Needs verification:** X claims

---

## CRITICAL ERRORS (Must fix before filming)

1. **[Claim]** - Line X
   - Error: [What's wrong]
   - Fix: [Corrected version]

[List all critical/high priority errors]

---

## MINOR CORRECTIONS (Should fix)

1. **[Claim]** - Line X
   - Issue: [Minor problem]
   - Fix: [Correction]

[List medium/low priority issues]

---

## COULD NOT VERIFY (Needs additional research)

1. **[Claim]** - Line X
   - Issue: [Why couldn't verify]
   - Recommendation: [What to do]

---

## PRIORITY ACTION PLAN

### ❌ MUST FIX (Script cannot be filmed):
- [ ] [Specific fix with line number]
- [ ] [Specific fix with line number]

### ⚠️ SHOULD FIX (Improves credibility):
- [ ] [Specific fix]
- [ ] [Specific fix]

### ✅ OPTIONAL (Nice to have):
- [ ] [Enhancement]

---

## FILMING STATUS

**Ready to film?** [✅ YES / ⚠️ AFTER CORRECTIONS / ❌ NO - MAJOR ERRORS]

**If NO:** [List blocking issues]
**If WITH CORRECTIONS:** [List required fixes + time estimate]
**If YES:** [Note any optional improvements]

---
```

## STEP 6: Special Checks

### CHECK 1: Catholic vs Protestant Sources
If script makes claims about "Christianity," verify:
- Are there Catholic AND Protestant sources?
- Or does script only cite one tradition?

Flag if imbalanced.

### CHECK 2: Timeline Math
For any "X years" claims:
- Calculate actual years between dates
- Flag if math is off by >50 years

### CHECK 3: Position Changes Over Time
Check if:
- Institution changed position (Vatican II, etc.)
- Script acknowledges this or presents old position as current?

### CHECK 4: Quote Attribution
For every "direct quote":
- Is it actually direct or paraphrased?
- Page number provided?
- Accessible source?

## STEP 7: Verification Limitations

Be honest about what you cannot verify:

```
⚠️ COULD NOT VERIFY: Micheline Ishay exact quote

**Script Quote:** 'Christianity stood for values inimical to those we
now associate with rights.'

**Issue:** Web search unavailable for exact page number verification.
Book confirmed: "The History of Human Rights" (UC Press) exists.
Ishay IS recognized historian.

**Recommendation:**
Option 1 (Safest): Get book and verify page number before filming
Option 2 (If unavailable): Rephrase to paraphrase instead of direct quote
Option 3 (If you have book): Add page number to script

**Priority:** MEDIUM - if quote is misworded, hurts credibility
```

## Output Standards

Every fact-check report must include:

✅ **Clear verdicts:** VERIFIED / ERROR / UNCERTAIN
✅ **Exact sources:** URLs, citations, page numbers when available
✅ **Priority ratings:** CRITICAL / HIGH / MEDIUM / LOW
✅ **Corrected text:** When errors found, provide exact replacement wording
✅ **Filming status:** Clear YES/NO/WITH CORRECTIONS verdict
✅ **Time estimate:** How long will fixes take
✅ **Action plan:** Specific checklist of what to fix

## Integration with Other Skills

**After fact-checking, offer:**
- Run **script-reviewer** to check argument quality and retention
- Use **script-generator** to rewrite corrected sections in Benoit's voice
- Generate **source list** formatted for video description

## Quality Control Checklist

Before sending fact-check report, verify:

- [ ] Checked every Tier 1 claim with authoritative source?
- [ ] Provided exact corrected wording for every error?
- [ ] Rated every issue by priority (CRITICAL/HIGH/MEDIUM/LOW)?
- [ ] Included accessible URLs for primary sources?
- [ ] Calculated timeline math for "X years" claims?
- [ ] Flagged Catholic-only vs Protestant-only source imbalances?
- [ ] Noted where position changes over time weren't acknowledged?
- [ ] Gave clear filming verdict (YES/NO/WITH CORRECTIONS)?
- [ ] Provided time estimate for fixes?
- [ ] Created actionable checklist?

---

**This skill ensures every factual claim is verified before filming, preventing credibility attacks and embarrassing corrections after publication.**
