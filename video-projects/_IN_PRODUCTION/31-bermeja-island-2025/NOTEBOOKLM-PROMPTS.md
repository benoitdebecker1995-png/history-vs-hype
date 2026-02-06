# NotebookLM Prompts - Bermeja Island

**Project:** 31-bermeja-island-2025
**Created:** 2026-01-30

---

## AUDIO OVERVIEW CUSTOMIZATION

When generating Audio Overview, click "Customize" and paste:

> Focus on the documentary evidence for Bermeja Island. I need:
> 1. The exact text from the 1539 Santa Cruz atlas describing Bermeja
> 2. What the 2000 Treaty says about maritime boundaries
> 3. The UNAM 2009 scientific findings - exact methodology and conclusions
> 4. Whether there's any geological evidence an island ever existed
>
> Avoid conspiracy theories. Focus on what the documents actually say.

---

## VERIFICATION PROMPTS

### Prompt 1: The 1539 Document
```
What exactly did Alonso de Santa Cruz write about Bermeja Island in his 1539 atlas?
Give me:
- The exact Spanish text (if available)
- English translation
- Any coordinates or positioning information
- Physical description of the island
- Which section of the atlas it appears in

Cite page numbers.
```

### Prompt 2: The 2000 Treaty
```
In the 2000 US-Mexico Maritime Boundary Treaty:
1. Is Bermeja Island mentioned anywhere?
2. How were the EEZ boundaries calculated?
3. What is the "Western Gap" and how was it divided?
4. What percentage did each country receive?
5. What is the 1.4 nautical mile buffer zone provision?

Give exact quotes with article numbers.
```

### Prompt 3: UNAM 2009 Study
```
What did the UNAM 2009 study conclude about Bermeja Island?
Give me:
1. Exact dates of the investigation
2. Ship and equipment used
3. Area and depth surveyed
4. The finding about "5,300 years" - exact quote
5. Names of scientists who led the study
6. Their exact conclusion about whether the island existed

Cite the source document.
```

### Prompt 4: Geological Evidence
```
What geological evidence exists (or doesn't exist) for Bermeja Island?
1. What did sonar/bathymetry show at the coordinates?
2. Is there any evidence of a submerged landmass?
3. What would remain if an island had sunk or eroded?
4. What did scientists say about the "CIA destroyed it" theory?

I need specific scientific findings, not speculation.
```

### Prompt 5: Oil Stakes
```
What were the economic stakes in the Bermeja/Western Gap dispute?
1. What oil reserves are in the Western Gap?
2. How would Mexico's EEZ have changed if Bermeja existed?
3. What is the estimated value of oil in the disputed area?
4. Who made these estimates and when?

I need primary sources for any numbers used.
```

### Prompt 6: Cartographic History
```
How did Bermeja appear on maps for 400 years without anyone checking?
1. Which maps after 1539 showed Bermeja?
2. When did cartographers stop including it?
3. Were there any expeditions to find it before 1997?
4. Is there evidence British maps showed it submerged (1844)?

Give me a timeline of Bermeja on maps.
```

### Prompt 7: The Conspiracy Theory
```
What is the "CIA destroyed Bermeja" conspiracy theory?
1. Who first raised this theory?
2. Which Mexican senators questioned this in 2008?
3. What evidence (if any) supports it?
4. What do geologists say would be required to destroy an island without a trace?

I need this to debunk fairly, not to promote.
```

### Prompt 8: Counter-Evidence
```
Is there ANY evidence that Bermeja Island ever existed?
1. Did any explorer report visiting it?
2. Are there any first-hand accounts?
3. What about the 2012 YouTube video claiming to show it?
4. Could it have been confused with another island (Cayo Arenas)?

I need to steelman the "it existed" position.
```

---

## SCRIPT-BUILDING PROMPTS

### Prompt 9: Key Quotes for On-Screen
```
Give me the 5-7 most important quotes I should display on screen:
1. Santa Cruz's original description
2. The treaty language on boundaries
3. UNAM's conclusion
4. A scientist quote debunking the conspiracy
5. Any quote showing the economic stakes

Format: "Quote" - Source, Page/Date
```

### Prompt 10: Timeline
```
Create a timeline of Bermeja Island:
- 1539: First appearance
- [Other map appearances]
- 1997: First modern search
- 2000: Treaty signed
- 2008: Senate inquiry
- 2009: UNAM study

Include exact dates where available.
```

### Prompt 11: Fact-Check My Claims
```
Verify these claims I found in internet research:
1. "Bermeja was on maps for 382 years" - True?
2. "22.5 billion barrels of oil at stake" - True? Source?
3. "Mexico lost 62% of the Western Gap" - True? (This seems backwards)
4. "No island for 5,300 years" - Exact UNAM finding?
5. "Would require hydrogen bomb to destroy without trace" - Who said this?

Tell me which are verified, which are wrong, which need clarification.
```

---

## AFTER RESEARCH

When done, update `01-VERIFIED-RESEARCH.md` with:
- ✅ for verified claims (with page numbers)
- ❌ for debunked claims
- Exact quotes for on-screen display
- Any new claims discovered

---

*Save responses to Notes in NotebookLM, then transfer to VERIFIED-RESEARCH.md*
