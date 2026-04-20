# Cheap Flights Routine

Scans **LIM / CUZ / LPB → MAD / LHR / BRU / AMS / CDG**, one-way, departing **July 1-7, 2026**. Emails you when any offer drops under **€500** (configurable).

## What it covers

| Coverage | Source | Mode |
|----------|--------|------|
| Direct + connecting flights (cached aggregator) | Travelpayouts v3/v2/v1 — **5 endpoints** | Always |
| Self-transfer two-ticket routes via PTY / BOG / LIS hubs | Travelpayouts + composition in `check_flights.py` | Always |
| Google Flights catalogue (different cache pool) — **0-3 stops** | `fast-flights` PyPI package (protobuf) | If installed |
| **Amadeus live GDS pricing** (Sabre/Amadeus/Galileo inventory) | `amadeus` Python SDK | If credentials set |
| ~~Skyscanner live prices~~ | ~~Playwright + Chromium~~ | **Deprecated — CAPTCHA-blocked** |

Every scan emits a single unified JSON — `scan.py` merges all sources, dedupes, sorts by price.

## Files

| File | Purpose |
|------|---------|
| `scan.py` | Orchestrator — runs all scanners, merges results. Start here. |
| `check_flights.py` | Travelpayouts 5-endpoint scanner + self-transfer builder. Stdlib only. |
| `scrape_gflights.py` | Google Flights scanner via `fast-flights` (protobuf, no browser). `max_stops=3`. Graceful skip if dep missing. |
| `scrape_amadeus.py` | Amadeus Flight Offers Search — live GDS inventory. Graceful skip if SDK / credentials missing. |
| `scrape_skyscanner.py` | **Deprecated stub.** Skyscanner CAPTCHAs on first navigation — kept for contract parity. |
| `routine.md` | Daily prompt — read by Claude when the routine fires. |
| `scans/` | Daily JSON output + `_log.md` running summary. |

## One-time setup

### 1. Free Travelpayouts token (~3 min, required)

1. Sign up: https://www.travelpayouts.com/signup
2. **Tools → API → Get token** (or https://www.travelpayouts.com/programs)
3. Copy the token — no card, no cap on cached endpoint.

### 2. Free Amadeus credentials (~5 min, unlocks live pricing)

Amadeus is the backbone GDS that feeds Sabre/Galileo/Worldspan inventory — what travel agents see. Different pool from Travelpayouts cache.

1. Sign up: https://developers.amadeus.com/register
2. **My Self-Service Workspace → Create New App** — name it anything.
3. Copy the **API Key** and **API Secret**.
4. Free tier = **production mode**, 2000 Flight Offers Search calls/month (our scan = 105/day = 3150/month — slightly over, but test mode works too if you'd rather stay well under).

### 3. Python deps

```bash
# Required to unlock Amadeus coverage
pip install amadeus

# Required to unlock Google Flights coverage (~60s extra per scan)
pip install fast-flights
```

Both are optional — if missing, `scan.py` degrades to whatever is available and logs the reason in `raw.<source>.reason_missing`.

### 4. Environment variables

```bash
# Required
export TRAVELPAYOUTS_TOKEN="your_token_here"

# Optional — unlocks Amadeus source
export AMADEUS_CLIENT_ID="your_client_id"
export AMADEUS_CLIENT_SECRET="your_client_secret"
export AMADEUS_HOSTNAME="production"       # or "test" for synthetic prices

# Optional tuning
export FLIGHT_THRESHOLD_EUR=500            # default 500
export SELF_TRANSFER_MAX_GAP_DAYS=2         # leg2 depart window after leg1
export SKIP_AMADEUS=1                       # skip Amadeus (e.g. if quota hit)
```

### 5. Smoke-test

```bash
cd "D:/History vs Hype/flight-deals"
python scan.py | head -80
```

Expect `total_offers_in_window > 0`, `sources_available.travelpayouts = true`. Other sources will be `false` until you install their deps / set credentials — that's fine.

### 6. Schedule

**Option A — Local Windows Task Scheduler (recommended — all sources available):**
1. Install both Python deps (step 3).
2. Set Amadeus env vars globally.
3. Create a scheduled task running daily at ~07:13:
   ```cmd
   cd /d "D:\History vs Hype\flight-deals"
   python scan.py > "scans\%date:~-4%-%date:~3,2%-%date:~0,2%.json"
   ```
4. Claude handles the email via the `/loop` or manual routine invocation.

**Option B — Anthropic CCR RemoteTrigger (API-only, cloud):**
1. Connect Gmail at https://claude.ai/settings/connectors.
2. Commit + push `flight-deals/` to the `history-vs-hype` repo.
3. Tell Claude: *"create the flight routine via RemoteTrigger, daily at 7:13 AM, repo history-vs-hype, Gmail connector, set TRAVELPAYOUTS_TOKEN and AMADEUS_*"*.

Cloud mode keeps Travelpayouts + self-transfer + Google Flights + Amadeus. Skyscanner is deprecated in both modes.

## Tweaking

| Want to change | Edit |
|----------------|------|
| Threshold | `FLIGHT_THRESHOLD_EUR` env var |
| Self-transfer hub list | `HUBS` at top of `check_flights.py` |
| Airports / dates | `ORIGINS`, `DESTINATIONS`, `DEPART_*` at top of `check_flights.py`, `scrape_gflights.py`, `scrape_amadeus.py` |
| Max layover gap (days between leg1 and leg2) | `SELF_TRANSFER_MAX_GAP_DAYS` env var |
| Email logic | `routine.md` step 3-4 |

## Why four sources?

Each surfaces different price pools. Empirically on SA→EU:

- **Travelpayouts (5 endpoints)** catches established carrier rates — cached snapshots (minutes-to-hours stale) but the broadest aggregator pool available free.
- **Self-transfer via hubs** routinely beats direct by €100-200 on LIM→EU because SA-to-hub legs are priced locally and hub-to-EU legs are priced on a separate European market. Two cheap tickets < one expensive through-ticket.
- **Google Flights (fast-flights)** pulls from Google's own ITA data with `max_stops=3` — critical for SA→EU where direct carriers are rare. Different airline inventory pool than the aviasales cache.
- **Amadeus Flight Offers** is **live GDS pricing** — the same feed travel agents see. Catches last-minute inventory dumps and airline-direct fares that aggregator caches miss entirely.

## Why Skyscanner is dead

Skyscanner deploys PerimeterX anti-bot and serves a CAPTCHA on the very first navigation — verified 2026-04-20 via Playwright with realistic headers. Defeating it requires paid residential proxies + captcha solving (~$100/mo) or a partner API key (individuals can't get one). Amadeus replaces it as the live-pricing source.

## Why `fast-flights` instead of full Playwright for Google Flights?

Google Flights serves CAPTCHA to anything that looks like a scraper on the rendered UI. Their internal protobuf search endpoint (what `fast-flights` talks to) is CAPTCHA-free and much faster — same catalogue, no browser, routine-compatible.

## Known limitations

- `fast-flights` returns prices in the locale of the IP running it — `scrape_gflights.py` labels them `price_eur` but they may actually be USD. Use the `price_currency_raw` field to audit. A currency-normalization pass is a future improvement.
- Amadeus free tier caps at 2000 Flight Offers Search calls/month in production. Our full scan = 105 calls/day = ~3150/month. If you hit the cap, set `SKIP_AMADEUS=1` or switch to `AMADEUS_HOSTNAME=test` (synthetic prices, higher quota).
- Self-transfer uses date matching only (the cached APIs don't expose arrival times) — the `MAX_GAP_DAYS=2` buffer catches most overnight-layover compositions but may surface a few impossible same-day connections. Verify before booking.
