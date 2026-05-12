# Thesis Articulation Prompt — for NotebookLM

**Notebook:** [#51 Treaty of Tripoli Article 11 (1797) — Hunter Miller / Arabic Discrepancy](https://notebooklm.google.com/notebook/b05813fc-0a59-4b93-ac34-dd63b9d60114)
**Notebook ID:** `b05813fc-0a59-4b93-ac34-dd63b9d60114`
**Sources already uploaded:** Hunter Miller 1931 vol. 2 (Tripoli passage, pp. 368–384), Hurgronje 1930 annotated translation (within Miller), Senate Executive Journal vol. 1 p. 244, Spellberg 2013 (*Thomas Jefferson's Qur'an*), Lambert 2005 (*The Barbary Wars*), Allison 1995 (*The Crescent Obscured*), Haselby 2015 (*The Origins of American Religious Nationalism*), Crane 2020 (*American Quarterly*), Cobbett 1797 (*Porcupine Gazette*).

---

## Paste this into NotebookLM as one prompt

```
You are a senior editor at a YouTube history channel that practices forensic, document-first historiography ("calm prosecutor" voice). I have just finished researching and scripting a 5-6 minute video about the Treaty of Tripoli's Article 11 — the 1797 ratified clause stating "the government of the United States of America is not in any sense founded on the Christian Religion," which Snouck Hurgronje found in 1930 has no equivalent in the Arabic original of the same treaty. Hunter Miller called this "wholly unexplained" in 1931. Crane (2020) argues the modern secular reading developed gradually across the 19th–20th centuries.

The video assembles strong evidence but lacks an articulable single-sentence THESIS — the takeaway the viewer should carry away. The video gives the audience a story; it doesn't give them an idea.

Using ONLY the sources in this notebook (Hunter Miller 1931, Hurgronje, Senate Executive Journal p. 244, Spellberg 2013, Lambert 2005, Allison 1995, Haselby 2015, Crane 2020, Cobbett 1797), generate FIVE candidate theses for this video. Do not rank them. Present them as a flat menu.

For EACH candidate, provide all six fields:

1. **Thesis sentence (≤12 words).**
   - Must be a CLAIM, not a summary, not an open question, not a "both sides do this" observation.
   - Must be bigger than the case study — the same sentence should plausibly caption an unrelated case (e.g., Sykes-Picot, Tordesillas, Bakassi, Operation Legacy). State which other case it could caption.
   - Must be falsifiable in principle — strong enough to be argued against.

2. **Thesis type.** Pick ONE:
   - Power-asymmetry (who decides what gets ratified, signed, recognized)
   - Time-shifted meaning (what we "always believed" was said is what later generations needed)
   - System-as-designed (the perceived flaw is the actual function)
   - Mechanism-over-narrative (the document/process drives politics, not the other way around)
   - Invisible-until-named (the consequential thing is what nobody noticed)

3. **The single piece of evidence in the notebook that most directly supports this thesis.** Give the source, the exact passage (verbatim, with page number), and a one-sentence reason this evidence anchors the thesis specifically.

4. **Hook tee-up sentence (the investigation question).** A single ≤20-word sentence that promises the viewer the question whose answer is the thesis — without spoiling the thesis itself. (Example structure: "What did the Senate actually ratify?" — promises the answer, doesn't state it.)

5. **Turn evidence — the moment the audience starts forming the thesis themselves.** Identify which single piece of evidence from the notebook, placed at 15–25% of the runtime, will make the audience see the pattern before the script states it. Don't say "the audience will think X" — name the evidence and why this specific evidence carries the thesis without articulating it.

6. **Closing line — exactly ≤12 words, anchored to a named artifact in the video.** The line that lands the thesis as the verdict. Must reference a specific artifact (the English Article 11 / the Arabic letter / the Senate Journal / Hurgronje's note / Miller's "wholly unexplained" / Crane's reading) — not the abstraction. Test: while reading this line, the viewer should be looking at something specific on screen.

Format each candidate as a numbered block (1 through 5), all six fields labeled. Do not preface the menu with commentary. Do not rank or recommend. Do not collapse two candidates that are similar — if two thesis sentences feel close, surface them both and articulate exactly what's different.

After the five candidates, end with one short paragraph (≤80 words) titled "What the notebook does NOT support" — name 1-2 candidate theses that a YouTuber might be tempted to use here that are NOT actually grounded in these sources, and explain in one sentence each why the notebook can't deliver them. (This is to protect against drift toward Christian-nation-debate framings the evidence doesn't actually carry.)

Cite verbatim from the sources at every opportunity. If a thesis cannot be supported by a verbatim passage, do not generate it.
```

---

## Why this prompt is shaped the way it is

- **5 candidates, no ranking** — you apply your instincts uncontaminated. Ranking would push you toward NotebookLM's preference; flat menu lets your read drive.
- **Universality test in the thesis itself** — forces NotebookLM to name another HvH case the same thesis would caption. If it can't name one, the thesis is still a case summary.
- **Verbatim passage requirement** — anchors every candidate to a specific sentence in Hunter Miller / Spellberg / Crane / Haselby. Prevents AI-generated theses that sound profound but aren't in the sources.
- **3-slot mapping (hook tee-up + turn evidence + close line)** — tests whether the thesis is *scriptable*, not just rhetorically clean. A thesis that has no candidate hook tee-up is not a real thesis — it's a slogan.
- **Closing line ≤12 words anchored to a named artifact** — locks the document-first rule from Tripoli's rough cut (Lesson 31 / instinct #7). The thesis must point at something on screen, not at an abstraction.
- **"What the notebook does NOT support" coda** — protects against drift toward "America was founded as a Christian nation" / "America was founded secular" framings that the actual evidence in your notebook can't carry. Keeps you honest.

---

## Workflow once you have the output

1. **You read the 5 candidates uncontaminated.** Apply your instincts. Note which one(s) you're drawn to and why.
2. **Tell me what your instincts point toward.** I'll share my read after — we triangulate.
3. We pick one (or build a hybrid).
4. **If the chosen thesis is different from what the script v5-FINAL implies**, decide whether to:
   - Reshoot a different closing for the Tripoli video (small lift)
   - Keep this video as-is and apply the thesis to a follow-up / sequel
   - Rework the edit to land the thesis (depends on what the rough cut already supports)
5. The chosen thesis goes into the SCRIPT METADATA block per Rule 36, and into the project's PROJECT-STATUS.md as the locked thesis-of-record.

When you've run the prompt and have the output, paste back the 5 candidates (or upload as a file) and I'll respond once you've shared your instincts.
