# Feature Landscape: v3.0 Adaptive Scriptwriter

**Domain:** YouTube scriptwriting with voice learning and retention optimization
**Focus:** Creator transcript analysis, edit-based learning, structured variants, retention science
**Researched:** 2026-02-12
**Confidence:** HIGH

---

## Executive Summary

Four feature categories for v3.0. The critical insight: the scriptwriter is a Claude agent reading markdown reference docs. "Making it smarter" means **better reference docs and better prompt context**, not new ML models.

---

## Feature Category 1: Creator Transcript Analysis

### Table Stakes (Must Have)
- **Structural extraction** — Parse transcripts to identify: hook type, section lengths, transition patterns, pacing rhythm (sentence length variance)
- **Technique categorization** — Classify extracted patterns into: openings, transitions, evidence presentation, rhythm, closings (matches existing Part 6 categories)
- **Searchable technique library** — Store techniques in DB with creator attribution, queryable by type

### Differentiators (Competitive Advantage)
- **Cross-creator pattern synthesis** — Identify patterns that appear across 3+ successful creators (e.g., "all top creators use first-person authority within 60 seconds")
- **Channel-specific technique matching** — Map creator techniques to History vs Hype's voice (which Kraut techniques work for this channel, which don't)
- **Retention-correlated patterns** — Cross-reference techniques with retention data (which patterns appear in videos with 35%+ retention)

### Anti-Features (Avoid)
- **Automatic style mimicry** — "Write like Kraut" button. Risk: produces generic imitation, not authentic voice.
- **Technique scoring/ranking** — Quantifying which techniques are "better" with small dataset. Too unreliable.

### Complexity: MEDIUM
- 80+ transcripts already available
- Text analysis is straightforward (word counts, sentence patterns, section identification)
- Main challenge: defining what constitutes a "technique" vs noise

### Dependencies
- Existing: transcripts/ folder (80+ files), STYLE-GUIDE.md Part 6 structure
- New: transcript_analyzer.py module

---

## Feature Category 2: YouTube Retention Science

### Table Stakes (Must Have)
- **First 30-second rules** — Bake in proven opening patterns: stakes immediate, payoff-first, evidence promise, first-person authority
- **Pattern interrupt scheduling** — Every 2-3 minutes, ensure script has: new evidence, perspective shift, modern relevance bridge, or visual change
- **Section length guardrails** — No section longer than 3 minutes without a break. Flag 4+ minute monologues.
- **Open loop mechanics** — Plant questions early, answer later. "We'll come back to why this matters."

### Differentiators
- **Retention drop prediction** — Based on existing retention_mapper.py data, identify script structural patterns that correlate with drops (already have data from published videos)
- **Section-level retention scoring** — Score each script section for predicted engagement based on: section type, length, evidence density, modern relevance proximity
- **Personalized retention model** — Use this channel's actual retention curves (not generic YouTube advice) to calibrate predictions

### Anti-Features
- **Generic YouTube guru advice** — "Use pattern interrupts!" without specifics. Must be actionable, tied to script text.
- **Clickbait optimization** — Optimizing titles/hooks at expense of documentary tone.
- **Formulaic structure** — Every video following identical template. Must preserve creative flexibility.

### Complexity: LOW-MEDIUM
- Retention mapper already exists (v2.0)
- Section diagnostics already exist (v2.0)
- Main work: synthesize existing analytics into prescriptive rules for the scriptwriter

### Dependencies
- Existing: retention_mapper.py, section_diagnostics.py, topic_strategy.py
- Existing: 29 voice patterns (Part 6) already encode some retention science
- New: Consolidate retention rules into scriptwriter-readable format

---

## Feature Category 3: Edit-Based Learning Loop

### Table Stakes (Must Have)
- **Version comparison** — Diff generated script (e.g., V4) against user's edited version (V5). Identify all changes.
- **Edit classification** — Categorize each edit: tone change, structural change, accuracy fix, voice preference, content cut, content addition
- **Preference extraction** — Convert recurring edits into rules: "User consistently removes staccato fragments" → add to forbidden patterns
- **Preference persistence** — Store preferences in a format the scriptwriter reads on next generation

### Differentiators
- **Semantic edit understanding** — Beyond "text changed": understand WHY. "User changed 'geologists were saying' to 'Mexican senators were estimating'" = accuracy fix, not voice preference. "User changed 'They found waves. Deep blue water. Nothing.' to 'They came back with nothing.'" = voice preference (anti-staccato).
- **Confidence-based application** — Only promote a preference to "always apply" after 3+ consistent edits of the same type. Single edits are "suggestions."
- **Preference dashboard** — Show user their accumulated preferences: "Based on your edits, I've learned: [list]". User can confirm, reject, or adjust.

### Anti-Features
- **Automatic application of every edit** — Some edits are content-specific, not general preferences. Must distinguish.
- **Silent preference changes** — User should always know what the system "learned" and be able to override.
- **Over-fitting to one script** — Learning from a single V4→V5 diff and applying everywhere. Need pattern across multiple scripts.

### Complexity: HIGH
- Diff generation is easy; semantic classification is hard
- Need Claude API for edit classification (not local NLP)
- Must handle edge cases: user adds content (not a "correction"), user restructures (not a line-level edit)
- Most valuable feature but most complex to get right

### Dependencies
- Existing: script-writer-v2 Rule 13 (preference auto-capture — explicit corrections only)
- New: edit_tracker.py, preferences.json, modified agent prompt
- Requires: user workflow change (save both versions for comparison)

---

## Feature Category 4: Structured Choice Architecture

### Table Stakes (Must Have)
- **Hook variants** — Generate 2-3 opening hook options before writing full script. User picks one.
- **Structure options** — For each video, propose 2 structural approaches (e.g., chronological vs payoff-first vs dual-timeline)
- **Choice logging** — Record which option user picks for each video

### Differentiators
- **Choice-informed defaults** — After 5+ videos, system knows: "user picks payoff-first structure 80% of the time" → make it default
- **Reason capture** — Ask WHY user picked option A over B. Store reasoning alongside choice.
- **Contextual recommendations** — "For territorial dispute topics, you've chosen Document-First opening 4/5 times. Recommending that here."

### Anti-Features
- **Too many options** — 5+ variants creates decision fatigue. Max 3 per category.
- **Variant generation before research** — Variants should be informed by verified research, not generic.
- **Full script variants** — Writing 3 complete scripts is wasteful. Variants at hook/structure level only.

### Complexity: LOW
- Prompt engineering change to script-writer-v2
- Simple choice tracking (SQLite table)
- Minimal new code

### Dependencies
- Existing: script-writer-v2 agent, opening hook templates, closing templates
- New: Variant mode in agent prompt, choice tracking table

---

## Priority Matrix

| Feature | Impact | Complexity | Priority |
|---------|--------|-----------|----------|
| Retention science integration | HIGH | LOW-MEDIUM | **1st — Quick win, immediate improvement** |
| Creator transcript analysis | HIGH | MEDIUM | **2nd — Builds technique library** |
| Structured choice architecture | MEDIUM | LOW | **3rd — Low effort, compounds over time** |
| Edit-based learning loop | VERY HIGH | HIGH | **4th — Most valuable but hardest** |

### Recommended Build Order

1. **Retention science** first — synthesize existing analytics into prescriptive rules. Immediate quality improvement.
2. **Creator analysis** second — builds the technique library that enriches the scriptwriter's reference material.
3. **Choice architecture** third — low effort to implement, starts generating data for learning.
4. **Edit learning** last — most complex, benefits from having other features producing data first.

---

## YouTube Retention Science: Key Patterns to Encode

Based on this channel's actual data + general YouTube retention research:

| Pattern | Evidence | Rule for Scriptwriter |
|---------|----------|--------------------|
| First 30 seconds decide retention | Channel data: Belize/Vance hook within 15 sec | Stakes or evidence promise in first 2 sentences |
| 1:11 dropout point | Industry standard, confirmed by channel data | No background/context dumps before 1:30 |
| 3-minute attention reset | Pattern interrupt data from retention curves | Every section must be under 3 min |
| Evidence density correlates with retention | Belize 23K views = high evidence density | Min 1 primary source quote per 90 seconds |
| Modern relevance as retention anchor | Channel pattern: modern hook every 90 sec | Flag any 2+ min stretch without modern connection |
| First-person authority hooks | "So, I read that treaty" within 25 sec (Belize) | First-person statement in first 60 seconds |
| Payoff-first structure | Top performers show consequence before history | Open with modern consequence, then explain how we got here |

---

*Researched: 2026-02-12 for v3.0 Adaptive Scriptwriter milestone*
