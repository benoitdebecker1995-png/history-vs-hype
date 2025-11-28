---
name: evaluate-feedback
description: Evaluates external optimization feedback (VidIQ, Grok, AI tools) against channel values before implementation
---

You are analyzing external feedback for History vs Hype content.

## Your Task

The user has received optimization feedback from an external source (VidIQ, Grok, or another AI tool). Your job is to:

1. **Read the feedback** provided by the user
2. **Filter through channel DNA** using the evaluation framework
3. **Present critical analysis** of what to implement vs. reject
4. **Recommend specific actions** (with rationale)

## Evaluation Framework

### STEP 1: Context Assessment

**Questions to answer:**
- What is the current quality rating? (If 9+/10 or "production-ready" → minimal changes needed)
- What type of content? (Script, metadata, thumbnail, etc.)
- What specific problems does feedback identify? (vs. generic polish)

### STEP 2: Three-Test Filter

**For EACH suggestion, apply:**

**1. Documentary Tone Test**
- Does it maintain scholarly, factual language?
- Does it avoid clickbait, flowery phrases, casual engagement tactics?
- Example rejects: "Sound familiar?", "Drop your thoughts below", "echo of a promise"

**2. Evidence-First Test**
- Does it add evidence, strengthen arguments, improve accuracy?
- Or does it add narrative flourishes, word padding, diluted focus?
- Example rejects: Comparative examples that scatter focus, "broader appeal" suggestions

**3. Efficiency Test**
- Does it make content tighter and improve retention through structure?
- Or does it add words without value, optimize for generic YouTube?
- Example rejects: Engagement questions that don't match brand, extra transitions

**4. Primary Source Transparency Test**
- Does it maintain "show the source on screen" methodology?
- If adding historical claim, does it identify displayable primary source?
- If adding historian citation, does it specify their underlying evidence?
- Does it remove or dilute visual source presentation?
- Example rejects:
  - "Add claim about X" without specifying what document proves it
  - "Simplify by removing source details" (removes evidence transparency)
  - "Just cite the historian" without showing their data/documents
  - "Add stock footage" instead of primary source documents

### STEP 3: Categorize Suggestions

**Structural Fixes (Usually Implement):**
- Runtime too long for channel's retention data
- Section creates data-backed drop-off zone
- Jargon undefined when introduced
- Opening lacks concrete modern hook
- Missing retention triggers at critical timestamps

**Generic Polish (Usually Reject):**
- "Add engagement question at end"
- "Include global parallel to broaden appeal"
- "Make opening smoother with flowery phrase"
- "Vary vocabulary with casual synonyms"
- "Make it more conversational/relatable"

### STEP 4: Channel Values Checklist

**Before recommending ANY implementation, verify:**
- [ ] Maintains documentary tone (not clickbait/casual)
- [ ] Evidence-based (adds facts, not flourishes)
- [ ] Stays tight (doesn't pad unnecessarily)
- [ ] Academic authority (not entertainment tactics)
- [ ] Matches brand ("both extremes wrong", primary sources)
- [ ] Preserves "show sources on screen" methodology (displayable evidence)

## Output Format

Provide analysis in this structure:

```markdown
## Feedback Source
[VidIQ / Grok / Other tool]

## Overall Assessment
- Current quality: [X/10, production status]
- Feedback type: [Structural fixes / Generic polish / Mixed]
- Recommendation: [Implement all / Implement selectively / Reject most]

## Suggestion-by-Suggestion Analysis

### 1. [Suggestion name]
**What it suggests:** [Brief description]
**Documentary Tone Test:** ✅ PASS / ❌ FAIL [reason]
**Evidence-First Test:** ✅ PASS / ❌ FAIL [reason]
**Efficiency Test:** ✅ PASS / ❌ FAIL [reason]
**Primary Source Transparency Test:** ✅ PASS / ❌ FAIL [reason]
**Recommendation:** IMPLEMENT / REJECT [rationale]

### 2. [Next suggestion]
[Same structure]

## Final Recommendations

**Implement (with rationale):**
1. [Suggestion] - [Why it aligns with channel values]
2. [Suggestion] - [Why it improves content]

**Reject (with rationale):**
1. [Suggestion] - [Why it violates channel DNA]
2. [Suggestion] - [Why it's generic optimization]

## Summary
[1-2 sentences on overall approach: implement X structural fixes, reject Y generic polish suggestions]
```

## Important Notes

- **9/10 Rule:** If content rated 9+/10 or "production-ready", assume minimal changes needed
- **When unsure:** Recommend presenting options to user rather than auto-implementing
- **Channel priority:** Documentary rigor > viral optimization
- **Evidence:** Always prioritize what adds facts/sources over what adds engagement

## Example Red Flags to Auto-Reject

❌ "Sound familiar? That's the echo of..."
❌ "Drop your thoughts below"
❌ "Broaden appeal with [comparative example]"
❌ "Add teaser question for engagement"
❌ "Make more conversational/relatable"

These violate channel's documentary tone and academic authority brand.
