"""
Packaging Lock — the code-enforced hard gate on packaging decisions.

Why this exists (ADR: "Packaging advancement is code-gated, not instruction-gated"):
#62 Volhynia was locked "from /greenlight + VidIQ" and justified by a single confident
number ("VidIQ 95/100") with NO record that the necessary-condition checks ever ran, and
no thumbnail. The rule already existed in greenlight.md prose — it simply didn't bind,
because a written step relies on the agent remembering to run it. A written rule about the
written rule wouldn't bind either. So the packaging lock is a checker that RUNS the
mechanical filters itself and WRITES a record; downstream commands refuse to advance a
project until a VALID lock exists.

The authority model (CONTEXT.md: "Packaging filter" / "Packaging enrichment"):
  FILTERS   — pass/fail NECESSARY CONDITIONS. All must PASS to advance. Not predictors.
              1. search-anchor      (title leads with a famous searchable parent)
              2. clickbait brand-gate (title_scorer hard_rejects empty)
              3. title<->thumb gap  (overlay doesn't restate the title) — JUDGMENT field
              4. thumbnail conditions (thumbnail_checker; PENDING until a concept exists)
  ENRICHMENT — recorded but NON-BINDING (title_scorer composite, /curiosity, VidIQ, NLM P5).
              Read, never gates; cannot upgrade a filter FAIL. Below-threshold = REVIEW nudge.

No pre-publish number is a "verdict" except demand. Live CTR is the only real one.

Usage:
    python -m tools.preflight.packaging_lock --project <path> --title "..." \
        [--curiosity N] [--vidiq "95/100 — clickbaity, rejected"] [--nlm "no diff risk"] \
        [--gap "overlay names the charge, title asks who — no overlap"] \
        [--territorial] [--person-focused] --write
    python -m tools.preflight.packaging_lock --project <path> --validate
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tools.logging_config import get_logger, safe_print, setup_logging
from tools.title_scorer import find_search_anchor, score_title
from tools.preflight.thumbnail_checker import check_project as check_thumbnail_project
# Fence markers + zone surgery live in status_doc; PACKAGING_LOCK_ZONE knows it
# sits BELOW the reconcile zone — this module renders its zone BODY only.
from tools.video_projects.status_doc import PACKAGING_LOCK_ZONE, StatusDoc

logger = get_logger(__name__)

# Curiosity/title-scorer nudge thresholds (enrichment only — NEVER gate on these).
CURIOSITY_NUDGE = 60
TITLE_SCORE_NUDGE = 65


# ---------------------------------------------------------------------------
# Title resolution
# ---------------------------------------------------------------------------

def _keyword_db_path() -> Optional[str]:
    """Best-effort locate keywords.db for DB-enriched title scoring. None on failure."""
    path = Path(__file__).resolve().parents[1] / 'discovery' / 'keywords.db'
    return str(path) if path.is_file() else None


def resolve_title(project_path: str, explicit: Optional[str] = None) -> Optional[str]:
    """Resolve the working title: explicit arg → lock zone → PROJECT-STATUS 'Working title' line."""
    if explicit:
        return explicit.strip().strip('"')

    doc = StatusDoc.load(Path(project_path) / 'PROJECT-STATUS.md')

    # Prefer a title already recorded inside the lock zone (round-trips validate).
    block = doc.zone(PACKAGING_LOCK_ZONE)
    if block:
        m = re.search(r'(?im)^\s*title:\s*"?(.+?)"?\s*$', block)
        if m:
            return m.group(1).strip().strip('"')

    # Fall back to the hand-written "Working title:" line (#62's format).
    return doc.working_title


# ---------------------------------------------------------------------------
# Filters + enrichment
# ---------------------------------------------------------------------------

def run_filters(
    title: str,
    project_path: str,
    *,
    curiosity_score: Optional[int] = None,
    vidiq: Optional[str] = None,
    nlm_note: Optional[str] = None,
    gap_note: Optional[str] = None,
    is_territorial: bool = False,
    is_person_focused: bool = False,
) -> Dict:
    """Run the four packaging FILTERS + collect ENRICHMENT. Never raises.

    Returns a dict:
      filters: {search_anchor, clickbait_gate, title_thumb_gap, thumbnail} each
               {'status': PASS|FAIL|PENDING|REVIEW, 'detail': str}
      enrichment: {title_scorer, curiosity, vidiq, nlm} each {'value', 'nudge'}
      verdict: 'LOCK VALID' | 'BLOCKED' | 'REVIEW'
      reasons: list[str]
    """
    filters: Dict[str, Dict[str, str]] = {}
    enrichment: Dict[str, Dict] = {}

    # --- FILTER 1: search anchor (mechanical) ---
    # describe() carries the PROVENANCE into the written block: a curated head term, or
    # a measured volume and where it was measured (ADR-0023). On a FAIL it carries the
    # repair command, because a FAIL means either "rewrite the title" or "this term is
    # famous and unmeasured" and the block should not leave the reader guessing which.
    anchor = find_search_anchor(title)
    filters['search_anchor'] = {
        'status': 'PASS' if anchor.found else 'FAIL',
        'detail': anchor.describe(),
    }

    # --- FILTER 2: clickbait brand-gate (mechanical) + title_scorer as ENRICHMENT ---
    ts = score_title(title, db_path=_keyword_db_path())
    hard_rejects = ts.get('hard_rejects') or []
    filters['clickbait_gate'] = {
        'status': 'PASS' if not hard_rejects else 'FAIL',
        'detail': 'no hard_rejects (clickbait tone clean)' if not hard_rejects
                  else 'BRAND-GATE REJECT: ' + '; '.join(hard_rejects),
    }
    ts_score = ts.get('score')
    enrichment['title_scorer'] = {
        'value': f"{ts_score}/100 (grade {ts.get('grade', '?')})",
        'nudge': (ts_score is not None and ts_score < TITLE_SCORE_NUDGE),
    }

    # --- FILTER 3: title<->thumbnail curiosity gap (JUDGMENT field) ---
    # Filled by the agent (greenlight). Blank = the lock is INVALID (can't advance).
    gap = (gap_note or '').strip()
    filters['title_thumb_gap'] = {
        'status': 'PASS' if gap else 'UNFILLED',
        'detail': gap if gap
                  else 'JUDGMENT REQUIRED — state why the overlay does not restate the title '
                       '(or mark PENDING with a reason if no concept exists yet)',
    }

    # --- FILTER 4: thumbnail necessary conditions (mechanical; PENDING when no concept) ---
    thumb = check_thumbnail_project(project_path, is_person_focused, is_territorial)
    tverdict = thumb.get('verdict', 'MISSING')
    if tverdict == 'MISSING':
        filters['thumbnail'] = {
            'status': 'PENDING',
            'detail': 'no thumbnail concept yet — generate 3 via /thumbnail; not a blocker for research',
        }
    else:
        # PASS→PASS, REVIEW→REVIEW (nudge, non-blocking), FAIL→FAIL (blocks)
        filters['thumbnail'] = {
            'status': tverdict,
            'detail': '; '.join(thumb.get('issues') or []) or 'necessary conditions met',
        }

    # --- ENRICHMENT: curiosity / VidIQ / NLM (agent-supplied, non-binding) ---
    if curiosity_score is not None:
        enrichment['curiosity'] = {
            'value': f'{curiosity_score}/100',
            'nudge': curiosity_score < CURIOSITY_NUDGE,
        }
    else:
        enrichment['curiosity'] = {'value': 'not run', 'nudge': False}
    enrichment['vidiq'] = {'value': vidiq or 'not queried', 'nudge': False}
    enrichment['nlm'] = {'value': nlm_note or 'not queried', 'nudge': False}

    verdict, reasons = _verdict(filters, enrichment)
    return {'filters': filters, 'enrichment': enrichment, 'verdict': verdict, 'reasons': reasons}


def _verdict(filters: Dict, enrichment: Dict) -> Tuple[str, List[str]]:
    """Derive the verdict. BLOCKED overrides REVIEW overrides VALID. Enrichment never blocks."""
    reasons: List[str] = []
    blocked = False

    # Mechanical filters that FAIL block advancement.
    for key in ('search_anchor', 'clickbait_gate'):
        if filters[key]['status'] == 'FAIL':
            blocked = True
            reasons.append(f'{key} FAILED — {filters[key]["detail"]}')

    # Thumbnail FAIL blocks; PENDING/REVIEW do not.
    if filters['thumbnail']['status'] == 'FAIL':
        blocked = True
        reasons.append(f'thumbnail conditions FAILED — {filters["thumbnail"]["detail"]}')

    # Judgment field must be filled (PASS) — UNFILLED = invalid lock.
    if filters['title_thumb_gap']['status'] == 'UNFILLED':
        blocked = True
        reasons.append('title<->thumbnail gap judgment is BLANK — a lock with an empty judgment '
                       'field is INVALID (fill it, or mark PENDING with a reason)')

    if blocked:
        return 'BLOCKED', reasons

    # Non-blocking REVIEW nudges (enrichment below threshold, or thumbnail REVIEW).
    if enrichment['title_scorer']['nudge']:
        reasons.append(f'title_scorer {enrichment["title_scorer"]["value"]} < {TITLE_SCORE_NUDGE} '
                       '— eyeball it (nudge, not a block)')
    if enrichment['curiosity']['nudge']:
        reasons.append(f'/curiosity {enrichment["curiosity"]["value"]} < {CURIOSITY_NUDGE} '
                       '— eyeball it (nudge, not a block)')
    if filters['thumbnail']['status'] == 'REVIEW':
        reasons.append(f'thumbnail REVIEW — {filters["thumbnail"]["detail"]} (nudge, not a block)')

    return ('REVIEW' if reasons else 'LOCK VALID'), reasons


# ---------------------------------------------------------------------------
# Render + write the lock block
# ---------------------------------------------------------------------------

def render_lock_block(title: str, result: Dict, today: Optional[str] = None) -> str:
    """Render the packaging-lock zone body (marker-less; StatusDoc frames it)."""
    today = today or date.today().isoformat()
    f = result['filters']
    e = result['enrichment']
    lines = [
        f'## Packaging Lock ({today})',
        f'title: "{title}"',
        'FILTERS (pass/fail — all must PASS to advance; PENDING allowed for thumbnail):',
        f'  search-anchor:        {f["search_anchor"]["status"]}  ({f["search_anchor"]["detail"]})',
        f'  clickbait brand-gate: {f["clickbait_gate"]["status"]}  ({f["clickbait_gate"]["detail"]})',
        f'  title<->thumb gap:    {f["title_thumb_gap"]["status"]}  ({f["title_thumb_gap"]["detail"]})',
        f'  thumbnail conditions: {f["thumbnail"]["status"]}  ({f["thumbnail"]["detail"]})',
        'ENRICHMENT (recorded, non-binding — cannot override a FILTER FAIL):',
        f'  title_scorer:  {e["title_scorer"]["value"]}'
        + ('   [REVIEW nudge]' if e['title_scorer']['nudge'] else ''),
        f'  /curiosity:    {e["curiosity"]["value"]}'
        + ('   [REVIEW nudge]' if e['curiosity']['nudge'] else ''),
        f'  VidIQ MCP:     {e["vidiq"]["value"]}   (clickbait-guard: rejected if it pushes a kill-list title)',
        f'  NLM P5:        {e["nlm"]["value"]}',
        f'VERDICT: {result["verdict"]}'
        + (f'  — {"; ".join(result["reasons"])}' if result['reasons'] else ''),
    ]
    return '\n'.join(lines)


def write_lock_block(project_path: str, body: str) -> str:
    """Write/replace the packaging-lock zone in PROJECT-STATUS.md, preserving
    everything else. Placement policy lives on PACKAGING_LOCK_ZONE: in place if
    present, else just below the reconcile zone, else prepended. Returns
    previous file content (for backup)."""
    doc = StatusDoc.load(Path(project_path) / 'PROJECT-STATUS.md')
    doc.write_zone(PACKAGING_LOCK_ZONE, body)
    return doc.save()


# ---------------------------------------------------------------------------
# Validate (the hard gate downstream commands call)
# ---------------------------------------------------------------------------

def _parse_block(project_path: str) -> Optional[Dict[str, str]]:
    """Parse the FILTERS lines + title out of an existing lock zone. None if no zone."""
    block = StatusDoc.load(Path(project_path) / 'PROJECT-STATUS.md').zone(PACKAGING_LOCK_ZONE)
    if block is None:
        return None

    parsed: Dict[str, str] = {}
    tm = re.search(r'(?im)^\s*title:\s*"?(.+?)"?\s*$', block)
    if tm:
        parsed['title'] = tm.group(1).strip().strip('"')
    for key, label in (
        ('search_anchor', r'search-anchor'),
        ('clickbait_gate', r'clickbait brand-gate'),
        ('title_thumb_gap', r'title<->thumb gap'),
        ('thumbnail', r'thumbnail conditions'),
    ):
        m = re.search(rf'(?im)^\s*{label}:\s*(\w+)', block)
        if m:
            parsed[key] = m.group(1).upper()
    return parsed


def validate_lock(project_path: str) -> Tuple[bool, List[str]]:
    """The hard gate. VALID iff: block present AND mechanical filters (recomputed from the
    live title, so hand-editing PASS onto a bad title can't fool it) PASS AND the judgment
    field is filled AND thumbnail is not FAIL. Thumbnail PENDING is allowed. Never raises."""
    parsed = _parse_block(project_path)
    if parsed is None:
        return False, ['no packaging-lock block on record — run `packaging_lock --write` at /greenlight']

    reasons: List[str] = []
    title = parsed.get('title')
    if not title:
        return False, ['packaging-lock block present but has no title line — regenerate it']

    # Recompute the mechanical filters from the current title (anti-tamper).
    anchor = find_search_anchor(title)
    if not anchor.found:
        reasons.append('search-anchor FAILS on the current title (recomputed) — '
                       + anchor.describe())
    hard_rejects = (score_title(title, db_path=_keyword_db_path()).get('hard_rejects') or [])
    if hard_rejects:
        reasons.append('clickbait brand-gate FAILS (recomputed): ' + '; '.join(hard_rejects))

    # Judgment field must be filled (recorded as PASS/PENDING, never UNFILLED).
    if parsed.get('title_thumb_gap', 'UNFILLED') == 'UNFILLED':
        reasons.append('title<->thumbnail gap judgment is BLANK — INVALID lock')

    # Thumbnail FAIL blocks; PENDING/REVIEW/PASS do not.
    if parsed.get('thumbnail') == 'FAIL':
        reasons.append('thumbnail conditions FAIL')

    return (len(reasons) == 0), reasons


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_result(title: str, result: Dict) -> None:
    # safe_print: this echoes the working title and filter details written by a human,
    # and main() exits 2 on BLOCKED. An unprintable character in a title must not
    # become a packaging-lock block.
    safe_print(f"\n{'=' * 64}")
    safe_print("  PACKAGING LOCK  (filters = necessary conditions, NOT a clickability score)")
    safe_print(f"{'=' * 64}")
    safe_print(f'  title: "{title}"')
    safe_print("  FILTERS:")
    for k in ('search_anchor', 'clickbait_gate', 'title_thumb_gap', 'thumbnail'):
        fl = result['filters'][k]
        safe_print(f"    {k:16} {fl['status']:8} {fl['detail']}")
    safe_print("  ENRICHMENT (non-binding):")
    for k in ('title_scorer', 'curiosity', 'vidiq', 'nlm'):
        en = result['enrichment'][k]
        nudge = '  [REVIEW nudge]' if en.get('nudge') else ''
        safe_print(f"    {k:16} {en['value']}{nudge}")
    safe_print(f"\n  VERDICT: {result['verdict']}")
    for r in result['reasons']:
        safe_print(f"    - {r}")
    safe_print(f"{'=' * 64}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Packaging lock — code-enforced hard gate")
    parser.add_argument("--project", required=True, help="Project folder path")
    parser.add_argument("--title", help="Working title (else resolved from PROJECT-STATUS.md)")
    parser.add_argument("--curiosity", type=int, help="/curiosity score (enrichment)")
    parser.add_argument("--vidiq", help="VidIQ MCP note/score (enrichment)")
    parser.add_argument("--nlm", help="NLM P5 differentiation note (enrichment)")
    parser.add_argument("--gap", help="title<->thumbnail curiosity-gap judgment (fills the required field)")
    parser.add_argument("--territorial", action="store_true")
    parser.add_argument("--person-focused", action="store_true")
    parser.add_argument("--write", action="store_true", help="Run filters and WRITE the lock block")
    parser.add_argument("--validate", action="store_true", help="Validate the existing lock (hard gate)")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()
    setup_logging(args.verbose, args.quiet)

    if args.validate and not args.write:
        valid, reasons = validate_lock(args.project)
        if valid:
            safe_print("PACKAGING LOCK: VALID — project may advance.")
            sys.exit(0)
        safe_print("PACKAGING LOCK: BLOCKED — project may NOT advance:")
        for r in reasons:
            safe_print(f"  - {r}")
        sys.exit(2)

    # Default / --write path
    title = resolve_title(args.project, args.title)
    if not title:
        safe_print("ERROR: no title (pass --title or add a 'Working title:' line to PROJECT-STATUS.md)")
        sys.exit(2)

    result = run_filters(
        title, args.project,
        curiosity_score=args.curiosity, vidiq=args.vidiq, nlm_note=args.nlm, gap_note=args.gap,
        is_territorial=args.territorial, is_person_focused=args.person_focused,
    )
    _print_result(title, result)

    if args.write:
        write_lock_block(args.project, render_lock_block(title, result))
        print(f"Wrote AUTO:packaging-lock block to {args.project}/PROJECT-STATUS.md")

    sys.exit(0 if result['verdict'] != 'BLOCKED' else 2)


if __name__ == '__main__':
    main()
