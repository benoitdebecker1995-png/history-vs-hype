# Contract: notebook-researcher

**Version locked:** 2026-05-13
**Agent file:** `.claude/agents/notebook-researcher.md`
**Assigned model:** Sonnet (Phase D citation grounding requires accurate verbatim matching)
**Pattern parent:** `wiki-researcher.contract.md` — same shape, NotebookLM-driven instead of Wikipedia-driven

---

## Input shape

The agent accepts a single free-text invocation prompt. It parses out:

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `notebook_name_or_id` | string | YES | `"Saltwater Slavery"` (fuzzy match) or `"a7d430b1-cba8-43b4-9f86-f4ab12e5560f"` |
| `topic_context` | string | NO | `"counter to the 'Africans sold their own' viral talking point"` |
| `output_path` | string (absolute) | NO | `"D:/History vs Hype/video-projects/_IN_PRODUCTION/56-.../_research/"` |

**Two valid invocation shapes:**

- **Shape A (minimal):** *"Use notebook 'Saltwater Slavery'."*
- **Shape B (with brief):** *"Use notebook 'Saltwater Slavery'. I'm thinking about a video that counters the 'Africans sold their own' talking point."*

**Caller examples:**
- Main conversation agent invoking via Task tool: `Task(subagent_type="notebook-researcher", prompt="...")`
- Direct user invocation: *"Use the notebook-researcher agent on X notebook."*

---

## Output shape

**File written to:** (priority order)
1. If `output_path` provided: written there as `notebook-brief-{YYYY-MM-DD}.md`
2. Else if invoked from / topic_context references a `video-projects/_IN_PRODUCTION/<slug>/` folder: `<slug>/_research/notebook-brief-{YYYY-MM-DD}.md`
3. Else: `~/.claude/notebook-briefs/{notebook-slug}-{YYYY-MM-DD}.md` (directory auto-created if missing)

**Chat reply:** 1-paragraph elevator summary + the absolute file path of the brief.

**Required H2 sections (exact strings — schema contract):**

```
## NOTEBOOK
## TOPIC SURVEY
## KEY FACTS
## CANDIDATE VIDEO ANGLES
## AGENT'S PICK + REASONING
## DEPTH RESEARCH
## GROUNDED EXHIBITS
## UNGROUNDED CANDIDATES
## SCHOLARLY DISAGREEMENTS
## RECOMMENDED NEXT STEPS
```

**Required header block** (first 5 lines of file):
```
# Notebook Brief: [Notebook Name]

**Generated:** [YYYY-MM-DD]
**Notebook:** [name] ([N] sources, last modified [date])
**Research question:** [topic_context if provided; else "blind scan"]
```

---

## Output content rules

| Section | Rule |
|---|---|
| `## NOTEBOOK` | UUID + title + source count + last-modified date + 1-sentence primary-topic characterization |
| `## TOPIC SURVEY` | 3-5 paragraphs synthesizing Q1 response. No citations required at this level. |
| `## KEY FACTS` | 10-20 bulleted facts/dates/figures/documents. Each cites scholarly source. |
| `## CANDIDATE VIDEO ANGLES` | 3-5 angles, each with: angle name, one-line pitch, primary exhibits available, audience-fit notes, strength signal |
| `## AGENT'S PICK + REASONING` | Names the primary pick explicitly. Lists 2-4 reasons. Lists rejected alternatives with one-line reasoning each. |
| `## DEPTH RESEARCH` | Synthesis of Phase C queries. One sub-section per query that ran (Q6-Q10 are optional based on angle). |
| `## GROUNDED EXHIBITS` | 4-5 exhibits, each with: source citation (Citation Format v2), authority blurb, verbatim blockquote, chapter+page location, ✅/⏳/❌ verdict, translation variants noted, contextual notes |
| `## UNGROUNDED CANDIDATES` | Table of exhibits surfaced but not grounded this run, with which alternate angle each serves |
| `## SCHOLARLY DISAGREEMENTS` | Table of scholar-A-vs-scholar-B contested topics + bear-trap framing |
| `## RECOMMENDED NEXT STEPS` | Concrete moves: if-proceeding-with-pick / if-picking-alternate / if-corpus-needs-more-sources / pre-filming prep |

**Citation Format v2** (mandatory throughout): `Author Last, First. "Full Title." Publisher, Year. p. XX. [Translator: Name, if translated]`

---

## Downstream consumers

| Consumer | What it reads | How it uses output |
|----------|--------------|-------------------|
| Human user | Full brief | Reviews `## AGENT'S PICK + REASONING` to decide angle; copies blockquotes from `## GROUNDED EXHIBITS` into `01-VERIFIED-RESEARCH.md` |
| `script-writer-v2` | Indirectly — verified blockquotes after user manually copies them to `01-VERIFIED-RESEARCH.md` | Quotes the verbatim passages with page citations on-screen |
| `structure-checker-v2` | Indirectly — thesis verb grounding cited in `## DEPTH RESEARCH` | Rule 36 thesis discipline audit (mechanism-word grounding) |
| `article-writer` (mode=WRITE) | Same blockquotes via `01-VERIFIED-RESEARCH.md` | Rule 21 thesis discipline / Rule 5C citation grounding |

**Breaking change definition:** Missing any required H2 section, or output file not written to the expected path, or any ungrounded ⏳ exhibit presented as ready-for-film.

---

## Tool dependencies

The agent requires these MCP tools (declared in YAML frontmatter):

```
- mcp__notebooklm__notebook_list      (Step 1: discover notebooks)
- mcp__notebooklm__notebook_describe  (Step 1: get AI summary + source count)
- mcp__notebooklm__notebook_query     (Steps 2/4/5: all research queries)
```

Plus standard Read/Write/Grep/Glob for output file handling.

**Authentication:** NotebookLM MCP requires `nlm login` to have been run by the user. The agent does NOT attempt to re-authenticate; it aborts with a clear error message if auth has expired.

---

## Canonical baseline

**Reference outputs from the workflow this agent codifies:**

| File | Role |
|---|---|
| `video-projects/_IN_PRODUCTION/56-no-lassos-atlantic-slave-trade-origin-2026/_research/saltwater-slavery-notebook-synthesis-2026-05-13.md` | Phase A landscape-scan shape — 7 candidate angles surfaced from a 25-source notebook |
| `video-projects/_IN_PRODUCTION/56-no-lassos-atlantic-slave-trade-origin-2026/01-VERIFIED-RESEARCH.md` | Phase D grounded-exhibit format — 4 exhibits with ✅ verbatim + page citations |

A successful run on a different notebook should produce a brief of comparable depth: 3-5 candidate angles surfaced, 4-5 grounded exhibits with page citations, recurring deflections named, scholarly disagreements documented.

---

## Validation procedure

After any change to the agent:

1. **Schema check** — `grep -E "^## " <output>` must return exactly the 10 required H2 sections in order.
2. **Smoke test** — Invoke against the Saltwater Slavery notebook with topic_context = *"counter to the 'Africans sold their own' viral talking point"*. Expect the four locked exhibits from #56 (Zurara Ch XIX / Afonso July 1526 / Pieter de Marees / Romanus Pontifex) to surface in `## GROUNDED EXHIBITS` with ✅ verdicts.
3. **New-topic trial** — Invoke against a different notebook (e.g. "Vance Speech – Historical Claims Research") with no topic_context. Confirm prompts aren't over-fitted to #56's counter-narrative framing.
4. **Failure-mode trial** — Invoke against a non-existent notebook name. Confirm graceful abort with disambiguation request, no hallucinated brief.

---

## Failure modes

| Failure | Agent behavior |
|---------|---------------|
| Notebook not found | Abort. List available notebooks, ask invoker to disambiguate. |
| Multiple fuzzy matches | Abort. List matches, ask invoker to specify. |
| Auth expired | Abort. Reply with `nlm login` instructions. |
| Notebook source count <5 | Abort with "insufficient corpus" message. |
| Phase A query empty / short | Continue; note corpus gap in `## SCHOLARLY DISAGREEMENTS`. |
| Phase D returns ⏳ | Flag in `## GROUNDED EXHIBITS`. Do NOT replace. |
| Phase D returns ❌ | Flag in `## GROUNDED EXHIBITS` + note source-acquisition gap in `## RECOMMENDED NEXT STEPS`. Do NOT replace. |
| Query timeout (>120s) | Skip that query, continue with rest. Note in `## RECOMMENDED NEXT STEPS`. |
| Phase B yields zero viable angles | Truncate brief at `## CANDIDATE VIDEO ANGLES` with explicit "no angle meets criteria" message. Stop. |

---

## Differences from `wiki-researcher` contract

- Sources: NotebookLM MCP instead of Wikipedia + WebFetch
- Output: research brief with grounded blockquotes instead of preliminary brief with unverified claims
- Phase: 2 (academic verification) instead of 1 (landscape scan)
- Cost profile: ~13-15 MCP calls per run instead of 2-4 Gemini WebFetch calls
- Verdict semantics: ✅/⏳/❌ per exhibit (not "Verify?" flag per claim)
- File write target: `notebook-brief-{date}.md` instead of `00-PRELIMINARY-BRIEF.md` (different file, both can coexist in `_research/`)

---

## Change log

- **1.0 — 2026-05-13** — Initial lock. Codified from #56 Atlantic slave trade workflow + `/grill-with-docs` design session. Single autonomous run, 4-5 grounded exhibits target, flag-and-move-on on ⏳/❌, anti-yes-manning via full-landscape brief.
