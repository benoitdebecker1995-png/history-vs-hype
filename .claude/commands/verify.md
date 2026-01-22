---
description: Fact-check scripts, extract claims, detect simplifications (Production Phase 2)
---

# /verify - Verification Entry Point

Fact-check scripts, extract claims from transcripts, or run simplification detection. This command consolidates all verification workflows.

## Usage

```
/verify                      # Interactive: fact-check current project
/verify --script [project]   # Fact-check a script
/verify --extract [file]     # Extract claims from transcript
/verify --simplify [project] # Run simplification detection only
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--script` | Full fact-check verification | `/verify --script 19-flat-earth-medieval-2025` |
| `--extract` | Extract claims from YouTube transcript | `/verify --extract transcript.vtt` |
| `--simplify` | Simplification detection only | `/verify --simplify 19-flat-earth-medieval-2025` |
| `--from-transcript` | Extract + fact-check workflow | `/verify --from-transcript video-url` |

---

## FACT-CHECK WORKFLOW (`--script` or default)

Comprehensive fact-checking using the History vs Hype protocol.

### Step 1: Identify the Script

- Read SCRIPT.md from project folder
- Or user pastes script content

### Step 2: Extract All Factual Claims

**Categories:**
- **Statistics & numbers** (dates, percentages, quantities, distances)
- **Direct quotes** (from historical figures, documents, politicians)
- **Historical events** (battles, treaties, laws, decisions)
- **Cause-effect claims** (X led to Y, X caused Z)
- **Attribution claims** (who said/wrote/did what)

### Step 3: Organize by Priority

**TIER 1 - SMOKING GUN EVIDENCE (Must verify before filming):**
- Primary document quotes
- Key statistics that form the thesis
- Viral quotes from current figures
- Claims that would discredit the video if wrong

**TIER 2 - SUPPORTING CLAIMS (Need 2+ sources):**
- Historical event details
- Timeline/date claims
- Attribution claims
- Academic consensus statements

**TIER 3 - CONTEXTUAL (Should verify):**
- Background information
- Comparative data
- Secondary quotes
- Common knowledge claims

**CONTESTED CLAIMS (Present both sides):**
- Any claim where sources disagree
- Claims that require "some historians argue..."
- Interpretation-dependent statements

### Step 4: Check Against Source Hierarchy

**Most Reliable (Tier 1):**
- Primary documents (treaties, census data, government archives)
- Peer-reviewed academic publications
- Expert historians specializing in the topic

**Use with Caution:**
- Respected journalists with expertise
- International organization reports
- Declassified government documents (note potential bias)

**Flag These:**
- Opinion pieces without sources
- Claims without attribution
- Statistics without clear methodology
- "Common knowledge" that can't be verified

### Step 5: Run Simplification Detection

**CRITICAL: Scan script for simplification patterns**

Read `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md` and check for:

| Rule | Pattern | Severity |
|------|---------|----------|
| 1 | Territorial claims without boundaries/percentages | CRITICAL |
| 2 | Present tense for past positions | CRITICAL |
| 3 | Absolutist language without qualifiers | IMPORTANT |
| 4 | Statistics without context | IMPORTANT |
| 5 | Contested claims as facts | IMPORTANT |
| 6 | Quotes without specific attribution | CRITICAL |
| 7 | Complex events oversimplified | RECOMMENDED |
| 8 | Vague timelines | RECOMMENDED |

### Step 6: Generate Fact-Check Report

```markdown
# FACT-CHECK REPORT: [Script Title]

## SIMPLIFICATION FLAGS

### CRITICAL - Fix before filming
[List Rule 1, 2, 6 violations with suggested fixes]

### IMPORTANT - Should fix
[List Rule 3, 4, 5 violations with suggested fixes]

### RECOMMENDED - Improves clarity
[List Rule 7, 8 violations with suggested fixes]

## VERIFIED CLAIMS (Source confirmed)
1. [Claim] - Source: [Exact citation]
2. [Claim] - Source: [Exact citation]

## NEEDS VERIFICATION (Missing or weak sources)
1. [Claim] - Issue: [What's missing/unclear]
2. [Claim] - Issue: [What's missing/unclear]

## INCORRECT OR MISLEADING
1. [Claim] - Problem: [What's wrong]
   Correction: [Accurate information]

## CONTESTED CLAIMS (Must acknowledge both sides)
1. [Claim] - Disagreement: [Who says what]
   Recommendation: [How to present fairly]

## MISSING CONTEXT
1. [Claim] - Additional context needed: [What's missing]

## OVERALL ASSESSMENT
- Ready to film? [YES/NO]
- Critical simplifications: [Number]
- Source issues: [Number]
- Recommendations: [What needs to be fixed/added]
```

### Step 7: Pre-Production Checklist

Before approving for filming:
- [ ] Every number has a source
- [ ] Every quote verified from original
- [ ] Contested claims clearly labeled
- [ ] At least 2 sources for each major point
- [ ] No logical fallacies in arguments
- [ ] Counter-evidence acknowledged where relevant
- [ ] **Simplification check complete** (all CRITICAL flags resolved)
- [ ] Territorial claims have specific boundaries/percentages
- [ ] Present-tense statements have temporal accuracy
- [ ] Attributions have specific sources (video timestamp, document, interview date)

### Output Location

`video-projects/[project]/03-FACT-CHECK-VERIFICATION.md`

**Proactive suggestion:** "Fact-check complete. [APPROVED/X issues to fix]. Run `/prep` for filming preparation."

---

## CLAIMS EXTRACTION (`--extract`)

Extract factual claims from YouTube video transcript for systematic fact-checking.

### Input

- YouTube video URL (will fetch transcript)
- Or path to transcript file (.vtt, .srt, .txt)

### Process

1. **Fetch/read transcript**
2. **Extract ALL factual claims:**
   - Dates (when events occurred)
   - Statistics (death tolls, population figures, numbers)
   - Quotes (who said what, with attribution)
   - Cause-effect relationships ("X caused Y")
   - Historical interpretations (contested claims)
   - Geographic claims (territorial boundaries, locations)

3. **Categorize by priority:**
   - **Priority 1:** Major claims central to video's argument
   - **Priority 2:** Supporting claims and context
   - **Priority 3:** Minor details

4. **Note red flags:**
   - Claims without sourcing
   - Contested framing presented as settled
   - Potential misattributions

### Output

```markdown
# Claims Extraction: [Video Title]

**Video:** [Title]
**URL:** [YouTube URL]
**Creator:** [Channel name]
**Duration:** [Length]
**Extraction Date:** [Today]

## PRIORITY 1: Major Claims (Must Fact-Check)

### Claim 1.1: [Category]
**Exact Quote:** "[Verbatim from video]"
**Timestamp:** [MM:SS]

**Factual Elements to Verify:**
- Date: [Specific date claimed]
- Number: [Specific statistic]
- Source attribution: [If they cite a source]

**Verification Needed:**
- [ ] Verify date accuracy
- [ ] Verify number/statistic
- [ ] Check if source cited actually supports claim

**Potential Red Flags:**
- [Any obvious issues]

[Continue for all claims...]

## SUMMARY

**Total Claims:** [Number]
- Priority 1: [X] major claims
- Priority 2: [X] supporting claims
- Priority 3: [X] minor details
```

### Output Location

`video-projects/[project]/CLAIMS-TO-VERIFY.md`

---

## SIMPLIFICATION DETECTION ONLY (`--simplify`)

Run simplification detection without full fact-check.

**Use when:** Quick scan before filming, or after revisions.

### Process

1. Read SCRIPT.md
2. Apply all 8 simplification rules
3. Generate severity report only

### Output

Quick report with only simplification flags (no verification status).

---

## NotebookLM Integration

If user has NotebookLM research notebook, provide fact-check prompt:

```
I need to fact-check these specific claims from my script:

1. CLAIM: "[Claim from script]"
   Script says: "[Exact wording]"
   Verify: Is this accurate? What do sources say?

2. CLAIM: "[Next claim]"
   Script says: "[Exact wording]"
   Verify: [Verification question]

For each claim:
- Exact quote from sources with page number
- VERIFIED / INACCURATE / PARTIALLY TRUE
- Any nuance or context the script is missing
```

---

## Key Principle

**If you can't verify it with 2+ credible sources, it doesn't go in the script.**

Historical integrity is the channel's core value. Better to cut a claim than to include something unverified.

---

## Reference Files

- **Simplification rules:** `.claude/REFERENCE/FACT-CHECK-SIMPLIFICATION-RULES.md`
- **Fact-check template:** `.claude/templates/03-FACT-CHECK-VERIFICATION-TEMPLATE.md`
- **Fact-checker agent:** `.claude/agents/fact-checker.md`

---

## Absorbed Commands

This command consolidates functionality from:
- `/fact-check` - Full fact-check verification
- `/extract-claims` - Claims extraction from transcripts

All original functionality preserved through flags.
