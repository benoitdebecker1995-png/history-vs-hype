# NotebookLM Comment Verification Template

**Created:** 2026-01-05
**Purpose:** Standardized prompts for verifying commenter claims using NotebookLM sources
**Based on:** Somaliland comment response session (Burji-Isaaq thread)

---

## When to Use NotebookLM for Comment Verification

Use NotebookLM instead of WebSearch when:

1. **Commenter cites academic sources** (books, legal documents, UN reports)
2. **Claims require cross-referencing** multiple primary sources
3. **You need exact page numbers** and word-for-word quotes
4. **The topic has an existing notebook** with sources already uploaded
5. **Commenter may be selectively citing** (need to check author's full conclusion)

---

## Standard Verification Prompt

Copy and customize this prompt for your NotebookLM session:

```
I'm responding to a YouTube commenter who made claims about [TOPIC]. I need to verify their claims against the sources in this notebook.

**COMMENTER'S CLAIMS TO VERIFY:**

1. CLAIM: "[Exact claim from comment - copy verbatim]"
   - Is this accurate according to the sources?
   - What is the exact quote with page number?
   - Any caveats or context the commenter omitted?

2. CLAIM: "[Second claim]"
   - Verification needed
   - Source and page number?

3. CLAIM: "[Third claim]"
   - Verification needed

**CLAIMS I PLAN TO MAKE IN MY RESPONSE:**

1. MY CLAIM: "[What I plan to say in response]"
   - Is this supported by the sources?
   - Exact quote and page number?

2. MY CLAIM: "[Second thing I'll assert]"
   - Source verification needed

**CRITICAL ANALYSIS QUESTIONS:**

1. What context might the commenter be OMITTING?
   - Did the author they cite reach a different overall conclusion?
   - Are there counter-arguments or caveats they're ignoring?
   - Did subsequent events change the situation they describe?

2. What is the cited author's ACTUAL CONCLUSION?
   - Not just the evidence, but what did they conclude from it?
   - Example: Contini documented procedural failures BUT concluded the union was lawful

3. Are there STRONGER arguments the commenter didn't mention?
   - Sometimes commenters cite weaker points while missing stronger ones
   - Example: Article 10 safeguards never implemented was stronger than signature issues

**OUTPUT FORMAT:**

For each claim, provide:
- Status: ✅ VERIFIED / ❌ INACCURATE / ⚠️ PARTIALLY TRUE / 🔍 NOT IN SOURCES
- Exact quote with [Source, page number]
- Context the commenter may have missed
- Confidence level: HIGH / MEDIUM / LOW

Flag if commenter is:
- Selectively citing (omitting author's conclusion)
- Missing stronger arguments
- Conflating different issues
```

---

## Specialized Prompts by Comment Type

### Legal/Treaty Claims

```
The commenter is making legal claims about [TREATY/AGREEMENT/COURT CASE].

**LEGAL CLAIMS TO VERIFY:**

1. "[Specific legal claim]"
   - What does the primary document actually say?
   - Exact article/clause with quote?

2. "[Procedural claim about ratification/signing/etc.]"
   - What is the documented sequence of events?
   - Dates and specific actions?

**KEY LEGAL QUESTIONS:**

1. Was there a subsequent legal instrument that addressed this issue?
   - Retroactive legislation?
   - Court ruling?
   - Constitutional amendment?

2. What is the current legal status vs. the historical defect?
   - Does the defect still matter legally?
   - Has it been "cured" by subsequent action?

3. What do legal scholars conclude (not just document)?
   - Distinction between documenting a problem vs. concluding invalidity
```

### Historical Naming/Cartography Claims

```
The commenter claims that historical names/maps show [SPECIFIC CLAIM].

**CARTOGRAPHIC/NAMING CLAIMS TO VERIFY:**

1. "[Claim about what historical maps showed]"
   - What do the sources say about historical terminology?
   - First recorded use of term?
   - What regions did the term apply to?

2. "[Claim about ethnic/territorial distinctions]"
   - What do sources say about pre-colonial political entities?
   - Were there distinct governance structures?

**KEY QUESTIONS:**

1. Distinguish between:
   - Place names on maps (which varied by cartographer/period)
   - Ethnic identity (who lived where)
   - Political entities (who governed what)

2. What is the commenter conflating or oversimplifying?
```

### Genocide/Atrocity Claims

```
The commenter claims [SPECIFIC ATROCITY CLAIM].

**ATROCITY CLAIMS TO VERIFY (Handle with care):**

1. "[Claim about investigation/finding]"
   - Was this investigation real?
   - Who conducted it? When?
   - What were the exact findings?

2. "[Claim about scale/casualties]"
   - What range do sources give?
   - Note: estimates often vary widely

3. "[Claim about perpetrators/responsibility]"
   - What do sources attribute to whom?
   - State-sponsored vs. other actors?

**CRITICAL NOTES:**

- Be precise about casualty figures (give ranges, not single numbers)
- Note when something is "documented" vs. "alleged"
- Distinguish between investigation findings and formal legal recognition
- Handle with respect for victims
```

---

## Post-Verification Checklist

After running the NotebookLM verification:

- [ ] All commenter claims verified with exact quotes and page numbers
- [ ] All MY planned claims also verified
- [ ] Identified any context commenter omitted
- [ ] Checked author's actual conclusion (not just cited evidence)
- [ ] Noted any stronger arguments commenter missed
- [ ] Flagged claims that are ⚠️ PARTIALLY TRUE with explanation
- [ ] Ready to draft response using verified facts

---

## Example: Somaliland Session (2026-01-05)

**What the commenter (Burji-Isaaq) cited:**
- Paolo Contini documented procedural failures in 1960 union

**What NotebookLM verification revealed:**
1. ✅ Procedural failures were real and documented
2. ⚠️ BUT Contini also concluded "a full and lawful union was formed"
3. ⚠️ Commenter omitted that Law No. 5 (1961) attempted to cure defects
4. ✅ Article 10 safeguards were promised but NEVER implemented (stronger argument than signature issues)

**Key insight:** Commenter was selectively citing Contini's documentation of problems while omitting his conclusion that the union was lawful.

---

## Integration with Workflow

1. **Before running NotebookLM:** Complete Step 0 (claim extraction) from respond-to-comment.md
2. **Customize prompt:** Use the appropriate specialized template
3. **Run verification:** Get exact quotes with page numbers
4. **Check for omissions:** What did commenter leave out?
5. **Draft response:** Use verified facts only
6. **Save research:** Add to research file and VERIFIED-CLAIMS-DATABASE

---

## Sources

- Based on Somaliland comment response session (2026-01-05)
- Uses NotebookLM Gemini 2.0 Flash capabilities
- Integrates with COMMENT-RESPONSE-STRATEGY.md framework
