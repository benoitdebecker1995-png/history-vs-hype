# Phase 24 Context: Edit Guide Generation

## Phase Goal
User can generate timing-aware edit guide with B-roll markers

## Requirements
- EDIT-01: Section durations at 150 WPM
- EDIT-02: Inline B-roll markers in script output
- EDIT-03: Timing sheet with cumulative times

## Decisions

### 1. Duration Calculation

**Decision:** Use 150 WPM as standard conversion rate (industry standard for spoken delivery)

**Implementation:**
- Calculate `section_duration_seconds = (word_count / 150) * 60`
- Round to nearest second for display
- Exclude B-roll markers from word count (use existing Section.word_count which already strips markers)

**Edge cases:**
- Very short sections (<30 words): Show minimum 10 seconds
- Very long sections (>1000 words): No maximum, but flag for pacing review

---

### 2. Shot-by-Shot Format

**Decision:** Match existing EDITING-GUIDE.md format exactly

**From existing guides (Chagos, Flat Earth), each shot includes:**
```markdown
#### SHOT {N}: {TALKING HEAD|B-ROLL} - {description} ({start_time} - {end_time})
**SRT #{start}-{end}** | **Duration: {X} sec**

> "{transcript quote}"

**VISUAL:** {description}

**WHY {TALKING HEAD|B-ROLL}:** {justification}

**CAMERA NOTES:** {delivery guidance or "N/A (B-roll)"}

**SOURCES:** (for B-roll only)
- {source 1}
- {source 2}

**CREATE IN:** {tool suggestion} (for B-roll only)
```

**Key patterns:**
- Group shots by sections (e.g., "[SECTION 1: THE HOOK]")
- Each section has purpose statement
- Duration comes from estimated word count (Phase 24), not SRT timestamps (post-filming)

---

### 3. Timing Accumulation

**Decision:** Track cumulative times at section level

**Format:**
```markdown
### [SECTION 1: THE HOOK] (0:00 - 1:15)
```

**Implementation:**
- Calculate cumulative start time by summing all previous sections
- Format as MM:SS
- Section end time = start time + section duration
- Running total displayed in header metadata

**Running time display:**
```markdown
**Total Runtime:** ~{minutes}:{seconds} (estimated at 150 WPM)
```

---

### 4. Output Structure

**Decision:** Generate complete EDITING-GUIDE.md matching existing format

**Sections to generate:**
1. Header metadata
2. Editing philosophy (reuse standard text)
3. Shot-by-shot breakdown
4. Visual assets checklist (derived from B-roll shots)
5. Retention optimization schedule
6. Quality checklist (template)
7. Change log entry

**What Phase 24 generates vs manual:**
- **Automated:** Header, shot-by-shot, timing calculations, asset checklist structure
- **Manual:** SRT corrections (requires actual recording), camera notes refinement, source verification

---

### 5. B-Roll Integration

**Decision:** Derive B-roll markers from Phase 23 shot list

**Integration flow:**
1. ScriptParser provides sections
2. EntityExtractor provides entities per section
3. BRollGenerator provides shots with section_references
4. EditGuideGenerator:
   - Maps shots to sections
   - Assigns shot numbers sequentially
   - Generates "WHY B-ROLL" from entity type and priority
   - Generates "SOURCES" from shot.source_urls

**Shot type classification:**
- Sections with entity mentions → B-ROLL shot
- Sections without entities → TALKING HEAD shot
- Default talking head ratio: 60-65% (documentary style)

---

### 6. Dependencies Available

**From Phase 22:**
- `ScriptParser.parse_file()` → List[Section] with word_count
- `EntityExtractor.extract_from_sections()` → List[Entity]
- `Section.word_count` → already excludes B-roll markers

**From Phase 23:**
- `BRollGenerator.generate()` → List[Shot] with section_references
- `Shot.visual_type`, `Shot.priority`, `Shot.source_urls`, `Shot.diy_instructions`

---

## Out of Scope (Deferred)

- SRT file parsing (post-filming tool, different workflow)
- Automatic camera notes generation (requires AI understanding of emotional beats)
- Pattern interrupt detection (covered by retention schedule template)
- Video length estimation beyond word count (doesn't account for pauses, B-roll holds)

---

## Files to Create

- `tools/production/editguide.py` - EditGuideGenerator class
- Update `tools/production/__init__.py` - export EditGuideGenerator
- Update `tools/production/parser.py` - add `--edit-guide` CLI flag

---

*Context captured: 2026-02-04*
