"""
Synthesis Engine Module

Merges internal script analysis + external VidIQ/Gemini intelligence into a
ranked metadata package with 3 A/B-testable title+thumbnail pairings.

Each variant is labeled by test hypothesis:
    Variant A: Keyword-Optimized — maximizes search discoverability
    Variant B: Curiosity Gap — creates knowledge-gap intrigue
    Variant C: Authority Angle — establishes intellectual credibility

Output includes content moderation scoring (informational, not blocking)
and Photoshop-ready thumbnail blueprints with per-element AI-generation tagging.

Usage:
    from tools.production.synthesis_engine import synthesize

    result = synthesize(
        project_path='video-projects/_IN_PRODUCTION/35-gibraltar-2026',
        script_path='video-projects/_IN_PRODUCTION/35-gibraltar-2026/02-SCRIPT-DRAFT.md'
    )
    # Returns {'output_path': str} or {'error': str}
"""

import re
from datetime import datetime, timezone
from pathlib import Path

from tools.logging_config import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Source weighting — each source contributes differently per variant type
# ---------------------------------------------------------------------------

SOURCE_WEIGHTS = {
    'vidiq_keyword_data': {'keyword_variant': 0.9, 'curiosity_variant': 0.3, 'authority_variant': 0.4},
    'vidiq_titles': {'keyword_variant': 0.7, 'curiosity_variant': 0.5, 'authority_variant': 0.5},
    'gemini_creative': {'keyword_variant': 0.2, 'curiosity_variant': 0.9, 'authority_variant': 0.8},
    'internal_entities': {'keyword_variant': 0.5, 'curiosity_variant': 0.4, 'authority_variant': 0.9},
    'intel_competitors': {'keyword_variant': 0.6, 'curiosity_variant': 0.3, 'authority_variant': 0.3},
}


# ---------------------------------------------------------------------------
# Content moderation triggers — informational, NOT blocking
# ---------------------------------------------------------------------------

MODERATION_TRIGGERS = {
    'HIGH': [
        'genocide', 'massacre', 'holocaust', 'nazi', 'torture',
        'execution', 'ethnic cleansing', 'rape', 'terrorism',
    ],
    'MEDIUM': [
        'coup', 'assassination', 'war crimes', 'atrocities', 'propaganda',
        'dictator', 'apartheid', 'slavery',
    ],
    'LOW': [
        'colonial', 'occupation', 'disputed', 'controversial',
        'conflict', 'invasion',
    ],
}

# Safe alternatives for HIGH-risk terms in titles (informational suggestions)
_SAFE_ALTERNATIVES = {
    'genocide': 'mass atrocity',
    'massacre': 'mass killing',
    'nazi': 'Third Reich',
    'torture': 'interrogation',
    'execution': 'death sentence',
    'ethnic cleansing': 'forced displacement',
    'rape': 'sexual violence',
    'terrorism': 'political violence',
    # holocaust: keep per channel policy (explicit about sensitive topics)
}

# Data types the engine checks for completeness
_EXPECTED_TYPES = [
    'keyword_data', 'title_suggestions', 'thumbnail_concepts',
    'tag_set', 'description_draft',
]

_MISSING_TYPE_WARNINGS = {
    'keyword_data': 'No keyword data — title variants will lack search volume grounding',
    'title_suggestions': 'No external title suggestions — using internal generation only',
    'thumbnail_concepts': 'No external thumbnail concepts — blueprints based on internal analysis only',
    'tag_set': 'No external tags — using internally generated tags only',
    'description_draft': 'No external description draft — using internally generated description only',
}


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def synthesize(project_path: str, script_path: str = None) -> dict:
    """Synthesize internal + external intelligence into ranked metadata package.

    Reads EXTERNAL-INTELLIGENCE.json from project_path.
    Optionally reads script for additional internal analysis.
    Writes METADATA-SYNTHESIS.md to project_path.

    Args:
        project_path: Path to the video project folder.
        script_path: Optional path to script for internal entity analysis.

    Returns:
        {'output_path': str} on success, {'error': str} on failure.
    """
    try:
        project = Path(project_path)
        if not project.exists():
            return {'error': f'synthesis_engine.synthesize: project folder not found — {project}'}

        # --- Load external intelligence ---
        from tools.production.intake_parser import load_or_create_intelligence

        intel_data = load_or_create_intelligence(project_path)
        sessions = intel_data.get('sessions', [])

        if not sessions:
            return {'error': 'synthesis_engine.synthesize: No intake data. Run /publish --intake first.'}

        # --- Data completeness check ---
        found_types = set()
        for s in sessions:
            found_types.add(s.get('type', ''))

        warnings = []
        for expected in _EXPECTED_TYPES:
            if expected not in found_types:
                msg = _MISSING_TYPE_WARNINGS.get(expected, f'Missing {expected}')
                warnings.append(msg)
                logger.warning(msg)

        completeness = len(found_types.intersection(_EXPECTED_TYPES))
        logger.info("Data completeness: %d/%d types available", completeness, len(_EXPECTED_TYPES))

        # --- Gather inputs from sessions ---
        all_keywords = _collect_from_sessions(sessions, 'keyword_data', 'keywords')
        all_titles = _collect_from_sessions(sessions, 'title_suggestions', 'titles')
        all_concepts = _collect_from_sessions(sessions, 'thumbnail_concepts', 'concepts')
        all_tags = _collect_from_sessions(sessions, 'tag_set', 'tags')
        all_descriptions = _collect_from_sessions(sessions, 'description_draft', 'description')

        # --- Internal analysis (optional) ---
        internal_entities = []
        sections = []
        if script_path:
            script = Path(script_path)
            if script.exists():
                logger.info("Analyzing script: %s", script.name)
                sections, internal_entities = _analyze_script_for_synthesis(script)
            else:
                logger.warning("Script not found: %s — skipping internal analysis", script)

        # --- Competitor context ---
        from tools.production.prompt_generator import _get_competitor_context
        competitor = _get_competitor_context()
        outlier_titles = competitor.get('outlier_titles', [])

        # --- Apply tone filter to all title candidates ---
        from tools.production.metadata import MetadataGenerator
        tone_filter = MetadataGenerator()

        filtered_ext_titles = []
        for t in all_titles:
            title_text = t.get('title', '')
            if title_text:
                filtered = tone_filter._apply_tone_filter(title_text)
                filtered_ext_titles.append({'title': filtered, 'char_count': len(filtered)})

        # --- Build 3 variants ---
        variant_a = _build_variant_a(filtered_ext_titles, all_keywords, outlier_titles, internal_entities, tone_filter)
        variant_b = _build_variant_b(filtered_ext_titles, all_concepts, internal_entities, tone_filter)
        variant_c = _build_variant_c(filtered_ext_titles, internal_entities, sections, tone_filter)

        # --- Ensure all 3 titles are distinct ---
        _ensure_distinct([variant_a, variant_b, variant_c])

        # --- Moderation scoring for each variant ---
        for variant in [variant_a, variant_b, variant_c]:
            variant['moderation'] = _score_moderation(variant['title'])

        # --- Thumbnail blueprints ---
        variant_a['thumbnail'] = _build_thumbnail_blueprint(
            'keyword', variant_a, all_concepts, internal_entities
        )
        variant_b['thumbnail'] = _build_thumbnail_blueprint(
            'curiosity', variant_b, all_concepts, internal_entities
        )
        variant_c['thumbnail'] = _build_thumbnail_blueprint(
            'authority', variant_c, all_concepts, internal_entities
        )

        # --- Description + tags ---
        merged_description = _merge_description(all_descriptions, sections, internal_entities)
        desc_moderation = _score_moderation(merged_description)
        merged_tags = _merge_tags(all_tags, internal_entities, sections)
        tags_str = ', '.join(merged_tags)
        tags_moderation = _score_moderation(tags_str)

        # --- Conflict flagging ---
        conflicts = _detect_conflicts(all_titles, all_concepts, outlier_titles, sessions)

        # --- Data quality notes ---
        parseable_ratios = [s.get('parseable_ratio', 0) for s in sessions if s.get('parseable_ratio') is not None]
        avg_ratio = sum(parseable_ratios) / max(len(parseable_ratios), 1)

        # --- Render output ---
        project_name = project.name
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        content = _render_synthesis(
            project_name=project_name,
            generated=now,
            found_types=sorted(found_types.intersection(_EXPECTED_TYPES)),
            completeness=completeness,
            variant_a=variant_a,
            variant_b=variant_b,
            variant_c=variant_c,
            description=merged_description,
            desc_moderation=desc_moderation,
            tags_str=tags_str,
            tags_count=len(merged_tags),
            tags_moderation=tags_moderation,
            conflicts=conflicts,
            warnings=warnings,
            avg_ratio=avg_ratio,
        )

        output_path = project / "METADATA-SYNTHESIS.md"
        output_path.write_text(content, encoding='utf-8')
        logger.info("Wrote %s", output_path.name)

        return {'output_path': str(output_path)}

    except Exception as e:
        return {'error': f'synthesis_engine.synthesize: unexpected error — {e}'}


# ---------------------------------------------------------------------------
# Session data collectors
# ---------------------------------------------------------------------------

def _collect_from_sessions(sessions: list, session_type: str, parsed_key: str) -> list:
    """Collect parsed items of a specific type from all sessions."""
    items = []
    for s in sessions:
        if s.get('type') == session_type:
            parsed = s.get('parsed', {})
            data = parsed.get(parsed_key, [])
            if isinstance(data, list):
                items.extend(data)
            elif isinstance(data, dict):
                items.append(data)
    return items


def _analyze_script_for_synthesis(script_path: Path):
    """Parse script and extract entities for synthesis. Returns (sections, entities)."""
    try:
        from tools.production.parser import ScriptParser
        from tools.production.entities import EntityExtractor

        parser = ScriptParser()
        sections = parser.parse_file(script_path)

        extractor = EntityExtractor()
        entities = extractor.extract_from_sections(sections)

        return sections, entities
    except Exception as e:
        logger.warning("Script analysis failed: %s", e)
        return [], []


# ---------------------------------------------------------------------------
# Variant builders
# ---------------------------------------------------------------------------

def _build_variant_a(ext_titles, keywords, outlier_titles, entities, tone_filter):
    """Variant A: Keyword-Optimized — maximize search volume keywords."""
    # Score external titles by keyword relevance
    keyword_terms = {kw.get('term', '').lower() for kw in keywords if kw.get('term')}

    best_title = None
    best_score = -1

    for t in ext_titles:
        title = t.get('title', '')
        if not title:
            continue
        # Score by keyword overlap
        title_words = set(title.lower().split())
        overlap = len(title_words.intersection(keyword_terms))
        # Prefer shorter titles (more focused)
        length_bonus = 0.5 if 50 <= len(title) <= 65 else 0
        score = overlap + length_bonus
        if score > best_score:
            best_score = score
            best_title = title

    # Fallback: build from top keywords + entities
    if not best_title:
        places = [e.text for e in entities if e.entity_type == 'place'][:2] if entities else []
        top_kw = [kw.get('term', '') for kw in keywords[:3]]
        if places and top_kw:
            best_title = f"{places[0]}: {' '.join(top_kw[:2])}"
        elif places:
            best_title = f"{places[0]}: Historical Evidence Examined"
        elif top_kw:
            best_title = f"{top_kw[0].title()}: Evidence-Based Analysis"
        else:
            best_title = "Historical Evidence Examined"

    best_title = tone_filter._apply_tone_filter(best_title)
    best_title = tone_filter._truncate_title(best_title)

    return {
        'label': 'Variant A: Keyword-Optimized',
        'hypothesis': 'Maximizes search discoverability via high-volume keywords',
        'title': best_title,
        'char_count': len(best_title),
    }


def _build_variant_b(ext_titles, concepts, entities, tone_filter):
    """Variant B: Curiosity Gap — create knowledge gap from creative angles."""
    # Prefer titles with question marks, colons, or intrigue words
    intrigue_words = {'why', 'how', 'what', 'secret', 'hidden', 'real', 'actually', 'really', 'truth'}

    best_title = None
    best_score = -1

    for t in ext_titles:
        title = t.get('title', '')
        if not title:
            continue
        title_words = set(title.lower().split())
        score = len(title_words.intersection(intrigue_words))
        if '?' in title:
            score += 2
        if ':' in title:
            score += 1
        if score > best_score:
            best_score = score
            best_title = title

    # Fallback: build curiosity gap from concepts or entities
    if not best_title:
        if concepts:
            label = concepts[0].get('label', '')
            best_title = f"What {label} Reveals About This Dispute"
        elif entities:
            places = [e.text for e in entities if e.entity_type == 'place'][:1]
            if places:
                best_title = f"Why Nobody Talks About {places[0]}"
            else:
                best_title = "The History They Left Out"
        else:
            best_title = "The History They Left Out"

    best_title = tone_filter._apply_tone_filter(best_title)
    best_title = tone_filter._truncate_title(best_title)

    return {
        'label': 'Variant B: Curiosity Gap',
        'hypothesis': 'Creates click-through intrigue via knowledge gap framing',
        'title': best_title,
        'char_count': len(best_title),
    }


def _build_variant_c(ext_titles, entities, sections, tone_filter):
    """Variant C: Authority Angle — establish intellectual credibility."""
    # Prefer titles mentioning documents, dates, specific evidence
    authority_words = {'document', 'treaty', 'evidence', 'source', 'court', 'ruling',
                       'clause', 'article', 'archive', 'manuscript', 'map', 'census'}

    best_title = None
    best_score = -1

    for t in ext_titles:
        title = t.get('title', '')
        if not title:
            continue
        title_words = set(title.lower().split())
        score = len(title_words.intersection(authority_words))
        if score > best_score:
            best_score = score
            best_title = title

    # Fallback: build from documents/entities
    if not best_title:
        documents = [e.text for e in entities if e.entity_type == 'document'][:1] if entities else []
        places = [e.text for e in entities if e.entity_type == 'place'][:1] if entities else []
        dates = [e.text for e in entities if e.entity_type == 'date'][:1] if entities else []

        if documents and dates:
            best_title = f"The {dates[0]} {documents[0]}: What It Actually Says"
        elif documents:
            best_title = f"Reading the {documents[0]}: Primary Source Analysis"
        elif places:
            best_title = f"{places[0]}: What the Primary Sources Show"
        else:
            best_title = "What the Primary Sources Actually Show"

    best_title = tone_filter._apply_tone_filter(best_title)
    best_title = tone_filter._truncate_title(best_title)

    return {
        'label': 'Variant C: Authority Angle',
        'hypothesis': 'Establishes intellectual credibility via primary source evidence',
        'title': best_title,
        'char_count': len(best_title),
    }


def _ensure_distinct(variants: list):
    """Ensure all 3 variant titles are distinct. Modify duplicates with suffix."""
    titles_seen = set()
    for variant in variants:
        title = variant['title']
        if title in titles_seen:
            # Append variant label fragment to disambiguate
            label_word = variant['label'].split(':')[1].strip().split()[0] if ':' in variant['label'] else 'Alt'
            new_title = f"{title} ({label_word})"
            if len(new_title) > 70:
                new_title = new_title[:67] + "..."
            variant['title'] = new_title
            variant['char_count'] = len(new_title)
        titles_seen.add(variant['title'])


# ---------------------------------------------------------------------------
# Moderation scoring
# ---------------------------------------------------------------------------

def _score_moderation(text: str) -> dict:
    """Scan text for moderation triggers. Returns risk level + details.

    Moderation is informational, NOT blocking. HIGH = flag with note + alternatives.
    """
    if not text:
        return {'level': 'LOW', 'triggers': [], 'notes': []}

    text_lower = text.lower()
    found_triggers = []
    notes = []
    highest_level = 'LOW'

    level_priority = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}

    for level in ['HIGH', 'MEDIUM', 'LOW']:
        for trigger in MODERATION_TRIGGERS[level]:
            if trigger in text_lower:
                found_triggers.append({'term': trigger, 'level': level})

                if level_priority[level] > level_priority[highest_level]:
                    highest_level = level

                # Generate context-aware notes
                if level == 'HIGH':
                    safe_alt = _SAFE_ALTERNATIVES.get(trigger)
                    note = f"Contains '{trigger}' — YouTube may restrict monetization. Standard for historical/educational content."
                    if safe_alt:
                        note += f" Safe alternative: '{safe_alt}'"
                    elif trigger == 'holocaust':
                        note += " Channel policy: keep explicit (per CLAUDE.md)."
                    notes.append(note)
                elif level == 'MEDIUM':
                    notes.append(f"Contains '{trigger}' — may affect ad suitability. Generally safe for educational context.")

    return {
        'level': highest_level,
        'triggers': found_triggers,
        'notes': notes,
    }


# ---------------------------------------------------------------------------
# Thumbnail blueprint generation
# ---------------------------------------------------------------------------

def _build_thumbnail_blueprint(variant_type: str, variant: dict, concepts: list, entities: list) -> dict:
    """Build a thumbnail blueprint for a variant.

    variant_type: 'keyword' | 'curiosity' | 'authority'
    """
    title = variant.get('title', '')
    moderation = variant.get('moderation', {})
    mod_level = moderation.get('level', 'LOW')

    # Determine if topic is sensitive (HIGH moderation)
    is_sensitive = mod_level == 'HIGH'

    # Select concept approach based on variant type
    if variant_type == 'keyword':
        concept = "Clear subject with readable text — optimized for search thumbnail grid"
        composition = "Subject centered, bold text overlay top-third. Clean background for legibility."
        color_palette = ["#1A1A2E (dark navy)", "#E94560 (accent red)", "#FFFFFF (text white)"]
        text_overlay = _suggest_text_overlay(title, 'top-left', 'bold sans-serif')
        asset_types = ['map', 'modern footage']
        ai_elements = [
            {'element': 'Background map highlight', 'tool': 'VidIQ image generator',
             'prompt': f'Clean geographic map highlighting region from: {title[:40]}'},
            {'element': 'Text overlay', 'tool': 'Manual Photoshop', 'description': 'Bold white text on dark gradient'},
        ]

    elif variant_type == 'curiosity':
        concept = "Contrast or question element — designed to create visual intrigue"
        composition = "Split or diagonal composition. Left: familiar image. Right: surprising reveal."
        color_palette = ["#0F3460 (deep blue)", "#E94560 (contrast red)", "#F5F5F5 (clean white)"]
        text_overlay = _suggest_text_overlay(title, 'center', 'bold sans-serif')
        asset_types = ['archival photo', 'modern footage', 'document scan']
        ai_elements = [
            {'element': 'Contrast background', 'tool': 'Napkin AI',
             'prompt': f'Split visual showing before/after or contrast for: {title[:40]}'},
            {'element': 'Question text overlay', 'tool': 'Manual Photoshop', 'description': 'Large question or hook text'},
        ]

    else:  # authority
        concept = "Primary source or document emphasis — establishes evidence-based credibility"
        composition = "Document or map as focal point, subtle vignette. Evidence front and center."
        color_palette = ["#2C3333 (charcoal)", "#D4A373 (parchment gold)", "#FFFFFF (text white)"]
        text_overlay = _suggest_text_overlay(title, 'bottom-right', 'serif')
        asset_types = ['document scan', 'map', 'archival photo']
        ai_elements = [
            {'element': 'Document texture background', 'tool': 'VidIQ image generator',
             'prompt': f'Aged parchment or document texture for historical topic: {title[:40]}'},
            {'element': 'Source highlight overlay', 'tool': 'Manual Photoshop',
             'description': 'Highlighted excerpt from primary source document'},
        ]

    # Override AI elements for sensitive topics
    sensitivity_note = ""
    if is_sensitive:
        sensitivity_note = "Use real archival photos only — no AI generation for this topic"
        ai_elements = [
            {'element': 'All visual elements', 'tool': 'Manual Photoshop',
             'description': 'Use real archival photographs. No AI-generated imagery for sensitive historical topics.'},
        ]

    # Incorporate external concepts if available
    if concepts:
        ext_concept = concepts[0].get('description', '')[:100]
        concept += f". External suggestion: {ext_concept}"

    # Moderation risk for thumbnail
    thumb_mod = _score_moderation(concept)

    return {
        'concept': concept,
        'composition': composition,
        'color_palette': color_palette,
        'text_overlay': text_overlay,
        'mobile_legibility': "Text readable at 120px width. Max 4 words. High contrast ratio (>4.5:1).",
        'asset_types': asset_types,
        'ai_elements': ai_elements,
        'sensitivity_note': sensitivity_note,
        'moderation_risk': thumb_mod['level'],
    }


def _suggest_text_overlay(title: str, position: str, font_style: str) -> dict:
    """Generate text overlay guidance from title."""
    # Extract 2-4 key words from title for overlay
    words = title.split()
    # Skip common small words
    skip = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'was', 'that', 'this'}
    key_words = [w for w in words if w.lower() not in skip][:4]
    overlay_text = ' '.join(key_words) if key_words else title[:20]

    return {
        'text': overlay_text,
        'position': position,
        'font_style': font_style,
        'size': 'Large — readable at 120px thumbnail width',
        'contrast': 'white on dark' if 'dark' in font_style or position in ('top-left', 'bottom-right') else 'dark on light',
    }


# ---------------------------------------------------------------------------
# Description + tag merging
# ---------------------------------------------------------------------------

def _merge_description(ext_descriptions: list, sections: list, entities: list) -> str:
    """Merge external description drafts with internal analysis."""
    parts = []

    # Use external description if available
    if ext_descriptions:
        for desc in ext_descriptions:
            if isinstance(desc, dict) and desc.get('text'):
                parts.append(desc['text'])
            elif isinstance(desc, list):
                for d in desc:
                    if isinstance(d, dict) and d.get('text'):
                        parts.append(d['text'])

    # Fallback: generate from sections + entities
    if not parts and sections:
        from tools.production.metadata import MetadataGenerator
        gen = MetadataGenerator()
        hook = gen._extract_hook(sections[0].content) if sections else ""
        if hook:
            parts.append(hook)

        # Add document list
        documents = [e.text for e in entities if e.entity_type == 'document'][:5] if entities else []
        if documents:
            parts.append("\nKey documents referenced:")
            for doc in documents:
                parts.append(f"- {doc}")

    if not parts:
        parts.append("[Description to be written — no external or internal data available]")

    return '\n'.join(parts)


def _merge_tags(ext_tags: list, entities: list, sections: list) -> list:
    """Merge external tags with internally generated tags. Deduplicate, respect 500-char limit."""
    seen = set()
    merged = []

    # External tags first
    for t in ext_tags:
        tag = t.get('tag', '') if isinstance(t, dict) else str(t)
        tag = tag.strip()
        if tag and tag.lower() not in seen:
            merged.append(tag)
            seen.add(tag.lower())

    # Internal entity tags
    if entities:
        for e in sorted(entities, key=lambda x: x.mentions, reverse=True)[:10]:
            tag = e.text.strip()
            if tag and tag.lower() not in seen and len(tag) <= 50:
                merged.append(tag)
                seen.add(tag.lower())

    # Section heading tags
    if sections and len(merged) < 15:
        for s in sections[:5]:
            for word in s.heading.split():
                word = word.strip('.,;:()[]')
                if len(word) >= 4 and word.lower() not in seen and word.lower() not in {'the', 'and', 'for', 'with', 'from', 'this', 'that', 'section'}:
                    merged.append(word)
                    seen.add(word.lower())
                    if len(merged) >= 25:
                        break
            if len(merged) >= 25:
                break

    # Enforce 500-char YouTube tag limit
    final = []
    total_chars = 0
    for tag in merged:
        # YouTube counts tag + comma + space
        tag_cost = len(tag) + 2
        if total_chars + tag_cost > 500:
            break
        final.append(tag)
        total_chars += tag_cost

    return final


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def _detect_conflicts(ext_titles: list, concepts: list, outlier_titles: list, sessions: list) -> list:
    """Detect conflicts between VidIQ, Gemini, and internal recommendations."""
    conflicts = []

    # Check if VidIQ and Gemini sessions exist with different title approaches
    vidiq_sessions = [s for s in sessions if s.get('source') == 'vidiq_pro_coach' and s.get('type') == 'title_suggestions']
    gemini_sessions = [s for s in sessions if s.get('source') == 'gemini' and s.get('type') == 'title_suggestions']

    if vidiq_sessions and gemini_sessions:
        conflicts.append(
            "VidIQ and Gemini both provided title suggestions. "
            "VidIQ titles tend toward keyword optimization; Gemini titles toward creative framing. "
            "Both included as separate variant inputs."
        )

    # Check if external and internal entity analysis disagree on focus
    vidiq_keywords = [s for s in sessions if s.get('type') == 'keyword_data']
    if vidiq_keywords and outlier_titles:
        conflicts.append(
            "Competitor outlier titles available alongside VidIQ keyword data. "
            "Outlier patterns may suggest different framing than keyword volume data."
        )

    if not conflicts:
        conflicts.append("No conflicts detected — all sources aligned.")

    return conflicts


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------

def _render_synthesis(
    project_name, generated, found_types, completeness,
    variant_a, variant_b, variant_c,
    description, desc_moderation,
    tags_str, tags_count, tags_moderation,
    conflicts, warnings, avg_ratio,
) -> str:
    """Render the final METADATA-SYNTHESIS.md content."""
    lines = [
        "# Metadata Synthesis",
        f"Generated: {generated}",
        f"Project: {project_name}",
        f"Data sources: {', '.join(found_types)}",
        f"Completeness: {completeness}/{len(_EXPECTED_TYPES)} data types available",
        "",
    ]

    if warnings:
        lines.append("**Warnings:**")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    # Variants
    for variant in [variant_a, variant_b, variant_c]:
        lines.append(f"## {variant['label']}")
        lines.append(f"**Title:** {variant['title']} ({variant['char_count']} chars)")
        lines.append(f"**Test Hypothesis:** {variant['hypothesis']}")
        mod = variant['moderation']
        mod_detail = '; '.join(mod['notes']) if mod['notes'] else 'No triggers detected'
        lines.append(f"**Moderation:** {mod['level']} — {mod_detail}")
        lines.append("")

        # Thumbnail blueprint
        thumb = variant['thumbnail']
        lines.append("### Thumbnail Blueprint")
        lines.append(f"- **Concept:** {thumb['concept']}")
        lines.append(f"- **Composition:** {thumb['composition']}")
        lines.append(f"- **Color Palette:** {', '.join(thumb['color_palette'])}")
        lines.append("- **Text Overlay:**")
        to = thumb['text_overlay']
        lines.append(f"  - Text: \"{to['text']}\"")
        lines.append(f"  - Position: {to['position']}")
        lines.append(f"  - Font style: {to['font_style']}")
        lines.append(f"  - Size: {to['size']}")
        lines.append(f"  - Contrast: {to['contrast']}")
        lines.append(f"- **Mobile Legibility:** {thumb['mobile_legibility']}")
        lines.append("- **Asset Types Needed:**")
        for asset in thumb['asset_types']:
            lines.append(f"  - {asset}")
        lines.append("- **AI-Generatable Elements:**")
        for elem in thumb['ai_elements']:
            tool = elem.get('tool', 'Unknown')
            if 'prompt' in elem:
                lines.append(f"  - {elem['element']}: [{tool}] — \"{elem['prompt']}\"")
            else:
                lines.append(f"  - {elem['element']}: [{tool}] — \"{elem.get('description', '')}\"")
        if thumb.get('sensitivity_note'):
            lines.append(f"- **AI Sensitivity Note:** {thumb['sensitivity_note']}")
        lines.append(f"- **Moderation Risk:** {thumb['moderation_risk']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Description
    lines.append("## Recommended Description")
    lines.append(description)
    desc_detail = '; '.join(desc_moderation['notes']) if desc_moderation['notes'] else 'No triggers detected'
    lines.append(f"**Moderation:** {desc_moderation['level']} — {desc_detail}")
    lines.append("")

    # Tags
    lines.append("## Tag Set")
    lines.append(tags_str)
    tags_detail = '; '.join(tags_moderation['notes']) if tags_moderation['notes'] else 'No triggers detected'
    lines.append(f"**Tag count:** {tags_count} | **Total chars:** {sum(len(t) + 2 for t in tags_str.split(', '))}/500")
    lines.append(f"**Moderation:** {tags_moderation['level']} — {tags_detail}")
    lines.append("")

    # Conflicts
    lines.append("## Conflicts & Notes")
    for c in conflicts:
        lines.append(f"- {c}")
    lines.append("")

    # Data quality
    lines.append("## Data Quality")
    lines.append(f"- Average parseable ratio: {avg_ratio:.2f}")
    lines.append(f"- Data types present: {completeness}/{len(_EXPECTED_TYPES)}")
    if warnings:
        lines.append("- Missing data types (may affect output quality):")
        for w in warnings:
            lines.append(f"  - {w}")
    if avg_ratio < 0.5:
        lines.append("- **Low parseable ratio** — consider re-running /publish --intake with cleaner tool output")
    lines.append("")

    return '\n'.join(lines)
