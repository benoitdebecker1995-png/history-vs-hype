# Phase 1b — Debunk Literature Audit (Gemini Flash)

**Run:** 2026-05-12
**Model:** gemini-2.5-flash
**Prompt:** open audit of published debunk literature, what primary documents they deploy, scored for streamer-debate viability

## Top 10 debunk works enumerated

1. Walter Rodney, *How Europe Underdeveloped Africa* (1972)
2. John Thornton, *Africa and Africans in the Making of the Atlantic World* (1998 2nd ed.)
3. Patrick Manning, *Slavery and African Life: Occidental, Oriental, and African Slave Trades* (1990)
4. Stephanie Smallwood, *Saltwater Slavery* (2007) — *NEW vs Phase 1a*
5. Toby Green, *A Fistful of Shells* (2019) — *NEW*
6. Robin Blackburn, *The Making of New World Slavery* (1997) — *NEW*
7. Inikori & Engerman eds., *The Atlantic Slave Trade* (1992) — *NEW*
8. Michael A. Gomez, "All Guilt Is Not Equal" (2010, The Root) — *NEW*
9. Osa Fasehun, "The Myth of Mass African Complicity" (2021 U Chicago MA thesis) — *NEW*
10. Ken Olende, "Slavery in precolonial Africa doesn't justify Atlantic trade" (2007 Socialist Worker)

## Streamer-debate viability ranking (Gemini scored 5 documents on 5 criteria, 1-5 each, max 25)

| Rank | Exhibit | Score | Compressibility | Bad-faith resistance | Timeline directness | Verbatim ammunition | Source-side moat |
|---|---|---:|---:|---:|---:|---:|---:|
| 🥇 | **Phillips' Journal / RAC records (1694)** | **24** | 5 | **5** | 4 | 5 | 5 |
| 🥈 | Romanus Pontifex (1455) | 22 | 5 | 3 | **5** | 4 | 5 |
| 🥉 | Gregson v. Gilbert (1783) | 22 | 5 | 5 | **2** | 5 | 5 |
| 4 | Code Noir (1685) | 19 | 5 | 2 | 3 | 4 | 5 |
| 5 | Afonso I letters (1514-26) | 18 | 4 | **1** | 5 | 4 | 4 |

**Note:** Afonso I scored 1/5 on bad-faith resistance — Gemini flagged that a right-wing debater can seize on Afonso's own admissions of holding a slave compound (*terreyro*) and use the letters AGAINST the thesis. Avoid as primary exhibit. Could appear briefly as supporting visual.

## Gemini's recommendation — Pairing

**Romanus Pontifex (1455) chronological shield + Phillips' Journal (1694) tactical sword.**

Logic: 1455 papal authorization addresses "before Europeans came" timeline directly. Phillips 1694 shows what the authorization operationalized — corporate branding irons, "as if they were so many beasts," mortality arithmetic.

## Section 5 — Destiny ammunition delivery (from Gemini, paired version)

Gemini wrote a 200-word real-time ammunition delivery using the pairing. Key moves:

1. **Concede:** intra-African slavery, debt-pawnship, trans-Saharan networks existed pre-1441 — baseline fact
2. **Deploy chronological shield:** Romanus Pontifex 1455 — supreme European legal authority authorized "in perpetuam servitutem redigendi" decades before mature trade
3. **Deploy operational sword:** Phillips 1694 — slaver's own log, branding "upon the naked breast... as if they were so many beasts"
4. **Close:** "You are confusing a regional pool with a transnational ocean liner built exclusively by the West."

The Phillips quote is the kill shot. The "I doubt not but this trade seems very barbarous to you, but since it is followed by mere necessity it must go on" line is uniquely powerful because it's the slaver explicitly acknowledging it's "barbarous" AND endorsing continuation — no abolitionist framing, no modern interpretation.

## Key verbatim quotes flagged (must NotebookLM round-trip)

### Romanus Pontifex (1455) — Latin + English

| Phrase | Language | Confidence |
|---|---|---|
| "invadendi, conquirendi, expugnandi, debellandi, et subiugandi" (invade, search out, capture, vanquish, subdue) | Latin | HIGH — well-documented |
| "in perpetuam servitutem redigendi" (reduce their persons to perpetual slavery) | Latin | HIGH |
| "appropriate to himself and his successors the kingdoms" | English (translated) | HIGH |

### Phillips' Journal (1694)

| Phrase | Confidence | Verification needed |
|---|---|---|
| "I doubt not but this trade seems very barbarous to you, but since it is followed by mere necessity it must go on" | HIGH | Donnan ed. or Awnsham Churchill *Voyages* (1732) — locate page |
| "brand them with a hot iron upon the naked breast" | HIGH | Same |
| "as if they were so many beasts" | MEDIUM-HIGH | Verify exact phrasing — Phillips uses similar but check verbatim |
| "we take all possible care that they are not burned too hard" | HIGH | Same |
| "entire and only trade for buying and selling" | HIGH | Likely from RAC charter, not Phillips — verify attribution |

## NotebookLM upload shortlist (revised)

**For exhibit verification (must include):**
1. Elizabeth Donnan ed., *Documents Illustrative of the Slave Trade to America*, Vol. 1 (1930) — contains Phillips' Journal in full + RAC records
2. Frances Davenport ed., *European Treaties Bearing on the History of the United States*, Vol. I (1917) — contains Romanus Pontifex Latin + English
3. Awnsham & John Churchill, *A Collection of Voyages and Travels*, Vol. VI (1732) — original Phillips Journal source

**For thesis grounding (concede half):**
4. John Thornton, *Africa and Africans in the Making of the Atlantic World* (1998 2nd ed.)
5. Patrick Manning, *Slavery and African Life* (1990) — quantitative demographic models
6. Toby Green, *A Fistful of Shells* (2019) — cowrie / fiscal-dependency framing

**For scoping (informational):**
7. Stephanie Smallwood, *Saltwater Slavery* (2007) — RAC corporate ledger close-read; potentially adds quotes to the Phillips arsenal
