# Phase 40: Translation Pipeline - Context

**Gathered:** 2026-02-17
**Status:** Ready for planning

<domain>
## Phase Boundary

AI-powered document translation pipeline: clause-by-clause translation using Claude, cross-checked against independent translation tools, with legal term annotations, surprise clause detection, and split-screen formatted output. Input is original-language document text; output is structured translation ready for video production.

</domain>

<decisions>
## Implementation Decisions

### Translation approach
- **Input format:** Both pasted text (stdin/argument) and --file flag for file paths
- **Granularity:** Clause-by-clause translation (one API call per article/section), not full-document pass
- **Structure detection:** Auto-detect article/clause boundaries, then show user detected structure for confirmation before translating
- **Context per clause:** Full document context sent with each clause (highlight active clause). Accuracy over token cost
- **Integration with Phase 39:** Structure assessor output can feed into boundary detection

### Cross-check protocol
- **DeepL:** Optional — use if API key available, fall back to free alternatives (googletrans or similar) if not
- **Discrepancy display:** Both inline flags AND summary report section
- **Threshold:** Semantic differences only — ignore stylistic variation ('shall' vs 'will'). Only flag when meaning changes
- **Explanations:** Include brief 1-2 sentence explanation of what the semantic difference means

### Legal term handling
- **Annotation scope:** Only terms with no direct English equivalent (not every legal term — focused, meaningful annotations)
- **Depth:** Historical context when relevant — modern dictionary definition PLUS period-specific meaning when it differs from modern usage
- **Placement:** Footnote style — numbered footnotes at bottom of each clause section for clean reading flow
- **Mistranslation flagging:** Flag when a term is commonly rendered differently in English-language discussions of the same document (e.g., Wikipedia says 'nationals' but actual term is closer to 'subjects')

### Surprise clause detection
- **Narrative baseline:** User provides description of what people commonly believe the document says. Tool compares each clause against this user-provided narrative
- **Severity levels:** Three tiers — Minor (nuance difference), Notable (significant omission from common narrative), Major (directly contradicts common narrative)
- **Architecture:** Separate post-translation analysis pass — modular, can re-run without retranslating if narrative description changes
- **Script beats:** Include 1-2 sentence script suggestion per surprise clause (how to present this moment in the video). Feeds into Phase 41 scriptwriting

### Claude's Discretion
- Exact prompt engineering for translation quality
- Free translation fallback implementation (googletrans vs other libraries)
- Auto-detection algorithm for article/clause boundaries
- Output file format details (markdown structure, heading levels)

</decisions>

<specifics>
## Specific Ideas

- Clause-by-clause approach mirrors the episode structure from the format guide (Phase 39): each clause gets context setup, original text, translation, significance
- Footnote annotations keep the translation clean for split-screen display while preserving scholarly depth
- Surprise severity levels map directly to video pacing: Major surprises get the most screen time, Minor surprises can be mentioned in passing
- Script beats on surprises create a bridge to Phase 41's document-structured scriptwriting mode
- Mistranslation flagging connects legal term annotations to surprise detection — when a commonly-used English term is wrong, that's both an annotation AND a surprise

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 40-translation-pipeline*
*Context gathered: 2026-02-17*
