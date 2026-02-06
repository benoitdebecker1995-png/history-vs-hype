---
description: Complete workflow from topic research to finished script
---

> 💡 **Note:** For the 3-phase verified workflow (research → script → fact-check) with quality gates, use `/new-video-verified` instead. This command (`/create-video`) is a 5-stage alternative focused on topic discovery and NotebookLM source recommendations.

---

I'll guide you through the complete video creation workflow: topic research → deep dive → source recommendations → NotebookLM prompts → script generation.

## Workflow Overview

**Stage 1:** Find trending topics (web research + VidIQ)
**Stage 2:** Deep preliminary research (free sources only)
**Stage 3:** Recommend sources to purchase (authoritative books/articles)
**Stage 4:** Generate custom NotebookLM prompts
**Stage 5:** Write script from NotebookLM output

We'll pause between each stage for your input and approval.

## Project Directory

I'll create: `video-projects/[topic-name]-[date]/`

With files:
- `01-trend-research.md`
- `02-preliminary-research.md`
- `03-source-recommendations.md`
- `04-notebooklm-prompts.md`
- `05-notebooklm-output.md` (when you provide it)
- `06-script-draft.md`

Everything organized in one place.

---

## STAGE 1: Topic Research

I'll research current trends and news to find topics that could be hits on your channel.

**What I'll do:**
- Search for recent news hooks (border disputes, political claims, historical myths going viral)
- Evaluate against your criteria (primary sources available, modern relevance, not overdone)
- Provide you a VidIQ CoachPro prompt
- Cross-reference my findings with your VidIQ data
- Give you top 3 recommendations with viral potential scores

**Your role:**
- Run the VidIQ prompt I provide
- Paste back VidIQ's response
- Choose which topic to pursue

**Output:** `01-trend-research.md`

---

Ready to start with topic research? Or do you already have a topic in mind?

(If they already have a topic, skip to Stage 2)

---

## STAGE 2: Deep Preliminary Research

I'll do comprehensive research using only free sources to validate your topic is worth the investment.

**What I'll do:**
- Mine Wikipedia and bibliographies
- Hunt for primary sources (treaties, documents, archives)
- Summarize academic consensus
- Research counter-arguments
- Find modern relevance examples
- Assess viral potential
- Give you YES/MAYBE/NO verdict

**Your role:**
- Review the research
- Confirm the topic is worth pursuing
- Note any gaps or concerns

**Output:** `02-preliminary-research.md`

---

**Checkpoint:** Based on preliminary research, do you want to proceed with this topic?

(If NO, return to Stage 1. If YES, continue to Stage 3)

---

## STAGE 3: Source Recommendations

I'll recommend 20-30 authoritative sources worth purchasing for NotebookLM upload.

**What I'll do:**
- Find "standard works" (definitive scholarship cited 100+ times)
- Recommend primary source collections
- Suggest key academic articles
- Include counter-perspective sources (academic balance)
- Research costs (ebook, used, library)
- Provide acquisition priority
- Create NotebookLM upload strategy

**Your role:**
- Review recommendations
- Note budget constraints
- Start acquiring sources (purchase, borrow, request)

**Output:** `03-source-recommendations.md`

---

**Checkpoint:** Ready to acquire sources and upload to NotebookLM? Or want me to generate the prompts first?

---

## STAGE 4: Custom NotebookLM Prompts

I'll create fully customized research prompts tailored to your specific topic and sources.

**What I'll do:**
- Generate 6-8 custom prompts:
  - Topic-specific research organization
  - Smoking gun evidence extraction
  - Counter-evidence analysis
  - Modern relevance mapping
  - Pattern recognition
  - Script hook generation
- Make them copy-paste ready
- Optimize for NotebookLM's format

**Your role:**
- Upload your sources to NotebookLM
- Copy each prompt I provide
- Paste into NotebookLM
- Collect all responses

**Output:** `04-notebooklm-prompts.md`

---

**Checkpoint:** Have you run all the NotebookLM prompts and collected the output?

---

## STAGE 5: Script Generation

I'll turn your NotebookLM output into a complete video script using the proven Vance/Essequibo formula.

**What I'll do:**
- Analyze NotebookLM output
- Cross-check against preliminary research
- Flag any inconsistencies or unsupported claims
- Generate script with:
  - Immediate drama opening (8 seconds)
  - Pattern revelation structure (3+ claims)
  - Primary sources marked with visual cues
  - Modern stakes by 2:00 mark
  - Fact-check priority list
  - B-roll requirements

**Your role:**
- Paste all NotebookLM output
- Review script draft
- Request revisions if needed

**Output:** `06-script-draft.md`

---

**Final step:** Run `/fact-check` on the completed script to verify all claims before filming.

---

## Quick Navigation

At any point you can:
- Skip stages if you already have that research done
- Jump back to revise earlier stages
- Use individual commands (`/find-topic`, `/deep-research`, etc.) instead of this workflow
- Pause and resume later (all outputs saved)

---

Let's start! Do you:

**A)** Want me to research trending topics?

**B)** Already have a topic and want to skip to deep research?

**C)** Have research done and just need NotebookLM prompts?

**D)** Have NotebookLM output ready and want to generate the script?

Which stage should we start at?
