"""
NotebookLM Research Bridge - Academic Source List Generator

Generates tiered academic source lists for NotebookLM upload using Claude API.
Follows History vs Hype source standards (NOTEBOOKLM-SOURCE-STANDARDS.md).

Usage:
    python tools/notebooklm_bridge.py "Library of Alexandria" --type ideological
    python tools/notebooklm_bridge.py "Sykes-Picot Agreement" --type territorial --output video-projects/project/
    python tools/notebooklm_bridge.py "Topic" --dry-run

Output: NOTEBOOKLM-SOURCE-LIST.md with tiered university press sources
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic>=0.40.0", file=sys.stderr)
    sys.exit(1)


def generate_source_list(topic: str, video_type: str = "general", num_sources: int = 15) -> Dict[str, Any]:
    """
    Generate academic source list via Claude API.

    Args:
        topic: Video topic (e.g., "Library of Alexandria")
        video_type: One of: territorial, ideological, fact-check, general
        num_sources: Number of sources to request (10-20 range)

    Returns:
        {'status': 'success', 'content': str, 'model': str} on success
        {'error': msg} on failure
    """
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return {
            'error': 'ANTHROPIC_API_KEY not set. Export your API key: export ANTHROPIC_API_KEY=sk-...'
        }

    # Build system message with detailed instructions
    system_message = f"""You are an academic research assistant specializing in source curation for historical documentary videos.

Your task: Generate a tiered academic source list for a video about "{topic}" (video type: {video_type}).

# SOURCE QUALITY STANDARDS

**MANDATORY Requirements:**
- University press publications ONLY (Cambridge, Oxford, Chicago, Harvard, Yale, Princeton, Stanford, Cornell)
- Top-tier scholars (leading authorities, endowed chairs, major universities)
- Critical editions for primary sources (scholarly apparatus, textual variants)
- NO Wikipedia, NO news articles, NO popular history books
- Budget is UNLIMITED - recommend best sources regardless of price

# TIER ORGANIZATION

**Tier 1: Primary Sources** (3+ required)
- Treaties, court rulings, official documents, contemporary accounts
- Critical editions with scholarly apparatus
- Government archives, diplomatic cables
- Focus based on video type:
  - territorial: treaties, boundary surveys, ICJ cases, colonial archives
  - ideological: manuscripts, primary chronicles, contemporary documents
  - fact-check: court filings, official records, primary documents
  - general: balanced mix

**Tier 2: Academic Monographs** (3+ required)
- University press books by leading scholars
- Peer-reviewed analysis
- Published 2010-present prioritized (note if earlier)
- Comprehensive treatments of topic

**Tier 3: Supplementary Sources** (optional)
- Think tank reports (Brookings, RAND, Chatham House)
- Legal encyclopedias (Oxford Public International Law)
- Expert interviews (oral histories)
- Background context

# FOR EACH SOURCE

Provide:
1. **Title** - Full title including subtitle
2. **Author** - Name with credentials (e.g., "Chris Wickham, Chichele Professor of Medieval History, Oxford")
3. **Publisher** - Must be university press
4. **Year** - Publication date
5. **ISBN** - If available
6. **Price** - Estimated cost ($40-60 for monographs, $0 for open access)
7. **Purchase Link** - Amazon or publisher direct link
8. **Relevance** - 1-2 sentences on why essential for this video
9. **Key Sections** - Chapters or page ranges to focus on

# NAMING CONVENTION

Use NotebookLM naming format:
- Primary sources: [P1], [P2], [P3]...
- Academic monographs: [A1], [A2], [A3]...
- Supplementary: [S1], [S2], [S3]...

# OUTPUT FORMAT

Start with SOURCE QUALITY CHECK table:

```markdown
## SOURCE QUALITY CHECK

| Requirement | Status |
|-------------|--------|
| 3+ Primary Sources | ✅ [count] identified |
| 3+ University Press Academic Sources | ✅ [count] identified |
| Total {num_sources} Sources | ✅ [count] sources |
| Wikipedia/News as citations | ❌ Excluded (reference only) |
```

Then organize sources by tier with full details.

# IMPORTANT

- Request {num_sources} sources total
- Ensure minimums met: 3+ Tier 1, 3+ Tier 2
- Only university press publishers
- Include price and purchase link for EVERY source
- Be specific about author credentials
- Provide exact ISBN when available
"""

    user_message = f"""Generate an academic source list for a video about: {topic}

Video type: {video_type}
Number of sources requested: {num_sources}

Please provide {num_sources} rigorously academic sources organized by tier, following all quality standards."""

    # Call Claude API
    try:
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=system_message,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # Extract text from response
        content = response.content[0].text if response.content else ""

        if not content:
            return {'error': 'API returned empty response'}

        return {
            'status': 'success',
            'content': content,
            'model': response.model
        }

    except anthropic.APIError as e:
        return {'error': f'API error: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}


def write_source_list(content: str, output_dir: str, topic: str) -> Dict[str, Any]:
    """
    Write source list to NOTEBOOKLM-SOURCE-LIST.md file.

    Args:
        content: Source list content from Claude API
        output_dir: Directory to write file to
        topic: Topic string for header

    Returns:
        {'status': 'success', 'path': str} on success
        {'error': msg} on failure
    """
    try:
        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Build file path
        file_path = output_path / 'NOTEBOOKLM-SOURCE-LIST.md'

        # Build header with metadata
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header = f"""# NotebookLM Source List

**Topic:** {topic}
**Generated:** {timestamp}
**Tool:** notebooklm_bridge.py (Claude API)

---

"""

        # Write file
        full_content = header + content
        file_path.write_text(full_content, encoding='utf-8')

        return {
            'status': 'success',
            'path': str(file_path)
        }

    except OSError as e:
        return {'error': f'File write error: {str(e)}'}
    except Exception as e:
        return {'error': f'Unexpected error: {str(e)}'}


def main():
    """CLI entry point for source list generation."""
    parser = argparse.ArgumentParser(
        description='Generate academic source list for NotebookLM research',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/notebooklm_bridge.py "Library of Alexandria" --type ideological
  python tools/notebooklm_bridge.py "Sykes-Picot Agreement" --type territorial --output video-projects/project/
  python tools/notebooklm_bridge.py "Topic" --dry-run

Output:
  Creates NOTEBOOKLM-SOURCE-LIST.md with tiered university press sources

Requirements:
  - ANTHROPIC_API_KEY environment variable must be set
  - pip install anthropic>=0.40.0
        """
    )

    parser.add_argument(
        'topic',
        help='Video topic (e.g., "Library of Alexandria")'
    )
    parser.add_argument(
        '--type',
        choices=['territorial', 'ideological', 'fact-check', 'general'],
        default='general',
        help='Video type for tailored source recommendations (default: general)'
    )
    parser.add_argument(
        '--output',
        default='.',
        help='Output directory for source list file (default: current directory)'
    )
    parser.add_argument(
        '--sources',
        type=int,
        default=15,
        help='Number of sources to request (10-20 range, default: 15)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print source list to stdout instead of writing file'
    )

    args = parser.parse_args()

    # Validate sources count
    if args.sources < 10 or args.sources > 20:
        print("WARNING: --sources should be in range 10-20 for optimal results", file=sys.stderr)

    # Generate source list
    print(f"Generating source list for: {args.topic}")
    print(f"Video type: {args.type}")
    print(f"Requesting {args.sources} sources...")
    print()

    result = generate_source_list(args.topic, args.type, args.sources)

    # Handle errors
    if 'error' in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Dry run - print to stdout
    if args.dry_run:
        print(result['content'])
        print()
        print(f"--- Generated by {result['model']} ---")
        sys.exit(0)

    # Write to file
    write_result = write_source_list(result['content'], args.output, args.topic)

    if 'error' in write_result:
        print(f"ERROR: {write_result['error']}", file=sys.stderr)
        sys.exit(1)

    # Success output
    print("SUCCESS!")
    print()
    print(f"Source list written to: {write_result['path']}")
    print(f"Sources generated: {args.sources} requested")
    print(f"Model used: {result['model']}")
    print()
    print("Next steps:")
    print("1. Review NOTEBOOKLM-SOURCE-LIST.md")
    print("2. Download/purchase sources (budget is unlimited for quality)")
    print("3. Upload to NotebookLM with naming convention ([P1], [A1], etc.)")
    print("4. Run verification prompts from /sources --prompts")
    print()


if __name__ == '__main__':
    main()
