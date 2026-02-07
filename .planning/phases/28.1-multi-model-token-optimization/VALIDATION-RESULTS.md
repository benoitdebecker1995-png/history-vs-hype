# Routing Validation Results

**Phase:** 28.1-multi-model-token-optimization
**Plan:** 02
**Created:** 2026-02-07
**Purpose:** Document routing tool setup and validate free model quality vs Claude baseline

---

## Setup Status

### Routing Tool: Native Claude Code `/model` Command

**Status:** ✅ AVAILABLE (built into Claude Code, no installation needed)

**Verification:**
- The `/model` command is a native Claude Code feature
- Allows per-conversation model switching
- Syntax: `/model openrouter/google/gemini-2.0-flash-exp:free`

### OpenRouter API Key Configuration

**Status:** ❌ NOT CONFIGURED

**Current environment check:**
```bash
$ echo $OPENROUTER_API_KEY
(empty - environment variable not set)
```

**What you need to do:**

1. **Create OpenRouter account:**
   - Go to https://openrouter.ai
   - Sign up (free tier is sufficient)

2. **Generate API key:**
   - Navigate to Settings → API Keys
   - Generate new API key (starts with `sk-or-v1-...`)
   - Copy the key

3. **Set environment variable (Windows):**

   **For current session (temporary):**
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-YOUR_KEY_HERE"
   ```

   **For permanent setup (Git Bash ~/.bashrc):**
   ```bash
   echo 'export OPENROUTER_API_KEY="sk-or-v1-YOUR_KEY_HERE"' >> ~/.bashrc
   source ~/.bashrc
   ```

   **For PowerShell:**
   ```powershell
   $env:OPENROUTER_API_KEY = "sk-or-v1-YOUR_KEY_HERE"
   ```

   **For permanent PowerShell (profile):**
   ```powershell
   Add-Content $PROFILE "`n`$env:OPENROUTER_API_KEY = 'sk-or-v1-YOUR_KEY_HERE'"
   ```

4. **Verify setup:**
   ```bash
   echo $OPENROUTER_API_KEY | head -c 20
   # Should show: sk-or-v1-...
   ```

5. **Test model switching in Claude Code:**
   ```
   /model openrouter/google/gemini-2.0-flash-exp:free
   /status
   ```

**Free tier limits:** 50 requests/day (sufficient for 2 req/day usage, 25x headroom)

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
| **PASS** | Free model output identical or better than Claude | ✅ Route immediately |
| **ACCEPTABLE** | Minor formatting differences, core content correct | ✅ Route with monitoring |
| **FAIL** | Missing content, incorrect logic, or broken formatting | ❌ Keep on Claude |

### Detailed Validation Tests

#### Test 1: `/status` Command

**Input:** Current project state (no parameters)

**Claude baseline expectations:**
- Shows current milestone (v1.6 Click & Keep)
- Shows current phase (28.1-multi-model-token-optimization)
- Shows plan status (Plan 01 complete, Plan 02 in progress)
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

### Test 1: `/status`

**Status:** ⏳ PENDING USER TESTING

**Instructions:**
1. Set OPENROUTER_API_KEY environment variable (see setup section)
2. Run Claude baseline: `/status`
3. Switch to free model: `/model openrouter/google/gemini-2.0-flash-exp:free`
4. Run test: `/status`
5. Compare outputs using checklist above
6. Document score below

**Score:** _[PASS / ACCEPTABLE / FAIL]_

**Notes:**
-

---

### Test 2: `/help`

**Status:** ⏳ PENDING USER TESTING

**Instructions:**
1. Run Claude baseline: `/help`
2. Switch to free model: `/model openrouter/google/gemini-2.0-flash-exp:free`
3. Run test: `/help`
4. Compare outputs using checklist above
5. Document score below

**Score:** _[PASS / ACCEPTABLE / FAIL]_

**Notes:**
-

---

### Test 3: `/prep`

**Status:** ⏳ PENDING USER TESTING

**Instructions:**
1. Identify a test script (suggest: any script in _READY_TO_FILM/)
2. Run Claude baseline: `/prep [path-to-script]`
3. Switch to free model: `/model openrouter/google/gemini-2.0-flash-exp:free`
4. Run test: `/prep [path-to-script]`
5. Compare B-ROLL-CHECKLIST.md and EDITING-GUIDE-SHOT-BY-SHOT.md
6. Document score below

**Script tested:** _[path]_

**Score:** _[PASS / ACCEPTABLE / FAIL]_

**Notes:**
-

---

## Overall Validation Summary

**Tests completed:** 0 / 3

**Scores:**
- PASS: 0
- ACCEPTABLE: 0
- FAIL: 0

**Routing decision:**

_[To be completed after user testing]_

**If all tests PASS or ACCEPTABLE:**
- ✅ Proceed with routing 10 tasks from ROUTING-CLASSIFICATION.md
- Estimated savings: $12-21/month
- Risk level: LOW
- Rollout: Gradual (high-frequency simple → mechanical → agents)

**If any test FAILS:**
- ❌ Remove failed task from routable list
- Document failure reason
- Update ROUTING-CLASSIFICATION.md with FAILED validation status
- Recalculate savings estimate

**If all tests FAIL:**
- ❌ Keep all tasks on Claude
- Phase still succeeds (documentation value)
- Finding: Free models not suitable for this workflow
- Estimated savings: $0/month

---

## Token Savings Estimate

**Baseline (from Plan 01 audit):**
- Total monthly cost: $557.55
- Routable task cost: $12-21 (Haiku tier tasks)
- Percentage: 2-4% of total

**Post-validation estimate:**

_[To be calculated after testing]_

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

## Next Steps

1. **User action required:** Set OPENROUTER_API_KEY environment variable
2. **User action required:** Run validation tests (3 commands)
3. **User action required:** Document scores in this file
4. **Claude action:** Update ROUTING-CLASSIFICATION.md with validation_status column
5. **Claude action:** Calculate final savings estimate
6. **User decision:** Approve routing strategy or request changes

**Estimated testing time:** 15-20 minutes

**Decision criteria:** Is the token savings worth the complexity of maintaining model switching?

---

*Setup documented: 2026-02-07*
*Awaiting user validation testing*
