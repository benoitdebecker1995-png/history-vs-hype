# Attribution Recovery — #35 Gibraltar / Treaty of Utrecht

**Date:** 2026-07-22
**Project:** 35-gibraltar-treaty-utrecht-2026 (PUBLISHED)
**Method:** raw-read of `source_get_content` per source, string-matched in local context (per instructions in the invocation — this is NOT a `primary-source-hunter` SOURCE-GENEALOGY run; no ledger upsert was requested or performed).
**Notebooks used:** `8740d7cc-33c0-4fa0-9a61-3730bdd094ca` ("Gibraltar and the British Mediterranean," 32 sources). The secondary notebook (`4add7058…`, "The Rock of Gibraltar") was not needed — the main notebook did not bottom out.
**Traps avoided:** all queries below are raw-reads of named scholarly sources by full UUID; the two circular sources (`4587d155…` "All notes," `76c830d3…` "History vs Hype - YouTube") were never queried. No `notebook_query` synthesis is reported as evidence anywhere below — every quote was string-matched in the raw source text I pulled myself.

---

### The Anglo-Dutch force that captured Gibraltar in 1704 comprised about 52 English and 10 Dutch ships of the line.
- **Status:** RECOVERED
- **Source:** Sir William G.F. Jackson, *The Rock of the Gibraltarians* (Associated University Presses, 1987), p. 95
- **Verbatim:** "Consideration was given to what other project might be undertaken by Rooke's powerful fleet of fifty-two English and ten Dutch ships of the line."
- **How verified:** raw-read of source `641447b4-8eb9-4db1-b58c-d17457d19410`, string-matched; page inferred from the running-header page markers embedded in the extracted text (marker for p.96 falls immediately after this passage).
- **Notes:** none — matches dossier exactly.

### The Treaty of Utrecht's ban on Jews and Moors in Gibraltar was quickly subverted in practice once Jewish merchants from Morocco became essential food suppliers to the garrison.
- **Status:** RECOVERED
- **Source:** Stephen Constantine, *Community and Identity: The Making of Modern Gibraltar Since 1704* (Manchester University Press, 2009), p. 21
- **Verbatim:** "Article X of the Treaty of Utrecht had particularly required the exclusion of Jews from Gibraltar, and yet this census showed that this had not been effected... True, corrupt local officials profited from the deals struck instead with Jews, but the men-on-the-spot also knew that Jews were valuable because their trading contacts, especially with Morocco across the straits, initially provided many of the food supplies which could no longer be obtained so easily from Spain across the isthmus."
- **How verified:** raw-read of source `9b871961-540c-49ed-a060-5f19c1b23058`, string-matched; page marker "Demographic roots of Gibraltarian identity 21" precedes the quote, next marker "22 Community and identity" follows it.
- **Notes:** Peter Gold's *Gibraltar* (p.5-ish, same passage the dossier already cites for the "no interest was shown from London" quote) corroborates the general fact ("a mixture of Jews, Moroccans and other civilians... were allowed to come back to the town") but does not mention food supply specifically — Constantine is the stronger, more specific source.

### British civilians first moved onto the disputed Gibraltar isthmus in 1814 during a yellow fever outbreak, with Spanish permission, and never left.
- **Status:** RECOVERED (core fact); "with Spanish permission" and "never left" are UNVERIFIED additions
- **Source:** Peter Gold, *Gibraltar: British or Spanish?* (Routledge, 2005), p. 11
- **Verbatim:** "The occupation of the isthmus by Gibraltar began partly as a consequence of the yellow fever epidemic of 1814, when many civilians were settled there in huts in order to escape the disease (Hills 1974: 374). Following a further outbreak in 1854, barracks were constructed on the isthmus and the guard-posts, sentry boxes and wooden huts were not removed when it was over."
- **How verified:** raw-read of source `895b6cf0-bb62-4d8b-aa82-9da40beb7e68`, string-matched; page marker "British Gibraltar / 11" precedes it, "12 / British Gibraltar" follows.
- **Notes:** I could not find "Spanish permission" or "never left" verbatim in Gold, Jackson, Grocott & Stockey, or Dadson — all four were checked. Gold's own account attributes the move to Britain unilaterally settling civilians there during the epidemic, not to a Spanish grant of permission; "not removed when it was over" (1854) is the closest the text gets to "never left," and that's about the 1854 outbreak, not 1814. These two details should be softened or re-verified before reuse — they read as plausible narrative gloss added on top of the sourced fact, not something a cited scholar states.

### The border fence on Gibraltar's isthmus was built in 1908-1909 not for military defense but to save money on sentries stopping tobacco smuggling.
- **Status:** RECOVERED
- **Source:** Sir William G.F. Jackson, *The Rock of the Gibraltarians* (1987), p. 263 (corroborated by Peter Gold, *Gibraltar*, p. 11)
- **Verbatim:** "the object is not to define a boundary nor to advance what has for generations been the line of sentries, but merely to economise the number of sentries in the existing line and, moreover, to afford increased facilities for repression of smuggling" — quoted by Jackson from the last British diplomatic note on the subject, 30 September 1909.
- **How verified:** raw-read of source `641447b4-8eb9-4db1-b58c-d17457d19410`, string-matched; page marker "The Rock in the First World War 263" appears in the same block of text.
- **Notes:** the word "tobacco" specifically is not in this Jackson passage (it just says "smuggling"); Gold's p.11 discussion of 19th-century Gibraltar smuggling separately identifies tobacco as the dominant smuggled good. Not a contradiction, just note that the "tobacco" specificity is an inference stitched from two separate passages rather than one source saying "tobacco fence."

### In the 1967 referendum, Gibraltarians voted to retain their link with Britain by 12,138 votes to 44 for Spain, on a 95.8% turnout.
- **Status:** RECOVERED
- **Source:** Peter Gold, *Gibraltar: British or Spanish?* (2005), p. 17
- **Verbatim:** "The result was about as decisive as it could be without being unanimous: 12,138 Gibraltarians voted in favour of continuing association with Britain and 44 voted for Spanish sovereignty out of 12,762 registered voters."
- **How verified:** raw-read of source `895b6cf0-bb62-4d8b-aa82-9da40beb7e68`, string-matched; page marker "Gibraltar incommunicado / 17" precedes the quote.
- **Notes:** none. 12,138 + 44 + the dossier's "55 invalid" = 12,237, consistent with a 95.8% turnout of 12,762 registered.

### In a 2002 referendum, Gibraltarians rejected a UK-Spain shared-sovereignty proposal by 17,900 votes to 192, on an 87.9% turnout.
- **Status:** CONTRADICTED
- **Source:** Peter Gold, *Gibraltar: British or Spanish?* (2005), p. 315; independently confirmed by Stephen Constantine, *Community and Identity* (2009), p. 414
- **Verbatim (Gold, p.315):** "the percentage of Gibraltarians who rejected the concept of shared sovereignty – 98.97 per cent (or 17,900) of the valid votes cast – was considerably higher than anyone had predicted. A mere 187 voted 'yes' to the question on the ballot paper (Efe, 8 November 2002)."
- **Verbatim (Constantine, p.414):** "collective and public expression of community solidarity was demonstrated, 187 voting in favour, 17,900 against."
- **How verified:** raw-read of both sources by full UUID (`895b6cf0…`, `9b871961…`), string-matched. Gold's page marker "Gibraltar holds its own referendum / 315" precedes the quote; Constantine's is on the page carrying footnote marker "414 Community and identity."
- **Notes:** **This is a genuine number error, not a rounding difference.** Two independent academic sources in the notebook, citing the same event, both give 187 "yes" votes, not 192. The arithmetic also settles it: 17,900 / (17,900+187) = 98.966% ≈ the dossier's own stated "98.97%"; 17,900/(17,900+192) = 98.94%, which does not match. **The dossier's "192" should be corrected to 187** before any further reuse of this figure.

### No Spanish government of any party has ever dropped Spain's sovereignty claim over Gibraltar, treating it as a sacred national duty.
- **Status:** UNVERIFIED
- **Source:** none found
- **Verbatim:** —
- **How verified:** searched Peter Gold's *Gibraltar* (895b6cf0…), Andrew Canessa (ed.), *Bordering on Britishness* (d565e1ee…), and Grocott & Stockey (c86ec2a6…) for "sacred," "never dropped," "never abandoned," "never relinquish," "consensus," "cross-party" — Gold's one "sacred" hit is Queen Isabella's will (a different claim, already separately verified in the dossier), not the modern cross-party-consensus claim. No source states this in these terms.
- **Notes:** the underlying fact (no Spanish government — PP or PSOE — has formally dropped the claim) is broadly consistent with everything else read across these books, but I could not find a scholar stating it as a discrete claim with the "sacred duty" framing. Recommend attributing this to general narrative synthesis rather than a specific citation, or re-querying with the phrase actually used in whichever source it came from originally.

### Spain claims Gibraltar based on territorial integrity while rejecting Morocco's identical argument for Ceuta and Melilla, calling those enclaves integral parts of the Spanish state rather than colonies.
- **Status:** RECOVERED
- **Source:** Peter Gold, *Europe or Africa? A Contemporary Study of the Spanish North African Enclaves of Ceuta and Melilla* (Liverpool University Press, 2000), p. 157
- **Verbatim:** "On the grounds that its North African enclaves are not colonies or dependent territories but integral parts of the Spanish state with their own representatives in the national Parliament, Spain has always rejected the suggestion that if it expects Britain to negotiate the transfer of the sovereignty of Gibraltar then it should also expect to have to negotiate the transfer of Ceuta and Melilla."
- **How verified:** raw-read of source `ee50f2f6-3c9d-476f-9c07-0182eb0d4433`, string-matched; page marker "The enclaves: Europe or Africa? / 157" precedes it (this book uses continuous absolute pagination confirmed against its own table of contents).
- **Notes:** none.

### Ceuta and Melilla are not listed as UN Non-Self-Governing Territories, unlike Gibraltar, and their residents hold full Spanish citizenship and parliamentary representation that Gibraltarians lack in the UK Parliament.
- **Status:** RECOVERED
- **Source:** Peter Gold, *Europe or Africa?* (2000), p. xii (UN-list point) and p. 1 / p. 157 (citizenship + Parliament point)
- **Verbatim (p. xii):** "Morocco also claims that the enclaves are colonies and therefore an anachronism, but the United Nations, which is keen to promote decolonization, does not include them in its list of territories waiting to be decolonized, on the grounds that Spanish settlers have been living there since long before the establishment of present-day Morocco."
- **Verbatim (p. 1):** "As part of Spain, with their own elected representatives in the national Parliament, these territories have well-established links with Europe... the majority of their citizens are Spanish and therefore now citizens of the European Union."
- **How verified:** raw-read of `ee50f2f6-3c9d-476f-9c07-0182eb0d4433`, string-matched.
- **Notes:** none — Gibraltar's own NSGT-list status is separately verified elsewhere in the dossier (UN GA Res 2353), so the contrast holds up.

### Franco closed the Spain-Gibraltar border completely in June 1969, cutting land, sea and telephone links for sixteen years, triggered by the 1967 referendum and a new Gibraltar constitution.
- **Status:** RECOVERED
- **Source:** Grocott & Stockey, *Gibraltar: A Modern History* (University of Wales Press, 2012), pp. 101-102
- **Verbatim:** "Franco ordered the full closure of the land frontier on 8 June 1969, and the ferry service between Algeciras and Gibraltar was suspended nineteen days later... The closure of the frontier was to last for over fifteen years..." Preceding text ties the trigger explicitly to "a new constitution granted in May 1969" that "further angered Franco."
- **How verified:** raw-read of source `c86ec2a6-019c-4982-b412-59d550eea844`, string-matched; page marker "RELATIONS WITH SPAIN, 1704–1969 / 101" precedes the passage. Corroborated by Robert Holland, "Gibraltar and the 'British Mediterranean': an overview," *The Round Table* 110:3 (2021), which independently gives the identical date: "on 8 June 1969 the Spanish authorities finally closed the frontier entirely, including the ferry plying between Algeciras and Gibraltar," triggered by "the pretext of the recent publication in London of a new constitutional instrument for Gibraltar."
- **Notes:** Grocott & Stockey describe the closure lasting "over fifteen years" (June 1969 – Feb 1985 = 15 years 8 months); the dossier's "sixteen years" is a common rounding also used by Gold's *Europe or Africa?* ("sixteen years of closure") — not a contradiction, just noting the underlying precise duration.

### Gibraltar's modern British identity was partly a deliberate 'melting pot' narrative constructed in the 1940s-50s to distance the territory from Spain, even though 85% of schoolchildren still spoke only Spanish as late as the 1950s.
- **Status:** RECOVERED
- **Source:** L.G. Martínez del Campo et al., "A New British Subject: The Creation of a Common Ethnicity," in Andrew Canessa (ed.), *Bordering on Britishness* (Palgrave Macmillan, 2019), p. 127
- **Verbatim:** "Gibraltar in the 1950s and 1960s was still a very Spanish-speaking place... For all the memories of children returning from the UK fluent in English, in 1953, it was estimated that 85% of Gibraltar's school children arrived on their first day of school knowing only Spanish (West 1953, in Stockey 2009: 191)."
- **How verified:** raw-read of source `d565e1ee-1f98-4f22-91fe-f9ff14d621e1`, string-matched; page marker "L. G. MARTÍNEZ DEL CAMPO ET AL. / 127" follows the quote directly.
- **Notes:** the same chapter (pp.123-125) extensively documents H.W. Howes's 1946/1951 construction of the "melting pot" narrative ("Howes only emphasised Gibraltarians' Maltese and Genoese backgrounds to create 'a common myth of descent'... He was describing Gibraltar as a melting pot of White races, in which Spanish and Moroccan heritages were elided"), so the dossier's Howes attribution is well grounded in this same source — I did not separately pin an exact page for the Howes sentence, but it's the same chapter, pp. 123-127.

### Franco's 1969-1985 border blockade acted as the catalyst that cemented a modern Gibraltarian identity defined more by being 'not Spanish' than by traditional Britishness.
- **Status:** RECOVERED
- **Source:** L.G. Martínez del Campo et al., in Canessa (ed.), *Bordering on Britishness* (2019), p. 123
- **Verbatim:** "In the 1940s, however, the Spanish dictator, General Franco, began a campaign to recover Gibraltar that culminated in the closure of the border in 1969. It was during this campaign that Gibraltarians developed the clearest articulation of their unique collective identity through a nationalist discourse that would make them new British subjects... The closed border situation (1969–1982) intensified the sense of solidarity within the community."
- **How verified:** raw-read of source `d565e1ee-1f98-4f22-91fe-f9ff14d621e1`, string-matched; page marker "A NEW BRITISH SUBJECT: THE CREATION OF A COMMON ETHNICITY… / 124" follows the quote.
- **Notes:** this source frames the "closed border situation" as 1969–1982 (full closure, before the pedestrian-only partial reopening), not 1969–1985 — a nuance, not a contradiction, since the dossier itself separately tracks the December 1982 partial reopening and February 1985 full reopening as two distinct dates.

### Gibraltar's economy stagnated but did not collapse during the sixteen-year blockade, growing in real terms with British development aid.
- **Status:** RECOVERED
- **Source:** Grocott & Stockey, *Gibraltar: A Modern History* (2012), p. 120, quoting former Governor Sir William Jackson
- **Verbatim:** "The local economy was, in the words of former governor Sir William Jackson, in a position where it 'stagnated, but did not fail' as a result of the frontier closure."
- **How verified:** raw-read of source `c86ec2a6-019c-4982-b412-59d550eea844`, string-matched; page marker "120 GIbRALTAR: A MODERN HISTORY" immediately precedes the passage.
- **Notes:** this is a nested attribution — Grocott & Stockey citing Jackson — cite it to Grocott & Stockey p.120 (that's the actual page reachable in the notebook); Jackson's own original wording was not separately located in his book's raw text.

### During the blockade, the Spanish city of Algeciras prospered as the exclusive cross-Strait shipping hub while La Línea, Gibraltar's immediate neighbor, suffered economically.
- **Status:** RECOVERED
- **Source:** Sir William G.F. Jackson, *The Rock of the Gibraltarians* (1987), p. 318
- **Verbatim:** "Other parts of the Campo prospered. Algeciras, for instance, boomed because it attracted all the cross-Straits ferry traffic that could no longer use Gibraltar. A large container handling complex was established, and Algeciras became one of the most active ports in Spain... The huge dockside cranes stood forlornly unused as a memorial to the Franco government's failure to make good its promises to La Linea, the population of which had fallen from seventy thousand to fifty thousand."
- **How verified:** raw-read of source `641447b4-8eb9-4db1-b58c-d17457d19410`, string-matched; page marker "318 THE ROCK OF THE GIBRALTARIANS" precedes the passage, "The Rock of the Gibraltarians 319" follows it.
- **Notes:** this single Jackson passage also directly confirms several other dossier bullets under "Algeciras Paradox" / "Impact on La Línea" not separately re-verified here (petrochemical plant near Carteia, steel rolling mill at the Palmones, La Línea population fall 70,000→50,000, "£4M over a three-year period" UK housing aid). Worth pointing the whole ACT 6 economic section at this one page.

### The 2025 UK-EU Gibraltar Trade and Mobility Agreement removes physical barriers at the La Línea border while including a clause stating it does not affect either side's sovereignty claims.
- **Status:** UNVERIFIED (from this notebook)
- **Source:** none in the academic notebook
- **Verbatim:** —
- **How verified:** all seven academic books/chapters in this notebook were published 2000-2019; none can cover a June 2025 treaty. The three 2021-2023 journal articles read (Garcia 2021, Holland 2021, O'Dubhghaill & Van Kerckhoven 2023) predate it too. This claim is inherently outside the notebook's reach.
- **Notes:** the dossier already marks this "NotebookLM / official government statements" — that's honest; it should simply drop the "NotebookLM" half of the tag and cite only the official joint declaration / government statements, since no notebook source can verify it.

### During the Great Siege of 1779-1783, British defenders destroyed all ten Spanish-French floating batteries using red-hot cannonballs after conventional bombardment had failed.
- **Status:** RECOVERED
- **Source:** Sir William G.F. Jackson, *The Rock of the Gibraltarians* (1987), pp. 176-177
- **Verbatim:** "Of the eight battering ships still afloat, six were burning fiercely and two were still intact. Three blew up during the morning and three were burnt to the waterline. Curtis tried to salvage the remaining two. One suddenly burst into flames and blew up, and the other proved impossible to save and was burnt deliberately in the afternoon... It is thought that about two thousand out of the five thousand men manning the battering ships were lost." (The other two of the ten — the flagship *Pastora* and the *Talla Piedra* — are described as catching fire and being abandoned/burnt earlier that night, in the same passage, p.175-176.)
- **How verified:** raw-read of source `641447b4-8eb9-4db1-b58c-d17457d19410`, string-matched; page marker "176 THE ROCK OF THE GIBRALTARIANS" precedes the passage.
- **Notes:** the dossier's "~2,000 lost during floating battery attack alone (out of 5,000 manning them)" is an exact match to Jackson's own figure — good sign this whole ACT 3 section traces to Jackson.

### Gibraltar has been besieged at least fourteen times across seven centuries, changing hands between Moorish, Castilian, and British control before Britain's final retention after the 1779-1783 Great Siege.
- **Status:** RECOVERED
- **Source:** Sir William G.F. Jackson, *The Rock of the Gibraltarians* (1987), Table of Contents
- **Verbatim:** "3. The First Five Sieges of the Rock: 1309 to 1350 / 4. The End of Moorish Gibraltar: The Sixth, Seventh, and Eighth Sieges, 1350 to 1462 / 5. Spanish Neglect: The Ninth and Tenth Sieges and the Corsair Raid, 1462 to 1560 / ... 7. Hapsburg Gibraltar: The Eleventh and Twelfth Sieges, 1693 to 1713 / 8. Gibraltar, the Bargaining Counter: The Thirteenth Siege, 1713 to 1727 / ... 10. As Safe as the Rock: The Fourteenth or Great Siege, 1779 to 1783 / ... 17. The Rock of the Gibraltarians: The Fifteenth Siege, 1969 to 1985."
- **How verified:** raw-read of source `641447b4-8eb9-4db1-b58c-d17457d19410`, string-matched (the book's own chapter structure numbers every siege).
- **Notes:** **Jackson's own chapter title literally calls Franco's 1969-1985 blockade "The Fifteenth Siege"** — a formal chapter heading, not an informal comparison. This is actually a *stronger* claim than the dossier's hedged "unofficial '15th Siege'" — worth tightening the script/card language to attribute "Fifteenth Siege" directly to Jackson's book structure rather than presenting it as an unofficial nickname.

### About 80,000 vessels pass through the Strait of Gibraltar each year, underscoring the strategic value of controlling the chokepoint.
- **Status:** UNVERIFIED
- **Source:** none found
- **Verbatim:** —
- **How verified:** searched for "80,000," "vessels," "bunker," "toneladas"/"buques" across Grocott & Stockey, Gino Naldi's 2013 territorial-waters article, "España y Gibraltar tras el Brexit," and the "Bottom-up Geopolitics" border-ethnography article — none contain a Strait vessel-traffic count. Grocott & Stockey's only "80,000" hit is an unrelated £80,000 Great Siege damage estimate.
- **Notes:** this figure most likely comes from a modern shipping-authority or Port of Gibraltar statistic outside this notebook (e.g. an IMO/Lloyd's List figure), not an academic history. Recommend re-sourcing to an official maritime-traffic report rather than "NotebookLM."

### Franco declared Spain 'non-belligerent' in WWII, favoring the Axis, while still allowing over 13,000 Spanish workers to cross daily to build British airport defenses at Gibraltar.
- **Status:** RECOVERED (non-belligerence); NUMBER/PERIOD MISMATCH on the workers figure
- **Source:** Sir William G.F. Jackson, *The Rock of the Gibraltarians* (1987), p. 282 (non-belligerence) and p. 297 (daily worker count)
- **Verbatim (p.282):** "When France collapsed, Franco had reinsured himself with Hitler by declaring Spain nonbelligerent instead of neutral."
- **Verbatim (p.297):** "An average of twelve thousand Spaniards came across the frontier from La Linea or by ferry from Algeciras to work in Gibraltar every day until 1954 when the Spanish authorities started to refuse requests for new work permits."
- **How verified:** raw-read of source `641447b4-8eb9-4db1-b58c-d17457d19410`, string-matched. Page 282 marker "282 THE ROCK OF THE GIBRALTARIANS" precedes the non-belligerence sentence; page 297 marker "Gibraltar before the United Nations 297" precedes the worker-count sentence.
- **Notes:** **worth flagging.** The only daily-worker figure I could find in Jackson is "twelve thousand," not "over 13,000," and — more importantly — it is explicitly framed as a *general post-war* average "every day until 1954" (in the chapter "Gibraltar before the United Nations," covering 1945-1969), not specifically as wartime labor "to build British airport defenses." I could not find a WWII-specific daily-crossing figure tied to airfield construction anywhere in Jackson or Gold. The non-belligerence fact is solid; the "13,000 / building the airport" framing needs re-verification or softening — it may be conflating two different periods/statistics.

### Hitler's Operation Felix plan to seize Gibraltar, involving 210 guns and 20,000 shells, was never executed because Franco stalled by demanding excessive grain, weapons and territory in return.
- **Status:** RECOVERED
- **Source:** Sir William G.F. Jackson, *The Rock of the Gibraltarians* (1987), p. 282
- **Verbatim:** "Some 210 guns were to be concentrated within range of the Rock. They would stun the defenders with twenty thousand shells, and dive bombers would join in to support the infantry assault that would be made across the isthmus from La Linea with Moorish Castle as the first day's objective... the infantry assault that would be carried out by specially selected mountain troops who were to be trained on a similar feature to Gibraltar in the French Alps." ... "Franco was overtly friendly and cooperative but presented a string of logical but unacceptable demands as the price for Spanish cooperation: replacement of Allied grain shipments by supplies from Germany; provision of weapons, equipment, and spares to bring the Spanish armed forces up to date; and the transfer of large slices of French North Africa to Spanish sovereignty."
- **How verified:** raw-read of source `641447b4-8eb9-4db1-b58c-d17457d19410`, string-matched; page marker "282 THE ROCK OF THE GIBRALTARIANS" precedes both passages (same page).
- **Notes:** none — precise, comprehensive match including the "mountain troops" detail the dossier doesn't even mention.

---

## SUMMARY

- **RECOVERED:** 15 of 20 claims (some with minor caveats noted above — see #3, #4, #10, #12, #13, #17, #19)
- **CONTRADICTED:** 1 claim (2002 referendum "yes" vote — dossier says 192, two independent academic sources say 187)
- **UNVERIFIED:** 4 claims (#7 "sacred duty" framing, #15 the 2025 treaty — inherently outside this notebook's date range, #18 the 80,000-vessel statistic, plus the "13,000 workers / WWII airfield" sub-claim inside #19 which is a number/period mismatch rather than a clean recovery)

## THE ONE FINDING THAT MATTERS MOST

**The 2002 referendum "yes" vote is wrong in the published dossier.** It says 192; Peter Gold's *Gibraltar: British or Spanish?* (p.315) and Stephen Constantine's *Community and Identity* (p.414) — two independent university-press sources in the notebook — both say **187**. The arithmetic settles it: 17,900/(17,900+187) = 98.97%, matching the dossier's own stated percentage; 17,900/(17,900+192) = 98.94%, which does not. This should be corrected wherever "192" appears (currently: `01-VERIFIED-RESEARCH.md` line ~389 and the extracted-claims JSON).

**Runner-up:** Jackson's own book literally titles its chapter on Franco's 1969-1985 blockade "The Fifteenth Siege" — not an informal nickname but his formal chapter heading. The dossier hedges this as an "unofficial '15th Siege,'" which undersells how directly citable it actually is.

OUTPUT: D:/History vs Hype/video-projects/_ARCHIVED/published/35-gibraltar-treaty-utrecht-2026/_research/ATTRIBUTION-RECOVERY.md
