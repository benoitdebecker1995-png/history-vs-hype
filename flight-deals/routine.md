# Cheap Flights Daily Routine

Scheduled prompt — fires once per day. Runs `scan.py`, which orchestrates four scanners, merges results, and drafts a Gmail to benoit.debecker1995@gmail.com.

**Scanners (graceful-degrade: missing deps = that source reports `available: false`, others still run):**
1. `check_flights.py` — Travelpayouts APIs (direct) + self-transfer via hub airports
2. `scrape_gflights.py` — Google Flights via `fast-flights` (local Playwright → `common` protobuf fallback)
3. `scrape_skyscanner.py` — stub (CAPTCHA-blocked; kept for contract parity, always emits `available: false`)
4. `scrape_amadeus.py` — Amadeus Flight Offers Search (live GDS prices; needs `AMADEUS_CLIENT_ID`/`SECRET`)

**Route coverage:**
- Origins: `LIM`, `CUZ`, `LPB`
- Direct destinations: `MAD`, `LHR`, `BRU`, `AMS`, `CDG`, `LGW`, `STN`, `BCN`, `FCO`, `LIS`, `OPO`, `FRA`, `MUC`
- Self-transfer hubs: `MIA`, `GRU`, `MEX`, `EZE`, `JFK`, `LIS` (two-ticket: origin→hub + hub→dest)
- Depart window: `2026-07-01` to `2026-07-09` inclusive (user constraint: must arrive before July 10)

---

## Execution modes

**Local-full (recommended)** — Windows Task Scheduler on user machine. Playwright + Amadeus available. Prereqs: `pip install fast-flights playwright amadeus && playwright install chromium`.

**Cloud-fallback (RemoteTrigger)** — Anthropic CCR daily cron. Playwright can't run (no Chromium), so gflights degrades to `common` protobuf mode automatically. Amadeus only runs if creds are in the trigger env; otherwise emits `available: false`. Travelpayouts always works.

---

## Steps

> **Path note:** all paths repo-relative. `TRAVELPAYOUTS_TOKEN` is exported by the caller before running. Optionally `FLIGHT_THRESHOLD_EUR` (default 500), `SKIP_AMADEUS=1`, `AMADEUS_CLIENT_ID`/`AMADEUS_CLIENT_SECRET`.

1. Run the orchestrator and save today's raw output:
   ```bash
   cd flight-deals
   mkdir -p scans
   python scan.py > "scans/$(date -u +%Y-%m-%d).json"
   ```

2. Read `scans/<today>.json`. Append one summary line to `scans/_log.md`:
   `YYYY-MM-DD | offers: N | cheap: M | close: K | cheapest: €XXX (LIM→MIA→BCN via self-transfer) | sources: tp/gf/sk/am — Y/Y/N/N`
   (Y/N reflects each `sources_available.<source>`.)

3. Decide email mode from the top-level JSON fields:
   - `cheap_count > 0` → **DEAL email**, subject `🛫 [N] cheap flight(s) — from €XXX`
   - `cheap_count == 0 AND close_call_count > 0` → **CLOSE-CALL email**, subject `🟡 Close call — cheapest today €XXX`
   - Both zero AND `total_offers_in_window > 0` AND today is Monday (`date -u +%u == 1`) → **DAILY-DIGEST email**, subject `📋 Weekly digest — top 5 from €XXX (none under threshold)`
   - Any source where `sources_available[s]` flipped from `true` yesterday to `false` today, OR `raw.travelpayouts.errors` length > 5 → **ERROR email** (may fire alongside deal/close/digest), subject `⚠️ Flight scanner diagnostics — <date>`
   - All of the above false → silent (no draft).

4. Compose the email body in markdown, four sections:
   - **Top deals**: table sorted by `unified_price_eur` ascending — `Price | Route | Date | Type | Stops | Airline | Source | Verify`
     - `Type` = `direct` or `self-transfer (via HUB)`
     - For self-transfer rows, `Route` reads `LIM→MIA→BCN`, `Price` is the total (leg1 + leg2), `Verify` gets two link-sets: one for each leg
     - For direct rows, `Verify` cell = three short links: `[GFlights](url) · [Sky](url) · [Kiwi](url)` from `verify_links`
     - Show at most 15 rows (cheap deals first, then close-calls if space)
   - **Source breakdown**: one line summarising `source_counts` — e.g. `Travelpayouts direct: 16 · Self-transfer: 12 · Google Flights: 30 · Amadeus: 8`
   - **Manual check**: bulleted list of `raw.travelpayouts.manual_verification_links` so the user can spot-check pairs that returned no API data
   - **Diagnostics**: `raw.travelpayouts.cache_pool_hits` summary + per-source error counts + any `sources_available=false` with its `reason_missing`

5. Create a Gmail draft via `mcp__Gmail__create_draft`. To: `benoit.debecker1995@gmail.com`. Subject per step 3. Body is the markdown from step 4. If the draft tool fails, write `scans/_draft-failed-YYYY-MM-DD.md` with the error and stop — do not retry. User reviews the draft in Gmail and sends manually.

6. Final stdout line (for log visibility in the trigger history):
   `<YYYY-MM-DD> | mode: <DEAL|CLOSE|DIGEST|SILENT|ERROR> | offers: N | cheap: M | cheapest: €XXX <origin>→<dest>`

---

## Hard constraints

- MUST create a DRAFT, never auto-send — user reviews in Gmail before sending
- MUST NOT modify `check_flights.py`, `scan.py`, `scrape_*.py`, `README.md`, or any file outside `scans/` during a routine run
- MUST NOT change the threshold, airport list, hub list, or date window without explicit approval (edit the top of `check_flights.py` if you do)
- MUST NOT send more than one email per mode per day (DEAL + ERROR may both fire; DEAL + CLOSE cannot)
- MUST stop after one Gmail draft failure — never retry in-loop
- MUST overwrite today's scan JSON if it already exists (re-runs are idempotent)
- MUST run `python scan.py`, not `python check_flights.py` directly — scan.py is the unified entry point
- DAILY-DIGEST fires on Mondays only (`date -u +%u == 1`)
- SILENT mode = exit cleanly with no draft, no `_log.md` entry beyond the summary line

## Done when

- ✅ `scans/YYYY-MM-DD.json` exists for today with `sources_available` populated
- ✅ `scans/_log.md` has today's line
- ✅ Gmail draft created IF deal/close-call/digest-Monday/error conditions warrant it — otherwise silent
- ✅ Summary line printed to stdout
