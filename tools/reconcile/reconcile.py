"""
Reconcile project state across video-projects/ and derived docs.

What this owns:
  - Folder moves between _IN_PRODUCTION/ <-> _READY_TO_FILM/ <-> _ARCHIVED/published/
  - AUTO:reconcile block at the top of each per-folder PROJECT-STATUS.md
  - Regeneration of video-projects/PROJECT_STATUS.md (root overview)
  - Regeneration of video-projects/PROJECT_REGISTRY.md
  - Refresh of .brain/index.md §3 Active Topics
  - Reversible diff log at .brain/_inbox/reconcile-YYYY-MM-DD-HHMM.diff
  - .pre-diff backups for every file edit (used by --undo)

What this does NOT touch:
  - In-folder PROJECT-STATUS.md narrative below <!-- /AUTO:reconcile -->
  - Memory snapshots (memory/[N]-state.md) in --auto-publish-only mode
  - YouTube API directly (uses analytics.db as truth source)

Modes:
  /reconcile                       full scan, interactive approval
  /reconcile <slug>                single project
  /reconcile --dry-run             show diff, do not apply
  /reconcile --migrate             first-run retro: extra unmatched-folder review
  /reconcile --auto-publish-only   Routine 6 mode: only archive YouTube-confirmed publishes;
                                   never touches memory snapshots
  /reconcile --undo                reverse the latest reconcile run
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.dashboard.project_scanner import detect_phase, extract_topic_slug
from tools.reconcile.match import (
    HIGH_CONFIDENCE,
    GRAY_FLOOR,
    MatchCandidate,
    load_videos,
    match_folder,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
VIDEO_PROJECTS = REPO_ROOT / 'video-projects'
IN_PRODUCTION = VIDEO_PROJECTS / '_IN_PRODUCTION'
READY_TO_FILM = VIDEO_PROJECTS / '_READY_TO_FILM'
ARCHIVED_PUBLISHED = VIDEO_PROJECTS / '_ARCHIVED' / 'published'
ANALYTICS_DB = REPO_ROOT / 'tools' / 'youtube_analytics' / 'analytics.db'
BRAIN_INBOX = REPO_ROOT / '.brain' / '_inbox'
BRAIN_INDEX = REPO_ROOT / '.brain' / 'index.md'
LAST_RECONCILE_TS = REPO_ROOT / '.brain' / 'last-reconcile-ts.txt'
MANUAL_MATCHES = REPO_ROOT / 'tools' / 'reconcile' / 'manual-matches.json'
ROOT_STATUS = VIDEO_PROJECTS / 'PROJECT_STATUS.md'
ROOT_REGISTRY = VIDEO_PROJECTS / 'PROJECT_REGISTRY.md'

AUTO_OPEN = '<!-- AUTO:reconcile — do not edit manually, regenerated each run -->'
AUTO_CLOSE = '<!-- /AUTO:reconcile -->'
DERIVED_OPEN = '<!-- AUTO:reconcile-dashboard — regenerated each run, do not edit -->'
DERIVED_CLOSE = '<!-- /AUTO:reconcile-dashboard -->'

# analytics.db freshness gate for --auto-publish-only mode (Routine 6).
# If metrics_fetched_at max is older than this, refuse to run.
MAX_DB_AGE_HOURS = 36


@dataclass
class FolderState:
    path: Path
    bucket: str               # '_IN_PRODUCTION' | '_READY_TO_FILM' | '_ARCHIVED/published'
    slug: str
    files: set
    phase: str
    video_id: str | None = None
    video_title: str | None = None
    published_at: str | None = None
    match_score: float = 0.0
    match_candidates: list = field(default_factory=list)
    blocked: bool = False     # manual-matches.json null entry: leave alone, no moves, no AUTO block writes


@dataclass
class ProposedChange:
    kind: str                 # 'move' | 'edit-auto-block'
    folder: Path
    target_bucket: str | None = None     # for 'move'
    video_id: str | None = None
    video_title: str | None = None
    published_at: str | None = None
    target_status: str = ''
    score: float = 0.0
    confidence: str = ''      # 'high' | 'gray' | 'none' | 'tier1'
    notes: str = ''


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------


def scan_buckets() -> list[FolderState]:
    """Return one FolderState per project folder across all 3 buckets."""
    states = []
    for bucket_path, bucket_name in (
        (IN_PRODUCTION, '_IN_PRODUCTION'),
        (READY_TO_FILM, '_READY_TO_FILM'),
        (ARCHIVED_PUBLISHED, '_ARCHIVED/published'),
    ):
        if not bucket_path.exists():
            continue
        for folder in sorted(bucket_path.iterdir()):
            if not folder.is_dir():
                continue
            if folder.name.startswith('README') or folder.name.startswith('_'):
                continue
            try:
                files = {f.name for f in folder.iterdir() if f.is_file()}
            except OSError:
                files = set()
            states.append(FolderState(
                path=folder,
                bucket=bucket_name,
                slug=extract_topic_slug(folder.name),
                files=files,
                phase=detect_phase(files),
            ))
    return states


def target_bucket(state: FolderState) -> str:
    """Determine which bucket a folder belongs in given its current state."""
    if state.phase == 'published' or state.video_id is not None:
        return '_ARCHIVED/published'
    if state.phase in ('filming-ready', 'filmed'):
        return '_READY_TO_FILM'
    return '_IN_PRODUCTION'


def target_status_label(state: FolderState) -> str:
    """Map phase to the Status label used in the AUTO:reconcile block."""
    return {
        'published': 'PUBLISHED',
        'filmed': 'FILMED',
        'filming-ready': 'SCRIPT_LOCKED',
        'fact-checked': 'FACT_CHECKED',
        'scripting': 'SCRIPTING',
        'research': 'RESEARCH',
        'idea': 'IDEA',
    }.get(state.phase, 'UNKNOWN')


# ---------------------------------------------------------------------------
# Matching pass
# ---------------------------------------------------------------------------


def load_manual_matches() -> dict:
    """Load hand-curated folder_name -> video_id overrides if present."""
    if not MANUAL_MATCHES.exists():
        return {}
    try:
        return json.loads(MANUAL_MATCHES.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return {}


def attach_matches(states: list[FolderState]) -> None:
    """Populate each state's video_id / video_title / score in-place."""
    videos = load_videos(ANALYTICS_DB)
    known_ids = {v['video_id'] for v in videos}
    manual = load_manual_matches()

    for s in states:
        # Manual override has highest priority.
        # - String value (Video ID): positive match.
        # - null/empty: explicit BLOCK — folder is unpublished or Tier 1 false-positive;
        #   skip all matching, leave folder in current bucket.
        if s.path.name in manual:
            vid = manual[s.path.name]
            if vid is None or vid == '':
                # Block: skip both Tier 1 and Tier 2; folder stays put — no moves, no AUTO block writes.
                s.blocked = True
                continue
            if vid in known_ids:
                v = next((x for x in videos if x['video_id'] == vid), None)
                if v:
                    s.video_id = vid
                    s.video_title = v['title']
                    s.published_at = v['published_at']
                    s.match_score = 1.0
                    continue

        # Existing AUTO block Video ID is trusted (post-Tier-1 caching)
        existing = read_auto_block(s.path / 'PROJECT-STATUS.md')
        if existing and existing.get('Video ID'):
            vid = existing['Video ID']
            if vid in known_ids:
                v = next((x for x in videos if x['video_id'] == vid), None)
                if v:
                    s.video_id = vid
                    s.video_title = v['title']
                    s.published_at = v['published_at']
                    s.match_score = 1.0
                    continue

        best, candidates = match_folder(s.path, s.slug, videos, known_ids, top_n=3)
        s.match_candidates = candidates
        if best:
            s.video_id = best.video_id
            s.video_title = best.title
            s.published_at = best.published_at
            s.match_score = best.score


# ---------------------------------------------------------------------------
# AUTO:reconcile block
# ---------------------------------------------------------------------------


def read_auto_block(path: Path) -> dict | None:
    """Parse the AUTO:reconcile block from a PROJECT-STATUS.md. Returns the
    key/value pairs or None if no block present."""
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return None
    if AUTO_OPEN not in text or AUTO_CLOSE not in text:
        return None
    start = text.index(AUTO_OPEN) + len(AUTO_OPEN)
    end = text.index(AUTO_CLOSE)
    block = text[start:end]
    result = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        key, _, value = line.partition(':')
        # Strip inline comments like "(only when published)"
        value = value.split('(', 1)[0].strip()
        result[key.strip()] = value
    return result


def render_auto_block(state: FolderState, today: str) -> str:
    """Render the AUTO:reconcile block as a string."""
    target = target_bucket(state)
    status = target_status_label(state)
    lines = [
        AUTO_OPEN,
        f'Status: {status}',
        f'Lifecycle: {target}',
    ]
    if state.video_id:
        lines.append(f'Video ID: {state.video_id}')
    if state.published_at:
        lines.append(f'Published: {state.published_at[:10]}')
    lines.append(f'Last reconciled: {today}')
    lines.append(AUTO_CLOSE)
    return '\n'.join(lines) + '\n'


def write_auto_block(path: Path, new_block: str) -> str:
    """Write or replace the AUTO block at the top of a PROJECT-STATUS.md.
    Preserves all narrative below <!-- /AUTO:reconcile -->. Returns the
    previous content (for backup)."""
    existing = ''
    if path.exists():
        try:
            existing = path.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            existing = ''

    if AUTO_OPEN in existing and AUTO_CLOSE in existing:
        # Replace existing block
        end = existing.index(AUTO_CLOSE) + len(AUTO_CLOSE)
        # Skip trailing newline after close marker if present
        if end < len(existing) and existing[end] == '\n':
            end += 1
        new_content = new_block + existing[end:]
    else:
        # Prepend block; preserve all existing content
        sep = '\n' if existing and not existing.startswith('\n') else ''
        new_content = new_block + sep + existing

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_content, encoding='utf-8')
    return existing


# ---------------------------------------------------------------------------
# Derived doc regeneration
# ---------------------------------------------------------------------------


def _classify_state(s: FolderState) -> str:
    """Coarse classification used in dashboard tables."""
    if s.bucket == '_ARCHIVED/published':
        return 'published'
    if s.video_id is not None:
        return 'published'
    if s.phase == 'published':
        return 'published'
    if s.phase == 'filmed':
        return 'filmed'
    if s.phase == 'filming-ready':
        return 'ready_to_film'
    if s.phase == 'fact-checked':
        return 'fact_checked'
    if s.phase == 'scripting':
        return 'scripting'
    if s.phase == 'research':
        return 'research'
    return 'idea'


def render_root_status_block(states: list[FolderState], today: str) -> str:
    """Render the AUTO:reconcile-dashboard block for video-projects/PROJECT_STATUS.md.

    Includes:
      - lifecycle bucket counts
      - per-bucket folder list (compact)
      - recently-published table (from analytics.db, last 60 days)
    """
    by_bucket = {'_IN_PRODUCTION': [], '_READY_TO_FILM': [], '_ARCHIVED/published': []}
    for s in states:
        by_bucket.setdefault(s.bucket, []).append(s)

    lines = [DERIVED_OPEN, f'Last reconciled: {today}', '']
    lines.append('## Lifecycle counts')
    lines.append('')
    lines.append('| Bucket | Count |')
    lines.append('|---|---|')
    lines.append(f'| `_IN_PRODUCTION/` (pre-script / scripting / fact-check) | {len(by_bucket["_IN_PRODUCTION"])} |')
    lines.append(f'| `_READY_TO_FILM/` (script-locked / filmed / in-post, pre-publish) | {len(by_bucket["_READY_TO_FILM"])} |')
    lines.append(f'| `_ARCHIVED/published/` (YouTube confirmed) | {len(by_bucket["_ARCHIVED/published"])} |')
    lines.append('')

    # In production
    lines.append('## In production')
    lines.append('')
    if by_bucket['_IN_PRODUCTION']:
        lines.append('| Folder | Phase |')
        lines.append('|---|---|')
        for s in sorted(by_bucket['_IN_PRODUCTION'], key=lambda x: x.path.name):
            lines.append(f'| `{s.path.name}` | {s.phase} |')
    else:
        lines.append('_(none)_')
    lines.append('')

    # Ready to film
    lines.append('## Ready to film / filmed pre-publish')
    lines.append('')
    if by_bucket['_READY_TO_FILM']:
        lines.append('| Folder | Phase |')
        lines.append('|---|---|')
        for s in sorted(by_bucket['_READY_TO_FILM'], key=lambda x: x.path.name):
            lines.append(f'| `{s.path.name}` | {s.phase} |')
    else:
        lines.append('_(none)_')
    lines.append('')

    # Recently published (last 60 days, sorted desc)
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
    recent = []
    for s in by_bucket['_ARCHIVED/published']:
        if s.published_at and s.published_at > cutoff:
            recent.append(s)
    recent.sort(key=lambda x: x.published_at or '', reverse=True)
    lines.append('## Recently published (last 60 days)')
    lines.append('')
    if recent:
        lines.append('| Published | Folder | Video ID | Title |')
        lines.append('|---|---|---|---|')
        for s in recent:
            title_short = (s.video_title or '')[:60].replace('|', '\\|')
            lines.append(f'| {(s.published_at or "")[:10]} | `{s.path.name}` | `{s.video_id}` | {title_short} |')
    else:
        lines.append('_(none in last 60 days)_')
    lines.append('')

    # Full archive count
    lines.append(f'## All archived ({len(by_bucket["_ARCHIVED/published"])} folders)')
    lines.append('')
    lines.append('_Full list in `_ARCHIVED/published/`. Reverse-chronological by publish date below._')
    lines.append('')
    archived = sorted(by_bucket['_ARCHIVED/published'], key=lambda x: x.published_at or '', reverse=True)
    if archived:
        lines.append('| Published | Folder | Video ID |')
        lines.append('|---|---|---|')
        for s in archived:
            lines.append(f'| {(s.published_at or "—")[:10]} | `{s.path.name}` | `{s.video_id or "—"}` |')
        lines.append('')

    lines.append(DERIVED_CLOSE)
    return '\n'.join(lines) + '\n'


def write_root_status(states: list[FolderState], today: str) -> str | None:
    """Write/replace the AUTO:reconcile-dashboard block at the top of
    video-projects/PROJECT_STATUS.md. Preserves narrative below the close marker.
    Returns the previous full content (for .pre-diff backup) or None if file didn't exist.
    """
    block = render_root_status_block(states, today)
    existing = ''
    pre_existing = ROOT_STATUS.exists()
    if pre_existing:
        try:
            existing = ROOT_STATUS.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            existing = ''

    if DERIVED_OPEN in existing and DERIVED_CLOSE in existing:
        end = existing.index(DERIVED_CLOSE) + len(DERIVED_CLOSE)
        if end < len(existing) and existing[end] == '\n':
            end += 1
        new_content = block + existing[end:]
    else:
        sep = '\n' if existing and not existing.startswith('\n') else ''
        new_content = block + sep + existing

    ROOT_STATUS.parent.mkdir(parents=True, exist_ok=True)
    ROOT_STATUS.write_text(new_content, encoding='utf-8')
    return existing if pre_existing else None


def render_registry(states: list[FolderState], today: str) -> str:
    """Full regen of video-projects/PROJECT_REGISTRY.md. No narrative preserved — this
    is a pure index file."""
    by_bucket = {'_IN_PRODUCTION': [], '_READY_TO_FILM': [], '_ARCHIVED/published': []}
    for s in states:
        by_bucket.setdefault(s.bucket, []).append(s)

    lines = [
        '# Project Registry',
        '',
        f'**Last regenerated by `/reconcile`:** {today}',
        '',
        '**Purpose:** Quick-reference index of every video project folder with full paths.',
        '',
        '**Usage:** Reference this file for exact paths instead of using Glob. Regenerated each `/reconcile` run.',
        '',
        '---',
        '',
    ]

    sections = [
        ('In Production', '_IN_PRODUCTION', by_bucket['_IN_PRODUCTION']),
        ('Ready to Film / Filmed pre-publish', '_READY_TO_FILM', by_bucket['_READY_TO_FILM']),
        ('Archived (Published)', '_ARCHIVED/published', by_bucket['_ARCHIVED/published']),
    ]

    for heading, bucket_path, folders in sections:
        folders = sorted(folders, key=lambda x: x.path.name)
        lines.append(f'## {heading} ({len(folders)} folders)')
        lines.append('')
        if not folders:
            lines.append('_(none)_')
            lines.append('')
            lines.append('---')
            lines.append('')
            continue
        lines.append('| Folder | Phase | Video ID | Full Path |')
        lines.append('|---|---|---|---|')
        for s in folders:
            vid = s.video_id or '—'
            lines.append(f'| `{s.path.name}` | {s.phase} | `{vid}` | `{s.path}` |')
        lines.append('')
        lines.append('---')
        lines.append('')

    return '\n'.join(lines)


def write_registry(states: list[FolderState], today: str) -> str | None:
    """Full regen of PROJECT_REGISTRY.md. Returns previous content for backup."""
    content = render_registry(states, today)
    existing = ''
    pre_existing = ROOT_REGISTRY.exists()
    if pre_existing:
        try:
            existing = ROOT_REGISTRY.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            existing = ''
    ROOT_REGISTRY.write_text(content, encoding='utf-8')
    return existing if pre_existing else None


def render_brain_active_topics(states: list[FolderState]) -> list[str]:
    """Render rows for the .brain/index.md §3 Active Topics table.

    Includes only IN_PRODUCTION and READY_TO_FILM (active work). Archived projects
    are not active topics. Each row: Topic | Lifecycle | Last Touched
    """
    active = [s for s in states if s.bucket in ('_IN_PRODUCTION', '_READY_TO_FILM')]
    rows = ['| Topic | Lifecycle | Phase | Last Touched |',
            '|-------|-----------|-------|--------------|']
    if not active:
        rows.append('| _(no active topics)_ | | | |')
        return rows
    # Sort by most recently touched (mtime)
    def mtime(s):
        try:
            return max((f.stat().st_mtime for f in s.path.iterdir() if f.is_file()), default=0)
        except OSError:
            return 0
    active = sorted(active, key=mtime, reverse=True)
    for s in active:
        ts = mtime(s)
        date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d') if ts else '—'
        topic = s.path.name
        lifecycle = s.bucket
        rows.append(f'| `{topic}` | `{lifecycle}` | {s.phase} | {date_str} |')
    return rows


def write_brain_index_section_3(states: list[FolderState]) -> str | None:
    """Replace the table rows under §3 Active Topics in .brain/index.md.

    Strategy: locate "## 3. Active Topics" header, find the start of the next "##"
    header, replace the table rows between them while preserving any prose.
    """
    if not BRAIN_INDEX.exists():
        return None
    try:
        text = BRAIN_INDEX.read_text(encoding='utf-8', errors='ignore')
    except OSError:
        return None

    lines = text.splitlines()
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('## 3.') and 'Active' in line:
            start_idx = i
            continue
        if start_idx is not None and line.strip().startswith('## ') and i > start_idx:
            end_idx = i
            break
    if start_idx is None:
        return text  # Section not found, return existing as backup

    if end_idx is None:
        end_idx = len(lines)

    # Find where the table starts within section 3 (look for '|' line)
    table_start = None
    for j in range(start_idx + 1, end_idx):
        if lines[j].lstrip().startswith('|'):
            table_start = j
            break

    # Find where the table ends (last consecutive '|' line)
    table_end = None
    if table_start is not None:
        for j in range(table_start, end_idx):
            if lines[j].lstrip().startswith('|'):
                table_end = j
            else:
                if table_end is not None:
                    break
    if table_start is None or table_end is None:
        # No table found — append rows at end of section
        new_rows = render_brain_active_topics(states)
        new_lines = lines[:end_idx] + new_rows + [''] + lines[end_idx:]
    else:
        new_rows = render_brain_active_topics(states)
        new_lines = lines[:table_start] + new_rows + lines[table_end + 1:]

    new_content = '\n'.join(new_lines) + ('\n' if text.endswith('\n') else '')
    BRAIN_INDEX.write_text(new_content, encoding='utf-8')
    return text


# ---------------------------------------------------------------------------
# Proposal generation
# ---------------------------------------------------------------------------


def build_proposals(states: list[FolderState]) -> list[ProposedChange]:
    """Compute all proposed changes (moves + AUTO block writes) from the
    current state of each folder."""
    proposals = []
    for s in states:
        if s.blocked:
            # Manually blocked — no moves, no AUTO block writes. Folder stays put.
            continue
        target = target_bucket(s)
        if s.bucket != target:
            # Determine confidence band for moves into _ARCHIVED/published
            confidence = 'tier1' if s.match_score >= 1.0 else (
                'high' if s.match_score >= HIGH_CONFIDENCE else (
                    'gray' if s.match_score >= GRAY_FLOOR else 'none'
                )
            )
            # Folders without a published phase OR a video_id should never
            # propose a move to _ARCHIVED/published — gate it.
            if target == '_ARCHIVED/published' and not s.video_id:
                # Phase says published but no Video ID matched — leave in place
                continue
            proposals.append(ProposedChange(
                kind='move',
                folder=s.path,
                target_bucket=target,
                video_id=s.video_id,
                video_title=s.video_title,
                published_at=s.published_at,
                target_status=target_status_label(s),
                score=s.match_score,
                confidence=confidence,
            ))

        # AUTO block write proposal — always if drift exists
        existing = read_auto_block(s.path / 'PROJECT-STATUS.md')
        target_status = target_status_label(s)
        target_lifecycle = target
        needs_write = False
        if existing is None:
            needs_write = True
        else:
            if existing.get('Status') != target_status:
                needs_write = True
            if existing.get('Lifecycle') != target_lifecycle:
                needs_write = True
            if s.video_id and existing.get('Video ID') != s.video_id:
                needs_write = True
        if needs_write:
            proposals.append(ProposedChange(
                kind='edit-auto-block',
                folder=s.path,
                target_bucket=target,
                video_id=s.video_id,
                video_title=s.video_title,
                published_at=s.published_at,
                target_status=target_status,
                score=s.match_score,
                confidence='high' if s.video_id or s.match_score >= HIGH_CONFIDENCE else 'low',
            ))
    return proposals


# ---------------------------------------------------------------------------
# Diff log & apply
# ---------------------------------------------------------------------------


def diff_log_path() -> Path:
    ts = datetime.now().strftime('%Y-%m-%d-%H%M')
    BRAIN_INBOX.mkdir(parents=True, exist_ok=True)
    return BRAIN_INBOX / f'reconcile-{ts}.diff'


def write_diff_log(path: Path, proposals: list[ProposedChange],
                    backups: list[tuple[str, str]], moves: list[tuple[str, str]]) -> None:
    """Persist a machine-readable diff log used by --undo."""
    payload = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'moves': [{'from': str(a), 'to': str(b)} for a, b in moves],
        'backups': [{'path': p, 'pre_diff': pd} for p, pd in backups],
        'proposals': [
            {
                'kind': pr.kind,
                'folder': str(pr.folder),
                'target_bucket': pr.target_bucket,
                'video_id': pr.video_id,
                'video_title': pr.video_title,
                'target_status': pr.target_status,
                'score': pr.score,
                'confidence': pr.confidence,
            } for pr in proposals
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def apply_proposals(proposals: list[ProposedChange], today: str,
                    states_by_path: dict) -> tuple[list, list]:
    """Apply moves and AUTO block edits. Returns (backups, moves) for the diff log.

    backups: list of (file_path, pre_diff_path) — the .pre-diff sibling backups.
    moves:   list of (src_folder, dst_folder).
    """
    backups = []
    moves = []

    # Apply AUTO block edits FIRST (before moves change the path)
    for pr in proposals:
        if pr.kind != 'edit-auto-block':
            continue
        status_md = pr.folder / 'PROJECT-STATUS.md'
        state = states_by_path[pr.folder]
        block = render_auto_block(state, today)
        # Snapshot existing content as .pre-diff
        pre_diff = status_md.with_suffix('.md.pre-diff')
        if status_md.exists():
            shutil.copy2(status_md, pre_diff)
            backups.append((str(status_md), str(pre_diff)))
        elif status_md.parent.exists():
            # Mark "did not exist" — undo will delete the file we create
            pre_diff.write_text('__RECONCILE_DID_NOT_EXIST__', encoding='utf-8')
            backups.append((str(status_md), str(pre_diff)))
        write_auto_block(status_md, block)

    # Apply moves second
    bucket_paths = {
        '_IN_PRODUCTION': IN_PRODUCTION,
        '_READY_TO_FILM': READY_TO_FILM,
        '_ARCHIVED/published': ARCHIVED_PUBLISHED,
    }
    for pr in proposals:
        if pr.kind != 'move':
            continue
        dst_parent = bucket_paths[pr.target_bucket]
        dst_parent.mkdir(parents=True, exist_ok=True)
        dst = dst_parent / pr.folder.name
        if dst.exists():
            # Conflict — log and skip
            continue
        shutil.move(str(pr.folder), str(dst))
        moves.append((str(pr.folder), str(dst)))

    return backups, moves


def regenerate_derived_docs(today: str) -> list[tuple[str, str]]:
    """Re-scan filesystem post-moves and write root PROJECT_STATUS.md,
    PROJECT_REGISTRY.md, and .brain/index.md §3. Returns list of (path, pre_diff)
    backups for the diff log."""
    fresh_states = scan_buckets()
    attach_matches(fresh_states)

    backups = []
    for doc_path, write_fn in (
        (ROOT_STATUS, lambda: write_root_status(fresh_states, today)),
        (ROOT_REGISTRY, lambda: write_registry(fresh_states, today)),
        (BRAIN_INDEX, lambda: write_brain_index_section_3(fresh_states)),
    ):
        pre_diff = doc_path.with_suffix(doc_path.suffix + '.pre-diff')
        if doc_path.exists():
            shutil.copy2(doc_path, pre_diff)
            backups.append((str(doc_path), str(pre_diff)))
        else:
            pre_diff.write_text('__RECONCILE_DID_NOT_EXIST__', encoding='utf-8')
            backups.append((str(doc_path), str(pre_diff)))
        try:
            write_fn()
        except Exception:
            # Regen failure: leave file as-is, continue with others.
            continue
    return backups


def undo_latest() -> int:
    """Reverse the most recent reconcile run. Returns count of operations undone."""
    if not BRAIN_INBOX.exists():
        print('No diff logs found.')
        return 0
    diffs = sorted(BRAIN_INBOX.glob('reconcile-*.diff'), reverse=True)
    if not diffs:
        print('No diff logs found.')
        return 0
    latest = diffs[0]
    print(f'Reading: {latest}')
    payload = json.loads(latest.read_text(encoding='utf-8'))

    ops = 0
    # Reverse moves first (most recent action)
    for mv in reversed(payload['moves']):
        src = Path(mv['to'])    # currently at 'to', restore to 'from'
        dst = Path(mv['from'])
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            ops += 1
            print(f'  reversed move: {src} -> {dst}')

    # Restore file backups
    for backup in payload['backups']:
        original = Path(backup['path'])
        pre_diff = Path(backup['pre_diff'])
        if not pre_diff.exists():
            continue
        marker = pre_diff.read_text(encoding='utf-8', errors='ignore')
        if marker == '__RECONCILE_DID_NOT_EXIST__':
            if original.exists():
                original.unlink()
                ops += 1
                print(f'  removed created file: {original}')
        else:
            shutil.copy2(pre_diff, original)
            ops += 1
            print(f'  restored: {original}')
        pre_diff.unlink()

    # Rename the diff to indicate it was undone
    latest.rename(latest.with_suffix('.diff.undone'))
    return ops


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_proposals(proposals: list[ProposedChange], states: list[FolderState] | None = None) -> None:
    """Pretty-print the proposed changes grouped by confidence band."""
    moves = [p for p in proposals if p.kind == 'move']
    edits = [p for p in proposals if p.kind == 'edit-auto-block']

    tier1 = [p for p in moves if p.confidence == 'tier1']
    high = [p for p in moves if p.confidence == 'high']
    none_band = [p for p in moves if p.confidence == 'none']

    print(f'\n=== Proposed moves: {len(moves)} ===\n')

    if tier1:
        print(f'  Tier 1 (Video ID extracted, deterministic): {len(tier1)}')
        for p in tier1:
            title_short = (p.video_title or '')[:55]
            print(f'    {p.folder.name:55s} -> {p.target_bucket}  [{p.video_id}] {title_short!r}')
        print()
    if high:
        print(f'  HIGH confidence (fuzzy >= 0.85): {len(high)}')
        for p in high:
            title_short = (p.video_title or '')[:55]
            print(f'    {p.folder.name:55s} -> {p.target_bucket}  [{p.video_id} @ {p.score:.2f}] {title_short!r}')
        print()
    if none_band:
        print(f'  CONSERVATIVE (no archive proposal — needs user pick OR has no candidate): {len(none_band)}')
        for p in none_band:
            print(f'    {p.folder.name}  ->  {p.target_bucket} (not archive)')
        print()

    # Surface gray-zone candidates for manual review even when no auto-proposal was made
    if states:
        gray_zone = []
        for s in states:
            if not s.match_candidates:
                continue
            if s.video_id:  # Already matched via Tier 1
                continue
            top = s.match_candidates[0]
            if GRAY_FLOOR <= top.score < HIGH_CONFIDENCE:
                gray_zone.append((s, top))
        if gray_zone:
            print(f'\n=== GRAY ZONE — manual review needed: {len(gray_zone)} ===')
            print('  These folders may be published but Tier 1 ID extraction failed AND fuzzy match is not')
            print('  confident enough to auto-archive. Review and either:')
            print('    (a) add the Video ID to the folder\'s PROJECT-STATUS.md and re-run, OR')
            print('    (b) accept the gray-zone match by running /reconcile <slug> interactively.\n')
            for s, top in gray_zone:
                title_short = top.title[:60]
                print(f'    {s.path.name:55s}  best={top.score:.2f}  candidate=[{top.video_id}] {title_short!r}')

    if edits:
        print(f'\n=== AUTO block writes: {len(edits)} (per-folder PROJECT-STATUS.md) ===')


# ---------------------------------------------------------------------------
# Freshness gate
# ---------------------------------------------------------------------------


def analytics_db_age_hours() -> float:
    """Return max metrics_fetched_at age in hours, or sentinel 999 if cannot read."""
    import sqlite3
    if not ANALYTICS_DB.exists():
        return 999
    try:
        conn = sqlite3.connect(str(ANALYTICS_DB))
        cur = conn.cursor()
        cur.execute('SELECT MAX(metrics_fetched_at) FROM videos')
        row = cur.fetchone()
        conn.close()
        if not row or not row[0]:
            return 999
        fetched = datetime.fromisoformat(row[0].replace('Z', '+00:00'))
        if fetched.tzinfo is None:
            fetched = fetched.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - fetched
        return delta.total_seconds() / 3600
    except (OSError, ValueError, KeyError, AttributeError):
        return 999


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description='Reconcile project state.')
    parser.add_argument('project', nargs='?', help='Folder slug substring to reconcile')
    parser.add_argument('--dry-run', action='store_true', help='Show diff only; do not apply')
    parser.add_argument('--migrate', action='store_true', help='First-run retro migration')
    parser.add_argument('--auto-publish-only', action='store_true',
                        help='Routine 6 mode: archive YouTube-confirmed only; never touch memory snapshots')
    parser.add_argument('--undo', action='store_true', help='Reverse the latest reconcile run')
    parser.add_argument('--apply', action='store_true', help='Apply without interactive prompt (CI/scripted use)')
    args = parser.parse_args()

    if args.undo:
        ops = undo_latest()
        print(f'\nReversed {ops} operations.')
        return 0

    # Freshness gate for auto-publish-only mode
    if args.auto_publish_only:
        age = analytics_db_age_hours()
        if age > MAX_DB_AGE_HOURS:
            alert = BRAIN_INBOX / f'reconcile-stale-db-{datetime.now().strftime("%Y-%m-%d")}.md'
            BRAIN_INBOX.mkdir(parents=True, exist_ok=True)
            alert.write_text(
                f'# Routine 6 ABORTED — analytics.db stale ({age:.1f}h)\n\n'
                f'Routine 3 (channel-health-snapshot, 08:00) may have failed.\n'
                f'Check `tools/youtube_analytics/` auth and retry.\n',
                encoding='utf-8',
            )
            print(f'ABORT: analytics.db is {age:.1f}h stale (max {MAX_DB_AGE_HOURS}h).')
            return 2

    states = scan_buckets()

    # Filter to a single project if requested
    if args.project:
        needle = args.project.lower()
        states = [s for s in states if needle in s.path.name.lower()]
        if not states:
            print(f'No folder matches: {args.project}')
            return 1

    attach_matches(states)
    proposals = build_proposals(states)

    if args.dry_run:
        if not proposals:
            print('No changes needed. Everything reconciled.')
        else:
            print_proposals(proposals, states=states)
            print('\n(dry-run) Nothing applied.')
        return 0

    if not proposals:
        # No moves/AUTO blocks needed, but still regen derived docs (they may
        # be stale even when filesystem state hasn't drifted — e.g. analytics.db
        # got new metrics).
        today = datetime.now().strftime('%Y-%m-%d')
        derived_backups = regenerate_derived_docs(today)
        log_path = diff_log_path()
        write_diff_log(log_path, [], derived_backups, [])
        LAST_RECONCILE_TS.write_text(datetime.now(timezone.utc).isoformat(), encoding='utf-8')
        print(f'No folder moves needed. Regenerated {len(derived_backups)} derived docs.')
        print(f'Diff log: {log_path}')
        return 0

    print_proposals(proposals, states=states)

    # In auto-publish-only mode, filter to publish-related moves only
    if args.auto_publish_only:
        proposals = [
            p for p in proposals
            if (p.kind == 'move' and p.target_bucket == '_ARCHIVED/published'
                and p.confidence in ('tier1', 'high'))
            or (p.kind == 'edit-auto-block' and p.target_status == 'PUBLISHED')
        ]
        if not proposals:
            print('No publish-only changes to apply.')
            LAST_RECONCILE_TS.write_text(datetime.now(timezone.utc).isoformat(), encoding='utf-8')
            return 0

    # Confirmation gate (interactive)
    if not args.apply and not args.auto_publish_only:
        try:
            answer = input(f'\nApply {len(proposals)} changes? (y/N): ').strip().lower()
        except EOFError:
            answer = 'n'
        if answer != 'y':
            print('Aborted.')
            return 0

    today = datetime.now().strftime('%Y-%m-%d')
    states_by_path = {s.path: s for s in states}
    backups, moves = apply_proposals(proposals, today, states_by_path)

    # Always regen derived docs on any apply (even no-op proposals — keeps root
    # PROJECT_STATUS.md, PROJECT_REGISTRY.md, .brain/index.md §3 fresh).
    derived_backups = regenerate_derived_docs(today)
    backups.extend(derived_backups)

    # Write diff log
    log_path = diff_log_path()
    write_diff_log(log_path, proposals, backups, moves)
    print(f'\nApplied {len(moves)} moves + {len(backups)} file edits ({len(derived_backups)} derived docs).')
    print(f'Diff log: {log_path}')
    print(f'Undo with: /reconcile --undo')

    LAST_RECONCILE_TS.write_text(datetime.now(timezone.utc).isoformat(), encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
