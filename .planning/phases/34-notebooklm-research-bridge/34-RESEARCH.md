# Phase 34: NotebookLM Research Bridge - Research

**Researched:** 2026-02-10
**Domain:** CLI tooling for academic source generation, NotebookLM citation extraction, and research prompt templating
**Confidence:** HIGH

## Summary

Phase 34 bridges the gap between topic selection and NotebookLM-powered research by providing three tool-assisted workflows: (1) generating academic source shopping lists via Claude API, (2) extracting structured citations from NotebookLM chat output, and (3) delivering optimized research prompts. This is a workflow enhancement phase, not API automation - NotebookLM has no public API, so the approach centers on making manual workflows faster and more reliable.

The technical domain is well-understood: Python CLI tools using the existing project architecture (SQLite-backed error dict pattern, argparse for CLI parsing, Claude API for generation tasks). The citation extraction challenge is straightforward regex parsing of NotebookLM's standardized output format (citation markers like [1], [2] with corresponding source references). The prompt library can be implemented as static Markdown templates (lowest complexity, highest reliability).

**Primary recommendation:** Implement as two Python modules (`notebooklm_bridge.py` ~250 LOC, `citation_extractor.py` ~150 LOC) integrated into existing `/sources` and `/verify` commands, plus a static prompt reference document. Avoid over-engineering - the value is in workflow speed, not technical sophistication.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Source List Generation (NLMB-01):**
- Source of recommendations: Claude API generation (no web search dependency) - fast, reliable, leverages Claude's training data on academic publishing
- Output format: Standalone `NOTEBOOKLM-SOURCE-LIST.md` file written to the project folder - serves as shopping/download checklist
- Detail level: Full academic citation per entry - title, author, publisher, year, ISBN, edition, estimated price, suggested purchase link (Amazon/publisher)
- Organization: By priority tier (Tier 1: must-have primary sources, Tier 2: key secondary, Tier 3: supplementary) - matches existing fact-checking source hierarchy

**Citation Extraction (NLMB-02):**
- Input method: User copies NotebookLM chat text into a `.txt` or `.md` file, tool reads the file - reliable, cross-platform, no clipboard dependencies
- Output format: Separate extraction file (`NOTEBOOKLM-EXTRACTIONS.md`) for review - user manually moves verified items to VERIFIED-RESEARCH.md (preserves review step, protects single source of truth)
- Citation format: Match existing VERIFIED-RESEARCH.md format (claim + source + page number + verification status) - seamless pipeline integration
- Citation marker handling: Claude's discretion - NotebookLM output format varies, tool should parse what's reliably available

**Prompt Library (NLMB-03):**
- Delivery: Claude's discretion on static templates vs CLI-generated prompts - pick based on complexity vs value tradeoff
- Specialization: Claude's discretion on whether to specialize by video type (territorial, ideological, fact-check) or keep generic
- Research phases covered: Claude's discretion on full pipeline (5 steps) vs core 3 (claim verification, quote extraction, counter-evidence)
- NotebookLM features: Claude's discretion on whether to include Audio Overview and Interactive Mode prompts

**Workflow Integration:**
- Source list command: Claude's discretion on which existing command to extend (`/sources --recommend` or `/research --sources`)
- Citation extraction command: Claude's discretion on placement (`/sources --extract` or `/verify --extract-nlm`)
- Prompt access: Claude's discretion on reference doc vs command vs both
- Implementation approach: Claude's discretion on Python modules in `tools/` vs reference docs + skill updates - pick what delivers the three requirements most reliably

### Claude's Discretion Areas
- Prompt library delivery mechanism (static vs dynamic)
- Prompt specialization level (by video type vs generic)
- Research phase coverage depth
- Audio Overview prompt inclusion
- Command placement for all three capabilities
- Implementation approach (code vs reference docs)
- Citation marker parsing strategy

### Deferred Ideas (OUT OF SCOPE)
None - discussion stayed within phase scope

</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| anthropic | 0.40+ | Claude API SDK | Official Anthropic SDK, type-safe, async support, streaming |
| sqlite3 | stdlib | Optional persistence | Already used in project (database.py pattern), no external dep |
| re | stdlib | Citation parsing | Standard library regex sufficient for citation marker patterns |
| pathlib | stdlib | File operations | Modern path handling, already used across codebase |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| argparse | stdlib | CLI argument parsing | Existing project standard (see tools/discovery/keywords.py) |
| json | stdlib | API responses | Claude API response parsing |
| markitdown | 0.1.5+ | Optional: document conversion | If future need to convert PDFs/DOCX to markdown for NotebookLM |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| anthropic SDK | Direct HTTP requests | SDK provides type safety, retries, error handling - clear win |
| argparse | click or typer | argparse is stdlib (no dep), already used in project, sufficient for this use case |
| Static templates | Claude-generated prompts | Static = zero latency, zero cost, 100% reliable; dynamic = flexible but slower/costlier |

**Installation:**
```bash
pip install anthropic>=0.40.0
# markitdown optional: pip install markitdown
```

## Architecture Patterns

### Recommended Project Structure
```
tools/
├── notebooklm_bridge.py        # Source list generation (Claude API)
├── citation_extractor.py       # Parse NotebookLM chat output
└── (existing modules)

.claude/
├── REFERENCE/
│   └── NOTEBOOKLM-RESEARCH-PROMPTS.md  # Static prompt library
└── commands/
    ├── sources.md              # Extend with --recommend flag
    └── verify.md               # Extend with --extract-nlm flag
```

### Pattern 1: Error Dict Pattern (Mandatory - Project Standard)
**What:** All functions return `dict` with results or `{'error': msg}` on failure
**When to use:** ALL functions in Phase 34 modules
**Example:**
```python
# Source: tools/discovery/database.py (existing project pattern)
def generate_source_list(topic: str) -> Dict[str, Any]:
    """Generate academic source list for topic."""
    try:
        # Call Claude API
        response = client.messages.create(...)
        return {
            'status': 'success',
            'sources': parsed_sources,
            'count': len(parsed_sources)
        }
    except Exception as e:
        return {'error': f"Source generation failed: {str(e)}"}
```

### Pattern 2: Claude API Call Pattern
**What:** Standard pattern for calling Claude API with error handling
**When to use:** Source list generation (NLMB-01)
**Example:**
```python
# Source: Anthropic SDK documentation
import anthropic

def generate_sources_via_claude(topic: str, video_type: str) -> Dict[str, Any]:
    """Generate source list using Claude API."""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Generate 10-15 academic sources for this topic:
    Topic: {topic}
    Video Type: {video_type}

    Requirements:
    - University press publications ONLY (Cambridge, Oxford, Chicago, Harvard, Yale)
    - Organize by tier (Tier 1: primary sources, Tier 2: academic monographs, Tier 3: supplementary)
    - Include: title, author, publisher, year, ISBN, estimated price, purchase link
    """

    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        return {'status': 'success', 'content': message.content[0].text}
    except anthropic.APIError as e:
        return {'error': f"Claude API error: {str(e)}"}
```

### Pattern 3: Citation Extraction via Regex
**What:** Parse NotebookLM chat output for citation markers and source references
**When to use:** Citation extraction (NLMB-02)
**Example:**
```python
# NotebookLM citation format: [1], [2] with legend at bottom
import re
from typing import List, Dict

def parse_notebooklm_citations(input_file: str) -> Dict[str, Any]:
    """Extract citations from NotebookLM chat output."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern 1: Citation markers in text [1], [2]
        citation_pattern = r'\[(\d+)\]'
        citations = re.findall(citation_pattern, content)

        # Pattern 2: Source legend (bottom of NotebookLM output)
        # Format: [1] Source Name, Page X
        source_pattern = r'\[(\d+)\]\s+(.+?),\s+(?:p\.?\s*)?(\d+)'
        sources = re.findall(source_pattern, content, re.MULTILINE)

        # Build citation map
        citation_map = {num: {'source': src, 'page': page}
                       for num, src, page in sources}

        return {
            'status': 'success',
            'citations': citations,
            'sources': citation_map,
            'total': len(citation_map)
        }
    except Exception as e:
        return {'error': f"Citation parsing failed: {str(e)}"}
```

### Pattern 4: File-Based Input (Mandatory - User Decision)
**What:** Read user-provided file instead of clipboard access
**Why:** Cross-platform reliability, no clipboard dependencies, matches project standards
**Example:**
```python
def extract_citations_from_file(filepath: str) -> Dict[str, Any]:
    """Extract citations from user-provided NotebookLM output file."""
    if not Path(filepath).exists():
        return {'error': f"File not found: {filepath}"}

    result = parse_notebooklm_citations(filepath)

    if 'error' in result:
        return result

    # Write to separate extraction file for review
    output_path = Path(filepath).parent / "NOTEBOOKLM-EXTRACTIONS.md"
    write_extractions(result, output_path)

    return {
        'status': 'success',
        'input': filepath,
        'output': str(output_path),
        'count': result['total']
    }
```

### Anti-Patterns to Avoid
- **Over-engineering the prompt library:** Static markdown templates are sufficient. Don't build dynamic prompt generation unless user requests it.
- **Clipboard access:** Brittle, platform-dependent. Use file input as specified in user decisions.
- **Complex citation parsing:** NotebookLM format is consistent. Simple regex is sufficient - don't reach for NLP libraries.
- **Tight coupling to NotebookLM API:** NotebookLM has no public API. Design for tool-assisted manual workflow, not automation.
- **Ignoring error dict pattern:** Project standard requires `{'error': msg}` returns, not exceptions.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Claude API calls | Custom HTTP client with retries | anthropic SDK | Official SDK handles auth, retries, streaming, type safety, error handling |
| Academic citation parsing from PDFs | Custom PDF text extraction | markitdown (optional) | Microsoft library handles multi-format conversion, edge cases, encodings |
| CLI argument parsing | String splitting and manual validation | argparse (stdlib) | Project standard, handles help text, type validation, subcommands |
| File path handling | String concatenation for paths | pathlib (stdlib) | Cross-platform, prevents path separator bugs, already used in project |

**Key insight:** This phase is about workflow glue, not novel algorithms. Prefer stdlib and existing project patterns over custom solutions.

## Common Pitfalls

### Pitfall 1: Assuming NotebookLM API Exists
**What goes wrong:** Planning automation features that require NotebookLM API access
**Why it happens:** NotebookLM is a Google product, assumption that API exists
**How to avoid:** Design for tool-assisted manual workflow (user copies/pastes, tool parses)
**Warning signs:** Requirements mention "auto-upload to NotebookLM", "fetch citations via API"

### Pitfall 2: Over-Parsing Citation Formats
**What goes wrong:** Building complex NLP-based citation parsers for edge cases
**Why it happens:** Trying to handle every possible citation format variation
**How to avoid:** NotebookLM output is consistent - simple regex for `[1]` markers and source legend is sufficient
**Warning signs:** Dependencies on spaCy, NLTK, or academic citation parsing libraries

### Pitfall 3: Claude API Rate Limits
**What goes wrong:** Source generation fails during high-volume usage
**Why it happens:** Not handling rate limit responses from Claude API
**How to avoid:** Use anthropic SDK (handles retries automatically), add rate limit error handling
**Warning signs:** 429 errors, "rate limit exceeded" failures without retry logic

### Pitfall 4: Breaking Single Source of Truth Pattern
**What goes wrong:** Tool writes directly to `01-VERIFIED-RESEARCH.md`, bypassing review
**Why it happens:** Trying to automate too much of the workflow
**How to avoid:** Write to separate `NOTEBOOKLM-EXTRACTIONS.md` file, user manually reviews and copies
**Warning signs:** Requirements mention "auto-update VERIFIED-RESEARCH.md"

### Pitfall 5: File Encoding Issues
**What goes wrong:** Citation extraction fails on files with non-ASCII characters (common in academic sources)
**Why it happens:** Not specifying UTF-8 encoding when reading files
**How to avoid:** Always use `open(file, 'r', encoding='utf-8')`
**Warning signs:** UnicodeDecodeError on files with accented characters, non-Latin scripts

### Pitfall 6: Ignoring Existing Command Structure
**What goes wrong:** Creating new standalone commands instead of extending existing `/sources` and `/verify`
**Why it happens:** Not reading existing command definitions first
**How to avoid:** Extend existing commands with new flags (`/sources --recommend`, `/verify --extract-nlm`)
**Warning signs:** Creating `/generate-sources` or `/extract-citations` as new top-level commands

## Code Examples

Verified patterns from official sources and project standards:

### Example 1: Source List Generation (Claude API)
```python
# Source: Anthropic SDK documentation + project error dict pattern
import anthropic
import os
from typing import Dict, Any

def generate_source_list(topic: str, video_type: str = "general") -> Dict[str, Any]:
    """
    Generate academic source list using Claude API.

    Args:
        topic: Video topic (e.g., "Library of Alexandria")
        video_type: territorial, ideological, or general

    Returns:
        {'status': 'success', 'sources': markdown_content, 'count': int}
        or {'error': message}
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Build prompt following user's tier structure requirement
    prompt = f"""Generate an academic source list for a History vs Hype video.

Topic: {topic}
Video Type: {video_type}

Requirements:
- 10-15 sources total
- University press publications ONLY (Cambridge, Oxford, Chicago, Harvard, Yale, Princeton, Cornell)
- Organize by tier:
  * Tier 1: Primary sources (treaties, documents, archives)
  * Tier 2: Key secondary sources (academic monographs)
  * Tier 3: Supplementary sources
- For each source provide:
  * Full title and author
  * Publisher and year
  * ISBN if available
  * Estimated price
  * Purchase link (Amazon or publisher direct)
  * Why this source is essential

Format as markdown for direct use in NOTEBOOKLM-SOURCE-LIST.md"""

    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        content = message.content[0].text
        # Count sources (rough estimate from Tier headers)
        source_count = content.count('###') - content.count('####')

        return {
            'status': 'success',
            'sources': content,
            'count': source_count
        }
    except anthropic.APIError as e:
        return {'error': f"Claude API error: {str(e)}"}
    except Exception as e:
        return {'error': f"Source generation failed: {str(e)}"}
```

### Example 2: Citation Extraction
```python
# Source: Project file handling patterns + NotebookLM format (verified via web research)
import re
from pathlib import Path
from typing import Dict, Any, List

def extract_citations(input_path: str) -> Dict[str, Any]:
    """
    Parse NotebookLM chat output and extract citations.

    NotebookLM format (from web research):
    - Citation markers: [1], [2], [3] inline
    - Source legend at bottom: "[1] Author, Book Title, p. 45"

    Args:
        input_path: Path to file with NotebookLM chat output

    Returns:
        {'status': 'success', 'citations': [...], 'output_path': str}
        or {'error': message}
    """
    input_file = Path(input_path)
    if not input_file.exists():
        return {'error': f"File not found: {input_path}"}

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError as e:
        return {'error': f"Encoding error (try UTF-8): {str(e)}"}

    # Extract citation markers and sources
    citations = _parse_citations(content)

    if not citations:
        return {'error': "No citations found in file. Check NotebookLM output format."}

    # Write to extraction file for review
    output_path = input_file.parent / "NOTEBOOKLM-EXTRACTIONS.md"
    _write_extractions(citations, output_path)

    return {
        'status': 'success',
        'citations': citations,
        'output_path': str(output_path),
        'count': len(citations)
    }

def _parse_citations(content: str) -> List[Dict[str, str]]:
    """Parse citation markers and source references from NotebookLM output."""
    # Pattern for source legend: [1] Source Name, Page X
    # Variations: "p. 45", "page 45", "pp. 45-46"
    source_pattern = r'\[(\d+)\]\s+(.+?),\s+(?:p\.?|page|pp\.?)\s*(\d+(?:-\d+)?)'

    sources = {}
    for match in re.finditer(source_pattern, content, re.MULTILINE | re.IGNORECASE):
        num, source, page = match.groups()
        sources[num] = {'source': source.strip(), 'page': page}

    # Find claims with citation markers
    # Look for sentence ending with [1], [2], etc.
    claim_pattern = r'(.+?)\s*\[(\d+)\]'

    citations = []
    for match in re.finditer(claim_pattern, content):
        claim, cite_num = match.groups()
        if cite_num in sources:
            citations.append({
                'claim': claim.strip(),
                'source': sources[cite_num]['source'],
                'page': sources[cite_num]['page'],
                'status': '⏳ RESEARCHING'  # User reviews and updates
            })

    return citations

def _write_extractions(citations: List[Dict[str, str]], output_path: Path):
    """Write extractions in VERIFIED-RESEARCH.md compatible format."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# NotebookLM Citation Extractions\n\n")
        f.write("**Status:** NEEDS REVIEW - Verify claims before moving to 01-VERIFIED-RESEARCH.md\n\n")
        f.write("---\n\n")

        for i, cite in enumerate(citations, 1):
            f.write(f"### Extracted Claim {i}\n")
            f.write(f"**Claim:** {cite['claim']}\n")
            f.write(f"**Source:** {cite['source']}, p. {cite['page']}\n")
            f.write(f"**Status:** {cite['status']}\n\n")
            f.write("**Action Required:**\n")
            f.write("- [ ] Verify claim accuracy\n")
            f.write("- [ ] Check page number\n")
            f.write("- [ ] Update status to ✅ VERIFIED or ❌ UNVERIFIABLE\n")
            f.write("- [ ] Copy to 01-VERIFIED-RESEARCH.md if verified\n\n")
            f.write("---\n\n")
```

### Example 3: Static Prompt Library (Recommended Approach)
```markdown
# Source: Project decision (static templates preferred for reliability)
# File: .claude/REFERENCE/NOTEBOOKLM-RESEARCH-PROMPTS.md

# NotebookLM Research Prompts

## Core Research Prompts

### Prompt 1: Claim Verification
Copy-paste this into NotebookLM chat:

"""
I need to verify specific claims for my History vs Hype video script.

For each claim below:
1. Is it accurate according to the sources?
2. Provide exact quote with page number
3. Note any nuance or context I'm missing

CLAIMS TO VERIFY:
[User pastes claims here]

Format your response as:
- CLAIM: [restate claim]
- VERDICT: ✅ VERIFIED / ❌ INACCURATE / ⚠️ PARTIALLY TRUE
- SOURCE: [exact quote], [source name], p. [page]
- CONTEXT: [additional context if needed]
"""

### Prompt 2: Quote Extraction
[Additional prompts follow...]
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual source finding | Claude API generates academic source lists | 2024-2025 | LLMs now have training data on academic publishers, can generate university press recommendations |
| Copy-paste citations manually | Regex parsing of NotebookLM output | 2026 | NotebookLM format is consistent enough for reliable extraction |
| No prompt templates | Static prompt library in reference docs | Phase 34 | Reduces prompt engineering time per video |

**Current state (February 2026):**
- NotebookLM has NO public API (verified via web research)
- NotebookLM uses Gemini 2.0 Flash with 2M token context window
- Citation format is consistent: `[1]` markers with source legend
- Claude API (Anthropic SDK) is stable and production-ready

**What's possible now:**
- ✅ Generate academic source recommendations via Claude API
- ✅ Parse NotebookLM citations with simple regex
- ✅ Template common research prompts
- ❌ NOT possible: NotebookLM API automation, auto-upload sources, fetch citations programmatically

## Open Questions

1. **Citation format edge cases**
   - What we know: NotebookLM uses `[1]`, `[2]` format with source legend
   - What's unclear: Variations in source legend format (how consistent is "p. 45" vs "page 45" vs "pp. 45-46"?)
   - Recommendation: Start with common patterns, add variants as users report issues

2. **Claude API cost per source list**
   - What we know: Source list generation uses ~4000 tokens output
   - What's unclear: Cost per video (depends on usage frequency)
   - Recommendation: Monitor costs in early usage, ~$0.15 per source list with Claude Opus 4.6

3. **Integration with existing commands**
   - What we know: User decision gives discretion on `/sources --recommend` vs `/research --sources`
   - What's unclear: User preference for command structure
   - Recommendation: Extend `/sources` command (already handles source workflows), add `--extract` flag to `/verify` (already handles extraction workflows)

## Sources

### Primary (HIGH confidence)
- [Anthropic Python SDK GitHub](https://github.com/anthropics/anthropic-sdk-python) - Official SDK documentation
- [Anthropic Python SDK PyPI](https://pypi.org/project/anthropic/) - Current version and installation
- [Claude API Documentation](https://platform.claude.com/docs/en/api/sdks/python) - Python SDK usage patterns
- Project codebase: `tools/discovery/database.py`, `tools/production/metadata.py` - Existing error dict pattern

### Secondary (MEDIUM confidence)
- [NotebookLM Help - Use chat](https://support.google.com/notebooklm/answer/16179559?hl=en) - Citation format in chat
- [GitHub - nicremo/notebookLM-citation](https://github.com/nicremo/notebookLM-citation) - Citation preservation tools (confirms `[1]` format)
- [Microsoft MarkItDown GitHub](https://github.com/microsoft/markitdown) - Document conversion library
- [MarkItDown PyPI](https://pypi.org/project/markitdown/) - Version 0.1.5b1 (latest as of Jan 2026)
- [RefExtract PyPI](https://pypi.org/project/refextract/) - Academic citation parsing library (if needed for complex cases)

### Tertiary (LOW confidence)
- Web search results on CLI argument parsing comparisons (argparse vs click vs typer) - General context, not specific to this phase
- Python regex documentation - Standard library, well-documented

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Anthropic SDK is official and stable, stdlib modules well-documented
- Architecture: HIGH - Error dict pattern verified in existing codebase, file-based I/O is specified requirement
- Citation parsing: MEDIUM-HIGH - NotebookLM format confirmed via multiple sources, edge cases may exist
- Pitfalls: HIGH - Based on project constraints (no API automation) and common pitfall patterns

**Implementation estimates:**
- `notebooklm_bridge.py`: ~250 LOC (Claude API call, prompt building, error handling, file writing)
- `citation_extractor.py`: ~150 LOC (regex parsing, extraction formatting, file I/O)
- Static prompt library: ~200 lines markdown (5-7 prompt templates)
- Command integration: ~50 LOC updates to existing commands
- Total: ~650 LOC + documentation

**Research date:** 2026-02-10
**Valid until:** 60 days (stable domain - CLI tools, established APIs, static prompt templates)

**Next step:** Planning can now create PLAN.md files with specific tasks for:
1. Source list generation via Claude API
2. Citation extraction with regex parsing
3. Static prompt library in reference docs
4. Integration with `/sources` and `/verify` commands
