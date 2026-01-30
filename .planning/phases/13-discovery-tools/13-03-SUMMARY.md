---
phase: 13-discovery-tools
plan: 03
subsystem: discovery
tags: [metadata, validation, vidiq, workflow, quality-gate]
requires: [13-01]
provides: [metadata-checker, vidiq-workflow, discover-command, publish-gate]
affects: [publishing, quality-control]
tech-stack:
  added: []
  patterns: [pre-publish-validation, guided-workflow]
key-files:
  created:
    - tools/discovery/metadata_checker.py
    - tools/discovery/vidiq_workflow.py
    - .claude/commands/discover.md
  modified:
    - .claude/commands/publish.md
decisions:
  - id: DISC-03-01
    what: Use ASCII instead of Unicode for Windows console compatibility
    why: Windows console encoding (cp1252) doesn't support checkmark/cross emojis
    alternative: Could set console UTF-8 mode, but ASCII is more portable
  - id: DISC-03-02
    what: 2% keyword density threshold for stuffing detection
    why: Industry standard for SEO, YouTube penalizes excessive repetition
    alternative: Could use 3-5% but that's too lenient for quality content
  - id: DISC-03-03
    what: Manual VidIQ workflow instead of API integration
    why: VidIQ has no public API, browser automation would violate TOS
    alternative: Could scrape but that's fragile and violates terms
  - id: DISC-03-04
    what: Infer primary keyword from title if not specified
    why: Most workflows won't specify keyword explicitly
    alternative: Could require explicit keyword, but that adds friction
metrics:
  duration: 68 minutes
  completed: 2026-01-29
---

# Phase 13 Plan 03: Metadata Integration & Pre-Publish Gate

**One-liner:** Pre-publish metadata validation with keyword stuffing detection and VidIQ guided workflow

## What Was Built

### 1. Metadata Consistency Checker (`metadata_checker.py`)

Pre-publish validation tool that checks title/description/tags for consistency and quality.

**Validation checks:**
- **HIGH priority:** Primary keyword in title, description opening, keyword stuffing detection (>2%)
- **MEDIUM priority:** Primary keyword in tags, title-tag overlap (3+ words)
- **WARNING priority:** Description length (200+ words), tag count (5-30)

**Features:**
- Infers primary keyword from title if not specified
- Parses YOUTUBE-METADATA.md files
- Outputs markdown or JSON format
- CLI interface: `--file`, `--title`, `--description`, `--tags`, `--keyword`
- Windows console compatible (ASCII output, no Unicode)

**Exit codes:**
- 0 = PASS (no HIGH severity issues)
- 1 = FAIL (has HIGH severity issues)

**Location:** `tools/discovery/metadata_checker.py`

### 2. VidIQ Guided Workflow (`vidiq_workflow.py`)

Step-by-step prompts for manual VidIQ data collection.

**3-step workflow:**
1. Search Primary Keyword (volume, competition, score, trend)
2. Check Related Keywords (high volume, low competition targets)
3. Analyze Competitors (top videos with stats)

**Features:**
- Generates formatted markdown prompts
- Interactive data collection mode with `--save`
- Saves to project folder or `channel-data/vidiq-research/`
- Outputs markdown or JSON

**Why manual:** VidIQ has no public API, browser automation violates TOS

**Location:** `tools/discovery/vidiq_workflow.py`

### 3. /discover Command

Unified keyword research and validation command.

**Workflows:**
- `/discover TOPIC` - Full keyword research
- `/discover --autocomplete "phrase"` - YouTube autocomplete extraction
- `/discover --intent "query"` - Search intent classification
- `/discover --check FILE` - Pre-publish metadata validation
- `/discover --vidiq "topic"` - VidIQ guided workflow

**Flags:** `--save`, `--json`, `-q` (quiet mode)

**Location:** `.claude/commands/discover.md`

### 4. /publish Integration

Added pre-publish quality gate to `/publish` command.

**New section:** "Pre-Publish Quality Gates"
- Documents metadata consistency check requirement
- Explains HIGH/MEDIUM/WARNING priority levels
- Requires [PASS] status before publishing
- References `/discover --check` for validation

**Location:** `.claude/commands/publish.md`

## How It Works

### Pre-Publish Workflow

```bash
# 1. Generate metadata
/publish --metadata project-name

# 2. Validate metadata (quality gate)
/discover --check video-projects/_IN_PRODUCTION/project/YOUTUBE-METADATA.md

# 3. Fix issues if [FAIL]
# Edit YOUTUBE-METADATA.md

# 4. Re-check until [PASS]
/discover --check YOUTUBE-METADATA.md

# 5. Upload to YouTube
```

### Keyword Research Workflow

```bash
# 1. Extract autocomplete suggestions
/discover --autocomplete "medieval history"

# 2. Classify search intent
/discover --intent "dark ages myth"

# 3. VidIQ research
/discover --vidiq "medieval history"

# 4. Choose primary keyword
# Based on volume, competition, intent match

# 5. Generate metadata with chosen keyword
/publish --metadata project-name
```

## Technical Implementation

### Metadata Checker Algorithm

```python
1. Infer primary keyword from title (if not specified)
   - Remove stop words
   - Find longest meaningful phrase (2-4 words)
   - Prioritize earlier words

2. Check title
   - Primary keyword present? (HIGH)
   - Keyword density >30%? (HIGH - stuffing)

3. Check description
   - Primary keyword in first 200 chars? (HIGH)
   - Keyword density >2%? (HIGH - stuffing)
   - Word count <200? (WARNING)

4. Check tags
   - Primary keyword present? (MEDIUM)
   - Tag count 5-30? (WARNING)

5. Calculate title-tag overlap
   - Extract meaningful words (no stop words)
   - Count overlap
   - <3 words = MEDIUM issue

6. Generate report
   - Passed = no HIGH issues
   - Failed = has HIGH issues
   - Group issues by severity
```

### VidIQ Workflow Structure

```python
# Step 1: Primary Keyword
prompts = {
  'instructions': [...],
  'data_points': [
    {'field': 'search_volume', 'label': 'Search Volume', ...},
    {'field': 'competition', 'label': 'Competition Score', ...},
    ...
  ]
}

# Step 2: Related Keywords
# Step 3: Competitor Analysis

# Format as markdown or JSON
# Save collected data to project folder
```

## Verification Results

✅ **All success criteria met:**

1. **Metadata checker identifies consistency issues**
   - Tested: Missing keyword, keyword stuffing, tag overlap
   - Result: All issues detected correctly

2. **Keyword stuffing detected (>2% density flagged)**
   - Tested: 40% density in title and description
   - Result: HIGH severity issues flagged, exit code 1

3. **VidIQ workflow generates clear step-by-step prompts**
   - Tested: `python vidiq_workflow.py "medieval history"`
   - Result: Formatted markdown with 3 steps, data points, examples

4. **/discover command documented with all flags**
   - Created: `.claude/commands/discover.md` (501 lines)
   - Includes: Usage, flags, workflows, examples, integration

5. **/publish includes metadata check as pre-publish gate**
   - Updated: `.claude/commands/publish.md`
   - Added: "Pre-Publish Quality Gates" section before metadata generation
   - Documents: Validation requirements, [PASS]/[FAIL] process

6. **All tools output markdown by default, JSON with --json flag**
   - metadata_checker.py: `--json` flag implemented
   - vidiq_workflow.py: `--json` flag implemented
   - Default: Formatted markdown

## Files Created/Modified

**Created:**
- `tools/discovery/metadata_checker.py` (448 lines)
- `tools/discovery/vidiq_workflow.py` (335 lines)
- `.claude/commands/discover.md` (501 lines)

**Modified:**
- `.claude/commands/publish.md` (+29 lines)

**Total:** 1,313 lines of code/documentation

## Integration Points

### With Existing Systems

**13-01 (Keyword Database):**
- Metadata checker can use keyword database for frequency data
- VidIQ workflow saves to same database schema
- Autocomplete + intent classification feed into metadata validation

**Publishing Workflow:**
- /publish now requires metadata validation
- /discover provides keyword research before /publish
- Quality gate prevents publishing with inconsistent metadata

**Analytics (Phase 7-10):**
- Future: Compare predicted keywords vs actual traffic sources
- Track which keywords drove views
- Refine keyword selection based on performance

### With External Tools

**VidIQ:**
- Guided workflow for manual data collection
- No API dependency (manual input)
- Saves data for future reference

**YouTube:**
- Metadata format matches YouTube requirements
- Description length/tag count aligned with YouTube best practices
- Keyword density thresholds prevent YouTube spam penalties

## Next Phase Readiness

**Phase 13-02 (Search Intent Classification):**
- Metadata checker references `intent_mapper.py` but handles missing gracefully
- Ready to integrate when 13-02 completes
- Will enhance metadata validation with intent matching

**Phase 14 (NotebookLM Workflow):**
- Keyword research informs source selection
- Metadata validation ensures research findings reach discovery
- VidIQ competitor analysis identifies content gaps

## Known Issues

**None.** All functionality working as specified.

**Improvements for future:**
- Add intent matching to metadata checker (requires 13-02)
- Track metadata check results over time (which issues are common?)
- Compare VidIQ predictions vs actual performance

## Deviations from Plan

**None.** Plan executed exactly as written.

**Minor adjustments:**
- Changed Unicode emojis to ASCII for Windows compatibility (DISC-03-01)
- Improved error handling for missing fields in metadata files

## Usage Examples

### Example 1: Pre-Publish Validation

```bash
# Check existing metadata file
cd tools/discovery
python metadata_checker.py --file "../../video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025/YOUTUBE-METADATA.md"

# Result: [PASS] or [FAIL] with specific issues
# Fix issues, re-run until [PASS]
```

### Example 2: Keyword Research

```bash
# Generate VidIQ prompts
cd tools/discovery
python vidiq_workflow.py "medieval history" --project-folder "../../video-projects/_IN_PRODUCTION/19-flat-earth-medieval-2025"

# Collect data manually in VidIQ
# Save results
python vidiq_workflow.py "medieval history" --save
```

### Example 3: Quick Metadata Check

```bash
# Check from command line (no file)
cd tools/discovery
python metadata_checker.py --title "Medieval History Facts" --description "This video explores medieval history..." --tags "medieval,history,facts" --keyword "medieval history"
```

## Lessons Learned

**1. Windows console encoding is a real constraint**
- Unicode emojis don't work in default Windows console
- ASCII alternatives are more portable
- Consider this for all CLI tools

**2. Manual workflows can be valuable**
- VidIQ has no API, but guided prompts are useful
- Step-by-step instructions reduce errors
- Structured data collection enables future analysis

**3. Pre-publish gates catch issues early**
- Metadata validation before upload prevents mistakes
- Better to catch keyword stuffing in tool than after YouTube penalizes
- Quality gates force good practices

**4. Inferred defaults reduce friction**
- Auto-inferring primary keyword from title saves time
- Most users won't specify keyword explicitly
- Heuristics work well for common cases

## Performance

**Execution time:** 68 minutes
- Task 1 (metadata checker): 25 min
- Task 2 (VidIQ workflow): 18 min
- Task 3 (/discover command + /publish update): 25 min

**Efficiency:** On track for phase completion

## Related Documentation

- **Phase 13-01 Summary:** Keyword extraction foundation
- **Phase 13-02 Plan:** Search intent classification (parallel)
- **/discover command:** `.claude/commands/discover.md`
- **/publish command:** `.claude/commands/publish.md`
- **VidIQ filter:** `.claude/REFERENCE/VIDIQ-CHANNEL-DNA-FILTER.md`
