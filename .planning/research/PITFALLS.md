# Domain Pitfalls: Script Quality, Discovery/SEO, and NotebookLM Workflow

**Domain:** YouTube content production with AI-assisted scriptwriting, SEO optimization, and research workflows
**Researched:** 2026-01-27
**Context:** Solo creator adding script quality, discovery, and NotebookLM features to existing workspace

---

## Executive Summary

When adding script quality improvements, discovery/SEO optimization, and NotebookLM workflow automation to an existing content production system, the primary risks are: **voice dilution** (AI makes scripts generic), **over-optimization** (chasing metrics at expense of channel DNA), **manual workarounds that don't scale** (NotebookLM file limits), and **scope creep** (new features breaking existing workflows). The creator already has 543 lines of documented voice patterns in STYLE-GUIDE.md - the challenge is enhancing quality WITHOUT losing what already works.

**Critical insight:** 52% of projects experience scope creep when adding features to existing systems. The user's repetition analysis shows scripts need LESS intervention (trim 10% from first drafts), not MORE prompting complexity.

---

## Critical Pitfalls (Cause Rewrites or Abandon Features)

### Pitfall 1: The Voice Dilution Trap

**What goes wrong:**
AI tools improve "quality" metrics (grammar, flow, clarity) while destroying creator voice. Scripts become indistinguishable from generic YouTube educational content. The 543-line STYLE-GUIDE.md becomes useless because AI "corrects" intentional patterns.

**Why it happens:**
- AI writing tools are trained on "good writing" from billions of sources, creating a gravitational pull toward median/generic patterns
- [Common AI writing mistakes](https://www.yomu.ai/resources/common-ai-writing-mistakes-and-how-to-avoid-them) include overly repetitive language, obvious keyword stuffing, and bland, abstract text
- AI cannot access emotional experience or express vulnerability authentically - [what matters most must be purely human](https://rivereditor.com/guides/how-to-use-ai-writing-tools-without-losing-voice-2026)
- Prompts like "improve clarity" or "make more engaging" flatten unique voice patterns

**Real example from this channel:**
- STYLE-GUIDE.md mandates: "It's not" (contraction), "On June 16th, 2014" (ordinal dates), 2-4 uses of "here's" per script
- Generic AI correction: "It is not" (formal), "June 16, 2014" (AP style), eliminates "here's" as "repetitive filler"
- Result: Script sounds like every other documentary, loses conversational authority that drives 42.6% retention

**Consequences:**
- Retention drops (viewers subscribed for "intellectual competence" delivered in specific voice)
- Creator spends MORE time reverting AI changes than original writing took
- Audience notices quality change: "This doesn't sound like you anymore"
- Competitive advantage (Kraut + Alex O'Connor voice fusion) lost

**Prevention:**
1. **Use AI as analyzer, not writer** - Ask it to flag unclear sections, then YOU fix them your way ([recommended by voice preservation experts](https://www.thetransmitter.org/from-bench-to-bot/keeping-it-personal-how-to-preserve-your-voice-when-using-ai/))
2. **Custom instruction files** - Feed STYLE-GUIDE.md to AI with explicit "preserve these patterns" prompts
3. **Targeted requests only** - "Scan for repetitive phrases" NOT "improve this section"
4. **Voice-first editing protocol:**
   ```
   Before accepting ANY AI suggestion:
   - Read aloud - does it sound like YOU?
   - Check against STYLE-GUIDE.md - violates documented patterns?
   - If yes to either → reject or heavily modify
   ```
5. **Vulnerable sections = human only** - Opening hooks, conclusions, steelmanning moments must be creator-written

**Detection:**
Early warning signs AI is diluting voice:
- Scripts pass quality checks but "feel off" when reading
- Contractions becoming formal ("it is" replacing "it's")
- Signature phrases disappearing ("The reality is...", "If we're being fair...")
- Transitions becoming formal ("However," "Nevertheless" instead of "But," "So")
- User finds themselves saying "this doesn't sound like me" repeatedly

---

### Pitfall 2: SEO Over-Optimization Death Spiral

**What goes wrong:**
Chasing keywords and CTR metrics transforms documentary channel into clickbait. VidIQ suggests "SHOCKING Truth About X" titles - creator accepts because "data says it works" - audience who subscribed for intellectual rigor leaves.

**Why it happens:**
- [YouTube SEO tools optimize for clicks](https://www.keywordtooldominator.com/youtube-seo), not audience fit
- Keyword stuffing titles like "YouTube SEO 2026 Tips Tricks Free Tools Optimization Ranking" are instant red flags but tools recommend them
- [Over-optimization prioritizes clicks over credibility](https://seosherpa.com/youtube-seo/) - Algorithm weighs viewer satisfaction equally with keywords
- Creator sees competitors getting higher CTR with clickbait, feels pressure to compete

**Real example from this channel:**
- VidIQ recommended: "The SHOCKING Truth About Belize That Guatemala Doesn't Want You To Know!" (emotional manipulation, all-caps, vague pronouns)
- Channel DNA requires: "Belize's 1859 Treaty: Why Guatemala's ICJ Case Will Fail" (documentary tone, specific, evidence-based)
- User correctly rejected via VIDIQ-CHANNEL-DNA-FILTER.md: "Would this work on PBS documentary? No → Reject"

**Consequences:**
- High CTR, terrible retention (clickbait attracts wrong audience)
- Subscriber quality drops (people expecting drama, getting academic analysis)
- Algorithm deprioritizes content (retention matters more than CTR)
- Creator burnout from constantly fighting tool suggestions
- Channel DNA erosion over time ("just this once" becomes pattern)

**Prevention:**
1. **Auto-reject rules BEFORE seeing suggestions** - Implement VIDIQ-CHANNEL-DNA-FILTER.md's AUTO-REJECT list:
   - Emotional manipulation: "You won't BELIEVE...", "SHOCKING..."
   - All-caps emphasis words (except acronyms)
   - Vague pronouns: "Why THEY Lied..."
   - Listicle formats: "Top 10...", "5 Reasons..."
2. **Channel DNA litmus tests:**
   ```
   For every SEO suggestion, ask:
   - Would this work on PBS documentary? (If no → reject)
   - Does this accurately represent content? (If no → reject)
   - Would this mislead viewers? (If yes → reject)
   - Does this prioritize clicks over credibility? (If yes → reject)
   ```
3. **Keyword integration without corruption:**
   - One clear primary keyword + one benefit
   - NOT: "YouTube SEO 2026 Tips Tricks Free"
   - YES: "YouTube SEO 2026: Rank #1 Without Paying for Ads"
4. **Performance tracking against channel values:**
   - Track: CTR, retention, subscriber quality, watch time
   - If high CTR + low retention → over-optimized, roll back
   - Channel philosophy: "Fewer clicks from right audience > more clicks from wrong audience"
5. **Separate discovery from integrity:**
   - Keywords in description/tags (technical SEO) = optimize freely
   - Title/thumbnail (editorial) = channel DNA rules apply strictly

**Detection:**
You've over-optimized when:
- Comments section fills with "this isn't what I expected"
- Retention dropping despite higher CTR
- Subscribers increasingly disengaged (views per subscriber declining)
- You feel uncomfortable with own titles
- Core audience comments: "What happened to your channel?"

---

### Pitfall 3: NotebookLM Manual Workarounds That Collapse

**What goes wrong:**
Creator develops workarounds for NotebookLM's 50-source limit (merging PDFs, splitting across notebooks). Works for one video. Collapses at scale when managing 5+ videos with 20+ sources each. Citations break, file organization destroyed, hours wasted on manual file manipulation.

**Why it happens:**
- NotebookLM Enterprise API exists but NOT available to consumer users ([no official public API](https://autocontentapi.com/blog/does-notebooklm-have-an-api))
- [Workarounds have serious drawbacks](https://elephas.app/blog/how-to-upload-more-files-notebooklm): consume significant time, reduce citation accuracy, destroy document organization
- File merging destroys original structure while splitting across notebooks becomes unmanageable for larger projects
- [Manual processes requiring file conversion with extra software](https://medium.com/@ferreradaniel/how-to-use-notebooklm-better-than-99-of-people-deep-research-workflow-guide-4e54199c9f82) don't scale
- Creator invests weeks perfecting workaround, then can't maintain it across multiple projects

**Real example scenarios:**
- Video 1: 15 sources, manually merge to fit limit, works fine
- Video 2-4: 45+ sources total, now managing merged files across 3 notebooks
- Need to verify cross-video claim: Which merged PDF has that source? Which notebook?
- Citation says "Source 3, page 47" but Source 3 is actually pages 120-180 of merged file
- 2 hours of research time wasted hunting for one citation

**Consequences:**
- [Invalid citations where source references become incorrect](https://medium.com/@ferreradaniel/how-to-use-notebooklm-better-than-99-of-people-deep-research-workflow-guide-4e54199c9f82)
- Loss of file organization where original structure and document names disappear
- Topic confusion from mixed subjects in merged files
- Research quality degradation (can't find sources to verify claims)
- Workaround maintenance becomes full-time job
- Eventually abandon NotebookLM entirely, lose benefits

**Prevention:**
1. **Accept the constraint, design around it:**
   - 10-20 sources per video (focused, not exhaustive) per NOTEBOOKLM-SOURCE-STANDARDS.md
   - Prioritize Tier 1 (primary) and Tier 2 (academic) sources only
   - One notebook per video, strict 50-source ceiling
2. **External citation management:**
   - Maintain VERIFIED-RESEARCH.md as single source of truth
   - Record page numbers FROM NotebookLM citations immediately
   - Don't rely on NotebookLM for long-term citation storage
3. **Source quality over quantity:**
   - 15 excellent sources &gt; 50 mediocre sources
   - Use NotebookLM Study Guides to extract maximum value from fewer sources
   - Academic monographs (500+ pages) COUNT AS ONE but contain multiple chapters worth of material
4. **No heroic workarounds:**
   - If you're considering PDF merging → stop, reconsider source selection instead
   - If you need 3rd-party scripts → you're fighting the tool, not using it
   - Manual processes requiring &gt;30 min setup per video won't survive at scale
5. **Alternative tools for different needs:**
   - NotebookLM: Deep synthesis of 10-20 focused sources
   - Zotero/Mendeley: Citation management for 100+ sources
   - Don't force NotebookLM to be citation database

**Detection:**
Workarounds are failing when:
- Spending &gt;20% of research time on file management vs. actual research
- Citations require "detective work" to trace back to original sources
- Anxiety about losing track of which notebook has which merged file
- Considering building custom scripts to manage NotebookLM organization
- Research quality declining because verification is "too hard"

---

### Pitfall 4: Prompt Over-Engineering Paralysis

**What goes wrong:**
Creator writes 2,000-token mega-prompts trying to capture every nuance of STYLE-GUIDE.md. AI output is worse than simple prompts because model gets lost in complexity. [Poorly optimized prompts burn capital across millions of API calls when 500 tokens would suffice](https://bigblue.academy/en/the-death-of-prompt-engineering-and-its-ruthless-resurrection-navigating-ai-orchestration-in-2026-and-beyond).

**Why it happens:**
- STYLE-GUIDE.md is 543 lines - creator tries to cram entire guide into every prompt
- [Making prompts overly complex](https://treyworks.com/common-prompt-engineering-mistakes-to-avoid/) by trying to cover too many topics at once
- Mistaken belief: more detailed prompt = better output
- Each script revision requires tweaking 2,000-token prompt, becomes unmaintainable

**Real example pattern:**
```
BAD MEGA-PROMPT (2,000 tokens):
"You are a YouTube script editor for History vs Hype channel.
Voice profile: Calm Prosecutor, emotionally low, intellectually high.
Style patterns: Use contractions (it's not it is), ordinal dates
(On June 16th not June 16), define terms immediately (estoppel -
a legal rule that...), limit here's to 2-4 uses, use But/So not
However/Nevertheless, fragments only for emphasis not information,
steelman opposing arguments, cite sources with author names,
use Kraut causal chains (consequently, thereby), Alex O'Connor
intellectual honesty (That's fair. But...), Shaun document-first...
[continues for 2,000 tokens]

Now improve this script section..."

Result: AI overwhelmed, defaults to generic patterns,
ignores most instructions.
```

**Consequences:**
- [Overloading prompts should be fixed by breaking tasks into simpler, focused steps](https://www.mygreatlearning.com/blog/prompt-engineering-beginners-mistakes/)
- AI performance WORSE with complex prompts (model attention diluted)
- Creator can't maintain prompts (each script needs prompt debugging)
- Expensive at scale (2,000 tokens × 50 script sections × $X per token)
- False precision: most of prompt ignored anyway

**Prevention:**
1. **Task-specific micro-prompts:**
   ```
   GOOD MICRO-PROMPT (150 tokens):
   "Scan this script section for:
   1. Repetitive phrases (same phrase 3+ times)
   2. Unclear transitions between topics
   3. Paragraphs that could be cut entirely

   List issues only, don't rewrite."

   Then: Creator fixes issues in their own voice.
   ```
2. **Layered approach:**
   - Layer 1: Detection ("Find repetitions")
   - Layer 2: Analysis ("Why is this repetitive?")
   - Layer 3: Creator decides fix
   - NOT: One mega-prompt trying to do everything
3. **Reference files, don't embed:**
   - Upload STYLE-GUIDE.md as reference document
   - Prompt: "Following style guide, identify violations"
   - NOT: Copy entire style guide into every prompt
4. **Ruthlessly eliminate unnecessary verbosity:**
   - [2026 sophisticated practitioners treat prompt optimization as cost-reduction](https://bigblue.academy/en/the-death-of-prompt-engineering-and-its-ruthless-resurrection-navigating-ai-orchestration-in-2026-and-beyond)
   - Monitor inference costs
   - Target: 500 tokens or less per prompt
5. **Specific over comprehensive:**
   - "Flag uses of 'However' and 'Nevertheless'" &gt; "Apply all transition rules from style guide"

**Detection:**
Prompts are over-engineered when:
- Takes longer to write prompt than to do task manually
- AI outputs ignore most of your instructions
- You're maintaining a "prompt library" with versions
- Token costs becoming significant
- Each new script requires prompt debugging session

---

## Moderate Pitfalls (Cause Delays or Technical Debt)

### Pitfall 5: Breaking Existing Workflows with "Improvements"

**What goes wrong:**
New script quality tool requires reformatting all scripts to JSON schema. Breaks existing `/script` command. Creator spends week on migration, realizes old workflow was actually better for their use case.

**Why it happens:**
- [52% of projects experience scope creep](https://projectmanagementacademy.net/resources/blog/pmp-scope-creep/) when adding features
- [Changing requirements and poor definition](https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep) cause additions without proper evaluation
- New tool solves problem that didn't exist, creates problems that did
- Sunk cost fallacy: invested time in setup, feel obligated to use it

**Real example from user context:**
- Current workflow: Write in Markdown, read aloud, manual fact-check against VERIFIED-RESEARCH.md
- "Improvement" idea: Automated fact-checking tool that cross-references database
- Reality: Tool requires structured data format user doesn't have, manual conversion takes longer than original fact-check process

**Prevention:**
1. **Minimum viable addition:**
   - Add ONE feature at a time
   - Test with ONE video before rolling out
   - If it doesn't save &gt;20% time or improve quality measurably → don't adopt
2. **Backwards compatibility requirement:**
   - New tool must work with existing files/format
   - If requires migration → probably wrong tool
3. **Kill switch planning:**
   - Before adopting: document how to revert
   - Test reversion process
   - Keep old workflow available for 3-5 videos before deprecating
4. **Actual problem definition:**
   ```
   Before adding feature, write:
   - Current problem: [specific issue]
   - Success criteria: [measurable improvement]
   - If success criteria not met after 3 videos → kill feature
   ```

**Detection:**
- Spending more time configuring tools than creating content
- Workarounds accumulating to make new tool compatible with old process
- Nostalgia for "simpler times" before improvement
- Decreased output (fewer videos completed since adding feature)

---

### Pitfall 6: The Repetition Over-Correction Trap

**What goes wrong:**
Creator reads REPETITION-ANALYSIS showing "deportation records, statistical reports" used 4 times. Implements rule: "Never repeat ANY phrase more than twice." Scripts become thesaurus-driven gibberish where every mention uses different synonym, confusing viewers.

**Why it happens:**
- Misunderstanding the problem: [AI repetition is about identical phrasing](https://the7eagles.com/common-mistakes-of-ai-writing/), not concept reinforcement
- Over-applying feedback (fix said "vary language," interpreted as "never repeat ever")
- Losing sight of goal: clarity for viewers, not variety for variety's sake

**Real example:**
```
ORIGINAL (repetitive):
"Deportation records showed X. Statistical reports confirmed Y.
The deportation records proved Z. These statistical reports..."

OVER-CORRECTED (confusing):
"Transportation logs showed X. Census data confirmed Y.
The removal documentation proved Z. These numeric analyses..."

Result: Viewer thinks these are different sources,
gets confused about what evidence exists.
```

**Better correction:**
```
"Deportation records and statistical reports showed X.
The Nazi paperwork confirmed Y. [Show document on screen]
As you can see, these numbers prove Z."

Result: Varies phrasing while maintaining clarity.
```

**Prevention:**
1. **Clarity > Variety:**
   - Technical terms SHOULD be consistent ("Guardian Council" not "Guardian Council → oversight body → clerical committee")
   - Vary delivery, not terminology
2. **Show, don't say:**
   - If document is on screen, you can repeat its name - visual variety compensates
   - "The Höfle Telegram shows... [cut to document] ...As you can see..." = not repetitive
3. **Concept vs. phrasing:**
   - OK to reference "this constitutional problem" 3 times (concept)
   - NOT OK to say "the constitutional problem that undermines democracy" 3 times (identical phrasing)

---

### Pitfall 7: Discovery Optimization Tunnel Vision

**What goes wrong:**
Creator sees "Belize territorial dispute" has 210 searches, "Guatemala controversy" has 8,900. Pivots entire video to controversy framing. Gets clicks from people expecting scandal, delivers academic border dispute analysis. Retention tanks.

**Why it happens:**
- [Keyword volume data doesn't show intent or audience quality](https://www.keywordtooldominator.com/youtube-seo)
- High-volume keywords often have wrong audience
- SEO tools can't measure channel DNA fit

**Prevention:**
1. **Audience quality over keyword volume:**
   - 210 searches from right audience &gt; 8,900 from wrong audience
   - Track: views per subscriber, not just total views
2. **Middle path keyword pivoting:**
   - ORIGINAL: "Belize territorial dispute" (210 searches, perfect fit)
   - VIDIQ: "Guatemala controversy" (8,900 searches, wrong audience)
   - MIDDLE: "Guatemala Belize border dispute" (4,200 searches, acceptable fit)
3. **Performance tracking by keyword type:**
   - Track retention by which keyword attracted viewer
   - If "controversy" keywords = low retention → avoid regardless of volume

---

## Minor Pitfalls (Cause Annoyance but Fixable)

### Pitfall 8: NotebookLM Source Quality Drift

**What goes wrong:**
Creator starts with academic monographs, gradually adds blog posts and news articles to meet source count targets. Research quality degrades silently.

**Prevention:**
- NOTEBOOKLM-SOURCE-STANDARDS.md enforces academic quality: university presses ONLY
- Budget is UNLIMITED for quality sources - buy what you need
- Better 8 excellent sources than 20 mediocre ones

---

### Pitfall 9: Metadata Template Ossification

**What goes wrong:**
Creator builds perfect metadata template, uses same structure for every video. Discovery suffers because template doesn't adapt to different video types (territorial vs. ideological myth).

**Prevention:**
- Templates are starting points, not rigid formats
- Each video type needs different hook:
  - Territorial: Document + modern stakes
  - Ideological: Myth + who believes it today
  - Fact-check: Claim + evidence reveal

---

### Pitfall 10: Verification Theater

**What goes wrong:**
Creator implements 3-phase verification process (VERIFIED-RESEARCH.md → SCRIPT → FACT-CHECK). Spends 2 hours verifying trivial facts ("France is in Europe"), skips verification of contested claims because "running out of time."

**Prevention:**
- Triage verification effort:
  - HIGH priority: Contested claims, statistics, direct quotes
  - MEDIUM priority: Historical events with multiple interpretations
  - LOW priority: Widely accepted facts
- Verification depth should match claim controversy

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Script Quality Setup | Voice dilution from AI "improvements" | Use AI as analyzer only, creator fixes issues in own voice |
| Discovery/SEO Integration | Over-optimization breaking channel DNA | Implement VIDIQ-CHANNEL-DNA-FILTER.md AUTO-REJECT rules first |
| NotebookLM Workflow | Manual workarounds that don't scale | Accept 50-source limit, design around it with quality over quantity |
| Prompt Engineering | Over-complex mega-prompts | Micro-prompts (150 tokens) for specific tasks only |
| Workflow Integration | Breaking existing working system | Add ONE feature at a time, test with ONE video |
| Repetition Detection | Over-correction creating confusion | Vary phrasing, not terminology; clarity &gt; variety |
| Keyword Research | High-volume wrong-audience keywords | Track retention by keyword source, optimize for fit not volume |
| Source Management | Quality drift toward easier/cheaper sources | Academic quality standards non-negotiable, budget unlimited |
| Template Usage | Rigid templates preventing adaptation | Templates as starting points for each video type |
| Verification Process | Spending time on trivial, skipping critical | Triage by claim controversy level |

---

## Integration Checklist (Before Adding Any Feature)

**Use this checklist BEFORE implementing script quality, SEO, or NotebookLM features:**

### Problem Definition
- [ ] Can state problem in one sentence
- [ ] Problem affects &gt;50% of videos
- [ ] Problem costs &gt;1 hour per video currently
- [ ] Solution would save time OR measurably improve quality

### Solution Validation
- [ ] Solution preserves creator voice (passes STYLE-GUIDE.md compatibility test)
- [ ] Solution respects channel DNA (passes VIDIQ-CHANNEL-DNA-FILTER.md litmus tests)
- [ ] Solution scales (works for 1 video AND 20 videos with similar effort)
- [ ] Solution has kill switch (can revert to old workflow if needed)

### Scope Control
- [ ] Adding ONE feature, not feature bundle
- [ ] Can test with ONE video before rolling out
- [ ] Doesn't require reformatting existing files
- [ ] Doesn't break existing commands/workflows

### Success Criteria
- [ ] Defined measurable improvement target
- [ ] Defined timeline for evaluation (e.g., 3 videos)
- [ ] Defined failure condition (when to abandon feature)

### If ANY checkbox is unchecked → HIGH RISK, reconsider addition.

---

## Sources

### AI Script Writing Pitfalls
- [Common AI Writing Mistakes and How to Avoid Them](https://www.yomu.ai/resources/common-ai-writing-mistakes-and-how-to-avoid-them) - Repetition, awkward flow, generic patterns
- [Common Mistakes of AI Writing](https://the7eagles.com/common-mistakes-of-ai-writing/) - Lack of big-picture context, word-by-word generation issues
- [Weaknesses of AI-Generated Writing](https://www.wordrake.com/resources/weaknesses-of-ai-generated-writing) - Bland, abstract, repetitive patterns

### Creator Voice Preservation
- [How to Use AI Writing Tools Without Losing Your Voice (2026)](https://rivereditor.com/guides/how-to-use-ai-writing-tools-without-losing-voice-2026) - Use AI as analyzer, not writer
- [Keeping it Personal: How to Preserve Your Voice When Using AI](https://www.thetransmitter.org/from-bench-to-bot/keeping-it-personal-how-to-preserve-your-voice-when-using-ai/) - Targeted requests, custom instructions
- [The Authenticity Deficit: Is AI Diluting Your Voice](https://medium.com/@adnanmasood/the-authenticity-deficit-is-ai-diluting-your-voice-54bd53afe01b) - Boundary maintenance

### YouTube SEO Pitfalls
- [Ultimate YouTube SEO Guide (2026)](https://www.keywordtooldominator.com/youtube-seo) - Keyword stuffing remains major problem
- [YouTube SEO: Rank Higher and Grow Your Channel in 2026](https://seosherpa.com/youtube-seo/) - Algorithm weighs satisfaction equally with keywords
- [SEO Mistakes and Common Errors to Avoid in 2026](https://content-whale.com/blog/seo-mistakes-and-common-errors-to-avoid-in-2026/) - Over-optimization dangers

### NotebookLM Workflow Issues
- [How to Upload More Files to NotebookLM? Quick Fixes and Better Alternatives (2026)](https://elephas.app/blog/how-to-upload-more-files-notebooklm) - Workarounds have serious drawbacks
- [How To Use NotebookLM Better Than 99% Of People](https://medium.com/@ferreradaniel/how-to-use-notebooklm-better-than-99-of-people-deep-research-workflow-guide-4e54199c9f82) - Manual process problems
- [Does NotebookLM Have an API?](https://autocontentapi.com/blog/does-notebooklm-have-an-api) - No public API, Enterprise only

### Prompt Engineering
- [Top Prompt Engineering Pitfalls & Mistakes to Avoid in 2026](https://treyworks.com/common-prompt-engineering-mistakes-to-avoid/) - Over-complication issues
- [Death of Prompt Engineering: AI Orchestration in 2026](https://bigblue.academy/en/the-death-of-prompt-engineering-and-its-ruthless-resurrection-navigating-ai-orchestration-in-2026-and-beyond) - Ruthlessly eliminate verbosity
- [5 Prompt Engineering Mistakes Beginners Make](https://www.mygreatlearning.com/blog/prompt-engineering-beginners-mistakes/) - Overloading prompts

### Scope Creep
- [Understanding and Managing Scope Creep In Project Management](https://projectmanagementacademy.net/resources/blog/pmp-scope-creep/) - 52% of projects experience it
- [What Is Scope Creep and How Can I Avoid It?](https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep) - Prevention strategies
- [What is scope creep in project management](https://miro.com/project-management/what-is-scope-creep/) - Common causes

---

*Research complete. Ready for roadmap creation.*
