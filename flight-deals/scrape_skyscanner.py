#!/usr/bin/env python3
"""
Skyscanner scraper — DEPRECATED.

Skyscanner deploys PerimeterX anti-bot, which serves a CAPTCHA on the very
first navigation — even from a real Chromium session with realistic headers.
Verified 2026-04-20: load redirects to /sttc/px/captcha-v2/index.html before
any DOM renders.

Defeating it requires either (a) a paid residential-proxy service with captcha
solving, or (b) a Skyscanner partner API key (individuals cannot obtain one).
Neither fits this tool's free-and-autonomous design.

This script stays in the tree so scan.py's orchestrator contract is unchanged,
but it always emits `available: false` with the CAPTCHA explanation. If you
want Skyscanner-tier coverage, the replacement is:

    - Amadeus (scrape_amadeus.py)   — live GDS pricing, free 2000 calls/month
    - Expanded Travelpayouts endpoints (inside check_flights.py) — cached but
      covers Skyscanner-indexed fares since Travelpayouts aggregates from the
      same pool Skyscanner reads.
"""

import json
import sys
from datetime import date


def main() -> None:
    json.dump({
        "scan_date": date.today().isoformat(),
        "source": "skyscanner.playwright",
        "available": False,
        "reason": ("Skyscanner serves PerimeterX CAPTCHA on first navigation; "
                   "headless scraping is blocked. Use Amadeus instead "
                   "(scrape_amadeus.py) or expand Travelpayouts endpoints."),
        "total_offers_in_window": 0,
        "top_5_overall": [],
        "all_deals": [],
        "errors": [],
    }, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
