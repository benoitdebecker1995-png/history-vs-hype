# _research/ Subfolder Template

**Purpose:** Standard structure for supporting research materials in video projects.

**When to use:** Projects with 10+ sources or extensive NotebookLM research. For simpler projects (3-5 sources), keep research in the main `01-VERIFIED-RESEARCH.md` file.

---

## Standard Folder Structure

```
[number]-[topic]-[year]/
  01-VERIFIED-RESEARCH.md          # Single source of truth (always at project root)
  02-SCRIPT-DRAFT.md
  03-FACT-CHECK-VERIFICATION.md
  _research/
    00-NOTEBOOKLM-SOURCE-LIST.md   # What to download (mandatory)
    01-PRELIMINARY-RESEARCH.md     # Internet research (Phase 1)
    02-NOTEBOOKLM-PROMPTS.md       # Verification queries (Phase 2)
    notebooklm-outputs/            # Raw outputs, organized by date (optional)
      2025-01-15-initial-queries.md
      2025-01-17-follow-up.md
```

**Key principle:** `01-VERIFIED-RESEARCH.md` stays at project root. Supporting files go in `_research/`. Raw NotebookLM outputs stay in `notebooklm-outputs/` subfolder if preserved.

---

## File Templates

### 00-NOTEBOOKLM-SOURCE-LIST.md

```markdown
# NotebookLM Source List - [Topic Name]

**Video:** [Project folder name]
**NotebookLM Notebook:** [Name of your notebook]
**Created:** [YYYY-MM-DD]
**Status:** [X]/[Y] sources downloaded

---

## PRIMARY SOURCES [P]

### [P1] [Document Name]
- **Type:** [Primary source / Treaty / Legislation / Census / Archive document]
- **Date:** [When created]
- **Repository:** [Where it's held]
- **Access:** [URL / Library / Purchase link]
- **Key content:** [What's relevant to this video]
- **Download status:** [ ] Pending / [x] Downloaded
- **NotebookLM filename:** `[P1] Document-Name.pdf`

### [P2] [Document Name]
- **Type:** [Type]
- **Date:** [Date]
- **Repository:** [Repository]
- **Access:** [Access method]
- **Key content:** [Relevance]
- **Download status:** [ ] Pending
- **NotebookLM filename:** `[P2] Document-Name.pdf`

---

## ACADEMIC SOURCES [A]

### [A1] [Author Last Name], [First Name]. *[Title]*
- **Type:** Academic monograph / Journal article / Book chapter
- **Publisher:** [University press, year]
- **ISBN/DOI:** [If available]
- **Access:** [JSTOR / University library / Purchase]
- **Price:** [If purchasing]
- **Key chapters:** [Ch. X, Ch. Y - what's relevant]
- **Relevance:** [Why this source matters]
- **Download status:** [ ] Pending / [x] Downloaded
- **NotebookLM filename:** `[A1] Author-Short-Title.pdf`

### [A2] [Author Last Name], [First Name]. *[Title]*
[Same format as A1]

---

## MODERN CONTEXT [M]

### [M1] [Article/Report Title]
- **Type:** News article / Think tank report / Government report
- **Source:** [Publication name]
- **Date:** [YYYY-MM-DD]
- **Access:** [URL]
- **Key content:** [What modern context it provides]
- **Download status:** [ ] Pending
- **NotebookLM filename:** `[M1] Source-Title.pdf`

---

## DOWNLOAD CHECKLIST

- [ ] All [P] sources downloaded
- [ ] All [A] sources downloaded
- [ ] All [M] sources downloaded
- [ ] Files renamed with prefix notation
- [ ] Files uploaded to NotebookLM
- [ ] Audio Overview generated (with custom instructions)

---

## NOTEBOOKLM NOTEBOOK NOTES

**Custom Audio Overview instructions used:**
> "[Paste the instructions you gave to Audio Overview]"

**Total sources in notebook:** [X]
**Token estimate:** [If known]
```

---

### 01-PRELIMINARY-RESEARCH.md

```markdown
# Preliminary Research - [Topic Name]

**Video:** [Project folder name]
**Phase:** 1 - Internet Research
**Date:** [YYYY-MM-DD]
**Status:** Complete / In Progress

---

## KEY QUESTIONS TO ANSWER

1. [Main question this video addresses]
2. [Supporting question]
3. [Supporting question]
4. [What counter-arguments exist?]

---

## CLAIMS TO VERIFY

| Claim | Status | Source Found | Notes |
|-------|--------|--------------|-------|
| [Claim 1] | Unverified | [Internet source] | Needs NotebookLM verification |
| [Claim 2] | Unverified | [Internet source] | Check [specific academic source] |
| [Claim 3] | Unverified | [None yet] | Search for [specific terms] |

---

## INTERNET SOURCES FOUND

### Source 1: [Title/Description]
- **URL:** [link]
- **Type:** Wikipedia / News / Blog / .edu
- **Reliability:** LOW - needs academic verification
- **Key info:** [What it says]
- **Claims to extract:** [List specific claims]

### Source 2: [Title/Description]
[Same format]

---

## OPPONENT/COUNTER-ARGUMENTS

### What the myth claims:
> "[The myth or misconception you're addressing]"

### Who promotes this:
- [Public figure / movement / common belief]
- [Source where this is stated]

### Their evidence (steelman):
- [What evidence do they cite?]
- [What's the strongest version of their argument?]

---

## NOTEBOOKLM UPGRADE PATH

**Sources to find for Phase 2:**
1. [ ] Academic monograph on [topic] - check university press catalogues
2. [ ] Primary source: [specific document needed]
3. [ ] Scholarly article on [specific aspect]

**Next step:** Complete `00-NOTEBOOKLM-SOURCE-LIST.md` with specific books/documents to download

---

## RESEARCH NOTES

[Any observations, leads to follow, or context to remember]
```

---

### 02-NOTEBOOKLM-PROMPTS.md

```markdown
# NotebookLM Prompts - [Topic Name]

**Video:** [Project folder name]
**Phase:** 2 - Academic Verification
**Notebook:** [NotebookLM notebook name]
**Date:** [YYYY-MM-DD]

---

## VERIFICATION PROMPT TEMPLATE

Use this template for each claim that needs verification:

```
I need to verify this specific claim: "[Exact claim statement]"

Please:
1. Confirm if this is accurate based on the sources
2. Provide the exact source and page number (click the citation link)
3. Note any caveats or nuances
4. Identify if any scholars in these sources dispute this
5. Give me a word-for-word quote I can display on screen

If the claim is contested, tell me:
- What the majority view is
- What the minority view argues
- Which sources support each position
```

---

## CLAIM VERIFICATIONS

### Claim 1: [Clear statement of fact]

**Prompt sent:**
> [Paste the prompt you used]

**NotebookLM response:**
> [Paste the response - keep for reference]

**Citation found:** [Author], *[Title]*, p. [page]
**Verified:** YES / NO / PARTIALLY
**Transfer to 01-VERIFIED-RESEARCH.md:** [ ] Done

---

### Claim 2: [Next claim]

**Prompt sent:**
> [Prompt]

**NotebookLM response:**
> [Response]

**Citation found:** [Citation]
**Verified:** YES / NO / PARTIALLY
**Transfer to 01-VERIFIED-RESEARCH.md:** [ ] Done

---

## QUOTE EXTRACTION

### Quote needed for: [Topic/Script section]

**Prompt sent:**
> "Find me a word-for-word quote about [topic] that I can display on screen. Include the exact page number."

**Quote found:**
> "[Exact quote]"
> - [Author], *[Title]*, p. [page]

**Transfer to 01-VERIFIED-RESEARCH.md:** [ ] Done

---

## FOLLOW-UP QUESTIONS

Prompts for deeper understanding:

1. "What's the scholarly consensus on [contested point]? Which sources support each view?"

2. "Are there any primary sources cited in these books that I should find the original of?"

3. "What counter-evidence or alternative interpretations do these scholars acknowledge?"

---

## EXTRACTION CHECKLIST

**Before closing NotebookLM session:**

- [ ] All claim verifications transferred to 01-VERIFIED-RESEARCH.md
- [ ] All quotes extracted with exact page numbers
- [ ] Contested claims noted with both sides
- [ ] Any corrections to preliminary research noted
- [ ] Raw outputs saved to `notebooklm-outputs/` if needed

---

## SESSION NOTES

**Date:** [YYYY-MM-DD]
**Duration:** [X hours]
**Key findings:**
- [Finding 1]
- [Finding 2]

**Still need to verify:**
- [Remaining claim]
- [Remaining claim]
```

---

## Usage Notes

### When to create _research/ subfolder:
- Videos with 10+ sources
- Topics requiring extensive NotebookLM work
- Complex fact-checks with multiple opponent claims
- Topics that may spawn follow-up videos (preserve research trail)

### When NOT to create _research/ subfolder:
- Simple fact-checks (3-5 sources)
- Quick response videos
- Topics where all research fits in 01-VERIFIED-RESEARCH.md

### Raw NotebookLM outputs:
- If preserving: Put in `notebooklm-outputs/` dated folder
- Better practice: Extract key findings immediately to 01-VERIFIED-RESEARCH.md
- Don't let raw outputs accumulate without extraction

### Integration with main project:
- 01-VERIFIED-RESEARCH.md at project root is the **single source of truth**
- _research/ files are supporting materials only
- Script pulls ONLY from 01-VERIFIED-RESEARCH.md, never directly from _research/ files
