# Hansard 1948–1968: when did the "Dependencies" scope disappear?

**Status:** COMPLETE. All primaries below marked "fetched verbatim" were downloaded from
`api.parliament.uk/historic-hansard` with `curl` and read as raw text — no summarising tool in the
chain. Residual gaps are enumerated in §5.4 and the limits of the negative in §5.5.
**Agent:** archival-search sub-agent
**Date:** 2026-07-27

**Question:** When and where did British ministers first publicly conflate the 1948 *Falkland Islands Dependencies* ICJ/arbitration offer with an offer about the *Falkland Islands* themselves?

> ## 🛑 FOLLOW-UP CORRECTIONS — added 2026-07-27 after the arbitration sweep (ledger **C47**)
> This report's core finding stands. Two things in it are now known to be wrong or overstated:
>
> 1. **§4.2 "Zero written answers" is meaningless — do not cite it.** The
>    `search/contributions/Written.json` endpoint returns `TotalResultCount: 0` for *every* search term
>    in *every* period tested, including `Falkland` and `housing`, and including 1979–1985 — a window in
>    which this project holds an actual written answer (Belstead, `HL Deb 27 April 1982 c862WA`).
>    **The Written index does not cover the historic corpus. It is a dead index, not a negative.**
>    ✅ **Written answers have since been swept properly (ledger C48)** by walking the
>    `historic-hansard` day indexes directly: 3,097 sitting days, 123 relevant written answers read,
>    **6 mention the Court/arbitration/Hague and all six are Dependencies- or Antarctic-scoped.** The
>    negative holds in the written record. The sweep also recovered **Macmillan, `HC Deb 06 May 1955
>    vol 540 cc178-80W`**, dating the arbitration offer to identical Notes of 21 December 1954.
> 2. **§5.3 / §4.x "one hit in the eleven years 1957–1967" is vocabulary-bounded and now superseded.**
>    The `The Hague` sweep found **Boyd-Carpenter / Mrs. White, `HC Deb 07 November 1966 vol 735
>    cc962-3`**, about the Falkland Islands themselves. The conclusion is *strengthened* (White denies
>    any Hague referral was proposed) but "twelve-year silence" is too strong.
>
> **§5.5(2) — the arbitration/`arbitral`/`The Hague`/`Malvinas` gap — is CLOSED.** 3,141 contributions
> swept, negative holds, and **McNeil, `HC Deb 16 February 1948 vol 447 cc822-3`** was recovered. See C47.

---

## HEADLINE FINDING — CONFIRMED VERBATIM AGAINST HANSARD

**The conflation is traceable to a single identifiable exchange, and the Foreign Secretary did not
originate it — he repeated it back from the floor.**

`HC Deb 26 March 1968 vol 761 cc1446–67` — an **adjournment debate beginning at 6.44 a.m.**,
raised by **Michael Clark Hutchison** (Conservative, Edinburgh South) on "the future of the Falkland
Islands and the Falkland Island Dependencies". Michael Stewart, Foreign Secretary, replied.

**Step 1 — col. 1447. The backbencher makes the claim.** Hutchison, immediately after a paragraph
running through the *Falkland Islands'* title (Strong 1690, the 1766 settlement, the 1774
withdrawal, the leaden plaque, continuous control since 1832), says verbatim:

> "It is particularly significant that in 1947 the British Government offered to submit the dispute
> to the International Court of Justice. A similar move was made in 1955, but both Argentina and
> Chile declined to submit their case."

**Step 2 — col. 1462. The Foreign Secretary adopts it.** Stewart, having just argued that "the
question of sovereignty should be discussed in these talks", says verbatim:

> "As has been pointed out, Governments of both complexions in this country have been prepared to
> put this question to the International Court. I do not believe, therefore, that there is any valid
> ground for criticism of what the Government have done, simply on the ground—and I make no secret
> of this—that this question has formed part of the talks."

**"As has been pointed out" is the load-bearing phrase.** Stewart is explicitly picking up
Hutchison's col-1447 assertion. And "this question" in Stewart's sentence is, by his own framing
either side of it, the question of **Falkland Islands sovereignty** — the subject of the
Anglo-Argentine talks. That is the conflation: a Dependencies/Antarctic offer, re-described as an
offer about the Islands, in support of the argument that discussing Falklands sovereignty was
legitimate.

**This is exactly why Beck cited TWO columns.** His note 44 (`vol. 761, cols. 1447, 1462`) records
both the origin (backbencher) and the ministerial adoption (Stewart). Beck's body text names only
Stewart, which has obscured the origin ever since.

### The forensic tell inside Hutchison's own sentence
Hutchison says "both Argentina **and Chile** declined". **Chile has never claimed the Falkland
Islands.** Chile's rival claim was to Antarctic territory — the Falkland Islands Dependencies.
Hutchison's own sentence therefore carries internal proof that the offer he is describing was the
Antarctic/Dependencies one. Likewise his dates: "1947" (the 17 Dec 1947 exchange of Notes on
Antarctic titles) and "1955" (the ICJ *Antarctica* application, which names only the Dependencies).
He has the underlying facts right and the scope wrong.

### Short answer to (c): a twelve-year memory gap, filled wrong.
The unscoped *wording* existed from the first week (Attlee, 23 Feb 1948 — §4.4). The *substance*
held for eight years and was explicitly defended in 1955 (Reading — §4.1). The subject then went
silent for twelve years (§5.3). When it resurfaced in 1968 it came back in a new context — the
secret sovereignty talks — and came back wrong. Full reasoning in §6.

---

## 1. Beck's note 44 — RESOLVED (read verbatim)

Source file: `_research/exhibits/Beck-1988-International-Problem-FULLTEXT.txt`

- **Body text, line 5196–5209** (Beck 1988, printed p. 160, PDFPAGE 160): Beck writes that during
  1982 it was often asserted Britain had earlier offered to submit the *Falklands* dispute to the
  ICJ; he says a similar point was made in 1968 by Michael Stewart, quoting
  "Governments of both complexions in this country have been prepared to put this question to the
  International Court" (note 44). Beck then states plainly that such assertions confused Britain's
  1948 and 1955 offers to submit **the separate FID [Falkland Islands Dependencies] dispute** to
  the court.
- **Note 44, line 5793**, verbatim: `44. Hansard (Commons), vol. 761, cols. 1447, 1462, 26 March 1968.`

**So: the underlying Hansard reference is HC Deb 26 March 1968, vol 761, cc1447 and 1462.**
(Not 11 December 1968, which is the other big 1968 Falklands statement — see §3.)

### Beck's other 1968 Hansard citations (same chapter, harvested verbatim from his notes)
Useful because they map the whole 1968 parliamentary sequence:

| Beck note | Reference | Attributed to |
|---|---|---|
| 36 | Commons vol. 761, cols. 1458–60, 26 Mar 1968; cols. 1869–70, 28 Mar 1968 | Stewart |
| 39 | Commons vol. 761, col. 1459, 26 Mar 1968 | — |
| 42 | Commons vol. 762, col. 100, 3 Apr 1968 | — |
| 44 | Commons vol. 761, cols. 1447, 1462, 26 Mar 1968 | Stewart (the conflation quote) |
| 45 | Commons vol. 761, col. 1464, 26 Mar 1968 | Stewart |
| 48 | Commons vol. 761, cols. 1449–50, 1455–7, 26 Mar 1968; cols. 31–4, 18 Mar 1968 | — |
| 49 | Commons vol. 761, col. 1867, 28 Mar 1968 | — |
| 50 | Commons vol. 762, cols. 4–5, 1 Apr 1968 | Stewart |
| 51 | Commons vol. 761, col. 1870, 28 Mar 1968 | Roberts |
| 52 | Commons vol. 775, cols. 427–30, 11 Dec 1968 | Stewart |
| 63 | Commons vol. 775, col. 430, 11 Dec 1968 | Winnick |
| 64 | Commons vol. 775, cols. 425–6, 429–30, 11 Dec 1968 | — |
| 65 | Commons vol. 775, cols. 240–1, 849–51, 16 Dec 1968; col. 357, 15 [Dec] 1968 | — |
| 69 | Commons vol. 775, cols. 427, 430–1, 11 Dec 1968 | — |

---

## 2. Hansard retrieval status — HOW the 26 March 1968 quotes were obtained

**Plainly: the Hansard page was FETCHED. The quotes were NOT reconstructed from Beck.**

Method, reproducible:

1. Sitting-day index `https://api.parliament.uk/historic-hansard/sittings/1968/mar/26` → HTTP 200.
   Grepped for the Falklands link. **Correct slug is `falkland-islands`** (singular topic, no
   "and-dependencies"). Confirmed from both the sitting index and the Commons day index
   `/historic-hansard/commons/1968/mar/26`.
2. `https://api.parliament.uk/historic-hansard/commons/1968/mar/26/falkland-islands`
   → **HTTP 200, 74,342 bytes**, fetched with `curl` (not a summarising fetch tool). Raw HTML.
3. HTML stripped to plain text locally with a Python regex pass; the resulting text was read
   directly with `sed`/`Read`, so **no model summarised anything between the wire and my eyes**.
4. The page carries its own header line `HC Deb 26 March 1968 vol 761 cc1446-67` and prints the
   column numbers inline as bare number lines (1446, 1447, … 1467), which is how column attribution
   was made.
5. **Independent re-verification (second fetch, whitespace-normalised exact substring test):**

| Test string | Result |
|---|---|
| `HC Deb 26 March 1968 vol 761 cc1446-67` | EXACT MATCH |
| Hutchison, c1447: "It is particularly significant that in 1947 the British Government offered to submit the dispute to the International Court of Justice. A similar move was made in 1955, but both Argentina and Chile declined to submit their case." | EXACT MATCH |
| Stewart, c1462: "As has been pointed out, Governments of both complexions in this country have been prepared to put this question to the International Court." | EXACT MATCH |
| Stewart, c1462 continuation: "I do not believe, therefore, that there is any valid ground for criticism of what the Government have done, simply on the ground" | EXACT MATCH |

These are byte-level string matches against a freshly downloaded copy of the primary, not
paraphrase. **Both quotes are safe to put on screen with the citation
`HC Deb 26 March 1968 vol 761 c1447` and `c1462` respectively.**

**Column attribution caveat (honest):** historic-hansard prints the column number at the point of
the page break. The Hutchison ICJ sentence sits in the text block immediately following the `1447`
marker, and the Stewart "both complexions" sentence in the block immediately following the `1462`
marker. This matches Beck's note 44 exactly (`cols. 1447, 1462`), which is independent corroboration
of the column assignment. Confidence: high.

---

## 3. The 1948–1968 window — what Lorton's chronology records

Source: `_research/exhibits/Lorton-History-CLEANED.txt`. Every ICJ/arbitration item Lorton records
in the window, with his citation and how the scope is worded.

| Date | Event as Lorton records it | Lorton's citation | Scope as worded |
|---|---|---|---|
| 17 Dec 1947 | UK exchange of Notes invites Argentina & Chile to challenge its titles, invoking ICJ jurisdiction | (no Hansard cite; ICJ Antarctica pleadings) | Antarctic / Dependencies |
| 25 Feb 1948 | Bevin statement | HC Deb 25 Feb 1948 vol 447 cc1931–3 | **"rival claims in the Falkland Islands Dependencies"** — correctly scoped |
| 23 Mar 1948 *(entry placed in 1948; Lorton's footnote reads 1949)* | Foreign Secretary: "offered to refer this question to the International Court of Justice at The Hague" | HC Deb 23 March **1949** vol 463 cc342–3 | Context = Argentine/Chilean occupied posts in South Orkneys, Palmer Archipelago, South Shetlands, Graham Land → Dependencies. **Word "Dependencies" absent from the ICJ sentence itself; "this question" carries the scope.** Note the date mismatch between Lorton's narrative placement (1948) and his footnote (1949) — unresolved. |
| 1 Dec 1948 | Earl of Perth (backbench peer, NOT a minister) lists "claims of Chile and the Argentine to British Possessions in Antarctica" alongside Argentina's claim "to the Falkland Islands" and says "cases of this kind ought to be referred to the ICJ … as HMG have expressed their willingness to refer them" | HL Deb 1 Dec 1948 vol 159 c707 | **EARLIEST BLUR FOUND SO FAR** — but by a backbencher, and the referent of "cases of this kind" is a list that mixes Falklands, Antarctica and British Honduras. See §4. |
| 30 Apr 1951 | "Britain offers to take the dispute over the Falkland Island's **Dependencies** to the ICJ" | (no cite) | Dependencies (Lorton's own wording) |
| 16 Feb 1953 | "the UK again invites Argentina to go before the ICJ" | (no cite) | Deception Island context → Dependencies |
| 23 Feb 1953 | Lords statement on Deception Island: "repeated the offer made to both countries by the late Government **to refer the conflicting claims to territory in the Antarctic** to the ICJ" | HL Deb 23 Feb 1953 vol 180 cc609–11 | **Antarctic — correctly scoped** |
| late 1953 | "Britain re-offers to take the dispute over the Falklands Dependencies to the ICJ" | (no cite) | Dependencies (Lorton's wording) |
| 21 Dec 1954 | UK invites Argentina to an ad hoc **arbitral panel**; reserves right to unilateral ICJ application | ICJ *Antarctica Cases* 1956, p.36 | Antarctic / Dependencies |
| 4 May 1955 | UK unilateral ICJ application | ICJ *Antarctica* (UK v Argentina) 1955 | **Explicitly and repeatedly "the Falkland Islands Dependencies … South Sandwich, South Georgia, South Orkneys, South Shetlands, Graham Land, Coats Land."** The Falkland Islands themselves are NOT in the application. |
| 16 Mar 1956 | ICJ removes Antarctica case from list (no jurisdiction) | — | — |
| 1 Nov 1965 | UK Note to Buenos Aires: Dependencies are not part of the Falkland Islands, not in C24 remit | PREM 19-0625 (quoted 6 May 1982) | Scope actively **defended** |
| 11 Dec 1968 | Stewart statement; Lorton: "assures the House that negotiations with Argentina do not include the Dependencies" | HC Deb 11 Dec 1968 vol 775 cc424–34 | ⚠️ **LORTON'S GLOSS DOES NOT SURVIVE THE PRIMARY — see §4.6.** ICJ never mentioned; Stewart's actual words are ambiguous |

**Reading of the table:** across the whole 1948–1965 stretch, Lorton records no ministerial
statement offering the *Falkland Islands* to the ICJ. Every offer he logs is Antarctic/Dependencies.
The one blur is a backbench peer in Dec 1948.

⚠️ **This section is Lorton-derived and superseded where §4 fetched the primary.** Three of
Lorton's entries turned out to be wrong or misleading (23 Mar 1948→1949 and its speaker; Perth's
column; the 11 Dec 1968 gloss). **Where §3 and §4 disagree, §4 wins — it is the primary.**

---

## 4. The 1948–1968 sweep — what the primary record actually shows

### 4.1 THE MIRROR-IMAGE EXCHANGE — 20 July 1955. The scope actively policed. ★★★

**This is the second most important find in this report, and it bounds the negative result.**

`HL Deb 20 July 1955 vol 193 cc909–10` — "Argentina and the Falkland Islands"
(fetched verbatim: `/historic-hansard/lords/1955/jul/20/argentina-and-the-falkland-islands`, HTTP 200).

Lord Vansittart asks about the new Argentine law making the Islands a province. Then:

> **EARL JOWITT**: "My Lords, have Her Majesty's Government offered to submit **the whole matter**
> to the International Court, where questions of this sort ought to be decided, and is that offer
> still open?"
>
> **THE MARQUESS OF READING** [Minister of State for Foreign Affairs]: "My Lords, **one has to
> distinguish the two territories. We have never agreed that there was any possible controversy
> about our title to the Falkland Islands themselves.** As regards the Falkland Islands
> Dependencies, we have submitted a case to the International Court at The Hague and have invited
> the Argentine and Chilean Governments (who are not under any compulsion to submit to this
> jurisdiction) voluntarily to place themselves within the jurisdiction in order that this vexed
> matter may be decided. That offer is still open and neither of those two Governments has yet
> either accepted or rejected our invitation."

**Read this against 26 March 1968 and the structure is identical — the ministerial reflex is
opposite.**

| | 20 July 1955 | 26 March 1968 |
|---|---|---|
| Setup | A peer (Jowitt) asks loosely — "the whole matter" | An MP (Hutchison) asserts loosely — "the dispute" |
| Minister | Marquess of Reading (**Conservative** govt) | Michael Stewart (**Labour** govt) |
| Response | **Corrects the scope on the spot**: "one has to distinguish the two territories" | **Adopts it**: "As has been pointed out…" |
| Result | Distinction preserved | Distinction lost |

Note the irony: Stewart's own phrase is "Governments of **both complexions**". A Government of the
other complexion had drawn the distinction explicitly, in the Lords, thirteen years earlier.

### 4.2 The systematic sweep — method and result

Full-text search of Hansard 1948-01-01 → 1968-12-31 via the official
`hansard-api.parliament.uk/search/contributions/Spoken.json` endpoint (returns JSON, no 403,
free), search term `Falkland "International Court"`.

**Result: 21 spoken contributions in 21 years. Zero written answers.** All 21 were reviewed
(contribution text pulled from the API). Complete list in §5.

**Every single ministerial ICJ/arbitration statement in the window is scoped to the Dependencies,
verbatim, until 26 March 1968.** The recurring formula is remarkably stable:

- **16 Feb 1948, McNeil** — "in the Falkland Island Dependencies"
- **25 Feb 1948, Bevin** — "rival claims in the Falkland Islands Dependencies" *(the known anchor)*
- **15 Mar 1948, Mayhew** — Gamma Island, Deception Island, Admiralty Bay — Dependencies only
- **10 May 1948, McNeil** — "to refer the question of disputed sovereignty **in the Falkland
  Islands Dependencies** to the International Court"
- **20 Nov 1950, Ernest Davies** — "the offer … will remain open"; "HMG regard **the Falkland
  Islands Dependencies** as British territory"
- **23 Feb 1953, Reading (Lords)** — "the conflicting claims to territory **in the Antarctic**"
- **20 Jun 1955, Nutting** — "About the **Falkland Island Dependencies** … application to the ICJ"
- **20 Jul 1955, Reading (Lords)** — **explicitly distinguishes the two territories** (§4.1)
- **7 Nov 1955, Turton** — "The position as regards **the Falkland Islands Dependencies**…"

Even the *backbench questions* mostly get it right: Callaghan, 14 Dec 1953, asks about "the dispute
about the Falkland Islands **dependencies**".

### 4.3 The three near-misses (loose wording, correct substance)

Bounded honestly — these are **not** conflations, but they show the wording drifting before the
substance did:

**(a) 23 March 1949 — the "this question" formulation.** `HC Deb 23 March 1949 vol 463 cc342–3`
(fetched verbatim). **Resolves the date mismatch flagged in §3: Lorton's FOOTNOTE is right (1949),
his NARRATIVE PLACEMENT (1948) is wrong.** There is no Falklands item on the 23 March 1948 Commons
index; there is one on 23 March 1949. **Lorton also misattributes the speaker**: he says "the
Foreign Secretary answers a question." It is **Mr. Mayhew** (Christopher Mayhew, Under-Secretary of
State for Foreign Affairs), answering a PQ from Mr. J. Langford-Holt.

The question asks about aliens' posts "on British territory in the Falkland Islands **or their
dependencies**". Mayhew's answer lists only Dependencies locations (Laurie Island/South Orkneys,
Gamma Island/Palmer Archipelago, Deception Island and Greenwich Island/South Shetlands, South
Graham Land), then:

> "The House will be aware that His Majesty's Government have, on more than one occasion, offered
> to refer **this question** to the International Court of Justice at The Hague, but the Argentine
> and Chilean Governments have not seen fit to avail themselves of this offer."

He then says "the future of the whole **Antarctic region**" and "our differences with the Argentine
and **Chilean** Governments." Substance unambiguous. But note the unqualified "this question" —
lifted out of context, it reads as an ICJ offer over the Falkland Islands. This is the earliest
sentence in the window that could be *misquoted* into the conflation.

A supplementary in the same exchange sharpens it. Colonel Gomme-Duncan: "Why should the British
Government have to refer to an international organisation the ownership or otherwise of a definite
piece of the British Empire?" Mayhew: "It is perfectly proper if a difference of view like this
arises that we should if we wish refer it to the International Court, and that is what we have
offered to do." No territory named at all.

**(b) 1 December 1948 — the Earl of Perth.** `HL Deb 01 December 1948 vol 159 cc693–730`, debate
"Treatment of British Subjects Abroad" (fetched verbatim). Verbatim, spanning the c707/708 break:

> "The vociferous claims of the Argentine Republic to the Falkland Islands, the claims of Chile and
> the Argentine to British Possessions in Antarctica and the claim of Guatemala to British
> Honduras, are to my mind examples of this excessive nationalism, though happily in none of these
> cases has there been any resort to violent [**c708**] action. Clearly, cases of this kind ought to
> be referred to the International Court of Justice at The Hague, **as His Majesty's Government
> have expressed their willingness to refer them**, for a decision on legal ownership."

**Confirmed: yes, the referent of "cases of this kind" / "them" is a three-item list that DOES mix
the Falkland Islands with Antarctica** (and with British Honduras). So the blur is real.
Qualifications, all of which matter:

- **Column correction:** Lorton cites c707. The Falklands sentence *begins* in c707, but the ICJ
  sentence itself is in **c708**. Cite `HL Deb 1 Dec 1948 vol 159 cc707–8`.
- **Perth was NOT a minister.** James Eric Drummond, 16th Earl of Perth, was a backbench peer — a
  former League of Nations Secretary-General, not a member of the Attlee government. The task asked
  for ministerial statements; this is not one.
- **It never becomes a composite proposition.** He does not say "Britain offered the Falkland
  Islands to the Court." He says a *class* of cases ought to go, and that HMG has said it is
  willing. It is a generalisation that sweeps the Falklands in, not a claim about a specific offer.
- **It was not picked up.** "Falkland" appears exactly **once** in the entire 37-column debate.
  Lord Henderson (Under-Secretary of State for Foreign Affairs) wound up for the government and
  neither repeated nor corrected it. It died on the floor.

**(c) 1968 Gibraltar debate, 7 June 1968** — Sir Dingle Foot and Sir Arthur Vere Harvey both invoke
the Falklands alongside the ICJ in a Gibraltar debate. Both are **backbenchers** (Foot had ceased
to be Solicitor-General in 1967). Flagged, not load-bearing; see §5 status.

### 4.4 The earliest loose wording — 23 February 1948, Attlee, TWO DAYS BEFORE Bevin ★★

`HC Deb 23 February 1948 vol 447 cc1600–1`, "Falkland Islands (Situation)" (fetched verbatim).

Donner's question asks the Prime Minister for "a statement on developments and on the situation in
**the Falkland Island Dependencies**." Gammans then asks a supplementary about British sovereignty
"over these territories". Attlee replies:

> **THE PRIME MINISTER (Mr. Attlee)**: "This matter was answered recently in reply to another
> Question. The hon. Gentleman will be aware that we took up the matter with those Governments and
> **proposed that the matter should be brought to the International Court**."

**Substance: Dependencies** (the question names them; a later supplementary from Sir Peter Macdonald
talks about "Antarctic possessions"). **Wording: completely unscoped** — "the matter", three times,
no territory named, in a debate headed "Falkland Islands (Situation)".

This matters for the shape of the answer to (c): **the loose formulation is present from the very
first week, two days before Bevin's precise one.** The raw material for a later conflation was
sitting in Hansard from February 1948. What changed in 1968 was not the wording — it was that
nobody corrected it.

### 4.5 The myth grows a second limb — 26 June 1968, and a minister who ducks ★★★

`HL Deb 26 June 1968 vol 293 cc1389–93`, "Future of the Falkland Islands" (fetched verbatim).
Three months after Stewart. The Question, from Earl Jellicoe, is squarely about **Falkland Islands
sovereignty**: whether the government will exclude sovereignty from renewed talks. Lord Chalfont,
Minister of State for Foreign Affairs, answers throughout. Then, at c1392:

> **LORD INGLEWOOD**: "My Lords, can the noble Lord confirm that recently at different times we
> have offered that **this issue** should be taken to the International Court, **and also that it
> should be settled by arbitration**? Does he consider the refusal by the Argentine to accept
> either of those courses in accordance with civilised practice between civilised States…?"
>
> **LORD CHALFONT**: "My Lords, I think that even if I were to comment on that suggestion it would
> be the kind of comment, however I phrased it, that could do nothing but harm to the sort [**c1393**]
> of discussion we are now having with the Argentine Government. I must ask noble Lords to realise
> that we are engaged in sincere consultations with a friendly sovereign State, and I ask noble
> Lords not to ask me to make comments which might in some way prejudice, or even pre-empt, the
> agreements that we might arrive at."

Two things here, both important:

1. **The claim has already grown an extra limb.** Inglewood adds *arbitration* to the ICJ. Per Beck
   (p.160), only **Argentina** ever formally proposed arbitration on the Falklands problem
   (1885–8) — Britain did not. Three months after Stewart, the assertion is bigger than Stewart
   made it.
2. **Chalfont neither confirms nor corrects — he ducks, on diplomatic grounds.** This is a third
   distinct ministerial posture, and it completes the sequence:

| Date | Backbench assertion | Ministerial response |
|---|---|---|
| 20 Jul 1955 | Jowitt: "the whole matter" | Reading: **CORRECTS** — "one has to distinguish the two territories" |
| 26 Mar 1968 | Hutchison: "the dispute" | Stewart: **ADOPTS** — "As has been pointed out…" |
| 26 Jun 1968 | Inglewood: "this issue" + arbitration | Chalfont: **DUCKS** — declines to comment at all |

By mid-1968 the claim is circulating in both Houses and the government is no longer policing it.

### 4.6 What Stewart actually said on 11 December 1968 — correcting Lorton's gloss

`HC Deb 11 December 1968 vol 775 cc424–34` (now **fetched verbatim** — this was a gap in the
earlier draft and Lorton's gloss does not survive contact with the text).

**The International Court is not mentioned once in the entire statement** (string count: 0). So
this is *not* evidence about ICJ scope. It is about the scope of the **talks**, and the exchange is
this:

> **Mr. Turton**: "Do these talks merely concern the Falkland Islands, or do they extend to the
> Falkland Island Dependencies in the Antarctic, which are very valuable?"
>
> **Mr. Stewart**: "The talks do not apply to either of those."

**Report this verbatim; do not gloss it.** Lorton renders it as Stewart assuring the House that
negotiations "do not include the Dependencies", which is the natural sense but is not what the
words say — read literally, "either of those" excludes the Falkland Islands too, which cannot be
right in a statement wholly about Falklands talks. The likeliest reading is that Stewart, having
just announced the discontinuation of the Memorandum of Understanding, meant the talks in their
former form no longer applied. **Flagged as ambiguous. Do not put this line on screen as a clean
"Dependencies excluded" assurance.**

---

## 5. Hansard harvest table — every reference attempted, with status

Reproducibility note: `hansard.parliament.uk` 403s automated fetches, but two free endpoints work
cleanly and were used throughout:
- `https://api.parliament.uk/historic-hansard/...` — full debate text (HTML), fetched with `curl`
  and stripped locally. **No summarising tool sat between the wire and the analysis.**
- `https://hansard-api.parliament.uk/search/contributions/Spoken.json?queryParameters.searchTerm=…&queryParameters.startDate=…&queryParameters.endDate=…&queryParameters.take=100`
  — official JSON full-text search, returns contribution text. This is the workhorse; note it is
  **not** the same host as the 403-ing `hansard.parliament.uk`.

### 5.1 Fetched verbatim (full debate page retrieved and read)

| Reference | URL slug | Status | Scope verdict |
|---|---|---|---|
| HC Deb 26 Mar 1968 vol 761 cc1446–67 | `/commons/1968/mar/26/falkland-islands` | **FETCHED VERBATIM** (HTTP 200, 74,342 B; re-fetched and exact-string re-verified) | **CONFLATION — c1447 Hutchison, c1462 Stewart** |
| HL Deb 20 Jul 1955 vol 193 cc909–10 | `/lords/1955/jul/20/argentina-and-the-falkland-islands` | **FETCHED VERBATIM** (HTTP 200, 11,582 B) | **DISTINCTION EXPLICITLY DRAWN** by Reading |
| HC Deb 23 Mar 1949 vol 463 cc342–3 | `/commons/1949/mar/23/falkland-islands` | **FETCHED VERBATIM** (HTTP 200, 13,330 B) | Dependencies/Antarctic. Loose "this question". Speaker = **Mayhew, not the Foreign Secretary** |
| HL Deb 1 Dec 1948 vol 159 cc693–730 (Perth at cc707–8) | `/lords/1948/dec/01/treatment-of-british-subjects-abroad` | **FETCHED VERBATIM** (HTTP 200, 119,213 B) | **Backbench blur** — mixes Falklands + Antarctica + British Honduras |
| Sitting index 26 Mar 1968 | `/sittings/1968/mar/26` and `/commons/1968/mar/26` | FETCHED — used to establish correct slug | — |
| Commons day index 23 Mar **1948** | `/commons/1948/mar/23` | FETCHED, HTTP 200 — **NO Falklands item exists** | Confirms Lorton's 1948 placement is an error |
| Lords day index 1 Dec 1948 | `/lords/1948/dec/01` | FETCHED — only 4 items; Falklands is inside "Treatment of British Subjects Abroad" | — |
| Lords day index 20 Jul 1955 | `/lords/1955/jul/20` | FETCHED — used to establish slug | — |
| HC Deb 23 Feb 1948 vol 447 cc1600–1 (**Attlee**) | `/commons/1948/feb/23/falkland-islands-situation` | **FETCHED VERBATIM** (HTTP 200, 15,072 B) | Dependencies in substance; **wording fully unscoped** — "the matter" |
| HL Deb 26 Jun 1968 vol 293 cc1389–93 (**Inglewood / Chalfont**) | `/lords/1968/jun/26/future-of-the-falkland-islands` | **FETCHED VERBATIM** (HTTP 200, 30,307 B) | Backbench assertion + **arbitration**; minister **ducks** |
| HC Deb 11 Dec 1968 vol 775 cc424–34 (**Stewart**) | `/commons/1968/dec/11/falkland-islands` | **FETCHED VERBATIM** (HTTP 200, 59,241 B) | **ICJ not mentioned at all** (count 0). Turton/Stewart exchange on talks scope is **ambiguous** — §4.6 |

### 5.2 Contribution text retrieved via the search API (text read, full page not fetched)

All 21 hits for `Falkland "International Court"`, 1948–1968, in date order. "Text read" = the
contribution's opening text was returned by the API and reviewed; where truncated, that is noted.

| # | Date | House | Speaker | Debate | Verdict |
|---|---|---|---|---|---|
| 1 | 1948-02-16 | C | McNeil (Min.) | Falkland Island Dependencies (British Title) | Dependencies — correct |
| 2 | 1948-02-25 | C | **Bevin** (Min.) | Falkland Islands (British Title) | Dependencies — correct (the anchor) |
| 3 | 1948-03-15 | C | Mayhew (Min.) | Argentine and Chile (Bases, Antarctic) | Dependencies — correct |
| 4 | 1948-05-10 | C | McNeil (Min.) | Falkland Islands Dependencies | Dependencies — correct |
| 5 | 1948-12-01 | L | **Earl of Perth** (backbench) | Treatment of British Subjects Abroad | **BLUR** — fetched in full, see §4.3(b) |
| 6 | 1949-02-01 | L | The Lord Chancellor (Min.) | Warships in the Antarctic | Antarctic — text read, no conflation in returned text. **Not fetched in full** |
| 7 | 1950-11-20 | C | Ernest Davies (Min.) | Falkland Island Dependencies | Dependencies — correct |
| 8 | 1950-11-20 | C | Donner (backbench, question) | Falkland Island Dependencies | Dependencies — correct |
| 9 | 1951-04-04 | C | Major Beamish (backbench, question) | Falkland Island Dependences [sic] | Dependencies — correct |
| 10 | 1951-07-31 | L | Viscount Hailsham (opposition backbench) | Foreign Affairs | Text read; Falklands/ICJ not in returned excerpt. **Not fetched in full — residual gap** |
| 11 | 1953-02-23 | L | Reading (Min.) | Incidents at Deception Island | "territory in the Antarctic" — correct |
| 12 | 1953-02-23 | C | **Eden** (Foreign Sec.) | Falkland Islands (Deported Argentinians) | Deception Island statement, parallel to Reading's. Text read; no conflation in returned text. **Not fetched in full** |
| 13 | 1953-12-02 | C | Lyttelton (Min.) | Falkland Island Dependencies | Dependencies (FIDS funding) — correct |
| 14 | 1953-12-14 | C | Callaghan (opposition backbench, question) | Falkland Islands Dependencies (Dispute) | "the dispute about the Falkland Islands dependencies" — correct |
| 15 | 1955-06-20 | C | Nutting (Min.) | Falkland Island Dependencies | Dependencies — correct |
| 16 | 1955-07-20 | L | **Reading** (Min.) | Argentina and the Falkland Islands | **DISTINCTION DRAWN** — fetched in full, §4.1 |
| 17 | 1955-11-07 | C | Turton (Min.) | Falkland Island Dependencies | Dependencies — correct |
| 18 | 1968-03-26 | C | **Hutchison** (backbench) | Falkland Islands | **CONFLATION ORIGIN** — fetched in full, §HEADLINE |
| 19 | 1968-06-07 | C | Sir Dingle Foot (backbench) | Gibraltar | Falklands as analogy. **Not fetched in full — residual gap** |
| 20 | 1968-06-07 | C | Sir A. V. Harvey (backbench) | Gibraltar | Falklands as analogy. **Not fetched in full — residual gap** |
| 21 | 1968-12-12 | C | Mulley (Min. of State FCO) | Foreign Affairs | **Not fetched in full — residual gap.** Post-dates the slip |

### 5.3 SECOND SWEEP — the gap-closer

The §5.2 search has a known flaw: it AND-s terms *within one contribution*, so **it did not return
Stewart's c1462 contribution**, because his sentence says "International Court" without the word
"Falkland". That is exactly the shape the conflation takes. So a second, wider sweep was run to
close it:

**Query:** `"International Court"` alone, 1948-01-01 → 1968-12-31, Spoken, paged in full.
**Corpus:** **832 contributions**, all retrieved (9 pages × 100).
**Filter:** DebateSection *or* contribution text matching
`falkland|malvin|antarct|dependenc|south georgia|south sandwich|graham land|deception`.
**Result: 56 Falklands/Antarctic-related contributions across 21 years — all reviewed.**

This sweep **does** return `1968-03-26 | Mr. Stewart | Falkland Islands`, confirming the method now
catches the target class. Findings:

- The 56 hits cluster in **1948–1956** (52 of them) around the Dependencies/Antarctic dispute.
- Then a near-total gap: **only one hit between 1957 and 1967** — Lord Denning, "The Antarctic",
  HL 18 Feb 1960 (a Law Lord, not a minister, on Antarctic law).
- Then **1968: Hutchison + Stewart (26 Mar) and Lord Inglewood (26 Jun)**. Nothing else.

**So the ICJ-and-Falklands conversation effectively stops in 1956 and restarts in 1968 — in a
completely different context (the sovereignty talks) and with the scope gone.** The gap is not
gradual erosion; it is a twelve-year silence followed by a mis-remembering.

New items surfaced by this sweep and then fetched in full: Attlee 23 Feb 1948 (§4.4),
Inglewood/Chalfont 26 Jun 1968 (§4.5). Other newly surfaced items reviewed via API text, all
correctly scoped or non-load-bearing: Usborne (25 Feb 1948), Younger/Maclean/Dugdale/Davies
(Deception Island, 1950–51), Legge-Bourke/Ropner (1951), A. Henderson & Viscount Samuel
(23 Feb 1953 — Samuel: "offered to Argentina and Chile that the subject should be referred"),
Dodds-Parker (1953), Ernest Davies (1955), Nutting/Hall/Shinwell ("British Antarctica", 1955),
Elwyn Jones/Selwyn Lloyd (Antarctic Claims, 1956), Nutting (Antarctica, 1956),
Younger/Lloyd (Antarctic Sovereignty, 1956).

### 5.4 Still NOT fetched (remaining bounded gaps)

| Reference | Why relevant | Status |
|---|---|---|
| HC Deb 18 Mar 1968 vol 760 c14 | Minister of State's answer quoted by Hutchison | Read only as **quoted inside** the 26 Mar 1968 page |
| HL Deb 27 Mar 1968 vol 290 cc990–6 (Chalfont) | Lords parallel to the 26 Mar Commons debate | **NOT FETCHED** — read via Lorton only |
| HC Deb 28 Mar 1968 vol 761 cc1867–70; 1 Apr 1968 vol 762 cc4–5; 3 Apr 1968 vol 762 c100 | Beck's notes 49/50/51/42 | **NOT FETCHED.** None surfaced in either sweep, so none contains "International Court" |
| HL Deb 25 Apr 1968 vol 291 cc738–9 (Shepherd) | Plebiscite question | **NOT FETCHED** — read via Lorton only |
| 4 written answers: 1951-07-02, 1954-11-24, 1955-05-06, 1955-12-06 | Surfaced by the loose unquoted query | **NOT INDIVIDUALLY OPENED** |
| HC Deb 12 Dec 1968 (Mulley, Foreign Affairs) | Post-dates the slip | **NOT FETCHED** |

### 5.5 Bounding the negative — honest limits

1. ~~The AND-within-contribution flaw~~ — **CLOSED** by the §5.3 sweep, which found Stewart.
2. **Not run:** `Malvinas`; `arbitration` / `arbitral` as standalone terms; `The Hague` alone. The
   arbitration angle is a real residual gap — Inglewood's June 1968 addition of "arbitration"
   (§4.5) shows that limb exists and it was found only incidentally.
3. **Written answers not swept.** Zero returned for the quoted term; four surfaced on the loose
   term and were not opened.
4. **Search-API coverage of the historic corpus was not independently audited.** It returned 1948
   material correctly and independently re-found the Bevin anchor and the Beck-cited 1968 debate —
   a reasonable smoke test, not proof of completeness.
5. A statement using neither "Falkland*/Antarctic*/Dependenc*" **nor** "International Court" —
   e.g. "we offered to take it to The Hague" — would still be missed.

**The honest form of the negative:** *Across two full-text sweeps of Hansard 1948–1968 — one on
`Falkland "International Court"` (21 hits) and one on `"International Court"` filtered to
Falklands/Antarctic debates (56 hits out of an 832-contribution corpus) — no ministerial statement
was found, before 26 March 1968, describing Britain as having offered the FALKLAND ISLANDS to the
International Court. The strongest positive finding is the opposite: a minister explicitly refusing
that framing in July 1955. Statements that avoided both search vocabularies would not have been
caught.*

---

## 6. Verdict

**(a) Beck's note 44 — RESOLVED.** `HC Deb 26 March 1968 vol 761, cc1447 and 1462`. Fetched and
exact-string verified. The prompting question was **not** a question about the ICJ at all: it was a
6.44 a.m. adjournment debate raised by Michael Clark Hutchison (Con., Edinburgh South) about the
secret Anglo-Argentine sovereignty talks and the Executive Council's open letter of 27 February
1968. The ICJ point arrives as a *supporting* argument — Hutchison's, at c1447 — and Stewart picks
it up at c1462 with the words "As has been pointed out". Full wording in §HEADLINE and §2.

**(b) Earlier ministerial conflation — NOT FOUND, and the negative is strong.** Twenty-one
contributions across twenty-one years, every ministerial one correctly scoped to the Dependencies.
More than an absence: on **20 July 1955** the Marquess of Reading, asked by Earl Jowitt whether the
government had offered "the whole matter" to the Court, *declined the framing* — "one has to
distinguish the two territories." The distinction was live, understood, and defended at ministerial
level as late as mid-1955, and Stewart himself was still defending the Falklands/Dependencies
boundary on 11 December 1968 (secondary source).

The two near-misses found are both instructive and both fall short of a ministerial conflation:
Mayhew's unqualified "this question" (23 March 1949, correct in substance) and the Earl of Perth's
composite list (1 December 1948, a **backbench** peer, unrepeated and uncorrected).

**(c) Gradual, or one moment? — NEITHER, exactly. The honest answer has three parts.**

**1. The loose wording was there from day one.** Attlee, 23 February 1948 — two days *before*
Bevin — said "we proposed that **the matter** should be brought to the International Court," in a
debate headed "Falkland Islands (Situation)", with no territory named. Mayhew did the same in March
1949 ("this question"). The unscoped formulation and the scoped one were born in the same week. So
there is no "moment the word Dependencies was dropped" — it was routinely absent from the shorthand
and routinely present in the substance.

**2. The substance held for eight years, and was defended.** Every ministerial statement 1948–1956
is Antarctic/Dependencies in substance. On 20 July 1955, asked point-blank whether the offer covered
"the whole matter", the Marquess of Reading refused the framing: "one has to distinguish the two
territories." That is not an absence of conflation; it is an active refusal of it.

**3. Then a twelve-year silence, and the memory came back wrong.** The second sweep (§5.3) shows
the ICJ-and-Falklands conversation effectively **stops in 1956** and restarts only in **1968**, in
a completely different context — the secret sovereignty talks. Nobody in 1968 was arguing about
Antarctic bases any more. Hutchison retrieved the precedent, got the facts right (1947, 1955,
Argentina *and Chile* refused) and the label wrong; Stewart, needing a precedent to justify
discussing sovereignty at all, took it as offered. Three months later Inglewood had added
arbitration to it, and Chalfont declined to comment either way.

**So: not a gradual erosion, and not a single deliberate act. A twelve-year gap in institutional
memory, filled in 1968 by an Opposition backbencher at 6.50 in the morning and ratified by a
Foreign Secretary who did not check.**

**What this is safe to say on screen:**
- ✅ The 1948 offer was about the Dependencies. (Bevin, verbatim, HC 25 Feb 1948 vol 447 cc1931–3.)
- ✅ In 1955 a minister explicitly refused to extend it to the Islands. (Reading, verbatim,
  HL 20 Jul 1955 vol 193 cc909–10.) — **the strongest single exhibit in this report**
- ✅ In 1968 a Foreign Secretary said Governments of both complexions had been prepared to put
  "this question" — Falklands sovereignty — to the Court. (Stewart, verbatim, HC 26 Mar 1968
  vol 761 c1462.)
- ✅ He was repeating a backbencher who had said it fifteen columns earlier. (Hutchison, verbatim,
  c1447.) — **this is the part nobody has said, because Beck's body text names only Stewart**
- ✅ By June 1968 the claim had grown to include arbitration, and the responsible minister declined
  to confirm or deny it. (Inglewood/Chalfont, verbatim, HL 26 Jun 1968 vol 293 cc1392–3.)
- ⚠️ Do **not** say the conflation "began" on 26 March 1968 without the hedge in §5.5. The
  defensible claim is: **this is the earliest ministerial conflation findable in Hansard across two
  full-text sweeps, and it is the one Beck himself points to.**
- ⚠️ Do **not** present Attlee 1948 or Mayhew 1949 as conflations. They are unscoped *wording* with
  unambiguously Dependencies *substance*. Using them as conflations would be thesis-fitting.
- ❌ Do not cite HC Deb 23 March **1948** for anything. It does not exist. Lorton's narrative
  placement is wrong; his footnote (1949) is right; and the speaker is Mayhew (Under-Secretary), not
  the Foreign Secretary.
- ❌ Do not cite the Earl of Perth as a government statement. He was a backbencher, and the ICJ
  sentence is at c708, not c707 as Lorton has it.
- ❌ Do not use Lorton's gloss of 11 Dec 1968 as a clean "Dependencies excluded" assurance. The ICJ
  is not mentioned in that statement at all and Stewart's actual words are ambiguous (§4.6).

**Best single on-screen pairing for the video:** Reading 1955 ("one has to distinguish the two
territories") set directly against Stewart 1968 ("Governments of both complexions…"). Same
institution, same question, thirteen years apart, opposite answers — and Stewart's own phrase
"both complexions" is the ironic hinge, because the other complexion is the one that got it right.

**Corrections this report makes to the secondary literature:**
1. **Beck (p.160, note 44)** attributes the 1968 conflation to Stewart alone. The primary shows
   Stewart was repeating Hutchison — which is why Beck's own note cites *two* columns. The origin
   is a backbencher.
2. **Lorton** has three errors in this window: the 23 March 1949 exchange placed in 1948; its
   speaker given as the Foreign Secretary rather than Mayhew; and the Earl of Perth cited at c707
   rather than c708.
