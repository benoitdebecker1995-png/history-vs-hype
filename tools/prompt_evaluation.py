"""
Prompt Evaluation Suite for History vs Hype

Uses prompttools to evaluate and compare prompts for:
1. Script generation quality
2. Fact-checking accuracy
3. Claim extraction completeness
4. Voice consistency with channel style

Run with: python tools/prompt_evaluation.py
Requires: ANTHROPIC_API_KEY environment variable
"""

import os
import json
from pathlib import Path

# Check for API key
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("Warning: ANTHROPIC_API_KEY not set. Set it to run live evaluations.")
    print("You can still review the prompt templates below.\n")

# ============================================================================
# EVALUATION PROMPTS FOR HISTORY VS HYPE
# ============================================================================

# Sample test cases for evaluation
TEST_CASES = {
    "territorial_topic": {
        "topic": "Sykes-Picot Agreement",
        "modern_hook": "Syria's 2024 civil war collapse",
        "extreme_a": "Sykes-Picot caused all Middle East problems",
        "extreme_b": "Colonial borders were rational administrative decisions",
    },
    "ideological_topic": {
        "topic": "Dark Ages myth",
        "modern_hook": "PragerU curriculum in Florida schools 2024",
        "extreme_a": "Christianity destroyed classical knowledge",
        "extreme_b": "Medieval period was a golden age of innovation",
    },
    "fact_check_claim": {
        "claim": "The Holocaust killed 6 million Jews",
        "source_type": "primary",
        "expected_verification": "verified",
    },
}

# ============================================================================
# PROMPT VARIANTS TO EVALUATE
# ============================================================================

SCRIPT_PROMPTS = {
    "baseline": '''You are a script writer for History vs Hype, a YouTube channel that debunks historical myths.

Write a video script about: {topic}
Modern hook: {modern_hook}

Requirements:
- 8-12 minutes long
- Use academic sources
- Include both perspectives
''',

    "kraut_style": '''You are a script writer for History vs Hype, a YouTube channel that uses the Kraut style of deep causal chains and comparative analysis.

Write a video script about: {topic}
Modern hook: {modern_hook}

STYLE REQUIREMENTS:
1. Open with sweep-then-specifics: Start with sweeping historical pattern, ground in specific examples
2. Deep causal chains: Use "consequently," "thereby," "which meant that," "as a result"
3. Comparative analysis: "While in Europe [X], in the Middle East [opposite]"
4. Real quotes with page numbers from academic sources
5. Explain WHY things happened, not just WHAT

STRUCTURE:
- Payoff-first: Show modern consequences BEFORE explaining historical causes
- Both extremes pattern: Frame Extreme A ({extreme_a}) and Extreme B ({extreme_b}), then show why both are wrong
- Evidence stacking: 3-4 examples building the pattern
- Modern relevance every 90 seconds

Target: 10-15 minutes, as long as needed for the topic
''',

    "alex_oconnor_style": '''You are a script writer for History vs Hype. Write in the Alex O'Connor (CosmicSkeptic) style - conversational authority with intellectual honesty.

Topic: {topic}
Modern hook: {modern_hook}

VOICE REQUIREMENTS:
1. Conversational think-aloud: "I don't know about this. Let me know what you think..."
2. Intellectual humility: "I'm not super convinced by this, mostly because..."
3. Define every term immediately in same sentence
4. Engage with counterarguments directly - steelman the opposition
5. Admit uncertainty where appropriate

STRUCTURE:
- Frame both extreme narratives:
  - Extreme A: {extreme_a}
  - Extreme B: {extreme_b}
- Explicitly state: "I think both of these are wrong, or at least oversimplified"
- Build argument incrementally with self-correction
- Return to both extremes in conclusion

Use real academic quotes with page numbers. Be honest about what the evidence does and doesn't show.
''',

    "optimized_v1": '''You are writing for History vs Hype, a YouTube channel that debunks historical myths using primary sources.

TOPIC: {topic}
MODERN HOOK: {modern_hook}

THE TWO EXTREME NARRATIVES (both are wrong):
- Extreme A: {extreme_a}
- Extreme B: {extreme_b}

=== HARD CONSTRAINTS ===
1. VERBATIM FACTS ONLY: Every statistic, quote, and date must come from verified sources with page numbers
2. LOGIC BRIDGE: Every A→B transition must have explicit causal connection ("consequently," "which meant that")
3. AUDIENCE ZERO: Define every technical term in the same sentence it appears
4. READ-ALOUD: Every sentence must sound natural when spoken

=== STRUCTURE ===

**HOOK (0:00-0:30)**
- Open with specific modern event with date and named person
- "On [date], [specific person] [specific action]..."
- Establish stakes: why this matters NOW

**BOTH EXTREMES (0:30-1:30)**
- Frame Extreme A clearly
- Frame Extreme B clearly
- "I think both of these are wrong. Here's why."

**EVIDENCE SECTION (1:30-8:00)**
- Payoff-first: Show consequences before causes
- Real quotes: "According to [Author] in [Book], page [X]: '[exact quote]'"
- Modern connection every 90 seconds
- Deep causal chains explaining mechanisms
- Acknowledge what opposing side gets right

**SYNTHESIS (8:00-10:00)**
- Return to both extremes
- "Extreme A is dangerous because..."
- "Extreme B is dangerous because..."
- Nuanced reality with evidence
- Why accurate history matters

**CTA (10:00-10:30)**
- Sources in description
- Subscribe for evidence-based history

=== OUTPUT FORMAT ===
Include [DOCUMENT: source] markers for B-roll
Include [MODERN HOOK] markers every 90 seconds
Include timestamps throughout
''',

    "optimized_v2": '''You are writing for History vs Hype, a YouTube channel using patterns from successful creators (Kraut, Alex O'Connor, Knowing Better, Historia Civilis, Shaun, Fall of Civilizations).

TOPIC: {topic}
MODERN HOOK: {modern_hook}

THE TWO EXTREME NARRATIVES (both are wrong):
- Extreme A: {extreme_a}
- Extreme B: {extreme_b}

=== CHANNEL-SPECIFIC TECHNIQUES ===

**From Knowing Better - Forensic Source Verification:**
- Quote the distortion → Ask "what's missing?" → Show full context → Reveal manipulation
- "So where did they get that number? Let's trace it to the source..."

**From Historia Civilis - Precise Detail Deployment:**
- "Using the sources, we can identify five key provisions. Number one..."
- "Do you see what they did there?"

**From Shaun - Document-First:**
- "Here's what the document actually says: [SHOW on screen]"
- "Notice what's NOT in this document: any mention of..."

**From Kraut - Deep Causal Chains:**
- Use: "consequently," "thereby," "which meant that," "as a result"
- "While in Europe [X], in [region] [opposite happened]"

**From Alex O'Connor - Intellectual Humility:**
- "I'm not entirely sure about this, but..."
- "The strongest version of this argument is..."
- Define every term immediately: "[Term]—[definition in same breath]"

**From Fall of Civilizations - Evidence Stacking:**
- "We now have that data. [Source 1] shows... [Source 2] shows... [Source 3] shows..."
- Reject single-cause explanations explicitly

=== THE "SPREADSHEET ANGLE" (Subscriber Growth) ===
Show HOW things work (mechanisms), not just WHY they happened (politics):
- Treaties: "what Article 3 actually says" not "why they signed"
- Borders: "the exact coordinates" not "the conflict"

=== VOICE REQUIREMENTS ===

**Natural Fillers (use 3-5):** "basically," "pretty," "sort of," "look," "honestly"

**Think-Aloud Moments (use 2-3):**
- "This is where it gets complicated..."
- "I've been wrestling with this question..."

**Conversational Quote Intros:**
- ✅ "The treaty actually says..."
- ❌ "Quote: 'The treaty states...'"

**Spoken Dates:**
- ✅ "On June 16th, 2014"
- ❌ "June 16, 2014."

=== STRUCTURE ===

**HOOK (0:00-0:30)** - Document-first or modern event
- Show the map/document IMMEDIATELY (not after context)
- "This is the map they ignored. This is what they drew instead."

**BOTH EXTREMES (0:30-1:30)**
- "One side says [Extreme A]. The other insists [Extreme B]."
- "They're both wrong—and the actual evidence is more interesting."

**EVIDENCE (1:30-8:00)** - Payoff before 1:11!
- Real quotes with page numbers throughout
- [DOCUMENT: source] markers for B-roll
- Causal chains explaining mechanisms
- Modern callback every 90 seconds

**STEELMANNING (Required - 30-60 seconds)**
- "To be fair to [opponent], they're not entirely wrong about [point]."
- Engage with their BEST evidence, not strawman

**SYNTHESIS (8:00-10:00)**
- Return to both extremes with new understanding
- "Do you see what they did there?" moment
- Why accurate history matters today

=== OUTPUT FORMAT ===
Include [DOCUMENT: source] markers for B-roll
Include [MODERN HOOK] markers every 90 seconds
Mark steelmanning section clearly
Include timestamps throughout
''',
}

FACT_CHECK_PROMPTS = {
    "baseline": '''Fact-check this claim: {claim}

Is it true or false? Provide sources.
''',

    "tiered_verification": '''You are a fact-checker for History vs Hype using the tiered source hierarchy.

CLAIM TO VERIFY: {claim}

=== SOURCE HIERARCHY ===
**Tier 1 (Most Reliable):**
- Primary documents (treaties, census data, government archives)
- Peer-reviewed academic publications (prioritize 2010-present)
- Expert historians specializing in the topic

**Tier 2:**
- Respected journalists with expertise
- International organization reports
- Declassified government documents (note potential bias)

**Tier 3:**
- Credible news sources (verify with multiple sources)
- Documentary evidence (verify authenticity)

=== VERIFICATION PROCESS ===
1. Search for Tier 1 sources first
2. Require 2+ independent sources for major claims
3. Note any contested aspects
4. Flag if claim needs qualification

=== OUTPUT FORMAT ===
**Verdict:** [VERIFIED / UNVERIFIABLE / FALSE / NEEDS QUALIFICATION]
**Confidence:** [HIGH / MEDIUM / LOW]
**Sources:**
- [Source 1 with full citation]
- [Source 2 with full citation]
**Notes:** [Any caveats or context needed]
''',

    "simplification_detection": '''You are a fact-checker for History vs Hype with simplification detection.

CLAIM TO VERIFY: {claim}

=== VERIFICATION ===
Check against Tier 1 sources (primary documents, peer-reviewed academics).

=== SIMPLIFICATION DETECTION ===
Check for these common errors:

🔴 CRITICAL FLAGS:
1. TERRITORIAL CLAIMS without specific boundaries/percentages
2. PRESENT-TENSE STATEMENTS that may have changed
3. VAGUE ATTRIBUTIONS ("historians say" without naming who)
4. ROUND NUMBERS that should be specific
5. CAUSATION claims without mechanism explanation
6. ABSOLUTE LANGUAGE ("all," "never," "always")
7. MISSING TIMEFRAMES for evolving situations
8. UNSOURCED QUOTES (no document/timestamp/date)

=== OUTPUT ===
**Claim:** {claim}
**Verdict:** [VERIFIED / FALSE / OVERSIMPLIFIED / NEEDS CONTEXT]
**Simplification Flags:** [List any 🔴 flags triggered]
**Corrected Version:** [If oversimplified, provide accurate version]
**Sources:** [Full citations]
''',
}

CLAIM_EXTRACTION_PROMPTS = {
    "baseline": '''Extract all factual claims from this text that can be fact-checked.

TEXT: {text}
''',

    "categorized_extraction": '''Extract all factual claims from this transcript for systematic fact-checking.

TEXT: {text}

=== EXTRACTION CATEGORIES ===

1. **STATISTICAL CLAIMS**
   - Numbers, percentages, dates
   - Population figures, casualties, distances

2. **CAUSAL CLAIMS**
   - "X caused Y"
   - "Because of X, Y happened"

3. **QUOTE ATTRIBUTIONS**
   - Who said what
   - Document citations

4. **HISTORICAL EVENTS**
   - What happened, when, where
   - Sequence of events

5. **DEFINITIONAL CLAIMS**
   - "X means Y"
   - Legal/technical definitions

=== OUTPUT FORMAT ===
For each claim:
```
CLAIM: [Exact claim from text]
CATEGORY: [Statistical/Causal/Quote/Event/Definition]
VERIFIABLE: [Yes/No/Partially]
PRIORITY: [High/Medium/Low based on video impact]
SOURCE NEEDED: [Type of source required to verify]
```
''',
}

VOICE_CHECK_PROMPTS = {
    "baseline": '''Does this script sound natural for a YouTube video?

SCRIPT: {script}
''',

    "channel_voice_check": '''Analyze whether this script matches the History vs Hype channel voice based on patterns from successful channels (Kraut, Alex O'Connor, Knowing Better, Historia Civilis, Shaun, Fall of Civilizations).

SCRIPT: {script}

=== VOICE CHECKLIST (Score 1 point each) ===

**1. Both Extremes Pattern (CRITICAL):**
- [ ] Opens with BOTH extreme narratives clearly framed
- [ ] Explicitly says "both are wrong" or equivalent
- [ ] Returns to both extremes in conclusion with new understanding

**2. Natural Fillers (Need 3-5 throughout):**
- [ ] "basically"
- [ ] "pretty" (as intensifier)
- [ ] "sort of" / "kind of"
- [ ] "look"
- [ ] "I mean"
- [ ] "honestly"

**3. Think-Aloud Moments (Alex O'Connor - Need 2-3):**
- [ ] "I'm not entirely sure about this, but..."
- [ ] "This is where it gets complicated..."
- [ ] "I've been wrestling with this question..."
- [ ] "I don't know about this. Let me know what you think."

**4. Signature Phrases (Need 1-2):**
- [ ] "Do you see what they did there?" (Historia Civilis)
- [ ] "And this is where it gets interesting"
- [ ] "So what went wrong?"
- [ ] "However, when we actually look at..."

**5. Steelmanning Section (Knowing Better - REQUIRED):**
- [ ] "To be fair to [opponent]..."
- [ ] "The strongest version of this argument is..."
- [ ] Actually engages with best opposing evidence

**6. Causal Chain Language (Kraut):**
- [ ] "consequently"
- [ ] "thereby"
- [ ] "which meant that"
- [ ] "as a result"

**7. Conversational Quote Introductions:**
- ✅ "The treaty actually says..."
- ✅ "Here's the exact language from the agreement..."
- ✅ "Look at what the document states..."
- ❌ "Quote: 'The treaty states...'"
- ❌ "According to historian X (2015)..."

**8. Spoken Date Formats:**
- ✅ "On June 16th, 2014, a farmer..."
- ❌ "June 16, 2014. A farmer..."

**9. Evidence Stacking (Fall of Civilizations):**
- [ ] Multiple independent sources for major claims
- [ ] "We now have that data. [Source 1] shows... [Source 2] shows..."

**10. Formal Language to AVOID:**
- [ ] NO "Furthermore," "Moreover," at sentence start
- [ ] NO "In conclusion"
- [ ] NO "It is evident that"
- [ ] NO academic passive voice

=== SCORING ===
- 10 points possible (1 per category)
- 7+ = Ready for filming
- 5-6 = Needs revision
- <5 = Major rewrite needed

=== OUTPUT ===
**Voice Authenticity Score:** [X/10]

**Categories Passed:**
[List which of the 10 categories are satisfied]

**Issues Found:**
[List specific problems with line numbers/quotes]

**Suggested Fixes:**
[Specific rewrites showing before/after in natural voice]

**Missing Elements:**
[Which patterns from successful channels are absent]
''',
}


PROJECT_EVALUATION_PROMPTS = {
    "project_health_check": '''You are evaluating the History vs Hype YouTube channel production system.

Analyze the following project files and identify issues, gaps, and improvements.

=== FILES TO ANALYZE ===
{project_files}

=== EVALUATION CRITERIA ===

**1. WORKFLOW CONSISTENCY (Score 0-10)**
- Do all commands/skills/agents reference the same workflow phases?
- Are file naming conventions consistent across all docs?
- Do templates match the workflow described in CLAUDE.md?
- Are there broken references to non-existent files?
- Is the phase progression clear (Research → Script → Fact-check → Film)?

**2. PATTERN INTEGRATION (Score 0-10)**
- Are successful channel patterns (Kraut, Alex O'Connor, etc.) referenced consistently?
- Is the "both extremes" pattern documented everywhere it should be?
- Is the "spreadsheet angle" (HOW > WHY) integrated?
- Are steelmanning requirements present in script-related files?
- Is voice check integrated into the workflow?

**3. DOCUMENTATION QUALITY (Score 0-10)**
- Are there redundant/conflicting instructions across files?
- Is there a clear "source of truth" for each concept?
- Are examples provided where needed?
- Is the documentation actionable vs. just descriptive?
- Can a new user follow the workflow without confusion?

**4. SKILL/AGENT COVERAGE (Score 0-10)**
- Are all workflow steps covered by skills or agents?
- Are there gaps where manual work is still required?
- Do skills reference each other correctly (integration)?
- Is the handoff between phases clear?

**5. QUALITY GATES (Score 0-10)**
- Are there clear "can't proceed until X" checkpoints?
- Is the 90% verification threshold enforced?
- Is voice check (7/10 score) integrated?
- Are fact-check requirements specific and measurable?

**6. TOOL INTEGRATION (Score 0-10)**
- Is NotebookLM workflow clearly documented?
- Is prompt_evaluation.py integrated into workflow?
- Are external tools (VidIQ, etc.) mentioned where relevant?
- Is the Claude/NotebookLM division of labor clear?

=== OUTPUT FORMAT ===

**OVERALL PROJECT HEALTH: [X/60]**

**SCORES BY CATEGORY:**
1. Workflow Consistency: [X/10]
2. Pattern Integration: [X/10]
3. Documentation Quality: [X/10]
4. Skill/Agent Coverage: [X/10]
5. Quality Gates: [X/10]
6. Tool Integration: [X/10]

**CRITICAL ISSUES (Fix Immediately):**
- [Issue with file reference]
- [Issue with file reference]

**IMPROVEMENTS NEEDED:**
- [Specific improvement with file to change]
- [Specific improvement with file to change]

**REDUNDANCIES TO CONSOLIDATE:**
- [Files X and Y say the same thing - consolidate]

**MISSING ELEMENTS:**
- [What's not documented but should be]

**RECOMMENDED ACTIONS (Priority Order):**
1. [Most important fix]
2. [Second priority]
3. [Third priority]
''',

    "workflow_audit": '''Audit the History vs Hype workflow for consistency and completeness.

=== WORKFLOW FILES ===
{workflow_files}

=== CHECK FOR ===

**Phase Alignment:**
- Phase 1: Research + Verification → 01-VERIFIED-RESEARCH.md
- Phase 2: Script Writing → 02-SCRIPT-DRAFT.md
- Phase 2.5: Voice Check → prompt_evaluation.py
- Phase 3: Final Verification → 03-FACT-CHECK-VERIFICATION.md

**For each file, verify:**
1. Does it reference the correct phase?
2. Does it use consistent file names?
3. Does it reference the correct skill/agent?
4. Are prerequisites clear?
5. Are outputs clear?

=== OUTPUT ===

**WORKFLOW DIAGRAM (Actual):**
[Draw the actual workflow based on file analysis]

**INCONSISTENCIES FOUND:**
| File | Says | Should Say |
|------|------|------------|
| [file] | [current] | [correct] |

**MISSING CONNECTIONS:**
- [File X doesn't reference File Y but should]

**ORPHANED FILES:**
- [Files not referenced by any workflow step]
''',

    "pattern_coverage_audit": '''Audit whether successful channel patterns are consistently applied across all relevant files.

=== PATTERN CHECKLIST ===

**Core Patterns (Must be in ALL script-related files):**
1. Both Extremes framing
2. Steelmanning (Knowing Better)
3. Causal chains (Kraut)
4. Think-aloud moments (Alex O'Connor)
5. Document-first hook
6. "Do you see what they did?" moments (Historia Civilis)
7. Evidence stacking (Fall of Civilizations)
8. Spreadsheet Angle (HOW > WHY)
9. Natural fillers (3-5 per script)
10. Conversational quote introductions

=== FILES TO CHECK ===
{pattern_files}

=== OUTPUT ===

**PATTERN COVERAGE MATRIX:**

| Pattern | script.md | script-generator.md | script-writer-v2.md | style-guide.md |
|---------|-----------|---------------------|---------------------|----------------|
| Both Extremes | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Steelmanning | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| ... | ... | ... | ... | ... |

**GAPS FOUND:**
- [Pattern X missing from File Y]

**INCONSISTENT DESCRIPTIONS:**
- [File X describes pattern differently than File Y]
''',
}

# ============================================================================
# EVALUATION METRICS
# ============================================================================

def evaluate_script_quality(response: str) -> dict:
    """Evaluate script against History vs Hype criteria."""
    scores = {
        "has_modern_hook": "[MODERN HOOK]" in response or "2024" in response or "2025" in response,
        "has_both_extremes": "extreme" in response.lower() or "both" in response.lower(),
        "has_document_markers": "[DOCUMENT:" in response,
        "has_timestamps": any(f"{i}:" in response for i in range(0, 15)),
        "has_causal_language": any(w in response.lower() for w in ["consequently", "thereby", "which meant", "as a result"]),
        "has_academic_quotes": "page" in response.lower() or "according to" in response.lower(),
        "word_count": len(response.split()),
    }

    # Calculate overall score
    binary_scores = [v for v in scores.values() if isinstance(v, bool)]
    scores["overall"] = sum(binary_scores) / len(binary_scores) if binary_scores else 0

    return scores


def evaluate_fact_check_quality(response: str) -> dict:
    """Evaluate fact-check response quality."""
    scores = {
        "has_verdict": any(v in response.upper() for v in ["VERIFIED", "FALSE", "UNVERIFIABLE"]),
        "has_sources": "source" in response.lower() or "citation" in response.lower(),
        "has_confidence": "confidence" in response.lower() or "high" in response.lower() or "low" in response.lower(),
        "identifies_simplification": "oversimpl" in response.lower() or "🔴" in response,
        "provides_context": "context" in response.lower() or "note" in response.lower(),
    }

    binary_scores = [v for v in scores.values() if isinstance(v, bool)]
    scores["overall"] = sum(binary_scores) / len(binary_scores) if binary_scores else 0

    return scores


# ============================================================================
# MAIN EVALUATION RUNNER
# ============================================================================

def run_project_health_check():
    """
    Run a comprehensive health check on the entire project.
    Reads key files and evaluates workflow consistency.
    """
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 70)
    print("HISTORY VS HYPE - PROJECT HEALTH CHECK")
    print("=" * 70)

    # Define key files to analyze
    key_files = {
        "workflow": [
            ".claude/CORE-WORKFLOW-SCRIPTWRITING-FACTCHECKING.md",
            ".claude/commands/script.md",
            ".claude/commands/new-video-verified.md",
        ],
        "skills": [
            ".claude/skills/script-generator.md",
            ".claude/skills/script-reviewer.md",
            ".claude/skills/notebooklm-prompt-generator.md",
        ],
        "style": [
            ".claude/SCRIPTWRITING-STYLE-GUIDE.md",
            ".claude/STYLE-GUIDE-ADDITIONS.md",
        ],
        "agents": [
            ".claude/agents/script-writer-v2.md",
        ],
        "templates": [
            ".claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md",
            ".claude/templates/02-SCRIPT-DRAFT-TEMPLATE.md",
        ],
    }

    # Read files
    project_root = Path(__file__).parent.parent
    file_contents = {}

    for category, files in key_files.items():
        print(f"\nReading {category} files...")
        for file_path in files:
            full_path = project_root / file_path
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding='utf-8')
                    file_contents[file_path] = content[:5000]  # Truncate for API
                    print(f"  ✅ {file_path}")
                except Exception as e:
                    print(f"  ❌ {file_path}: {e}")
            else:
                print(f"  ❌ {file_path}: NOT FOUND")
                file_contents[file_path] = "[FILE NOT FOUND]"

    # Build project summary
    project_summary = "\n\n".join([
        f"=== {path} ===\n{content[:3000]}..."
        for path, content in file_contents.items()
    ])

    # Check if API key available
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("\n" + "=" * 70)
        print("Running AI-powered health check...")
        print("=" * 70)

        try:
            from anthropic import Anthropic
            client = Anthropic()

            prompt = PROJECT_EVALUATION_PROMPTS["project_health_check"].format(
                project_files=project_summary
            )

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            print("\n" + response.content[0].text)

        except Exception as e:
            print(f"Error running health check: {e}")
    else:
        print("\n" + "=" * 70)
        print("SET ANTHROPIC_API_KEY to run AI-powered health check")
        print("=" * 70)
        print("\nManual checklist based on files found:")

        # Manual checks - read full files for accurate checking
        def check_file_contains(file_path, search_term):
            full_path = project_root / file_path
            if full_path.exists():
                try:
                    content = full_path.read_text(encoding='utf-8').lower()
                    return search_term.lower() in content
                except:
                    return False
            return False

        checks = {
            "script-generator.md exists": (project_root / ".claude/skills/script-generator.md").exists(),
            "Workflow references voice check": check_file_contains(".claude/CORE-WORKFLOW-SCRIPTWRITING-FACTCHECKING.md", "voice check"),
            "Script.md references Kraut patterns": check_file_contains(".claude/commands/script.md", "kraut"),
            "Script.md references spreadsheet angle": check_file_contains(".claude/commands/script.md", "spreadsheet angle"),
            "Style guide has both extremes": check_file_contains(".claude/SCRIPTWRITING-STYLE-GUIDE.md", "both extremes"),
            "Style additions has Knowing Better": check_file_contains(".claude/STYLE-GUIDE-ADDITIONS.md", "knowing better"),
            "Script-generator has steelmanning": check_file_contains(".claude/skills/script-generator.md", "steelman"),
            "Workflow has Phase 2.5": check_file_contains(".claude/CORE-WORKFLOW-SCRIPTWRITING-FACTCHECKING.md", "phase 2.5"),
            "Templates exist": (project_root / ".claude/templates/01-VERIFIED-RESEARCH-TEMPLATE.md").exists(),
        }

        passed_count = sum(1 for v in checks.values() if v)
        total_count = len(checks)

        print(f"\n  Score: {passed_count}/{total_count}")
        print()
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")

    return file_contents


def run_evaluation():
    """Run prompt evaluation (prints templates if no API key)."""
    import sys
    import io
    # Handle Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 70)
    print("HISTORY VS HYPE - PROMPT EVALUATION SUITE")
    print("=" * 70)

    # Display prompt variants
    print("\n### SCRIPT GENERATION PROMPTS ###\n")
    for name, prompt in SCRIPT_PROMPTS.items():
        print(f"\n--- {name.upper()} ---")
        print(f"Length: {len(prompt)} chars")
        # Show formatted version with test case
        formatted = prompt.format(**TEST_CASES["territorial_topic"])
        print(f"Sample (first 500 chars):\n{formatted[:500]}...")
        print()

    print("\n### FACT-CHECK PROMPTS ###\n")
    for name, prompt in FACT_CHECK_PROMPTS.items():
        print(f"\n--- {name.upper()} ---")
        print(f"Length: {len(prompt)} chars")
        formatted = prompt.format(**TEST_CASES["fact_check_claim"])
        print(f"Sample (first 500 chars):\n{formatted[:500]}...")
        print()

    print("\n### CLAIM EXTRACTION PROMPTS ###\n")
    for name, prompt in CLAIM_EXTRACTION_PROMPTS.items():
        print(f"\n--- {name.upper()} ---")
        print(f"Length: {len(prompt)} chars")
        print()

    print("\n### VOICE CHECK PROMPTS ###\n")
    for name, prompt in VOICE_CHECK_PROMPTS.items():
        print(f"\n--- {name.upper()} ---")
        print(f"Length: {len(prompt)} chars")
        print()

    # If API key is set, offer to run live evaluation
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("\n" + "=" * 70)
        print("API KEY DETECTED - Ready for live evaluation")
        print("=" * 70)
        print("\nTo run live comparisons, use:")
        print("  from prompt_evaluation import run_live_comparison")
        print("  run_live_comparison('script', 'territorial_topic')")
    else:
        print("\n" + "=" * 70)
        print("SET ANTHROPIC_API_KEY to run live prompt comparisons")
        print("=" * 70)
        print("\nExample:")
        print('  import os')
        print('  os.environ["ANTHROPIC_API_KEY"] = "your-key-here"')
        print('  from prompt_evaluation import run_live_comparison')
        print('  run_live_comparison("script", "territorial_topic")')

    # Save prompts to JSON for reference
    output = {
        "script_prompts": SCRIPT_PROMPTS,
        "fact_check_prompts": FACT_CHECK_PROMPTS,
        "claim_extraction_prompts": CLAIM_EXTRACTION_PROMPTS,
        "voice_check_prompts": VOICE_CHECK_PROMPTS,
        "test_cases": TEST_CASES,
    }

    output_path = Path(__file__).parent.parent / "prompt_evaluation_templates.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nPrompt templates saved to: {output_path}")


def run_live_comparison(prompt_type: str, test_case: str):
    """
    Run live comparison of prompt variants using Anthropic API.

    Args:
        prompt_type: "script", "fact_check", "claim_extraction", or "voice_check"
        test_case: Key from TEST_CASES dict
    """
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Install anthropic: pip install anthropic")
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY environment variable")
        return

    client = Anthropic()

    # Select prompts
    prompt_sets = {
        "script": SCRIPT_PROMPTS,
        "fact_check": FACT_CHECK_PROMPTS,
        "claim_extraction": CLAIM_EXTRACTION_PROMPTS,
        "voice_check": VOICE_CHECK_PROMPTS,
    }

    prompts = prompt_sets.get(prompt_type, SCRIPT_PROMPTS)
    test_data = TEST_CASES.get(test_case, TEST_CASES["territorial_topic"])

    results = {}

    for name, template in prompts.items():
        print(f"\nTesting: {name}...")

        try:
            formatted_prompt = template.format(**test_data)
        except KeyError:
            formatted_prompt = template.format(
                text="Sample text for extraction",
                script="Sample script for voice check",
                **test_data
            )

        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": formatted_prompt}]
            )

            output = response.content[0].text

            # Evaluate based on type
            if prompt_type == "script":
                scores = evaluate_script_quality(output)
            elif prompt_type == "fact_check":
                scores = evaluate_fact_check_quality(output)
            else:
                scores = {"response_length": len(output)}

            results[name] = {
                "scores": scores,
                "response_preview": output[:500] + "...",
                "full_response": output,
            }

            print(f"  Score: {scores.get('overall', 'N/A')}")

        except Exception as e:
            print(f"  Error: {e}")
            results[name] = {"error": str(e)}

    # Summary
    print("\n" + "=" * 70)
    print("COMPARISON RESULTS")
    print("=" * 70)

    for name, result in results.items():
        if "error" not in result:
            print(f"\n{name.upper()}:")
            for key, value in result["scores"].items():
                print(f"  {key}: {value}")

    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "health":
        run_project_health_check()
    else:
        run_evaluation()
        print("\n" + "=" * 70)
        print("TIP: Run 'python prompt_evaluation.py health' for project health check")
        print("=" * 70)
