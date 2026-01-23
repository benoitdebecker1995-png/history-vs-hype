---
deprecated: true
replaced_by: (removed - rarely used, use /verify --extract instead)
---

> **DEPRECATED:** This command has been removed (rarely used).
> For extracting claims from transcripts, use `/verify --extract`.
> Run `/help` to see current commands.

[Original content below for reference]
---

---
description: Analyze interview transcript and build production documents for fact-check video
---

You are analyzing a long interview transcript (from politicians, podcasters, etc.) to create a fact-check video for History vs Hype.

This command automates the workflow: **Interview Transcript -> Fact-Check Matrix -> Script Structure -> Production-Ready Research**

---

## WORKFLOW

### **STEP 1: Get NotebookLM Extracted Claims**

Ask the user:
- "Have you already extracted claims from the transcript using NotebookLM?"

**If NO:**
- Provide them with the NotebookLM extraction prompt (below)
- Tell them to run it and come back with results

**If YES:**
- Ask them to paste the NotebookLM output

---

## **NotebookLM Extraction Prompt (Give to User):**

```
This interview transcript contains historical claims I need to fact-check for a video.

EXTRACT:

1. HOLOCAUST/WW2 CLAIMS:
   Every statement about:
   - Death tolls, methods, timeline
   - Nazi intentions/planning
   - Camps, gas chambers, logistics
   - Churchill's role, Allied actions
   - WW2 causation/responsibility

2. OTHER HISTORICAL CLAIMS:
   - Specific dates, events, statistics
   - Cause-effect assertions
   - Historical comparisons
   - Treaty/document references

3. RHETORICAL FRAMING:
   - How is each claim qualified?
   - "Some historians say" / "allegedly" / stated as fact?
   - Dog whistles vs. explicit claims
   - Hedging language vs. definitive statements

FORMAT EACH AS:
---
[TIMESTAMP if available]
SPEAKER: [Name]
QUOTE: "[Exact quote]"
CLAIM TYPE: [Holocaust/WW2/Colonial/Economic/Other]
SPECIFIC ASSERTION: [What factual claim is being made]
VERIFIABLE: [Yes/No - can this be checked against documents?]
IMPACT: [High/Medium/Low - how explosive/important]
---
```

[Content truncated for brevity - see original file for full content]
