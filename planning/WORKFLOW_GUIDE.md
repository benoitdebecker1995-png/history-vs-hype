# Complete Video Production Workflow

Your Claude Code environment is now set up with a complete research-to-script pipeline.

## Quick Start

Type `/create-video` and I'll guide you through everything.

## The 5-Stage Workflow

### Stage 1: Find Trending Topics
**Command:** `/find-topic`

**What happens:**
1. I research web trends (border disputes, political claims, historical myths)
2. I evaluate topics against your channel criteria
3. I give you a VidIQ CoachPro prompt to run
4. You paste VidIQ's response back to me
5. I cross-reference and give you top 3 recommendations with viral scores

**Output:** `video-projects/topic-research-[date]/01-trend-research.md`

---

### Stage 2: Deep Preliminary Research
**Command:** `/deep-research [topic]`

**What happens:**
1. I use only free sources (Wikipedia, archives, Google Scholar, news)
2. I extract 5-10 smoking gun primary sources with URLs
3. I identify patterns (3+ interconnected incidents)
4. I research counter-arguments
5. I find modern relevance examples (2024-2025)
6. I give you a YES/MAYBE/NO verdict

**What you get:**
- Complete evidence roadmap
- Source URLs you can access immediately
- Video structure outline
- Viral potential assessment
- Research gaps identified

**Output:** `video-projects/[topic-slug]-[date]/02-preliminary-research.md`

**Decision point:** Is this topic worth investing in paid sources?

---

### Stage 3: Source Recommendations
**Command:** `/suggest-sources`

**What happens:**
1. I recommend 20-30 authoritative sources (up to 50 if all essential)
2. I prioritize "standard works" (cited 100+ times by scholars)
3. I research costs (Kindle, used, library availability)
4. I organize by tier (essential → nice-to-have)
5. I create acquisition priority list

**What you get:**
- Tier 1: Essential standard works
- Tier 2: Primary source collections
- Tier 3: Key academic articles
- Tier 4: Contemporary analysis
- Tier 5: Counter-perspective sources
- Tier 6: Historical context
- Total cost summary
- NotebookLM upload strategy

**Output:** `video-projects/[topic-slug]/03-source-recommendations.md`

**Your action:** Purchase/borrow sources and upload to NotebookLM

---

### Stage 4: Custom NotebookLM Prompts
**Command:** `/notebooklm-prompts`

**What happens:**
1. I create 6-8 fully customized prompts for your specific topic
2. Each prompt targets specific evidence needs
3. All prompts are copy-paste ready
4. Optimized for NotebookLM's capabilities

**Prompts include:**
- Research organization (extract most important evidence)
- Smoking gun evidence extraction
- Pattern recognition (systematic issues)
- Counter-evidence analysis (academic balance)
- Modern relevance mapping (2024-2025 impact)
- Script hook generation (viral opening ideas)
- Academic consensus summary
- Fact-check preparation

**Output:** `video-projects/[topic-slug]/04-notebooklm-prompts.md`

**Your action:**
1. Copy each prompt
2. Paste into NotebookLM
3. Save all responses
4. Paste complete output back to me

---

### Stage 5: Script Generation
**Command:** `/script`

**What happens:**
1. You paste all NotebookLM output
2. I save it to your project directory
3. I cross-check against preliminary research
4. I flag inconsistencies or unsupported claims
5. I generate complete script using proven Vance/Essequibo formula

**Script includes:**
- Immediate drama opening (8 seconds)
- Pattern revelation structure (3+ claims)
- Primary sources marked with visual cues
- Modern stakes by 2:00 mark
- Precise language (exact numbers, named individuals)
- Investigation framing
- Fact-check priority list (Tier 1-3)
- B-roll requirements (Critical/Important/Nice-to-have)
- Visual planning markers

**Output:** `video-projects/[topic-slug]/06-script-draft.md`

**Next step:** `/fact-check` to verify before filming

---

## Verification Stage

### Fact-Check Script
**Command:** `/fact-check`

**What happens:**
1. I extract all factual claims from your script
2. I organize by evidence tier (1-3)
3. I check against source hierarchy
4. I flag contested or unverified claims
5. I give you pre-filming approval or issues list

**Categories checked:**
- Statistics & numbers
- Direct quotes
- Historical events
- Cause-effect claims
- Attribution claims

**Output:** Fact-check report with ✅ verified / ⚠️ needs verification / ❌ incorrect

---

## Your Project Directory

After running `/create-video`, you'll have:

```
video-projects/
└── [topic-name]-[date]/
    ├── 01-trend-research.md
    ├── 02-preliminary-research.md
    ├── 03-source-recommendations.md
    ├── 04-notebooklm-prompts.md
    ├── 05-notebooklm-output.md
    └── 06-script-draft.md
```

Everything in one organized location.

---

## Three Ways to Use This System

### Option 1: Full Pipeline (Exploring)
```
/create-video
```
Guides you through all 5 stages with pauses for input.

### Option 2: Jump In Anywhere (Targeted)
```
/find-topic           → Just need topic ideas
/deep-research        → Have topic, need validation
/suggest-sources      → Have research, need source list
/notebooklm-prompts   → Have sources, need prompts
/script               → Have NotebookLM output, need script
```

### Option 3: Legacy Quick Script
```
/script
```
If you have research ready and just need the script.

---

## Key Principles Enforced

These tools automatically apply your proven formula:

**Opening (First 8 seconds):**
- Concrete action or number in first sentence
- Visual elements immediately clear
- Stakes obvious
- Specificity: "114 nautical miles" not "over 100"

**Structure:**
- Modern stakes by 2:00 mark (payoff-first)
- Pattern revelation (minimum 3 interconnected claims)
- Primary sources on screen (marked with **[DOCUMENT: Name]**)
- Academic framing (evidence-based, not political)

**Language:**
- Investigation framing: "So I went to the archives..."
- Named individuals: "Second Lieutenant Ansel Murray" not "a soldier"
- Precise numbers: exact figures, not approximations
- No vague language: "many," "some," "a lot"

**Quality:**
- Every claim needs 2+ sources
- Counter-evidence acknowledged
- Contested claims labeled
- Historical integrity above all

---

## Example: Complete Workflow in Action

**Monday:** `/find-topic`
- Research trends
- Run VidIQ prompt
- Choose topic: "The Treaty That's Causing a War in 2025"

**Tuesday:** `/deep-research`
- Deep dive on free sources
- Find smoking gun evidence
- Get YES verdict
- Identified 8 primary sources (all free online)

**Wednesday:** `/suggest-sources`
- Get list of 25 authoritative books/articles
- Total cost: $280 (ebooks for instant access)
- Purchase top 15 essential sources

**Thursday-Friday:** Upload sources, run NotebookLM
- Upload 15 sources to NotebookLM
- `/notebooklm-prompts` gives me 7 custom prompts
- Run all prompts, collect responses

**Saturday:** `/script`
- Paste NotebookLM output
- Get complete 12-minute script
- Includes fact-check list and B-roll requirements

**Sunday:** `/fact-check`
- Verify all claims
- Get approval to film
- Start production

**One week: Idea → Script-ready**

---

## Tips for Best Results

1. **Don't skip stages** - Each builds on the last
2. **VidIQ integration is crucial** - Trend validation matters
3. **Preliminary research saves money** - Know topic is viable before buying sources
4. **NotebookLM prompts are customized** - Not generic templates
5. **Cross-checking happens automatically** - I flag inconsistencies
6. **Fact-check before filming** - Always

---

## Questions?

- Check `.claude/README.md` for technical details
- Review individual skill files in `.claude/skills/` for methodology
- All commands have help text built in

**Ready to create your next video?**

Type `/create-video` and let's start.
