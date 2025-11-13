---
description: Start a new video project with the complete History vs Hype workflow
---

You are helping create a new video project for the History vs Hype YouTube channel.

## CRITICAL: Folder Structure

**Before creating any project files:**

1. **Determine project stage:**
   - New research/scripting → `video-projects/_IN_PRODUCTION/[project-name]/`
   - Script ready for filming → `video-projects/_READY_TO_FILM/[project-name]/`

2. **Create project folder:**
   ```
   Format: video-projects/_IN_PRODUCTION/[number]-[topic-slug-year]/
   Example: video-projects/_IN_PRODUCTION/3-kashmir-partition-2025/
   ```

3. **Check PROJECT_STATUS.md:**
   - Read current status before creating
   - Find next available project number
   - Update status file after creation

## Step 1: Topic Validation

**Ask these questions ONLY (don't ask for info you can research):**

1. **What's the topic/myth to debunk?**
2. **What's the modern hook?** (Current event, political claim, recent news)
3. **Why does this matter in 2025?**

Then evaluate:
- Colonial history, borders, or geopolitical myths?
- Modern news hook or political relevance?
- PRIMARY SOURCES available (treaties, documents, archives)?
- "Colonial borders still killing people" angle?
- Academic research available?

## Step 2: Research Setup Guide

Based on `guides/History-vs-Hype_Master-Project-Template.md`, guide them to:

1. **Create NotebookLM Research Notebook**
   - Name: `[Topic]_[Date]_Research`
   - Upload primary sources, academic papers, news analysis, counter-evidence
   - Max 50 sources, 25M words

2. **Run Key NotebookLM Prompts:**
   - Research organization prompt (5 essential questions)
   - Video hook generation prompt (3 compelling openings)
   - Evidence extraction prompt (tiered evidence list)
   - Counter-evidence prompt (strongest opposing arguments)

3. **Source Hierarchy Check:**
   - Tier 1: Primary documents (treaties, archives, census data)
   - Tier 2: Peer-reviewed academic publications
   - Tier 3: Expert historians specializing in the topic
   - Every major claim needs 2+ sources

## Step 3: Script Generation

Once research is ready, offer to:
- Generate the script using `/script` command
- Or guide them through manual script development

## Step 4: Fact-Checking Protocol

Remind them:
- Every factual claim needs 2+ sources
- Run NotebookLM fact-check prompt on completed script
- See `guides/fact-checking-protocol.md` for full process
- No filming until all Tier 1 evidence is verified

## Step 5: Production Planning

Help them create:
- **B-roll requirements list** (Critical/Important/Nice-to-have)
- **Visual strategy** using `guides/HYBRID_TALKING_HEAD_GUIDE.md`
- **Timeline**: Research → Script → Fact-check → Film → Edit → Publish

## Step 6: Next Steps Checklist

Provide them with:
- [ ] Topic validated against channel criteria
- [ ] NotebookLM notebook created with sources
- [ ] Research prompts run and evidence organized
- [ ] Script generated or outline ready
- [ ] Fact-checking completed (all Tier 1 evidence verified)
- [ ] B-roll requirements identified
- [ ] Visual strategy planned (when to show face vs. evidence)
- [ ] Ready to film

## Channel Mission Reminder

Quality over quantity, always. The goal is evidence-based education that reveals how distorted history fuels present-day conflicts. Historical integrity above all.

Target: 8-12 minutes, 41.5% average view duration, academic balance, modern relevance.
