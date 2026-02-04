---
phase: 23-b-roll-generation
plan: 01
subsystem: production-tools
tags: [python, b-roll, script-parsing, entity-extraction, automation]

# Dependency graph
requires:
  - phase: 22-script-parser
    provides: ScriptParser and EntityExtractor for structured script analysis
provides:
  - BRollGenerator class that converts entities to actionable shot lists
  - Shot dataclass with visual type, priority, and source URL fields
  - Archive hierarchy by topic (holocaust, legal, medieval, colonial, general)
  - CLI integration via parser.py --broll flag
  - Markdown checklist generation matching B-ROLL-DOWNLOAD-LINKS.md format
affects: [24-asset-finder, production-pipeline, video-workflow]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Topic detection from entity keywords for archive selection
    - Priority assignment based on mention count and visual type
    - DIY instruction templates for user-created assets
    - URL generators return search URLs (safe, always valid)

key-files:
  created:
    - tools/production/broll.py
  modified:
    - tools/production/__init__.py
    - tools/production/parser.py

key-decisions:
  - "Use search URLs instead of fabricated file paths (safe, always valid)"
  - "Archive hierarchy organized by topic category for relevant source suggestions"
  - "Priority 1 threshold: 3+ mentions for documents, 5+ mentions for maps/portraits"
  - "DIY instructions for maps use MapChart.net (free, zero-budget friendly)"
  - "Visual type classification uses keyword detection (maritime, territory)"

patterns-established:
  - "Shot dataclass pattern: entity + visual_type + priority + source_urls + diy_instructions + section_references"
  - "Topic detection: Aggregate entity text, check keyword matches, return category"
  - "Priority assignment: Type-specific thresholds based on mention counts"
  - "Markdown output: Group by visual type, include DIY instructions, priority checklist at end"

# Metrics
duration: 4min
completed: 2026-02-04
---

# Phase 23 Plan 01: B-Roll Generation Summary

**BRollGenerator converts entities to shot lists with archive search URLs, priority levels, and DIY instructions - reducing B-roll planning from 2-4 hours to <30 seconds**

## Performance

- **Duration:** 4 min (237 seconds)
- **Started:** 2026-02-04T13:33:55Z
- **Completed:** 2026-02-04T13:37:53Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments
- Shot dataclass with 7 visual types (map, primary_source_document, portrait, historical_photo, timeline_graphic, strategic_map, logo_or_building)
- Archive hierarchy by topic with search URL templates (Yad Vashem for holocaust, ICJ for legal, etc.)
- BRollGenerator.generate_checklist() produces markdown matching existing B-ROLL-DOWNLOAD-LINKS.md format
- CLI integration: `python tools/production/parser.py script.md --broll` generates complete checklist
- Priority assignment (1=Critical, 2=High, 3=Nice-to-have) based on mention counts
- DIY instruction templates for MapChart.net maps, timeline graphics, quote cards

## Task Commits

Each task was committed atomically:

1. **Task 1: Create Shot dataclass and visual type classifier** - `7ed659e` (feat)
2. **Task 2: Implement source URL generator and priority assignment** - `f9b31fb` (feat)
3. **Task 3: Create BRollGenerator class and markdown output** - `df38e4f` (feat)

## Files Created/Modified
- `tools/production/broll.py` - Shot dataclass, classify_visual_type(), URL generators, BRollGenerator class
- `tools/production/__init__.py` - Added BRollGenerator and Shot to exports
- `tools/production/parser.py` - Added --broll CLI flag for checklist generation

## Decisions Made

**Use search URLs instead of fabricated file paths**
- Rationale: Search URLs are always valid, never break, safe to generate automatically
- Implementation: URL generators return archive search pages with entity as query parameter

**Archive hierarchy organized by topic category**
- Rationale: Different topics need different archive sources (Yad Vashem for holocaust, ICJ for legal)
- Implementation: detect_topic_category() checks entity keywords, selects appropriate archives
- Categories: holocaust, legal, medieval, colonial, general

**Priority thresholds**
- Documents with 3+ mentions → Priority 1
- Maps/portraits with 5+ mentions → Priority 1
- Timeline graphics/logos → Priority 2
- Everything else → Priority 3
- Rationale: High-mention items are critical to narrative, need visual support

**DIY instructions for zero-budget assets**
- Maps: MapChart.net (free, browser-based)
- Timeline graphics: Canva/PowerPoint
- Quote cards: Canva with aged paper templates
- Rationale: Users can create professional assets without budget constraints

**Visual type classification via keyword detection**
- Maritime keywords (gulf, ocean, sea, strait) → strategic_map
- Territory keywords (island, archipelago) → map
- Rationale: Context-aware classification improves asset suggestions

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

**Import path issues in CLI mode**
- Problem: Relative imports failed when running parser.py as __main__
- Solution: Added project root to sys.path in __main__ block
- Verification: CLI --broll flag works correctly

## Next Phase Readiness

**Ready for Phase 24 (Asset Finder):**
- BRollGenerator provides structured shot lists with source URLs
- Shot.source_urls field contains actionable download links
- Priority field enables automated "must-have" asset filtering

**Available for production use:**
- CLI: `python tools/production/parser.py path/to/script.md --broll > B-ROLL-CHECKLIST.md`
- Python API: `from tools.production import BRollGenerator, Shot`
- Output matches existing B-ROLL-DOWNLOAD-LINKS.md format (ready to replace manual creation)

---
*Phase: 23-b-roll-generation*
*Completed: 2026-02-04*
