---
name: NotebookLM Citation Grounding (article-writer Rule 5C + script-writer-v2 Rule 42)
description: Both article-writer AND script-writer-v2 must round-trip every direct quote through the project's NotebookLM notebook before output is locked. Script-stage research-file verification is necessary but not sufficient.
type: feedback
originSessionId: 1d752b6d-75c0-42f1-a54d-0f1ea7ada73b
---
# NotebookLM Citation Grounding for Articles AND Scripts

## Scope expansion (2026-05-09)

Originally rule was article-writer-only. Extended to script-writer-v2 after Inquisition #54 §6 "worse death/enemy" slip — the Toledo converso quote went to film with `⏳ Confirm verbatim` status in `03-FACT-CHECK-VERIFICATION.md` row 90; script wrote *"continual fear is a worse **death** than a sudden demise"*; user spoke *"worse **enemy**"* in the rough cut. Either is wrong; the verification gate should have caught it pre-record. Script-writer-v2 v15.0 (2026-05-09) added Rule 42 — exact mirror of article-writer Rule 5C — to close the script-stage gap.

**Cross-agent rule:** A script cannot be marked ✅ DRAFT-LOCKED if `03-FACT-CHECK-VERIFICATION.md` contains any ⏳ rows for blockquotes. Memory ≠ source; "memory file confirms this quote and page" + ⏳ status = NOT verified.

---

# Original — NotebookLM Citation Grounding for Articles

**Rule:** Every direct quote in an article draft must be verified verbatim against the project's NotebookLM notebook BEFORE the draft is written. The script-stage `01-VERIFIED-RESEARCH.md` is necessary but not sufficient — script→article conversion can introduce paraphrases, reformatted attributions, and citation drift that the script-stage check doesn't catch.

**Why:** Berlin Conference article (2026-04-29, project #40) was generated from local files only. The Anthony Anghie reference shipped as a paraphrase styled as authority — agent self-disclosed it after the fact. User caught it with "you didnt even consult the notebook???" — a fair indictment. The competitive advantage the channel runs on (CLAUDE.md: "NEVER skip Phase 2 — that's the competitive advantage") was being honored at script stage but quietly skipped at article stage. Closing that gap restores citation discipline across both formats.

**How to apply (article-writer agent procedure, baked into Rule 5C):**

1. **Locate the notebook.** `mcp__notebooklm__notebook_list` → find the project's notebook by topic. If absent, raise `[NOTEBOOK GAP: no notebook found for <topic>]` and stop. Do not draft.
2. **Query every direct quote.** For each blockquote planned in the draft, `mcp__notebooklm__notebook_query` with the exact quoted text + cited author/work. Returns verbatim status + page + source.
3. **Triage:**
   - **Verbatim found** → use the quote, lock the page number into the citation block.
   - **Paraphrase** → rewrite to verbatim OR demote to indirect attribution (no blockquote).
   - **Not found** → flag `[NEEDS VERIFICATION: <quote> not in notebook for <work>]`. No blockquote.
4. **Log the trace.** Append `## NOTEBOOK VERIFICATION` table to the bottom of the draft: source / status / page / notebook source ID. The user reads this to confirm citation discipline.

**Where it lives:** `.claude/agents/article-writer.md` Rule 5C (HARD RULE, Tier 1) — bumped to v5.3. NotebookLM MCP tools added to agent toolset (`notebook_list`, `notebook_query`, `notebook_describe`). Quality Gate item added.

**Operational dependency:** Requires `nlm login` to be active. If auth expires, the agent must surface the auth error to the user (not silently fall back to script-stage research). Run `! nlm login` to re-authenticate.

**What this catches that previous rules missed:**
- Rule 5A (Verbatim Facts Only) only checked the script + research files — both could be paraphrased.
- Rule 5B (Earn-Your-Inclusion Test) checked narrative discipline — not citation accuracy.
- Rule 5C closes the loop: every blockquote is grounded against the primary-source notebook, not against secondary aggregations.

## Scope extension — mechanism claims (added 2026-05-10)

Round-trip verification extends from blockquotes to four specific claim types. **STOPS HERE** — does not extend beyond these four:

**(a) Blockquotes** — existing scope, unchanged.

**(b) Title's mechanism word** — the word locked under ADR-0003 must return HIGH confidence from the notebook. LOW confidence → soften the language OR pause for source acquisition. Cannot lock title with LOW-confidence mechanism word. (Pairs with Auditor's Edge extension in `feedback-auditors-edge.md`.)

**(c) Central thesis verb** — the action verb in the ≤12-word throughline (per THESIS-DISCIPLINE.md). If the thesis is "Italy *mistranslated* the treaty to manufacture a colonial claim," the verb "mistranslated" must be grounded. Notebook LOW confidence on the thesis verb = thesis is not yet lockable.

**(d) Named-figure protagonist-agency claim when the figure is a co-protagonist of the script** — when a named historical figure is given a verb of discovery, action, or resistance ("caught," "exposed," "rigged," "resisted") AND that figure appears for ≥30s of screen time or ≥1 full paragraph in the article, the claim must round-trip. Applies to co-protagonists, not to incidental mentions. A figure named once in a transition clause does not trigger this gate.

**Does NOT extend to:** every protagonist-agency verb, routine historical-action verbs ("signed," "led," "invaded"), connector verbs ("caused," "led to"), secondary-cited paraphrases where the scholar's reading is explicitly attributed. Those continue to use the citation-tag pattern.

**If load-bearing claim returns LOW confidence:** either (1) soften the language to what sources support — "the translation was used to manufacture a colonial claim" instead of "Italy rigged the treaty" — OR (2) pause for source acquisition. Cannot reach DRAFT-LOCKED with any unverified load-bearing claim in these four categories.

**Origin:** Adwa #39 (2026-05-10) — grill proposed "Italy Rigged + Empress Taytu Caught It" as title candidates. Phase 1 NotebookLM grounding returned LOW confidence on both: McLachlan documents the discrepancy but characterizes cause as "unclear"; does not credit Taytu with discovery. Title cannot lock until Phase 2 sources (Jonas, Prouty, Sereke-Brhan) are in the notebook and return HIGH confidence on the mechanism word.
