# VidIQ Channel DNA Filter Rules

This file contains automatic filtering rules for VidIQ suggestions to maintain History vs Hype's documentary tone and editorial standards.

**Purpose:**
- Reject clickbait suggestions that violate channel DNA
- Automate filtering to save time
- Maintain consistency across videos
- Track what VidIQ suggestions work vs. hurt retention

---

## AUTO-REJECT Rules

**These suggestions are automatically rejected without user review:**

### Title Suggestions - AUTO-REJECT if contains:

❌ **Emotional manipulation:**
- "You won't BELIEVE..."
- "SHOCKING..."
- "This will BLOW your mind..."
- "What THEY don't want you to know..."
- "INSANE..."
- "MIND-BLOWING..."

❌ **All-caps words** (except acronyms like ICJ, UN, CIA):
- "The TRUTH About..."
- "DESTROYED by Facts..."
- Any word in all-caps for emphasis

❌ **Excessive punctuation:**
- Multiple exclamation marks (!!!)
- Multiple question marks (???)
- Ellipses for drama (...)

❌ **Vague pronouns without antecedents:**
- "Why THEY Lied About..."
- "What IT Really Means..."
- "How THIS Changed History..." (when 'this' isn't defined)

❌ **Listicle format:**
- "Top 10..."
- "5 Reasons Why..."
- "3 Things You Didn't Know..."

❌ **False accusations without evidence:**
- "X LIED About..."
- "The Truth They HID..."
- "EXPOSED: ..."

### Thumbnail Suggestions - AUTO-REJECT if contains:

❌ **Shocked face expressions:**
- Open mouth
- Wide eyes with hands on face
- Exaggerated surprise

❌ **Red circles/arrows pointing at nothing specific:**
- Generic red arrows
- Circles highlighting vague areas

❌ **Clickbait text overlays:**
- "SHOCKING"
- "EXPOSED"
- "LIED"
- "ILLEGAL"

❌ **Misleading visuals:**
- Suggesting content not in video
- Fabricated confrontations
- Fake quotes

### Tag Suggestions - AUTO-REJECT if:

❌ **Misleading/controversy-baiting:**
- Tags for topics not covered
- Partisan political tags unrelated to content
- Tags designed to exploit algorithm without relevance

---

## REVIEW-REQUIRED Rules

**These suggestions need user judgment—present with recommendation:**

### Title Suggestions - FLAG FOR REVIEW:

⚠️ **Keyword pivoting:**
- VidIQ suggests different primary keyword
- **Present:** Original vs. VidIQ keyword, search volume comparison
- **Recommend:** Use high-volume keywords if factually accurate

⚠️ **Simplified complexity:**
- VidIQ simplifies nuanced title
- **Present:** Both versions side-by-side
- **Recommend:** Use simplified if doesn't create misleading impression

⚠️ **Length optimization:**
- VidIQ shortens/lengthens title
- **Present:** Character count, mobile preview
- **Recommend:** Follow mobile-first principle (60-70 chars)

### Thumbnail Suggestions - FLAG FOR REVIEW:

⚠️ **Documentary vs. YouTube-native style:**
- VidIQ suggests higher contrast/bolder text
- **Present:** Professional vs. optimized version
- **Recommend:** A/B test if possible, default to documentary style

⚠️ **Face vs. no-face:**
- VidIQ has face CTR data
- **Present:** Data on face-in-thumbnail performance
- **Recommend:** Based on data, not assumptions

⚠️ **Text amount:**
- VidIQ suggests more/less text
- **Present:** Readability on mobile
- **Recommend:** 2-4 words max, legible on phone screen

---

## AUTO-ACCEPT Rules

**These suggestions are automatically accepted (still show to user):**

✅ **SEO keyword optimization:**
- Suggestions to frontload keywords in description
- Natural keyword integration recommendations
- Tag additions that are factually relevant

✅ **Technical improvements:**
- Chapter/timestamp suggestions
- Description structure optimization
- Tag organization for discovery

✅ **Mobile optimization:**
- Character count warnings (title too long)
- Thumbnail readability on small screens
- Description hook frontloading

---

## Integration with `/youtube-metadata` Command

**When user provides VidIQ data:**

1. **Parse VidIQ suggestions** (title, thumbnail, tags, description)

2. **Run through filter rules:**
   ```
   For each suggestion:
   - Check AUTO-REJECT rules → Discard with reason
   - Check REVIEW-REQUIRED rules → Present with recommendation
   - Check AUTO-ACCEPT rules → Include in metadata
   ```

3. **Present filtered results:**
   ```markdown
   ## VidIQ Suggestions - Filtered

   ### ✅ Accepted (Auto)
   - [Suggestion] - Reason

   ### ⚠️ Recommended for Review
   - [Suggestion] - Why flagged - Recommendation

   ### ❌ Rejected (Channel DNA Conflict)
   - [Suggestion] - Rule violated
   ```

4. **Generate final metadata** incorporating accepted suggestions

---

## Tracking What Works

**File location:** `channel-data/vidiq-performance-tracking.md`

**Format:**
```markdown
## [Video Title] - [Date]

**VidIQ Suggestions Used:**
- Title: [Original] → [VidIQ version] → [Final used]
- Thumbnail: [Documentary style / VidIQ optimized / Hybrid]
- Primary keyword: [Original] → [VidIQ suggestion]

**Results:**
- CTR: [X%]
- AVD: [X:XX]
- Retention: [X%]
- Views (30 days): [X]

**Verdict:**
- ✅ VidIQ suggestions helped (higher CTR/retention than channel avg)
- ⚠️ Mixed results (some worked, some didn't)
- ❌ VidIQ suggestions hurt (lower performance than channel avg)

**Lessons:**
[What worked, what didn't, why]
```

**Update after every video to identify patterns:**
- Do VidIQ keyword pivots improve CTR?
- Does bolder thumbnail text hurt/help retention?
- Which accepted suggestions consistently work?

---

## Example: VidIQ Filtering in Action

**VidIQ suggests:**
1. Title: "The SHOCKING Truth About Belize That Guatemala Doesn't Want You To Know!"
2. Thumbnail: Red arrow pointing at map with "ILLEGAL" text
3. Keyword: Pivot from "Belize territorial dispute" to "Guatemala controversy"

**After filtering:**

**❌ REJECTED - Title:**
- Rule violated: Emotional manipulation ("SHOCKING"), vague pronouns ("That"), all-caps emphasis
- Reason: Clickbait format conflicts with documentary tone

**❌ REJECTED - Thumbnail:**
- Rule violated: Red arrow, misleading text overlay
- Reason: Creates false impression of scandal/illegality

**⚠️ REVIEW REQUIRED - Keyword:**
- VidIQ data: "Guatemala controversy" has 8,900 monthly searches vs. "Belize territorial dispute" with 210
- Recommendation: Pivot to "Guatemala Belize Border Dispute" (4,200 searches) - higher volume than current, factually accurate, no sensationalism
- User decision needed: Balance SEO vs. precise terminology

---

## Channel DNA Core Principles

**When in doubt, apply these tests:**

1. **Would this work on a PBS documentary?**
   - If no → Reject

2. **Does this accurately represent the content?**
   - If no → Reject

3. **Would this mislead a viewer about what they're watching?**
   - If yes → Reject

4. **Does this prioritize clicks over credibility?**
   - If yes → Reject

**The user's philosophy:**
"I'd rather get fewer clicks from the right audience than more clicks from people expecting something I don't deliver. Retention and trust matter more than CTR."

---

## Maintenance

**After each video:**
- Add to performance tracking file
- Note which VidIQ suggestions were used
- Track results after 30 days

**Quarterly review:**
- Analyze performance patterns
- Update AUTO-ACCEPT/REJECT rules based on data
- Adjust recommendations based on what works

---

## Usage in Commands

### `/youtube-metadata` command:
```
If user provides VidIQ data:
1. Read VIDIQ-CHANNEL-DNA-FILTER.md
2. Apply filtering rules
3. Present filtered suggestions with reasons
4. Generate metadata using accepted suggestions
```

### `/evaluate-feedback` command:
```
When evaluating VidIQ or other optimization feedback:
1. Check against channel DNA filter rules
2. Recommend acceptance/rejection with reasoning
3. Save decision to performance tracking
```
