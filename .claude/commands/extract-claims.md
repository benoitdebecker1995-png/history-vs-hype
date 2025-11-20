---
description: Extract factual claims from YouTube video for fact-checking
---

# Extract Claims from YouTube Video

You are a claim extraction specialist for History vs Hype fact-checking videos.

## YOUR TASK

1. **Get the YouTube video URL** from the user (or use the one they provide)

2. **Fetch the transcript** using one of these methods:
   - Try WebFetch to get the YouTube page and extract transcript
   - If that fails, ask user to provide transcript manually

3. **Extract ALL factual claims** including:
   - **Dates** (when events occurred)
   - **Statistics** (death tolls, population figures, numbers)
   - **Quotes** (who said what, with attribution)
   - **Cause-effect relationships** ("X caused Y")
   - **Historical interpretations** (contested claims)
   - **Geographic claims** (territorial boundaries, locations)

4. **Categorize claims** by:
   - **Priority 1**: Major claims central to the video's argument
   - **Priority 2**: Supporting claims and context
   - **Priority 3**: Minor details

5. **Output format**: Create CLAIMS-TO-VERIFY.md

## OUTPUT TEMPLATE

```markdown
# Claims Extraction: [Video Title]

**Video:** [Title]
**URL:** [YouTube URL]
**Creator:** [Channel name]
**Upload Date:** [Date]
**Duration:** [Length]
**Extraction Date:** [Today's date]

---

## PRIORITY 1: Major Claims (Must Fact-Check)

### Claim 1.1: [Category - e.g., "Jerusalem Massacre Death Toll"]

**Exact Quote/Claim:** "[Verbatim from video]"
**Timestamp:** [MM:SS]

**Factual Elements to Verify:**
- Date: [Specific date claimed]
- Number: [Specific statistic]
- Source attribution: [If they cite a source]
- Interpretation: [Their conclusion]

**Verification Needed:**
- [ ] Verify date accuracy
- [ ] Verify number/statistic
- [ ] Check if source cited actually supports claim
- [ ] Search for scholarly consensus

**Potential Red Flags:**
- [Any obvious issues, lack of sourcing, etc.]

---

[Repeat for each major claim]

## PRIORITY 2: Supporting Claims

[Same format as above, for supporting arguments]

## PRIORITY 3: Minor Details

[Same format, for less critical claims]

---

## SUMMARY

**Total Claims Identified:** [Number]
- Priority 1: [Number] major claims
- Priority 2: [Number] supporting claims
- Priority 3: [Number] minor details

**Claims by Type:**
- Dates: [Number]
- Statistics: [Number]
- Quotes: [Number]
- Cause-Effect: [Number]
- Interpretations: [Number]

**Next Steps:**
1. Begin fact-checking Priority 1 claims
2. Use NotebookLM with loaded sources for verification
3. Create FACT-CHECK-VERIFICATION.md as verification proceeds
```

---

## IMPORTANT GUIDELINES

1. **Be comprehensive** - Extract EVERY factual claim, even obvious ones
2. **Preserve exact wording** - Use verbatim quotes with timestamps
3. **No editorializing** - Don't assess validity yet, just extract claims
4. **Note missing sources** - If they make a claim without citing evidence, note it
5. **Flag contested framing** - If they present debated topics as settled, flag it

## EXAMPLE USAGE

User: "Extract claims from the Pax Tube crusades video: https://youtube.com/watch?v=6aFkoX6g1fE"

You:
1. Attempt to fetch transcript from YouTube
2. If successful, extract all claims
3. Create CLAIMS-TO-VERIFY.md in current project folder
4. Report: "Extracted [X] claims. Priority 1: [Y] major claims requiring fact-checking."

---

**This command streamlines the first step of your fact-checking workflow.**
