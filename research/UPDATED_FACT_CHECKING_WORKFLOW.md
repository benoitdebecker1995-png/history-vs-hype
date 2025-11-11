# Updated Fact-Checking Workflow
## Integrating Quote Verification into Production Process

**Last Updated:** November 7, 2025
**Reason for Update:** Attribution errors found in Vance Part 2 (Luther/Thornwell quotes)

---

## What Changed

### New Requirement: Quote-Specific Verification

**Old process:**
- General fact-checking of claims
- Source hierarchy for information
- No specific protocol for quote attributions

**New process:**
- **Mandatory Quote Verification Protocol for every historical quote**
- See: `research/QUOTE_VERIFICATION_PROTOCOL.md`

---

## Integrated Production Workflow

### Phase 1: Topic Research (VidIQ/NotebookLM)
**Existing process - no change**
- VidIQ generates initial draft
- Upload sources to NotebookLM
- Run research organization prompts

### Phase 2: Script Development
**Existing process - no change**
- Enhance with Claude Pro
- Structure: Hook → Context → Deep-dive → Modern connections → CTA

### Phase 3: Fact-Checking (ENHANCED)

**Step 3A: General Fact-Checking (Existing)**
✓ Every number has a source
✓ Every date verified
✓ Contested claims clearly labeled
✓ 2+ sources for each major point

**Step 3B: Quote Verification (NEW - MANDATORY)**

For EVERY quote from a historical figure:

1. **Create Quote Tracking Spreadsheet**
   - List every quote in the script
   - Document: Person, Quote, Source claim, Verification status

2. **Run Quote Verification Checklist** (see QUOTE_VERIFICATION_PROTOCOL.md)
   - [ ] Specific work/document identified
   - [ ] Year/date documented
   - [ ] Page/section number found
   - [ ] Exact wording verified
   - [ ] Not a common misattribution
   - [ ] Academic source confirms it

3. **Red Flag Scan**
   - Vague attributions? ("Luther in the 1520s...")
   - Cross-cultural attributions? (Greek concepts → Medieval theologians)
   - Only in secondary sources?
   - Politically convenient?

   **If yes to any: Extra verification required**

4. **Document Citations in Script**
   Format: [Person, *Work Title* (Year), Page/Section]

   Example in script:
   ```
   As James Madison wrote in his Memorial and Remonstrance (1785):
   [QUOTE]

   [CITATION FOR VIDEO DESCRIPTION:
   James Madison, Memorial and Remonstrance Against Religious
   Assessments (1785), Section 1
   Source: founders.archives.gov]
   ```

**Step 3C: Cross-Reference Check**
- Run completed script through NotebookLM fact-check prompt
- Check for logical consistency
- Verify modern relevance connections

### Phase 4: Pre-Production Review (NEW CHECKPOINT)

**Quote Verification Sign-Off**

Before filming begins, complete this checklist:

- [ ] All quotes verified with primary sources
- [ ] All citations documented with specific page/section
- [ ] No vague attributions remain ("1850s says...")
- [ ] Red flag quotes either verified or removed
- [ ] Quote tracking spreadsheet complete
- [ ] Citations ready for video description

**Reviewer signs off:** [Name] verified on [Date]

### Phase 5: Production
**No changes** - proceed with filming

### Phase 6: Post-Production
**Enhanced**
- Add source citations to video description (include page numbers)
- Consider on-screen citations for major quotes
- Keep quote tracking spreadsheet for comment responses

---

## Tools You Now Have

### In `/research/`
1. **fact-checking-protocol.md** (existing - general fact-checking)
2. **QUOTE_VERIFICATION_PROTOCOL.md** (NEW - quote-specific)
3. **UPDATED_FACT_CHECKING_WORKFLOW.md** (this document)

### In `/video-projects/vance-part-2-review/`
4. **ATTRIBUTION_ERRORS_LOG.md** (documents what went wrong)
5. **CORRECTED_PROTESTANT_SLAVERY_SOURCES.md** (correct sources for future reference)

---

## Quick Reference: When to Use Each Document

**Starting a new video?**
→ Use: `fact-checking-protocol.md` + `QUOTE_VERIFICATION_PROTOCOL.md`

**Script has a quote from a historical figure?**
→ Use: `QUOTE_VERIFICATION_PROTOCOL.md` (mandatory checklist)

**Someone challenges your attribution?**
→ Use: `ATTRIBUTION_ERRORS_LOG.md` as template for documenting the issue

**Need Protestant slavery sources for future video?**
→ Use: `CORRECTED_PROTESTANT_SLAVERY_SOURCES.md` as reference

---

## For Already-Recorded Vance Part 2 Video

Since the video is already recorded with the Luther/Thornwell attribution errors:

### Option 1: Pin a Correction Comment (Recommended)
When you publish, immediately pin a top comment:

```
📌 CORRECTION: At [timestamp], I attributed "slaves as tools with voice"
to Martin Luther. This phrase actually comes from Aristotle's Politics
(350 BCE). Luther DID defend social hierarchy and condemned peasant
rebellions (Admonition to Peace, 1525), but I misattributed this
specific phrase.

For a fact-checking channel, accuracy matters. I've implemented stricter
quote verification protocols to prevent this in future videos. Full
corrected sources in the description.
```

### Option 2: Add Correction to Video Description
Include a "CORRECTIONS" section at the top:

```
⚠️ CORRECTION:
- "Tools with voice" quote (timestamp): Actually Aristotle (Politics,
  Book I), not Luther
- Corrected sources: [link to description section with proper citations]
```

### Option 3: On-Screen Annotation (If Platform Allows)
Add a text correction overlay at the relevant timestamp

### Option 4: Accept It and Move Forward
- Error is relatively minor in context of 11-minute video
- Main point (Protestant reformers defended hierarchy) remains true
- Focus on prevention for future videos

---

## Integration with Existing Protocols

### From Master Project Template
**Add to NotebookLM Prompts Section:**

"After generating script, run additional prompt:
'List every quote attributed to a historical figure. For each, identify:
1) The person, 2) The quote, 3) The claimed source. Flag any that lack
specific document/year/page citations.'"

### From Workflow Guide
**Add between "Script Development" and "Production":**

"MANDATORY: Quote Verification Pass
- Use QUOTE_VERIFICATION_PROTOCOL.md
- Complete quote tracking spreadsheet
- Sign-off required before filming"

---

## How to Use the Quote Verification Checklist

### Format for Your Quote Tracking Spreadsheet:

| Quote | Person | Claimed Source | Specific Citation | Verified? | Notes |
|-------|--------|----------------|-------------------|-----------|-------|
| "tools with voice" | Luther | 1520s writings | ❌ NOT FOUND | NO | Actually Aristotle, Politics Book I |
| "infinite wisdom..." | Thornwell | 1850s sermon | ❌ VAGUE | NO | Need specific work title |
| "pride and indolence..." | Madison | Memorial & Remon. | ✅ Section 1, 1785 | YES | founders.archives.gov verified |

**Before filming:** Every row must show "YES" in Verified column

---

## Enforcement

### This is Now Part of Your Process

Just like you wouldn't film without:
- ✓ Checking papal documents on papalencyclicals.net
- ✓ Verifying founder quotes on founders.archives.gov
- ✓ Running NotebookLM fact-check prompts

You also won't film without:
- ✓ Running Quote Verification Protocol
- ✓ Completing quote tracking spreadsheet
- ✓ Getting specific citations for every quote

---

## Why This Matters

**Your channel's credibility depends on accuracy.**

One misattributed quote can:
- Undermine your fact-checking of others
- Give opponents ammunition to dismiss your work
- Damage trust with your audience
- Contradict your core mission (historical integrity)

**Prevention is worth the extra 30-60 minutes per video.**

---

## Questions to Ask Yourself During Verification

For every quote in your script:

1. "If someone asks me where this person said this, can I give them a specific book, page number, and year?"

2. "Have I seen this quote in multiple academic sources, or just in blogs/websites?"

3. "Does this quote sound suspiciously perfect for my argument?"

4. "Is the person I'm attributing this to actually from the right time period to have said this?"

5. "If I'm wrong about this attribution, would it undermine my main argument?"

If you can't confidently answer these questions: **Don't use the quote.**

---

## Future Video Checklist Addition

Add this to your pre-production checklist:

```
QUOTE VERIFICATION (Required before filming)
- [ ] Quote tracking spreadsheet created
- [ ] Every quote has specific citation (work, year, page)
- [ ] Red flag quotes double-checked
- [ ] Common misattributions checked
- [ ] All citations ready for description
- [ ] Verified by: __________ Date: __________
```

---

## Long-Term: Build a Quote Database

As you research future videos, maintain a database of verified quotes you might reuse:

**Format:**
```
QUOTE: "The government of the United States is not in any sense
founded on the Christian Religion"

PERSON: John Adams (signed) / U.S. Senate (ratified)

SOURCE: Treaty of Tripoli, Article 11

DATE: Ratified June 7, 1797; Signed June 10, 1797

FULL CITATION: Treaty of Peace and Friendship between the United
States and the Bey and Subjects of Tripoli of Barbary, Article 11

WHERE TO FIND: Avalon Project (Yale), founders.archives.gov

VERIFIED: ✅ Primary source confirmed

COMMON MISATTRIBUTIONS: None known

NOTES: Ratified unanimously without debate
```

Over time, you'll build a library of rock-solid quotes you can reuse with confidence.

---

## Summary: Three-Tier Fact-Checking System

**Tier 1: General Facts** (existing protocol)
- Numbers, dates, events
- 2+ sources required
- Academic sources prioritized

**Tier 2: Quotes** (NEW protocol)
- Specific citations mandatory
- Primary source verification required
- Red flag screening

**Tier 3: Interpretations** (existing protocol)
- Scholarly consensus documented
- Counter-evidence acknowledged
- Multiple perspectives when contested

All three tiers required before filming.

---

*Remember: Taking an extra hour to verify quotes properly is faster than dealing with corrections, lost credibility, and comment section debates after publication.*
