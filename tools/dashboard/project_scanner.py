"""
Project scanner for the History vs Hype multi-project dashboard.

Scans _IN_PRODUCTION/ and _READY_TO_FILM/, classifies projects by phase,
ranks by priority, detects staleness, and cross-references intel trends.

All stdlib — no external dependencies required.
"""

from pathlib import Path
import time
import re

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PHASE_PRIORITY = {
    'filming-ready': 1,
    'fact-checked': 2,
    'scripting': 3,
    'research': 4,
    'idea': 5,
}

NEXT_ACTION = {
    'filming-ready': 'Film it',
    'fact-checked': '/prep --edit-guide',
    'scripting': '/verify',
    'research': '/script',
    'idea': '/research --new',
}

STALE_THRESHOLD_DAYS = 14

# ---------------------------------------------------------------------------
# Phase detection
# ---------------------------------------------------------------------------


def detect_phase(files: set) -> str:
    """Detect project phase from the set of file names present in a folder.

    Priority order (highest to lowest):
      filming-ready > fact-checked > scripting > research > idea

    Args:
        files: set of file name strings (top-level files only, no paths)

    Returns:
        Phase string: one of 'filming-ready', 'fact-checked', 'scripting',
        'research', 'idea'
    """
    # Filming-ready: FINAL-SCRIPT.md or any TELEPROMPTER file
    if 'FINAL-SCRIPT.md' in files:
        return 'filming-ready'
    if any('TELEPROMPTER' in f.upper() for f in files):
        return 'filming-ready'

    # Fact-checked: verification file + script present
    has_verification = '03-FACT-CHECK-VERIFICATION.md' in files
    has_script = '02-SCRIPT-DRAFT.md' in files or 'SCRIPT.md' in files
    if has_verification and has_script:
        return 'fact-checked'

    # Scripting: script draft present (even without verification)
    if has_script:
        return 'scripting'

    # Research: verified research file present
    if '01-VERIFIED-RESEARCH.md' in files:
        return 'research'

    # Default: idea phase (folder only or unrecognised files)
    return 'idea'


# ---------------------------------------------------------------------------
# Days since activity
# ---------------------------------------------------------------------------


def days_since_activity(folder: Path) -> int:
    """Calculate days since the most recent top-level file modification.

    Only top-level files are examined (not subdirectories), preventing
    subdirectory activity from inflating the count (Pitfall 3).

    Uses time.time() - st_mtime to avoid timezone-aware/naive mixing
    (Pitfall 1): both values are UTC epoch seconds on all platforms.

    Args:
        folder: Path to the project folder

    Returns:
        Integer days since most recent modification. Returns 999 sentinel
        if no files found or any OSError occurs.
    """
    latest_mtime = 0.0
    try:
        for item in folder.iterdir():
            if not item.is_file():
                continue
            try:
                mtime = item.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime
            except OSError:
                continue
    except OSError:
        return 999

    if latest_mtime == 0.0:
        return 999

    delta = time.time() - latest_mtime
    return int(delta / 86400)


# ---------------------------------------------------------------------------
# Topic extraction
# ---------------------------------------------------------------------------


def extract_topic_slug(folder_name: str) -> str:
    """Extract topic words from a folder name slug.

    Strips the leading numeric prefix (e.g. '35-') and trailing year
    (e.g. '-2026'), then replaces hyphens with spaces.

    Args:
        folder_name: raw folder name like '35-gibraltar-treaty-utrecht-2026'

    Returns:
        Lowercased topic words string, e.g. 'gibraltar treaty utrecht'
    """
    slug = re.sub(r'^\d+-', '', folder_name)
    slug = re.sub(r'-\d{4}$', '', slug)
    slug = slug.replace('-', ' ')
    return slug.lower()


# ---------------------------------------------------------------------------
# Intel topic extraction
# ---------------------------------------------------------------------------


def extract_intel_topics(intel_path: Path) -> list:
    """Read youtube-intelligence.md and return trending topic words.

    Scans for the '### Trending Topics' header, then parses the Markdown
    table rows that follow, stopping at the next '#' heading. Returns an
    empty list if the file is missing or any error occurs — never raises.

    Args:
        intel_path: Path to channel-data/youtube-intelligence.md

    Returns:
        List of topic strings (lowercase), e.g. ['war', 'roman', 'empire']
    """
    if not intel_path.exists():
        return []

    try:
        topics = []
        in_trending = False

        for line in intel_path.read_text(encoding='utf-8').splitlines():
            if 'Trending Topics' in line:
                in_trending = True
                continue

            if in_trending:
                if line.startswith('#'):
                    # Next heading — section ended
                    break
                if line.startswith('|'):
                    parts = [p.strip() for p in line.split('|')]
                    parts = [p for p in parts if p]
                    if parts and parts[0] not in ('Topic', '-----'):
                        topics.append(parts[0].lower())

        return topics
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Main scanner
# ---------------------------------------------------------------------------


def scan_projects(project_root: str = '.') -> dict:
    """Scan _IN_PRODUCTION/ and _READY_TO_FILM/ for all video projects.

    For each folder in _IN_PRODUCTION/:
      - Detects phase from top-level file names
      - Calculates days since most recent top-level file modification
      - Checks whether project has been published (POST-PUBLISH-ANALYSIS.md)
      - Extracts topic slug from folder name for intel cross-referencing
      - Flags stale projects (>14 days inactive)

    Sorted: published projects last, then by priority ascending (1=highest),
    then by days_since ascending (most recent activity first).

    Also reads _READY_TO_FILM/ folder names and intel trending topics.

    Args:
        project_root: root directory of the workspace (default: '.')

    Returns:
        dict with keys:
          'projects'     — list of project dicts
          'ready_to_film' — list of folder names from _READY_TO_FILM/
          'intel_topics'  — list of trending topic strings
    """
    root = Path(project_root)
    prod_dir = root / 'video-projects' / '_IN_PRODUCTION'
    ready_dir = root / 'video-projects' / '_READY_TO_FILM'
    intel_path = root / 'channel-data' / 'youtube-intelligence.md'

    projects = []

    if prod_dir.exists():
        for folder in sorted(prod_dir.iterdir()):
            # Skip non-directories and README files (Pitfall 2)
            if not folder.is_dir():
                continue
            if folder.name.startswith('README'):
                continue

            # Top-level file names only (no subdirectory contents)
            try:
                files = {f.name for f in folder.iterdir() if f.is_file()}
            except OSError:
                files = set()

            phase = detect_phase(files)
            days = days_since_activity(folder)
            published = 'POST-PUBLISH-ANALYSIS.md' in files
            topic_slug = extract_topic_slug(folder.name)

            projects.append({
                'name': folder.name,
                'phase': phase,
                'priority': PHASE_PRIORITY.get(phase, 99),
                'next_action': NEXT_ACTION.get(phase, '?'),
                'days_since': days,
                'stale': days > STALE_THRESHOLD_DAYS,
                'published': published,
                'topic_slug': topic_slug,
            })

    # Sort: published last, then priority ascending, then days_since ascending
    projects.sort(key=lambda p: (p['published'], p['priority'], p['days_since']))

    # Collect _READY_TO_FILM folder names
    ready_to_film = []
    if ready_dir.exists():
        for folder in sorted(ready_dir.iterdir()):
            if folder.is_dir() and not folder.name.startswith('README'):
                ready_to_film.append(folder.name)

    # Extract intel trending topics (gracefully skips if missing)
    intel_topics = extract_intel_topics(intel_path)

    return {
        'projects': projects,
        'ready_to_film': ready_to_film,
        'intel_topics': intel_topics,
    }


# ---------------------------------------------------------------------------
# Dashboard formatter
# ---------------------------------------------------------------------------


def format_dashboard(data: dict) -> str:
    """Format scan results as a scannable Markdown dashboard.

    Layout:
      1. Header
      2. Active projects table (not published), sorted by priority
         - Activity column shows days count with "STALE" if >14 days
      3. Intel cross-reference notes (trending topic matches)
      4. Published footer line
      5. _READY_TO_FILM footer (if any)
      6. Idea-phase summary line (if suppressed from table)

    Idea-phase projects are suppressed from the main table only when there
    are more than 10 active non-idea projects (to keep the table scannable).
    A summary line is shown at the bottom when there are more than 5 ideas.

    Args:
        data: dict returned by scan_projects()

    Returns:
        Complete Markdown string ready for display.
    """
    projects = data.get('projects', [])
    ready_to_film = data.get('ready_to_film', [])
    intel_topics = data.get('intel_topics', [])

    active = [p for p in projects if not p['published']]
    published = [p for p in projects if p['published']]

    # Decide whether to suppress idea-phase projects from the main table
    non_idea_active = [p for p in active if p['phase'] != 'idea']
    idea_projects = [p for p in active if p['phase'] == 'idea']
    suppress_ideas = len(non_idea_active) > 10

    if suppress_ideas:
        table_projects = non_idea_active
    else:
        table_projects = active

    # ---------------------------------------------------------------------------
    # Build table
    # ---------------------------------------------------------------------------
    lines = []
    lines.append('## Project Dashboard')
    lines.append('')

    if not table_projects:
        lines.append('_No active projects found in _IN_PRODUCTION/._')
    else:
        lines.append('| Project | Phase | Next Action | Activity |')
        lines.append('|---------|-------|-------------|----------|')
        for p in table_projects:
            activity = str(p['days_since']) if p['days_since'] < 999 else '?'
            if p['stale']:
                activity += ' STALE'
            lines.append(
                f"| {p['name']} | {p['phase']} | {p['next_action']} | {activity} |"
            )

    # ---------------------------------------------------------------------------
    # Intel cross-reference
    # ---------------------------------------------------------------------------
    if intel_topics:
        matches = {}  # topic -> list of project names
        for p in active:
            slug = p['topic_slug']
            for topic in intel_topics:
                if topic and topic in slug:
                    matches.setdefault(topic, []).append(p['name'])

        if matches:
            lines.append('')
            for topic, names in matches.items():
                lines.append(
                    f"Trending topic match: **{topic}** — {', '.join(names)}"
                )

    # ---------------------------------------------------------------------------
    # Published footer
    # ---------------------------------------------------------------------------
    if published:
        pub_names = ', '.join(p['name'] for p in published)
        lines.append('')
        lines.append(
            f"**{len(published)} published (not archived):** {pub_names}"
        )

    # ---------------------------------------------------------------------------
    # _READY_TO_FILM footer
    # ---------------------------------------------------------------------------
    if ready_to_film:
        lines.append(
            f"**_READY_TO_FILM:** {', '.join(ready_to_film)}"
        )

    # ---------------------------------------------------------------------------
    # Idea-phase summary line (when suppressed or when count > 5)
    # ---------------------------------------------------------------------------
    if suppress_ideas and idea_projects:
        lines.append('')
        lines.append(
            f"_{len(idea_projects)} idea-phase projects not shown_"
        )
    elif not suppress_ideas and len(idea_projects) > 5:
        lines.append('')
        lines.append(
            f"_{len(idea_projects)} idea-phase projects included above_"
        )

    return '\n'.join(lines)
