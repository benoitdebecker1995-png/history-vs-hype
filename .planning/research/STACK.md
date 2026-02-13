# Stack Research: v3.0 Adaptive Scriptwriter

**Domain:** YouTube scriptwriting with creator voice learning, retention science, and adaptive feedback
**Researched:** 2026-02-12
**Confidence:** HIGH (based on existing codebase analysis + domain knowledge)

---

## Executive Summary

v3.0 adds adaptive intelligence to an existing script-writer-v2 agent (1284-line prompt, 14 rules). The key constraint: the scriptwriter is a **Claude Code agent** (prompt-based), not a traditional ML model. "Learning" means evolving the prompt context and reference documents, not training weights.

**Stack additions needed:** Minimal. The existing Python + SQLite + Claude API stack handles everything. The main work is data pipeline design, not new libraries.

---

## What Already Exists (DO NOT Add)

| Capability | Location | Status |
|-----------|----------|--------|
| Python 3.11-3.13 | tools/ (~20K LOC) | Working |
| SQLite with auto-migration | keywords.db, analytics.db (PRAGMA user_version=27) | Working |
| Claude API (Anthropic SDK) | notebooklm_bridge.py | Working |
| Script quality checkers | tools/script-checkers/ (~3,200 LOC) | Working |
| Voice fingerprinting (basic) | Part of v1.2 | Working (but underused) |
| 29 voice patterns | STYLE-GUIDE.md Part 6 | Working |
| script-writer-v2 agent | .claude/agents/script-writer-v2.md (1284 lines) | Working |
| SRT transcript parsing | srt library | Available |
| Feature flags | VARIANTS/BENCHMARKS/FEEDBACK/DIAGNOSTICS_AVAILABLE | Pattern established |

---

## New Stack Needed

### 1. Transcript Analysis Pipeline

**What:** Parse creator transcripts, extract structural patterns (pacing, hooks, transitions)

**Libraries needed:**
- `difflib` (stdlib) — For edit-based comparison between script versions
- `srt` (already installed) — Parse SRT transcripts
- `re` (stdlib) — Pattern extraction from transcript text

**Rationale:** No new external libraries needed. Transcripts are already in `transcripts/` as `.srt`, `.vtt`, and `.txt` files (80+ files). The analysis is text processing — word counts, sentence length distributions, section timing, pattern matching. Python stdlib handles this.

**Integration:** New module `tools/script-analysis/transcript_analyzer.py`

### 2. Edit Delta Capture

**What:** Compare generated script (V1) with user's edited version (V5) and extract patterns

**Libraries needed:**
- `difflib.SequenceMatcher` (stdlib) — Line-level and word-level diff
- `json` (stdlib) — Preference storage format

**Rationale:** The edit deltas are text diffs. `difflib` provides unified diffs and similarity ratios. No NLP library needed — the deltas are small enough that Claude API can classify them (e.g., "removed staccato fragment" or "softened transition").

**What NOT to add:** spaCy, NLTK, or any heavy NLP library. The classification of edit types should use Claude API (already available) rather than local NLP. Keeps stack simple.

**Integration:** New module `tools/script-analysis/edit_tracker.py`

### 3. Preference Model Storage

**What:** Store learned preferences, edit patterns, and creator technique analyses

**Options evaluated:**

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| SQLite tables | Consistent with existing pattern, queryable | May be over-structured for flexible preferences | **Use for structured data** |
| JSON files | Human-readable, easy to edit, version-controllable | Not queryable, harder to aggregate | **Use for preference model** |
| Markdown reference docs | Already how voice patterns work (Part 6), Claude reads them directly | Not programmatically queryable | **Use for technique library** |

**Recommended hybrid:**
- **SQLite:** Edit history log (timestamp, file, diff summary, classified edit type)
- **JSON:** `tools/script-analysis/preferences.json` — Accumulated preference model (forbidden patterns, preferred patterns, weights)
- **Markdown:** Updated STYLE-GUIDE.md sections — Technique extractions from creator analysis

**Rationale:** The scriptwriter is a Claude agent that reads markdown. The most effective "learning" is updating the reference docs it reads. SQLite logs the history; JSON stores the model; markdown delivers it to the agent.

### 4. Variant Generation

**What:** script-writer-v2 generates multiple hook/structure options

**Libraries needed:** None. This is a prompt engineering change, not a code change.

**Approach:** Modify script-writer-v2 agent prompt to include a "variant generation" mode where it outputs 2-3 hook variants and 2 structural approaches before writing the full script. User picks, choice is logged.

**Integration:** Modify `.claude/agents/script-writer-v2.md` + new tracking in edit_tracker.py

---

## Database Schema Additions

```sql
-- Edit tracking
CREATE TABLE script_edits (
    id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,          -- e.g., "36-panama-canal-deconcini-2026"
    generated_version TEXT,             -- e.g., "V4"
    edited_version TEXT,                -- e.g., "V5"
    edit_type TEXT NOT NULL,            -- classified: tone, structure, accuracy, voice, cut
    original_text TEXT,
    edited_text TEXT,
    classification TEXT,                -- e.g., "removed staccato fragment"
    created_at TEXT DEFAULT (datetime('now'))
);

-- Choice tracking (for variant generation)
CREATE TABLE script_choices (
    id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,
    choice_type TEXT NOT NULL,          -- hook, structure, opening, closing
    options_offered TEXT NOT NULL,       -- JSON array of options
    option_chosen INTEGER NOT NULL,     -- index of chosen option
    created_at TEXT DEFAULT (datetime('now'))
);

-- Creator technique library
CREATE TABLE creator_techniques (
    id INTEGER PRIMARY KEY,
    creator TEXT NOT NULL,              -- e.g., "Kraut", "Knowing Better"
    technique_type TEXT NOT NULL,       -- opening, transition, evidence, pacing, closing
    technique_name TEXT NOT NULL,
    description TEXT,
    example TEXT,
    source_file TEXT,                   -- transcript file it was extracted from
    effectiveness_notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
```

**Migration:** user_version 27 → 28

---

## Architecture Summary

```
Existing:
  script-writer-v2 ← reads → STYLE-GUIDE.md Part 6 (29 patterns)

v3.0 Additions:
  transcript_analyzer.py → creator_techniques table → STYLE-GUIDE.md Part 8 (new)
  edit_tracker.py → script_edits table → preferences.json → agent prompt context
  variant mode → script_choices table → preferences.json

Flow:
  1. Analyze transcripts → extract techniques → store in DB + update markdown
  2. Generate script with variants → user picks → log choice
  3. User edits script → compare versions → classify edits → update preferences
  4. Next script generation reads updated preferences + techniques
```

---

## What NOT to Add

| Temptation | Why Not |
|-----------|---------|
| spaCy/NLTK for NLP | Overkill — Claude API does better classification than local NLP |
| ML model for preference learning | Too complex for solo creator workflow, small dataset |
| Vector database for embeddings | No similarity search needed — preferences are explicit rules |
| Web scraping for competitor analysis | Already have 80+ transcripts, manual download is fine |
| Real-time editing integration | Out of scope — compare versions after editing, not during |

---

## Total New Code Estimate

| Module | Estimated LOC | Purpose |
|--------|-------------|---------|
| transcript_analyzer.py | ~400-600 | Parse and analyze creator transcripts |
| edit_tracker.py | ~300-500 | Compare script versions, classify edits |
| preferences.json | ~50-100 | Accumulated preference model |
| DB migration (→v28) | ~50 | New tables |
| Agent prompt updates | ~200-300 | Variant mode, preference injection |
| STYLE-GUIDE.md additions | ~200-400 | New Part 8: Creator Techniques |

**Total:** ~1,200-2,000 lines of new code/content

---

*Researched: 2026-02-12 for v3.0 Adaptive Scriptwriter milestone*
