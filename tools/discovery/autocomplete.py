"""
YouTube Autocomplete Scraper

Extract keyword suggestions from YouTube's autocomplete feature using browser automation.
Uses pyppeteer (Python port of Puppeteer) with stealth plugin to avoid detection.

IMPORTANT: YouTube blocks simple HTTP requests to autocomplete endpoint.
Must use full browser simulation with anti-detection measures.

Usage:
    CLI:
        python autocomplete.py "dark ages myth"
        python autocomplete.py "dark ages, crusades, colonialism"
        python autocomplete.py --seed-file seeds.txt
        python autocomplete.py "dark ages" --save
        python autocomplete.py "dark ages" --json

    Python:
        import asyncio
        from autocomplete import get_autocomplete_suggestions

        result = asyncio.run(get_autocomplete_suggestions("dark ages myth"))
        if 'error' not in result:
            print(result['suggestions'])

Returns:
    Success: {'keyword': str, 'suggestions': [...], 'fetched_at': timestamp}
    Failure: {'error': str, 'details': str}

Rate Limiting:
    - Minimum 2 second delay between requests
    - Random jitter 1-3s additional
    - Exponential backoff on errors (1s, 2s, 4s, 8s)

Installation:
    pip install pyppeteer pyppeteer-stealth

Dependencies:
    - pyppeteer (Python port of Puppeteer)
    - pyppeteer-stealth (anti-detection plugin)
"""

import asyncio
import os
import random
import time
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    from pyppeteer import launch
    from pyppeteer_stealth import stealth
    PYPPETEER_AVAILABLE = True
except ImportError:
    PYPPETEER_AVAILABLE = False


async def get_autocomplete_suggestions(seed_keyword: str, max_suggestions: int = 10) -> Dict[str, Any]:
    """
    Extract autocomplete suggestions from YouTube for a seed keyword.

    Uses headless browser with stealth settings to avoid detection.

    Args:
        seed_keyword: Keyword to get suggestions for
        max_suggestions: Maximum suggestions to return (default 10)

    Returns:
        Success: {'keyword': seed_keyword, 'suggestions': [...], 'fetched_at': timestamp}
        Failure: {'error': str, 'details': str}
    """
    if not PYPPETEER_AVAILABLE:
        return {
            'error': 'pyppeteer not installed',
            'details': 'Install with: pip install pyppeteer pyppeteer-stealth',
            'install_note': 'See requirements.txt for details'
        }

    browser = None
    try:
        # Launch headless browser with stealth
        browser = await launch({
            'headless': True,
            'executablePath': os.environ.get(
                'PYPPETEER_EXECUTABLE_PATH',
                r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            ),
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920x1080'
            ]
        })

        page = await browser.newPage()

        # Apply stealth settings to avoid detection
        await stealth(page)

        # Set viewport and user agent
        await page.setViewport({'width': 1920, 'height': 1080})
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # Navigate to YouTube
        await page.goto('https://www.youtube.com', {'waitUntil': 'networkidle0', 'timeout': 30000})

        # Wait for search box
        await page.waitForSelector('input[name="search_query"]', {'timeout': 10000})

        # Click search box to focus
        await page.click('input[name="search_query"]')

        # Type seed keyword slowly (more human-like)
        for char in seed_keyword:
            await page.type('input[name="search_query"]', char, {'delay': random.randint(50, 150)})

        # Wait for autocomplete dropdown to appear
        await asyncio.sleep(1.5)

        # Extract suggestions from dropdown
        # YouTube autocomplete uses several possible selectors depending on version
        suggestions = await page.evaluate('''() => {
            // Try multiple selector strategies for YouTube autocomplete
            const selectors = [
                'ytd-search-suggestion-renderer span',
                'ytd-search-suggestion-renderer .style-scope',
                '.sbdd_b li .sbqs_c',
                '.sbdd_b ul li',
                'ul.sbdd_b li',
                '#search-suggestions li',
                'ytd-search-suggestions-renderer li',
                '.gsfs_e',
                '[role="listbox"] [role="option"]',
                'li.sbsb_c',
                '.sbsb_a li .sbqs_c',
                '.sbsb_a li',
            ];

            const results = [];
            for (const selector of selectors) {
                const elements = document.querySelectorAll(selector);
                for (const el of elements) {
                    const text = el.textContent.trim();
                    if (text && text.length > 2 && !results.includes(text)) {
                        results.push(text);
                    }
                }
                if (results.length > 0) break;
            }
            return results;
        }''')

        # Close browser
        await browser.close()
        browser = None

        # Filter and limit suggestions
        filtered = [s for s in suggestions if s and len(s) > 0][:max_suggestions]

        return {
            'keyword': seed_keyword,
            'suggestions': filtered,
            'count': len(filtered),
            'fetched_at': datetime.now(timezone.utc).isoformat() + 'Z'
        }

    except Exception as e:
        # Clean up browser on error
        if browser:
            await browser.close()

        error_type = type(e).__name__

        # Provide helpful error messages
        if 'timeout' in str(e).lower():
            return {
                'error': 'Request timeout',
                'details': 'YouTube did not respond in time. Try again or check network connection.',
                'type': error_type
            }
        elif 'rate limit' in str(e).lower() or '429' in str(e):
            return {
                'error': 'Rate limited by YouTube',
                'details': 'Too many requests. Wait 5-10 minutes before retrying.',
                'type': error_type
            }
        else:
            return {
                'error': f'Autocomplete extraction failed: {error_type}',
                'details': str(e)
            }


def extract_keywords_batch(seeds: List[str], delay_seconds: float = 2.0) -> List[Dict[str, Any]]:
    """
    Extract autocomplete suggestions for multiple seed keywords.

    Implements rate limiting with random jitter and exponential backoff on errors.

    Args:
        seeds: List of seed keywords
        delay_seconds: Base delay between requests (default 2.0)

    Returns:
        List of results (each is dict from get_autocomplete_suggestions)
    """
    results = []
    backoff = 1.0

    for i, seed in enumerate(seeds):
        print(f"Processing {i+1}/{len(seeds)}: {seed}", file=sys.stderr)

        # Run async function
        result = asyncio.run(get_autocomplete_suggestions(seed))
        results.append(result)

        # Check for rate limit error
        if 'error' in result and 'rate limit' in result['error'].lower():
            print(f"Rate limited. Backing off {backoff}s...", file=sys.stderr)
            time.sleep(backoff)
            backoff = min(backoff * 2, 8.0)  # Exponential backoff, max 8s
        else:
            # Reset backoff on success
            backoff = 1.0

        # Delay before next request (not on last item)
        if i < len(seeds) - 1:
            jitter = random.uniform(delay_seconds, delay_seconds * 2)
            print(f"Waiting {jitter:.1f}s before next request...", file=sys.stderr)
            time.sleep(jitter)

    return results


def save_to_database(suggestions_result: Dict[str, Any], db_path: Optional[str] = None) -> int:
    """
    Save autocomplete suggestions to keyword database.

    Args:
        suggestions_result: Result dict from get_autocomplete_suggestions()
        db_path: Optional database path (default: auto-detect)

    Returns:
        Count of new keywords added (0 if error or no new keywords)
    """
    if 'error' in suggestions_result:
        print(f"Cannot save: {suggestions_result['error']}", file=sys.stderr)
        return 0

    try:
        from database import KeywordDB

        db = KeywordDB(db_path)
        count = 0

        for suggestion in suggestions_result.get('suggestions', []):
            result = db.add_keyword(suggestion, source='autocomplete')
            if 'error' not in result and result.get('action') == 'inserted':
                count += 1

        db.close()
        return count

    except ImportError:
        print("ERROR: database module not found. Cannot save to database.", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"ERROR saving to database: {e}", file=sys.stderr)
        return 0


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Extract keyword suggestions from YouTube autocomplete',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python autocomplete.py "dark ages myth"
  python autocomplete.py "dark ages, crusades, colonialism"
  python autocomplete.py --seed-file seeds.txt
  python autocomplete.py "dark ages" --save
  python autocomplete.py "dark ages" --json

Rate Limiting:
  Minimum 2s delay between requests with random jitter.
  Exponential backoff on errors.
        """
    )

    parser.add_argument('seeds', nargs='?', help='Seed keyword(s) - comma-separated for batch')
    parser.add_argument('--seed-file', type=str, help='File with seed keywords (one per line)')
    parser.add_argument('--save', action='store_true', help='Save suggestions to database')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--max-suggestions', type=int, default=10, help='Max suggestions per seed (default 10)')

    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("--verbose", "-v", action="store_true", help="Show debug output on stderr")
    verbosity.add_argument("--quiet", "-q", action="store_true", help="Only show errors on stderr")

    args = parser.parse_args()

    from tools.logging_config import setup_logging
    setup_logging(args.verbose, args.quiet)

    # Check pyppeteer availability
    if not PYPPETEER_AVAILABLE:
        print("ERROR: pyppeteer not installed", file=sys.stderr)
        print("Install with: pip install pyppeteer pyppeteer-stealth", file=sys.stderr)
        sys.exit(1)

    # Determine seed keywords
    seeds = []

    if args.seed_file:
        # Read from file
        path = Path(args.seed_file)
        if not path.exists():
            print(f"ERROR: Seed file not found: {args.seed_file}", file=sys.stderr)
            sys.exit(1)

        seeds = [line.strip() for line in path.read_text().splitlines() if line.strip()]

    elif args.seeds:
        # Parse from command line (comma-separated)
        seeds = [s.strip() for s in args.seeds.split(',') if s.strip()]

    else:
        parser.print_help()
        sys.exit(1)

    if not seeds:
        print("ERROR: No seed keywords provided", file=sys.stderr)
        sys.exit(1)

    # Extract suggestions
    if len(seeds) == 1:
        # Single keyword
        result = asyncio.run(get_autocomplete_suggestions(seeds[0], args.max_suggestions))
        results = [result]
    else:
        # Batch processing
        results = extract_keywords_batch(seeds, delay_seconds=2.0)

    # Save to database if requested
    if args.save:
        total_saved = 0
        for result in results:
            saved = save_to_database(result)
            total_saved += saved

        print(f"\nSaved {total_saved} new keywords to database", file=sys.stderr)

    # Output results
    if args.json:
        if len(results) == 1:
            print(json.dumps(results[0], indent=2))
        else:
            print(json.dumps(results, indent=2))
    else:
        # Markdown output
        for result in results:
            if 'error' in result:
                print(f"\n## {result.get('keyword', 'Unknown')}\n")
                print(f"**Error:** {result['error']}")
                print(f"**Details:** {result.get('details', 'N/A')}")
            else:
                print(f"\n## {result['keyword']}\n")
                print(f"**Suggestions:** {result['count']}")
                print(f"**Fetched:** {result['fetched_at']}\n")
                for i, suggestion in enumerate(result['suggestions'], 1):
                    print(f"{i}. {suggestion}")


if __name__ == '__main__':
    main()
