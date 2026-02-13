# Architecture Research: v3.0 Adaptive Scriptwriter Integration

**Domain:** Adding adaptive learning to existing YouTube content production workspace
**Researched:** 2026-02-12
**Confidence:** HIGH (full codebase context)

---

## Integration Context

**Problem:** script-writer-v2 generates good scripts but doesn't improve over time. The creator significantly edits every script (V4→V5 type changes), but those edits are lost — the next script starts from zero. Voice patterns (Part 6) are static, creator transcripts sit unused in `transcripts/`, and retention science is in analytics tools but not in the scriptwriter.

**Solution:** Close the feedback loop. Make every edit teach the system. Make every transcript enrich the technique library. Make retention science prescriptive, not just diagnostic.

---

## Existing Architecture Map

```
Claude Code CLI
  ├── /script command
  │     └── Spawns script-writer-v2 agent (Opus)
  │           ├── Reads: STYLE-GUIDE.md (Parts 1-7)
  │           ├── Reads: 01-VERIFIED-RESEARCH.md
  │           ├── Reads: Opening/Closing templates
  │           ├── Reads: Pre-script intelligence (topic_strategy + feedback)
  │           └── Writes: 02-SCRIPT-DRAFT.md
  │
  ├── /verify command
  │     └── Spawns fact-checker agent
  │
  ├── /analyze command
  │     ├── retention_mapper.py (maps drops to sections)
  │     ├── section_diagnostics.py (diagnoses drops, recommends Part 6 patterns)
  │     └── topic_strategy.py (aggregate performance by topic type)
  │
  ├── tools/script-checkers/
  │     ├── pacing_checker.py
  │     ├── repetition_checker.py
  │     ├── flow_checker.py
  │     └── scaffolding_checker.py
  │
  └── transcripts/ (80+ files, unused by scriptwriter)
```

---

## v3.0 Architecture Additions

### New Module: `tools/script-analysis/`

```
tools/script-analysis/
  ├── __init__.py
  ├── transcript_analyzer.py    # Parse and extract techniques from creator transcripts
  ├── edit_tracker.py           # Compare script versions, classify edits, build preferences
  ├── preferences.json          # Accumulated preference model (human-readable)
  └── technique_library.py      # Query and manage creator technique database
```

### Modified Components

| Component | Change | Purpose |
|-----------|--------|---------|
| `.claude/agents/script-writer-v2.md` | Add Rules 15-17 | Variant mode, preference injection, technique awareness |
| `.claude/REFERENCE/STYLE-GUIDE.md` | Add Part 8 | Creator Techniques (extracted from transcript analysis) |
| `/script` skill | Add `--variants` flag | Trigger variant generation mode |
| `/script` skill | Add preference injection | Auto-read preferences.json before spawning agent |
| analytics.db | New tables (v28) | script_edits, script_choices, creator_techniques |

### Data Flow: Complete Loop

```
PHASE A: Build Knowledge Base (Run Once, Update Periodically)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

transcripts/Kraut/*.txt ──┐
transcripts/Shaun/*.txt ──┤
transcripts/KnowingBetter/ ┼──→ transcript_analyzer.py ──→ creator_techniques (DB)
transcripts/AlexOConnor/ ──┤                                    │
transcripts/*.srt (own) ──┘                                    ▼
                                                     STYLE-GUIDE.md Part 8
                                                     (Creator Techniques)

retention_mapper.py data ──┐
section_diagnostics.py ────┼──→ Retention Rules Doc ──→ STYLE-GUIDE.md Part 9
channel retention curves ──┘                            (Retention Playbook)


PHASE B: Generate Script (Every Video)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/script --variants
    │
    ├── Read: preferences.json (learned preferences)
    ├── Read: STYLE-GUIDE.md Parts 6, 8, 9 (patterns + techniques + retention)
    ├── Read: 01-VERIFIED-RESEARCH.md (facts)
    ├── Read: Pre-script intelligence (topic strategy + feedback)
    │
    ▼
script-writer-v2 (with Rules 15-17)
    │
    ├── OUTPUT 1: 2-3 hook variants + 2 structure options
    │               └── User picks → logged to script_choices (DB)
    │
    └── OUTPUT 2: Full script draft (V1)
                    └── Saved as 02-SCRIPT-DRAFT.md


PHASE C: Learn From Edits (After User Edits)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

02-SCRIPT-DRAFT.md (V1, generated)
        │
        ├── User edits to V2, V3... Vn
        │
        ▼
edit_tracker.py compare V1 Vn
        │
        ├── Line-level diff (difflib)
        ├── Edit classification (Claude API)
        │     ├── tone_change: "removed staccato fragment"
        │     ├── accuracy_fix: "changed source attribution"
        │     ├── voice_preference: "softened transition"
        │     ├── structural: "moved section"
        │     └── content_cut: "trimmed redundant closing"
        │
        ├── Log to: script_edits (DB)
        │
        └── If 3+ consistent edits of same type:
              └── Promote to preferences.json
                    └── Next /script generation reads updated preferences
```

---

## Preference Model Design

### preferences.json Structure

```json
{
  "version": 1,
  "last_updated": "2026-02-12",
  "confirmed_preferences": [
    {
      "id": "pref-001",
      "type": "voice",
      "rule": "Avoid staccato informational fragments",
      "examples": [
        {"avoid": "They found waves. Deep blue water. Nothing.", "prefer": "They came back with nothing."},
        {"avoid": "Population: 4.5M. GDP: $2.1B.", "prefer": "Somaliland has a population of 4.5 million and a GDP of $2.1 billion."}
      ],
      "confidence": "high",
      "source_edits": 5,
      "first_seen": "2026-01-15",
      "last_seen": "2026-02-12"
    }
  ],
  "candidate_preferences": [
    {
      "id": "cand-001",
      "type": "tone",
      "rule": "Replace colons with natural sentences for spoken delivery",
      "examples": [
        {"avoid": "Official cause: mechanical failure", "prefer": "The official cause was mechanical failure"}
      ],
      "confidence": "low",
      "source_edits": 1,
      "first_seen": "2026-02-12"
    }
  ],
  "choice_patterns": {
    "opening_hook": {"document_first": 3, "stakes_immediate": 2, "both_extremes": 1},
    "structure": {"payoff_first": 4, "chronological": 1, "dual_timeline": 0}
  }
}
```

### Confidence Levels

| Level | Criteria | Agent Behavior |
|-------|----------|---------------|
| **high** | 3+ consistent edits across different scripts | Apply automatically |
| **medium** | 2 consistent edits | Apply but note in metadata |
| **low** | 1 edit (candidate) | Don't apply — wait for confirmation |

---

## Agent Prompt Additions

### Rule 15: Preference-Aware Generation

```markdown
### RULE 15: LEARNED PREFERENCES (v3.0)

Before writing, read `preferences.json` (provided as context).

**For each "confirmed" preference (high confidence):**
- Apply automatically during writing
- Note in VOICE PATTERNS APPLIED metadata

**For "candidate" preferences (low/medium):**
- Consider but don't force
- If naturally applicable, use it

**Never override:** Rules 1-14 take priority over learned preferences.
Accuracy (Rule 1) > Voice preference (Rule 15).
```

### Rule 16: Variant Generation Mode

```markdown
### RULE 16: VARIANT GENERATION (v3.0)

When `--variants` flag is set:

**Step 1: Generate Options (before full script)**

Output a CHOICES section:

## HOOK VARIANTS

**A. [Hook Type Name]**
> [2-3 sentence hook text]

**B. [Hook Type Name]**
> [2-3 sentence hook text]

**C. [Hook Type Name]** (if applicable)
> [2-3 sentence hook text]

## STRUCTURE OPTIONS

**Option 1: [Structure Name]**
[Brief outline of act structure]

**Option 2: [Structure Name]**
[Brief outline of act structure]

---
Pick your hook (A/B/C) and structure (1/2), then I'll write the full script.

**Step 2: Write full script using chosen options**
```

### Rule 17: Creator Technique Awareness

```markdown
### RULE 17: CREATOR TECHNIQUES (v3.0)

Read STYLE-GUIDE.md Part 8 (Creator Techniques) for proven patterns
extracted from top-performing YouTube creators.

**When writing each section, consider:**
- Does a proven creator technique fit this moment?
- Has this technique been correlated with high retention?
- Is it compatible with the channel voice?

**Note in metadata:** Which creator techniques were applied.
```

---

## Build Order (Dependency-Aware)

```
Phase 36: Retention Science Foundation
  ├── Synthesize retention data into prescriptive rules
  ├── Create STYLE-GUIDE.md Part 9 (Retention Playbook)
  └── No code needed — reference doc update + agent rule

Phase 37: Creator Transcript Analysis
  ├── Build transcript_analyzer.py
  ├── Analyze 80+ transcripts
  ├── Create creator_techniques DB table
  ├── Create STYLE-GUIDE.md Part 8 (Creator Techniques)
  └── Depends on: nothing (can run in parallel with 36)

Phase 38: Structured Choice Architecture
  ├── Add Rule 16 to script-writer-v2
  ├── Create script_choices DB table
  ├── Modify /script skill for --variants flag
  └── Depends on: 36 + 37 (choices should reference techniques)

Phase 39: Edit-Based Learning Loop
  ├── Build edit_tracker.py
  ├── Create script_edits DB table
  ├── Create preferences.json
  ├── Add Rule 15 to script-writer-v2
  ├── Build preference promotion logic
  └── Depends on: 38 (needs scripts being generated to track edits)
```

---

## Integration Points with Existing System

| Existing Component | Integration |
|-------------------|-------------|
| `/script` skill | Add `--variants` flag, preference injection |
| script-writer-v2 agent | Add Rules 15-17, read preferences.json |
| STYLE-GUIDE.md | Add Parts 8 (Techniques) and 9 (Retention Playbook) |
| analytics.db | Add 3 new tables (migration v28) |
| section_diagnostics.py | Feed retention patterns to Part 9 |
| retention_mapper.py | Feed retention data to Part 9 |
| transcripts/ folder | Input for transcript_analyzer.py |
| Rule 13 (auto-capture) | Subsumed by Rule 15 (broader preference system) |

---

*Researched: 2026-02-12 for v3.0 Adaptive Scriptwriter milestone*
