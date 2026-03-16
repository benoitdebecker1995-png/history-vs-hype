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
from tools.production.synthesis_engine import MODERATION_TRIGGERS, SAFE_ALTERNATIVES, score_moderation

logger = get_logger(__name__)

# VidIQ Pro Coach has a practical character limit for script context.
# If VidIQ truncates your prompt, reduce this value.
VIDIQ_CHAR_LIMIT = 2000

# Section headings to skip when falling back to script-based topic extraction
_STRUCTURAL_HEADINGS = {
    'cold open', 'act 1', 'act 2', 'act 3', 'act 4', 'intro', 'introduction',
    'conclusion', 'outro', 'opening', 'closing', 'hook',
}


def generate_prompts(project_path: str, script_path: str) -> dict:
    """Generate EXTERNAL-PROMPTS.md with VidIQ + Gemini prompts.

    Checks project metadata files (YOUTUBE-METADATA.md, PROJECT-STATUS.md,
    01-VERIFIED-RESEARCH.md) first for curated context. Falls back to
    script entity extraction when metadata files are unavailable.

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

        # --- Project context from metadata files (preferred) ---
        project_files = _discover_project_files(project)
        project_ctx = _load_project_context(project_files)
        has_project_ctx = project_ctx.get('topic') is not None
        logger.info("Project metadata context: %s", 'available' if has_project_ctx else 'falling back to script')

        # --- Build script context (auto-adapted to char limit) ---
        script_context = _build_script_context(sections, entities, project_ctx)
        logger.info("Script context: %d chars (limit %d)", len(script_context), VIDIQ_CHAR_LIMIT)

        # --- Competitor context (graceful degradation) ---
        competitor = _get_competitor_context()
        logger.info("Competitor context available: %s", competitor['available'])

        # --- Moderation scoring on full script text ---
        script_text = script.read_text(encoding='utf-8')
        moderation = score_moderation(script_text)
        logger.info("Script moderation: %s", moderation['level'])

        # --- Build prompts ---
        topic_summary = _extract_topic_summary(sections, entities, project_ctx)
        outlier_titles = competitor.get('outlier_titles', [])
        outlier_block = _format_outlier_titles(outlier_titles)

        vidiq_prompts = _build_vidiq_prompts(
            topic_summary, script_context, outlier_block, moderation=moderation
        )
        gemini_prompt = _build_gemini_prompt(topic_summary, entities, project_ctx, moderation=moderation)

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


def _discover_project_files(project: Path) -> dict:
    """Check which metadata files exist in the project folder."""
    candidates = {
        'metadata': project / 'YOUTUBE-METADATA.md',
        'status': project / 'PROJECT-STATUS.md',
        'research': project / '01-VERIFIED-RESEARCH.md',
    }
    return {k: v if v.exists() else None for k, v in candidates.items()}


def _load_project_context(project_files: dict) -> dict:
    """Read project metadata files and extract curated context.

    Returns a dict with keys: topic, core_question, myth, modern_hook,
    people, places, documents, hook_text, titles. All values may be None.
    """
    ctx = {
        'topic': None, 'core_question': None, 'myth': None,
        'modern_hook': None, 'people': [], 'places': [], 'documents': [],
        'hook_text': None, 'titles': [],
    }

    # --- YOUTUBE-METADATA.md (priority 1: project name + strategy + titles) ---
    if project_files.get('metadata'):
        try:
            text = project_files['metadata'].read_text(encoding='utf-8')
            lines = text.splitlines()

            # Project name from H1
            for line in lines[:5]:
                if line.startswith('# '):
                    raw = line[2:].strip()
                    # Strip "YOUTUBE METADATA: " prefix if present
                    if raw.upper().startswith('YOUTUBE METADATA:'):
                        raw = raw.split(':', 1)[1].strip()
                    ctx['topic'] = raw
                    break

            # Strategy line
            for line in lines[:15]:
                if line.lower().startswith('**strategy:**'):
                    ctx['modern_hook'] = line.split(':', 1)[1].strip().rstrip('*')
                    break

            # Title options (first 2 code-fenced titles)
            in_title_section = False
            for line in lines:
                if '## TITLE' in line.upper():
                    in_title_section = True
                    continue
                if in_title_section and line.startswith('## '):
                    break
                if in_title_section and line.startswith('```') and len(ctx['titles']) < 2:
                    # Next non-empty line after ``` is the title
                    continue
                if in_title_section and line.strip() and not line.startswith('```') and not line.startswith('#') and not line.startswith('-') and not line.startswith('*') and not line.startswith('>'):
                    candidate = line.strip()
                    # Filter out metadata lines and comments
                    if '(' in candidate and candidate.endswith(')') and 'chars' in candidate.lower():
                        # This is a title with char count like "Title Text (61 chars)"
                        candidate = re.sub(r'\s*\(\d+\s*chars?\)\s*$', '', candidate).strip()
                    if candidate and len(ctx['titles']) < 2 and len(candidate) > 15 and len(candidate) < 100:
                        ctx['titles'].append(candidate)
        except Exception as e:
            logger.debug("Failed to parse YOUTUBE-METADATA.md: %s", e)

    # --- PROJECT-STATUS.md (priority 2: concept + core question) ---
    if project_files.get('status'):
        try:
            text = project_files['status'].read_text(encoding='utf-8')
            lines = text.splitlines()

            in_concept = False
            concept_lines = []
            for line in lines:
                if line.strip().lower().startswith('## concept'):
                    in_concept = True
                    continue
                if in_concept and line.startswith('## '):
                    break
                if in_concept:
                    # Extract core question
                    if '**core question:**' in line.lower():
                        raw = line.split('**core question:**', 1)[-1] if '**core question:**' in line.lower() else line.split(':', 1)[1]
                        # Split on "Core question:" case-insensitively
                        for marker in ('**Core question:**', '**core question:**', '**Core Question:**'):
                            if marker in line:
                                raw = line.split(marker, 1)[1]
                                break
                        ctx['core_question'] = raw.strip().strip('"*').strip()
                    elif line.strip() and not line.startswith('**') and not concept_lines:
                        concept_lines.append(line.strip())

            # Use concept paragraph as topic fallback
            if concept_lines and not ctx['topic']:
                ctx['topic'] = concept_lines[0][:200]
        except Exception as e:
            logger.debug("Failed to parse PROJECT-STATUS.md: %s", e)

    # --- 01-VERIFIED-RESEARCH.md (priority 3: myth + hook + entities) ---
    if project_files.get('research'):
        try:
            text = project_files['research'].read_text(encoding='utf-8')
            lines = text.splitlines()

            in_hook_analysis = False
            in_hook_text = False
            hook_lines = []
            for line in lines:
                if '## MODERN HOOK ANALYSIS' in line.upper():
                    in_hook_analysis = True
                    continue
                if in_hook_analysis and line.startswith('## ') and 'MODERN HOOK' not in line.upper():
                    break
                if not in_hook_analysis:
                    continue

                # Myth
                if '**the myth:**' in line.lower():
                    for marker in ('**The myth:**', '**the myth:**', '**THE MYTH:**'):
                        if marker in line:
                            raw = line.split(marker, 1)[1]
                            break
                    else:
                        raw = line.split(':', 1)[1]
                    ctx['myth'] = raw.strip().strip('"*').strip()

                # Modern consequence (always prefer this over strategy line)
                if line.lower().startswith('**modern consequence:**'):
                    ctx['modern_hook'] = line.split(':', 1)[1].strip().strip('*').strip()

                # Script opening hook
                if 'script opening hook' in line.lower():
                    in_hook_text = True
                    continue
                if in_hook_text:
                    stripped = line.strip().lstrip('> ').strip('"')
                    if stripped:
                        hook_lines.append(stripped)
                    elif hook_lines:
                        in_hook_text = False

            if hook_lines:
                ctx['hook_text'] = ' '.join(hook_lines)

            # Extract people, places, documents from VERIFIED CLAIMS section
            _extract_entities_from_research(text, ctx)
        except Exception as e:
            logger.debug("Failed to parse 01-VERIFIED-RESEARCH.md: %s", e)

    return ctx


def _extract_entities_from_research(text: str, ctx: dict):
    """Extract entity names from verified research text.

    Looks for repeated proper nouns in claim headings and source citations.
    """
    # People: names in "Claim:" lines and source attributions
    people = set()
    places = set()
    documents = set()

    for line in text.splitlines():
        # Source lines like: "1. Marrus & Paxton (Tier 1) — *Vichy France and the Jews*"
        m = re.match(r'\d+\.\s+(.+?)\s*\(Tier\s*\d\)', line)
        if m:
            author = m.group(1).strip()
            # Clean "Marrus & Paxton" → individual names
            for name in re.split(r'\s*[&,]\s*', author):
                name = name.strip()
                if name and len(name) > 2:
                    people.add(name)

        # Document titles in single-italics from source lines: *Title Here*
        # Exclude bold markers (**text**) by requiring non-* before/after
        if re.match(r'^\s*(?:\d+\.|[-•])\s', line):
            for doc_match in re.finditer(r'(?<!\*)\*([A-Z][^*]{5,60})\*(?!\*)', line):
                doc = doc_match.group(1).strip()
                if doc and not doc.startswith('Tier') and ':' not in doc[:15]:
                    documents.add(doc)

    # Claim headings: "### Claim: The Statut des Juifs was a French initiative"
    for m in re.finditer(r'###\s*Claim:\s*(.+)', text):
        claim_text = m.group(1)
        # Extract capitalized multi-word names as potential entities
        for name_m in re.finditer(r'[A-Z][a-zéèêëàâùûîïôç]+(?:\s+(?:des?|du|la|le|von|van|al-|el-)\s+)?[A-Z][a-zéèêëàâùûîïôç]+(?:\s+[A-Z][a-zéèêëàâùûîïôç]+)?', claim_text):
            candidate = name_m.group(0).strip()
            if len(candidate) > 3:
                # Heuristic: if it looks like a document/law name, add to documents
                if any(kw in candidate.lower() for kw in ('statut', 'law', 'treaty', 'act', 'decree', 'loi', 'accord')):
                    documents.add(candidate)

    # NOTEBOOKLM SOURCES section for places
    sources_section = re.search(r'## NOTEBOOKLM SOURCES.*?(?=\n## |\Z)', text, re.DOTALL)
    if sources_section:
        src_text = sources_section.group(0)
        # Look for place names in source titles
        for place_m in re.finditer(r'(?:France|Algeria|Germany|Italy|Spain|Argentina|Chile|Paraguay|Uruguay|Brazil|Congo|Belgium|Britain|England|Scotland|Ireland|Israel|Palestine|Egypt|Syria|Iraq|Jordan|Lebanon|Turkey|Russia|Soviet|China|Japan|India|Mexico|Cuba|Vietnam|Korea|Antarctica|Gibraltar|Belize|Guatemala|Bermeja|Panama)', src_text):
            places.add(place_m.group(0))

    # Also check the MODERN HOOK section for places
    hook_section = re.search(r'## MODERN HOOK ANALYSIS.*?(?=\n## |\Z)', text, re.DOTALL)
    if hook_section:
        hook_text = hook_section.group(0)
        for place_m in re.finditer(r'(?:France|Vichy France|Algeria|French colonial empire|Germany|Italy|Spain|Argentina|Chile|Paraguay|Uruguay|Brazil|Congo|Belgium|Britain|Gibraltar|Belize|Guatemala|Bermeja|Panama)', hook_text):
            places.add(place_m.group(0))

    # Deduplicate documents: drop shorter titles that are substrings of longer ones
    deduped_docs = set()
    sorted_docs = sorted(documents, key=len, reverse=True)
    for doc in sorted_docs:
        if not any(doc != existing and doc in existing for existing in deduped_docs):
            deduped_docs.add(doc)

    # Merge into context (don't overwrite if already populated)
    if people and not ctx['people']:
        ctx['people'] = sorted(people)[:5]
    if places and not ctx['places']:
        ctx['places'] = sorted(places)[:5]
    if deduped_docs and not ctx['documents']:
        ctx['documents'] = sorted(deduped_docs)[:5]


def _build_script_context(sections, entities, project_ctx: dict = None) -> str:
    """Auto-adapt script context to fit within VIDIQ_CHAR_LIMIT.

    Prefers project metadata context. Falls back to hook/intro text or
    topic summary with key entities.
    """
    if project_ctx is None:
        project_ctx = {}

    # Best: use project metadata context
    if project_ctx.get('topic'):
        summary = _extract_topic_summary(sections, entities, project_ctx)
        if len(summary) <= VIDIQ_CHAR_LIMIT:
            return summary

    # Try full hook/intro
    intro_parts = [s.content for s in sections[:2]]
    full_intro = "\n\n".join(intro_parts)

    if len(full_intro) <= VIDIQ_CHAR_LIMIT:
        return full_intro

    # Fall back to topic summary with key entities
    return _extract_topic_summary(sections, entities, project_ctx)


def _extract_topic_summary(sections, entities, project_ctx: dict = None) -> str:
    """Generate a concise topic summary with key entities.

    Prefers curated context from project metadata files. Falls back to
    script-based extraction (section headings + EntityExtractor output).
    """
    if project_ctx is None:
        project_ctx = {}

    # --- Entity sourcing: prefer project context, fall back to EntityExtractor ---
    if project_ctx.get('places'):
        places = project_ctx['places'][:3]
    else:
        places = [e.text for e in entities if e.entity_type == 'place'][:3]

    if project_ctx.get('people'):
        people = project_ctx['people'][:3]
    else:
        people = [e.text for e in entities if e.entity_type == 'person'][:3]

    if project_ctx.get('documents'):
        documents = project_ctx['documents'][:3]
    else:
        documents = [e.text for e in entities if e.entity_type == 'document'][:3]

    # --- Topic line: prefer project context ---
    if project_ctx.get('topic'):
        topic = project_ctx['topic']
    elif sections:
        # Skip structural headings (COLD OPEN, ACT 1, etc.)
        topic = "Unknown topic"
        for s in sections:
            heading_lower = re.sub(r'\s*\([\d:–-]+\)\s*$', '', s.heading).strip().lower()
            if heading_lower not in _STRUCTURAL_HEADINGS:
                topic = s.heading
                break
    else:
        topic = "Unknown topic"

    parts = [f"Topic: {topic}"]

    # Core question from PROJECT-STATUS.md
    if project_ctx.get('core_question'):
        parts.append(f"Core question: {project_ctx['core_question']}")

    # Myth + modern hook from VERIFIED-RESEARCH.md
    if project_ctx.get('myth'):
        parts.append(f"Myth being debunked: {project_ctx['myth']}")
    if project_ctx.get('modern_hook'):
        parts.append(f"Modern relevance: {project_ctx['modern_hook']}")

    # Fallback: script core claim (only if no project context available)
    if not project_ctx.get('core_question') and not project_ctx.get('myth'):
        if sections:
            core_claim = sections[0].content[:200].strip()
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


def _build_vidiq_prompts(topic_summary, script_context, outlier_block, moderation=None) -> list:
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
    if moderation is not None and moderation.get('level') in ('HIGH', 'MEDIUM'):
        trigger_terms = [t['term'] for t in moderation.get('triggers', [])]
        safe_alts = {t: SAFE_ALTERNATIVES[t] for t in trigger_terms if t in SAFE_ALTERNATIVES}
        safe_alts_str = (
            ', '.join(f"'{k}' → '{v}'" for k, v in safe_alts.items())
            if safe_alts else 'see YouTube advertiser guidelines'
        )
        title_parts.append(
            f"\nIMPORTANT: This topic contains sensitive content "
            f"({moderation['level']} risk: {', '.join(trigger_terms)}).\n"
            f"YouTube may restrict monetization for titles containing these terms.\n"
            f"Suggest titles that convey the topic accurately without using trigger words.\n"
            f"Safe alternatives: {safe_alts_str}.\n"
        )
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


def _build_gemini_prompt(topic_summary, entities, project_ctx: dict = None, moderation=None) -> dict:
    """Build one comprehensive Gemini creative brief."""
    if project_ctx is None:
        project_ctx = {}

    # Prefer project context entities, fall back to EntityExtractor
    if project_ctx.get('places'):
        places = project_ctx['places'][:3]
    else:
        places = [e.text for e in entities if e.entity_type == 'place'][:3]

    if project_ctx.get('people'):
        people = project_ctx['people'][:3]
    else:
        people = [e.text for e in entities if e.entity_type == 'person'][:3]

    if project_ctx.get('documents'):
        documents = project_ctx['documents'][:3]
    else:
        documents = [e.text for e in entities if e.entity_type == 'document'][:3]

    entity_block = []
    if places:
        entity_block.append(f"Places: {', '.join(places)}")
    if people:
        entity_block.append(f"People: {', '.join(people)}")
    if documents:
        entity_block.append(f"Documents: {', '.join(documents)}")

    entities_str = "\n".join(entity_block) if entity_block else "No specific entities extracted."

    # Build debunking angle block from project context
    angle_block = ""
    if project_ctx.get('myth') or project_ctx.get('hook_text'):
        angle_parts = []
        if project_ctx.get('myth'):
            angle_parts.append(f"Myth being debunked: {project_ctx['myth']}")
        if project_ctx.get('core_question'):
            angle_parts.append(f"Core question: {project_ctx['core_question']}")
        if project_ctx.get('hook_text'):
            angle_parts.append(f"Draft hook: \"{project_ctx['hook_text'][:300]}\"")
        angle_block = "\n\nDebunking angle:\n" + "\n".join(angle_parts) + "\n"

    text = (
        f"I'm creating a YouTube video for a small educational history channel "
        f"(under 500 subscribers, educated international audience aged 25-44). "
        f"The video uses primary sources and academic research — it's evidence-based "
        f"myth-busting, not political commentary.\n\n"
        f"Topic summary:\n{topic_summary[:500]}\n\n"
        f"Key entities:\n{entities_str}\n"
        f"{angle_block}\n"
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

    if moderation is not None and moderation.get('level') in ('HIGH', 'MEDIUM'):
        trigger_terms = [t['term'] for t in moderation.get('triggers', [])]
        safe_alts = {t: SAFE_ALTERNATIVES[t] for t in trigger_terms if t in SAFE_ALTERNATIVES}
        safe_alts_str = (
            '\n'.join(f"   - '{k}' → '{v}'" for k, v in safe_alts.items())
            if safe_alts else '   - See YouTube advertiser guidelines'
        )
        text += (
            f"\n\n5. **Monetization-safe framing:** This topic involves sensitive content "
            f"({moderation['level']} risk: {', '.join(trigger_terms)}).\n"
            f"YouTube may limit monetization for metadata containing these terms.\n"
            f"How can titles, descriptions, and thumbnail text convey the gravity of this "
            f"topic while remaining advertiser-friendly?\n"
            f"Suggest specific alternative phrasings for:\n{safe_alts_str}"
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
