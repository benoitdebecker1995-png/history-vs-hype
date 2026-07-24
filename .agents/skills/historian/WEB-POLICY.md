# Web/Gemini Verbatim Policy

Tool-agnostic. Applies regardless of which tool (Gemini, Grok, ChatGPT, Claude general knowledge, WebFetch, web scraping) produced the text.

---

## Hard Ban

**Verbatim text from books, journals, manuscripts, or any source NOT in the NLM notebook is BANNED from `## VERIFIED QUOTES` and `## VERIFIED CLAIMS` regardless of tool.**

This catches:
- Gemini producing a "verbatim passage" from Hancock's *Fingerprints of the Gods* (book not in NLM)
- Grok generating plausible Arabic phrases attributed to Ibn al-Jawzī (source not verified in primary)
- WebFetch scraping a book preview from Google Books and presenting it as verbatim
- Claude general knowledge "quoting" a scholar from training data
- ChatGPT producing a convincingly-cited passage from a manuscript

The tool is irrelevant. The NLM-anchor status is what matters.

---

## Allowed: Freely-Accessible Web Verbatim

Verbatim text from **freely-accessible web sources** is allowed WITH the source URL captured inline.

Qualifies:
- News articles (Reuters, BBC, AP, NYT if URL works)
- Blog posts, op-eds, public essays
- Wikipedia article text (cite the URL, not Wikipedia as an authority)
- Public podcast transcripts (if a transcript URL exists and is stable)
- YouTube transcripts (capture the video URL + timestamp)
- Openly-accessible PDFs of primary documents (if the URL is a stable archive link, not a paywalled download)

Does NOT qualify:
- A book's Amazon preview page (not the whole book; fragment only; paraphrase it)
- A paywalled article (only the accessible abstract portion qualifies with URL)
- A cached or scraped version of a normally-paywalled source

---

## Always Allowed (No NLM Anchor Needed)

The following never need NLM grounding regardless of tool:

- Factual summaries and paraphrases (Hancock *argues* that the map shows Antarctica)
- Biographical facts (Piri Reis died in 1553; Hancock was born in 1950)
- Publication dates, pricing, ISBN, availability
- Finding what to acquire ("McIntosh's *The Piri Reis Map of 1513* is available on Amazon for $45")
- Research landscape orientation ("three major scholars have written on this: McIntosh, Soucek, Kahle")

---

## Numbers & Figures — Tier by KIND (not by age)

The "freely-accessible web = OK with URL" allowance above is for **prose/paraphrase**. It does NOT extend a free pass to a **load-bearing figure**. A Wikipedia death toll is NOT grounded just because the URL resolves. Classify every load-bearing number by the KIND of fact (not its age — a 1947 admin count and a 2016 vote are both administrative; a recent death toll is still historical):

| Kind | Examples | Grounding rule |
|---|---|---|
| **1 — contested / historical / atrocity, or any quote** | death tolls, casualties, who-killed-whom, verbatim | **Academic / NLM / primary ALWAYS.** Web-only = not grounded → holding pen or re-ground. This is the #62 failure mode (Operation Vistula `140,575` came in "web-confirmed Wikipedia/ENRS"). |
| **2 — administrative fact of record** | official counts, vote tallies, treaty text, event dates | Academic-preferred; **authoritative** web (ENRS / gov / primary registry) as fallback **only when no academic source carries it**, labeled with its tier. Try the notebook first. |
| **3 — recent / media number** | current-events figures too new for academic press | Web is legitimate but disciplined: attribute to the outlet, cross-check 2+ independent outlets, label "reported" not "established," re-verify week-of-film. |

Extends the "web/Gemini verbatim ban" from quotes to numbers. When in doubt about kind 1 vs 2, treat as kind 1 (academic).

---

## Paraphrase vs Verbatim — the Line

| What you're writing | Requires NLM anchor? |
|---|---|
| Hancock *argues* that the map shows an ice-free Antarctica | No — paraphrase |
| "bombshell ... irrefutable evidence of a vanished civilization" (verbatim Hancock 1995) | YES — banned without NLM source ID |
| In McIntosh's reading, the Spanish prisoner "confused" Columbus's voyages | No — paraphrase with attribution |
| "It is questionable whether the Spanish sailor had been on three voyages with Columbus" (verbatim McIntosh) | YES — NLM source ID required |
| The Gaspar 2008 paper proposes a magnetic declination mechanism | No — factual summary |
| [exact coordinate rotation matrix notation from Gaspar verbatim] | YES — NLM source ID required |

---

## Worked Examples

| Source | Verbatim OK? | Ruling |
|---|---|---|
| Hancock *Fingerprints of the Gods* (1995) passage | **BAN** | Book not in NLM notebook |
| Hancock *Magicians of the Gods* (2015) passage | **BAN** | Book not in NLM notebook |
| von Däniken *Chariots of the Gods* passage | **BAN** | Book not in NLM notebook |
| Reuters article about a court ruling (URL available) | **OK with URL** | Freely-accessible web |
| Wikipedia article text | **OK with URL** | Freely-accessible web |
| Grok-produced "verbatim Arabic" from Ibn al-Jawzī | **BAN** | Source not in NLM; AI fabrication risk confirmed in Hijab #52 |
| Gemini factual summary of Hancock's argument | **OK** | Paraphrase, not verbatim |
| Gemini "verbatim passage" from Hancock book not in NLM | **BAN** | Book not in NLM; tool irrelevant |
| NLM query returning a quote with source ID | **OK** | NLM-anchored |
| Mallery 1956 radio transcript (not in NLM, no stable URL) | **BAN** unless web-accessible URL found | Broadcast not in NLM; no URL captured |
| Ohlmeyer 1960 USAF letter (if PDF URL is stable) | **OK with URL** | Primary document, freely accessible |
| Podcastnotes.org JRE episode summary | **OK with URL** | Freely-accessible web |

---

## Candidate Quotes Holding Pen

Verbatim text that fails the policy but has an acquisition path goes to `## Candidate Quotes (Not Yet NLM-Verified)` in `01-VERIFIED-RESEARCH.md`. This section is the authorized holding pen — NOT `## VERIFIED QUOTES`. Moving text from the holding pen to VERIFIED QUOTES requires:

1. Acquire the source
2. Upload to NLM notebook
3. Run NLM round-trip verification (per `feedback-notebook-citation-grounding.md`)
4. Confirm verbatim match + page number
5. Add NLM source ID to the quote entry

Until that round-trip is complete, the text stays in the holding pen.
