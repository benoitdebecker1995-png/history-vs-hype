"""
CTR Quick Add — Zero-friction CTR ingestion for post-publish feedback.

Instead of manually editing CROSS-VIDEO-SYNTHESIS.md then running ctr_ingest,
just pass the title, CTR, views, and impressions. This tool:
1. Appends to CROSS-VIDEO-SYNTHESIS.md (keeps the master table current)
2. Writes directly to keywords.db ctr_snapshots table
3. Shows what pattern the title scorer would assign

Usage:
    python -m tools.ctr_quick_add "Title Here" --ctr 4.3 --views 1962 --impressions 36129
    python -m tools.ctr_quick_add "Title Here" --ctr 4.3 --views 1962  # impressions optional
    python -m tools.ctr_quick_add --batch ctr_data.txt   # One per line: title|ctr|views|impressions
    python -m tools.ctr_quick_add --show                 # Show all CTR data in DB

Designed for the 48-hour post-publish check: open YouTube Studio, read CTR, paste it in.
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


_SYNTHESIS_PATH = Path("channel-data/patterns/CROSS-VIDEO-SYNTHESIS.md")


def quick_add_ctr(
    title: str,
    ctr_percent: float,
    views: int,
    impressions: Optional[int] = None,
    retention: Optional[float] = None,
    subs_gained: Optional[int] = None,
    topic_type: str = "",
    snapshot_date: Optional[str] = None,
) -> dict:
    """
    Add CTR data for a video in one step.

    Updates both CROSS-VIDEO-SYNTHESIS.md and keywords.db.

    Returns:
        {'status': 'ok', 'db_written': bool, 'synthesis_updated': bool,
         'pattern': str, 'score': int}
    """
    from tools.title_scorer import score_title, detect_pattern

    if snapshot_date is None:
        snapshot_date = datetime.now(timezone.utc).date().isoformat()

    pattern = detect_pattern(title)
    result = score_title(title)

    response = {
        'status': 'ok',
        'pattern': pattern,
        'score': result['score'],
        'grade': result['grade'],
        'db_written': False,
        'synthesis_updated': False,
    }

    # 1. Write to DB
    try:
        from tools.discovery.database import KeywordDB
        db = KeywordDB()

        # Try to find video_id by title
        video_id = db.search_video_performance_by_title(title)

        if video_id:
            db_result = db.add_ctr_snapshot(
                video_id=video_id,
                ctr_percent=ctr_percent,
                impression_count=impressions or 0,
                view_count=views,
                snapshot_date=snapshot_date,
                is_late_entry=True,
            )
            if 'error' not in db_result:
                response['db_written'] = True
                response['video_id'] = video_id
            else:
                response['db_error'] = db_result['error']
        else:
            response['db_error'] = f"No video_performance match for: {title[:50]}"

        db.close()
    except Exception as e:
        response['db_error'] = str(e)

    # 2. Append to synthesis table
    try:
        if _SYNTHESIS_PATH.exists():
            _append_to_synthesis(
                title=title,
                views=views,
                retention=retention,
                ctr=ctr_percent,
                impressions=impressions,
                subs=subs_gained,
                topic_type=topic_type,
            )
            response['synthesis_updated'] = True
    except Exception as e:
        response['synthesis_error'] = str(e)

    return response


def _append_to_synthesis(
    title: str,
    views: int,
    retention: Optional[float],
    ctr: float,
    impressions: Optional[int],
    subs: Optional[int],
    topic_type: str,
) -> None:
    """Append a row to the master performance table in CROSS-VIDEO-SYNTHESIS.md."""
    content = _SYNTHESIS_PATH.read_text(encoding='utf-8')

    # Find the last row number in the table
    last_num = 0
    for match in re.finditer(r'^\|\s*(\d+)\s*\|', content, re.MULTILINE):
        num = int(match.group(1))
        if num > last_num:
            last_num = num

    new_num = last_num + 1
    ret_str = f"{retention:.1f}%" if retention is not None else "TBD"
    imp_str = f"{impressions:,}" if impressions is not None else "TBD"
    subs_str = f"+{subs}" if subs is not None else "TBD"
    topic_str = topic_type or "TBD"

    new_row = (
        f"| {new_num} | {title} | {views:,} | {ret_str} | {ctr:.2f}% "
        f"| {imp_str} | {subs_str} | {topic_str} |"
    )

    # Insert before the first blank line after the table (after the last | row)
    lines = content.split('\n')
    insert_idx = None
    in_table = False
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and '---' not in line:
            in_table = True
        elif in_table and not line.strip().startswith('|'):
            insert_idx = i
            break

    if insert_idx is not None:
        lines.insert(insert_idx, new_row)
        _SYNTHESIS_PATH.write_text('\n'.join(lines), encoding='utf-8')


def show_all_ctr() -> None:
    """Print all CTR snapshots from the DB."""
    try:
        from tools.discovery.database import KeywordDB
        db = KeywordDB()
        cursor = db._conn.cursor()
        cursor.execute("""
            SELECT vp.title, cs.ctr_percent, cs.view_count,
                   cs.impression_count, cs.snapshot_date
            FROM ctr_snapshots cs
            JOIN video_performance vp ON vp.video_id = cs.video_id
            WHERE cs.ctr_percent > 0
            ORDER BY cs.ctr_percent DESC
        """)
        rows = cursor.fetchall()
        db.close()

        if not rows:
            print("No CTR data in DB. Run: python -m tools.ctr_quick_add --help")
            return

        print(f"\n{'CTR':>6}  {'Views':>7}  {'Impr':>8}  {'Date':>10}  Title")
        print("-" * 90)
        for title, ctr, views, impressions, date in rows:
            print(f"{ctr:>5.1f}%  {views:>7,}  {impressions:>8,}  {date:>10}  {title[:50]}")
        print(f"\nTotal: {len(rows)} videos with CTR data")
    except Exception as e:
        print(f"Error reading DB: {e}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description='CTR Quick Add -- zero-friction post-publish data entry',
        epilog=(
            'Examples:\n'
            '  python -m tools.ctr_quick_add "My Title" --ctr 4.3 --views 1962 --impressions 36129\n'
            '  python -m tools.ctr_quick_add "My Title" --ctr 4.3 --views 1962 --retention 35.6\n'
            '  python -m tools.ctr_quick_add --show\n'
            '  python -m tools.ctr_quick_add --batch data.txt\n'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('title', nargs='?', help='Video title (as published)')
    parser.add_argument('--ctr', type=float, help='CTR percentage (e.g., 4.3)')
    parser.add_argument('--views', type=int, help='Total views')
    parser.add_argument('--impressions', type=int, help='Total impressions')
    parser.add_argument('--retention', type=float, help='Average retention %%')
    parser.add_argument('--subs', type=int, help='Subscribers gained')
    parser.add_argument('--topic', default='', help='Topic type (territorial, ideological, etc.)')
    parser.add_argument('--date', default=None, help='Snapshot date (YYYY-MM-DD, default: today)')
    parser.add_argument('--show', action='store_true', help='Show all CTR data in DB')
    parser.add_argument('--batch', help='Batch file: one line per video (title|ctr|views|impressions)')

    args = parser.parse_args()

    if args.show:
        show_all_ctr()
        return

    if args.batch:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            print(f"ERROR: Batch file not found: {args.batch}")
            sys.exit(1)
        lines = [l.strip() for l in batch_path.read_text().splitlines() if l.strip() and not l.startswith('#')]
        for line in lines:
            parts = line.split('|')
            if len(parts) < 3:
                print(f"SKIP (need title|ctr|views): {line}")
                continue
            title = parts[0].strip()
            ctr = float(parts[1].strip())
            views = int(parts[2].strip())
            impressions = int(parts[3].strip()) if len(parts) > 3 else None
            result = quick_add_ctr(title, ctr, views, impressions, snapshot_date=args.date)
            status = 'OK' if result['db_written'] else 'DB-MISS'
            print(f"  [{status}] {ctr:.1f}% CTR | {result['pattern']} | score={result['score']} | {title[:50]}")
        return

    if not args.title or args.ctr is None or args.views is None:
        parser.print_help()
        print("\nERROR: title, --ctr, and --views are required")
        sys.exit(1)

    result = quick_add_ctr(
        title=args.title,
        ctr_percent=args.ctr,
        views=args.views,
        impressions=args.impressions,
        retention=args.retention,
        subs_gained=args.subs,
        topic_type=args.topic,
        snapshot_date=args.date,
    )

    print(f"\n{'=' * 50}")
    print(f"  CTR QUICK ADD")
    print(f"{'=' * 50}")
    print(f"  Title:    {args.title}")
    print(f"  CTR:      {args.ctr:.1f}%")
    print(f"  Views:    {args.views:,}")
    if args.impressions:
        print(f"  Impr:     {args.impressions:,}")
    print(f"  Pattern:  {result['pattern']}")
    print(f"  Score:    {result['score']}/100 ({result['grade']})")
    print(f"  DB:       {'Written' if result['db_written'] else result.get('db_error', 'Failed')}")
    print(f"  Synth:    {'Updated' if result['synthesis_updated'] else result.get('synthesis_error', 'Skipped')}")
    print()


if __name__ == '__main__':
    main()
