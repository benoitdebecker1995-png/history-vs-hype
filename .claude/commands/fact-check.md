---
description: Fact-check a script using the History vs Hype protocol
---

You are fact-checking a video script for the History vs Hype YouTube channel. This channel prioritizes **historical integrity above all** - every claim must be verified with credible sources.

**Use the fact-checker skill** for systematic 3-tier verification and detailed reporting.

## Your Task

1. **Identify the script to fact-check:**
   - Ask which script file they want to fact-check
   - Or if they'll paste the script content

2. **Extract all factual claims:**
   - **Statistics & numbers** (dates, percentages, quantities, distances)
   - **Direct quotes** (from historical figures, documents, current politicians)
   - **Historical events** (battles, treaties, laws, decisions)
   - **Cause-effect claims** (X led to Y, X caused Z)
   - **Attribution claims** (who said/wrote/did what)

3. **Organize claims by priority:**

   **TIER 1 - SMOKING GUN EVIDENCE (Must verify before filming):**
   - Primary document quotes
   - Key statistics that form the thesis
   - Viral quotes from current figures
   - Claims that would discredit the video if wrong

   **TIER 2 - SUPPORTING CLAIMS (Need 2+ sources):**
   - Historical event details
   - Timeline/date claims
   - Attribution claims
   - Academic consensus statements

   **TIER 3 - CONTEXTUAL (Should verify):**
   - Background information
   - Comparative data
   - Secondary quotes
   - Common knowledge claims

   **CONTESTED CLAIMS (Present both sides):**
   - Any claim where sources disagree
   - Claims that require "some historians argue..."
   - Interpretation-dependent statements

4. **Check against source hierarchy:**

   **Most Reliable (Tier 1):**
   - Primary documents (treaties, census data, government archives)
   - Peer-reviewed academic publications
   - Expert historians specializing in the topic

   **Use with Caution:**
   - Respected journalists with expertise
   - International organization reports
   - Declassified government documents (note potential bias)

   **Flag These:**
   - Opinion pieces without sources
   - Claims without attribution
   - Statistics without clear methodology
   - "Common knowledge" that can't be verified

5. **Run simplification detection:**

   **CRITICAL: Before generating report, scan script for simplification patterns**

   Read `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` and check for:
   - Territorial claims without boundaries/percentages (Rule 1)
   - Present tense for past positions (Rule 2)
   - Absolutist language without qualifiers (Rule 3)
   - Statistics without context (Rule 4)
   - Contested claims as facts (Rule 5)
   - Quotes without specific attribution (Rule 6)
   - Complex events oversimplified (Rule 7)
   - Vague timelines (Rule 8)

   Flag each violation with severity:
   - 🔴 CRITICAL - Will cause viewer confusion or factual error
   - 🟡 IMPORTANT - Reduces accuracy, should fix
   - 🟢 RECOMMENDED - Improves clarity, nice to have

6. **Generate fact-check report:**

   ```markdown
   # FACT-CHECK REPORT: [Script Title]

   ## 🚨 SIMPLIFICATION FLAGS

   ### 🔴 CRITICAL - Fix before filming
   [List Rule 1, 2, 6 violations with suggested fixes]

   ### 🟡 IMPORTANT - Should fix
   [List Rule 3, 4, 5 violations with suggested fixes]

   ### 🟢 RECOMMENDED - Improves clarity
   [List Rule 7, 8 violations with suggested fixes]

   ## ✅ VERIFIED CLAIMS (Source confirmed)
   1. [Claim] → Source: [Exact citation]
   2. [Claim] → Source: [Exact citation]

   ## ⚠️ NEEDS VERIFICATION (Missing or weak sources)
   1. [Claim] → Issue: [What's missing/unclear]
   2. [Claim] → Issue: [What's missing/unclear]

   ## ❌ INCORRECT OR MISLEADING
   1. [Claim] → Problem: [What's wrong]
      Correction: [Accurate information]

   ## 🔍 CONTESTED CLAIMS (Must acknowledge both sides)
   1. [Claim] → Disagreement: [Who says what]
      Recommendation: [How to present fairly]

   ## 📝 MISSING CONTEXT
   1. [Claim] → Additional context needed: [What's missing]

   ## OVERALL ASSESSMENT
   - Ready to film? [YES/NO]
   - Critical simplifications: [Number]
   - Source issues: [Number]
   - Recommendations: [What needs to be fixed/added]
   ```

6. **Provide NotebookLM guidance:**
   - If they have NotebookLM research notebook, offer to provide the fact-check prompt
   - Prompt from `guides/History-vs-Hype_Master-Project-Template.md`

## Pre-Production Checklist

Before approving for filming:
- [ ] Every number has a source
- [ ] Every quote verified from original
- [ ] Contested claims clearly labeled
- [ ] At least 2 sources for each major point
- [ ] No logical fallacies in arguments
- [ ] Counter-evidence acknowledged where relevant
- [ ] **Simplification check complete** (all 🔴 CRITICAL flags resolved)
- [ ] Territorial claims have specific boundaries/percentages
- [ ] Present-tense statements have temporal accuracy
- [ ] Attributions have specific sources (video timestamp, document, interview date)

## Key Principle

**If you can't verify it with 2+ credible sources, it doesn't go in the script.**

This isn't optional. Historical integrity is the channel's core value. Better to cut a claim than to include something unverified.
