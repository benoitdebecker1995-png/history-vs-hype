#!/usr/bin/env python3
"""
Tests for pattern_synthesizer_v2.py - Cross-creator synthesis and Part 8 generation.
"""

import pytest
import sqlite3
import json
import tempfile
from pathlib import Path
from datetime import datetime

from pattern_synthesizer_v2 import (
    load_part6_patterns,
    synthesize_universal_patterns,
    generate_part8,
    write_part8_to_style_guide,
    _find_part6_match,
    _format_technique_entry
)
from technique_library import TechniqueLibrary


# =========================================================================
# FIXTURES
# =========================================================================

@pytest.fixture
def temp_db():
    """Create temporary database for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.db', delete=False) as f:
        db_path = f.name

    lib = TechniqueLibrary(db_path)
    yield lib

    # Cleanup
    lib._conn.close()
    Path(db_path).unlink()


@pytest.fixture
def mock_style_guide():
    """Create mock STYLE-GUIDE.md for testing."""
    content = """# Style Guide

## Part 6: Voice Pattern Library

### 6.1 Opening Formulas

#### Opening: Visual Contrast Hook (Belize Pattern)

**Formula:** [Action: Open map A] → [What you see]

#### Opening: Current Event Hook

**Formula:** [Specific date/time] → [Military action]

### 6.2 Transition Sequences

#### Transition: Kraut-Style Causal Chain

**Formula:** [Event A] → [connector] → [Result B]

#### Transition: Temporal Jump with "Now"

**Formula:** [Complete section] → "Now" + [new topic]

### 6.3 Evidence Introduction Patterns

#### Evidence: Setup → Quote → Implication

**Formula:** [State claim] → [Quote] → [Implication]

### 6.4 Sentence Rhythm Patterns

#### Rhythm: Long Setup + Short Punch

**Effect:** Creates emphasis through contrast

### 6.5 Closing Patterns

#### Closing: Return to Overlooked Stakeholders

**Formula:** [Big-picture stakes] → [Return to affected]

### 6.7 Additional High-Performance Patterns

#### Pattern: Immediate Contradiction

**Formula:** [What is claimed] → "But" → [Reality]

## Part 9: Retention Playbook

*Auto-generated section*
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(content)
        style_guide_path = f.name

    yield Path(style_guide_path)

    # Cleanup
    Path(style_guide_path).unlink()


# =========================================================================
# TESTS: Part 6 Pattern Loading
# =========================================================================

def test_load_part6_patterns(mock_style_guide):
    """Test Part 6 pattern loading from STYLE-GUIDE.md."""
    patterns = load_part6_patterns(mock_style_guide)

    assert 'openings' in patterns
    assert 'transitions' in patterns
    assert 'evidence' in patterns
    assert 'rhythm' in patterns
    assert 'closings' in patterns
    assert 'additional' in patterns

    # Check specific patterns were extracted
    assert 'Visual Contrast Hook' in patterns['openings']
    assert 'Current Event Hook' in patterns['openings']
    assert 'Kraut-Style Causal Chain' in patterns['transitions']
    assert 'Setup' in patterns['evidence'][0] if patterns['evidence'] else False


def test_load_part6_patterns_missing_file():
    """Test Part 6 pattern loading with missing file."""
    patterns = load_part6_patterns(Path('/nonexistent/style-guide.md'))

    assert 'error' in patterns
    assert 'not found' in patterns['error']


# =========================================================================
# TESTS: Universal Pattern Synthesis
# =========================================================================

def test_synthesize_universal_patterns_empty_db(temp_db):
    """Test synthesis with empty database."""
    universal_patterns = synthesize_universal_patterns(temp_db)

    # Should return empty dict, not error
    assert isinstance(universal_patterns, dict)
    assert len(universal_patterns) == 0


def test_synthesize_universal_patterns_with_data(temp_db):
    """Test synthesis with techniques in database."""
    # Add techniques with various creator counts
    temp_db.add_technique(
        'opening_hook',
        'visual_contrast',
        '[Action] → [What you see]',
        'Territorial disputes',
        [
            {'creator': 'Kraut', 'video': 'video1.txt', 'text': 'Example 1'},
            {'creator': 'Knowing Better', 'video': 'video2.txt', 'text': 'Example 2'},
            {'creator': 'Shaun', 'video': 'video3.txt', 'text': 'Example 3'}
        ]
    )

    # Update creator_count manually (normally done by store_analysis_results)
    cursor = temp_db._conn.cursor()
    cursor.execute("UPDATE creator_techniques SET creator_count = 3 WHERE technique_name = 'visual_contrast'")
    temp_db._conn.commit()

    # Add technique with low creator count (should NOT be universal)
    temp_db.add_technique(
        'transition',
        'rare_pattern',
        '[Pattern]',
        'Rarely used',
        [{'creator': 'Kraut', 'video': 'video1.txt', 'text': 'Example'}]
    )

    cursor.execute("UPDATE creator_techniques SET creator_count = 1 WHERE technique_name = 'rare_pattern'")
    temp_db._conn.commit()

    # Synthesize
    universal_patterns = synthesize_universal_patterns(temp_db)

    # Check that visual_contrast is universal
    assert 'opening_hook' in universal_patterns
    assert len(universal_patterns['opening_hook']) == 1
    assert universal_patterns['opening_hook'][0]['name'] == 'visual_contrast'
    assert universal_patterns['opening_hook'][0]['creator_count'] == 3

    # Check that rare_pattern is NOT in universal patterns
    assert 'transition' not in universal_patterns or len(universal_patterns['transition']) == 0


# =========================================================================
# TESTS: Part 6 Cross-Reference Detection
# =========================================================================

def test_find_part6_match_exact():
    """Test exact pattern name matching."""
    part6_patterns = {
        'openings': ['Visual Contrast Hook', 'Current Event Hook'],
        'transitions': []
    }

    match = _find_part6_match('visual_contrast_hook', 'opening_hook', part6_patterns)
    assert match is not None
    assert 'Visual Contrast Hook' in match


def test_find_part6_match_partial():
    """Test partial pattern name matching."""
    part6_patterns = {
        'transitions': ['Kraut-Style Causal Chain'],
        'openings': []
    }

    match = _find_part6_match('causal_chain', 'transition', part6_patterns)
    assert match is not None
    assert 'Causal Chain' in match


def test_find_part6_match_no_match():
    """Test no match found."""
    part6_patterns = {
        'openings': ['Visual Contrast Hook'],
        'transitions': []
    }

    match = _find_part6_match('completely_different', 'opening_hook', part6_patterns)
    assert match is None


# =========================================================================
# TESTS: Part 8 Markdown Generation
# =========================================================================

def test_generate_part8_structure(temp_db):
    """Test Part 8 markdown has correct structure."""
    part8_content = generate_part8(temp_db)

    # Check headers
    assert '## Part 8: Creator Technique Library (Auto-Generated)' in part8_content
    assert '### 8.1 Opening Hooks' in part8_content
    assert '### 8.2 Transitions' in part8_content
    assert '### 8.3 Evidence Presentation' in part8_content
    assert '### 8.4 Pacing & Rhythm' in part8_content
    assert '### 8.5 Part 6 Cross-References' in part8_content

    # Check metadata
    assert 'Last updated:' in part8_content
    assert 'Techniques:' in part8_content
    assert 'Creators analyzed:' in part8_content


def test_generate_part8_with_universal_technique(temp_db):
    """Test Part 8 includes universal techniques."""
    # Add universal technique
    temp_db.add_technique(
        'opening_hook',
        'visual_contrast',
        '[Action] → [What you see]',
        'Territorial disputes',
        [
            {'creator': 'Kraut', 'video': 'video1.txt', 'text': 'Example from Kraut'},
            {'creator': 'Knowing Better', 'video': 'video2.txt', 'text': 'Example from KB'},
            {'creator': 'Shaun', 'video': 'video3.txt', 'text': 'Example from Shaun'}
        ],
        is_universal=True
    )

    cursor = temp_db._conn.cursor()
    cursor.execute("UPDATE creator_techniques SET creator_count = 3 WHERE technique_name = 'visual_contrast'")
    temp_db._conn.commit()

    part8_content = generate_part8(temp_db)

    # Check technique appears in Part 8
    assert 'Visual Contrast' in part8_content
    assert '(3 creators)' in part8_content
    assert '**Formula:** [Action] → [What you see]' in part8_content
    assert '**When to use:** Territorial disputes' in part8_content

    # Check examples
    assert 'Kraut' in part8_content
    assert 'Knowing Better' in part8_content


def test_format_technique_entry():
    """Test technique entry formatting."""
    technique = {
        'name': 'visual_contrast',
        'creator_count': 3,
        'formula': '[Action] → [What you see]',
        'when_to_use': 'Territorial disputes',
        'creator_examples': [
            {'creator': 'Kraut', 'video': 'video1.txt', 'text': 'Example text'},
            {'creator': 'Shaun', 'video': 'video2.txt', 'text': 'Another example'}
        ]
    }

    lines = _format_technique_entry(technique)
    content = '\n'.join(lines)

    assert '**Visual Contrast** (3 creators)' in content
    assert '**Formula:** [Action] → [What you see]' in content
    assert '**When to use:** Territorial disputes' in content
    assert '**Kraut**' in content
    assert '**Shaun**' in content


def test_format_technique_entry_with_part6_ref():
    """Test technique entry with Part 6 cross-reference."""
    technique = {
        'name': 'visual_contrast',
        'creator_count': 3,
        'formula': '[Pattern]',
        'when_to_use': 'Usage',
        'creator_examples': [],
        'part6_ref': 'Part 6.1: Visual Contrast Hook'
    }

    lines = _format_technique_entry(technique)
    content = '\n'.join(lines)

    assert 'See also: Part 6.1: Visual Contrast Hook' in content


# =========================================================================
# TESTS: STYLE-GUIDE.md Writing
# =========================================================================

def test_write_part8_new_section(mock_style_guide):
    """Test writing Part 8 to STYLE-GUIDE.md (new section)."""
    part8_content = "## Part 8: Creator Technique Library\n\nTest content"

    result = write_part8_to_style_guide(part8_content, mock_style_guide)

    assert 'success' in result
    assert result['success'] is True

    # Read back and verify
    updated_content = mock_style_guide.read_text(encoding='utf-8')
    assert '## Part 8: Creator Technique Library' in updated_content

    # Check Part 8 appears before Part 9
    part8_pos = updated_content.find('## Part 8:')
    part9_pos = updated_content.find('## Part 9:')
    assert part8_pos < part9_pos


def test_write_part8_replace_existing(mock_style_guide):
    """Test replacing existing Part 8 (idempotent)."""
    # First write
    part8_v1 = "## Part 8: Creator Technique Library\n\nVersion 1"
    write_part8_to_style_guide(part8_v1, mock_style_guide)

    # Second write (should replace)
    part8_v2 = "## Part 8: Creator Technique Library\n\nVersion 2"
    result = write_part8_to_style_guide(part8_v2, mock_style_guide)

    assert 'success' in result

    # Read back and verify only Version 2 exists
    updated_content = mock_style_guide.read_text(encoding='utf-8')
    assert 'Version 2' in updated_content
    assert 'Version 1' not in updated_content

    # Check no duplication
    assert updated_content.count('## Part 8:') == 1


def test_write_part8_preserves_other_parts(mock_style_guide):
    """Test that writing Part 8 doesn't modify other parts."""
    original_content = mock_style_guide.read_text(encoding='utf-8')

    part8_content = "## Part 8: Creator Technique Library\n\nTest"
    write_part8_to_style_guide(part8_content, mock_style_guide)

    updated_content = mock_style_guide.read_text(encoding='utf-8')

    # Check Part 6 is preserved
    assert '## Part 6: Voice Pattern Library' in updated_content
    assert '#### Opening: Visual Contrast Hook' in updated_content

    # Check Part 9 is preserved
    assert '## Part 9: Retention Playbook' in updated_content


def test_write_part8_missing_file():
    """Test error handling when STYLE-GUIDE.md doesn't exist."""
    result = write_part8_to_style_guide(
        "## Part 8: Test",
        Path('/nonexistent/style-guide.md')
    )

    assert 'error' in result
    assert 'not found' in result['error']


# =========================================================================
# INTEGRATION TEST
# =========================================================================

def test_full_integration(temp_db, mock_style_guide):
    """Test full integration: add techniques → synthesize → generate Part 8 → write."""
    # Add multiple techniques
    temp_db.add_technique(
        'opening_hook',
        'visual_contrast',
        '[Action] → [What you see]',
        'Territorial disputes',
        [
            {'creator': 'Kraut', 'video': 'v1.txt', 'text': 'Ex1'},
            {'creator': 'Knowing Better', 'video': 'v2.txt', 'text': 'Ex2'},
            {'creator': 'Shaun', 'video': 'v3.txt', 'text': 'Ex3'}
        ]
    )

    temp_db.add_technique(
        'transition',
        'causal_chain',
        '[Event] → [Result]',
        'Multi-step causation',
        [
            {'creator': 'Kraut', 'video': 'v1.txt', 'text': 'Chain1'},
            {'creator': 'Fall of Civilizations', 'video': 'v2.txt', 'text': 'Chain2'},
            {'creator': 'Historia Civilis', 'video': 'v3.txt', 'text': 'Chain3'}
        ]
    )

    # Update creator counts
    cursor = temp_db._conn.cursor()
    cursor.execute("UPDATE creator_techniques SET creator_count = 3 WHERE technique_name IN ('visual_contrast', 'causal_chain')")
    temp_db._conn.commit()

    # Synthesize
    universal_patterns = synthesize_universal_patterns(temp_db)

    # Should have 2 universal patterns
    assert len(universal_patterns) == 2
    assert 'opening_hook' in universal_patterns
    assert 'transition' in universal_patterns

    # Generate Part 8
    part8_content = generate_part8(temp_db)

    # Write to STYLE-GUIDE.md
    result = write_part8_to_style_guide(part8_content, mock_style_guide)
    assert result['success'] is True

    # Verify content
    updated = mock_style_guide.read_text(encoding='utf-8')
    assert '## Part 8: Creator Technique Library' in updated
    assert 'Visual Contrast' in updated
    assert 'Causal Chain' in updated
    assert '(3 creators)' in updated


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
