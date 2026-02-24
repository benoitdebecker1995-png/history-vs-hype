"""Corpus builder for comparing scripts to transcripts.

This module provides functions to:
1. Extract clean plaintext from markdown scripts
2. Parse SRT subtitle files to text
3. Compare scripts to transcripts using word-level diffs
4. Find all available script+SRT pairs in the project

Performance notes:
- Uses word-level comparison (not character-level) to avoid O(n^2) on long texts
- Handles malformed SRT gracefully via srt library
- Normalizes whitespace before comparison
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
import srt


def extract_script_body(markdown_text: str) -> str:
    """Remove markdown formatting and stage directions from script.

    Extracts clean plaintext for comparison by removing:
    - Markdown headers (# ## ###)
    - Stage directions ([ON-CAMERA], [MAP: ...], **[...]**)
    - Bold/italic markers (** *)
    - Multiple spaces (normalize whitespace)

    Args:
        markdown_text: Raw markdown script content

    Returns:
        Clean plaintext suitable for word-level comparison

    Example:
        >>> text = "## Opening\\n\\n[ON-CAMERA]\\n\\nThis is **important**."
        >>> extract_script_body(text)
        'This is important.'
    """
    # Remove markdown headers
    text = re.sub(r'^#+\s+.*$', '', markdown_text, flags=re.MULTILINE)

    # Remove stage directions [ON-CAMERA], [MAP: ...], **[...]**
    text = re.sub(r'\*?\[.*?\]\*?', '', text)

    # Remove bold/italic markers
    text = re.sub(r'\*\*?', '', text)

    # Remove multiple spaces, normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def parse_srt_to_text(srt_path: Path) -> str:
    """Parse SRT subtitle file and concatenate content into continuous text.

    Uses srt library to handle timing data and malformed files gracefully.

    Args:
        srt_path: Path to SRT subtitle file

    Returns:
        Concatenated subtitle text with spaces between blocks

    Raises:
        FileNotFoundError: If SRT file doesn't exist
        UnicodeDecodeError: If file encoding is not UTF-8 (tries common alternatives)
    """
    # Try UTF-8 first, fall back to common alternatives
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(srt_path, 'r', encoding=encoding) as f:
                content = f.read()
                subtitles = list(srt.parse(content))
                # Concatenate all subtitle content with spaces
                return ' '.join(sub.content.replace('\n', ' ') for sub in subtitles)
        except UnicodeDecodeError:
            continue
        except srt.SRTParseError as e:
            # Log warning but continue - may be malformed SRT
            print(f"Warning: Malformed SRT at {srt_path}: {e}")
            return ""

    raise UnicodeDecodeError(f"Could not decode {srt_path} with any common encoding")


def compare_script_to_transcript(script_path: Path, srt_path: Path) -> List[Dict]:
    """Compare script to transcript and extract word-level modifications.

    Uses difflib.SequenceMatcher for word-level comparison to identify:
    - Substitutions (replace): Word/phrase changed
    - Deletions (delete): Word/phrase removed
    - Insertions (insert): Word/phrase added

    Args:
        script_path: Path to markdown script file
        srt_path: Path to SRT transcript file

    Returns:
        List of modification dictionaries with structure:
        [
            {'type': 'substitution', 'original': 'utilize', 'modified': 'use'},
            {'type': 'deletion', 'original': 'it should be noted that'},
            {'type': 'addition', 'modified': 'actually'}
        ]

    Performance:
        - Word-level comparison is O(n*m) where n, m are word counts
        - For typical scripts (2000 words), completes in <1 second
    """
    # Read and extract script body
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = extract_script_body(f.read())

    # Parse SRT transcript
    transcript_text = parse_srt_to_text(srt_path)

    # Tokenize to word lists (lowercase for comparison)
    script_words = script_text.lower().split()
    transcript_words = transcript_text.lower().split()

    # Skip if lengths are drastically different (>50% = likely wrong pair)
    if len(script_words) == 0 or len(transcript_words) == 0:
        return []

    length_ratio = max(len(script_words), len(transcript_words)) / min(len(script_words), len(transcript_words))
    if length_ratio > 1.5:
        print(f"Warning: Script/transcript length mismatch ({len(script_words)} vs {len(transcript_words)} words)")
        print(f"  Ratio: {length_ratio:.2f} - may be wrong pair")

    # Word-level sequence matching
    matcher = SequenceMatcher(None, script_words, transcript_words)

    # Extract modifications from opcodes
    modifications = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            modifications.append({
                'type': 'substitution',
                'original': ' '.join(script_words[i1:i2]),
                'modified': ' '.join(transcript_words[j1:j2])
            })
        elif tag == 'delete':
            modifications.append({
                'type': 'deletion',
                'original': ' '.join(script_words[i1:i2])
            })
        elif tag == 'insert':
            modifications.append({
                'type': 'addition',
                'modified': ' '.join(transcript_words[j1:j2])
            })
        # 'equal' tag ignored - no modifications

    return modifications


def find_video_pairs(projects_dir: Path) -> List[Tuple[Path, Path]]:
    """Scan video projects for folders with both script and SRT files.

    Searches _IN_PRODUCTION and _READY_TO_FILM for video pairs.
    Matches SCRIPT.md or SCRIPT-PART*.md with *.srt files.
    Excludes SPANISH and BACKUP SRT files.

    Args:
        projects_dir: Root video-projects directory

    Returns:
        List of (script_path, srt_path) tuples for valid pairs

    Example:
        >>> pairs = find_video_pairs(Path('video-projects'))
        >>> len(pairs)
        11
        >>> pairs[0]
        (Path('video-projects/_IN_PRODUCTION/1-somaliland-2025/SCRIPT.md'),
         Path('video-projects/_IN_PRODUCTION/1-somaliland-2025/somaliland.srt'))
    """
    pairs = []

    # Search both lifecycle folders
    lifecycle_folders = ['_IN_PRODUCTION', '_READY_TO_FILM']

    for lifecycle in lifecycle_folders:
        lifecycle_path = projects_dir / lifecycle
        if not lifecycle_path.exists():
            continue

        # Iterate through video project folders
        for project_dir in lifecycle_path.iterdir():
            if not project_dir.is_dir():
                continue

            # Find script file (prefer SCRIPT.md, fall back to SCRIPT-PART*.md)
            script_file = project_dir / 'SCRIPT.md'
            if not script_file.exists():
                # Try SCRIPT-PART*.md (for multi-part videos like Iran)
                part_scripts = list(project_dir.glob('SCRIPT-PART*.md'))
                if part_scripts:
                    # Use first part for pattern analysis
                    script_file = part_scripts[0]
                else:
                    continue

            # Find SRT files (exclude SPANISH, BACKUP)
            srt_files = [
                f for f in project_dir.glob('*.srt')
                if 'SPANISH' not in f.name.upper() and 'BACKUP' not in f.name.upper()
            ]

            if srt_files:
                # Use first valid SRT file
                pairs.append((script_file, srt_files[0]))

    return pairs
