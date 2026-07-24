# Ad-lib Verification Queries — #62 Volhynia (four claims)

**Generated:** 2026-07-15
**Method note (READ FIRST):** `mcp__notebooklm__*` tools were **not available in this session** (tool call returned
"No such tool available"). I could not run live NotebookLM queries against notebook
`d4cab11f-29e9-4e3f-8a42-c055d0e82b8d`. Per the anti-fabrication rule, I did NOT invent quotes or
page numbers. Instead I searched the project's **existing NLM-grounded artifacts**
(`_research/NLM-GROUNDING-BRIEF.md`, which records prior `sources_used`-checked grounding queries
against this same notebook) for anything that already answers these four claims. Where the existing
grounding brief covers a claim, I report it as GROUNDED (citing that file). Where it does not, I mark
the claim **NOT RUN** (not "not supported by the corpus" — simply not yet queried) and specify the
exact query to re-run once NotebookLM MCP access is restored.

**Recommendation:** re-invoke this task (or re-run `/verify` / the `notebook-researcher` agent) in a
session where `mcp__notebooklm__notebook_query` is actually registered, targeting notebook
`d4cab11f-29e9-4e3f-8a42-c055d0e82b8d`, using the four query strings below verbatim.

---

## QUERY 1 — DESERTION MOTIVE (~5,000 auxiliary police, March–April 1943)

**VERDICT: NOT RUN — no prior grounding pass in this notebook covers the desertion motive.**

What the existing `NLM-GROUNDING-BRIEF.md` does confirm (Exhibit 4 timeline, ✅ VERIFIED) is only the
**correlation**, not the causal "why":

> "Systematic mass murders begin: March 1943 (coinciding with ~5,000 Ukrainian auxiliary police
> deserting German service to join UPA)"
> — *Source: McBride pp. 633, 640; Snyder Reconstruction pp. 154, 168ff; Rossoliński-Liebe endnotes 1262–1274 area.* (NLM-GROUNDING-BRIEF.md, Exhibit 4)

That line was itself synthesized language from the earlier grounding pass, not a verbatim quote —
so even the "coinciding with" framing hasn't been round-tripped. **None of the four candidate reasons
you listed (OUN-B recall order / post-Stalingrad fortunes turning / German reprisals / deportation
avoidance) have been tested against McBride specifically.**

**Safe VO phrasing (until re-grounded):** Do not assert a single motive. If the beat is needed before
a re-grounding pass, use the neutral, already-grounded fact only: "That same spring, thousands of
Ukrainian policemen who'd been serving the Germans deserted and joined the UPA" — with no causal claim
attached — OR cut the beat until grounded.

**Query to re-run verbatim once MCP access exists:**
> "In McBride's 'Peasants into Perpetrators' (Slavic Review 2016), what does the source say motivated the roughly 5,000 Ukrainian auxiliary policemen who deserted German service in March–April 1943 to join the UPA? Was it an OUN-B recall/mobilization order, fear following German setbacks (e.g. Stalingrad), German reprisals against the police, fear of deportation to Germany, or a combination? Quote verbatim with page number."

---

## QUERY 2 — TERRITORIAL MOTIVE (killing/removing Poles to fix the post-war border)

**VERDICT: NOT RUN — no prior grounding pass in this notebook tested this specific claim.**

Adjacent material exists in `00-NOTEBOOKLM-SOURCE-LIST.md` (source-selection notes, NOT a grounded
NLM query result) describing Snyder's *Reconstruction of Nations* as covering "why nationalists
ethnically cleansed to pre-empt a future Polish claim" — but that is the research team's own
characterization of what the book is *about*, written before any citation-grounding pass, not a
verified verbatim quote with page number. It cannot be used on screen as-is.

**Safe VO phrasing (until re-grounded):** Do not state the "facts on the ground for a peace
conference" thesis as scholarly consensus. If used, frame as one interpretive layer clearly attributed
("Snyder argues that...") only after grounding — not yet available.

**Query to re-run verbatim once MCP access exists:**
> "Do Snyder ('The Reconstruction of Nations' or 'The Causes of Ukrainian-Polish Ethnic Cleansing 1943') and Motyka (as cited by McBride) support the argument that the OUN/UPA killed or removed Poles from Volhynia specifically so the territory would fall to a future Ukrainian state rather than Poland after the war — i.e., pre-empting a post-war border settlement or repeating the 1918–21 territorial dispute? Quote verbatim with page number, or state if this motive is not supported by the corpus."

---

## QUERY 3 — UPA ANTI-SOVIET INSURGENCY END-DATE

**VERDICT: NOT RUN — not covered in any existing grounding artifact for this project.**

Nothing in `NLM-GROUNDING-BRIEF.md`, `SOURCE-GENEALOGY.md`, or the exhibits index addresses the
post-1945 UPA-vs-Soviet insurgency timeline, Klyachkivsky's 1945 death, or Vasyl Kuk's 1954 capture.
None of these are stated anywhere in this project's research files with a source citation — I am not
reporting the "expected" dates you listed as fact, since they have not been round-tripped against the
notebook.

**Safe VO phrasing (until re-grounded):** Do not state a specific end-date or Kuk's capture year on
screen without grounding.

**Query to re-run verbatim once MCP access exists:**
> "How long did the UPA continue its armed insurgency against Soviet forces after WWII ended? When and how did Klyachkivsky die? When was UPA's last commander, Vasyl Kuk, captured, and by whom? Quote verbatim with page/citation from any source in the corpus (Plokhy, Snyder, Motyka, Rossoliński-Liebe, Himka, McBride, Armstrong, Viatrovych)."

---

## QUERY 4 — SANITIZATION FOOTNOTE PIN (1941 Act, deleted Hitler-collaboration passage)

**VERDICT: ✅ GROUNDED** — this claim WAS run in a prior NotebookLM grounding pass against this same
notebook and is recorded in `_research/NLM-GROUNDING-BRIEF.md` (Exhibit 1, "BONUS FIND — the
sanitized-text angle").

**Verbatim finding as recorded from that pass:**

> "Rossoliński-Liebe documents that post-war nationalist historiography and Ukrainian diaspora
> publications **deleted** the Hitler/Nazi collaboration passage from reprints of the Act, presenting
> it instead as a purely anti-German act of resistance. Confirmed at exhibition level (a Lviv museum
> display case showed 'an amended version' with the Hitler passage omitted). This is direct
> primary-source evidence of document falsification..."

**Source + location (as recorded in the prior grounding pass):**
Rossoliński-Liebe, Grzegorz. *Stepan Bandera: The Life and Afterlife of a Ukrainian Nationalist.*
ibidem-Verlag, 2014. **p. 2036 area (footnote)** for the diaspora-reprint deletion; **p. 2249 area
(footnote)** for the Lviv museum exhibit with the amended version. Also cross-referenced in the
GAP ANALYSIS table of that brief: "Post-war nationalist reprints deleted the Hitler passage | E1 |
✅ VERIFIED | Rossoliński-Liebe (2036, 2249 area footnotes)."

**Important caveat you should know before this goes on an on-screen card:** the prior grounding
pass's own language uses "area" for both page/footnote numbers (2036 area, 2249 area) — meaning the
original query returned an approximate ebook-location range, not a hard-locked exact footnote number.
This is short of a full ✅ VERIFIED VERBATIM pin (it's closer to "confirmed as fact + approximate
citation location" than "exact footnote number confirmed verbatim"). **The underlying deletion FACT is
solid** (it appears twice, independently, in the earlier grounding brief's exhibit table). But if you
want the precise footnote NUMBER (e.g. "fn. 187" rather than "p. 2036 area") pinned for an on-screen
citation card, that needs one more targeted grounding query — it was not done in the original pass.

**Safe VO phrasing (usable now):** "Rossoliński-Liebe's biography of Bandera documents that post-war
nationalist and diaspora reprints of the Act quietly deleted the line pledging cooperation with Hitler
— and that a Lviv museum once displayed one of these amended versions." (Do not put an exact footnote
number on screen yet — cite as "Rossoliński-Liebe, *Stepan Bandera*, ibidem-Verlag 2014" without a
locked fn. number, or run the follow-up query below first.)

**Query to re-run verbatim to pin the exact footnote number for the on-screen card:**
> "CITATION GROUNDING — Rossoliński-Liebe's claim that post-war nationalist/diaspora reprints of the 30 June 1941 Act of Restoration deleted the passage pledging cooperation with Adolf Hitler, and that a Lviv museum displayed an amended version of the Act omitting that passage. Give the exact footnote number(s) (not an ebook-location range) and quote the footnote text verbatim."

---

## SUMMARY TABLE

| # | Claim | Verdict | Notes |
|---|---|---|---|
| 1 | Desertion motive (~5,000 police, Mar–Apr 1943) | NOT RUN | Only the timeline correlation is grounded (McBride pp.633/640); no causal motive tested. Needs live NLM query. |
| 2 | Territorial pre-emption motive | NOT RUN | Research-team's characterization of Snyder exists but was never citation-grounded with verbatim/page. Needs live NLM query. |
| 3 | UPA anti-Soviet insurgency end-date / Kuk capture | NOT RUN | No prior artifact touches this at all. Needs live NLM query. |
| 4 | 1941 Act sanitization footnote pin | ✅ GROUNDED (fact) / ⏳ approximate citation location | Rossoliński-Liebe, *Stepan Bandera* (ibidem, 2014), pp. 2036 & 2249 "area" footnotes (ebook locations, not exact fn. numbers). Fact is solid; exact footnote number needs one more targeted query. |

**Bottom line:** I could ground 1 of 4 claims (partially — fact solid, exact footnote number still
open) from this project's existing NotebookLM grounding history. Claims 1–3 require live NotebookLM
MCP access, which was not available in this session. Do not put claims 1–3 in the script or on any
on-screen card until they are actually queried against the notebook.
