# Model Assignment Guide

This document explains how models are assigned to skills (slash commands) and agents for token optimization.

## Overview

Model assignment optimizes token usage by matching model capability to task complexity:

| Model | Cost | Speed | Best For |
|-------|------|-------|----------|
| **Haiku** | Lowest | Fastest | Simple, templated, mechanical tasks |
| **Sonnet** | Medium | Balanced | Reasoning, analysis, verification tasks |
| **Opus** | Highest | Slowest | Complex creative, retention engineering |

## Skill Assignments (13 Commands)

### Haiku (6 skills) - Simple/Fast Tasks

| Skill | Description | Why Haiku |
|-------|-------------|-----------|
| `/status` | Project status and routing | File scanning, simple logic |
| `/help` | Command menu display | Static menu, no reasoning |
| `/fix` | Subtitle correction | Pattern replacement, mechanical |
| `/sources` | Source recommendations | Template-based, no synthesis |
| `/prep` | Filming preparation | Template-based guides |
| `/discover` | Keyword research workflow | Orchestration, mostly templated |

### Sonnet (6 skills) - Reasoning/Analysis Tasks

| Skill | Description | Why Sonnet |
|-------|-------------|------------|
| `/verify` | Fact-checking | Source evaluation, reasoning |
| `/publish` | YouTube metadata | Creative generation |
| `/engage` | Comment responses | Nuance, empathy required |
| `/analyze` | Post-publish analysis | Pattern recognition |
| `/patterns` | Cross-video patterns | Synthesis across videos |
| `/research` | Topic research | Research synthesis |

### Opus (1 skill) - Complex Creative Tasks

| Skill | Description | Why Opus |
|-------|-------------|----------|
| `/script` | Script generation | Retention engineering, style matching, highest-value output |

## Agent Assignments (6 Agents)

### Haiku (3 agents) - Mechanical/Templated Tasks

| Agent | Description | Why Haiku |
|-------|-------------|-----------|
| `diy-asset-creator` | B-roll asset guides | Template-based checklists |
| `research-organizer` | Research organization | Mechanical organization |
| `claims-extractor` | Claim extraction | Pattern matching, structured output |

### Sonnet (2 agents) - Analysis/Verification Tasks

| Agent | Description | Why Sonnet |
|-------|-------------|------------|
| `fact-checker` | Source verification | Web research, source evaluation |
| `structure-checker-v2` | Script analysis | Retention prediction, pattern analysis |

### Opus (1 agent) - Complex Creative Tasks

| Agent | Description | Why Opus |
|-------|-------------|----------|
| `script-writer-v2` | Script writing | Complex creative writing, style matching, retention engineering |

## Decision Framework

When assigning models to new skills or agents, use this framework:

### Use Haiku when:
- Task is primarily templated or mechanical
- Output follows a predictable structure
- No creative synthesis required
- Speed is more valuable than depth
- Examples: status checks, file organization, checklist generation

### Use Sonnet when:
- Task requires reasoning or analysis
- Source evaluation or fact-checking needed
- Moderate creativity with structured output
- Balance of quality and cost important
- Examples: verification, comment responses, pattern analysis

### Use Opus when:
- Task is the highest-value creative output
- Retention engineering matters
- Style matching required
- Quality directly impacts channel performance
- Worth the higher token cost
- Examples: script writing, complex narrative construction

## Updating Assignments

### For Skills
Edit the YAML frontmatter in `.claude/commands/{skill}.md`:
```yaml
---
description: Skill description
model: haiku|sonnet|opus
---
```

### For Agents
Edit the YAML frontmatter in `.claude/agents/{agent}.md`:
```yaml
---
name: agent-name
description: Agent description
tools: [...]
model: haiku|sonnet|opus
---
```

## Summary Statistics

| Model | Skills | Agents | Total |
|-------|--------|--------|-------|
| Haiku | 6 | 3 | 9 |
| Sonnet | 6 | 2 | 8 |
| Opus | 1 | 1 | 2 |
| **Total** | **13** | **6** | **19** |

## Maintenance Notes

- Review assignments quarterly or after significant workflow changes
- Monitor token usage patterns to identify optimization opportunities
- If a Haiku task consistently needs escalation, consider upgrading
- If a Sonnet/Opus task is underutilized, consider downgrading
- Document any changes in this guide

---

*Last updated: 2026-01-29 (Phase 13.1 Token Optimization)*
