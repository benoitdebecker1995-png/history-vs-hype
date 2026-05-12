# NotebookLM Research Prompts — Vichy Statut des Juifs

**Project:** 37-untranslated-vichy-statut-juifs-2026
**Notebook:** Single notebook with all sources
**Created:** 2026-02-19

**Tip:** After each NotebookLM response, copy to a `.txt` file and run:
```
python tools/citation_extractor.py response.txt
```

---

## Prompt 1: Verify Core Claims

```
I need to verify the following claims about the Vichy Statut des Juifs (October 3, 1940) using the sources you have access to:

CLAIM 1: The Statut des Juifs was a French initiative — Germany did NOT request anti-Jewish legislation from Vichy as part of the armistice or otherwise.

CLAIM 2: Raphaël Alibert (Minister of Justice, Action Française member) was the principal drafter of the statute.

CLAIM 3: The German ordinance of September 27, 1940 for the occupied zone was limited to a census of Jews and registration of Jewish property — it did NOT include professional exclusions.

CLAIM 4: The French statute of October 3, 1940 was BROADER in scope than the German September 27 ordinance — covering professional exclusions, a racial definition, and extending to all French colonies.

CLAIM 5: Pétain personally annotated a draft of the statute, making every change harsher (expanding the definition of Jewish, removing protections for established families, eliminating veteran exceptions, adding professions to the ban).

CLAIM 6: Serge Klarsfeld announced the discovery of Pétain's annotated draft on October 3, 2010 at the Mémorial de la Shoah.

CLAIM 7: The armistice of June 22, 1940 contained NO provisions regarding Jews.

For each claim, provide:
1. VERDICT: VERIFIED / INACCURATE / PARTIALLY TRUE / NO EVIDENCE FOUND
2. EXACT QUOTE from source with page number
3. NUANCE: What context or complexity does the source add?
4. COUNTER-EVIDENCE: What do other sources say that contradicts or complicates this?

Use [1], [2] citation markers in your response and include a SOURCES section at the end with:
1. Author, "Title", p. XX
```

---

## Prompt 2: French Antisemitism Before Vichy

```
I'm arguing that the Vichy Statut des Juifs grew from French antisemitic traditions, not German pressure.

Help me build the evidence for FRENCH antisemitism predating the occupation:

1. What was the role of Action Française and Charles Maurras in French antisemitism?
2. What was the Dreyfus Affair's lasting impact on French political culture?
3. Were there anti-Jewish measures or proposals in France BEFORE 1940?
4. What antisemitic legislation did Vichy pass BEFORE the October 3 statute (e.g., repeal of Marchandeau Law on August 27, naturalization review commission on July 22)?
5. How does Paxton characterize the relationship between French antisemitic tradition and Vichy policy?

For each point, provide:
- EXACT QUOTE from source with page number
- Who makes this argument (scholar name)
- What evidence they cite

Use [1], [2] citation markers and include a SOURCES section at the end.
```

---

## Prompt 3: Quote Extraction (for On-Screen Display)

```
I need quotable excerpts from the uploaded sources about the Vichy Statut des Juifs and French responsibility for anti-Jewish legislation.

Requirements for each quote:
- Under 30 words (fits on screen)
- Self-contained (makes sense without context)
- Authoritative (clearly from expert analysis)
- Visually presentable (no dense academic jargon)

For each quote provide:
1. The exact quote word-for-word
2. Author name and credential
3. Book title and page number
4. Brief context: what point does this support?

Find 5-7 quotes covering these themes:
- French initiative (not German orders)
- Pétain's personal involvement
- The scope/severity of the statute
- The myth of German coercion
- French reckoning with Vichy past

Include [1], [2] citation markers and a SOURCES section at the end.
```

---

## Prompt 4: Article-by-Article Academic Analysis

```
I'm doing a clause-by-clause reading of the Statut des Juifs (October 3, 1940) for a YouTube video.

For each article of the statute (Articles 1-10), tell me:

1. What do the uploaded sources say about HOW this article was drafted?
2. Were there earlier drafts that differed? (especially re: Pétain's annotations)
3. How did this article compare to the German Nuremberg Laws or the September 27 ordinance?
4. What was the PRACTICAL IMPACT of this article? (How many people affected, which institutions, what happened?)
5. Any specific cases or stories of individuals affected by this article?

For Articles 1 (definition) and 2 (professional exclusions) especially, I need detailed analysis.

Use [1], [2] citation markers. Include a SOURCES section at the end with page numbers.
```

---

## Prompt 5: Counter-Evidence and Steelmanning

```
I'm arguing that France wrote the Statut des Juifs independently, without German pressure.

Help me steelman the opposing view:

1. What is the STRONGEST counter-argument found in these sources? Did the German occupation create conditions that enabled French antisemitism to become law?
2. Is there any evidence of German pressure, even indirect, on Vichy regarding Jewish policy?
3. What do historians say about whether Vichy was trying to PREEMPT German demands — acting first to maintain sovereignty over Jewish policy?
4. Were there Vichy officials who later claimed they acted to "protect" French Jews from harsher German measures? How do historians evaluate this claim?
5. What does the "shield thesis" (Vichy as shield protecting France from worse German measures) look like, and how has scholarship assessed it?

For each counter-argument, provide:
- The argument in its strongest form
- Who makes this argument (scholar name)
- What evidence they cite
- Page numbers for all claims

Use [1], [2] citation markers and include a SOURCES section.
```

---

## Prompt 6: Timeline with Academic Citations

```
Using the uploaded sources, create a chronological timeline of Vichy France's anti-Jewish policy from June 1940 to June 1941 (armistice through second Statut des Juifs).

For each timeline entry, provide:
1. EXACT DATE
2. WHAT HAPPENED (one sentence)
3. CITATION: [Author, Book, p. XX]

Focus on events that show:
- French government actions BEFORE any German anti-Jewish demands
- The escalation pattern from first statute to second statute
- Key decisions that demonstrate French initiative vs German pressure

Also include:
- The Marchandeau Law repeal (Aug 27, 1940)
- The naturalization review commission (July 22, 1940)
- The Crémieux Decree abrogation (Oct 7, 1940)
- The law on foreign Jews (Oct 4, 1940)
- Any German reactions to French anti-Jewish measures

Use [1], [2] citation markers. Include a SOURCES section at the end.
```

---

## Prompt 7: The Pétain Draft (Deep Dive)

```
I need a detailed analysis of Pétain's annotated draft of the Statut des Juifs discovered in 2010.

From the uploaded sources, tell me:

1. DISCOVERY: When and where was the draft found? Who found it? Where is it now?
2. PHYSICAL DESCRIPTION: What does the document look like? Typed draft with handwritten annotations?
3. SPECIFIC CHANGES: What exactly did Pétain write or cross out? List every known annotation.
4. AUTHENTICATION: Has the handwriting been verified? By whom? Any disputes?
5. HISTORICAL SIGNIFICANCE: How did this discovery change the historical understanding of Pétain's role?
6. BEFORE vs AFTER: What did the draft say BEFORE Pétain's changes vs. the final published version?

For each point, provide exact quotes from sources with page numbers.

Use [1], [2] citation markers and include a SOURCES section at the end.
```

---

## Prompt 8: Colonial Application (Article 9)

```
Article 9 of the Statut des Juifs extends the law to "Algeria, the colonies, protectorate countries, and mandated territories."

From the uploaded sources:

1. How was the statute applied in ALGERIA specifically? What was the Jewish population of Algeria? What was the impact of the separate Crémieux Decree abrogation (Oct 7, 1940)?
2. How was it applied in FRENCH NORTH AFRICA (Morocco, Tunisia)?
3. How was it applied in other colonies or mandated territories (Syria, Lebanon, Indochina)?
4. Were there differences in enforcement across different territories?
5. What do sources say about the colonial dimension being overlooked in English-language scholarship?

Use [1], [2] citation markers and include a SOURCES section at the end.
```

---

## Prompt 9: Modern Reckoning (Chirac → Present)

```
I need to trace France's reckoning with the Vichy Statut des Juifs from 1944 to the present.

From the uploaded sources:

1. How did de Gaulle frame Vichy after liberation? What was the official position?
2. When and how did the Paxton thesis (1972) change French historiography?
3. What was the significance of Chirac's 1995 Vel d'Hiv speech? Exact quotes if available.
4. How was Klarsfeld's 2010 discovery of the Pétain draft received in France?
5. What is the current state of French memory of Vichy? Any ongoing debates?

Use [1], [2] citation markers and include a SOURCES section at the end.
```

---

## Audio Overview Customization

**Paste this into the "Customize" field before generating Audio Overview:**

```
Create a podcast focusing on:

1. SURPRISING FINDINGS: What in these sources contradicts the popular belief that Germany forced Vichy to pass anti-Jewish laws?
2. PÉTAIN'S ROLE: What do the sources say about Pétain's personal involvement, especially the 2010 annotated draft discovery?
3. THE LAW ITSELF: Walk through what the Statut des Juifs actually says — the racial definition, the professional exclusions, the colonial application. What surprises people who actually read it?
4. FRENCH vs GERMAN: How did French anti-Jewish measures compare to and differ from German ones?
5. MODERN IMPACT: How has France reckoned with this history? Chirac 1995, Macron 2017, ongoing debates.

Emphasize:
- Specific page numbers for key claims (I'll need to cite these)
- Direct quotes suitable for video overlay text (under 30 words)
- The timeline proving French initiative (armistice June 22 → statute Oct 3, with NO German request in between)

De-emphasize:
- Biographical background of authors (I need content, not credentials)
- Overly broad summaries of WW2 (I want specifics about this law)
```

---

## After NotebookLM Research

1. Copy each response to `_research/nlm-response-01.txt`, `nlm-response-02.txt`, etc.
2. Run: `python tools/citation_extractor.py _research/nlm-response-01.txt`
3. Review extracted claims
4. Copy verified claims to `01-VERIFIED-RESEARCH.md`
5. When 90%+ verified → run `/script --document-mode`
