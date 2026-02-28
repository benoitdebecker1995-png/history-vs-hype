"""
Prompt Generator Module

Generates tailored VidIQ Pro Coach + Gemini prompts from script analysis.
Produces EXTERNAL-PROMPTS.md with numbered, copy-paste-ready prompts that
auto-adapt to script length via the VIDIQ_CHAR_LIMIT constant.

If VidIQ truncates your prompt, reduce VIDIQ_CHAR_LIMIT below.

Usage:
    from tools.production.prompt_generator import generate_prompts

    result = generate_prompts(
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

# VidIQ Pro Coach has a practical character limit for script context.
# If VidIQ truncates your prompt, reduce this value.
VIDIQ_CHAR_LIMIT = 2000


def generate_prompts(project_path: str, script_path: str) -> dict:
    """Generate EXTERNAL-PROMPTS.md with VidIQ + Gemini prompts.

    Parses the script for sections and entities, builds auto-adapted
    script context, and writes sequenced prompts to the project folder.

    Args:
        project_path: Path to the video project folder.
        script_path: Path to the script markdown file.

    Returns:
        {'output_path': str} on success, {'error': str} on failure.
    """
    try:
        project = Path(project_path)
        script = Path(script_path)

        if not script.exists():
            return {'error': f'prompt_generator.generate_prompts: script not found — {script}'}

        if not project.exists():
            return {'error': f'prompt_generator.generate_prompts: project folder not found — {project}'}

        # --- Script analysis (reuse existing tools) ---
        logger.info("Parsing script: %s", script.name)
        sections, entities, total_words = _analyze_script(script)

        if not sections:
            return {'error': 'prompt_generator.generate_prompts: script produced no sections'}

        project_name = project.name
        hook_text = sections[0].content[:500] if sections else ""

        # --- Build script context (auto-adapted to char limit) ---
        script_context = _build_script_context(sections, entities)
        logger.info("Script context: %d chars (limit %d)", len(script_context), VIDIQ_CHAR_LIMIT)

        # --- Competitor context (graceful degradation) ---
        competitor = _get_competitor_context()
        logger.info("Competitor context available: %s", competitor['available'])

        # --- Build prompts ---
        topic_summary = _extract_topic_summary(sections, entities)
        outlier_titles = competitor.get('outlier_titles', [])
        outlier_block = _format_outlier_titles(outlier_titles)

        vidiq_prompts = _build_vidiq_prompts(
            topic_summary, script_context, outlier_block
        )
        gemini_prompt = _build_gemini_prompt(topic_summary, entities)

        # --- Write EXTERNAL-PROMPTS.md ---
        output_path = project / "EXTERNAL-PROMPTS.md"
        content = _render_output(
            project_name=project_name,
            total_words=total_words,
            section_count=len(sections),
            vidiq_prompts=vidiq_prompts,
            gemini_prompt=gemini_prompt,
            competitor_available=competitor['available'],
            competitor_note=competitor.get('note', ''),
        )

        # Check line count (Pitfall 5: keep under 200 lines)
        line_count = content.count('\n') + 1
        if line_count > 200:
            logger.warning("EXTERNAL-PROMPTS.md is %d lines (target: <200)", line_count)

        output_path.write_text(content, encoding='utf-8')
        logger.info("Wrote %s (%d lines)", output_path.name, line_count)

        return {'output_path': str(output_path)}

    except Exception as e:
        return {'error': f'prompt_generator.generate_prompts: unexpected error — {e}'}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _analyze_script(script_path: Path):
    """Parse script and extract entities. Returns (sections, entities, total_words)."""
    from tools.production.parser import ScriptParser
    from tools.production.entities import EntityExtractor

    parser = ScriptParser()
    sections = parser.parse_file(script_path)

    extractor = EntityExtractor()
    entities = extractor.extract_from_sections(sections)

    total_words = sum(s.word_count for s in sections)
    return sections, entities, total_words


def _build_script_context(sections, entities) -> str:
    """Auto-adapt script context to fit within VIDIQ_CHAR_LIMIT.

    If the hook/intro text (first 2 sections) fits, include full text.
    Otherwise, generate a topic summary with key entities.
    """
    # Try full hook/intro
    intro_parts = [s.content for s in sections[:2]]
    full_intro = "\n\n".join(intro_parts)

    if len(full_intro) <= VIDIQ_CHAR_LIMIT:
        return full_intro

    # Fall back to topic summary with key entities
    return _extract_topic_summary(sections, entities)


def _extract_topic_summary(sections, entities) -> str:
    """Generate a concise topic summary with key entities."""
    places = [e.text for e in entities if e.entity_type == 'place'][:3]
    people = [e.text for e in entities if e.entity_type == 'person'][:3]
    documents = [e.text for e in entities if e.entity_type == 'document'][:3]

    # Use first section heading + first 200 chars of content for topic
    if sections:
        heading = sections[0].heading
        core_claim = sections[0].content[:200].strip()
    else:
        heading = "Unknown topic"
        core_claim = ""

    parts = [f"Topic: {heading}"]
    if core_claim:
        parts.append(f"Core claim: {core_claim}")
    if places:
        parts.append(f"Key places: {', '.join(places)}")
    if people:
        parts.append(f"Key people: {', '.join(people)}")
    if documents:
        parts.append(f"Key documents: {', '.join(documents)}")

    summary = "\n".join(parts)

    # Truncate if still too long
    if len(summary) > VIDIQ_CHAR_LIMIT:
        summary = summary[:VIDIQ_CHAR_LIMIT - 3] + "..."

    return summary


def _get_competitor_context() -> dict:
    """Get competitor patterns for prompt grounding. Degrades gracefully."""
    default_db = Path(__file__).parent.parent / "intel" / "intel.db"

    if not default_db.exists():
        logger.debug("intel.db not found at %s — skipping competitor context", default_db)
        return {
            'available': False,
            'note': 'Run /intel --refresh for competitor context',
        }

    try:
        from tools.intel.kb_store import KBStore

        store = KBStore(str(default_db))
        outliers = store.get_competitor_videos(outliers_only=True, limit=10)
        niche = store.get_latest_niche_snapshot()

        # Handle error dicts from KBStore
        if isinstance(outliers, dict) and 'error' in outliers:
            logger.debug("KBStore outliers error: %s", outliers['error'])
            outliers = []

        if isinstance(niche, dict) and 'error' in niche:
            niche = None

        outlier_titles = [v.get('title', '') for v in (outliers if isinstance(outliers, list) else []) if v.get('title')]

        return {
            'available': True,
            'outlier_titles': outlier_titles[:5],  # Cap at 5 (Pitfall 5)
            'niche_snapshot': niche,
        }

    except Exception as e:
        logger.debug("Failed to load competitor context: %s", e)
        return {
            'available': False,
            'note': f'Error loading intel.db: {e}',
        }


def _format_outlier_titles(titles) -> str:
    """Format outlier titles for inclusion in prompts."""
    if not titles:
        return ""
    lines = ["Competitor outlier titles in this niche (for context):"]
    for t in titles:
        lines.append(f"- {t}")
    return "\n".join(lines)


def _build_vidiq_prompts(topic_summary, script_context, outlier_block) -> list:
    """Build 4 sequenced VidIQ Pro Coach prompts."""
    prompts = []

    # Step 1: Keyword Research
    kw_parts = [
        f"I'm making a video about the following topic. My channel focuses on "
        f"evidence-based history myth-busting for an educated international audience "
        f"(25-44 males). What are the best keywords to target? Include search volume "
        f"and competition data.\n",
        f"Script context:\n{script_context}\n",
    ]
    if outlier_block:
        kw_parts.append(f"\n{outlier_block}\n")
    prompts.append({
        'step': 1,
        'title': 'Keyword Research',
        'instruction': 'Paste into VidIQ Pro Coach. Copy the full response.',
        'text': "\n".join(kw_parts).strip(),
    })

    # Step 2: Title Optimization
    title_parts = [
        f"Based on your keyword analysis, generate 5-8 title options for this video. "
        f"Requirements: 50-65 characters, documentary tone (not clickbait), factually "
        f"accurate. The channel is small (under 500 subscribers) — optimize for "
        f"discovery, not existing audience.\n",
    ]
    if outlier_block:
        title_parts.append(f"\nStyle references from successful videos in this niche:\n{outlier_block}\n")
    prompts.append({
        'step': 2,
        'title': 'Title Optimization',
        'instruction': 'Paste into VidIQ Pro Coach after Step 1. Copy the full response.',
        'text': "\n".join(title_parts).strip(),
    })

    # Step 3: Tag Strategy
    prompts.append({
        'step': 3,
        'title': 'Tag Strategy',
        'instruction': 'Paste into VidIQ Pro Coach. Copy the full response.',
        'text': (
            f"For a video about: {topic_summary[:300]}\n\n"
            f"Suggest 20-30 tags. Mix: primary keywords (high volume), secondary "
            f"(specific discovery), and long-tail (niche). Format: comma-separated, "
            f"ready to paste into YouTube."
        ),
    })

    # Step 4: Description Optimization
    prompts.append({
        'step': 4,
        'title': 'Description Optimization',
        'instruction': 'Paste into VidIQ Pro Coach. Copy the full response.',
        'text': (
            f"Write the first 3 lines of a YouTube description optimized for search. "
            f"The video is about: {topic_summary[:300]}\n\n"
            f"Include the primary keyword naturally. Tone: academic documentary, not "
            f"promotional. The channel has under 500 subscribers — focus on search "
            f"discoverability over brand recognition."
        ),
    })

    return prompts


def _build_gemini_prompt(topic_summary, entities) -> dict:
    """Build one comprehensive Gemini creative brief."""
    places = [e.text for e in entities if e.entity_type == 'place'][:3]
    people = [e.text for e in entities if e.entity_type == 'person'][:3]
    documents = [e.text for e in entities if e.entity_type == 'document'][:3]

    entity_block = []
    if places:
        entity_block.append(f"Places: {', '.join(places)}")
    if people:
        entity_block.append(f"People: {', '.join(people)}")
    if documents:
        entity_block.append(f"Documents: {', '.join(documents)}")

    entities_str = "\n".join(entity_block) if entity_block else "No specific entities extracted."

    text = (
        f"I'm creating a YouTube video for a small educational history channel "
        f"(under 500 subscribers, educated international audience aged 25-44). "
        f"The video uses primary sources and academic research — it's evidence-based "
        f"myth-busting, not political commentary.\n\n"
        f"Topic summary:\n{topic_summary[:500]}\n\n"
        f"Key entities:\n{entities_str}\n\n"
        f"Please address all of the following:\n\n"
        f"1. **Hook psychology:** What emotional or intellectual hook would make an "
        f"educated viewer click on this video? What's the knowledge gap?\n\n"
        f"2. **Thumbnail concepts:** Suggest 3 thumbnail concepts that would work for "
        f"this topic. For each, describe the visual composition, color palette, and "
        f"any text overlay. Consider mobile readability.\n\n"
        f"3. **Curiosity gap framing:** How should this topic be framed as a knowledge "
        f"gap the viewer didn't know they had? What makes them feel they NEED to watch?\n\n"
        f"4. **Audience emotional triggers:** What makes this topic shareable for a "
        f"25-44 male, internationally educated audience? What emotional response drives "
        f"sharing — surprise, indignation, intellectual satisfaction?"
    )

    return {
        'step': 5,
        'title': 'Creative Angles',
        'instruction': 'Paste into Google Gemini. Copy the full response.',
        'text': text,
    }


def _render_output(
    project_name,
    total_words,
    section_count,
    vidiq_prompts,
    gemini_prompt,
    competitor_available,
    competitor_note,
) -> str:
    """Render the final EXTERNAL-PROMPTS.md content."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    comp_status = "available" if competitor_available else f"not available ({competitor_note})"

    lines = [
        f"# External Intelligence Prompts",
        f"Generated: {now}",
        f"Project: {project_name}",
        f"Script: {total_words} words, {section_count} sections",
        "",
        "## VidIQ Pro Coach Prompts",
        "",
    ]

    for prompt in vidiq_prompts:
        lines.append(f"### Step {prompt['step']}: {prompt['title']}")
        lines.append(f"> {prompt['instruction']}")
        lines.append("")
        lines.append(prompt['text'])
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Gemini Creative Brief")
    lines.append("")
    lines.append(f"### Step {gemini_prompt['step']}: {gemini_prompt['title']}")
    lines.append(f"> {gemini_prompt['instruction']}")
    lines.append("")
    lines.append(gemini_prompt['text'])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Notes")
    lines.append(f"- VidIQ char limit: {VIDIQ_CHAR_LIMIT} (adjust in tools/production/prompt_generator.py if truncated)")
    lines.append(f"- Competitor context: {comp_status}")
    lines.append("")

    return "\n".join(lines)
