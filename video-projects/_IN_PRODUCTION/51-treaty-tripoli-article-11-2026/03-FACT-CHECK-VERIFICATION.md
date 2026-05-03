# 03 — Fact-Check Verification (NotebookLM-driven)

**Method:** Every factual claim in `02-SCRIPT-DRAFT.md` was extracted and cross-checked against the academic sources in the NotebookLM notebook (`b05813fc-0a59-4b93-ac34-dd63b9d60114`). Sources used: Hunter Miller 1931 (Tripoli passage), Hurgronje 1930 (within Miller), Spellberg 2013, Lambert 2005, Allison 1995, Haselby 2015, Crane 2020, Senate Executive Journal page 244.

**Date:** 2026-04-24
**Script version reviewed:** v5-FINAL (NLM source_id `33c1a052-104b-4214-8614-83a97c0e6b4a`)

---

## Final summary

| | Count |
|---|---|
| ✅ VERIFIED | 39 |
| ⚠️ PARTIAL | 4 |
| ❌ UNSUPPORTED | 1 |
| 🚨 CONTRADICTED | 1 |
| **TOTAL CLAIMS CHECKED** | **45** |

**Verdict:** Script needed 2 blocking fixes pre-shipping. Both have been applied (see "Fixes applied" below). 4 advisory items remain for review.

---

## Fixes applied (post-NLM critique)

### 🚨 B1 — CONTRADICTED → FIXED
- **Original (v5):** "Barlow sent the document to the Senate."
- **Source:** Miller p. 349 — treaty was submitted to Senate May 29, 1797 via Adams's message of May 26. Treaties are transmitted by the President, not the Consul.
- **Fix applied:** "President Adams transmitted the document to the Senate."

### ⚠️ B2 — PARTIAL (misquote) → FIXED
- **Original (v5):** *"the English text which in the United States has always been deemed the text of the treaty."*
- **Source:** Miller p. 384 — actual phrasing begins "that English text" (the/that swap).
- **Fix applied:** *"that English text which in the United States has always been deemed the text of the treaty."*

---

## Advisory items (non-blocking, your call)

### A1 — ⚠️ Claim #2: "United States Government Printing Office published"
- **Issue:** NLM cannot find the words "Government Printing Office" verbatim in the notebook source excerpts.
- **Reality:** Hunter Miller's *Treaties and Other International Acts of the United States of America* (1931) was published by the U.S. Government Printing Office. This is on the volume's title page (visible in the NLM-uploaded `tripoli miller.pdf` cover). Externally rock-solid.
- **Recommendation:** **KEEP**. Add a footnote to the YouTube description citing Miller, 1931, GPO, Washington as the publisher.

### A2 — ⚠️ Claim #20: "the State Department historian Hunter Miller"
- **Issue:** Miller's title as "State Department historian" not in the uploaded source excerpts.
- **Reality:** Hunter Miller (1875–1956) was the official Editor of Treaties for the U.S. Department of State, 1929–1944. He is also commonly referred to as a State Department historian. External sources rock-solid (Library of Congress, Wikipedia, Department of State Office of the Historian).
- **Recommendation:** **KEEP**. Optional softer phrasing: "the State Department's editor of treaties, Hunter Miller."

### A3 — ❌ Claim #38: "the president of Yale"
- **Issue:** Timothy Dwight's title as "president of Yale" not explicitly stated in the academic-source excerpts NLM had access to.
- **Reality:** Timothy Dwight IV was the 8th president of Yale College, 1795–1817. This is a well-documented, uncontested biographical fact (Yale University's own historical records, Britannica, every standard biographical reference).
- **Recommendation:** **KEEP**. The line is historically airtight even though it's not in the academic excerpts.

### A4 — ⚠️ Claim #42: "most extraordinary, and wholly unexplained" (punctuation)
- **Issue:** Miller's actual phrasing on p. 384 uses parentheses: *"Most extraordinary (and wholly unexplained)"*.
- **Reality:** Spoken delivery doesn't render parentheses. The script-spoken version drops them by necessity. The on-screen text overlay (per ROUGH-STRUCTURE.md visual asset list) should preserve the parentheses for absolute fidelity.
- **Recommendation:** **KEEP** spoken text as-is. **FIX** the visual asset: when this quote appears on screen as a text overlay, render it as *"Most extraordinary (and wholly unexplained)."*

---

## Full claim ledger (45 items)

### Beat 1 — Cold open
1. ✅ "In 1930, a Dutch scholar named Snouck Hurgronje examined the Arabic original of an American treaty." → Spellberg ch. 6; Miller p. 368
2. ⚠️ "The next year, the United States Government Printing Office published what he found." → Miller 1931 vol. (institution not verbatim in excerpts; see A1)
3. ✅ "What he found, the State Department couldn't explain. And almost a hundred years later, neither can anyone else." → Miller p. 384

### Beat 2 — The treaty + Arabic Chekhov's gun
4. ✅ "American merchant ships were being seized. Their crews were being held for ransom." → Allison p. 20; Spellberg ch. 4
5. ✅ "The United States needed a treaty." → Allison p. 20
6. ✅ "That document was the 1796 Treaty of Tripoli." → Miller p. 349
7. ✅ "It was signed at Tripoli on November 4th, 1796..." → Miller p. 349
8. ✅ "...then certified at Algiers in January 1797 by Joel Barlow, the United States Consul to Algiers." → Miller p. 349; Spellberg ch. 6
9. 🚨→✅ FIXED: "President Adams transmitted the document to the Senate." → Miller p. 349 (msg May 26, submitted May 29)
10. ✅ "On Wednesday, June 7th, 1797, the Senate voted on it." → Senate Executive Journal p. 244
11. ✅ "Adams signed the ratification three days later." → Miller p. 349 (June 10, 1797)
12. ✅ "The Arabic original of that same treaty was held, for over a century, in the State Department file." → Miller pp. 382, 384

### Beat 3 — Article 11 read
13. ✅ Verbatim Article 11 text. → Miller p. 365
14. ✅ "The Senate voted yes. Twenty-three senators. None against." → Senate Executive Journal p. 244
15. ✅ "The Senate Journal records it on page 244." → Senate Executive Journal p. 244

### Beat 4 — The Arabic reveal
16. ✅ "The Arabic version of the treaty does not contain Article 11." → Miller p. 384; Hurgronje p. 371
17. ✅ "Not mistranslated. Not paraphrased. Missing." → Miller p. 384 ("does not exist at all. There is no Article 11")
18. ✅ "In 1930, the United States State Department hired a Dutch scholar — Doctor Snouck Hurgronje, of the University of Leiden — to examine the Arabic original." → Spellberg ch. 6 fn 71; Miller p. 368
19. ✅ "He produced an annotated translation." → Miller p. 368
20. ⚠️ "...volume two of a multi-volume work edited by the State Department historian Hunter Miller." → Miller p. 349 (title not in excerpts; see A2)
21. ✅ "And on page 371, Hurgronje wrote this." → Miller p. 371
22. ✅ Verbatim Hurgronje quote about no equivalent in Arabic + Hassan Pasha letter. → Miller p. 371
23. ✅ "Hurgronje read the letter itself." → Miller p. 371
24. ✅ Verbatim Hurgronje "stupid secretary / bombastic words / failed to catch their real meaning." → Miller p. 371

### Beat 5 — Forensic interpretation + Cobbett + Dwight
25. ✅ "Hunter Miller, in 1931, called it..." → Miller p. 384
26. ⚠️→✅ FIXED: Miller verbatim "that English text" (was: "the English text"). → Miller p. 384
27. ✅ "neither Barlow nor any of his American colleagues could read Arabic." → Spellberg ch. 6
28. ✅ "They relied on the consul of Spain to verify the Arabic seals." → Spellberg ch. 6 fn 69
29. ✅ "Barlow attested to the accuracy of the document." → Spellberg ch. 6
30. ✅ Spellberg verbatim "he probably never knew that Article 11 never existed in an Arabic translation." → Spellberg ch. 6
31. ✅ "Which is why, in 1797, almost nobody said a word." → Spellberg ch. 6 ("substantially no contemporary public controversy")
32. ✅ "Adams said nothing publicly. Jefferson — then Vice President — said nothing publicly." → Spellberg ch. 6
33. ✅ "The Senate Journal records no debate on Article 11. None." → Senate Executive Journal p. 244; Spellberg ch. 6
34. ✅ "Historians point to two preserved reactions." → Spellberg ch. 6; Haselby p. 109
35. ✅ "The first came from William Cobbett, a Federalist editor in Philadelphia, in the *Porcupine Gazette* on June 23rd, 1797." → Spellberg ch. 6
36. ✅ Cobbett verbatim "trampling upon the cross." → Spellberg ch. 6
37. ✅ "The second came from Timothy Dwight... and Joel Barlow's former mentor." → Haselby p. 109 ("his wayward protégé")
38. ❌ "the president of Yale" → externally rock-solid (Yale records); not in NLM source excerpts (see A3)
39. ✅ "Per Sam Haselby, on page 109 of his 2015 Oxford monograph." → Haselby p. 109
40. ✅ "Dwight rejected Barlow's radicalism, translated his own replacement Psalms, and took Barlow's portrait down at Yale." → Haselby p. 109

### Beat 6 — Closing
41. ✅ "Hunter Miller, on page 384 of his 1931 volume, called it..." → Miller p. 384
42. ⚠️ "most extraordinary, and wholly unexplained." → Miller p. 384 (parens dropped — see A4)
43. ✅ "In 2020, the historian Jacob Crane published a study in *American Quarterly*." → Crane 2020
44. ✅ Crane's argument about modern reading developing through 19th–20th c. domestic fights. → Crane p. 405
45. ✅ Crane verbatim "wielded as often by Christian nationalists as by militant secularists." → Crane p. 405

---

## Conclusion

**Script status:** FACT-CHECK CLEAR after the 2 blocking fixes (B1 and B2). The 4 advisory items (A1–A4) are stylistic/external-verification items that do not affect script integrity. Recommend keeping the spoken script as-is and applying A4 to the on-screen text overlay only.
