"""
Keyword Management CLI

Main command-line interface for keyword database operations.
Add, search, export keywords with multiple output formats.

Usage:
    python keywords.py add "sykes picot" --source manual
    python keywords.py add "sykes picot, bir tawil, dark ages" --batch
    python keywords.py search --pattern "dark%"
    python keywords.py search --source autocomplete
    python keywords.py search --intent MYTH_BUSTING
    python keywords.py list --all
    python keywords.py stats
    python keywords.py export --json > keywords.json
    python keywords.py export --markdown > keywords.md

Output formats:
    - Default: Markdown tables
    - --json: JSON format

Exit codes:
    0 = Success
    1 = Error
"""

import sys
import json
import argparse
from typing import Dict, List, Any, Optional
from pathlib import Path

from database import KeywordDB


def add_keyword(
    keyword: str,
    source: str = 'manual',
    search_volume: Optional[int] = None,
    competition: Optional[float] = None,
    db: Optional[KeywordDB] = None
) -> Dict[str, Any]:
    """
    Add single keyword to database.

    Args:
        keyword: Keyword text
        source: Source ('autocomplete', 'manual', 'competitor', 'vidiq')
        search_volume: Optional search volume
        competition: Optional competition score 0-100
        db: Optional KeywordDB instance (creates new if None)

    Returns:
        Keyword record dict with ID on success
        {'error': msg} on failure
    """
    close_db = False
    if db is None:
        db = KeywordDB()
        close_db = True

    result = db.add_keyword(keyword, source, search_volume, competition)

    if close_db:
        db.close()

    return result


def add_keywords_batch(
    keywords: List[str],
    source: str = 'manual',
    db: Optional[KeywordDB] = None
) -> Dict[str, Any]:
    """
    Add multiple keywords to database.

    Args:
        keywords: List of keyword strings
        source: Source for all keywords
        db: Optional KeywordDB instance

    Returns:
        {'added': int, 'updated': int, 'skipped': int, 'errors': [...]} summary
    """
    close_db = False
    if db is None:
        db = KeywordDB()
        close_db = True

    added = 0
    updated = 0
    errors = []

    for keyword in keywords:
        result = db.add_keyword(keyword, source)

        if 'error' in result:
            errors.append({'keyword': keyword, 'error': result['error']})
        elif result.get('action') == 'inserted':
            added += 1
        elif result.get('action') == 'updated':
            updated += 1

    if close_db:
        db.close()

    return {
        'added': added,
        'updated': updated,
        'skipped': 0,  # Currently no duplicate detection at this level
        'total_processed': len(keywords),
        'errors': errors
    }


def search_keywords(
    pattern: Optional[str] = None,
    source: Optional[str] = None,
    intent: Optional[str] = None,
    limit: int = 50,
    db: Optional[KeywordDB] = None
) -> List[Dict[str, Any]]:
    """
    Search keywords with optional filters.

    Args:
        pattern: SQL LIKE pattern (e.g., 'dark%')
        source: Source filter
        intent: Intent category filter
        limit: Maximum results
        db: Optional KeywordDB instance

    Returns:
        List of keyword records
    """
    close_db = False
    if db is None:
        db = KeywordDB()
        close_db = True

    # Determine which search to use
    if intent:
        results = db.get_keywords_by_intent(intent, limit)
    elif source:
        results = db.get_keywords_by_source(source, limit)
    else:
        results = db.search_keywords(pattern, limit)

    if close_db:
        db.close()

    return results


def export_keywords(
    format: str = 'markdown',
    filters: Optional[Dict[str, Any]] = None,
    db: Optional[KeywordDB] = None
) -> str:
    """
    Export keywords in specified format.

    Args:
        format: 'markdown' or 'json'
        filters: Optional filters dict (pattern, source, intent, limit)
        db: Optional KeywordDB instance

    Returns:
        Formatted string (markdown table or JSON)
    """
    close_db = False
    if db is None:
        db = KeywordDB()
        close_db = True

    # Apply filters
    filters = filters or {}
    keywords = search_keywords(
        pattern=filters.get('pattern'),
        source=filters.get('source'),
        intent=filters.get('intent'),
        limit=filters.get('limit', 1000),
        db=db
    )

    if close_db:
        db.close()

    # Format output
    if format == 'json':
        return json.dumps(keywords, indent=2)
    else:
        # Markdown table
        if not keywords:
            return "No keywords found.\n"

        output = ["# Keywords\n"]
        output.append("| Keyword | Source | Search Volume | Competition | Last Updated |")
        output.append("|---------|--------|---------------|-------------|--------------|")

        for kw in keywords:
            keyword = kw.get('keyword', '')
            source = kw.get('source', 'N/A')
            volume = kw.get('search_volume', 'N/A')
            competition = kw.get('competition_score', 'N/A')
            updated = kw.get('last_updated', 'N/A')

            # Format competition as percentage if present
            if competition != 'N/A' and competition is not None:
                competition = f"{competition:.1f}"

            output.append(f"| {keyword} | {source} | {volume} | {competition} | {updated} |")

        output.append("")
        return "\n".join(output)


def format_stats(stats: Dict[str, Any]) -> str:
    """
    Format database statistics as markdown.

    Args:
        stats: Stats dict from db.get_keyword_stats()

    Returns:
        Formatted markdown string
    """
    output = ["# Keyword Database Statistics\n"]

    output.append(f"**Total Keywords:** {stats.get('total_keywords', 0)}")
    output.append("")

    # By source
    by_source = stats.get('by_source', {})
    if by_source:
        output.append("**Keywords by Source:**")
        for source, count in by_source.items():
            output.append(f"- {source}: {count}")
        output.append("")

    output.append(f"**With Intent Classification:** {stats.get('with_intent', 0)}")
    output.append(f"**With Performance Data:** {stats.get('with_performance', 0)}")
    output.append("")

    return "\n".join(output)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Keyword database management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add keywords
  python keywords.py add "sykes picot" --source manual
  python keywords.py add "sykes picot, bir tawil" --batch

  # Search keywords
  python keywords.py search --pattern "dark%"
  python keywords.py search --source autocomplete
  python keywords.py search --intent MYTH_BUSTING

  # List and export
  python keywords.py list --all
  python keywords.py stats
  python keywords.py export --json > keywords.json
  python keywords.py export --markdown > keywords.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add keyword(s) to database')
    add_parser.add_argument('keywords', help='Keyword(s) - comma-separated for batch')
    add_parser.add_argument('--source', default='manual', choices=['manual', 'autocomplete', 'competitor', 'vidiq'],
                            help='Keyword source (default: manual)')
    add_parser.add_argument('--batch', action='store_true', help='Treat as comma-separated batch')
    add_parser.add_argument('--volume', type=int, help='Search volume estimate')
    add_parser.add_argument('--competition', type=float, help='Competition score 0-100')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search keywords')
    search_parser.add_argument('--pattern', help='SQL LIKE pattern (e.g., "dark%%")')
    search_parser.add_argument('--source', choices=['manual', 'autocomplete', 'competitor', 'vidiq'],
                               help='Filter by source')
    search_parser.add_argument('--intent', help='Filter by intent category (e.g., MYTH_BUSTING)')
    search_parser.add_argument('--limit', type=int, default=50, help='Max results (default 50)')
    search_parser.add_argument('--json', action='store_true', help='Output JSON')

    # List command
    list_parser = subparsers.add_parser('list', help='List all keywords')
    list_parser.add_argument('--all', action='store_true', help='List all keywords')
    list_parser.add_argument('--limit', type=int, default=50, help='Max results (default 50)')
    list_parser.add_argument('--json', action='store_true', help='Output JSON')

    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output JSON')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export keywords')
    export_parser.add_argument('--json', action='store_true', help='Export as JSON (default: markdown)')
    export_parser.add_argument('--markdown', action='store_true', help='Export as Markdown table')
    export_parser.add_argument('--pattern', help='Filter pattern')
    export_parser.add_argument('--source', help='Filter by source')
    export_parser.add_argument('--intent', help='Filter by intent')
    export_parser.add_argument('--limit', type=int, default=1000, help='Max results (default 1000)')

    args = parser.parse_args()

    # Require command
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize database connection
    db = KeywordDB()

    # Execute command
    try:
        if args.command == 'add':
            if args.batch:
                # Batch add
                keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
                result = add_keywords_batch(keywords, args.source, db)

                print(f"Added: {result['added']}")
                print(f"Updated: {result['updated']}")
                print(f"Total processed: {result['total_processed']}")

                if result['errors']:
                    print(f"\nErrors: {len(result['errors'])}")
                    for err in result['errors']:
                        print(f"  - {err['keyword']}: {err['error']}")
            else:
                # Single add
                result = add_keyword(
                    args.keywords,
                    args.source,
                    args.volume,
                    args.competition,
                    db
                )

                if 'error' in result:
                    print(f"ERROR: {result['error']}", file=sys.stderr)
                    sys.exit(1)
                else:
                    print(f"Keyword '{result['keyword']}' {result['action']} (ID: {result['keyword_id']})")

        elif args.command == 'search':
            results = search_keywords(
                pattern=args.pattern,
                source=args.source,
                intent=args.intent,
                limit=args.limit,
                db=db
            )

            if args.json:
                print(json.dumps(results, indent=2))
            else:
                if not results:
                    print("No keywords found.")
                else:
                    output = export_keywords('markdown', filters={'limit': len(results)}, db=None)
                    # Manually format since export uses new DB connection
                    print(f"# Search Results ({len(results)} keywords)\n")
                    print("| Keyword | Source | Search Volume | Competition | Last Updated |")
                    print("|---------|--------|---------------|-------------|--------------|")
                    for kw in results:
                        keyword = kw.get('keyword', '')
                        source = kw.get('source', 'N/A')
                        volume = kw.get('search_volume', 'N/A')
                        competition = kw.get('competition_score', 'N/A')
                        updated = kw.get('last_updated', 'N/A')

                        if competition != 'N/A' and competition is not None:
                            competition = f"{competition:.1f}"

                        print(f"| {keyword} | {source} | {volume} | {competition} | {updated} |")

        elif args.command == 'list':
            results = search_keywords(pattern=None, limit=args.limit, db=db)

            if args.json:
                print(json.dumps(results, indent=2))
            else:
                if not results:
                    print("No keywords in database.")
                else:
                    print(f"# All Keywords ({len(results)} total)\n")
                    print("| Keyword | Source | Search Volume | Competition | Last Updated |")
                    print("|---------|--------|---------------|-------------|--------------|")
                    for kw in results:
                        keyword = kw.get('keyword', '')
                        source = kw.get('source', 'N/A')
                        volume = kw.get('search_volume', 'N/A')
                        competition = kw.get('competition_score', 'N/A')
                        updated = kw.get('last_updated', 'N/A')

                        if competition != 'N/A' and competition is not None:
                            competition = f"{competition:.1f}"

                        print(f"| {keyword} | {source} | {volume} | {competition} | {updated} |")

        elif args.command == 'stats':
            stats = db.get_keyword_stats()

            if args.json:
                print(json.dumps(stats, indent=2))
            else:
                print(format_stats(stats))

        elif args.command == 'export':
            format_type = 'json' if args.json else 'markdown'
            filters = {
                'pattern': args.pattern,
                'source': args.source,
                'intent': args.intent,
                'limit': args.limit
            }

            output = export_keywords(format_type, filters, db)
            print(output)

    finally:
        db.close()


if __name__ == '__main__':
    main()
