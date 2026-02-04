# Phase 25: Metadata Draft Generation - Context

**Gathered:** 2026-02-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Generate YouTube metadata (title candidates, description template, tags) from parsed scripts. System extracts content from existing script structure and entities, following established channel patterns. This phase creates METADATA-DRAFT.md files for publishing preparation.

Requirements:
- META-01: Extract 3-5 title candidates from script
- META-02: Generate description template with section timestamps
- META-03: Suggest 15-20 tags based on script content

</domain>

<decisions>
## Implementation Decisions

### Title Extraction

- Extract title candidates from opening hook and thesis (first 2-3 sentences)
- Generate 3 title variants (matches VidIQ A/B testing limit)
- Apply documentary tone filter — auto-reject clickbait patterns ('SHOCKING', 'You won't believe')
- Respect 60-70 character limit (mobile-friendly, per CLAUDE.md guideline)

### Description Structure

- First 2-3 lines: Script hook rephrased for reading (not speaking)
- Timestamps: Use Phase 24 edit guide cumulative times (already calculated at 150 WPM)
- Match existing YOUTUBE-METADATA.md file structure (scan existing files for section headers)
- Include sources section: Auto-list key documents, treaties, books from script entities

### Tag Generation

- Primary source: Channel patterns + script entities
- Blend entity names with tags from existing successful videos
- Generate 15-20 tags (per CLAUDE.md guideline)
- Format: Comma-separated, ready to paste into YouTube
- Priority: Entity names first (places, people, documents), then broader topics

### Output Format

- Match existing YOUTUBE-METADATA.md file structure exactly
- Output file name: METADATA-DRAFT.md (indicates draft status)
- Include [PLACEHOLDER] markers for sections needing manual completion
- CLI flag: `--metadata` (parser.py script.md --metadata)

### Claude's Discretion

- Exact title phrasing within documentary tone constraints
- How to detect and extract "hook" vs other content
- How to identify which entities qualify as "key" for sources section
- Specific channel pattern matching logic

</decisions>

<specifics>
## Specific Ideas

- Timestamps should come from Phase 24 EditGuideGenerator output (SectionTiming dataclass)
- Tag generation should reference existing channel patterns — may need to scan existing YOUTUBE-METADATA.md files
- Documentary tone filter should match existing VIDIQ-CHANNEL-DNA-FILTER.md rules

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 25-metadata-draft-generation*
*Context gathered: 2026-02-04*
