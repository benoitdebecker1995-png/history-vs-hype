# Phase 70: Metadata & Packaging Integration - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce a metadata bundle where description, thumbnail concept, and title all reinforce the same hook element — enforced by tool output rather than manual checklist. Covers META-01 (description template enforcement), META-02 (thumbnail concept generation), META-03 (metadata coherence check). Also reconciles CLICKBAIT_PATTERNS inconsistency between metadata.py and title_scorer.py (carried from STATE.md).

</domain>

<decisions>
## Implementation Decisions

### Description Template Enforcement (META-01)
- **First sentence:** Keyword-stuffed SEO line — lead with primary search keyword + topic type, optimized for YouTube search results (not rephrased hook)
- **Source citations:** Auto-extracted from script body — parse actual academic citations (author names, book titles, page numbers) instead of [PLACEHOLDER]
- **Timestamps/chapters:** From SectionTiming (150 WPM via EditGuideGenerator) — existing _generate_chapters() pattern
- **Missing element enforcement:** Flag with ⚠️ warnings listing what's missing (e.g., "Missing: source citations, timestamps"). Output the description anyway but append warnings. Not a hard block

### Thumbnail Concept Generation (META-02)
- **Specificity level:** Script-grounded specifics — extract actual documents, maps, entities from script (reuse TitleMaterialExtractor) and name them in concepts. "Treaty of Tordesillas manuscript with red line across Atlantic" not "document on map"
- **Pattern selection:** Topic-adaptive — Claude auto-detects topic type from script, picks best 3 patterns for that topic. Not fixed to split-map/document-on-map/geo+evidence for every video
- **Validation:** Auto-check each concept via thumbnail_checker.py — show ✅/⚠️ per concept so user knows which comply with PACKAGING_MANDATE before Photoshop
- **Always 3 concepts** — pattern mix varies by topic type

### Metadata Coherence Check (META-03)
- **Hook element definition:** Shared entity/keyword — extract primary entity from title, check it appears in thumbnail concept text AND description first sentence
- **Display format:** Per-element pass/fail — show each pair (title↔thumb, title↔desc, thumb↔desc) as pass/fail with specific missing entity named
- **Trigger:** Auto after /publish — runs at end of /publish output after all sections generated
- **Title input:** Check ALL title candidates — show coherence count (3/3, 2/3, 1/3) as column in ranked table
- **Detail level:** Summary count in title table, detailed breakdown below for candidates with mismatches only
- **Ranking impact:** Annotation only — coherence does NOT influence title ranking. User sees both title score and coherence independently

### CLICKBAIT_PATTERNS Reconciliation
- **Single source:** Move CLICKBAIT_PATTERNS to title_scorer.py as authoritative source. metadata.py imports from title_scorer — delete local CLICKBAIT_PATTERNS list
- **Scope:** Clickbait filtering applies to titles only — not descriptions, tags, or thumbnail text
- **ALLOWED_ACRONYMS placement:** Claude's discretion
- **Tone unification:** Merge active_verbs (positive signal) and CLICKBAIT_PATTERNS (negative signal) into a single tone scoring system in title_scorer.py. Clickbait = negative score, active verbs = positive score, documentary tone is the net result

### Output Structure
- **File output:** Everything written to YOUTUBE-METADATA.md — including coherence check results and description warnings
- **Section order:** Titles → Description → Chapters → Tags → Thumbnail Concepts → 🔗 Coherence Check → VidIQ Research Notes [placeholder]

### /publish Flag Surface
- **Default mode:** All-in-one — running /publish with no flags generates full bundle (titles + description + chapters + tags + thumbnail concepts + coherence check)
- **Individual flags:** --titles, --thumbs, --desc still work for single-section generation
- **--topic flag:** Yes — overrides auto-detection for thumbnail pattern selection and coherence check. Consistent with Phase 67 title_scorer and Phase 69 hook_scorer

### Claude's Discretion
- Which 3 thumbnail patterns to generate per topic type
- Source citation extraction regex/heuristics
- ALLOWED_ACRONYMS placement (title_scorer.py or shared)
- SEO first-line keyword density and phrasing
- How to detect "primary entity" from title for coherence check

</decisions>

<specifics>
## Specific Ideas

- Title table with coherence column (from discussion):
  ```
  | # | Title | Score | Grade | Coherence |
  |---|-------|-------|-------|-----------|
  | 1 | Spain vs Portugal... | 78 | B+ | 3/3 ✅ |
  | 2 | How Two Countries... | 71 | B  | 2/3 ⚠️ |
  | 3 | The Pope Drew...     | 68 | B- | 1/3 ❌ |
  ```
- Coherence detail section for mismatched candidates:
  ```
  ## 🔗 Coherence Detail

  ### #2: How Two Countries...
  ✅ Title ↔ Description
  ❌ Title ↔ Thumbnail: no 'countries' in any thumbnail concept
  ✅ Thumbnail ↔ Description
  ```
- Description warnings format:
  ```
  ⚠️ MISSING ELEMENTS:
  • No source citations found in script
  • No timestamps (no SectionTiming data)
  ```
- Thumbnail concept format: script-grounded with specific visual elements named per concept, each with ✅/⚠️ from thumbnail_checker
- Unified tone scoring in title_scorer.py: clickbait patterns → negative, active verbs → positive, net = documentary tone score

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/production/metadata.py`: `MetadataGenerator` — main class to upgrade. `_generate_description()`, `_generate_chapters()`, `_generate_tags()` exist. `_generate_title_variants()` already delegates to title_generator.py
- `tools/production/title_generator.py`: `TitleMaterialExtractor` — extracts numbers, documents, contradictions, entities from scripts. Reuse for thumbnail concept material and description keyword extraction
- `tools/production/entities.py`: `EntityExtractor` — extracts people, places, documents with mention counts. Used for coherence check entity matching
- `tools/title_scorer.py`: `score_title()`, `detect_pattern()`, `has_year()`, `has_specific_number()`, `has_active_verb()` — title scoring + pattern detection. Will become the single source for CLICKBAIT_PATTERNS + tone scoring
- `tools/preflight/thumbnail_checker.py`: Text-based thumbnail concept validator (MAP_SIGNALS, FACE_SIGNALS, TEXT_OVERLAY_SIGNALS). Auto-check each generated concept
- `tools/production/synthesis_engine.py`: `_build_thumbnail_blueprint()` — existing thumbnail blueprint with color palettes and AI tool prompts. Can inform concept generation patterns

### Established Patterns
- Phase 68: `format_title_candidates()` outputs ranked table with warnings below — same pattern for coherence column + detail section
- Phase 67: `--topic` flag pattern in title_scorer CLI — reuse for /publish --topic
- Phase 69: `--title` flag pattern in hook_scorer — consistent flag naming
- `CLICKBAIT_PATTERNS` list in metadata.py (to be moved to title_scorer.py)
- `ALLOWED_ACRONYMS` list in metadata.py (placement at Claude's discretion)

### Integration Points
- `/publish` command → calls MetadataGenerator → outputs YOUTUBE-METADATA.md
- `thumbnail_checker.py` → called per generated concept for validation
- `score_title()` → called per title candidate (already wired in Phase 68)
- `TitleMaterialExtractor` → reused for thumbnail concept material extraction
- `/preflight` → reads YOUTUBE-METADATA.md for scoring — will now find richer content

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 70-metadata-packaging-integration*
*Context gathered: 2026-03-18*
