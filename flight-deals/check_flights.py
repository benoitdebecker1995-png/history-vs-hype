#!/usr/bin/env python3
"""
Cheap-flight scanner: LIM/CUZ/LPB -> MAD/LHR/BRU/AMS/CDG, depart July 1-7, 2026.

Queries THREE Travelpayouts endpoints per city pair (different cache pools)
and merges deduped results.

Also constructs SELF-TRANSFER (two-ticket) connecting routes through hubs
PTY / BOG / LIS — combines cheapest leg1 (origin->hub) with cheapest leg2
(hub->dest) where leg2 departs 0-2 days after leg1. This routinely beats
direct and single-ticket-with-stops prices on SA->EU routes.

Stdlib only.

Endpoints used:
  - aviasales/v3/prices_for_dates    (sorted by price, by date)
  - v2/prices/latest                  (latest cached, broader pool)
  - v1/prices/calendar                (per-day calendar prices)

Required env vars:
  TRAVELPAYOUTS_TOKEN     — get free at https://www.travelpayouts.com/programs
Optional:
  FLIGHT_THRESHOLD_EUR    — default 500
  SELF_TRANSFER_MAX_GAP_DAYS — default 2 (leg2 depart can be 0-N days after leg1)
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta

ORIGINS = ["LIM", "CUZ", "LPB"]
# Primary destinations + alt EU entry points. Cheap LCC entries (LGW/STN/BCN/FCO/
# LIS/OPO/FRA/MUC) often undercut the big 5 by €50-100; user can hop onwards by
# rail or budget carrier. All are within SA<->EU legacy carrier routes.
DESTINATIONS = ["MAD", "LHR", "BRU", "AMS", "CDG",
                "LGW", "STN", "BCN", "FCO", "LIS", "OPO", "FRA", "MUC"]
# Hubs where Travelpayouts cache has both leg1 (SA->hub) and leg2 (hub->EU) coverage.
# PTY/BOG removed — zero leg1 coverage from LIM/CUZ/LPB in 2026-07 cache.
# MIA/GRU/MEX/EZE/JFK have live leg1 data; LIS added for leg2 variety (cheap EU terminal).
HUBS = ["MIA", "GRU", "MEX", "EZE", "JFK", "LIS"]
DEPART_MONTH = "2026-07"
DEPART_START = date(2026, 7, 1)
DEPART_END = date(2026, 7, 9)  # user constraint: must arrive before July 10
CURRENCY = "eur"
THRESHOLD = float(os.getenv("FLIGHT_THRESHOLD_EUR", "500"))
MAX_GAP_DAYS = int(os.getenv("SELF_TRANSFER_MAX_GAP_DAYS", "2"))
# leg2 (hub->dest) allowed to depart up to MAX_GAP_DAYS after leg1.
LEG2_END = DEPART_END + timedelta(days=MAX_GAP_DAYS)

TOKEN = os.environ.get("TRAVELPAYOUTS_TOKEN")
if not TOKEN:
    sys.stderr.write("ERROR: set TRAVELPAYOUTS_TOKEN (free at travelpayouts.com)\n")
    sys.exit(2)

V3_PRICES_FOR_DATES = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
V3_GROUPED_PRICES = "https://api.travelpayouts.com/aviasales/v3/grouped_prices"
V2_LATEST = "https://api.travelpayouts.com/v2/prices/latest"
V1_CALENDAR = "https://api.travelpayouts.com/v1/prices/calendar"
V1_CHEAP = "https://api.travelpayouts.com/v1/prices/cheap"


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
        "airline": r.get("gate", ""),  # v2 uses "gate" for airline code
        "flight_number": "",
        "stops": int(r.get("number_of_changes", 0)),
        "duration_min": 0,
        "source": "v2.prices_latest",
    } for r in rows if r.get("depart_date")]


def fetch_v1_cheap(origin: str, dest: str) -> list[dict]:
    """Travelpayouts v1/prices/cheap — cheapest flights, different cache pool."""
    qs = urllib.parse.urlencode({
        "origin": origin, "destination": dest,
        "depart_date": DEPART_MONTH, "currency": CURRENCY,
        "token": TOKEN,
    })
    payload = http_get(f"{V1_CHEAP}?{qs}")
    raw = payload.get("data", {}) if payload.get("success", True) else {}
    # Schema: data -> dest_code -> variant_index -> {price, airline, ...}
    out = []
    for _dest_code, variants in (raw or {}).items():
        if not isinstance(variants, dict):
            continue
        for _idx, item in variants.items():
            if not isinstance(item, dict):
                continue
            depart_at = item.get("departure_at", "")
            out.append({
                "depart_date": depart_at[:10],
                "depart_time": depart_at,
                "price": float(item.get("price", 0)),
                "airline": item.get("airline", ""),
                "flight_number": str(item.get("flight_number", "")),
                "stops": 0,  # v1 cheap endpoint doesn't expose transfers
                "duration_min": 0,
                "source": "v1.cheap",
            })
    return out


def fetch_v3_grouped(origin: str, dest: str) -> list[dict]:
    """Travelpayouts v3/grouped_prices grouped by departure_at."""
    qs = urllib.parse.urlencode({
        "origin": origin, "destination": dest,
        "departure_at": DEPART_MONTH, "currency": CURRENCY,
        "group_by": "departure_at", "token": TOKEN,
    })
    payload = http_get(f"{V3_GROUPED_PRICES}?{qs}")
    raw = payload.get("data", {}) if payload.get("success", True) else {}
    out = []
    for depart_key, item in (raw or {}).items():
        if not isinstance(item, dict):
            continue
        out.append({
            "depart_date": (item.get("departure_at") or depart_key)[:10],
            "depart_time": item.get("departure_at", depart_key),
            "price": float(item.get("price", 0)),
            "airline": item.get("airline", ""),
            "flight_number": str(item.get("flight_number", "")),
            "stops": int(item.get("transfers", 0)),
            "duration_min": int(item.get("duration", 0)),
            "source": "v3.grouped_prices",
        })
    return out


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


def in_window(depart_date: str, start: date = DEPART_START, end: date = DEPART_END) -> bool:
    try:
        d = date.fromisoformat(depart_date[:10])
    except ValueError:
        return False
    return start <= d <= end


def make_links(origin: str, dest: str, depart_date: str = "") -> dict:
    if depart_date:
        gflights = (f"https://www.google.com/travel/flights?q=Flights+from+{origin}"
                    f"+to+{dest}+on+{depart_date}+one-way")
        yymmdd = depart_date.replace("-", "")[2:]
        skyscanner = (f"https://www.skyscanner.net/transport/flights/"
                      f"{origin.lower()}/{dest.lower()}/{yymmdd}/")
        kiwi = (f"https://www.kiwi.com/en/search/results/{origin}/{dest}/"
                f"{depart_date}/no-return")
    else:
        gflights = (f"https://www.google.com/travel/flights?q=Flights+from+{origin}"
                    f"+to+{dest}+in+July+2026+one-way")
        skyscanner = (f"https://www.skyscanner.net/transport/flights/"
                      f"{origin.lower()}/{dest.lower()}/260701/")
        kiwi = (f"https://www.kiwi.com/en/search/results/{origin}/{dest}/"
                f"2026-07-01_2026-07-07/no-return")
    return {"google_flights": gflights, "skyscanner": skyscanner, "kiwi": kiwi}


def merge_dedupe(buckets: list[list[dict]], start: date, end: date) -> list[dict]:
    seen: dict[tuple, dict] = {}
    for bucket in buckets:
        for r in bucket:
            if not in_window(r["depart_date"], start, end):
                continue
            key = (r["depart_date"], r["airline"], r["flight_number"], round(r["price"]))
            existing = seen.get(key)
            if existing is None or r["price"] < existing["price"]:
                seen[key] = r
    return list(seen.values())


def scan_pair(origin: str, dest: str, leg2: bool = False) -> tuple[list[dict], dict]:
    """Scan a city pair across all 5 endpoints, return merged deals + per-endpoint hit counts."""
    hits = {
        "v3.prices_for_dates": 0, "v3.grouped_prices": 0,
        "v2.prices_latest": 0, "v1.calendar": 0, "v1.cheap": 0,
    }
    start, end = (DEPART_START, LEG2_END) if leg2 else (DEPART_START, DEPART_END)
    buckets = [
        fetch_v3_prices_for_dates(origin, dest),
        fetch_v3_grouped(origin, dest),
        fetch_v2_latest(origin, dest),
        fetch_v1_calendar(origin, dest),
        fetch_v1_cheap(origin, dest),
    ]
    for src, bucket in zip(hits.keys(), buckets):
        hits[src] = sum(1 for r in bucket if in_window(r["depart_date"], start, end))
    return merge_dedupe(buckets, start, end), hits


def build_self_transfers(pair_deals: dict[tuple, list[dict]]) -> list[dict]:
    """Combine origin->hub + hub->dest tickets. Returns sorted list of multi-leg offers.

    Uses only date matching (cached APIs don't expose arrival times).
    leg2 depart must fall in [leg1_depart, leg1_depart + MAX_GAP_DAYS].
    """
    out: list[dict] = []
    for origin in ORIGINS:
        for dest in DESTINATIONS:
            for hub in HUBS:
                if hub in (origin, dest):
                    continue
                leg1s = pair_deals.get((origin, hub), [])
                leg2s = pair_deals.get((hub, dest), [])
                if not leg1s or not leg2s:
                    continue
                # Index leg2 by date for fast lookup.
                leg2_by_date: dict[date, dict] = {}
                for l2 in leg2s:
                    try:
                        d = date.fromisoformat(l2["depart_date"][:10])
                    except ValueError:
                        continue
                    cur = leg2_by_date.get(d)
                    if cur is None or l2["price"] < cur["price"]:
                        leg2_by_date[d] = l2
                # For each leg1 date in the core window, find cheapest valid leg2.
                for l1 in leg1s:
                    try:
                        l1_date = date.fromisoformat(l1["depart_date"][:10])
                    except ValueError:
                        continue
                    if not (DEPART_START <= l1_date <= DEPART_END):
                        continue
                    candidates = []
                    for offset in range(MAX_GAP_DAYS + 1):
                        l2 = leg2_by_date.get(l1_date + timedelta(days=offset))
                        if l2:
                            candidates.append(l2)
                    if not candidates:
                        continue
                    cheapest_l2 = min(candidates, key=lambda x: x["price"])
                    total = l1["price"] + cheapest_l2["price"]
                    out.append({
                        "origin": origin,
                        "destination": dest,
                        "hub": hub,
                        "departure_date": l1["depart_date"],
                        "arrive_hub_date": l1["depart_date"],
                        "leg2_date": cheapest_l2["depart_date"],
                        "total_price_eur": round(total, 2),
                        "leg1": {
                            "route": f"{origin}->{hub}",
                            "price_eur": l1["price"],
                            "airline": l1["airline"],
                            "stops": l1["stops"],
                            "source_endpoint": l1["source"],
                        },
                        "leg2": {
                            "route": f"{hub}->{dest}",
                            "price_eur": cheapest_l2["price"],
                            "airline": cheapest_l2["airline"],
                            "stops": cheapest_l2["stops"],
                            "source_endpoint": cheapest_l2["source"],
                        },
                        "verify_links": {
                            "leg1": make_links(origin, hub, l1["depart_date"]),
                            "leg2": make_links(hub, dest, cheapest_l2["depart_date"]),
                        },
                        "route_type": "self_transfer",
                    })
    out.sort(key=lambda x: x["total_price_eur"])
    # Dedupe: keep cheapest per (origin, dest, depart_date).
    seen: dict[tuple, dict] = {}
    for r in out:
        key = (r["origin"], r["destination"], r["departure_date"])
        cur = seen.get(key)
        if cur is None or r["total_price_eur"] < cur["total_price_eur"]:
            seen[key] = r
    return sorted(seen.values(), key=lambda x: x["total_price_eur"])


def main() -> None:
    # Step 1: scan direct pairs (origin -> dest) and hub legs (origin -> hub, hub -> dest).
    pair_deals: dict[tuple, list[dict]] = {}
    cache_pool_hits = {
        "v3.prices_for_dates": 0, "v3.grouped_prices": 0,
        "v2.prices_latest": 0, "v1.calendar": 0, "v1.cheap": 0,
    }
    errors: list[dict] = []
    per_pair_links: list[dict] = []

    # Direct pairs.
    direct_pairs = [(o, d) for o in ORIGINS for d in DESTINATIONS]
    # Self-transfer legs.
    leg1_pairs = [(o, h) for o in ORIGINS for h in HUBS if h not in ORIGINS]
    leg2_pairs = [(h, d) for h in HUBS for d in DESTINATIONS if h not in DESTINATIONS]

    all_pairs = [(p, False) for p in direct_pairs] + \
                [(p, True) for p in leg1_pairs + leg2_pairs]

    for (origin, dest), is_leg2 in all_pairs:
        try:
            merged, hits = scan_pair(origin, dest, leg2=is_leg2)
            pair_deals[(origin, dest)] = merged
            for k, v in hits.items():
                cache_pool_hits[k] += v
            # Manual-verify links only for direct pairs.
            if (origin, dest) in direct_pairs:
                per_pair_links.append({
                    "route": f"{origin}->{dest}",
                    "links": make_links(origin, dest),
                })
            time.sleep(0.4)
        except Exception as e:  # noqa: BLE001
            errors.append({"origin": origin, "dest": dest, "error": str(e)})

    # Step 2: build direct deal list (existing behavior).
    direct_deals: list[dict] = []
    for (origin, dest) in direct_pairs:
        for r in pair_deals.get((origin, dest), []):
            direct_deals.append({
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
                "route_type": "direct",
            })
    direct_deals.sort(key=lambda x: x["price_eur"])

    # Step 3: build self-transfer deals.
    self_transfers = build_self_transfers(pair_deals)

    # Step 4: classify.
    cheap_direct = [d for d in direct_deals if d["price_eur"] < THRESHOLD]
    close_direct = [d for d in direct_deals if THRESHOLD <= d["price_eur"] < THRESHOLD + 50]
    cheap_self = [d for d in self_transfers if d["total_price_eur"] < THRESHOLD]
    close_self = [d for d in self_transfers
                  if THRESHOLD <= d["total_price_eur"] < THRESHOLD + 50]

    # Unified best-of list: merge direct + self-transfer on comparable price key.
    unified = [{"price_eur": d["price_eur"], **d} for d in direct_deals] + \
              [{"price_eur": d["total_price_eur"], **d} for d in self_transfers]
    unified.sort(key=lambda x: x["price_eur"])

    json.dump({
        "scan_date": date.today().isoformat(),
        "threshold_eur": THRESHOLD,
        "currency": CURRENCY.upper(),
        "source": "travelpayouts.multi-endpoint+self-transfer",
        "hubs_scanned": HUBS,
        "city_pairs_scanned": len(all_pairs),
        "cache_pool_hits": cache_pool_hits,
        "total_offers_in_window": len(direct_deals),
        "self_transfer_offers": len(self_transfers),
        "cheap_count": len(cheap_direct) + len(cheap_self),
        "cheap_deals": cheap_direct,
        "cheap_self_transfers": cheap_self,
        "close_call_count": len(close_direct) + len(close_self),
        "close_call_deals": close_direct[:10],
        "close_call_self_transfers": close_self[:10],
        "top_5_overall": unified[:5],
        "manual_verification_links": per_pair_links,
        "errors": errors,
    }, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
