# 02 — NotebookLM Verification Prompts (Phase 2)

**Use these prompts AFTER uploading the source list from `01-PRELIMINARY-RESEARCH.md`.** Each prompt has a pass/fail condition. If NLM can't cite the specific page/passage for the answer, the claim stays ❓ and doesn't enter the script.

---

## Prompt 1 — Article 11 text, verbatim

> Using only the sources I've uploaded, quote Article 11 of the 1796/1797 Treaty of Tripoli exactly as it appears in the Barlow translation submitted to the US Senate for ratification. I need the full sentence, not a paraphrase. Cite the exact page or document reference for this quote.

**Pass:** Direct quote with page citation from Miller 1931 OR Senate Executive Journal 1797.
**Fail:** Paraphrase, or citation to a secondary source only.

---

## Prompt 2 — Senate ratification mechanics

> What does the Senate Executive Journal record about the ratification of the Treaty of Tripoli in June 1797? Specifically: the exact date of the vote, whether the vote was unanimous among those present, the number of senators voting, and whether there is any recorded debate about Article 11. Quote the Journal entry directly.

**Pass:** Direct Journal quote with date and vote count.
**Fail:** Secondary-source claim of "unanimous" without the Journal entry.

---

## Prompt 3 — Hunter Miller's 1931 finding

> In Hunter Miller's 1931 notes (Treaties and Other International Acts of the United States of America, Volume 2), what does Miller say about the relationship between the Barlow English translation and the Arabic original of the 1796 Treaty of Tripoli? Specifically, what does he say about Article 11? Quote his exact words, not a summary. Cite page numbers.

**Pass:** Direct quote of Miller saying Article 11 has no counterpart in the Arabic, with page citation.
**Fail:** Paraphrase or secondhand attribution.

---

## Prompt 4 — What IS in the Arabic where Article 11 should be

> According to Miller's 1931 analysis, what does the Arabic manuscript of the Treaty of Tripoli actually contain in the position where Article 11 would be expected? Specifically, is it a letter from the Dey of Algiers to the Pasha of Tripoli, and if so, what does Miller say about its content and date? Quote Miller directly and cite pages.

**Pass:** Direct Miller quote describing the content at that position + what the document is.
**Fail:** Repetition of "there is no Article 11" without describing what IS there.

---

## Prompt 5 — Barlow as translator and drafter

> What do the sources say about Joel Barlow's role in producing the English text of the Treaty of Tripoli? Was he the sole translator, or was there a State Department revision process before Senate transmission? Was Barlow a diplomat, a poet, both? Quote the sources directly.

**Pass:** Clear account of Barlow's role with citations. Distinguishes translation from drafting.
**Fail:** Vague "Barlow wrote it" without source attribution.

---

## Prompt 6 — Contemporary reaction to Article 11

> Between 1797 and 1805, is there any documented contemporary public reaction, newspaper commentary, sermon, pamphlet, or congressional debate that specifically addresses Article 11 of the Treaty of Tripoli as controversial, heretical, or noteworthy? If not, say so explicitly. Quote any documented reactions you find.

**Pass:** Either specific documented reactions with citations, OR a clear statement from an academic source that there was no documented contemporary controversy (which is itself the story).
**Fail:** Modern-era commentary presented as contemporary.

---

## Prompt 7 — The 1805 superseding treaty

> The 1796/1797 Treaty of Tripoli was superseded by the 1805 Treaty of Tripoli after the First Barbary War. Does the 1805 treaty contain an article equivalent to Article 11 of the earlier treaty? If not, what does the 1805 treaty say about religion, if anything? Quote the 1805 treaty directly.

**Pass:** Direct text of the 1805 treaty on religion (or confirmation that it's silent on the subject).
**Fail:** "It was different" without quoting the 1805 document.

---

## Prompt 8 — Scholarly interpretations of the Arabic discrepancy

> Since Hunter Miller flagged the Article 11 Arabic/English discrepancy in 1931, have academic historians (not popular writers) proposed explanations for why the Arabic original lacks Article 11? Cite specific scholars and their hypotheses, with page references. If scholarship has not proposed a consensus explanation, say so.

**Pass:** Named scholars, specific hypotheses, citations. OR a clear "no consensus exists" with source.
**Fail:** Speculation presented as scholarly consensus.

---

## Prompt 9 — The secular-founding question in Adams's 1797 context

> In 1797, what was the prevailing legal understanding among Senators and the Adams administration about the relationship between the federal government and Christianity? Use primary sources and academic commentary (not modern polemical writers). Distinguish between (a) the religious practice of most Americans, (b) state-level establishment practices still in place in 1797, and (c) the legal framing of the federal government itself. Cite sources.

**Pass:** A nuanced answer that distinguishes the three categories with citations.
**Fail:** A simple "yes" or "no" to the modern question.

**Purpose of this prompt:** bulletproof the mitigation. If the script preempts the obvious objection by noting that "most 1797 Americans were Christian, but the legal framing of the federal government was a different question," this prompt verifies that's a defensible statement, not a rhetorical move.

---

## Prompt 10 — Pre-filming attribution audit

> List every direct quote this video will need with: (a) the exact speaker or document, (b) the exact page or document reference, (c) a confidence score for whether the quote is attributed correctly in mainstream sources versus commonly misattributed. Flag anything that looks like a disputed attribution.

**Pass:** Complete audit table.
**Fail:** Vague confidence without citation.

**This is the standard pre-filming audit prompt from `NOTEBOOKLM-RESEARCH-PROMPTS.md`.** Run it LAST, just before the script is locked.
