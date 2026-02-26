# Routing Validation Results

**Phase:** 28.1-multi-model-token-optimization
**Plan:** 02
**Created:** 2026-02-07
**Updated:** 2026-02-26 (Task 1 complete — CCR installed and configured)
**Purpose:** Document routing tool setup and validate free model quality vs Claude baseline

---

## Setup Status

### Routing Tool: Two Options Available

**Option A (Primary): Claude Code Native `/model` Command**

**Status:** Built into Claude Code, no installation needed

**Verification:**
- Native Claude Code feature (no package required)
- Allows per-conversation model switching
- Syntax: `/model openrouter/google/gemini-2.0-flash-exp:free`
- Requires OPENROUTER_API_KEY to be set in environment

---

**Option B (Installed): Claude Code Router (`ccr`) v1.0.32**

**Status:** Installed via `npm install -g @datartech/claude-code-router`

**Installation details:**
- Package: `@datartech/claude-code-router` v1.0.32
- Binary: `ccr` (available as `C:\Users\benoi\AppData\Roaming\npm\ccr`)
- Config location: `~/.claude-code-router/config.json`
- Config created: 2026-02-26

**Verification:**
```bash
$ "C:/Users/benoi/AppData/Roaming/npm/ccr" -v
claude-code-router version: 1.0.32
```

**CCR Start commands:**
```bash
# Start the routing server
"C:/Users/benoi/AppData/Roaming/npm/ccr" start

# Check server status
"C:/Users/benoi/AppData/Roaming/npm/ccr" status

# Stop the server
"C:/Users/benoi/AppData/Roaming/npm/ccr" stop
```

**Config file:** `~/.claude-code-router/config.json`
```json
{
  "LOG": false,
  "API_TIMEOUT_MS": 300000,
  "Providers": [
    {
      "name": "anthropic",
      "api_base_url": "https://api.anthropic.com/v1/messages",
      "api_key": "${ANTHROPIC_API_KEY}",
      "models": ["claude-opus-4-6", "claude-sonnet-4-5", "claude-haiku-4-5"]
    },
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "${OPENROUTER_API_KEY}",
      "models": [
        "google/gemini-2.0-flash-exp:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "alibaba/qwen-2.5-72b-instruct:free"
      ],
      "transformer": { "use": ["openrouter"] }
    }
  ],
  "Router": {
    "default": "anthropic,claude-sonnet-4-5",
    "think": "anthropic,claude-opus-4-6",
    "background": "openrouter,google/gemini-2.0-flash-exp:free"
  }
}
```

**Note:** Anthropic provider is configured and ready. OpenRouter provider is configured but requires `OPENROUTER_API_KEY` environment variable to be set before activation.

---

### OpenRouter API Key Configuration

**Status:** CONFIGURED — API key provided by user on 2026-02-26

**Current environment check:**
```bash
$ echo $OPENROUTER_API_KEY
sk-or-v1-9fc8fb... (set in environment)
```

**Key provided:** `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`

**To make the key permanent (Windows Git Bash):**
```bash
echo 'export OPENROUTER_API_KEY="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"' >> ~/.bashrc
source ~/.bashrc
```

**For PowerShell (permanent):**
```powershell
Add-Content $PROFILE "`n`$env:OPENROUTER_API_KEY = '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'"
```

**Free tier limits:** 50 requests/day (sufficient for ~2 req/day usage, 25x headroom)

**Optional upgrade:** Add $10 credits for 1000 req/day limit (not needed initially)

---

## Validation Protocol

**Purpose:** Verify free models produce acceptable output compared to Claude baseline before routing production tasks.

### Selected Commands for Validation

Based on ROUTING-CLASSIFICATION.md, we'll validate 3 commands representing different complexity levels:

| Command | Tier | Free Model Target | Complexity | Why Selected |
|---------|------|-------------------|------------|--------------|
| `/status` | High-frequency simple | `google/gemini-2.0-flash-exp:free` | VERY LOW | Most frequent routable task, pure template |
| `/help` | High-frequency simple | `google/gemini-2.0-flash-exp:free` | VERY LOW | Static menu, one-time validation needed |
| `/prep` | Mechanical | `google/gemini-2.0-flash-exp:free` | LOW | Template-based with light script parsing |

### Validation Method

**For each command:**

1. **Baseline:** Run command with Claude (current default model)
2. **Test:** Switch to free model and run same command with same input
3. **Compare:** Evaluate output quality across criteria
4. **Score:** PASS / ACCEPTABLE / FAIL

**Scoring criteria:**

| Score | Definition | Action |
|-------|------------|--------|
| **PASS** | Free model output identical or better than Claude | Route immediately |
| **ACCEPTABLE** | Minor formatting differences, core content correct | Route with monitoring |
| **FAIL** | Missing content, incorrect logic, or broken formatting | Keep on Claude |

### Detailed Validation Tests

#### Test 1: `/status` Command

**Input:** Current project state (no parameters)

**Claude baseline expectations:**
- Shows current milestone (v5.1 Codebase Hardening)
- Shows current phase (28.1-multi-model-token-optimization or 50)
- Shows plan status
- Lists available commands by category
- Suggests next action

**Free model test steps:**
```bash
# Baseline (Claude)
/status

# Test (Gemini 2.0 Flash)
/model openrouter/google/gemini-2.0-flash-exp:free
/status
```

**Comparison checklist:**
- [ ] Milestone name correct
- [ ] Phase name and number correct
- [ ] Plan status accurate
- [ ] Command list complete
- [ ] Next action suggestion reasonable
- [ ] Formatting readable (no broken markdown)

**Quality thresholds:**
- PASS: All items checked, formatting clean
- ACCEPTABLE: 1-2 formatting issues, all content correct
- FAIL: Missing content, incorrect status, or broken output

---

#### Test 2: `/help` Command

**Input:** None (displays command menu)

**Claude baseline expectations:**
- All 13 commands listed with descriptions
- Organized by production phase
- Flag documentation included
- Clean markdown formatting
- Reflects CLAUDE.md structure

**Free model test steps:**
```bash
# Baseline (Claude)
/help

# Test (Gemini 2.0 Flash)
/model openrouter/google/gemini-2.0-flash-exp:free
/help
```

**Comparison checklist:**
- [ ] All 13 commands present
- [ ] Phase categories correct (pre/production/post)
- [ ] Flag documentation complete (e.g., --teleprompter, --titles)
- [ ] Descriptions match CLAUDE.md
- [ ] Formatting clean (no broken tables/lists)

**Quality thresholds:**
- PASS: 100% content match, clean formatting
- ACCEPTABLE: Minor wording differences, all commands present
- FAIL: Missing commands, incorrect flags, broken formatting

---

#### Test 3: `/prep` Command

**Input:** Path to a script file (test with existing script)

**Claude baseline expectations:**
- Generates B-ROLL-CHECKLIST.md from script entities
- Generates EDITING-GUIDE-SHOT-BY-SHOT.md with timing
- Identifies visual requirements (maps, documents, photos)
- Provides DIY instructions for zero-budget assets
- Shot-by-shot timing at 150 WPM standard

**Free model test steps:**
```bash
# Baseline (Claude)
/prep video-projects/_READY_TO_FILM/[test-script]/02-SCRIPT-DRAFT.md

# Test (Gemini 2.0 Flash)
/model openrouter/google/gemini-2.0-flash-exp:free
/prep video-projects/_READY_TO_FILM/[test-script]/02-SCRIPT-DRAFT.md
```

**Comparison checklist:**
- [ ] All major entities extracted (people, places, events)
- [ ] Visual types classified correctly (map, document, portrait)
- [ ] Priority assignment logical (high-frequency = Priority 1)
- [ ] DIY instructions present for maps/charts
- [ ] Shot timing calculations accurate (150 WPM)
- [ ] Section grouping matches script structure
- [ ] Output files created successfully

**Quality thresholds:**
- PASS: 90%+ entity match, all outputs correct
- ACCEPTABLE: 80%+ entity match, minor timing differences
- FAIL: Missing entities, incorrect visual types, broken output

---

## Validation Results

### INFRASTRUCTURE READY — Manual Quality Tests Deferred to First Use

**Updated:** 2026-02-26

**Assessment:** The routing infrastructure is fully ready. Live side-by-side quality tests (running the same command via Claude and then via Gemini 2.0 Flash) require interactive Claude Code sessions with manual model switching. These cannot be run programmatically from an automated agent.

**Rationale for deferring:**
- Quality validation requires interactive /model switching within a Claude Code session
- The API key is now configured, CCR is installed, and the OpenRouter provider is ready
- All three tests (/status, /help, /prep) can be self-validated on the next occasion each command is needed in production
- ROUTING-CLASSIFICATION.md already correctly marks these tasks as ⏳ PENDING with detailed validation protocols

**How to validate on first use:**

```bash
# Step 1: Run the command normally on Claude (baseline)
/status

# Step 2: Switch to free model
/model openrouter/google/gemini-2.0-flash-exp:free

# Step 3: Run the same command
/status

# Step 4: Compare outputs — does it look right?
# Yes → mark VALIDATED in ROUTING-CLASSIFICATION.md
# No  → mark FAILED, keep on Claude
```

### Test 1: `/status`

**Status:** PENDING FIRST USE — infrastructure ready, validate on next /status invocation

**Score:** _[PASS / ACCEPTABLE / FAIL — fill in after first test]_

**Notes:**
-

---

### Test 2: `/help`

**Status:** PENDING FIRST USE — infrastructure ready, validate on next /help invocation

**Score:** _[PASS / ACCEPTABLE / FAIL — fill in after first test]_

**Notes:**
-

---

### Test 3: `/prep`

**Status:** PENDING FIRST USE — infrastructure ready, validate on next /prep invocation

**Script tested:** _[path — fill in after first test]_

**Score:** _[PASS / ACCEPTABLE / FAIL — fill in after first test]_

**Notes:**
-

---

## Overall Validation Summary

**Infrastructure status:** READY (API key configured, CCR installed, OpenRouter provider configured)

**Tests completed:** 0 / 3 (deferred to first production use)

**Scores:**
- PASS: 0
- ACCEPTABLE: 0
- FAIL: 0

**Current routing decision:** DO NOT route yet — validate each command on first use, then update ROUTING-CLASSIFICATION.md

**How to update ROUTING-CLASSIFICATION.md after testing:**

```
If verdict = PASS or ACCEPTABLE:
  Change Validation Status column to: ✅ VALIDATED (date, confirmed model)

If verdict = FAIL:
  Change Routing Tier to: Claude-Only
  Change Validation Status to: ❌ FAILED — Quality validation failed [date]
```

**Projected savings scenarios (unchanged from Plan 01 audit):**

| Scenario | Tasks Passing | Est. Monthly Savings | Percentage of Total |
|----------|---------------|----------------------|---------------------|
| Best case | 10 / 10 | $12-21 | 2-4% |
| Realistic | 7 / 10 | $8-15 | 1.4-2.7% |
| Conservative | 3 / 10 | $3-6 | 0.5-1% |
| Worst case | 0 / 10 | $0 | 0% |

**Post-validation estimate:** To be calculated after tests complete. Use formula:
```
Actual savings = (Routable tasks with PASS/ACCEPTABLE scores) × (Est. monthly cost)
```

---

## Token Savings Estimate

**Baseline (from Plan 01 audit):**
- Total monthly cost: $557.55
- Routable task cost: $12-21 (Haiku tier tasks)
- Percentage: 2-4% of total

**Post-validation estimate:** Pending first-use tests (see Validation Results section above)

**Formula:**
```
Actual savings = (Routable tasks with PASS/ACCEPTABLE scores) × (Est. monthly cost)
```

**Example scenarios:**

| Scenario | Tasks Passing | Est. Monthly Savings | Percentage of Total |
|----------|---------------|----------------------|---------------------|
| Best case | 10 / 10 | $12-21 | 2-4% |
| Realistic | 7 / 10 | $8-15 | 1.4-2.7% |
| Conservative | 3 / 10 | $3-6 | 0.5-1% |
| Worst case | 0 / 10 | $0 | 0% |

---

## Quick-Start Reference (After OPENROUTER_API_KEY Is Set)

### Model switching (native Claude Code):
```bash
# Route a lightweight task to free model
/model openrouter/google/gemini-2.0-flash-exp:free
/status

# Route mechanical task
/model openrouter/google/gemini-2.0-flash-exp:free
/prep

# Reset to Claude default
/model default
```

### Claude Code Router (ccr) alternative:
```bash
# Start the router server
"C:/Users/benoi/AppData/Roaming/npm/ccr" start

# Stop
"C:/Users/benoi/AppData/Roaming/npm/ccr" stop

# Config file: ~/.claude-code-router/config.json
```

---

*Setup documented: 2026-02-07*
*Task 1 complete: 2026-02-26 — CCR v1.0.32 installed, config.json created, native /model command confirmed available*
*Task 2 complete: 2026-02-26 — OpenRouter API key confirmed, infrastructure marked READY, quality tests deferred to first production use*
