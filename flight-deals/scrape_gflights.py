#!/usr/bin/env python3
"""
Google Flights scraper — uses `fast-flights` in **local Playwright mode** with
forced EUR currency, then falls back to the protobuf-only `common` mode on failure.

Why the local (browser) path is default:
  - The protobuf-only `common` mode returned empty results on SA->EU routes when
    Google's edge geolocated the IP to an unusual region (we saw it hand back
    an ARS-labeled empty shell).
  - `local` drives a real Chromium session via Playwright — Google serves the
    same page a human would see, and we pass `curr=EUR` to force euro pricing
    regardless of IP locale.

Setup:
    pip install fast-flights playwright
    playwright install chromium

If either dep is missing, this script prints an empty-but-valid JSON payload and
exits 0 so `scan.py` can degrade gracefully.
"""

import json
import sys
import time
from datetime import date, timedelta

ORIGINS = ["LIM", "CUZ", "LPB"]
DESTINATIONS = ["MAD", "LHR", "BRU", "AMS", "CDG",
                "LGW", "STN", "BCN", "FCO", "LIS", "OPO", "FRA", "MUC"]
DEPART_START = date(2026, 7, 1)
DEPART_END = date(2026, 7, 9)  # user constraint: must arrive before July 10
MAX_RETRIES = 2

try:
    from fast_flights import FlightData, Passengers  # type: ignore
    from fast_flights.filter import TFSData  # type: ignore
    from fast_flights.core import get_flights_from_filter  # type: ignore
    HAS_FAST_FLIGHTS = True
except ImportError:
    HAS_FAST_FLIGHTS = False


def _fmt_links(origin: str, dest: str, depart_date: str) -> dict:
    yymmdd = depart_date.replace("-", "")[2:]
    return {
        "google_flights": (f"https://www.google.com/travel/flights?q=Flights+from+{origin}"
                           f"+to+{dest}+on+{depart_date}+one-way"),
        "skyscanner": f"https://www.skyscanner.net/transport/flights/{origin.lower()}/{dest.lower()}/{yymmdd}/",
        "kiwi": f"https://www.kiwi.com/en/search/results/{origin}/{dest}/{depart_date}/no-return",
    }


def _daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def _fetch_one(origin: str, dest: str, iso: str):
    """One call. Local Playwright primary; `common` (protobuf) fallback on hard error.

    No retry loop — 105 calls × retries would blow the 30-min budget. If local
    fails once, try protobuf; if both fail, move on.
    """
    filt = TFSData.from_interface(
        flight_data=[FlightData(date=iso, from_airport=origin, to_airport=dest, max_stops=3)],
        trip="one-way", seat="economy",
        passengers=Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0),
        max_stops=3,
    )
    last_err = None
    for mode in ("local", "common"):
        try:
            return get_flights_from_filter(filt, currency="EUR", mode=mode), None
        except Exception as e:  # noqa: BLE001
            last_err = f"[{mode}] {str(e)[:150]}"
    return None, last_err


def fetch_pair(origin: str, dest: str) -> tuple[list[dict], list[dict]]:
    deals: list[dict] = []
    errors: list[dict] = []
    for d in _daterange(DEPART_START, DEPART_END):
        iso = d.isoformat()
        result, err = _fetch_one(origin, dest, iso)
        if result is None:
            errors.append({"origin": origin, "dest": dest, "date": iso, "error": err or "unknown"})
            continue
        for flight in (result.flights or []):
            price_str = (flight.price or "").replace("$", "").replace(",", "").replace("€", "").replace("EUR", "").strip()
            try:
                price = float(price_str)
            except (ValueError, TypeError):
                continue
            if price <= 0 or not flight.name:
                continue
            deals.append({
                "origin": origin,
                "destination": dest,
                "departure_date": iso,
                "depart_time": flight.departure or iso,
                "arrive_time": flight.arrival or "",
                "price_eur": price,
                "price_currency_raw": flight.price or "",
                "airline": flight.name or "",
                "flight_number": "",
                "stops": _parse_stops(flight.stops),
                "duration_min": _parse_duration_min(flight.duration or ""),
                "source_endpoint": "gflights.fast-flights",
                "verify_links": _fmt_links(origin, dest, iso),
                "route_type": "direct" if _parse_stops(flight.stops) == 0 else "connecting",
            })
    return deals, errors


def _parse_stops(val) -> int:
    if val is None or val == "":
        return 0
    if isinstance(val, int):
        return val
    s = str(val).strip().lower()
    if s in ("nonstop", "direct", "non-stop"):
        return 0
    if s == "unknown":
        return 0
    try:
        return int(s)
    except ValueError:
        import re
        m = re.search(r"(\d+)", s)
        return int(m.group(1)) if m else 0


def _parse_duration_min(s: str) -> int:
    if not s:
        return 0
    s = s.lower().replace(",", " ")
    hours = minutes = 0
    token_acc = ""
    for ch in s:
        if ch.isdigit():
            token_acc += ch
        else:
            if token_acc and ch in "h":
                hours = int(token_acc); token_acc = ""
            elif token_acc and ch == "m":
                minutes = int(token_acc); token_acc = ""
            elif not ch.isalpha():
                token_acc = ""
    return hours * 60 + minutes


def main() -> None:
    if not HAS_FAST_FLIGHTS:
        sys.stderr.write("fast-flights not installed — skipping gflights scan.\n")
        json.dump({
            "scan_date": date.today().isoformat(),
            "source": "gflights.fast-flights",
            "available": False,
            "reason": "fast-flights package not installed (pip install fast-flights playwright && playwright install chromium)",
            "total_offers_in_window": 0,
            "all_deals": [],
            "top_5_overall": [],
            "errors": [],
        }, sys.stdout, indent=2)
        return

    all_deals: list[dict] = []
    errors: list[dict] = []
    for origin in ORIGINS:
        for dest in DESTINATIONS:
            deals, errs = fetch_pair(origin, dest)
            all_deals.extend(deals)
            errors.extend(errs)

    all_deals.sort(key=lambda x: x["price_eur"])

    json.dump({
        "scan_date": date.today().isoformat(),
        "source": "gflights.fast-flights",
        "available": True,
        "mode": "local-playwright+common-fallback",
        "currency_forced": "EUR",
        "city_pairs_scanned": len(ORIGINS) * len(DESTINATIONS),
        "total_offers_in_window": len(all_deals),
        "top_5_overall": all_deals[:5],
        "all_deals": all_deals,
        "errors": errors,
    }, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
