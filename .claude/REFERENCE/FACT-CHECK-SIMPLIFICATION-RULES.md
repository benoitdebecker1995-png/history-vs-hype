# Simplification Detection Rules for Fact-Checking

This file defines specific patterns that the fact-checker should flag during script review to prevent oversimplification errors.

## Rule 1: Territorial Claims Without Specifics

**Pattern to detect:**
- "claims the entire [country/territory]"
- "wants all of [territory]"
- "[Country] claims [Country]"

**Flag with:**
⚠️ **TERRITORIAL SIMPLIFICATION**: Territorial claims need specific boundaries and percentages.

**Required specifics:**
- River names or geographic boundaries (e.g., "from Sibun River to Sarstoon River")
- Percentage or square kilometers (e.g., "approximately 53% of Belize" or "11,030 square kilometers")
- What's included (e.g., "plus all offshore cayes and islands")

**Example:**
```
❌ "Guatemala claims this entire country"
✅ "Guatemala claims the territory from Sibun River to Sarstoon River—approximately 53% of Belize, plus all offshore cayes and islands"
```

---

## Rule 2: Present Tense for Past Positions

**Pattern to detect:**
- "[Country] refuses to recognize [Country]"
- "[Country] denies [historical event]"
- "[Country] claims [territory]" (without temporal qualifier)
- "[Leader] believes [statement]" (when leader is no longer in power)

**Flag with:**
⚠️ **TEMPORAL INACCURACY**: Statement in present tense may only be true for past period. Add date qualifier.

**Required fix:**
- Add "as of [year]" qualifier
- Use past tense: "refused to recognize until [year]"
- Specify time period: "from [year] to [year]"

**Example:**
```
❌ "Guatemala refuses to recognize it" (when referring to 1981 independence, but Guatemala recognized Belize in 1991)
✅ "Guatemala refused to recognize Belize's independence from 1981 until September 1991"
```

---

## Rule 3: Absolutist Language Without Qualifiers

**Pattern to detect:**
- "always has been"
- "never [verb]"
- "all historians agree"
- "completely [adjective]"
- "entirely [adjective]"

**Flag with:**
⚠️ **ABSOLUTIST LANGUAGE**: Categorical statement may oversimplify. Consider adding nuance.

**Required check:**
- Is there ANY exception to this claim?
- Do all sources agree on this?
- Is this contested by any credible scholars?

**Example:**
```
❌ "Britain never built the road"
✅ "Britain never built the road, despite negotiating a £50,000 payment in 1863 and proposing alternative routes as late as 1934"
```

---

## Rule 4: Statistics Without Context

**Pattern to detect:**
- Percentages without totals
- Population numbers without date
- Economic figures without comparison
- Geographic measurements without scale

**Flag with:**
⚠️ **MISSING CONTEXT**: Statistic needs context for viewer comprehension.

**Required additions:**
- Date/year for time-sensitive stats
- Total amount if giving percentage
- Comparison point for scale
- Source with specific citation

**Example:**
```
❌ "26,000 Maya people live there"
✅ "According to the 2022 census, approximately 26,000-32,000 Maya people live in the disputed territory—representing the majority population in Toledo District"
```

---

## Rule 5: Contested Claims Presented as Facts

**Pattern to detect:**
- Definitive statements where sources disagree
- "X caused Y" without acknowledging debate
- Historical interpretations stated as objective fact
- Legal positions stated without attribution

**Flag with:**
⚠️ **CONTESTED CLAIM**: Sources disagree on this. Must acknowledge multiple perspectives.

**Required fix:**
- "According to [source], X caused Y, though [other source] argues Z"
- "Guatemala argues [position]. Belize counters that [position]"
- "Some historians interpret this as... Others contend..."

**Example:**
```
❌ "The treaty was signed under duress"
✅ "Guatemalan scholars argue the treaty was signed under duress due to filibuster threats, while British sources present it as standard diplomatic negotiation"
```

---

## Rule 6: Quotes Without Specific Attribution

**Pattern to detect:**
- "[Person] said..." without source
- "[Person] claimed..." without date/context
- Quotes without "in [document/interview]"
- Paraphrased positions without citation

**Flag with:**
⚠️ **UNVERIFIED ATTRIBUTION**: Need specific source for this claim about what someone said/wrote.

**Required specifics:**
- Video timestamp: "In his 2019 video at 3:45..."
- Tweet with date: "April 16, 2025 tweet..."
- Court document: "In court filing 21-CR-175..."
- Published interview: "During BBC interview on [date]..."

**Example:**
```
❌ "Fuentes has claimed there's no evidence"
✅ "In his December 2024 interview with Tucker Carlson at timestamp 14:23, Fuentes claimed 'there is no evidence'"
```

---

## Rule 7: Complex Events Oversimplified to Single Cause

**Pattern to detect:**
- "X caused Y" (for complex historical events)
- "The reason for [event] was [single factor]"
- "This led to [outcome]" (without acknowledging other factors)

**Flag with:**
⚠️ **OVERSIMPLIFIED CAUSATION**: Complex event reduced to single cause. Add contributing factors.

**Required fix:**
- "Among the factors contributing to X were..."
- "While Y played a significant role, Z also contributed"
- "This was one of several factors leading to..."

**Example:**
```
❌ "The treaty caused the border dispute"
✅ "The treaty contributed to the border dispute, alongside British expansion beyond agreed limits, Guatemala's weakness after independence, and the Clayton-Bulwer Treaty's constraints on British colonization"
```

---

## Rule 8: Date Ranges Without Endpoints

**Pattern to detect:**
- "For decades..."
- "For years..."
- "Throughout the [century/era]..."
- "Eventually..."

**Flag with:**
⚠️ **VAGUE TIMELINE**: Replace vague time reference with specific dates.

**Required fix:**
- "For 15 years (1869-1884)..."
- "From 1859 to 1991..."
- "Throughout the 1800s (1821-1900)..."

**Example:**
```
❌ "For years Guatemala tried to negotiate"
✅ "From 1869 to 1884, Guatemala attempted negotiations through diplomatic channels"
```

---

## Implementation in Fact-Checking Workflow

**During script review, fact-checker agent should:**

1. **Scan script for all 8 patterns** listed above
2. **Flag each instance** with specific rule violated
3. **Suggest specific fix** with required additions
4. **Categorize severity:**
   - 🔴 **CRITICAL** - Will cause viewer confusion or factual error (Rules 1, 2, 6)
   - 🟡 **IMPORTANT** - Reduces accuracy, should fix (Rules 3, 4, 5)
   - 🟢 **RECOMMENDED** - Improves clarity, nice to have (Rules 7, 8)

**Example fact-check output:**

```markdown
## SIMPLIFICATION FLAGS

### 🔴 CRITICAL - Fix before filming

**Line 23: "Guatemala claims this entire country"**
- Rule violated: Territorial Simplification (Rule 1)
- Fix: "Guatemala claims territory from Sibun River to Sarstoon River (53% of Belize) plus all offshore cayes"

**Line 142: "Guatemala refuses to recognize it"**
- Rule violated: Temporal Inaccuracy (Rule 2)
- Fix: "Guatemala refused to recognize Belize from 1981 until September 1991"

### 🟡 IMPORTANT - Should fix

**Line 89: "26,000 Maya people"**
- Rule violated: Statistics Without Context (Rule 4)
- Fix: Add census year and geographic distribution

### 🟢 RECOMMENDED - Improves clarity

**Line 156: "For years Britain did nothing"**
- Rule violated: Vague Timeline (Rule 8)
- Fix: "From 1859 to 1869, Britain took no action on road construction"
```

---

## Edge Cases and Judgment Calls

**When simplification is acceptable:**
- In the hook/opening (first 30 seconds) for engagement—BUT must clarify specifics within 2 minutes
- When explaining to contrast with complexity ("Simply put, X—but it's more complicated...")
- When the nuance was already explained earlier in the video

**When to flag even if technically accurate:**
- True statement that creates misleading impression
- Literally accurate but missing critical context
- Correct for one time period but viewer will assume it's current

**User's philosophy:**
"I'd rather cut a claim than oversimplify it. Complexity is the channel's value proposition."

---

## Testing These Rules

**Use this test script to validate the rules:**

```
1. "China claims the entire South China Sea"
   → Should flag: Territorial simplification, needs specific claims (nine-dash line)

2. "Russia refuses to withdraw from Crimea"
   → Should NOT flag: Present tense is accurate as of 2025

3. "Russia annexed Crimea"
   → Should flag: Contested claim (Russia says referendum, Ukraine/West say illegal annexation)

4. "The treaty was violated"
   → Should flag: Need specific article, date, by whom

5. "Historians agree the Crusades were brutal"
   → Should flag: Absolutist language ("all historians")

6. "The war lasted years"
   → Should flag: Vague timeline (needs specific dates)
```
