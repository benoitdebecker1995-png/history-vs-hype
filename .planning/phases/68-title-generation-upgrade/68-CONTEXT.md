# Phase 68: Title Generation Upgrade - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Upgrade `/publish --titles` so title candidates are grounded in the script's actual specific material (numbers, documents, contradictions, entities), versus-format variants are auto-generated when competing entities are detected, and all candidates are scored/ranked with data-driven penalties rather than blind rejection. Covers TITLE-01, TITLE-02, TITLE-03.

</domain>

<decisions>
## Implementation Decisions

### Script Extraction Strategy
- **Full script scan** — scan entire script (not just opening) for title raw material
- **All four material types extracted:** specific numbers, document/treaty names, named contradictions (myth vs reality pairs), and named entities (people, places)
- **Priority ranking:** frequency + position weighting (mention count, bonus for appearing in opening/closing)
- **Input types:** both markdown scripts AND SRT subtitle files (some videos only have SRT when retitling post-publish)
- EntityExtractor from metadata.py already extracts people/places/documents — reuse and extend

### Versus Auto-Detection
- **Trigger:** entities + explicit conflict markers — two named entities co-occurring with conflict language ("against", "disputed", "competed", "rivalry", "divided", "vs", etc.)
- **Entity types:** any named entities in opposition (countries, people, organizations, ideologies), not limited to countries
- **Multi-entity handling:** Claude's discretion — pick strongest pair or generate multiple versus variants based on signal strength
- **Myth vs reality as versus:** Claude's discretion — determine case by case whether myth/reality opposition warrants versus framing
- **Versus weight in output:** Claude's discretion — weight versus prominence based on how strong the versus signal is (weak signal = one option among equals; strong signal = primary recommendation)

### Rejection Filters (SC3 REINTERPRETED)
- **NOT blind pattern-matching** — SC3 reinterpreted as data-driven scoring, not hiding
- **All candidates shown** — titles with year/colon/the_x_that/question patterns get heavy score penalties and appear last with warning labels, but ARE shown to user
- **Score via title_scorer** — existing Phase 67 penalties (-50 for year, -50 for colon, -50 for the_x_that) serve as ranking signal, not as hide signal
- **Penalized candidates show warning** — e.g., "⚠️ #7 penalized: year in title (-15 CTR impact)"
- **Philosophy:** intelligently learn what works, don't blindly reject because a pattern failed once. Data informs ranking, user makes final call

### Candidate Generation
- **Volume:** Claude's discretion based on script richness — more specific material = more candidates, thin script = fewer
- **Pattern types actively generated:** versus (when detected), declarative (always at least one), how/why, curiosity/paradox, plus any other angle that could get views
- **Every candidate auto-scored** — run through score_title() with --db and --topic before display
- **Output format:** ranked list with scores (replaces A/B/C table)
  - Each entry shows: rank, title, score, grade, pattern type
  - Penalized titles show warning explaining the penalty
  - Variable length — show whatever was generated, ranked best to worst

### Claude's Discretion
- Number of candidates to generate (proportional to script material richness)
- Versus weight in ranking (based on signal strength)
- Multi-entity pair selection strategy
- Myth vs reality versus framing (case by case)
- Internal generation algorithm (template-based, LLM-assisted, or hybrid)

</decisions>

<specifics>
## Specific Ideas

- Output format preview (from discussion):
  ```
  ## Title Candidates (ranked by score)

  | # | Title | Score | Grade | Pattern |
  |---|-------|-------|-------|---------|
  | 1 | Spain vs Portugal: Who Really Owned... | 78 | B+ | versus |
  | 2 | How Two Countries Divided the World | 71 | B | how_why |
  | 3 | The Pope Drew a Line Across the Ocean | 68 | B- | declarative |
  | 4 | Why Brazil Speaks Portuguese | 55 | C | how_why |

  ⚠️ #4 penalized: year pattern (-15 CTR impact)
  ```
- User philosophy: "intelligently learn what works and what doesn't, don't blindly reject everything just because it didn't work once"
- SRT support enables retitling workflow (/retitle from Phase 60) to use the same generation pipeline

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tools/production/metadata.py`: `MetadataGenerator._generate_title_variants()` — current 3-variant generation (mechanism, document, paradox). Template-based, uses EntityExtractor output. Needs upgrade, not replacement
- `tools/production/entities.py`: `EntityExtractor` — already extracts people, places, documents with mention counts. Reusable for title material extraction
- `tools/production/parser.py`: `ScriptParser` — parses markdown scripts into sections. Reusable for full-script scanning
- `tools/title_scorer.py`: `score_title()` — Phase 67 recalibrated scorer with niche benchmarks, topic-type grading, pattern detection, hard reject penalties. Use for auto-scoring all candidates
- `tools/title_scorer.py`: `detect_pattern()`, `has_year()`, `has_specific_number()`, `has_active_verb()` — reusable detection functions
- `tools/benchmark_store.py`: `TOPIC_GRADE_THRESHOLDS`, `get_niche_score()`, `load()` — niche benchmark data access

### Established Patterns
- `PATTERN_SCORES` dict + `db_enriched`/`niche_enriched` layering — score override pattern from Phase 67
- `CLICKBAIT_PATTERNS` list in metadata.py — tone filter for documentary channel (reconciliation with title_scorer deferred to Phase 70)
- EntityExtractor returns entities with `.mentions` count and `.entity_type` — direct input for frequency-based prioritization

### Integration Points
- `/publish --titles` command → calls MetadataGenerator → output goes to YOUTUBE-METADATA.md
- `score_title()` → called per candidate with db_path and topic_type for full scoring
- SRT parsing → existing subtitle fix workflow has SRT readers; need to wire into title generation input
- `/retitle` pipeline (Phase 60) → could benefit from same generation engine for retitling candidates

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 68-title-generation-upgrade*
*Context gathered: 2026-03-17*
