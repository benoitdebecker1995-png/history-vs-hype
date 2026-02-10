# Phase 34: NotebookLM Research Bridge - Context

**Gathered:** 2026-02-10
**Status:** Ready for planning

<domain>
## Phase Boundary

CLI tools and reference documents that bridge the gap between topic selection and NotebookLM research sessions. Three capabilities: (1) generate academic source lists for a topic, (2) extract structured citations from NotebookLM chat output, (3) provide optimized prompts for NotebookLM fact extraction. No NotebookLM API automation — tool-assisted manual workflow.

</domain>

<decisions>
## Implementation Decisions

### Source List Generation (NLMB-01)
- **Source of recommendations:** Claude API generation (no web search dependency) — fast, reliable, leverages Claude's training data on academic publishing
- **Output format:** Standalone `NOTEBOOKLM-SOURCE-LIST.md` file written to the project folder — serves as shopping/download checklist
- **Detail level:** Full academic citation per entry — title, author, publisher, year, ISBN, edition, estimated price, suggested purchase link (Amazon/publisher)
- **Organization:** By priority tier (Tier 1: must-have primary sources, Tier 2: key secondary, Tier 3: supplementary) — matches existing fact-checking source hierarchy

### Citation Extraction (NLMB-02)
- **Input method:** User copies NotebookLM chat text into a `.txt` or `.md` file, tool reads the file — reliable, cross-platform, no clipboard dependencies
- **Output format:** Separate extraction file (`NOTEBOOKLM-EXTRACTIONS.md`) for review — user manually moves verified items to VERIFIED-RESEARCH.md (preserves review step, protects single source of truth)
- **Citation format:** Match existing VERIFIED-RESEARCH.md format (claim + source + page number + verification status) — seamless pipeline integration
- **Citation marker handling:** Claude's discretion — NotebookLM output format varies, tool should parse what's reliably available

### Prompt Library (NLMB-03)
- **Delivery:** Claude's discretion on static templates vs CLI-generated prompts — pick based on complexity vs value tradeoff
- **Specialization:** Claude's discretion on whether to specialize by video type (territorial, ideological, fact-check) or keep generic
- **Research phases covered:** Claude's discretion on full pipeline (5 steps) vs core 3 (claim verification, quote extraction, counter-evidence)
- **NotebookLM features:** Claude's discretion on whether to include Audio Overview and Interactive Mode prompts

### Workflow Integration
- **Source list command:** Claude's discretion on which existing command to extend (`/sources --recommend` or `/research --sources`)
- **Citation extraction command:** Claude's discretion on placement (`/sources --extract` or `/verify --extract-nlm`)
- **Prompt access:** Claude's discretion on reference doc vs command vs both
- **Implementation approach:** Claude's discretion on Python modules in `tools/` vs reference docs + skill updates — pick what delivers the three requirements most reliably

### Claude's Discretion
- Prompt library delivery mechanism (static vs dynamic)
- Prompt specialization level (by video type vs generic)
- Research phase coverage depth
- Audio Overview prompt inclusion
- Command placement for all three capabilities
- Implementation approach (code vs reference docs)
- Citation marker parsing strategy

</decisions>

<specifics>
## Specific Ideas

- Source list should match the existing Tier 1/2/3 source hierarchy from `.claude/REFERENCE/fact-checking-protocol.md`
- Citation extraction must produce output compatible with VERIFIED-RESEARCH.md format (the single source of truth pattern)
- The existing Phase 14 (NotebookLM Workflow, v1.2) already created `NOTEBOOKLM-SOURCE-STANDARDS.md` — Phase 34 builds on top of that, not replacing it
- Research synthesis from v2.0 planning identified: `notebooklm_bridge.py` (~300 LOC) and `citation_extractor.py` (~200 LOC) as potential modules
- markitdown library (Microsoft) identified in research as useful for document-to-markdown conversion

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 34-notebooklm-research-bridge*
*Context gathered: 2026-02-10*
