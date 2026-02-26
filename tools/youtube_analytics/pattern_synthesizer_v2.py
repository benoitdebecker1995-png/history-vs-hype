#!/usr/bin/env python3
"""
Pattern Synthesizer v2 - Cross-creator synthesis and STYLE-GUIDE.md Part 8 generation.

Identifies universal patterns from 3+ creators, cross-references with Part 6 to avoid
duplication, and auto-generates Part 8 as a creator-validated technique library.

Usage:
    from pattern_synthesizer_v2 import synthesize_universal_patterns, generate_part8

    # Run full pipeline (analyze all transcripts → store → synthesize → write Part 8)
    python pattern_synthesizer_v2.py --synthesize

    # Regenerate Part 8 from existing DB data (skip re-analysis)
    python pattern_synthesizer_v2.py --update

    # Dry run - print Part 8 to stdout without writing
    python pattern_synthesizer_v2.py --dry-run

    # Output raw synthesis data as JSON
    python pattern_synthesizer_v2.py --json

Dependencies:
    - stdlib only: sys, json, pathlib, re, argparse, datetime
    - technique_library.TechniqueLibrary for database access
    - transcript_analyzer for parsing transcripts
"""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

try:
    from .technique_library import TechniqueLibrary
    from .transcript_analyzer import analyze_all_transcripts
except ImportError as e:
    print(f"Error: Required dependencies not found: {e}", file=sys.stderr)
    sys.exit(1)


# =========================================================================
# PART 6 PATTERN LOADING
# =========================================================================

def load_part6_patterns(style_guide_path: Optional[Path] = None) -> Dict[str, List[str]]:
    """
    Parse STYLE-GUIDE.md Part 6 to get existing 29 patterns.

    Returns dict mapping category to pattern name list.
    Used to cross-reference and avoid Part 8 duplicating Part 6.

    Returns:
        {
            'openings': ['Visual Contrast Hook', 'Current Event Hook', ...],
            'transitions': ['Kraut-Style Causal Chain', 'Temporal Jump', ...],
            'evidence': ['Setup Quote Implication', 'Notice this specific phrase', ...],
            'rhythm': ['Long Setup Short Punch', 'Question Zero Answer', ...],
            'closings': ['Return to Overlooked Stakeholders', 'Unanswered Question', ...],
            'additional': ['Immediate Contradiction', 'Specific Stakeholder Quote', ...]
        }
    """
    if style_guide_path is None:
        # Default to .claude/REFERENCE/STYLE-GUIDE.md
        repo_root = Path(__file__).parent.parent.parent
        style_guide_path = repo_root / '.claude' / 'REFERENCE' / 'STYLE-GUIDE.md'

    if not style_guide_path.exists():
        return {'error': f'STYLE-GUIDE.md not found at {style_guide_path}'}

    try:
        content = style_guide_path.read_text(encoding='utf-8')
    except Exception as e:
        return {'error': f'Failed to read STYLE-GUIDE.md: {e}'}

    # Find Part 6 section (capture everything until Part 7, 8, 9, or another ## heading)
    part6_match = re.search(r'^## Part 6:.*?(?=^## (?:Part [789]:|[A-Z])|\Z)', content, re.MULTILINE | re.DOTALL)
    if not part6_match:
        return {'error': 'Part 6 section not found in STYLE-GUIDE.md'}

    part6_content = part6_match.group(0)

    # Extract patterns by category
    patterns = {
        'openings': [],
        'transitions': [],
        'evidence': [],
        'rhythm': [],
        'closings': [],
        'additional': []
    }

    # Section 6.1 Opening Formulas
    openings_section = re.search(r'### 6\.1 Opening Formulas\n(.*?)(?=\n### |\Z)', part6_content, re.DOTALL)
    if openings_section:
        # Extract pattern names from "#### Opening: [Pattern Name]"
        opening_patterns = re.findall(r'#### Opening: (.+?)(?:\s*\(|\s*$)', openings_section.group(1), re.MULTILINE)
        patterns['openings'] = [p.strip() for p in opening_patterns]

    # Section 6.2 Transition Sequences
    transitions_section = re.search(r'### 6\.2 Transition Sequences\n(.*?)(?=\n### |\Z)', part6_content, re.DOTALL)
    if transitions_section:
        transition_patterns = re.findall(r'#### Transition: (.+?)(?:\s*\(|\s*$)', transitions_section.group(1), re.MULTILINE)
        patterns['transitions'] = [p.strip() for p in transition_patterns]

    # Section 6.3 Evidence Introduction Patterns
    evidence_section = re.search(r'### 6\.3 Evidence Introduction Patterns\n(.*?)(?=\n### |\Z)', part6_content, re.DOTALL)
    if evidence_section:
        evidence_patterns = re.findall(r'#### Evidence: (.+?)(?:\s*\(|\s*$)', evidence_section.group(1), re.MULTILINE)
        patterns['evidence'] = [p.strip() for p in evidence_patterns]

    # Section 6.4 Sentence Rhythm Patterns
    rhythm_section = re.search(r'### 6\.4 Sentence Rhythm Patterns\n(.*?)(?=\n### |\Z)', part6_content, re.DOTALL)
    if rhythm_section:
        rhythm_patterns = re.findall(r'#### Rhythm: (.+?)(?:\s*\(|\s*$)', rhythm_section.group(1), re.MULTILINE)
        patterns['rhythm'] = [p.strip() for p in rhythm_patterns]

    # Section 6.5 Closing Patterns
    closings_section = re.search(r'### 6\.5 Closing Patterns\n(.*?)(?=\n### |\Z)', part6_content, re.DOTALL)
    if closings_section:
        closing_patterns = re.findall(r'#### Closing: (.+?)(?:\s*\(|\s*$)', closings_section.group(1), re.MULTILINE)
        patterns['closings'] = [p.strip() for p in closing_patterns]

    # Section 6.7 Additional High-Performance Patterns
    additional_section = re.search(r'### 6\.7 Additional High-Performance Patterns\n(.*?)(?=\n### |\Z)', part6_content, re.DOTALL)
    if additional_section:
        additional_patterns = re.findall(r'#### Pattern: (.+?)(?:\s*\(|\s*$)', additional_section.group(1), re.MULTILINE)
        patterns['additional'] = [p.strip() for p in additional_patterns]

    return patterns


# =========================================================================
# FULL PIPELINE
# =========================================================================

def run_full_pipeline(transcripts_dir: Optional[Path] = None, db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    End-to-end pipeline: analyze transcripts → store techniques → synthesize universals.

    Args:
        transcripts_dir: Path to transcripts directory (default: ../../transcripts/)
        db_path: Path to database (default: keywords.db)

    Returns:
        Dict with:
        - 'transcripts_analyzed': int
        - 'techniques_stored': int
        - 'universal_patterns': dict of universal techniques by category
    """
    if transcripts_dir is None:
        repo_root = Path(__file__).parent.parent.parent
        transcripts_dir = repo_root / 'transcripts'

    print(f"[Pattern Synthesizer v2] Running full pipeline...", file=sys.stderr)
    print(f"[1/3] Analyzing all transcripts from {transcripts_dir}...", file=sys.stderr)

    # Step 1: Analyze all transcripts
    analyses = analyze_all_transcripts(transcripts_dir)

    # analyses is a list of analysis dicts
    if isinstance(analyses, dict) and 'error' in analyses:
        return {'error': f'Transcript analysis failed: {analyses["error"]}'}

    transcripts_analyzed = len(analyses)
    print(f"[1/3] ✓ Analyzed {transcripts_analyzed} transcripts", file=sys.stderr)

    # Step 2: Store results in database
    print(f"[2/3] Storing techniques in database...", file=sys.stderr)
    lib = TechniqueLibrary(db_path)
    store_result = lib.store_analysis_results(analyses)

    if 'error' in store_result:
        return {'error': f'Database storage failed: {store_result["error"]}'}

    techniques_stored = store_result.get('techniques_added', 0)
    print(f"[2/3] ✓ Stored {techniques_stored} techniques", file=sys.stderr)

    # Step 3: Synthesize universal patterns
    print(f"[3/3] Synthesizing universal patterns (3+ creators)...", file=sys.stderr)
    universal_patterns = synthesize_universal_patterns(lib)

    if 'error' in universal_patterns:
        return {'error': f'Synthesis failed: {universal_patterns["error"]}'}

    universal_count = sum(len(patterns) for patterns in universal_patterns.values())
    print(f"[3/3] ✓ Identified {universal_count} universal patterns", file=sys.stderr)

    return {
        'transcripts_analyzed': transcripts_analyzed,
        'techniques_stored': techniques_stored,
        'universal_patterns': universal_patterns
    }


# =========================================================================
# UNIVERSAL PATTERN SYNTHESIS
# =========================================================================

def synthesize_universal_patterns(lib: TechniqueLibrary) -> Dict[str, List[Dict]]:
    """
    Identify universal patterns (3+ creators) and mark them in database.

    Cross-references with Part 6 patterns to avoid duplication.
    Updates is_universal=True for techniques with creator_count >= 3.

    Returns:
        Dict mapping category to list of universal techniques:
        {
            'opening_hook': [
                {'name': 'visual_contrast', 'creator_count': 5, 'part6_ref': 'Visual Contrast Hook', ...},
                ...
            ],
            ...
        }
    """
    # Load Part 6 patterns for cross-reference
    part6_patterns = load_part6_patterns()

    if 'error' in part6_patterns:
        print(f"Warning: Could not load Part 6 patterns: {part6_patterns['error']}", file=sys.stderr)
        part6_patterns = {}

    # Get all techniques from database
    all_techniques = lib.get_all_techniques()

    if 'error' in all_techniques:
        return {'error': all_techniques['error']}

    universal_by_category = defaultdict(list)

    # Process each technique
    for category, techniques in all_techniques.items():
        for tech in techniques:
            creator_count = tech.get('creator_count', 0)

            # Mark as universal if 3+ creators
            is_universal = creator_count >= 3

            # Cross-reference with Part 6
            part6_ref = None
            technique_name = tech.get('technique_name', tech.get('name', ''))
            if is_universal:
                part6_ref = _find_part6_match(technique_name, category, part6_patterns)

            # Update database
            if is_universal:
                update_result = lib._update_technique_universal_status(
                    tech['id'],
                    is_universal=True,
                    style_guide_ref=part6_ref
                )

                if 'error' not in update_result:
                    universal_by_category[category].append({
                        'id': tech['id'],
                        'name': technique_name,
                        'formula': tech.get('formula', ''),
                        'when_to_use': tech.get('when_to_use', ''),
                        'creator_count': creator_count,
                        'creator_examples': tech.get('creator_examples', []),
                        'part6_ref': part6_ref
                    })

    return dict(universal_by_category)


def _find_part6_match(technique_name: str, category: str, part6_patterns: Dict) -> Optional[str]:
    """
    Find matching Part 6 pattern name for technique.

    Uses fuzzy matching to detect similar patterns.
    """
    # Map internal categories to Part 6 categories
    category_map = {
        'opening_hook': 'openings',
        'transition': 'transitions',
        'evidence_pattern': 'evidence',
        'rhythm': 'rhythm',
        'closing': 'closings'
    }

    part6_category = category_map.get(category)
    if not part6_category or part6_category not in part6_patterns:
        return None

    # Normalize technique name for comparison
    norm_tech_name = technique_name.lower().replace('_', ' ')

    # Check for exact or partial matches
    for pattern_name in part6_patterns[part6_category]:
        norm_pattern_name = pattern_name.lower()

        # Exact match
        if norm_tech_name == norm_pattern_name:
            return f"Part 6.{list(category_map.values()).index(part6_category) + 1}: {pattern_name}"

        # Partial match (technique name in pattern name or vice versa)
        if norm_tech_name in norm_pattern_name or norm_pattern_name in norm_tech_name:
            return f"Part 6.{list(category_map.values()).index(part6_category) + 1}: {pattern_name}"

    return None


# =========================================================================
# PART 8 MARKDOWN GENERATION
# =========================================================================

def generate_part8(lib: TechniqueLibrary, part6_patterns: Optional[Dict] = None) -> str:
    """
    Generate Part 8 markdown from database.

    Includes:
    - Header with metadata (last updated, source count)
    - Sections by technique category (8.1-8.5)
    - Universal technique entries with creator examples
    - Part 6 cross-reference section

    Returns:
        Markdown string for Part 8
    """
    if part6_patterns is None:
        part6_patterns = load_part6_patterns()

    # Get all universal techniques
    universal_patterns = {}
    all_techniques = lib.get_all_techniques()

    if 'error' in all_techniques:
        return f"Error generating Part 8: {all_techniques['error']}"

    # Filter for universal patterns (3+ creators)
    for category, techniques in all_techniques.items():
        universal_in_cat = [t for t in techniques if t.get('is_universal', False) or t.get('creator_count', 0) >= 3]
        if universal_in_cat:
            universal_patterns[category] = universal_in_cat

    # Get database stats
    stats = lib.get_statistics()
    total_techniques = stats.get('total_techniques', 0)
    universal_count = stats.get('universal_count', 0)

    # Get transcript count (approximate from creator examples)
    unique_creators = set()
    for techniques in all_techniques.values():
        for tech in techniques:
            examples = tech.get('creator_examples', [])
            if isinstance(examples, str):
                try:
                    examples = json.loads(examples)
                except (json.JSONDecodeError, TypeError):
                    examples = []
            for ex in examples:
                if isinstance(ex, dict):
                    unique_creators.add(ex.get('creator', 'Unknown'))

    transcript_count = len(unique_creators)

    # Build Part 8 markdown
    lines = []
    lines.append("## Part 8: Creator Technique Library (Auto-Generated)")
    lines.append("")
    lines.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d')} | Techniques: {total_techniques} total, {universal_count} universal (3+ creators) | Creators analyzed: {transcript_count}*")
    lines.append("")
    lines.append("> **This section is auto-generated by `python -m tools.youtube_analytics.pattern_synthesizer_v2 --update`.**")
    lines.append("> Run after adding new creator transcripts to update with cross-validated patterns.")
    lines.append("")
    lines.append("**Purpose:** Identify techniques validated across multiple successful creators. Part 8 complements Part 6 by providing creator-validated examples (Part 6 = History vs Hype's proven patterns, Part 8 = cross-creator validation).")
    lines.append("")

    # Section 8.1: Opening Hooks
    lines.append("### 8.1 Opening Hooks")
    lines.append("")
    opening_hooks = universal_patterns.get('opening_hook', [])
    if opening_hooks:
        for technique in opening_hooks:
            lines.extend(_format_technique_entry(technique))
    else:
        lines.append("*Insufficient cross-creator data. Re-run after adding more transcripts.*")
        lines.append("")

    # Section 8.2: Transitions
    lines.append("### 8.2 Transitions")
    lines.append("")
    transitions = universal_patterns.get('transition', [])
    if transitions:
        for technique in transitions:
            lines.extend(_format_technique_entry(technique))
    else:
        lines.append("*Insufficient cross-creator data. Re-run after adding more transcripts.*")
        lines.append("")

    # Section 8.3: Evidence Presentation
    lines.append("### 8.3 Evidence Presentation")
    lines.append("")
    evidence_patterns = universal_patterns.get('evidence_pattern', [])
    if evidence_patterns:
        for technique in evidence_patterns:
            lines.extend(_format_technique_entry(technique))
    else:
        lines.append("*Insufficient cross-creator data. Re-run after adding more transcripts.*")
        lines.append("")

    # Section 8.4: Pacing & Rhythm
    lines.append("### 8.4 Pacing & Rhythm")
    lines.append("")
    pacing_patterns = universal_patterns.get('pacing', [])
    if pacing_patterns:
        for technique in pacing_patterns:
            lines.extend(_format_technique_entry(technique))
    else:
        lines.append("*Insufficient cross-creator data. Re-run after adding more transcripts.*")
        lines.append("")

    # Section 8.5: Part 6 Cross-References
    lines.append("### 8.5 Part 6 Cross-References")
    lines.append("")
    lines.append("**Techniques that overlap with Part 6 patterns:**")
    lines.append("")

    # Build cross-reference table
    cross_refs = []
    for category, techniques in universal_patterns.items():
        for tech in techniques:
            part6_ref = tech.get('part6_ref') or tech.get('style_guide_ref')
            if part6_ref:
                tech_name = tech.get('name') or tech.get('technique_name', '')
                cross_refs.append({
                    'technique': tech_name.replace('_', ' ').title(),
                    'part6': part6_ref,
                    'creators': tech.get('creator_count', 0)
                })

    if cross_refs:
        lines.append("| Part 8 Technique | Part 6 Reference | Creators |")
        lines.append("|------------------|------------------|----------|")
        for ref in cross_refs:
            lines.append(f"| {ref['technique']} | {ref['part6']} | {ref['creators']} |")
    else:
        lines.append("*No overlapping patterns detected.*")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*End of Part 8: Creator Technique Library*")
    lines.append("")

    return '\n'.join(lines)


def _format_technique_entry(technique: Dict) -> List[str]:
    """
    Format single technique as markdown entry.

    Returns list of lines (for joining into markdown).
    """
    lines = []

    # Handle both 'name' and 'technique_name' keys
    name = technique.get('name') or technique.get('technique_name', '')
    name = name.replace('_', ' ').title()
    creator_count = technique.get('creator_count', 0)
    part6_ref = technique.get('part6_ref') or technique.get('style_guide_ref', '')

    # Header: **Name** (N creators) — with Part 6 cross-ref if applicable
    header = f"**{name}** ({creator_count} creators)"
    if part6_ref:
        header += f" — *See also: {part6_ref}*"
    lines.append(header)
    lines.append("")

    # Formula
    formula = technique.get('formula', '')
    if formula:
        lines.append(f"**Formula:** {formula}")
        lines.append("")

    # When to use
    when_to_use = technique.get('when_to_use', '')
    if when_to_use:
        lines.append(f"**When to use:** {when_to_use}")
        lines.append("")

    # Examples (2-3 max)
    examples = technique.get('creator_examples', [])
    if isinstance(examples, str):
        try:
            examples = json.loads(examples)
        except (json.JSONDecodeError, TypeError):
            examples = []

    if examples:
        lines.append("**Examples:**")
        lines.append("")
        for i, example in enumerate(examples[:3], 1):  # Limit to 3 examples
            if isinstance(example, dict):
                creator = example.get('creator', 'Unknown')
                video = example.get('video', '')
                text = example.get('text', '')

                if text:
                    lines.append(f"{i}. **{creator}** ({video}):")
                    lines.append(f"   > {text}")
                    lines.append("")

    lines.append("")

    return lines


# =========================================================================
# STYLE-GUIDE.md UPDATE
# =========================================================================

def write_part8_to_style_guide(content: str, style_guide_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Update STYLE-GUIDE.md with Part 8 content.

    Idempotent: replaces existing Part 8 if present, inserts before Part 9 if not.

    Args:
        content: Part 8 markdown content
        style_guide_path: Path to STYLE-GUIDE.md (default: .claude/REFERENCE/STYLE-GUIDE.md)

    Returns:
        {'success': True} or {'error': str}
    """
    if style_guide_path is None:
        repo_root = Path(__file__).parent.parent.parent
        style_guide_path = repo_root / '.claude' / 'REFERENCE' / 'STYLE-GUIDE.md'

    if not style_guide_path.exists():
        return {'error': f'STYLE-GUIDE.md not found at {style_guide_path}'}

    try:
        original_content = style_guide_path.read_text(encoding='utf-8')
    except Exception as e:
        return {'error': f'Failed to read STYLE-GUIDE.md: {e}'}

    # Check if Part 8 already exists
    part8_match = re.search(r'(^## Part 8:.*?)(?=^## Part [79])', original_content, re.MULTILINE | re.DOTALL)

    if part8_match:
        # Replace existing Part 8 (preserve everything after it)
        start_pos = part8_match.start()

        # Find where Part 8 ends (start of next Part section)
        next_part = re.search(r'^## Part [79]:', original_content[start_pos:], re.MULTILINE)
        if next_part:
            end_pos = start_pos + next_part.start()
            new_content = original_content[:start_pos] + content + '\n\n' + original_content[end_pos:]
        else:
            # Part 8 exists but nothing after it
            new_content = original_content[:start_pos] + content + '\n'
    else:
        # Insert Part 8 before Part 9 (or at end if Part 9 doesn't exist)
        part9_match = re.search(r'^## Part 9:', original_content, re.MULTILINE)

        if part9_match:
            # Insert before Part 9
            insert_pos = part9_match.start()
            new_content = original_content[:insert_pos] + content + '\n\n' + original_content[insert_pos:]
        else:
            # Append at end
            new_content = original_content.rstrip() + '\n\n' + content + '\n'

    # Write updated content
    try:
        style_guide_path.write_text(new_content, encoding='utf-8')
        return {'success': True}
    except Exception as e:
        return {'error': f'Failed to write STYLE-GUIDE.md: {e}'}


# =========================================================================
# CLI
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Cross-creator pattern synthesis and Part 8 generation'
    )

    parser.add_argument(
        '--synthesize',
        action='store_true',
        help='Run full pipeline (analyze transcripts -> store -> synthesize -> generate Part 8)'
    )

    parser.add_argument(
        '--update',
        action='store_true',
        help='Regenerate Part 8 from existing DB data (skip re-analysis)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print Part 8 to stdout without writing to STYLE-GUIDE.md'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output raw synthesis data as JSON'
    )

    parser.add_argument(
        '--transcripts-dir',
        type=Path,
        help='Override transcripts directory'
    )

    parser.add_argument(
        '--db',
        type=str,
        help='Override database path'
    )

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Default action: dry run
    if not any([args.synthesize, args.update, args.dry_run, args.json]):
        args.dry_run = True

    if args.synthesize:
        # Full pipeline
        result = run_full_pipeline(args.transcripts_dir, args.db)

        if 'error' in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)

        # Generate Part 8
        lib = TechniqueLibrary(args.db)
        part8_content = generate_part8(lib)

        # Write to STYLE-GUIDE.md
        write_result = write_part8_to_style_guide(part8_content)

        if 'error' in write_result:
            print(f"Error writing Part 8: {write_result['error']}", file=sys.stderr)
            sys.exit(1)

        print(f"\n✓ Part 8 generated and written to STYLE-GUIDE.md", file=sys.stderr)
        print(f"  Transcripts analyzed: {result['transcripts_analyzed']}")
        print(f"  Techniques stored: {result['techniques_stored']}")
        print(f"  Universal patterns: {sum(len(p) for p in result['universal_patterns'].values())}")

    elif args.update:
        # Regenerate from DB
        lib = TechniqueLibrary(args.db)
        part8_content = generate_part8(lib)

        write_result = write_part8_to_style_guide(part8_content)

        if 'error' in write_result:
            print(f"Error writing Part 8: {write_result['error']}", file=sys.stderr)
            sys.exit(1)

        print(f"✓ Part 8 regenerated from database and written to STYLE-GUIDE.md", file=sys.stderr)

    elif args.dry_run:
        # Print to stdout
        lib = TechniqueLibrary(args.db)
        part8_content = generate_part8(lib)
        print(part8_content)

    elif args.json:
        # Output raw data
        lib = TechniqueLibrary(args.db)
        universal_patterns = synthesize_universal_patterns(lib)
        print(json.dumps(universal_patterns, indent=2))


if __name__ == '__main__':
    main()
