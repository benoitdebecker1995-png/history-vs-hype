# Phase 32: Model Assignment Refresh - Research

**Researched:** 2026-02-09
**Domain:** Claude Code model configuration and YAML frontmatter updates
**Confidence:** HIGH

## Summary

Phase 32 updates all slash command files and agent configurations from outdated placeholder model tier names (opus/sonnet/haiku) to current Claude 4.x model identifiers. The research confirms that Claude Code's model routing system uses **short aliases** (opus, sonnet, haiku) rather than full versioned IDs, which map to the latest model versions automatically. This means the current YAML frontmatter is already using the correct format, but documentation refers to outdated "Claude 3.5" naming that should be updated to reflect Claude 4.x lineup.

The phase will update documentation references, verify no old model IDs exist in the codebase, mark Phase 28.1 Plan 02 as deliberately skipped in the roadmap, and optionally close Phase 4 (deferred since v1.0).

**Primary recommendation:** Keep current `model: opus/sonnet/haiku` format in YAML frontmatter (already correct). Update documentation only. Skip 28.1 Plan 02. Simple grep verification sufficient.

## User Constraints (from CONTEXT.md)

### Locked Decisions

**Model Tier Mapping:**
- Keep existing tier assignments from Phase 13.1 (Opus/Sonnet/Haiku per command)
- Claude reviews and flags any obvious mismatches but preserves the current distribution
- Script-writer-v2 stays on Opus — script quality is the channel's competitive edge, don't downgrade

**Phase 28.1 Closure:**
- Skip Phase 28.1 Plan 02 (routing validation via OpenRouter) entirely — not worth pursuing
- Mark Phase 28.1 as complete in roadmap with note that Plan 02 was deliberately skipped

**Scope of Refresh:**
- At minimum: 13 slash command YAML frontmatter + agent files in .claude/agents/
- Update existing MODEL-ASSIGNMENTS.md from Phase 13.1

### Claude's Discretion

- Model ID format: Claude picks what works best with Claude Code's model routing (short aliases vs full versioned IDs)
- Whether to reference the 28.1 token audit findings (routing notes) without scope creep
- Verification approach (grep audit, smoke test, or both)
- Extended thinking annotations in agent configs (whether to add explicit flags or let Claude Code handle it)
- Whether MODEL-REFERENCE.md should be created/updated
- Extended scope: full repo sweep including docs (CLAUDE.md, STATE.md, etc.) if old references found
- Phase 4 cleanup in roadmap

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope

## Standard Stack

### Core Technology

| Component | Current State | Required Action |
|-----------|---------------|-----------------|
| **Claude Code** | Model aliases: `opus`, `sonnet`, `haiku` | No change needed |
| **Command YAML** | 13 files with `model: opus\|sonnet\|haiku` | Already correct format |
| **Agent YAML** | 6 files with `model: opus\|sonnet\|haiku` | Already correct format |
| **Documentation** | References "Claude 3.5" lineup | Update to Claude 4.x |

### Model Identifiers (February 2026)

**Official API model names:**
- Opus 4.6: `claude-opus-4-6`
- Opus 4.5: `claude-opus-4-5-20251101`
- Sonnet 4.5: `claude-sonnet-4-5-20250929`
- Haiku 4.5: `claude-haiku-4-5-20251001`

**Claude Code model aliases (RECOMMENDED for this codebase):**
- `opus` → automatically maps to latest Opus (currently 4.6)
- `sonnet` → automatically maps to latest Sonnet (currently 4.5)
- `haiku` → automatically maps to latest Haiku (currently 4.5)
- `default` → recommended model based on account type
- `opusplan` → Opus for planning, Sonnet for execution

**Source:** [Claude Code Model Configuration](https://code.claude.com/docs/en/model-config)

### Why Short Aliases Are Better

**Advantages of `model: opus` over `model: claude-opus-4-6`:**
1. **Future-proof:** Aliases automatically point to latest version
2. **Cleaner syntax:** Shorter, more readable YAML
3. **Claude Code native:** Official documented approach
4. **Version agnostic:** No need to update when 4.7/4.8 releases
5. **Consistency:** Matches Claude Code's `/model` command format

**When to use full IDs:**
- Pinning to specific version (testing, reproducibility)
- Setting environment variables like `ANTHROPIC_DEFAULT_OPUS_MODEL`

### Current State Verification

**Checked files:**
- `.claude/commands/*.md` (13 files) — ALL use short aliases ✓
- `.claude/agents/*.md` (6 files) — ALL use short aliases ✓
- `.claude/REFERENCE/MODEL-ASSIGNMENT-GUIDE.md` — Uses short aliases, documents Phase 13.1 decisions ✓

**Conclusion:** YAML frontmatter is already correct. No code changes needed.

## Architecture Patterns

### Pattern 1: YAML Frontmatter Model Assignment

**Current (correct) format:**

```yaml
---
description: Command description
model: haiku|sonnet|opus
---
```

**For agents:**

```yaml
---
name: agent-name
description: Agent description
tools: [Read, Write, ...]
model: haiku|sonnet|opus
---
```

**DO NOT change to:**
```yaml
model: claude-opus-4-6  # ❌ Too specific, needs updates with each release
```

### Pattern 2: Documentation References to Models

**OUTDATED (found in docs):**
- "Claude 3.5 Opus"
- "Claude 3.5 Sonnet"
- "Claude 3.5 Haiku"
- "Claude 3 model family"

**UPDATED (should use):**
- "Claude Opus 4.6" (or "Opus" in casual context)
- "Claude Sonnet 4.5" (or "Sonnet")
- "Claude Haiku 4.5" (or "Haiku")
- "Claude 4.x lineup"

### Pattern 3: Phase 13.1 Model Assignment Logic (Preserve)

**From MODEL-ASSIGNMENT-GUIDE.md:**

| Task Complexity | Model Tier | Examples |
|-----------------|------------|----------|
| **Mechanical/templated** | Haiku | Status checks, file organization, checklists |
| **Reasoning/analysis** | Sonnet | Verification, comment responses, pattern analysis |
| **Complex creative** | Opus | Script writing, retention engineering |

**This logic remains valid. No reassignment needed.**

### Pattern 4: Extended Thinking (Opus 4.6)

**Extended thinking is automatic for Opus 4.6** — no explicit configuration needed in YAML.

From script-writer-v2.md (line 3):
> description: World-class scriptwriting agent using extended thinking...

This is **documentation only**, not a configuration flag. Claude Code handles extended thinking automatically when using Opus.

**No action needed:** Extended thinking annotation is descriptive, not prescriptive.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Model routing | Custom model switcher logic | Claude Code native aliases | Built-in, maintained, documented |
| Version tracking | Manual version update system | Short aliases (auto-update) | Claude Code handles mapping |
| Model capability detection | Parse model names for features | Use tier system (opus/sonnet/haiku) | Simpler, more maintainable |

## Common Pitfalls

### Pitfall 1: Over-Specifying Model Versions

**What goes wrong:** Using `claude-opus-4-6` instead of `opus` creates maintenance burden. When 4.7 releases, every file needs updating.

**Why it happens:** Assumption that explicit versions = more control.

**How to avoid:** Use short aliases for ongoing work, full IDs only for reproducibility needs.

**Warning signs:** Finding version numbers in YAML frontmatter.

### Pitfall 2: Breaking Changes Assumption

**What goes wrong:** Assuming model updates will break existing commands.

**Why it happens:** Fear of automatic version changes.

**How to avoid:** Trust Claude Code's alias system. Anthropic maintains backward compatibility within model families. If breaking changes occur, Claude Code team handles the mapping.

**Warning signs:** Reluctance to use aliases, desire to "lock" versions everywhere.

### Pitfall 3: Documentation-Config Confusion

**What goes wrong:** Reading "uses extended thinking" in agent description and trying to add configuration flags for it.

**Why it happens:** Confusing documentation of capabilities with configuration requirements.

**How to avoid:** Extended thinking, prompt caching, and other model features are automatic. No YAML configuration needed beyond `model: opus`.

**Warning signs:** Looking for `extended_thinking: true` or similar flags.

### Pitfall 4: Incomplete Grep Searches

**What goes wrong:** Searching only `.md` files misses references in Python scripts, JSON configs, etc.

**Why it happens:** Assuming model references only in documentation.

**How to avoid:** Grep across all file types: `grep -r "claude-3" . --include="*.md" --include="*.py" --include="*.json"`

**Warning signs:** Finding old model IDs after claiming "all updated."

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Claude 3.5 lineup (Opus/Sonnet/Haiku) | Claude 4.x lineup (Opus 4.6, Sonnet 4.5, Haiku 4.5) | Oct 2025 - Feb 2026 | Same tier system, better performance |
| Full model IDs in configs | Short aliases in configs | Claude Code launch | Easier maintenance, future-proof |
| Manual model switching | Claude Code `/model` command | Claude Code 2025 | Better UX, instant switching |

**Deprecated/outdated:**
- **Claude 3 model family references** — superseded by Claude 4.x
- **"Claude 3.5" naming** — confusing given Claude 4 exists
- **Phase 28.1 Plan 02 (routing validation)** — skipped, not worth hardware constraints

## Code Examples

### Current State (Verified Correct)

**Command file (.claude/commands/script.md):**

```yaml
---
description: Write, revise, review, or export scripts
model: opus
---
```

**Agent file (.claude/agents/script-writer-v2.md):**

```yaml
---
name: script-writer-v2
description: World-class scriptwriting agent using extended thinking
tools: [Read, Write, WebFetch, WebSearch, Grep, Glob]
model: opus
---
```

### Documentation Update Pattern

**BEFORE (in CLAUDE.md or other docs):**

```markdown
Uses Claude 3.5 Sonnet for reasoning tasks
```

**AFTER:**

```markdown
Uses Claude Sonnet 4.5 for reasoning tasks
```

**OR (more future-proof):**

```markdown
Uses Sonnet for reasoning tasks
```

### Roadmap Phase 28.1 Update

**BEFORE (.planning/ROADMAP.md):**

```markdown
### Phase 28.1: Multi-Model Token Optimization
Plans:
- [x] 28.1-01-PLAN.md — Token audit + routing classification
- [ ] 28.1-02-PLAN.md — Routing setup + quality validation
```

**AFTER:**

```markdown
### Phase 28.1: Multi-Model Token Optimization
Plans:
- [x] 28.1-01-PLAN.md — Token audit + routing classification
- [skipped] 28.1-02-PLAN.md — Routing setup (not pursued due to hardware constraints)

**Note:** Plan 02 deliberately skipped. Token audit complete, but OpenRouter routing not worth complexity given 14.9GB RAM limitation and Claude Code's existing model tier system. Phase closed as complete.
```

### MODEL-ASSIGNMENT-GUIDE.md Header Update

**BEFORE:**

```markdown
# Model Assignment Guide

This document explains how models are assigned to skills (slash commands) and agents for token optimization.

## Overview

Model assignment optimizes token usage by matching model capability to task complexity:

| Model | Cost | Speed | Best For |
|-------|------|-------|----------|
| **Haiku** | Lowest | Fastest | Simple, templated, mechanical tasks |
| **Sonnet** | Medium | Balanced | Reasoning, analysis, verification tasks |
| **Opus** | Highest | Slowest | Complex creative, retention engineering |
```

**AFTER (add version context):**

```markdown
# Model Assignment Guide

This document explains how models are assigned to skills (slash commands) and agents for token optimization.

**Current lineup (as of February 2026):**
- **Opus 4.6** — Latest flagship model
- **Sonnet 4.5** — Balanced reasoning and speed
- **Haiku 4.5** — Fast, efficient for simple tasks

Commands use short aliases (`model: opus`) which automatically map to latest versions.

## Overview

Model assignment optimizes token usage by matching model capability to task complexity:

| Model Tier | Current Model | Cost | Speed | Best For |
|------------|---------------|------|-------|----------|
| **Haiku** | Claude Haiku 4.5 | Lowest | Fastest | Simple, templated, mechanical tasks |
| **Sonnet** | Claude Sonnet 4.5 | Medium | Balanced | Reasoning, analysis, verification tasks |
| **Opus** | Claude Opus 4.6 | Highest | Slowest | Complex creative, retention engineering |
```

## Open Questions

### 1. Should Phase 4 (Workflow Simplification) be closed?

**What we know:**
- Phase 4 marked "DEFERRED" in roadmap since v1.0 (Jan 2026)
- Phase 7 delivered slash command system (10 commands)
- Current system works well, no user complaints

**What's unclear:**
- Was Phase 4's intent fully satisfied by Phase 7?
- Is there residual work worth pursuing?

**Recommendation:** Review Phase 4 requirements against Phase 7 deliverables. If redundant, mark as "Closed - Superseded by Phase 7" in roadmap. If distinct goals remain, keep deferred.

### 2. Should extended thinking be explicitly documented in agent configs?

**What we know:**
- Opus 4.6 uses extended thinking automatically
- script-writer-v2.md mentions it in description (line 3)
- No configuration flag needed

**What's unclear:**
- Should we add a comment in YAML explaining it's automatic?
- Does lack of explicit documentation cause confusion?

**Recommendation:** Add brief comment in MODEL-ASSIGNMENT-GUIDE.md explaining extended thinking is automatic for Opus 4.6. No YAML changes needed.

### 3. Should old model IDs be searched in .gitignore'd files?

**What we know:**
- Standard grep search covers committed files
- .gitignore excludes node_modules, venv, etc.

**What's unclear:**
- Could old model IDs persist in local configs or caches?

**Recommendation:** Focus on committed files only. Local configs/caches are environment-specific and regenerated as needed.

## Verification Protocol

### Step 1: Grep Audit for Old Model References

**Search patterns:**

```bash
# Primary search (committed files only)
cd "G:\History vs Hype"
grep -r "claude-3" . --include="*.md" --include="*.py" --include="*.json" --include="*.yaml" --include="*.yml"
grep -r "opus-3\|sonnet-3\|haiku-3" . --include="*.md" --include="*.py" --include="*.json"
grep -r "Claude 3\.5\|Claude 3\.0" . --include="*.md"
```

**Expected result:** No matches (or only in archived/historical documentation).

### Step 2: Verify Current Assignments Unchanged

**Check files:**
- `.claude/commands/*.md` (13 files)
- `.claude/agents/*.md` (6 files)

**Verification:**
```bash
cd "G:\History vs Hype\.claude\commands"
grep "^model:" *.md

cd "G:\History vs Hype\.claude\agents"
grep "^model:" *.md
```

**Expected result:** All show `model: opus`, `model: sonnet`, or `model: haiku`.

### Step 3: Documentation Consistency Check

**Files to review:**
- `.claude/REFERENCE/MODEL-ASSIGNMENT-GUIDE.md`
- `CLAUDE.md` (if model references exist)
- `.planning/ROADMAP.md` (Phase 28.1 section)
- `.planning/STATE.md` (if model references exist)

**Check for:**
- References to "Claude 3.5" → update to "Claude 4.x" or generic "Opus/Sonnet/Haiku"
- Outdated version numbers
- Correct tier assignments from Phase 13.1

### Step 4: Phase 28.1 and 4 Closure

**Update ROADMAP.md:**
- Phase 28.1: Mark Plan 02 as [skipped] with reason
- Phase 4: Decide if closing as superseded or keeping deferred

**No functional testing needed:**
- Model aliases already work correctly
- No code changes = no new bugs
- Existing commands continue working unchanged

## Sources

### Primary (HIGH confidence)

- **Claude Code Model Configuration:** https://code.claude.com/docs/en/model-config
  - Model aliases (opus, sonnet, haiku)
  - Environment variable configuration
  - Model switching and opusplan mode

- **Anthropic Models Overview:** https://platform.claude.com/docs/en/about-claude/models/overview
  - Official model identifiers
  - Model capabilities and context windows

- **Current model lineup (verified):**
  - Opus 4.6: https://www.anthropic.com/news/claude-opus-4-6
  - Sonnet 4.5: Verified via Claude Code docs
  - Haiku 4.5: https://www.anthropic.com/news/claude-haiku-4-5

- **Local codebase files (verified 2026-02-09):**
  - `.claude/commands/*.md` (13 files) — all use short aliases
  - `.claude/agents/*.md` (6 files) — all use short aliases
  - `.claude/REFERENCE/MODEL-ASSIGNMENT-GUIDE.md` — Phase 13.1 decisions documented
  - `.planning/phases/28.1-multi-model-token-optimization/TOKEN-AUDIT.md` — token consumption analysis

### Secondary (MEDIUM confidence)

- **Claude Code model configuration guide:** https://www.eesel.ai/blog/model-configuration-claude-code
  - Third-party tutorial on model switching

- **Model comparison articles:**
  - https://medium.com/@ayaanhaider.dev/sonnet-4-5-vs-haiku-4-5-vs-opus-4-1-which-claude-model-actually-works-best-in-real-projects-7183c0dc2249
  - Community perspectives on model selection

### Tertiary (LOW confidence)

None — all claims verified with primary sources (Claude Code docs, Anthropic official releases, local files).

## Metadata

**Confidence breakdown:**
- Model alias format: **HIGH** — Verified via Claude Code official docs + local file inspection
- Current model lineup: **HIGH** — Anthropic official announcements + Claude Code docs
- No code changes needed: **HIGH** — All files already use correct format
- Documentation needs: **MEDIUM** — Some "Claude 3.5" references may exist, grep will confirm

**Research date:** 2026-02-09
**Valid until:** 90 days (stable domain, model naming conventions don't change frequently)

**Key findings for planner:**
1. **No YAML changes needed** — Current `model: opus/sonnet/haiku` format is correct
2. **Documentation updates only** — Change "Claude 3.5" to "Claude 4.x" or generic tier names
3. **Simple grep verification** — No smoke testing needed, it's a documentation refresh
4. **Phase 28.1 closure** — Mark Plan 02 as skipped in roadmap
5. **Phase 4 decision** — Optional cleanup: close as superseded or keep deferred
6. **Model tier assignments preserved** — Phase 13.1 decisions remain unchanged

**Estimated effort:** 30-45 minutes (grep audit + documentation updates + roadmap cleanup)
