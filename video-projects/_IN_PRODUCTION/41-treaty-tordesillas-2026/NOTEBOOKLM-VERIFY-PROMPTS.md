# NotebookLM Verification Prompts — Tordesillas Transcript Claims

**Purpose:** Copy-paste into NotebookLM to verify claims and extract on-screen quotes.
**Grouped by source** for efficiency — run one prompt per source notebook.

## STATUS (2026-03-06)

**PROMPTS 1-7:** Mostly resolved via direct PDF verification + web search. 46/50 claims verified.
**REMAINING:** 2 partially verified claims (Prompt 8 below) + on-screen quote extraction (Prompt 9).
**NEW:** Script-preparation prompts (Prompt 10) for strongest audio material.

---

## PROMPT 1: Miller (Discovering Indigenous Lands) + Williams (American Indian in Western Legal Thought)

```
I need to verify the following claims using the sources you have access to. For each claim, provide:
1. VERDICT: VERIFIED / INACCURATE / PARTIALLY TRUE / NO EVIDENCE FOUND
2. EXACT QUOTE from source with page number
3. NUANCE: What context or complexity does the source add?

CLAIM 1: In City of Sherrill v. Oneida Indian Nation (2005), the U.S. Supreme Court cited the Doctrine of Discovery to prevent a tribe from reasserting sovereignty over land they had REPURCHASED. What exactly did the Court rule and what was their reasoning?

CLAIM 2: In Tee-Hit-Ton Indians v. United States (1955), the Court described indigenous land rights as "permission from the whites to occupy." Is this the exact quote? What page in Miller?

CLAIM 3: Marshall relied on the "Norman Yoke" concept (post-1066 feudal logic that all land belongs to the Crown) in Johnson v. M'Intosh. Does Williams discuss this?

CLAIM 4: Williams argues that if the Supreme Court had ruled Indians had full ownership in Johnson v. M'Intosh, the U.S. would have gone bankrupt — because the government had already sold millions of acres of frontier land to pay Revolutionary War debts. What exactly does Williams say about this economic motivation?

CLAIM 5: Williams states that Romanus Pontifex was NOT generated in the Vatican — it codified legal opinions of two specific canonists, Antonio Manucci and Antonio Roselli, commissioned by King Duarte of Portugal. Is this accurate? What page?

Use [1], [2] citation markers in your response.
```

---

## PROMPT 2: Anghie (Imperialism, Sovereignty and International Law)

```
I need to verify the following claims about Francisco de Vitoria and international law using Anghie's text. For each claim, provide:
1. VERDICT: VERIFIED / INACCURATE / PARTIALLY TRUE / NO EVIDENCE FOUND
2. EXACT QUOTE from source with page number

CLAIM 1: Vitoria argued that because indigenous peoples possess human reason, they are bound by the universal jus gentium (law of nations). Under this framework, the Spanish had three specific "natural rights": (a) right to travel/sojourn anywhere, (b) right to trade/commerce, (c) right to preach the gospel. Any indigenous resistance to these = violation of jus gentium = legal justification for "just war." Is this accurate? What pages?

CLAIM 2: Anghie argues that international law was NOT created in Europe and then exported — it was built out of the colonial encounter itself. It was specifically designed to manage the subjugation of different cultures. What is his exact argument and where does he make it?

CLAIM 3: Anghie describes a "dynamic of difference" — international law creates a conceptual gap between "civilized" and "uncivilized," uses the gap to justify conquest, then introduces "civilizing" techniques that NEVER close the gap, generating endless new justifications for domination. Is this the right framing? What pages?

CLAIM 4: Vitoria created an additional exception allowing conquest if infidel rulers "tyrannize their own people" (e.g., human sacrifice), providing a "humanitarian intervention" justification. Does Anghie discuss this?

Use [1], [2] citation markers.
```

---

## PROMPT 3: Schwartz (Early Brazil) + Disney (Portuguese Empire)

```
I need to verify the following claims. For each, provide VERDICT, EXACT QUOTE with page number, and any nuance.

CLAIM 1: A German newsletter "Copia der Newen Zeitung auss Presillg Landt" (1514), discussed by Schwartz around p.10, was likely written by a German merchant in Madeira. It reports a ship loaded with brazilwood below deck, and "above deck... full of purchased young boys and girls." Is this the correct quote and page?

CLAIM 2: Caminha's letter (May 1, 1500) called Brazil "the island of the True Cross" (ilha de Vera Cruz) — they believed they had found an island, not a continent. Does Schwartz discuss this around p.9?

CLAIM 3: Spain vs. Portugal colonization contrast: Spain found Aztec/Inca empires with centralized taxation and labor systems, so Spain could "decapitate the indigenous leadership and place themselves at the top of an already functioning imperial machine." Portugal found no stone cities — diverse, semi-nomadic Tupi groups. Does Schwartz make this comparison?

CLAIM 4: The donatario (captaincy) system: 15 horizontal bands given to 12 men (lesser nobility, courtiers, soldiers). Each strip extended from coast to the Tordesillas line inland. Crown had no treasury — franchised colonization as private venture capital. Most captains went bankrupt, were killed, or never visited. Is this accurate? What pages in Disney or Schwartz?

CLAIM 5: French incursions harvesting brazilwood (the red dye wood that eventually gave the colony its name) forced Portugal to formalize settlement via the donatario system in the 1530s. Is this accurate?

CLAIM 6: King Afonso V sought Dum Diversas. King Duarte commissioned the legal framework for Romanus Pontifex. Are these the correct kings?

CLAIM 7: The Volta do Mar — swinging far west into the Atlantic to catch trade winds — was King John II's practical reason for demanding the line move from 100 to 370 leagues. At 100 leagues, Portuguese ships would enter Spanish territory during routine Cape navigation. Does Disney discuss this?

Use [1], [2] citation markers.
```

---

## PROMPT 4: Seed (Ceremonies of Possession)

```
I need to verify two specific claims from Patricia Seed's work. For each, provide VERDICT, EXACT QUOTE with page number.

CLAIM 1: Around pp.143-144, Seed discusses Portuguese preference for abstract mathematical boundaries (no physical landmarks, purely conceptual/astronomical) vs. English preference for natural landmarks (specific trees, rivers, rock formations). She traces this to medieval Portuguese property law vs. English land charters. Tordesillas as the "ultimate expression of the Portuguese mathematical mindset." Is this accurate?

CLAIM 2: Around p.132, Seed describes padrao stone pillars as 6-8 feet tall, brought from Lisbon in cargo holds, topped with a square stone block carved with the year and King's coat of arms, crowned with a cross. The core Portuguese sovereignty claim was the act of measuring latitude with an astrolabe — "you possessed land by mathematically locating it in the heavens." Is this accurate?

Use [1], [2] citation markers.
```

---

## PROMPT 5: Laudares & Valencia Caicedo (Tordesillas paper)

```
I need to verify several specific data points from the Laudares & Valencia Caicedo paper. For each, provide VERDICT and exact page number.

CLAIM 1: Table 3 (around p.55) shows a -0.0794 ratio gap between Black and white incomes based on which side of the Tordesillas line a town falls on. Is this the correct figure and page?

CLAIM 2: Around p.17, the OLS results show that a 1% increase in enslaved population in 1872 correlates with a 0.03 increase in modern Gini index AND a 25% drop in average Black household income relative to white household income. Is this accurate?

CLAIM 3: The 0.04 Gini point finding has 99% confidence / p-value < 0.01. What is the actual statistical significance reported?

CLAIM 4: The researchers used a "Donut RD" approach (citing Bereca et al. 2011), excluding municipalities within 1 degree of longitude (~73 km) of the estimated line. Final causal estimates come from the 73-500 km range using 2,468 municipality observations. Is this accurate? What page (around p.18)?

CLAIM 5: Around p.16, the 2010 Gini index shows a "statistically significant spike in economic inequality exactly at 48.7 degrees west" — 260 years after the treaty was formally scrapped. Is this the right framing and page?

CLAIM 6: On p.3, Laudares describes the legal architecture as existing BEFORE the physical reality was confirmed — an "a priori foundation" that set Brazil's legal destiny six years before anyone landed. Is this the right quote and page?

Use [1], [2] citation markers.
```

---

## PROMPT 6: Rossi (Tordesillas Syndrome, Cornell ILJ)

```
I need to verify these claims from Rossi's article. For each, provide VERDICT, EXACT QUOTE with page number.

CLAIM 1: Rossi distinguishes between dominium (property ownership over resources) and imperium (sovereign jurisdiction/right to rule), arguing that the Treaty of Tordesillas fused both. Modern UNCLOS tries to separate them, but powerful nations keep collapsing them back together. What pages?

CLAIM 2: Rossi traces UNCLOS back to Hugo Grotius's Mare Liberum (Freedom of the Seas) concept and frames the China/South China Sea dispute as a relapse into Tordesillas-style ocean enclosure. What pages?

CLAIM 3: The South China Sea carries $5 trillion in annual commercial activity and one-third of all global maritime traffic. Does Rossi cite these figures? What page?

CLAIM 4: The 2016 Hague Tribunal ruled against China's nine-dash line under UNCLOS. Does Rossi discuss this ruling?

Use [1], [2] citation markers.
```

---

## PROMPT 7: Cross-Source Verification (Quick Checks)

```
Quick verification across all sources:

1. Did the Vatican's 2023 repudiation specifically cite Sublimis Deus (1537, Pope Paul III) — declaring indigenous peoples rational humans who shouldn't be enslaved — as representing the Church's "true teaching"? Is this their justification for NOT rescinding the original bulls?

2. The Relacao (high court) was established in Bahia in 1609. Can any source confirm this date?

3. In modern Brazilian Portuguese, does "legal" colloquially mean "cool" or "good"? Any source reference?

4. The bandeirantes — Portuguese frontier explorers/slavers who pushed deep into the Amazon and Mato Grosso, establishing uti possidetis facts on the ground. Which source discusses them most thoroughly?

5. Pope Innocent IV (not Innocent V) established three specific triggers for papal intervention over non-Christians: (a) they violated natural law, (b) they threatened Christians' spiritual welfare, (c) they refused missionaries. Does Muldoon discuss these triggers? What page?

Use [1], [2] citation markers.
```

---

---

## PROMPT 8: Remaining Partially Verified Claims (PRIORITY)

**Run in:** Williams/Muldoon notebook + Schwartz (Sovereignty and Society) notebook

```
I need to resolve two partially verified claims. For each, provide VERDICT, EXACT QUOTE with page number, and any corrections.

CLAIM 1: Robert Williams states that Romanus Pontifex (1455) codified legal opinions of two specific canonists named "Antonio Manucci" and "Antonio Roselli," commissioned by King Duarte of Portugal.
- Are these the correct names?
- What pages in Williams?
- NOTE: King Duarte died in 1438, before Romanus Pontifex (1455). Did Duarte commission the legal framework that was completed under Afonso V's reign? Or is the attribution to Duarte incorrect?

CLAIM 2: Stuart Schwartz's book "Sovereignty and Society in Colonial Brazil" discusses letrados (magistrates) trained at the University of Coimbra in Roman law who served as the institutional backbone of Portuguese colonial administration. The Relacao (high court) was established in Bahia in 1609.
- Can you confirm the 1609 date for the Bahia Relacao?
- Does Schwartz describe the letrados as the primary mechanism of crown control over the donatario system?
- What specific pages discuss this?

Use [1], [2] citation markers.
```

---

## PROMPT 9: On-Screen Quote Extraction (SCRIPT PREP)

**Run in:** Main Tordesillas notebook (all 21 sources)

```
I am writing a YouTube script about the Treaty of Tordesillas. I need SHORT, PUNCHY quotes (under 25 words each) that can be displayed on screen while I narrate. Each quote must be exact, word-for-word from a source, with author and page number.

Find quotes for these specific script moments:

1. THE AUDACITY — A quote capturing how absurd it was for two countries to divide the entire world. Something expressing shock, irony, or the scale of the presumption.

2. THE UNMEASURABLE LINE — A quote about the impossibility of measuring longitude in 1494 or the failure to determine where the line was. Disney's "no means of determining precisely where the line ran" is good — any others?

3. THE REQUERIMIENTO ABSURDITY — Las Casas saying he "did not know whether to laugh or to cry." Any other contemporary reactions to the Requerimiento being read to empty beaches?

4. THE SLAVERY PIPELINE — A quote capturing the scale or horror of the Portuguese slave trade in Brazil. The German newsletter quote about "purchased young boys and girls" works — any other early primary source quotes?

5. THE MODERN GHOST — A quote from Laudares/Valencia Caicedo capturing the finding that inequality is STILL measurable at the treaty line. Something data-driven and shocking.

6. THE VATICAN GAP — A quote from the 2023 Vatican statement that sounds strong but, in context, changes nothing legally. The "repudiates those concepts" quote — any others that reveal the gap between rhetoric and legal reality?

7. FRANCIS I RESPONSE — Pagden quotes Francis I of France demanding to see "the clause in Adam's will" that gave Spain half the world. Is this the exact quote? Page number?

For each, provide:
- Exact quote (word-for-word)
- Author, title, page number
- Script context: what point does this support?

Use [1], [2] citation markers.
```

---

## PROMPT 10: Script-Ready Mechanism Explanations (NEW MATERIAL)

**Run in:** Main Tordesillas notebook (all 21 sources)

```
I'm building the "HOW mechanism" section of my script — explaining the logistics of how the Treaty of Tordesillas actually worked in practice. My audience subscribes for logistics and systems, not political commentary. I need source-grounded explanations for these three mechanisms:

MECHANISM 1: THE DUAL MONOPOLY
Romanus Pontifex (1455) gave Portugal monopoly on the African coast. Tordesillas (1494) gave them eastern South America. Together, they controlled BOTH shores of the South Atlantic — the supply of enslaved people AND the destination. Spain had to use the asiento licensing system.

Question: Walk me through exactly how this dual monopoly worked in practice. What was the asiento system? How did Portuguese merchants profit from Spain's labor needs? What specific trading posts (feitorias) in Africa fed the Brazil pipeline? Cite exact sources and pages.

MECHANISM 2: THE DONATARIO FRANCHISE MODEL
King Joao III divided the coast into 15 captaincies and gave them to 12 men to colonize at their own expense — essentially franchising colonization.

Question: Which captaincies succeeded and why? Which failed? How did the failure of this system lead to centralized royal government (Tome de Sousa, 1549)? What was the connection between sugar cultivation and the demand for enslaved labor? Cite Schwartz and Disney with page numbers.

MECHANISM 3: THE BANDEIRANTE BREACH
Portuguese settlers pushed far beyond the Tordesillas line into the interior, establishing uti possidetis facts on the ground that the Treaty of Madrid (1750) eventually recognized.

Question: What specifically drove the bandeirantes west? Was it gold, slaves, or territorial ambition? How far beyond the treaty line did they actually go? What was Alexandre de Gusmao's argument for abandoning the Tordesillas line? Cite Disney with page numbers.

For each mechanism, provide:
- The key facts with page citations
- One or two short quotes I can use on screen
- Any counterarguments or nuances I should acknowledge

Use [1], [2] citation markers.
```

---

## PROMPT 11: Customized Audio Overview — Act-by-Act Script Prep

**Run in:** Main Tordesillas notebook (all 21 sources)
**Use:** Click "Customize" before generating Audio Overview

```
Generate an audio overview structured as a 3-act conversation between the hosts:

ACT 1 (5 min): THE LINE AND THE MAP
Focus on: The Treaty of Tordesillas itself — the 1493 Inter caetera line, Portugal's pushback, the 370-league compromise, the Volta do Mar as practical motivation, the unmeasurable longitude problem, and the joint survey that never happened. Use Disney, the treaty text, and Laudares.

ACT 2 (7 min): THE MACHINE
Focus on: How the treaty created a functioning colonial economic system. The dual monopoly (Romanus Pontifex + Tordesillas = both shores of the Atlantic). The donatario franchise model. The German newsletter of 1514 showing slavery from the very first decade. The Spain vs. Portugal colonization contrast. The letrados and legal infrastructure. Use Schwartz, Boxer, Disney, Laudares.

ACT 3 (5 min): THE GHOST IN THE DATA
Focus on: Modern consequences. The Laudares regression discontinuity finding (2,628 vs 1,184 slaves, 0.04 Gini points in 2010). The Vatican's 2023 repudiation and why it changes nothing legally. The South China Sea as "Tordesillas Syndrome." End with the question: are we about to write a new Tordesillas for space? Use Laudares, Rossi, the Vatican statement.

IMPORTANT: Cite specific page numbers from the sources. When quoting, use exact language. Focus on MECHANISMS and LOGISTICS, not moral judgments — the audience cares about HOW systems work.
```

---

## After Running These Prompts

For each verified claim, update `01-VERIFIED-RESEARCH.md`:
- Change ⏳ to ✅ VERIFIED (with page number)
- Change ⏳ to ❌ INACCURATE (with correction)
- Add exact quotes for on-screen display where provided
