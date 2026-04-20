#!/usr/bin/env python3
"""
Orchestrator: runs all scanners (Travelpayouts APIs + self-transfer, Google
Flights via fast-flights, Skyscanner via Playwright), merges results, emits
a single unified scan JSON.

Each sub-scanner degrades gracefully if its deps are missing — this script
always succeeds with at least the API results (no external deps).

Output schema is a superset of check_flights.py's:
    - total_offers_in_window, cheap_deals, close_call_deals  (direct, Travelpayouts)
    - self_transfer_offers, cheap_self_transfers             (two-ticket via hubs)
    - gflights_offers, gflights_cheap                        (fast-flights)
    - skyscanner_offers, skyscanner_cheap                    (Playwright)
    - top_5_overall                                          (merged, price asc)
    - sources_available                                      (which scanners ran)

Required env: TRAVELPAYOUTS_TOKEN (check_flights requires it)
Optional env: FLIGHT_THRESHOLD_EUR (default 500), SKIP_SKYSCANNER=1 (skip Playwright path)
"""

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THRESHOLD = float(os.getenv("FLIGHT_THRESHOLD_EUR", "500"))


def _run(script: str, timeout: int = 600) -> dict:
    """Run a sub-scanner as a subprocess. Capture stdout as JSON."""
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / script)],
            capture_output=True, text=True, timeout=timeout, cwd=str(ROOT),
        )
    except subprocess.TimeoutExpired:
        return {"available": False, "reason": f"{script} timed out after {timeout}s"}
    if proc.returncode != 0:
        return {"available": False, "reason": f"{script} exited {proc.returncode}",
                "stderr": (proc.stderr or "")[:500]}
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as e:
        return {"available": False, "reason": f"{script} stdout not JSON: {e}",
                "stdout_head": (proc.stdout or "")[:500]}


def _normalize(deal: dict, fallback_source: str) -> dict:
    """Coerce a deal to the unified shape (price_eur + route_type + source_endpoint).

    Self-transfer rows don't have a top-level source_endpoint (their legs each
    have one), so use route_type to pick the right label.
    """
    if "total_price_eur" in deal:
        price = deal["total_price_eur"]
    else:
        price = deal.get("price_eur", 0)
    route_type = deal.get("route_type", "direct")
    if deal.get("source_endpoint"):
        source = deal["source_endpoint"]
    elif route_type == "self_transfer":
        source = "travelpayouts.self_transfer"
    else:
        source = fallback_source
    return {
        **deal,
        "unified_price_eur": float(price),
        "unified_source": source,
        "unified_route_type": route_type,
    }


def main() -> None:
    sources_available: dict[str, bool] = {}

    # 1. Travelpayouts APIs + self-transfer. Degrade gracefully if token missing
    # or endpoint errors — other sources may still return data.
    api_result = _run("check_flights.py")
    travelpayouts_ok = "total_offers_in_window" in api_result
    sources_available["travelpayouts"] = travelpayouts_ok
    if not travelpayouts_ok:
        sys.stderr.write(f"WARN: check_flights.py unavailable — {api_result}\n")
        api_result = {
            "available": False,
            "reason": api_result.get("reason", "check_flights.py returned no data"),
            "stderr": api_result.get("stderr", ""),
        }

    # 2. Google Flights via fast-flights. Optional. Local Playwright path can
    # take 10-15 min for 105 calls, so give it a 30-min budget.
    gflights = _run("scrape_gflights.py", timeout=1800)
    sources_available["gflights"] = bool(gflights.get("available", False))

    # 3. Skyscanner — deprecated (CAPTCHA-blocked). Left as a stub for contract parity.
    skyscanner = _run("scrape_skyscanner.py")
    sources_available["skyscanner"] = bool(skyscanner.get("available", False))

    # 4. Amadeus live GDS pricing. Optional. Skip if user sets SKIP_AMADEUS.
    if os.getenv("SKIP_AMADEUS"):
        amadeus = {"available": False, "reason": "SKIP_AMADEUS env set"}
    else:
        amadeus = _run("scrape_amadeus.py")
    sources_available["amadeus"] = bool(amadeus.get("available", False))

    # Merge all deals into a unified list, sorted by price.
    unified: list[dict] = []
    for d in api_result.get("cheap_deals", []) + api_result.get("close_call_deals", []):
        unified.append(_normalize(d, "travelpayouts.direct"))
    for d in api_result.get("top_5_overall", []):
        # top_5_overall already includes both direct + self-transfer — pick up any we missed.
        unified.append(_normalize(d, "travelpayouts.direct"))
    for d in api_result.get("cheap_self_transfers", []) + api_result.get("close_call_self_transfers", []):
        unified.append(_normalize(d, "travelpayouts.self_transfer"))
    for d in gflights.get("all_deals", []):
        unified.append(_normalize(d, "gflights.fast-flights"))
    for d in skyscanner.get("all_deals", []):
        unified.append(_normalize(d, "skyscanner.playwright"))
    for d in amadeus.get("all_deals", []):
        unified.append(_normalize(d, "amadeus.flight_offers"))

    # Dedupe by (origin, destination, departure_date, round(price), source)
    seen: dict[tuple, dict] = {}
    for d in unified:
        key = (d.get("origin"), d.get("destination"),
               d.get("departure_date", ""), round(d["unified_price_eur"]),
               d["unified_source"])
        cur = seen.get(key)
        if cur is None or d["unified_price_eur"] < cur["unified_price_eur"]:
            seen[key] = d
    unified = sorted(seen.values(), key=lambda x: x["unified_price_eur"])

    cheap_all = [d for d in unified if d["unified_price_eur"] < THRESHOLD]
    close_all = [d for d in unified
                 if THRESHOLD <= d["unified_price_eur"] < THRESHOLD + 50]

    # Per-source counts for the diagnostic block.
    source_counts: dict[str, int] = {}
    for d in unified:
        source_counts[d["unified_source"]] = source_counts.get(d["unified_source"], 0) + 1

    json.dump({
        "scan_date": date.today().isoformat(),
        "threshold_eur": THRESHOLD,
        "sources_available": sources_available,
        "source_counts": source_counts,

        # Top-level counts (routine.md reads these).
        "cheap_count": len(cheap_all),
        "close_call_count": len(close_all),
        "total_offers_in_window": len(unified),

        # Unified lists (sorted, deduped).
        "cheap_deals": cheap_all[:30],
        "close_call_deals": close_all[:10],
        "top_5_overall": unified[:5],

        # Raw per-source payloads (for deep audit / debugging).
        "raw": {
            "travelpayouts": {
                "available": travelpayouts_ok,
                "total": api_result.get("total_offers_in_window", 0),
                "self_transfers": api_result.get("self_transfer_offers", 0),
                "cache_pool_hits": api_result.get("cache_pool_hits", {}),
                "errors": api_result.get("errors", []),
                "manual_verification_links": api_result.get("manual_verification_links", []),
                "reason_missing": api_result.get("reason") if not travelpayouts_ok else None,
            },
            "gflights": {
                "available": sources_available["gflights"],
                "total": gflights.get("total_offers_in_window", 0),
                "reason_missing": gflights.get("reason"),
                "errors": gflights.get("errors", []),
            },
            "skyscanner": {
                "available": sources_available["skyscanner"],
                "total": skyscanner.get("total_offers_in_window", 0),
                "reason_missing": skyscanner.get("reason"),
                "errors": skyscanner.get("errors", []),
            },
            "amadeus": {
                "available": sources_available["amadeus"],
                "total": amadeus.get("total_offers_in_window", 0),
                "hostname": amadeus.get("hostname"),
                "reason_missing": amadeus.get("reason"),
                "errors": amadeus.get("errors", []),
            },
        },
    }, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
