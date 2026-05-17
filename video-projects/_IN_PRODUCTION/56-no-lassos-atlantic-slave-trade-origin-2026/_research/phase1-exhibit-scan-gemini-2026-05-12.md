# Phase 1 — Open Exhibit Scan (Gemini Flash)

**Run:** 2026-05-12
**Model:** gemini-2.5-flash
**Prompt:** open landscape scan, no pre-loaded candidate list (per `feedback-open-research-prompts.md`)
**Diff vs Claude pre-load:** Claude's closed 4-candidate list (Zurara / papal bulls / Portuguese letters / Slave Voyages) was REPLACED — none made Gemini's top 3.

## Gemini's full enumeration (11 candidates)

| # | Document | Date | Origin |
|---|---|---|---|
| 1 | Zurara, *Crónica dos feitos notáveis que se passaram na conquista da Guiné* | 1453-60 | Portuguese Royal Court |
| 2 | Pope Nicholas V, *Dum Diversas* | 1452 | Papal States |
| 3 | Pope Nicholas V, *Romanus Pontifex* | 1455 | Papal States |
| 4 | Virginia General Assembly, Act XII *Partus Sequitur Ventrem* | 1662 | British Colonial Virginia |
| 5 | Second Charter of the Royal Adventurers Trading into Africa | 1663 | Kingdom of England |
| 6 | Royal Charter of the Royal African Company | 1672 | Kingdom of England |
| 7 | Louis XIV, *Le Code Noir* | 1685 | Kingdom of France |
| 8 | Captain Thomas Phillips, *Journal of a Voyage Made in the Hannibal* | 1694 | Royal African Company |
| 9 | Asiento de Negros (Treaty of Utrecht) | 1713 | Britain + Spain |
| 10 | Gregson v. Gilbert (Zong appeal transcript) | 1783 | British Court of King's Bench |
| 11 | Slave Trade Act (Dolben's Act) | 1788 | Parliament of Great Britain |

## Gemini's top 3

| Rank | Document | Pitch | Risk |
|---|---|---|---|
| 🥇 | **Gregson v. Gilbert (1783)** | Highest English common law court treating 132 drowned humans as insurance cargo loss under "general average" doctrine. Unique to European maritime law; no African analog. | **Late date (1783)** — captures the system mature, not built. Mansfield ordered retrial; civil case ended without final ruling. |
| 🥈 | **Code Noir (1685)** | Royal edict explicitly classifying enslaved persons as *meubles* (movable property). Article XLIV: *"Déclarons les esclaves être meubles."* | Paternalistic clauses (baptism, Sunday rest, master-care) give bad-faith opening. |
| 🥉 | **Asiento de Negros (1713)** | International treaty between sovereign crowns; introduces *pieza de India* — humans as standardized financial unit. Quintessentially European corporate-state. | Clinical prose obscures violence; needs active translation by host. |

Gemini's recommendation: **Gregson v. Gilbert** for online-debate audience — "cuts through abstract historical debates by demonstrating the Atlantic trade was a highly financialized, corporate, and state-sanctioned capitalist enterprise unique to the European imperial apparatus."

## Concede-half verification (Gemini)

- ✅ Intra-African slavery pre-1441: TRUE (Manning 2016)
- ✅ Trans-Saharan trade 7th-c onward: TRUE (Manning 2016)
- ✅ European model raid→trade transition 1450-1500: TRUE (PBS / Wikipedia)
- ✅ Asante/Dahomey/Oyo militarized due to Atlantic demand: TRUE (Rodney + Thornton — but Gemini's framing of Thornton may overstate; needs NLM verification)
- ⚠️ **Gates 2010 NYT op-ed summary FLAGGED for NotebookLM verification** — Gemini's summary ("Gates argued... entire African societies actively organized the capture and sale of foreign captives for immense economic gain") sounds like it may oversimplify Gates's actual position. Round-trip required before use.

## Verbatim-quote authenticity flags (must NotebookLM round-trip)

| Quote | Attribution | Confidence |
|---|---|---|
| "The case of slaves was the same as if horses had been thrown overboard" | Mansfield | HIGH — well-documented |
| "Blacks are goods and property; it is madness to accuse these well-serving honourable men of murder" | Solicitor General John Lee | MEDIUM — Lee said something like this but exact phrasing needs primary verification |
| "(though it shocks one very much) that the Case of Slaves was the same as if Horses had been thrown overboard" | Mansfield with parenthetical | LOW — sounds paraphrased; needs verbatim from King's Bench Reports 3 Doug. 232 |
| "Déclarons les esclaves être meubles" | Code Noir Article XLIV | HIGH — verbatim French text well-attested |
| "144,000 Negroes, Piezas de India, of both Sexes" | Asiento Article I | HIGH — Davenport edition verbatim |

## Gemini's NotebookLM upload shortlist

1. Donnan ed., *Documents Illustrative of the Slave Trade to America*, Vol. 1 (1441-1700)
2. Davenport ed., *European Treaties Bearing on the History of the United States*, Vol. III
3. Hening ed., *Statutes at Large of Virginia*, Vol. 2
4. Gregson v. Gilbert (1783) 3 Doug. KB 232 — primary court report
5. Manning, *Slavery and Slave Trade in West Africa 1450-1930* (2016)

## Claude additions (suggested for NotebookLM upload)

- Walvin, *The Zong: A Massacre, the Law and the End of Slavery* (Yale, 2011) — if Zong wins, this is the primary-source secondary
- Thornton, *Africa and Africans in the Making of the Atlantic World*, 2nd ed. (Cambridge 1998) — original demand-shaping thesis source
- Gates 2010 NYT op-ed — direct primary for verifying Gemini's summary
- Sue Peabody / John Garrigus translation of *Code Noir* (current scholarly English translation) — if Code Noir wins
