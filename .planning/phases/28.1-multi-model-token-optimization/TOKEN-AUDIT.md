# Token Usage Audit - Phase 28.1

**Date:** 2026-02-07
**Method:** ccusage CLI + manual profiling
**Period analyzed:** January-February 2026

## Hardware Constraints

**System Specs:**
- **Total RAM:** 14.9 GB (14,877,257,728 bytes)
- **Available RAM:** ~3.7 GB (fluctuates)
- **GPU:** AMD Radeon Graphics (integrated, not NVIDIA)
- **Platform:** Windows (MSYS_NT-10.0-26200)

**Implications for local models:**
- **Ollama Qwen 2.5 Coder 32B:** NOT feasible (requires 20-24GB RAM minimum)
- **Ollama 7B models:** Marginal (require 4-6GB RAM, would consume nearly all available RAM, risk system instability)
- **Ollama 3B models:** Technically possible but limited capability for complex tasks
- **Primary routing target:** OpenRouter free tier (no local RAM constraints)

**Conclusion:** Local model routing is NOT recommended for this hardware. Focus on OpenRouter free tier for cost optimization.

## ccusage Data Summary

**Total usage (Jan-Feb 2026):**
- **Total tokens:** 595,534,366 tokens
- **Total cost:** $557.55 USD
- **Input tokens:** 985,934
- **Output tokens:** 114,367
- **Cache create:** 50,206,481
- **Cache read:** 544,227,584

**Model breakdown:**

| Model | Input | Output | Cache Create | Cache Read | Total Tokens | Cost | % Total Cost |
|-------|-------|--------|--------------|------------|--------------|------|--------------|
| Opus 4.5 | 627,669 | 60,852 | 39,889,627 | 439,080,813 | 479,658,961 | $473.51 | 84.9% |
| Sonnet 4.5 | 293,003 | 19,832 | 6,557,293 | 80,529,641 | 87,399,769 | $49.93 | 9.0% |
| Haiku 4.5 | 26,722 | 433 | 406,735 | 1,720,852 | 2,154,742 | $0.71 | 0.1% |
| Opus 4.6 | 37,340 | 32,553 | 3,353,023 | 22,895,381 | 26,318,297 | $33.40 | 6.0% |
| stepfun/step-3.5-flash:free | 200 | 697 | 0 | 0 | 897 | $0.00 | 0.0% |

**Key findings from ccusage:**
1. **Opus 4.5 dominates:** 84.9% of total cost ($473.51)
2. **Cache read is massive:** 544M cache read tokens vs 985K input tokens (553x multiplier)
3. **Prompt caching is working:** High cache read ratio indicates effective caching
4. **Free model experiment visible:** One session used stepfun/step-3.5-flash:free (897 tokens, $0 cost)

## Token Consumption by Command (Ranked)

**Estimation method:**
- Command file word count × 1.3 (tokens per word avg) = base prompt tokens
- Context file estimates (STYLE-GUIDE, VERIFIED-RESEARCH, etc.)
- Typical output length based on command purpose
- Usage frequency based on video production workflow

| Rank | Command/Agent | Tier | Est. Input/Invoke | Est. Output/Invoke | Frequency | Monthly Invocations | Monthly Total | % Total Est. |
|------|---------------|------|-------------------|-------------------|-----------|---------------------|---------------|--------------|
| 1 | `/script` | Opus | 8,500 | 6,000 | Per video | 4 | 58,000 | 35% |
| 2 | `script-writer-v2` | Opus | 7,000 | 8,000 | Per video | 2 | 30,000 | 18% |
| 3 | `/research` | Sonnet | 2,200 | 3,000 | Per video | 4 | 20,800 | 13% |
| 4 | `/verify` | Sonnet | 1,500 | 1,000 | Per video | 4 | 10,000 | 6% |
| 5 | `fact-checker` | Sonnet | 1,800 | 1,200 | Per video | 3 | 9,000 | 5% |
| 6 | `/analyze` | Sonnet | 1,100 | 1,500 | Per video | 2 | 5,200 | 3% |
| 7 | `structure-checker-v2` | Sonnet | 1,600 | 1,200 | Per video | 2 | 5,600 | 3% |
| 8 | `/publish` | Sonnet | 1,200 | 1,800 | Per video | 2 | 6,000 | 4% |
| 9 | `/patterns` | Sonnet | 800 | 1,000 | Weekly | 4 | 7,200 | 4% |
| 10 | `/prep` | Haiku | 900 | 800 | Per video | 2 | 3,400 | 2% |
| 11 | `/engage` | Sonnet | 600 | 500 | Per video | 3 | 3,300 | 2% |
| 12 | `/discover` | Haiku | 700 | 600 | Per topic research | 3 | 3,900 | 2% |
| 13 | `/sources` | Haiku | 500 | 400 | Per video | 2 | 1,800 | 1% |
| 14 | `/status` | Haiku | 1,100 | 300 | Daily | 20 | 28,000 | 2% |
| 15 | `research-organizer` | Haiku | 600 | 500 | Per video | 2 | 2,200 | 1% |
| 16 | `claims-extractor` | Haiku | 700 | 800 | Per video | 2 | 3,000 | 2% |
| 17 | `diy-asset-creator` | Haiku | 500 | 600 | Per video | 1 | 1,100 | 1% |
| 18 | `/fix` | Haiku | 400 | 200 | As needed | 2 | 1,200 | 1% |
| 19 | `/help` | Haiku | 200 | 150 | Rare | 1 | 350 | 0% |
| | **TOTAL** | | | | | **68** | **166,050** | **100%** |

**Notes on estimates:**
- `/script` input includes: command prompt (1,787 words × 1.3 = 2,323 tokens) + STYLE-GUIDE.md (~4,500 tokens) + VERIFIED-RESEARCH.md (avg ~1,500-20,000 tokens, estimate 5,000) = ~11,823 tokens base, reduced to 8,500 for cache effects
- Output: 3,000-8,000 word scripts = ~4,000-10,000 tokens, estimated 6,000 avg
- Frequency assumptions: 4 videos per month (current production rate as of v1.6 milestone)
- `/status` invoked frequently during development (daily checks)

## Pareto Analysis

**Top 5 commands consume 75% of monthly tokens:**

| Rank | Command/Agent | Monthly Tokens | Cumulative % |
|------|---------------|----------------|--------------|
| 1 | `/script` | 58,000 | 35% |
| 2 | `script-writer-v2` | 30,000 | 53% |
| 3 | `/research` | 20,800 | 66% |
| 4 | `/verify` | 10,000 | 72% |
| 5 | `fact-checker` | 9,000 | 77% |

**80/20 breakdown:**
- **Top 3 commands** (16% of tasks) = **65% of tokens** (108,800 tokens)
- **Top 5 commands** (26% of tasks) = **77% of tokens** (127,800 tokens)
- **Bottom 14 tasks** (74% of tasks) = **23% of tokens** (38,250 tokens)

**Optimization targets:**
1. **Primary target:** `/script` and `script-writer-v2` (Opus tasks, 53% of total)
2. **Secondary target:** `/research`, `/verify`, `fact-checker` (Sonnet tasks, 24% of total)
3. **Tertiary target:** High-frequency low-value tasks like `/status` (2% of total but 20 invocations/month)

## Key Findings

### 1. Opus Dominance
- Opus 4.5 accounts for **84.9% of actual costs** ($473.51 of $557.55)
- `/script` and `script-writer-v2` are the primary Opus consumers
- **Cannot route Opus tasks to free models** without severe quality degradation (retention engineering, style matching requires best model)

### 2. Cache Efficiency
- Cache read tokens (544M) are **553x higher** than input tokens (985K)
- Prompt caching is working extremely well
- This reduces the actual optimization opportunity (we're not paying full price for repeat context)

### 3. Surprising Low Usage
- **Haiku tasks barely register** in actual costs (0.1% of total)
- Haiku is already optimized to near-zero cost
- **No optimization value in routing Haiku tasks** — they're already negligible

### 4. Sonnet is the Real Target
- Sonnet 4.5: 9.0% of costs ($49.93)
- If we can route 50% of Sonnet tasks to free models: **$25/month savings**
- Safe candidates: `/discover`, `/sources`, `/prep` (mechanical tasks currently on Haiku/Sonnet)

### 5. Frequency Multiplier
- `/status` is low per-invoke but high-frequency (20x/month)
- Moving `/status` to a free model could save ~2% of monthly tokens with zero quality risk

### 6. Free Model Precedent
- stepfun/step-3.5-flash:free was used successfully (897 tokens, $0 cost)
- Proves free model routing is technically working in Claude Code
- Need to expand usage systematically

## Optimization Opportunities (Ranked by Savings Potential)

| Opportunity | Target Tasks | Est. Monthly Savings | Risk Level | Priority |
|-------------|--------------|----------------------|------------|----------|
| **1. Route mechanical Sonnet tasks** | `/discover`, `/sources`, `/prep` | $15-20 | LOW | HIGH |
| **2. Route high-frequency simple tasks** | `/status`, `/help` | $3-5 | VERY LOW | HIGH |
| **3. Route mechanical agents** | `research-organizer`, `claims-extractor`, `diy-asset-creator` | $5-8 | LOW | MEDIUM |
| **4. Validation layer for Sonnet tasks** | `/analyze`, `/publish` after free model generates draft | $10-15 | MEDIUM | LOW |

**Total potential savings:** $33-48/month (6-9% of current costs)

**NOT viable:**
- ❌ **Opus tasks** (`/script`, `script-writer-v2`) — quality-critical, retention engineering requires best model
- ❌ **Local models** — insufficient RAM (14.9GB), no NVIDIA GPU, would compromise system stability
- ❌ **Complex reasoning tasks** (`/verify`, `fact-checker`) — source evaluation needs Claude-level reasoning

## Recommendations for Plan 02 (Routing Implementation)

### Phase 1: High-frequency low-risk (immediate)
1. Route `/status` to OpenRouter Gemini 2.0 Flash (free)
2. Route `/help` to OpenRouter Gemini 2.0 Flash (free)
3. Validate outputs match Claude quality

### Phase 2: Mechanical tasks (after validation)
1. Route `/discover` to OpenRouter Llama 3.3 70B (free)
2. Route `/sources` to OpenRouter Gemini 2.0 Flash (free)
3. Route `/prep` to OpenRouter Gemini 2.0 Flash (free)

### Phase 3: Agent routing (if Phase 2 succeeds)
1. Route `research-organizer` to free models
2. Route `claims-extractor` to free models
3. Route `diy-asset-creator` to free models

### Do NOT route (keep on Claude):
- `/script` (Opus) — channel's primary value, needs best model
- `script-writer-v2` (Opus) — retention engineering critical
- `/verify` (Sonnet) — source evaluation requires reasoning
- `fact-checker` (Sonnet) — fact-checking cannot be delegated to weaker models
- `structure-checker-v2` (Sonnet) — retention prediction needs intelligence
- `/research` (Sonnet) — research synthesis requires reasoning
- `/analyze` (Sonnet) — pattern analysis requires intelligence
- `/patterns` (Sonnet) — cross-video synthesis requires reasoning
- `/engage` (Sonnet) — comment responses need nuance and empathy
- `/publish` (Sonnet) — metadata generation has moderate creativity

---

**Next step:** Create ROUTING-CLASSIFICATION.md with per-task routing tiers and strategy decision.
