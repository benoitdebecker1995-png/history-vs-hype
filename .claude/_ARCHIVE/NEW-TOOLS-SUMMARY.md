# New Tools Summary - 2025-11-30

Based on your preferences, I've created a complete suite of tools to improve your workflow. Here's what's new and how to use it.

---

## 1. Comment Response Workflow - `/respond-to-comment`

**What it does:**
- Classifies comments (legitimate correction, nationalist argument, troll, genuine question)
- Reads your video script to see what was actually said
- Checks existing research before doing new searches
- Saves new research to avoid repeating work
- Drafts professional responses in your voice

**How to use:**
```
You: /respond-to-comment

I provide the comment text and tell you which video it's from.

The tool will:
1. Read the script
2. Check existing research
3. Verify the commenter's claims
4. Save research to research/[Topic]-Comment-Response-Research.md
5. Draft a response for your approval
```

**Example from today:**
- You gave me the Belize-Guatemala comment
- I read the script, checked research, did targeted verification
- Saved findings to `research/Belize-Guatemala-Comment-Response-Research.md`
- Drafted response acknowledging errors (Guatemala claims 53%, not all; recognized Belize in 1991)

**File:** `.claude/commands/respond-to-comment.md`

---

## 2. Post-Publication Corrections - `/publish-correction`

**What it does:**
- Documents errors in a corrections log
- Generates pinned comment
- Updates video description
- Creates reusable response template
- Identifies what fact-check would have caught the error

**How to use:**
```
You: /publish-correction

I tell you:
- Which video has the error
- What was stated incorrectly
- What is correct
- How it was discovered

The tool creates:
1. Entry in video-projects/_CORRECTIONS-LOG.md
2. Pinned comment draft (< 300 words)
3. Updated description text
4. Response template for similar comments
5. Entry in .claude/FACT-CHECK-IMPROVEMENTS.md
```

**Prevents:**
- Repeating the same error in future videos
- Inconsistent correction messaging
- Losing track of what went wrong and why

**File:** `.claude/commands/publish-correction.md`

---

## 3. Simplification Detection (Built into `/fact-check`)

**What it does:**
Automatically scans scripts for 8 types of oversimplification that cause errors like the ones in your Belize-Guatemala video.

**8 Rules it checks:**
1. **Territorial claims** without boundaries/percentages
2. **Present tense** for past positions
3. **Absolutist language** ("always," "never," "all")
4. **Statistics** without context (date, totals, comparison)
5. **Contested claims** presented as facts
6. **Quotes** without specific attribution (timestamp, document)
7. **Complex events** oversimplified to single cause
8. **Vague timelines** ("for years" instead of "1869-1884")

**Severity levels:**
- 🔴 **CRITICAL** - Will cause viewer confusion or errors (Rules 1, 2, 6)
- 🟡 **IMPORTANT** - Reduces accuracy (Rules 3, 4, 5)
- 🟢 **RECOMMENDED** - Improves clarity (Rules 7, 8)

**Example output:**
```markdown
## 🚨 SIMPLIFICATION FLAGS

### 🔴 CRITICAL - Fix before filming

**Line 23: "Guatemala claims this entire country"**
- Rule violated: Territorial Simplification (Rule 1)
- Fix: "Guatemala claims territory from Sibun River to Sarstoon River (53% of Belize) plus all offshore cayes"

**Line 142: "Guatemala refuses to recognize it"**
- Rule violated: Temporal Inaccuracy (Rule 2)
- Fix: "Guatemala refused to recognize Belize from 1981 until September 1991"
```

**This would have caught both errors in your Belize video.**

**Files:**
- `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` (the rules)
- `.claude/commands/fact-check.md` (updated to use rules)

---

## 4. Verified Claims Database - `VERIFIED-CLAIMS-DATABASE.md`

**What it does:**
Stores fact-checked claims for reuse across videos. Avoids re-researching the same facts.

**Structure:**
```markdown
### [Claim Statement]
**Verified:** 2025-11-30
**Used in:** Belize vs Guatemala
**Tier:** 1 (Primary sources)
**Status:** ✅ Current

**Claim:** Guatemala claims the territory from Sibun River to Sarstoon River...

**Sources:**
1. OAS Timeline - [URL]
2. MIT Cascon Case - [URL]

**Notes:** This is Guatemala's ICJ position, not validation of claim.
```

**Organized by topic clusters:**
- Belize-Guatemala Territorial Dispute
- [Future topics as you create videos]

**Tracks:**
- Research gaps (things you tried to verify but couldn't)
- Outdated claims (need updating after X years)
- Usage statistics (claims reused across videos)

**Integration:**
- `/script` checks database before researching
- `/fact-check` adds new verified claims
- `/respond-to-comment` checks database before searching

**File:** `.claude/VERIFIED-CLAIMS-DATABASE.md`

**Already populated with:**
- Guatemala's territorial claim (53%, Sibun to Sarstoon)
- Guatemala recognition of Belize (September 1991)
- Atlantic Highway to Puerto Barrios (1950s)
- Islands/cayes dispute (separate ICJ case)

---

## 5. Save Insightful Comments - `/save-comment`

**What it does:**
Saves valuable YouTube comments for future reference instead of losing them.

**Categories:**
- **Research leads** - Commenter suggests sources, books, experts
- **Video ideas** - Topic suggestions from viewers
- **Viewer insights** - What resonated, what confused people
- **Expert corrections** - From academics, locals, specialists

**How to use:**
```
You: /save-comment

I ask which category, then save to:
channel-data/saved-comments/[category]-comments.md
```

**Creates cross-references:**
- Research lead → Add to research/[topic]-sources-to-investigate.md
- Video idea → Add to topics-list.md
- Expert correction → Link to _CORRECTIONS-LOG.md
- Viewer insight → Add to channel-data/audience-insights.md

**Example entry:**
```markdown
## Belize vs Guatemala - Juan Rodriguez - 2025-11-30

**Comment:**
> Check out Alberto Herrarte González's "La Cuestión de Belice" (2000).
> It's the definitive Guatemalan legal scholarship, cited in ICJ submissions.

**Why saved:**
Primary source from knowledgeable viewer. High credibility.

**Potential use:**
Future video on Guatemala's legal arguments

**Follow-up action:**
- [ ] Check university library access
- [ ] Add to NOTEBOOKLM-RESEARCH-PLAN.md
```

**File:** `.claude/commands/save-comment.md`

---

## 6. VidIQ Channel DNA Filter - Auto-filtering

**What it does:**
Automatically filters VidIQ suggestions through your documentary tone requirements.

**AUTO-REJECT (no review needed):**
❌ Clickbait language ("You won't BELIEVE," "SHOCKING")
❌ All-caps emphasis (except acronyms)
❌ Excessive punctuation (!!!, ???, ...)
❌ Listicles ("Top 10," "5 Reasons")
❌ Shocked face thumbnails
❌ Red circles/arrows on thumbnails

**REVIEW-REQUIRED (presents with recommendation):**
⚠️ Keyword pivoting (show data, recommend if factually accurate)
⚠️ Simplified titles (show both versions, assess misleading risk)
⚠️ Thumbnail style (documentary vs. optimized)

**AUTO-ACCEPT (shows you but approves):**
✅ SEO keyword optimization
✅ Technical improvements (chapters, tags)
✅ Mobile optimization

**Integration:**
When you run `/youtube-metadata` and provide VidIQ data:
1. Tool reads VIDIQ-CHANNEL-DNA-FILTER.md
2. Applies filtering rules automatically
3. Shows you: ✅ Accepted / ⚠️ Review / ❌ Rejected
4. Generates metadata using accepted suggestions

**Performance tracking:**
After each video, update `channel-data/vidiq-performance-tracking.md`:
- Which VidIQ suggestions were used
- Results (CTR, retention, views)
- Verdict: Did VidIQ help or hurt?
- Pattern identification over time

**File:** `.claude/VIDIQ-CHANNEL-DNA-FILTER.md`

---

## How These Tools Work Together

**Typical workflow:**

### Before Filming
1. **Script writing** → Checks VERIFIED-CLAIMS-DATABASE.md for existing research
2. **Fact-checking** → Runs simplification detection + source verification
3. **Approval** → All 🔴 CRITICAL flags must be resolved before filming

### After Publishing
4. **Comment engagement** → `/respond-to-comment` for detailed responses
5. **Error discovery** → `/publish-correction` to document and fix
6. **Insight capture** → `/save-comment` for valuable feedback
7. **Database update** → Add verified claims from comment research

### Continuous Improvement
8. **Performance tracking** → Update VidIQ tracking after 30 days
9. **Pattern analysis** → Review corrections log quarterly
10. **System refinement** → Update auto-reject rules based on data

---

## Testing the New Tools

**Want to test them? Here's how:**

### Test `/respond-to-comment`
```
Use the Belize-Guatemala comment we just worked on.
You'll see it:
1. Read the script
2. Find existing research
3. Do targeted verification
4. Save new research
5. Draft response
```

### Test `/publish-correction`
```
Use the two Belize-Guatemala errors:
1. "Claims entire country" → Should be "53%"
2. "Refuses to recognize" → Should be "recognized in 1991"

See how it creates log, pinned comment, response template, improvement entry.
```

### Test `/fact-check` with simplification detection
```
Give it a script with these test phrases:
- "China claims the entire South China Sea"
- "Russia refuses to withdraw"
- "The war lasted years"

Watch it flag simplifications with specific fixes.
```

### Test `/save-comment`
```
Save a valuable comment (research lead, video idea, etc.)
See how it cross-references and creates follow-up actions.
```

---

## Files Created/Updated

**New commands:**
- `.claude/commands/respond-to-comment.md`
- `.claude/commands/publish-correction.md`
- `.claude/commands/save-comment.md`

**New reference files:**
- `.claude/FACT-CHECK-SIMPLIFICATION-RULES.md` (8 rules with examples)
- `.claude/VERIFIED-CLAIMS-DATABASE.md` (with Belize-Guatemala claims)
- `.claude/VIDIQ-CHANNEL-DNA-FILTER.md` (auto-filtering rules)

**Updated commands:**
- `.claude/commands/fact-check.md` (now runs simplification detection)

**Future files (created on first use):**
- `video-projects/_CORRECTIONS-LOG.md`
- `.claude/FACT-CHECK-IMPROVEMENTS.md`
- `channel-data/saved-comments/[category]-comments.md`
- `channel-data/vidiq-performance-tracking.md`

---

## Quick Reference

**Comment needs response:** `/respond-to-comment`
**Found an error:** `/publish-correction`
**Valuable comment:** `/save-comment`
**Fact-checking script:** `/fact-check` (now includes simplification detection)
**VidIQ suggestions:** Auto-filtered in `/youtube-metadata`

---

## Philosophy Behind These Tools

**From today's session, I learned:**

1. **Errors happen from oversimplification** - Rules 1 & 2 would have caught both Belize-Guatemala errors
2. **Research gets repeated** - Database prevents token waste and ensures consistency
3. **Comments have value** - Legitimate corrections improve future videos
4. **VidIQ conflicts with brand** - Filtering maintains documentary tone
5. **Systems > memory** - Document corrections to prevent repetition

**Your principle:**
"I'd rather cut a claim than oversimplify it. Complexity is the channel's value proposition."

**These tools enforce that principle systematically.**

---

## Next Steps

1. **Test the tools** with existing content to validate they work as expected
2. **Adjust rules** based on your preferences (e.g., add Rule 9 if you identify new pattern)
3. **Build the database** as you verify claims in future videos
4. **Track performance** to see which VidIQ suggestions actually help

**Questions or adjustments needed?** Let me know and I'll refine the tools.
