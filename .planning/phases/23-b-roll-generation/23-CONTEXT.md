# Phase 23: B-Roll Generation - Context

**Gathered:** 2026-02-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Generate shot lists with source suggestions from parsed scripts. Users can see what visuals they need and where to find them. Builds on Phase 22's ScriptParser and EntityExtractor to produce actionable B-roll checklists.

**Not in scope:** Edit guide generation (Phase 24), metadata generation (Phase 25), teleprompter export (Phase 26).

</domain>

<decisions>
## Implementation Decisions

### Shot list structure
- Organize by priority tier (Priority 1: Critical → Priority 2: High Value → Priority 3: Nice to Have)
- Include both section name AND line range for each shot (maximum context for editing)
- Deduplicate shots from same entity - one entry per entity, show all section references
- Include full DIY creation instructions (Canva/PowerPoint steps, MapChart instructions, font suggestions) when applicable

### Source URL strategy
- Prioritize free sources (Wikimedia Commons, Archive.org, LOC, public domain archives)
- Include premium hints as backups (Getty, Shutterstock with licensing notes)
- Generate both actual URLs where patterns are known AND search instructions otherwise
- For maps: MapChart first (user's preferred workflow), Wikimedia as fallback
- Include topic-aware specialized archives (Colonial topics → UK National Archives; treaties → ICJ; US topics → LOC)

### Visual categorization
- Match existing B-roll file categories: Primary Source Documents, Maps, Historical Photos, Military/Institutional Imagery, etc.
- Split documents by type: Primary Sources vs Court Rulings vs Treaties
- Auto-infer visual type from entity type (Person → Portrait; Place → Map; Document → Document display)
- Places are context-dependent: City → historical photo; Region/territory → map; Maritime → strategic map

### Output format
- Match existing B-ROLL-DOWNLOAD-LINKS.md format (same headings, structure, checklist format)
- Include priority checklist at end (Priority 1/2/3 with checkboxes)
- Include header metadata: Project name, date, entity count, estimated assets needed
- Filename: B-ROLL-CHECKLIST.md (matches Phase 26 success criteria)

### Claude's Discretion
- Specific category organization within priority tiers
- Which archives to suggest for edge cases
- Exact URL patterns vs search instructions on case-by-case basis
- How verbose DIY instructions should be for each shot type

</decisions>

<specifics>
## Specific Ideas

- Output should look like existing files: `video-projects/_IN_PRODUCTION/14-chagos-islands-2025/B-ROLL-DOWNLOAD-LINKS.md` and `video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025/B-ROLL-DOWNLOAD-LINKS.md`
- MapChart.net is the preferred map creation tool (user has established workflow)
- Canva and PowerPoint are the DIY creation tools for documents/graphics
- Entity types from Phase 22: place, person, document, date, organization

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 23-b-roll-generation*
*Context gathered: 2026-02-03*
