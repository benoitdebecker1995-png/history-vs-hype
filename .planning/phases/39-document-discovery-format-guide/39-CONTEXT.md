# Phase 39: Document Discovery & Format Guide - Context

**Gathered:** 2026-02-16
**Status:** Ready for planning

<domain>
## Phase Boundary

Tools to discover untranslated documents, verify translation gaps, assess document structure, and a reference guide defining the "Untranslated Evidence" series format. Covers requirements DISC-01 (gap verification), DISC-02 (structure assessment), DISC-03 (archive lookup), and SCPT-03 (format guide).

The translation pipeline itself (Phase 40) and integration into existing commands (Phase 41) are out of scope.

</domain>

<decisions>
## Implementation Decisions

### Document Input & Gap Verification
- Free-form query input — user describes the document naturally (e.g., "Statut des Juifs 1940" or "Bartolome de las Casas Brevisima relacion")
- Language-agnostic from the start — not limited to French
- Check all source categories: academic sourcebooks, Google Scholar + JSTOR, government/institutional sites, and general web search
- Documents qualify for the series if: (a) no full English translation exists, OR (b) existing translations are misleading/distort the original
- Partial translations or summaries do not disqualify — the bar is "no complete, faithful English translation available"

### Structure Assessment & Length Estimation
- Full outline with one-line summaries per section/article/chapter
- Must handle both structured legal documents (articles, clauses) AND longer-form historical texts (books, chapters)
- Input is document name + optional location/publication info — not necessarily a URL
- Support both full-document and excerpt-based video planning (user decides scope after seeing structure)

### Archive Lookup
- Always lead with academic/critical editions — scholarly publications first, free archive versions as supplementary
- Search all major archives: Legifrance, national archives, Wikisource, Internet Archive, Google Books, HathiTrust, Gallica (BnF), Europeana, Library of Congress
- Best available version preferred — critical editions, clean scans, scholarly reproductions over raw scans
- Build archive framework generically so new country-specific archives can be added easily
- Prefer academic editions with ISBN/purchase links alongside free archive URLs

### Series Format Guide
- Covers all four areas: episode structure template, visual/staging standards, quality bar & source rules, tone & framing rules
- Branding undecided — format guide defines the format without committing to whether it's a branded sub-series or a category
- Video length: as long as needed (same philosophy as main channel)
- Documents per video: usually one, but related documents can be grouped when they tell a connected story
- Visual specifics (split-screen layout, presenter interaction) left for later — guide establishes that split-screen is the approach without locking in exact layout
- Filming technique details deferred — guide covers structure, not specific production methods

### Claude's Discretion
- Gap verification output format and detail level
- Video length estimation approach (per-clause formula vs word count vs hybrid)
- Structure assessment output format (markdown outline vs table — adapt to document type)
- Whether to classify document types (legal code vs book vs treaty) and adapt parsing
- Whether summaries appear in English only or original + English
- Archive lookup caching/persistence strategy
- Whether to flag "interesting" clauses during structure assessment
- How to handle translation disagreements in the format guide (show contrast vs present best)
- How to handle misleading translations on screen (show bad vs correct, or just correct)
- Whether to include example video outlines in the format guide
- Format guide file location in the repo

</decisions>

<specifics>
## Specific Ideas

- De las Casas's *Brevisima relacion* mentioned as an example of a book-length source (not just legal codes) — the tool must handle whole books, not just article-by-article statutes
- Academic editions are the priority source — not just "find something free," but identify the scholarly critical edition first (e.g., Brill, Cambridge, Oxford editions)
- Two qualification scenarios for the series: genuinely untranslated documents AND documents where existing English versions distort the original meaning

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 39-document-discovery-format-guide*
*Context gathered: 2026-02-16*
