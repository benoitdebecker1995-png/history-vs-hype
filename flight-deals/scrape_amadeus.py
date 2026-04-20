#!/usr/bin/env python3
"""
Amadeus Flight Offers Search — uses the official amadeus-python SDK to hit the
Amadeus Self-Service Flight Offers Search endpoint.

Key difference from Travelpayouts: Amadeus returns live GDS-sourced prices
(Sabre/Amadeus/Galileo inventory), not cached aggregator snapshots. Catches
deals the Travelpayouts cache doesn't see — particularly last-minute inventory
dumps and airline-direct pricing.

Free tier: 2000 Flight Offers Search calls/month (test env) with synthetic
prices, or get an API key via https://developers.amadeus.com/self-service and
use production env (real prices, free quota is tighter but sufficient for
15 city pairs × 7 days = 105 calls/day).

Required env vars:
    AMADEUS_CLIENT_ID      — from developers.amadeus.com
    AMADEUS_CLIENT_SECRET  — from developers.amadeus.com
    AMADEUS_HOSTNAME       — optional, "test" or "production" (default: production)

If the SDK isn't installed or credentials are missing, emits a graceful empty
payload with a reason_missing so scan.py can degrade.

Setup:
    pip install amadeus
    # Register at developers.amadeus.com, create an app, copy the keys:
    export AMADEUS_CLIENT_ID="..."
    export AMADEUS_CLIENT_SECRET="..."
"""

import json
import os
import sys
from datetime import date

ORIGINS = ["LIM", "CUZ", "LPB"]
DESTINATIONS = ["MAD", "LHR", "BRU", "AMS", "CDG"]
DEPART_START_ISO = "2026-07-01"
DEPART_END_ISO = "2026-07-07"
MAX_OFFERS_PER_PAIR = 5
NON_STOP_ONLY = False  # SA->EU routes rarely have direct service

try:
    from amadeus import Client, ResponseError  # type: ignore
    HAS_AMADEUS = True
except ImportError:
    HAS_AMADEUS = False


def _fmt_links(origin: str, dest: str, depart_date: str) -> dict:
    yymmdd = depart_date.replace("-", "")[2:]
    return {
        "google_flights": (f"https://www.google.com/travel/flights?q=Flights+from+{origin}"
                           f"+to+{dest}+on+{depart_date}+one-way"),
        "skyscanner": f"https://www.skyscanner.net/transport/flights/{origin.lower()}/{dest.lower()}/{yymmdd}/",
        "kiwi": f"https://www.kiwi.com/en/search/results/{origin}/{dest}/{depart_date}/no-return",
    }


def _stop_count(itinerary: dict) -> int:
    """Amadeus itinerary -> number of stops = segments - 1."""
    return max(0, len(itinerary.get("segments", [])) - 1)


def _primary_airline(itinerary: dict) -> str:
    segs = itinerary.get("segments", [])
    return segs[0].get("carrierCode", "") if segs else ""


def _duration_iso_to_min(iso: str) -> int:
    """Parse ISO 8601 duration (PT12H35M) -> int minutes."""
    if not iso or not iso.startswith("PT"):
        return 0
    hours = minutes = 0
    acc = ""
    for ch in iso[2:]:
        if ch.isdigit():
            acc += ch
        elif ch == "H":
            hours = int(acc or 0); acc = ""
        elif ch == "M":
            minutes = int(acc or 0); acc = ""
    return hours * 60 + minutes


def fetch_pair(amadeus, origin: str, dest: str, depart: str) -> tuple[list[dict], str | None]:
    try:
        resp = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=dest,
            departureDate=depart,
            adults=1,
            currencyCode="EUR",
            max=MAX_OFFERS_PER_PAIR,
            nonStop="true" if NON_STOP_ONLY else "false",
        )
    except Exception as e:  # noqa: BLE001
        return [], str(e)[:200]

    deals: list[dict] = []
    for offer in (resp.data or []):
        # One-way = single itinerary per offer.
        itins = offer.get("itineraries", [])
        if not itins:
            continue
        itin = itins[0]
        price = float(offer.get("price", {}).get("grandTotal", 0))
        if price <= 0:
            continue
        deals.append({
            "origin": origin,
            "destination": dest,
            "departure_date": depart,
            "depart_time": (itin.get("segments", [{}])[0].get("departure", {}).get("at", "") or ""),
            "arrive_time": (itin.get("segments", [{}])[-1].get("arrival", {}).get("at", "") or ""),
            "price_eur": price,
            "airline": _primary_airline(itin),
            "flight_number": "",
            "stops": _stop_count(itin),
            "duration_min": _duration_iso_to_min(itin.get("duration", "")),
            "source_endpoint": "amadeus.flight_offers",
            "verify_links": _fmt_links(origin, dest, depart),
            "route_type": "direct" if _stop_count(itin) == 0 else "connecting",
        })
    return deals, None


def main() -> None:
    if not HAS_AMADEUS:
        json.dump({
            "scan_date": date.today().isoformat(),
            "source": "amadeus.flight_offers",
            "available": False,
            "reason": "amadeus SDK not installed — run: pip install amadeus",
            "total_offers_in_window": 0,
            "top_5_overall": [], "all_deals": [], "errors": [],
        }, sys.stdout, indent=2)
        return

    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
    if not client_id or not client_secret:
        json.dump({
            "scan_date": date.today().isoformat(),
            "source": "amadeus.flight_offers",
            "available": False,
            "reason": "AMADEUS_CLIENT_ID/SECRET env vars not set — get them free at developers.amadeus.com",
            "total_offers_in_window": 0,
            "top_5_overall": [], "all_deals": [], "errors": [],
        }, sys.stdout, indent=2)
        return

    amadeus = Client(
        client_id=client_id,
        client_secret=client_secret,
        hostname=os.getenv("AMADEUS_HOSTNAME", "production"),
    )

    # Iterate every depart date in the window (Amadeus requires a specific date).
    from datetime import timedelta
    dates: list[str] = []
    d = date.fromisoformat(DEPART_START_ISO)
    end = date.fromisoformat(DEPART_END_ISO)
    while d <= end:
        dates.append(d.isoformat())
        d += timedelta(days=1)

    all_deals: list[dict] = []
    errors: list[dict] = []
    for origin in ORIGINS:
        for dest in DESTINATIONS:
            for depart in dates:
                deals, err = fetch_pair(amadeus, origin, dest, depart)
                all_deals.extend(deals)
                if err:
                    errors.append({"origin": origin, "dest": dest, "date": depart, "error": err})

    all_deals.sort(key=lambda x: x["price_eur"])

    json.dump({
        "scan_date": date.today().isoformat(),
        "source": "amadeus.flight_offers",
        "available": True,
        "hostname": os.getenv("AMADEUS_HOSTNAME", "production"),
        "city_pairs_scanned": len(ORIGINS) * len(DESTINATIONS) * len(dates),
        "total_offers_in_window": len(all_deals),
        "top_5_overall": all_deals[:5],
        "all_deals": all_deals,
        "errors": errors,
    }, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
