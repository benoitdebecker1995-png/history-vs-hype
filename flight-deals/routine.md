# Cheap Flights Daily Routine

Scheduled prompt — fires once per day. Scans LIM/CUZ/LPB → MAD/LHR/BRU/AMS/CDG one-way for July 1-7, 2026 across 3 Travelpayouts cache pools and emails benoit.debecker1995@gmail.com.

## Steps

1. Run the scanner and save today's raw output:
   ```bash
   cd "D:/History vs Hype/flight-deals"
   mkdir -p scans
   python check_flights.py > "scans/$(date +%Y-%m-%d).json"
   ```

2. Read `scans/<today>.json`. Append one summary line to `scans/_log.md`:
   `YYYY-MM-DD | offers: N | cheap: M | close: K | cheapest: €XXX (LIM→MAD 2026-07-03) | cache hits — v3:A v2:B v1:C`

3. Decide email mode from the JSON:
   - `cheap_count > 0` → **DEAL email**, subject `🛫 [N] cheap flight(s) — from €XXX`
   - `cheap_count == 0 AND close_call_count > 0` → **CLOSE-CALL email**, subject `🟡 Close call — cheapest today €XXX`
   - Both zero AND `total_offers_in_window > 0` → **DAILY-DIGEST email**, subject `📋 Daily digest — top 5 from €XXX (none under threshold)`. Send this **once per week** (only on Mondays) to avoid noise; otherwise stay silent.
   - All zero AND no offers → silent (no email). Just step 2 logged.
   - `len(errors) > 5` → also send **ERROR email**, subject `⚠️ Flight scanner errors today (K/15 pairs)`

4. Compose the email body in markdown, three sections:
   - **Top deals**: table sorted by price ascending — `Price | Route | Date | Stops | Airline | Source endpoint | Verify`
     - "Verify" cell = three short links: `[GFlights](url) · [Sky](url) · [Kiwi](url)` from each offer's `verify_links`
   - **Manual check**: bulleted list of all 15 routes with their `manual_verification_links` so you can spot-check pairs that returned no API data
   - **Diagnostics**: `cache_pool_hits` per endpoint + error count

5. Send via Gmail MCP (`mcp__claude_ai_Gmail__*`). To: `benoit.debecker1995@gmail.com`. If auth fails, write `scans/_auth-needed.md` with the date and stop — do not retry.

## Hard constraints

- MUST NOT modify `check_flights.py`
- MUST NOT change the threshold, airport list, or date window without explicit approval
- MUST NOT send more than one email per mode per day
- MUST stop after one Gmail auth failure — never retry in-loop
- MUST overwrite today's scan JSON if it already exists
- DAILY-DIGEST mode fires on Mondays only — verify `date +%u == 1` before sending

## Done when
- ✅ `scans/YYYY-MM-DD.json` exists for today
- ✅ `scans/_log.md` has today's line
- ✅ Email sent IF deals/close-calls/digest-day/errors warrant it, otherwise silent
