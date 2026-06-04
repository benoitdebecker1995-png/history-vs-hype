---
name: Past Projects = Pattern Library
description: Before designing a new project artifact's structure or filename convention, Glob recent project folders for similar artifacts. User's actual conventions live in past work, not in CLAUDE.md.
type: feedback
originSessionId: acf6893b-dd34-4e58-89e9-9290f916aa55
---

# Past Projects = Pattern Library

## The rule

Before specifying a NEW project artifact's structure, file format, or filename convention, Glob 2-3 recent project folders for similar artifacts. The user's actual conventions live in past work, not in CLAUDE.md.

## Why

2026-05-11 — initial `/editing-guide` design was a timestamp table (IN/OUT timecode per shot). After exploring `52-hijab/`, `51-tripoli/`, `45-manhattan/`, found `EDITING-GUIDE-HOOK.md` already existed in Tripoli — a validated 9-section template (TL;DR / segment notes / issue tables / B-roll / pacing / captions / pickups / music / done state). Completely restructured the plan to match.

The miss: I designed from scratch instead of looking for precedents. The Tripoli template was richer, more useful, and already aligned with how the user thinks about post-production. Designing from CLAUDE.md alone would have shipped a worse artifact.

Cost of the miss: nearly built the wrong format, would have needed iteration. Cost of preventing: one `Glob` call (<5 seconds).

CLAUDE.md describes the *ideal*; project folders show the *actual*. When the two differ, actual wins.

## How to apply

**Triggers when:** about to specify a NEW project artifact's structure, file format, filename convention, or section template. Not for code; for *channel artifacts* (script docs, research files, B-roll plans, fact-check docs, post-mortems, editing guides, metadata, etc.).

**Action:**

1. **Glob 2-3 recent project folders** for the artifact category:
   - `Glob 'video-projects/_IN_PRODUCTION/*/[ARTIFACT-NAME]*'`
   - `Glob 'video-projects/_IN_PRODUCTION/*/' | head 3` then `ls` each for naming patterns
2. **If a precedent exists, match it.** Use the same naming, the same section structure, the same metadata conventions. Don't reinvent.
3. **If no precedent exists, design fresh** — but read 2-3 recent projects' general structure to match the channel's style of organization (headers, frontmatter, section breakdown).

## Counter-examples (when NOT to fire)

- Adding to an existing artifact format already in widespread use (don't search for "another B-ROLL-FACSIMILE-SHOT-LIST.md format" when one exists in the active project)
- Writing one-off analyses (no reuse concern)
- Code changes outside `video-projects/` (this is about channel artifacts specifically)

The rule is about **artifact format design**, not every file write.
