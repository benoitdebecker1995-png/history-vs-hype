# Routing Classification Guide

**Created:** 2026-02-07 (Phase 28.1)
**Extends:** MODEL-ASSIGNMENT-GUIDE.md (Phase 13.1)
**Purpose:** Maps which commands and agents can be routed to free models for cost optimization

## Hardware Constraints

**System specs:**
- Total RAM: 14.9 GB
- Available RAM: ~3.7 GB (fluctuates)
- GPU: AMD Radeon Graphics (integrated, not NVIDIA CUDA)
- Platform: Windows (MSYS_NT-10.0-26200)

**Why local models are NOT feasible:**

| Model Type | RAM Required | Status | Reason |
|------------|--------------|--------|---------|
| Qwen 2.5 Coder 32B | 20-24 GB | ❌ BLOCKED | Exceeds total system RAM |
| Llama 3.3 70B | 40+ GB | ❌ BLOCKED | Exceeds total system RAM |
| Mistral 7B | 4-6 GB | ⚠️ RISKY | Would consume all available RAM, system instability |
| Qwen 2.5 3B | 2-3 GB | ⚠️ LIMITED | Technically possible but insufficient capability for complex tasks |

**Conclusion:** Focus on **OpenRouter free tier** for cost optimization. Local models are not viable on this hardware.

## Routing Tiers (Definitions)

| Tier | Description | Target | Quality Risk |
|------|-------------|--------|--------------|
| **Claude-Only** | Quality-critical, complex reasoning, creative synthesis | Keep on Claude (Opus 4.5/4.6 or Sonnet 4.5) | N/A |
| **Routable-Free** | Simple/mechanical tasks, or validated low-risk tasks | OpenRouter free models (Gemini 2.0 Flash, Llama 3.3 70B) | LOW to MEDIUM |
| **Routable-Local** | NOT APPLICABLE | Ollama (blocked by hardware constraints) | N/A |

## Classification Table (All 19 Tasks)

| Command/Agent | Phase 13.1 Tier | Routing Tier | Free Model Target | Quality Risk | Est. Monthly Savings | Validation Status |
|---------------|-----------------|--------------|-------------------|--------------|---------------------|-------------------|
| **COMMANDS (13)** | | | | | | |
| `/script` | Opus | Claude-Only | N/A | N/A | $0 | N/A |
| `/research` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `/verify` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `/analyze` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `/patterns` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `/publish` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `/engage` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `/status` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | VERY LOW | $2-3 | ⏳ PENDING |
| `/help` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | VERY LOW | $0.50 | ⏳ PENDING |
| `/fix` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | LOW | $0.50 | UNTESTED |
| `/sources` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | LOW | $1-2 | UNTESTED |
| `/prep` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | LOW | $2-3 | ⏳ PENDING |
| `/discover` | Haiku | **Routable-Free** | `meta-llama/llama-3.3-70b-instruct:free` | LOW | $2-4 | UNTESTED |
| **AGENTS (6)** | | | | | | |
| `script-writer-v2` | Opus | Claude-Only | N/A | N/A | $0 | N/A |
| `fact-checker` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `structure-checker-v2` | Sonnet | Claude-Only | N/A | N/A | $0 | N/A |
| `research-organizer` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | LOW | $1-2 | UNTESTED |
| `claims-extractor` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | LOW | $2-3 | UNTESTED |
| `diy-asset-creator` | Haiku | **Routable-Free** | `google/gemini-2.0-flash-exp:free` | LOW | $0.50-1 | UNTESTED |
| | | | | **TOTAL** | **$12-21/month** | |

## Claude-Only Tasks (DO NOT ROUTE)

### Opus Tasks (2)
**Cannot route** — These are the channel's highest-value outputs requiring retention engineering, style matching, and creative synthesis.

| Task | Reason |
|------|--------|
| `/script` | Retention engineering, Alex O'Connor/Kraut style matching, narrative construction — the channel's core value proposition |
| `script-writer-v2` | Complex creative writing, 8,000-word scripts with academic rigor — requires best available model |

### Sonnet Tasks (7)
**Cannot route** — These require reasoning, source evaluation, nuance, or moderate creativity that free models cannot reliably match.

| Task | Reason |
|------|--------|
| `/research` | Research synthesis, source evaluation, connecting disparate academic sources |
| `/verify` | Fact-checking requires source evaluation, detecting logical fallacies, academic rigor |
| `/analyze` | Post-publish pattern analysis, cross-metric synthesis, actionable insights |
| `/patterns` | Cross-video pattern recognition, extracting winning formulas from data |
| `/publish` | YouTube metadata needs creativity + documentary tone filter (not pure template) |
| `/engage` | Comment responses need empathy, nuance, channel voice consistency |
| `fact-checker` | Source verification, tier-based evaluation, detecting misleading claims |
| `structure-checker-v2` | Retention prediction, narrative flow analysis, energy arc detection |

**Why Sonnet tasks stay on Claude:**
- Source evaluation (distinguish academic vs popular sources)
- Nuance and empathy (comment responses, balanced argumentation)
- Pattern synthesis (cross-video insights, not just aggregation)
- Creative + structured (metadata generation with tone constraints)

### Validation Status Legend

| Status | Meaning | Action |
|--------|---------|--------|
| N/A | Claude-Only task, no validation needed | Keep on Claude |
| ⏳ PENDING | Validation protocol defined, awaiting user testing | See VALIDATION-RESULTS.md |
| UNTESTED | Routable candidate, validation protocol not yet created | Defer to later validation rounds |
| ✅ VALIDATED | Tested and scored PASS or ACCEPTABLE | Safe to route |
| ❌ FAILED | Tested and scored FAIL | Keep on Claude, remove from routable list |

**Current validation focus (Plan 02):** 3 tasks marked ⏳ PENDING (`/status`, `/help`, `/prep`)

**Next validation rounds:** Remaining 7 tasks marked UNTESTED will be validated after initial 3 tasks pass

---

## Routable Tasks (7 commands + 3 agents)

### High-Frequency Simple (Immediate Routing Candidates)

| Task | Free Model | Why Safe to Route | Validation |
|------|------------|-------------------|------------|
| `/status` | Gemini 2.0 Flash | File scanning, simple logic, no creativity | Compare 5 outputs to Claude baseline |
| `/help` | Gemini 2.0 Flash | Static menu display, pure template | One-time validation (menu doesn't change) |

**Monthly savings:** $2.50-3.50 (high frequency × near-zero cost = measurable impact)

### Mechanical Tasks (After Initial Validation)

| Task | Free Model | Why Safe to Route | Validation |
|------|------------|-------------------|------------|
| `/fix` | Gemini 2.0 Flash | Pattern-based subtitle correction, deterministic | Test on 3 SRT files with known errors |
| `/sources` | Gemini 2.0 Flash | Template-based source recommendations | Compare 5 outputs to Claude baseline |
| `/prep` | Gemini 2.0 Flash | Template-based filming guides (B-roll checklist, edit guide) | Test on 2 scripts |
| `/discover` | Llama 3.3 70B | Orchestration, mostly templated output | Test on 3 keywords |

**Monthly savings:** $5.50-11 (moderate frequency × low cost)

### Agent Tasks (After Command Validation)

| Task | Free Model | Why Safe to Route | Validation |
|------|------------|-------------------|------------|
| `research-organizer` | Gemini 2.0 Flash | Mechanical organization, no synthesis | Test on 2 VERIFIED-RESEARCH files |
| `claims-extractor` | Gemini 2.0 Flash | Pattern matching, structured output | Test on 2 transcripts |
| `diy-asset-creator` | Gemini 2.0 Flash | Template-based checklists | Test on 2 B-roll requests |

**Monthly savings:** $3.50-6 (low frequency but consistent)

## Estimated Savings Summary

| Category | Tasks | Monthly Savings | Risk Level |
|----------|-------|-----------------|------------|
| High-frequency simple | 2 | $2.50-3.50 | VERY LOW |
| Mechanical tasks | 4 | $5.50-11 | LOW |
| Agent tasks | 3 | $3.50-6 | LOW |
| **TOTAL** | **10 of 19** | **$12-21/month** | **LOW** |

**Percentage of total costs:** 2-4% savings ($12-21 of $557.55)

**Caveats:**
- Savings are modest because Haiku tasks are already near-zero cost ($0.71/month)
- Main benefit is **removing friction** (faster responses, no token anxiety)
- Opus tasks (84.9% of costs) cannot be routed without severe quality degradation
- Actual savings may be lower due to prompt caching efficiency

## Routing Strategy Decision

### Chosen Tool: Claude Code Native `/model` Switching + Wave Terminal for Testing

**Decision rationale:**

After evaluating routing tools against this project's requirements, the chosen strategy is:

1. **Primary:** Use Claude Code's **native `/model` command** for manual model switching
   - Already available in Claude Code (no installation needed)
   - Allows per-conversation model selection
   - Syntax: `/model openrouter/google/gemini-2.0-flash-exp:free`
   - User remains in control of when to route

2. **Testing:** Use **Wave Terminal** for side-by-side validation
   - Install: `brew install waveterm/waveterm-dev/waveterm` (macOS) or download from waveterm.dev
   - Allows running same prompt on Claude vs free model simultaneously
   - Visual comparison for quality validation
   - Use during Phase 2 validation period

**Why this approach:**

| Factor | Rationale |
|--------|-----------|
| Hardware constraints | No local models viable (14.9GB RAM, AMD integrated GPU) → must use cloud routing |
| Daily usage pattern | 4 videos/month = 68 total invocations/month → low enough for manual switching |
| Quality sensitivity | User retains control over which tasks to route → gradual rollout, no surprises |
| OpenRouter limits | 50 req/day default, 1000/day with $10 credits → manual switching stays within limits |
| Complexity tradeoff | Automated routing adds complexity (config, errors, debugging) → not worth it for 68 invocations/month |

**Configuration path:**

```bash
# No installation needed for Claude Code /model command (built-in)

# For Wave Terminal (validation only):
# 1. Download from waveterm.dev
# 2. Install per platform instructions
# 3. Add API keys in Wave settings:
#    - Anthropic API key for Claude
#    - OpenRouter API key for free models

# For OpenRouter API key:
# 1. Sign up at openrouter.ai
# 2. Generate API key in Settings
# 3. Add to Claude Code: export OPENROUTER_API_KEY=sk-or-v1-...
# 4. Optional: Add $10 credits for 1000 req/day limit (vs 50 req/day free)
```

**Usage workflow:**

```bash
# High-frequency simple tasks:
/model openrouter/google/gemini-2.0-flash-exp:free
/status

# Mechanical tasks:
/model openrouter/google/gemini-2.0-flash-exp:free
/prep

# Quality-critical tasks (default):
/model anthropic/claude-opus-4-6
/script

# Reset to default:
/model default
```

### Rejected Alternatives

| Tool | Reason Rejected |
|------|-----------------|
| **Claude Code Router** | Requires separate process, config file management, adds complexity for minimal benefit (68 invocations/month) |
| **Ollama (local)** | Insufficient RAM (14.9GB total, 3.7GB available), no NVIDIA GPU, 32B/70B models not viable |
| **LiteLLM Proxy** | Over-engineered for this use case (designed for team-wide routing), adds operational overhead |
| **Automated routing via shell wrapper** | Removes user control, risk of routing quality-critical tasks by accident |

**Why manual > automated:**
- 68 invocations/month = ~2-3 per day
- Manual switching takes 2 seconds: `/model openrouter/...`
- Automated routing adds: config maintenance, error handling, debugging time
- **Tradeoff:** Save 2 seconds/invocation × 68 = 136 seconds/month = 2.3 minutes/month
- **Not worth:** Config complexity, loss of control, potential quality issues

## Rate Limit Analysis

**OpenRouter free tier limits:**
- **Default:** 50 requests/day
- **With $10 credits:** 1000 requests/day

**Projected daily usage (routable tasks only):**

| Task | Daily Invocations | Monthly Invocations |
|------|-------------------|---------------------|
| `/status` | 1 | 30 |
| `/help` | 0.1 | 3 |
| `/fix` | 0.1 | 2 |
| `/sources` | 0.1 | 2 |
| `/prep` | 0.1 | 2 |
| `/discover` | 0.2 | 6 |
| `research-organizer` | 0.1 | 2 |
| `claims-extractor` | 0.1 | 2 |
| `diy-asset-creator` | 0.03 | 1 |
| **TOTAL** | **~2** | **~50** |

**Rate limit verdict:**
- **Current usage:** ~2 requests/day if all routable tasks are routed
- **Free tier capacity:** 50 requests/day
- **Headroom:** 25x current usage
- **Recommendation:** Free tier is sufficient, no need to add $10 credits initially

**Growth scenario:**
- If production scales to 8 videos/month: ~4 requests/day (still well within 50/day limit)
- If production scales to 30 videos/month: ~15 requests/day (still within limit)
- Threshold for adding credits: >50 videos/month (unlikely for this channel)

## Implementation Roadmap (Phase 2)

### Week 1: Validation
1. Test `/status` on 5 different project states
2. Test `/help` once (static menu)
3. Compare outputs to Claude baseline
4. Document any quality issues

### Week 2: Mechanical Tasks
1. Route `/fix` for 2 SRT files
2. Route `/sources` for 2 videos
3. Route `/prep` for 2 videos
4. Monitor quality, revert if issues

### Week 3: Agent Tasks
1. Route `research-organizer` for 1 video
2. Route `claims-extractor` for 1 video
3. Route `diy-asset-creator` for 1 video

### Week 4: Monitor & Measure
1. Calculate actual savings vs estimate
2. Document any quality degradations
3. Adjust routing classification if needed

## Maintenance Protocol

**Monthly review:**
- Check actual usage vs rate limits
- Measure actual savings vs estimates
- Review quality issues log
- Adjust routing classification if patterns change

**Escalation triggers:**
- If free model output needs Claude correction >20% of time → remove from routable list
- If OpenRouter free tier becomes unreliable → evaluate paid tier or alternatives
- If hardware is upgraded (more RAM, NVIDIA GPU) → re-evaluate local models

---

**Next step:** Plan 02 will implement routing validation and measure actual savings.

*Created: 2026-02-07 (Phase 28.1-01)*
*Extends: MODEL-ASSIGNMENT-GUIDE.md (Phase 13.1)*
