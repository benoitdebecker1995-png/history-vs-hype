# Cheap Flights Routine

Scans **LIM / CUZ / LPB → MAD / LHR / BRU / AMS / CDG**, one-way, departing **July 1-7, 2026**. Emails you when any offer drops under **€500**.

Uses **Travelpayouts Aviasales v3** — free, no card, instant API token. 15 API calls per day (1 per city pair, queries the whole month then filters dates locally).

## Files

| File | Purpose |
|------|---------|
| `check_flights.py` | Stdlib-only Travelpayouts client. JSON to stdout. |
| `routine.md` | Daily prompt — read by Claude when the routine fires. |
| `scans/` | Daily JSON output + `_log.md` running summary. |

## One-time setup

### 1. Get free Travelpayouts token (~3 min)

1. Sign up: https://www.travelpayouts.com/signup
2. Once logged in, go to **Tools → API → Get token** (or https://www.travelpayouts.com/programs)
3. Copy the token (no card, no approval queue, no monthly cap on this endpoint)

### 2. Set environment variable

Local run:
```bash
export TRAVELPAYOUTS_TOKEN="your_token_here"
export FLIGHT_THRESHOLD_EUR=500   # optional, default 500
```

Cloud routine: paste the token directly into the routine prompt (see `routine.md`).

### 3. Smoke-test

```bash
cd "D:/History vs Hype/flight-deals"
python check_flights.py | head -60
```

Expect JSON with `total_offers_in_window > 0`. Takes ~10 seconds. If `cheap_count == 0` that's normal — SA→EU rarely under €500 — you'll still see `top_5_overall` for sanity.

### 4. Schedule

**Option A — Cloud routine (recommended for 2-3 week run):**
1. Connect Gmail at https://claude.ai/settings/connectors
2. Commit + push `flight-deals/` to your `history-vs-hype` repo
3. Tell Claude: *"create the flight routine via RemoteTrigger, daily at 7:13 AM, repo history-vs-hype, Gmail connector"*

**Option B — Local Windows Task Scheduler:**
Run `python check_flights.py > scans/today.json` daily, then mail yourself with a separate script. More setup but no Anthropic plan limits.

## Tweaking

| Want to change | Edit |
|----------------|------|
| Threshold | `FLIGHT_THRESHOLD_EUR` env var |
| Airports / dates | Top of `check_flights.py` constants |
| Email logic | `routine.md` step 3-4 |

## Why Travelpayouts vs. Amadeus

| | Travelpayouts | Amadeus |
|---|---|---|
| Signup friction | Email only | Email + phone verify, sometimes flaky |
| Card required | No | No (test env), yes (prod) |
| Free quota | Effectively unlimited on cached endpoint | 2000/mo (test), 10/mo (prod free) |
| Data type | Cached real prices from past searches | Live availability |
| Calls per day for our scan | 15 | 105 |
| Booking link in response | Yes | No |

Travelpayouts data is cached (minutes-to-hours stale) which is fine for "alert me when a deal appears". Amadeus is live but the test environment returns synthetic prices and the production free tier is too tight.
