#!/usr/bin/env python3
"""
Cheap-flight scanner: LIM/CUZ/LPB -> MAD/LHR/BRU/AMS/CDG, depart July 1-7, 2026.

Queries THREE Travelpayouts endpoints per city pair (different cache pools)
and merges deduped results. Also generates Google Flights / Skyscanner / Kiwi
deep links per route so you can verify any deal in one click. Stdlib only.

Endpoints used:
  - aviasales/v3/prices_for_dates    (sorted by price, by date)
  - v2/prices/latest                  (latest cached, broader pool)
  - v1/prices/calendar                (per-day calendar prices)

Required env vars:
  TRAVELPAYOUTS_TOKEN     — get free at https://www.travelpayouts.com/programs
Optional:
  FLIGHT_THRESHOLD_EUR    — default 500
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date

ORIGINS = ["LIM", "CUZ", "LPB"]
DESTINATIONS = ["MAD", "LHR", "BRU", "AMS", "CDG"]
DEPART_MONTH = "2026-07"
DEPART_START = date(2026, 7, 1)
DEPART_END = date(2026, 7, 7)
CURRENCY = "eur"
THRESHOLD = float(os.getenv("FLIGHT_THRESHOLD_EUR", "500"))

TOKEN = os.environ.get("TRAVELPAYOUTS_TOKEN")
if not TOKEN:
    sys.stderr.write("ERROR: set TRAVELPAYOUTS_TOKEN (free at travelpayouts.com)\n")
    sys.exit(2)

V3_PRICES_FOR_DATES = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
V2_LATEST = "https://api.travelpayouts.com/v2/prices/latest"
V1_CALENDAR = "https://api.travelpayouts.com/v1/prices/calendar"


def http_get(url: str, retry: int = 0) -> dict:
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=45) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code == 429 and retry < 3:
            time.sleep(2 ** retry)
            return http_get(url, retry + 1)
        if e.code in (400, 404):
            return {}
        raise


def fetch_v3_prices_for_dates(origin: str, dest: str) -> list[dict]:
    qs = urllib.parse.urlencode({
        "origin": origin, "destination": dest,
        "departure_at": DEPART_MONTH, "currency": CURRENCY,
        "sorting": "price", "direct": "false", "limit": 30,
        "page": 1, "one_way": "true", "token": TOKEN,
    })
    payload = http_get(f"{V3_PRICES_FOR_DATES}?{qs}")
    rows = payload.get("data", []) if payload.get("success", True) else []
    return [{
        "depart_date": (r.get("departure_at") or "")[:10],
        "depart_time": r.get("departure_at") or "",
        "price": float(r.get("price", 0)),
        "airline": r.get("airline", ""),
        "flight_number": str(r.get("flight_number", "")),
        "stops": int(r.get("transfers", 0)),
        "duration_min": int(r.get("duration", 0)),
        "source": "v3.prices_for_dates",
    } for r in rows]


def fetch_v2_latest(origin: str, dest: str) -> list[dict]:
    qs = urllib.parse.urlencode({
        "currency": CURRENCY, "period_type": "month",
        "origin": origin, "destination": dest,
        "one_way": "true", "limit": 30, "page": 1,
        "show_to_affiliates": "true", "sorting": "price",
        "token": TOKEN,
    })
    payload = http_get(f"{V2_LATEST}?{qs}")
    rows = payload.get("data", []) if payload.get("success", True) else []
    return [{
        "depart_date": r.get("depart_date", ""),
        "depart_time": r.get("depart_date", ""),
        "price": float(r.get("value", 0)),
        "airline": r.get("gate", ""),  # v2 uses "gate" for airline
        "flight_number": str(r.get("number_of_changes", "")),
        "stops": int(r.get("number_of_changes", 0)),
        "duration_min": 0,
        "source": "v2.prices_latest",
    } for r in rows if r.get("depart_date")]


def fetch_v1_calendar(origin: str, dest: str) -> list[dict]:
    qs = urllib.parse.urlencode({
        "depart_date": DEPART_MONTH, "origin": origin, "destination": dest,
        "calendar_type": "departure_date", "currency": CURRENCY,
        "token": TOKEN,
    })
    payload = http_get(f"{V1_CALENDAR}?{qs}")
    raw = payload.get("data", {}) if payload.get("success", True) else {}
    out = []
    for depart_date, item in (raw or {}).items():
        if not isinstance(item, dict):
            continue
        out.append({
            "depart_date": depart_date,
            "depart_time": depart_date,
            "price": float(item.get("price", 0)),
            "airline": item.get("airline", ""),
            "flight_number": str(item.get("flight_number", "")),
            "stops": int(item.get("transfers", 0)),
            "duration_min": 0,
            "source": "v1.calendar",
        })
    return out


def in_window(depart_date: str) -> bool:
    try:
        d = date.fromisoformat(depart_date[:10])
    except ValueError:
        return False
    return DEPART_START <= d <= DEPART_END


def make_links(origin: str, dest: str, depart_date: str = "") -> dict:
    """Generate verification deep links — no scraping, just URLs."""
    if depart_date:
        gflights = (f"https://www.google.com/travel/flights?q=Flights+from+{origin}"
                    f"+to+{dest}+on+{depart_date}+one-way")
        yymmdd = depart_date.replace("-", "")[2:]
        skyscanner = (f"https://www.skyscanner.net/transport/flights/"
                      f"{origin.lower()}/{dest.lower()}/{yymmdd}/")
        kiwi = (f"https://www.kiwi.com/en/search/results/{origin}/{dest}/"
                f"{depart_date}/no-return")
    else:
        # whole-window verification (no specific date)
        gflights = (f"https://www.google.com/travel/flights?q=Flights+from+{origin}"
                    f"+to+{dest}+in+July+2026+one-way")
        skyscanner = (f"https://www.skyscanner.net/transport/flights/"
                      f"{origin.lower()}/{dest.lower()}/260701/")
        kiwi = (f"https://www.kiwi.com/en/search/results/{origin}/{dest}/"
                f"2026-07-01_2026-07-07/no-return")
    return {"google_flights": gflights, "skyscanner": skyscanner, "kiwi": kiwi}


def merge_dedupe(buckets: list[list[dict]]) -> list[dict]:
    seen: dict[tuple, dict] = {}
    for bucket in buckets:
        for r in bucket:
            if not in_window(r["depart_date"]):
                continue
            key = (r["depart_date"], r["airline"], r["flight_number"], round(r["price"]))
            existing = seen.get(key)
            # keep cheapest if price differs slightly between sources
            if existing is None or r["price"] < existing["price"]:
                seen[key] = r
    return list(seen.values())


def main() -> None:
    all_deals: list[dict] = []
    errors: list[dict] = []
    per_pair_links: list[dict] = []
    cache_pool_hits = {"v3.prices_for_dates": 0, "v2.prices_latest": 0, "v1.calendar": 0}

    for origin in ORIGINS:
        for dest in DESTINATIONS:
            try:
                buckets = [
                    fetch_v3_prices_for_dates(origin, dest),
                    fetch_v2_latest(origin, dest),
                    fetch_v1_calendar(origin, dest),
                ]
                for src, bucket in zip(cache_pool_hits.keys(), buckets):
                    cache_pool_hits[src] += sum(1 for r in bucket if in_window(r["depart_date"]))

                merged = merge_dedupe(buckets)
                for r in merged:
                    deal = {
                        "origin": origin, "destination": dest,
                        "departure_date": r["depart_date"],
                        "depart_time": r["depart_time"],
                        "price_eur": r["price"],
                        "airline": r["airline"],
                        "flight_number": f"{r['airline']}{r['flight_number']}",
                        "stops": r["stops"],
                        "duration_min": r["duration_min"],
                        "source_endpoint": r["source"],
                        "verify_links": make_links(origin, dest, r["depart_date"]),
                    }
                    all_deals.append(deal)
                per_pair_links.append({
                    "route": f"{origin}->{dest}",
                    "links": make_links(origin, dest),
                })
                time.sleep(0.4)
            except Exception as e:  # noqa: BLE001
                errors.append({"origin": origin, "dest": dest, "error": str(e)})

    all_deals.sort(key=lambda x: x["price_eur"])
    cheap = [d for d in all_deals if d["price_eur"] < THRESHOLD]
    close_call = [d for d in all_deals if THRESHOLD <= d["price_eur"] < THRESHOLD + 50]

    json.dump({
        "scan_date": date.today().isoformat(),
        "threshold_eur": THRESHOLD,
        "currency": CURRENCY.upper(),
        "source": "travelpayouts.multi-endpoint",
        "city_pairs_scanned": len(ORIGINS) * len(DESTINATIONS),
        "cache_pool_hits": cache_pool_hits,
        "total_offers_in_window": len(all_deals),
        "cheap_count": len(cheap),
        "cheap_deals": cheap,
        "close_call_count": len(close_call),
        "close_call_deals": close_call[:10],
        "top_5_overall": all_deals[:5],
        "manual_verification_links": per_pair_links,
        "errors": errors,
    }, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
