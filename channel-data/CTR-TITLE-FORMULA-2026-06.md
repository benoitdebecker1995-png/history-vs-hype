# CTR Title Formula — derived from real Studio data (2026-06-27)

**Status:** evidence-derived from the channel's own impressions+CTR (n=56). CTR is the
VERIFIED #1 lever (views↔CTR r=0.62; views↔retention r=0.07). Median title CTR = 2.51%
(weak; healthy = 4–6%). Titles are A/B-testable — treat this as a FILTER (necessary
conditions), learn the rest via single-variable native swaps. See
`channel-data/FLOP-AUTOPSY-PLAN-2026-06.md` for the full funnel autopsy.

---

## The natural experiment that proves the formula

Same famous name, 6× the CTR — only the predicate changed:

| CTR | title |
|---:|---|
| **9.37%** | JD Vance Claims Christians Found **Child Sacrifice** |
| **1.48%** | JD Vance vs History: **Who Invented Human Rights?** |

Fame got both into the impression pool. The **predicate** won or lost the click.

## ⚠️ FULL-DATA RECALIBRATION (2026-06-27, all 56 videos)

This doc was first drafted from the 12 CTR-extreme videos. Re-tested across ALL 56 with the
real Studio CTR, two of the original axes DID NOT generalize — recorded here for honesty:

| axis | full-data median CTR delta | verdict |
|---|---:|---|
| **FAMOUS subject** | **+0.87** (n=31) | ROBUST — survives stratification by colon. THE lever. |
| evidence-promise | +1.02 (n=8) | holds |
| controversy/myth frame | +0.68 (n=17) | holds |
| "visceral predicate" (shock words) | +0.08 (n=20) | **~zero — over-fit, dropped** |
| "abstraction penalty" | +0.10 (n=8) | **~zero — over-fit, dropped** |
| colon | +1.15 raw, but **flat once you control for fame** | confounded by fame, NOT a driver |

**Corrected takeaway:** the durable title levers are **FAME + myth-busting framing +
evidence-promise** — not "shock words" or "avoid abstract nouns." Use the formula below as a
mnemonic, but FAME is doing most of the work. (n modest, deltas small, confounded → FILTER,
learn weights via A/B.)

## The formula (mnemonic — fame is the load-bearing term)

**CTR ≈ Recognition × Curiosity-gap**, with myth-frame + evidence-promise as boosters.

A clickable title needs:

1. **Recognition** — a proper noun the viewer already reacts to: a famous person (Putin,
   Trump, JD Vance, Hancock), a menacing institution (KGB, London Stock Exchange), a
   famous topic (Crusades, Israel/Palestine), or a clean "Country vs Country" (Guatemala
   vs Belize, Venezuela vs Guyana). No recognition = no pool = no click.
2. **Stakes / shock** — a visceral, concrete predicate: "funded a genocide,"
   "weaponized," "child sacrifice," "might disappear," "oil war," "destroy."
3. **Curiosity gap / contradiction** — X can't be true if Y: "Piri Reis cites Columbus →
   Hancock says 12,000 years old."

## The kill-list (what tanked CTR, with real numbers)

- **Abstract nouns** — "pattern" (1.02%), "literacy boom" (1.12%), "structures,"
  "narrative," "human rights" (1.48%). The eye has nothing to grab.
- **Hidden subject** — "It Was Forbidden for Slaves Before It Was Mandatory" (1.56% —
  forbidden *what*?); "3 Men Signed 1 Document" (0.93% — who cares?).
- **Obscure proper nouns** — Operation Condor (1.61%), Vichy (1.11%), Sol Invictus,
  Bir Tawil, "$24 Manhattan … 19th-Century Fraud" (0.48%). Unrecognized = unserved.
- **Homework / lecture framing** — "Who Invented Human Rights?", "Hidden Literacy Boom."
  Sounds like a seminar, not a fight.
- **Known fact, no surprise** — "Stalin Purged His Army. Then Hitler Invaded" (1.57%):
  famous names but a story the viewer already feels they know. Fame needs a NEW angle.

## Mechanism in action — rebuild your own dead titles

Same research, same video; only the packaging changes.

| dead (real CTR) | rebuilt on the formula |
|---|---|
| $24 Manhattan Myth: A 19th-Century Fraud (0.48%) | **No, Nobody Sold Manhattan for $24 in Beads** |
| JD Vance vs History: Who Invented Human Rights? (1.48%) | **JD Vance Says the West Invented Human Rights. The Documents Disagree.** |
| Medieval Europe's Hidden Literacy Boom (1.12%) | **Everyone Thinks Medieval People Couldn't Read. They're Wrong.** |
| 3 Men Signed 1 Document. The USSR Ceased to Exist (0.93%) | **The Soviet Union Was Killed in a Forest Cabin** |

Pattern in every rebuild: front-load the famous/held belief → attach a concrete shocking
predicate → create the contradiction → delete the academic noun.

## Accessibility note (the channel's actual mission)

The mission is "make the academic discipline accessible," not "be a geopolitics channel"
or "copy a creator." This formula SERVES that: the title is the doorway. Win the click
with a famous, visceral, surprising hook; deliver the rigor inside. The rigor is the moat;
the title is just what gets a stranger through the door.

## How to use

1. Draft a title only after a FAMOUS target/belief is chosen (recognition is upstream).
2. Score against the 3-gate (recognition / stakes / curiosity). Missing one = rewrite.
3. Run against the kill-list.
4. Ship 2 variants via native A/B; keep the winner; log CTR. The formula is the filter;
   A/B is how we learn the channel-specific weights.
