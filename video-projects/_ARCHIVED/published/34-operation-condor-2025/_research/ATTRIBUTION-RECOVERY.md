# Attribution Recovery — Operation Condor (#34, published)

**Date:** 2026-07-22
**Project:** 34-operation-condor-2025 (published)
**Task:** Recover named source + page for the 14 claims in `01-VERIFIED-RESEARCH.md` currently cited only to "Multiple sources confirm" / "Academic sources" / "Multiple academic sources with declassified documents."
**Notebook:** `cc2902e2-0d55-4aea-9658-81df97318935` — "No Safe Haven: The Theory of Cooperative Transnational Repression" (20 sources)
**Excluded from citation (own material re-uploaded to notebook):** source `615e15be-f02c-4b10-9ca9-9992130c5f17` ("All notes 5/2/2026") — this is our own research dossier, not a scholarly source. Not cited anywhere below.
**Method:** For every claim below, `notebook_query` (scoped, excluding the note above) was used only as a *pointer*; every verbatim and page number was then confirmed by `source_get_content` raw-read (Python regex grep on the extracted book text) or by fetching the actual National Security Archive page and stripping it to plain text myself. No page number or quote below comes from `notebook_query` prose alone.

**Counts:** 12 RECOVERED · 0 UNVERIFIED · 2 CONTRADICTED (one of the two is a compound claim where half is recovered and half is factually wrong — counted as CONTRADICTED per "flag loudly" instruction)

---

## CONTRADICTED #1 — the CIA "Logistics Department" encryption machine (headline finding)

### Claim
"The CIA's Logistics Department manufactured a machine specifically for the 'Condor System' to encode and decode secure communications between member intelligence services."

- **Status:** CONTRADICTED (the "declassified documents" framing is false; the real chain is single-source oral testimony, doubted by the citing scholar — but a much stronger, genuinely declassified alternative exists and should replace this claim on screen)
- **Tier of what the dossier actually rests on:** [T4] third-hand oral testimony via a self-published book, not documents.

**The ladder, raw-read:**
1. **McSherry, *Predatory States* (Rowman & Littlefield, 2005), p.9** (confirmed against an online preview showing the same page number): "A former Bolivian agent of Condor, Juan Carlos Fortún, told a Bolivian journalist in the early 1990s that an advanced system of communications was installed in the Ministry of the Interior in La Paz... He said that a special machine to encode and decode messages was made especially for the Condor system by the Logistics Department of the CIA." Footnote 10 (raw-read from the endnotes block, found ~250K characters after the main quote): **"He may have meant the Technical Services Department of the CIA. Irusta, Espionaje, 547–550. Much of the information in this book seems credible, but some is impossible to verify..."** — McSherry herself doubts the department name.
2. **Dinges, *The Condor Years* (New Press, 2004), main text + endnote 122** (raw-read, verbatim): "A Bolivian security agent, quoted by author Gerardo Irusta, revealed the existence of the machines and claimed that the devices were provided by the CIA. The agent, Juan Carlos Fortun, said, 'The chief of our department, generally an Army liaison officer, had access to a special machine, which was kept locked, that served to encode and decode the messages...'" Endnote 122: **"Encrypting machines: See Gerardo Irusta, Espionaje y servicios secretos en Bolivia (La Paz, 1995, no publisher listed), 301. Irusta's source, Interior ministry official Juan Carlos Fortun, provided copies of coded and decoded telexes from Condortel. Fortun said his boss told him, 'It was a machine specially manufactured for the "Condor System" by the Logistics Department of the American Central Intelligence Agency.'"**
3. **Bedrock:** Gerardo Irusta, *Espionaje y servicios secretos en Bolivia y el Cono Sur: Nazis en la Operación Cóndor*, 2nd ed. (La Paz, 1997) — a self/small-published Bolivian book, "no publisher listed." Its source is Juan Carlos Fortún, a former Bolivian interior-ministry official, relaying what **his boss told him** — third-hand, oral, uncorroborated by any document either scholar could produce. **Both** academic sources that cite this claim (McSherry and Dinges) treat it with explicit hedging ("claimed," "he may have meant") — neither presents it as documentary fact, contrary to the dossier's "declassified documents" framing.

### The real declassified record — and it tells a bigger, better story
Raw-read of **National Security Archive Briefing Book #696, "The CIA's 'Minerva' Secret"** (compiled by Peter Kornbluh and Carlos Osorio, published Feb 11, 2020), fetched and stripped to plain text directly (not AI-summarized):
- **Document 1:** Operation Condor Foundation Act, "Minutes of the Conclusion of the First Interamerican Meeting on National Intelligence," Secret, Nov 28, 1975 (source: *The Pinochet File*): members "recommend the use of a Cryptography System that will be available to member countries within the next 30 days... it will be replaced in the future with cryptographic machines to be selected by common agreement."
- **Document 3:** CIA cable, "Communications System Employed by the Condor Organization," Secret, **Feb 1, 1977** (Argentina Declassification Project): **"the cipher system employed by Condor is a manual machine system of Swiss origin given to all Condor countries by the Brazilians and bearing the designation CX52."**
- **Document 4:** DIA Intelligence Appraisal, "Latin America: Counterterrorism and Trends in Terrorism," **Aug 11, 1978**: **"in late 1977, Argentina provided Hagelin Crypto H-4605 equipment to Condortel to enhance the security of its teletype nets."**
- The CX-52 and H-4605 were Crypto AG products — and Crypto AG was **secretly co-owned by the CIA and West German BND** (operation "Minerva"/"Rubicon," revealed 2020 via Washington Post/ZDF reporting on internal CIA/BND histories). The CIA/NSA "rigged the company's devices so they could easily break the codes that countries used to send encrypted messages."
- **URL:** https://nsarchive.gwu.edu/briefing-book/chile-cyber-vault-intelligence-southern-cone/2020-02-11/cias-minerva-secret

**This is a different, better-documented, and more dramatic story than the dossier's claim.** The CIA did not build a bespoke "Condor machine." Condor used commercially available Swiss Hagelin/Crypto AG machines supplied through Brazil and then Argentina — and the CIA had *already secretly compromised the manufacturer itself*, meaning U.S. intelligence could plausibly read Condor's "secure" traffic all along. That is backed by four named, dated, declassified cables with a stable public URL — a strictly stronger on-screen claim than "the CIA's Logistics Department built Condor a machine."

- **Showable file:** the NSA briefing-book page itself is a clean, citable, screen-showable page (document titles, dates, and quoted excerpts are on the page).
- **How verified:** raw-read of McSherry p.9 and Dinges main text + endnote 122 (both via `source_get_content` grep against saved book text); fetched NSA URL directly via curl, stripped HTML, and read the plain text myself (not WebFetch's AI summary, which I cross-checked against but did not rely on for quotes).

### On-screen recommendation
Drop "CIA's Logistics Department manufactured a machine specifically for the Condor System." Replace with the Crypto AG/Minerva finding, sourced to NSA Briefing Book #696 Documents 1/3/4 — it is primary, dated, freely viewable, and a stronger claim than the one currently in the dossier.

---

## CONTRADICTED #2 — Contreras's Fort Belvoir training (compound claim; the 7:30 AM briefing half is fine)

### Claim
"DINA director Manuel Contreras met privately with Pinochet every morning at 7:30 AM and received U.S. Army training at Fort Belvoir, Virginia, between 1967 and 1969."

- **Status:** CONTRADICTED (the Fort Belvoir/1967-1969 detail) — RECOVERED (the 7:30 AM briefing detail)
- **Tier:** [S→P] for the briefing (scholar directly quoting a declassified cable) / no source found for Fort Belvoir, and the best available evidence contradicts it.

**7:30 AM briefings — RECOVERED.**
Raw-read, **Kornbluh, *The Pinochet File* (New Press, 2003/2013), pp.174-175** (page confirmed via the book's own back-of-book index entry "Corcoran, Lawrence, 174" and the in-text running header "pinochet in power 175" immediately after the quote):
> "But during a dinner party with 'a very senior DINA official'—perhaps Contreras himself—the U.S. air force attaché in Santiago, Lt. Col. Lawrence Corcoran, gathered intelligence on Pinochet's personal involvement in the operations of his secret police. Contreras met Pinochet every morning at 7:30 a.m., and privately briefed him on 'the coming events and status of existing DINA activities,' this official informed Corcoran. 'The president issues instructions on DINA; is aware of its activities; and in fact heads it.'"

This is genuinely primary-via-scholar: Kornbluh is quoting a **declassified U.S. Air Force attaché report**, not asserting the fact himself. Solid tier for on-screen use, attributed correctly ("a declassified U.S. attaché cable reports that...").

**Fort Belvoir, Virginia, 1967-1969 — CONTRADICTED.**
- Searched all four core notebook sources (McSherry, Dinges *Condor Years*, Kornbluh, Lessa) for "Fort Belvoir": **zero matches in any of them.** No source in the notebook supports this detail.
- Best available evidence (Wikipedia's Manuel Contreras article, sourced) states: **"In 1967, Contreras completed a Postgraduate Course as a General Staff Officer at the School of the Americas in Fort Gulick, located in the Panama Canal Zone. Upon returning to Chile in 1969... Contreras assumed the role of an intelligence instructor at the Tejas Verdes School of Engineers."**
- Fort Gulick (Panama Canal Zone, home of the U.S. Army School of the Americas 1963–1984) and Fort Belvoir (Virginia, U.S. Army engineer/intelligence schools) are two different institutions on two different continents. Nothing in the notebook's academic corpus, and nothing found in an open search, places Contreras at Fort Belvoir. This looks like a fabricated or conflated detail from an earlier research pass.

- **Showable file:** none — this detail should be corrected, not sourced.
- **How verified:** raw-read (grep, zero hits) of McSherry, Dinges *Condor Years*, Kornbluh, Lessa; WebFetch of `en.wikipedia.org/wiki/Manuel_Contreras` (fetched directly, quote reproduced above), cross-checked with two independent WebSearch queries that converged on Fort Gulick/School of the Americas and never surfaced Fort Belvoir for Contreras.

### On-screen recommendation
Keep the 7:30 AM briefing detail, attributed to Kornbluh quoting a declassified U.S. attaché cable (pp.174–175). **Cut "Fort Belvoir, Virginia" and the 1967–1969 U.S. Army training claim** — it is not supported by any source in the research notebook and contradicts the best available published biography (School of the Americas, Fort Gulick, Panama, 1967).

---

## RECOVERED claims

### DINA was dissolved August 13, 1977 under international pressure after the Letelier assassination, and its personnel and infrastructure passed to the new CNI in a transition that was largely cosmetic.
- **Status:** RECOVERED
- **Source:** National Security Archive Briefing Book #862, "The Pinochet Regime Declassified: DINA: 'A Gestapo-Type Police Force' in Chile" (ed. Peter Kornbluh & John Dinges, published June 18, 2024), Documents 14–15; corroborated in Kornbluh, *The Pinochet File*, p.180.
- **Tier:** [P] — declassified CIA and State Department cables, freely viewable online.
- **Verbatim:** Document 14: "CIA, National Intelligence Daily Cable, [DINA Dissolution], Top Secret, August 13, 1977" (source: Clinton Chile Declassification Project). Document 15: U.S. Embassy Santiago cable, "The DINA/CNI Transformation," Aug 19, 1977, quoted directly: **"the functions and the language of the decrees establishing DINA in 1974 and now CNI are almost identical"** and **"Should this reform prove to be no more than a change in name, the GOC will stand to lose irreparably."** The Archive's own framing text (not the cable itself) states: "U.S. intelligence reports and Embassy assessments noted that the rebranding of the Chilean secret police was **largely cosmetic**" — an exact match to the dossier's wording. Kornbluh's book (p.180, raw-read) independently corroborates: "On August 13, 1977, the Junta issued decree law No. 1876 abolishing DINA... A second decree, No. 1878, issued the same day, established the National Center for Information, CNI... But Contreras remained as director, meaning that this change in the structure of the secret police was in name only."
- **Showable file:** https://nsarchive.gwu.edu/briefing-book/chile/2024-06-18/pinochet-regime-declassified-dina-gestapo-type-police-force-chile (Documents 14 & 15 are individually viewable declassified cables)
- **How verified:** fetched the NSA URL directly and stripped it to plain text myself; raw-read of Kornbluh p.180 via `source_get_content` grep.
- **Notes:** this upgrades the dossier's citation from "Multiple sources confirm" to an actual named, dated, freely viewable pair of declassified cables — better than the book citation alone.

---

### Orlando Letelier was killed by a remote-control car bomb at Sheridan Circle, Washington, D.C., on September 21, 1976 / Michael Townley placed and detonated the device.
- **Status:** RECOVERED
- **Source:** Dinges & Landau, *Assassination on Embassy Row: The Shocking Story of the Letelier-Moffitt Murders* (1980), pp.19, 153, 155; Dinges, *The Condor Years* (main narrative, opening chapter).
- **Tier:** [S] — narrative reconstruction by the two journalists/scholars most directly embedded in the case, drawing on FBI investigation and Townley's own trial testimony.
- **Verbatim:** "TOWNLEY ADDED the final touches to the bomb as Paz held the parts in place for him... Townley planned to place the bomb under the driver's seat; he molded the plastique to blow the full explosive force directly upward." (p.19, "The Act") "Smith sold him a Fanon-Courier brand paging system consisting of a radio transmitter, a ten-tone encoding device, and six receivers" (p.153); Townley's trial testimony: "Townley described how he received the TNT and C4 explosives and the Fanon-Courier paging device he had modified as a remote control detonator." Dinges, *Condor Years*: "The bomb exploded just as the car entered Sheridan Circle, on a stretch of road known as Embassy Row. Letelier's legs were blown off, and he died almost immediately."
- **Showable file:** none digitized/public-domain found; both are in-notebook PDFs (`a9b0b96e...`, `db37b916...`).
- **How verified:** raw-read via `source_get_content` grep of both books; page numbers for Dinges & Landau confirmed against in-text page-header artifacts ("The Act 19," "Open Season 153/155").

---

### Ronni Moffitt, a 25-year-old American, was killed alongside Letelier when bomb shrapnel severed her carotid artery.
- **Status:** RECOVERED
- **Source:** Dinges, *The Condor Years* (New Press, 2004), narrative passage (opening chapter, no clean page marker recovered from the extraction — same passage covers the Sheridan Circle detonation above).
- **Tier:** [S]
- **Verbatim:** "Ronni Moffitt, in the front seat, caught a piece of shrapnel to the neck, which severed her carotid artery and windpipe. She drowned in her own blood. Michael Moffitt, riding in back and shielded from the main force of the blast, suffered cuts but survived."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep of Dinges' book text.

---

### Michael Townley, a U.S. expatriate recruited by DINA in 1974, led the Letelier assassination and later became a U.S. prosecution witness after his 1978 expulsion from Chile.
- **Status:** RECOVERED
- **Source:** Dinges & Landau, *Assassination on Embassy Row* (courtroom/trial chapter, "A Measure of Justice," ~p.345 area); Dinges, *The Condor Years*.
- **Tier:** [S] — corroborated by Townley's own plea-bargained trial testimony as reproduced in the book.
- **Verbatim:** "Then the jury saw wires, plastic cups, electric matches—the stuff of bombs... Townley explained how these items, when put together, had served to kill Orlando Letelier and Ronni Moffitt." Trial exhibit: "a receipt for a Fanon-Courier paging device."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep.

---

### Operation Condor operated in three phases (intelligence-sharing, cross-border kidnapping/torture centered on Automotores Orletti, and international assassination missions codenamed Teseo).
- **Status:** RECOVERED
- **Source:** Dinges, *The Condor Years*, pp.10–17 and 116–124 (page range confirmed via the book's own back-of-book index: "three phases, 10–17, 116–24"); corroborated structurally by McSherry, *Predatory States*, chs. 3–5 (pp.69, 107, 139 — table of contents: "Ch.4 Condor's Killing Machine: Phase II Transnational Operations," "Ch.5 Phase III: Condor's Assassination Capability").
- **Tier:** [S]
- **Verbatim:** "Phase One—intelligence exchange, the data bank, and communications system—and Phase Two—joint operations in one another's countries—had been working well... Now Chile, Argentina, and Uruguay—the three most militant countries—agreed to move to Phase Three: joint operations outside of Latin America to track down and assassinate enemies who were operating from exile."
- **Showable file:** none digitized; in-notebook PDFs.
- **How verified:** raw-read via `source_get_content` grep on both books; index cross-check for page numbers.
- **Notes:** Lessa's newer scholarship (*The Condor Trials*, 2022) proposes a broader five-phase periodization of "transnational repression" (of which Condor is the "apex" three-year phase) — this doesn't contradict the three-phase Condor-specific framework, it contextualizes it. Worth knowing if a future script wants to cite Lessa instead of Dinges/McSherry for this claim.

---

### The commonly cited figure of 60,000 refers to Uruguayan civilians detained (1 in every 50 citizens), not the death toll of Operation Condor as a whole.
- **Status:** RECOVERED
- **Source:** Cameselle-Pesce & Sharnak (eds.), *Uruguay in Transnational Perspective* (Routledge, 2023), ch.1, endnote 10.
- **Tier:** [S→P] — the chapter's own endnote cites the ultimate primary source directly.
- **Verbatim:** "The 1989 Uruguay: Nunca Más report highlighted the Orwellian character of Uruguay's totalitarianism... A total of 1 in every 50 citizens (or more than 60,000 civilians) was detained, with over 7,000 long-term political prisoners and an estimated 20,000 detainees." Cited to: Servicio Paz y Justicia, *Uruguay, Nunca Más: Human Rights Violations, 1972–1985*, trans. Elizabeth Hampsten (Temple University Press, 1992) — Uruguay's own truth-commission-style report.
- **Showable file:** none digitized found for the Nunca Más report itself; in-notebook PDF for the citing chapter.
- **How verified:** raw-read via `source_get_content` grep.

---

### Italy sentenced Uruguayan officer Jorge Troccoli to life imprisonment in 2019, and its Court of Cassation ratified the sentence in 2021, leading to his arrest.
- **Status:** RECOVERED (with a minor number caveat)
- **Source:** Lessa, *The Condor Trials* (Yale University Press, 2022), ch. "Justice Across the Atlantic" (~pp.235–254).
- **Tier:** [S] — court-record-based scholarly account.
- **Verbatim:** "In 2019 the Assize Appeals Court condemned twenty-four Uruguayan, Chilean, Peruvian, and Bolivian defendants to life terms for the murders of thirty-eight Italian and Uruguayan citizens... On July 9, 2021, the Court of Cassation (Italy's highest court) ratified the life sentences of eleven Uruguayan and three Chilean officials; consequently, Troccoli (the only convict who lives in Italy) was arrested the following day and taken to Salerno's prison."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep.
- **Notes:** The dossier's specific figure of "20 Uruguayan victims" for Troccoli individually was not found verbatim in this passage — the 2019 sentence covered 24 defendants collectively for 38 Italian+Uruguayan victims. Not contradicted, just not independently confirmed at this granularity in the raw text I could search; flagging so it isn't over-stated on screen as a Troccoli-specific number.

---

### The October 1998 arrest of Augusto Pinochet in London on a Spanish warrant established the modern concept of universal jurisdiction and triggered hundreds of new criminal complaints in Chile.
- **Status:** RECOVERED
- **Source:** Wright, *Impunity, Human Rights, and Democracy: Chile and Argentina, 1990–2005* (2007), pp.90–91 (page confirmed via in-text running header "90 Impunity, Human Rights, and Democracy" immediately preceding the quote).
- **Tier:** [S]
- **Verbatim:** "In an event that sent shock waves around the world, Pinochet was arrested in London on October 16, 1998, on an extradition warrant from Judge Garzón charging him with torture, murder, and hostage-taking."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep.

---

### Chile's 1978 Decree Law 2191 granted a blanket amnesty for dictatorship-era crimes, later circumvented by courts treating forced disappearance as an ongoing "permanent kidnapping."
- **Status:** RECOVERED
- **Source:** Roht-Arriaza, *The Pinochet Effect: Transnational Justice in the Age of Human Rights* (Pennsylvania Studies in Human Rights, University of Pennsylvania Press, 2005/2011), pp.70–71 (page confirmed via in-text running header "The Investigations Come Home to Chile 71" immediately following the quote).
- **Tier:** [S]
- **Verbatim:** "An even greater obstacle was (and is) the 1978 self-amnesty law. Decree-Law 2191 of April 18, 1978 applied a global amnesty to 'all persons who committed ... criminal offenses during the period of the state of siege, between 11 September 1973 and 10 March 1978.' ... murder, kidnapping, and assault were not [excluded]."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep.
- **Notes:** the source itself contains an unrelated error in the same passage — it dates the Letelier-Moffitt bombing to "1975" instead of 1976. Our dossier already has the correct 1976 date elsewhere and does not repeat this error, so no action needed — flagging only so it isn't picked up if this source is used again.

---

### Argentina's amnesty laws (1986 Punto Final, 1987 Due Obedience) were declared unconstitutional by a judge in 2001, ratified by the Supreme Court in 2005.
- **Status:** RECOVERED
- **Source:** Wright, *Impunity, Human Rights, and Democracy*, Preface + pp.101–102 (page confirmed via in-text running header "102 Impunity, Human Rights, and Democracy").
- **Tier:** [S]
- **Verbatim:** Preface: "By 2004, the armed forces' institutional resistance to justice ended... The following year, the Argentine Supreme Court ruled amnesty laws enacted in 1986 and 1987 unconstitutional..." Body (pp.101-102): "In a major turning point, federal Judge Gabriel Cavallo, citing international jurisprudence and the Inter-American Commission's and Court's stance on the invalidity of amnesties, ruled the punto final and due obedience laws unconstitutional in March 2001. Other courts followed Cavallo's groundbreaking decision, and the Buenos Aires Appeals Court upheld the rulings in November 2001."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep.

---

### Uruguay repealed its amnesty law, the Ley de Caducidad, in October 2011, following the Inter-American Court's Gelman ruling.
- **Status:** RECOVERED
- **Source:** Lessa, *The Condor Trials*, p.155 (page confirmed via in-text running header "J u s t i C e s e e k e r s 155" immediately following the quote).
- **Tier:** [S]
- **Verbatim:** "Eventually, on October 27, [Uruguay's] Parliament approved Law 18.831, which effectively repealed the impunity law almost twenty-five years after its sanctioning. The joint efforts of impunity challengers and strategic facilitators also benefited from the international pressure generated by the Gelman v. Uruguay sentence dictated just a few months earlier by the Inter-American Court of Human Rights."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep.

---

### Brazil's role in Operation Condor is contested: officially limited to intelligence exchange, but records show Brazilian agents present at torture sessions and abductions.
- **Status:** RECOVERED
- **Source:** Dinges, *The Condor Years* (main narrative, Phase Three chapter).
- **Tier:** [S→P] for the "official limitation" half (Dinges quotes a CIA report directly); [S] for the torture-session-presence half (based on Paraguayan Archives of Terror survivor testimony as related by Dinges).
- **Verbatim (official limitation):** CIA report, three days after the Letelier assassination, titled "Operation Condor Goes Forward": **"With the Brazilian decision to confine its activities to the territorial limits of the Condor nations, training has begun in Buenos Aires for Argentine, Chilean and Uruguayan agents, who will operate in Western Europe."** **Verbatim (Brazilian presence at interrogations):** describing a Paraguayan interrogation session, "Several prisoners interviewed said they could tell from the questions and accents that the visitors included Chileans, Argentines, Uruguayans, and Brazilians."
- **Showable file:** none digitized; in-notebook PDF.
- **How verified:** raw-read via `source_get_content` grep.

---

## Summary

| Status | Count |
|---|---|
| RECOVERED | 12 |
| UNVERIFIED | 0 |
| CONTRADICTED | 2 (CIA "Logistics Department" encryption-machine claim; Contreras "Fort Belvoir" training detail) |

**Loudest flags for the invoker:**
1. **CIA encryption-machine claim is misframed as "declassified documents."** It actually rests on third-hand oral testimony (Fortún → Irusta's self-published 1995/97 Bolivian book) that both citing scholars (McSherry, Dinges) explicitly hedge. A **genuinely declassified, better, freely-viewable** alternative exists: NSA Briefing Book #696 ("The CIA's 'Minerva' Secret") shows Condor used compromised Crypto AG machines the CIA/BND covertly owned — a stronger on-screen claim, sourced to four dated cables.
2. **"Fort Belvoir, Virginia, 1967-1969" for Contreras is not supported anywhere in the research notebook and contradicts the best available biography**, which places his U.S.-linked training at the School of the Americas, Fort Gulick, Panama Canal Zone, in 1967. This should be corrected if the video is ever re-edited or referenced again.
3. Minor: the "20 Uruguayan victims" figure specific to Troccoli wasn't independently confirmed at that granularity — the 2019 sentence covered 24 defendants collectively for 38 victims.

OUTPUT: D:/History vs Hype/video-projects/_ARCHIVED/published/34-operation-condor-2025/_research/ATTRIBUTION-RECOVERY.md
