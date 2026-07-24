# BLIND-EVIDENCE-DESIGN-2026-07-21.md — a clean-room evidence architecture for #62, then the diff

> **TIER: IDEA / hypothesis, all of it.** Nothing here is a mandate. Your live picks are the only ground truth.
> Everything below is either (a) a *measured* count/verbatim from competitor transcripts I actually pulled, or
> (b) an *inferred* design judgment. I mark which, every time.
>
> **Structure of this file:** §0 blindness disclosure · §1–§2 PHASE 1 (lane evidence-architecture study + my
> independent design, written before opening `SCRIPT.md`) · §3 PHASE 2 (the diff, written after) · §4 the ranked
> menu with prices.

---

## §0 — BLINDNESS DISCLOSURE (read this first; it changes how much §2 is worth)

**Files I did NOT open before writing §1–§2:** `SCRIPT.md`, `02-STRUCTURE-SYNTHESIS.md`, anything in `_adlib/`,
`_research/STRUCTURE-STUDY-KRAUT.md`, `_research/agent-outputs/*`, `VOICE-DRAFT.md`, `SCRIPT-VOICE-PLAN.md`,
`ADLIB-BRIEF.md`, `_research/SCRIPT-CONVERGENCE-PROMPT-2026-07-20.md`, `RECORD-CARDS.md`. I also did not open
`scratchpad/v61.md` (a cached script version I found while working and deliberately left shut).

**But the blindness is only partial, and I'm not going to pretend otherwise.** The files I was *directed* to read
leak the script's structure badly:

| Source | What it leaked |
|---|---|
| `SOURCES.md` §A | The whole exhibit inventory **organised by ACT 1–5**, with each act's subject named |
| `SOURCE-GENEALOGY.md` | Chapter numbers (CH6) and three verbatim script lines (rows 5c, 12, 13) |
| `01-VERIFIED-RESEARCH.md` | CH2/CH3/CH4/CH5/CH6/CH7/CH8 references; several quoted VO fragments; the blind-spot audit quotes CH6's "what no one has ever found is his signature" verbatim |
| `_research/REFERENCE-LANE-FIGURATION-2026-07-21.md` | **16 verbatim v7.0 script lines** with chapter tags, and the note that CH6/CH8/CH9/CH10 need no figuration change |
| `CREATOR-INTENT.md` | Cold open locked (the ally, not Russia); close = comprehension → mirror; ACT 5 named |
| `VOICE-PROFILE.md` | Two #62 grill lines, including a real T5 delivered line |

So: **I knew the act-level allocation and roughly a dozen individual lines before designing.** What I genuinely did
*not* know is the ordering inside acts, the runtime split, the transitions, how the crux is staged, what is on
screen when, and — crucially — **what the script leaves out.** That last one is what this exercise was for, and it
survives. Treat §2 as *semi-blind*: a design built from the ledger and from a fresh lane study, by someone who knew
the shelf labels but not the contents. Where §3 reports convergence, discount it by the leakage; where §3 reports an
omission, the finding is clean.

---

# PHASE 1 (written before opening the script)

## §1 — HOW THE LANE ACTUALLY BUILDS AN EVIDENCE-FIRST VIDEO

### 1.0 Method (what's measured)

The prior figuration study left 14 fully **timestamped** transcripts cached in this session's scratchpad
(`tx/*.txt`) — I reused those, so every timestamp below is real, not reconstructed. `youtube_transcript_api` is
currently **IP-blocked** from this machine; where I needed text the cache didn't have I re-pulled via the vidIQ MCP
(`vidiq_video_transcript`), which returns **full text but no timestamps**. Any quote I cite without a timestamp came
from that path and is flagged.

Sample (14 videos, 6 channels, ~38.3k transcript words):

| File | Channel / video | Runtime | Words |
|---|---|---|---|
| `prem_alexandria` | Premodernist — Library of Alexandria (`M4WU8gqrgsQ`) | 22:27 | 3,689 |
| `prem_alaska` | Premodernist — Alaska Purchase (`vjlZsJaVptQ`) | 17:11 | 2,995 |
| `milo_footprints` | Stefan Milo — White Sands footprints (`9fUAV4DcyD4`) | 16:15 | 2,619 |
| `milo_rock` | Stefan Milo — Altar Stone (`GyqoGuabkE0`) | 15:50 | 2,837 |
| `rfb_genz` | ReligionForBreakfast — Gen Z revival (`UdsPPxaGVUs`) | 11:26 | 2,110 |
| `rfb_lilith` | RFB — Origins of Lilith (`uIY0tKSg_XY`) | 18:31 | 3,191 |
| `rfb_statues` | RFB — (bonus, statue destruction) | 27:29 | 4,754 |
| `rfb_atheists` | RFB — (bonus) | 15:31 | 2,787 |
| `atun_confedsoldiers` | Atun-Shei — Did Confederate Soldiers Fight for Slavery (`nQTJgWkHAwI`) | 8:55 | 1,342 |
| `atun_northernagg` | Atun-Shei — War of Northern Aggression (`Lac-8tTuyhs`) | 16:47 | 2,463 |
| `figtree_minoans` | fig tree — Manufactured Minoans (`INokIVWNASQ`) | 11:35 | 2,368 |
| `figtree_gobekli` | fig tree — Göbekli Tepe (`6eJXWv7hFis`) | 13:59 | 2,718 |
| `hc_pomerium` | Historia Civilis — The Roman Pomerium (`s9qlNBBoFG4`) | 16:26 | 2,417 |
| `hc_newpolitical` | Historia Civilis — Rome's New Political Order (`PDvriMq6r6I`) | 13:25 | 2,061 |

---

### 1.1 Where does the first real document/exhibit enter? (MEASURED, with one inference)

| Video | First primary exhibit | % of runtime | Earned or led? |
|---|---|---|---|
| Premodernist Alaska | the 1867 newspaper record / the treaty + Senate ratification vote | **~9%** (1:29–1:48) | **Led.** Myth stated 0:00–0:21, busted at **0:24** ("But in fact that's not true"), thesis by 0:33, documents by 1:30 |
| Premodernist Alexandria | the *absence* is the exhibit; first named source (Strabo, quoted) at **~53%** (11:53) | ~53% | Earned by 10 minutes of establishing the record's limits first |
| Milo — Altar Stone | Inigo Jones's own 17th-c. hedge, quoted verbatim, **1:55 = 12%** | **12%** | Led — but it's a *hedge*, not a proof |
| Milo — footprints | the trackways themselves at 0:25; the dating evidence at **4:18 = 26%** | 26% | Earned |
| RFB Gen Z | three opposing headlines named at **0:00–0:15**; the Pew dataset at **0:38 = 6%** | **6%** | Led |
| RFB statues | first inscription on screen **14:29 = 53%** | 53% | Earned |
| Atun-Shei Confederate soldiers | Lincoln's first inaugural quoted **4:53 = 55%**; the 40% slaveholding stat at **4:42** | 55% | Earned — 4½ min of the opposing camp's own words first |
| Historia Civilis pomerium | **none** — no document on screen in 16:26 | n/a | n/a |

**Finding (measured):** the lane splits cleanly in two, and the split is *not* about quality.

- **Fast-lead (6–12%)** when the video's job is to **falsify a live public claim**: Premodernist Alaska, RFB Gen Z.
  Both state the myth in the myth's own published words in the first 20 seconds, bust it inside 30, and have the
  countervailing dataset on screen inside 90.
- **Slow-earn (26–55%)** when the video's job is to **explain what the record can and can't support**: Alexandria,
  RFB statues, Atun-Shei, Milo footprints. These spend the first third building the *evidentiary situation* so the
  exhibit lands as a verdict rather than a fact.

**Inferred:** #62 is structurally a *falsify-a-live-claim* video (Poland says planned genocide, Ukraine says no
plan, Russia says Nazi state) with a *what-the-record-supports* crux buried in the middle. The lane suggests you can
have both — lead fast on the public dispute, then slow-earn the crux — which is why my design in §2 puts a cheap
document (the decree) at 0:15 and the *real* exhibit at ~2:00.

---

### 1.2 How is a source introduced? (MEASURED)

**Seconds per exhibit — the lane is fast.** Counted on the three cleanest cases:

- Atun-Shei, Frank Meyers's diary: introduction + full quote = **5:12 → 5:33, 21 seconds.** The introduction itself
  is nine words: *"here's a quote, this is Confederate cavalryman Frank Meyers"* + *"this is directly from his
  diary"* (5:21).
- Atun-Shei, Lincoln's first inaugural: setup + quote = **4:50 → 5:06, 16 seconds.**
- Milo, Inigo Jones: **1:52 → 1:58, 6 seconds** — *"It was probably given the name Altar Stone by Inigo Jones, a
  17th century architect who wrote, 'Whether it be an altar or not, I leave to the judgment of others.'"*

**The introduction form is: one appositive of role + one clause of provenance, then the words.** Nobody in the
sample reads an archive call number aloud. Nobody says "tier". What they *do* say aloud is the **evidentiary class**
and its **limits** — that's a different thing, and it's the credibility move:

- Milo, `GyqoGuabkE0` 7:05: *"How confident are you that this rock came from the Orcadian Basin — like is there a
  margin of error? What's your confidence level?"* → 7:08 *"There's certainly a margin of error. As
  geochronologists, we operate within uncertainty."* → 7:24 *"we're greater than 95% certain."*
  **He asks for the error bar on camera.**
- Milo, `9fUAV4DcyD4` 15:09: *"Now that's not my idea, that's not my idea. And I don't know the paper where that
  idea came from, I've just heard it in conversation talking to other archeologists."*
- fig tree, `6eJXWv7hFis` 8:13: *"it has been argued — I'm telling you what's been argued, I'm not arguing it —"*
  **Nine words. That is the entire referee disclaimer.**

**Transferable, measured:** the lane spends **~6–21 seconds** per exhibit and **0 seconds** on archival apparatus in
VO, but will spend a **whole beat** on the *reliability class* of a load-bearing source. This is the exact shape your
own §Owning-source-weight rule already has ("The second piece of evidence looks stronger").

---

### 1.3 ⭐ How do they handle evidence that is MISSING, CONTESTED, or INACCESSIBLE?

This is the crux question, so it gets the most space. I found **six distinct moves**, all measured.

#### MOVE 1 — State the falsification test *before* the evidence, so absence reads as a finding

RFB, `UdsPPxaGVUs` 0:00–0:22. He names three opposing claims by outlet — *"USA Today, Gen Z is returning to
Christianity. Axios, young men are leading a religious resurgence… the Gospel Coalition. It's here. Gen Z revival
hits campuses."* — then, at 0:22: **"A real revival would leave a clear statistical footprint, and it's just not
there."**

That single sentence does all the work. Because the test is stated *first*, the absence that follows is a **result**,
not an excuse. Every "we don't have X" for the next eleven minutes reads as the test being run.

*(Inferred, and it's my central structural bet in §2: this is the move #62 is missing-shaped for. "No signed order"
is a weak sentence on its own and a strong one if you've already told the viewer what an order would look like in a
functioning archive.)*

#### MOVE 2 — When the direct evidence is gone, pivot to a *converging set of independent proxies* and name it

Milo, `GyqoGuabkE0`. There is **no** direct evidence of how a six-ton stone travelled 700km. He does not stop. He
runs four independent proxies that each establish *capability and contact*, none of which is about the stone:

1. a gneiss macehead from Lewis found in a burial (~11:30);
2. grooved ware pottery, earliest at Orkney, found at Stonehenge (~11:50);
3. isotope analysis of animal bones at Durrington Walls showing animals walked from Scotland (~12:20) —
   *"If an animal is traveling that far… someone had to travel with it, and maybe they brought a six ton rock
   with them"*;
4. the Orkney vole's DNA, a Neolithic stowaway from Europe (~12:50).

Then he **names the method aloud**: *"It's really incredible the lines of evidence we can tease apart to try and
understand ancient history. The DNA of a vole on a Scottish island can tell us so much."* (13:05, per the prior
study's own extraction — I confirmed the wording in the cache.)

**The structure is: direct evidence absent → four cheap independent proxies → name what they collectively license,
and no more.** He never claims the proxies prove the boat.

#### MOVE 3 — Reason from a physical or institutional *constraint* when documents don't exist

Premodernist, Alexandria, **8:55–10:20 (~40–46% of runtime)**. He has essentially no data — *"We have no
archaeological information — or virtually none. The site of the Museum has not been excavated. And literary
references to the library are very rare"* (5:25–5:35). So he argues from papyrus:

> *"the realistic lifespan of a papyrus roll… Alexandria is not a dry place. It's humid… They would have decayed
> and fallen apart much more quickly, probably within a century or so… None of the books that were put into the
> library in the 3rd century BC would have lasted that long. There would have to be other books. And that requires
> constant maintenance… And that presumes that the library was a stable and functioning and well-funded institution
> all through those centuries, which wasn't necessarily the case."*

He converts an evidentiary void into a **positive argument about what must have been true** — and flags his own
assumption ("that presumes") in the same breath.

#### MOVE 4 — Enumerate the branches of the unknown, refuse to pick, and keep moving

Premodernist, Alexandria, on the Serapeum books: *"Maybe the Christians destroyed the books. Maybe the Christians
took the books and kept them. Maybe they distributed them to churches. Maybe they sold them on the open market. We
don't know what happened to those books."*

Historia Civilis, `s9qlNBBoFG4` **3:17 (20%)**, on the founding murder: **"How much of this actually happened?
Maybe some of it, maybe none of it, but the important thing is that later generations of Romans fully integrated
this story into their own mythology."** — *one sentence*, then he redirects to the thing that *is* documented (the
legal consequence) and never returns.

Same channel, 8:05 (49%): *"there was probably an elaborate religious ceremony each time an elected official crossed
the pomerium, but the details of this are lost to us."* **~5 seconds. No dwelling.**

**Measured discriminator:** the gap gets a *long* beat only when the gap is the video's subject (Alexandria, ~90
seconds). Otherwise it gets **one clause and a pivot**. HC spends 5 seconds admitting a total blank.

#### MOVE 5 — For contested evidence, run the three-step: claim → *mechanism* of the doubt → the independent test

Milo, `9fUAV4DcyD4` 8:08–9:20, the single best template in the sample:

1. **Claim:** the 21–23,000-year-old footprint dates.
2. **Mechanism of the doubt, explained physically:** *"they relied on radiocarbon dating aquatic plants. This is a
   problem because aquatic plants can pull old carbon out of the lake mud and sludge through their roots, and can
   potentially give a much older radiocarbon date than their real age."* (8:12–8:28) Then the concession in the same
   breath: *"The team were obviously aware of this effect and made every effort to ensure the dates were accurate,
   but nevertheless, it created an avenue for doubt."*
3. **The independent test, with a number:** another team radiocarbon-dated *Ruppia* specimens **known to have been
   collected in 1947**; the result came back **7,400 years old**. *"So you can see the problem here."* (8:39–8:58)
4. **The response:** new dating on terrestrial pollen plus OSL, *"totally different method"* (9:05–9:15).

Note what he does *not* do: he never says "critics say." He gives the doubt a **mechanism** and then a **test with
a number**. That's why the beat reads as forensic rather than he-said-she-said.

#### MOVE 6 — Attack the *method*, not the conclusion; and when the opponent's document is real, supply its custody

RFB Gen Z, 3:50–5:30: the Bible Society reported UK male 18–24 attendance jumping 4%→21%. He doesn't call it
false. He routes it through a named scholar — *"the sociologist David Voas, one of the leading experts on religious
change, took a closer look at the data and said, 'Not so fast'"* — and then explains the **sampling method**: an
opt-in YouGov panel, not probability-based, and young adults in opt-in panels *"tend to look very different from
their peers."* Verdict is quoted, not minted: *"Dr. Voas's bottom line is the old cliche that extraordinary claims
require extraordinary data"* — attributed **and flagged as a cliché**.

Atun-Shei, `Lac-8tTuyhs` 6:11–7:09 does the historian's version. The opposing camp produces a **genuine** Lincoln
quote (the Greeley letter). He concedes the quote entirely, then: *"Trouble is, you've taken it completely out of
context. Lincoln wrote that as a public response to an editorial in the New York Tribune… It's worth noting that
when Lincoln wrote that response, he actually had a draft of the Emancipation Proclamation already written and was
just waiting for an opportunity to put it into effect."*

**The move is document custody, not document denial.** Who wrote it, to whom, in what forum, with what already in
the drawer.

#### MOVE 7 (bonus, visual) — show the fragment map

fig tree, `INokIVWNASQ` (~6:10, vidIQ text; timestamp approximate from the cache): on the "Ladies in Blue" fresco —
*"you can see in the picture how many fragments both Evans and Gieron had to work with and which parts of the Fresco
have been made up and created."*

She puts a **reconstruction diagram** on screen: surviving fragment vs. modern infill. Then the killer line, on the
1926 re-restoration: *"so now it's just an interpretation of an interpretation."*

**Inferred, and I think it's the highest-value visual idea in this whole study for #62:** the "which parts are real"
graphic is exactly what a contested archival folio wants.

#### The anti-move: how they stop "no evidence" reading as "nothing happened"

Three mechanisms, all measured:

- **RFB Lilith, 12:26 (67%)** — the absence is stated as a *positive discovery about the tradition*, not a hole:
  *"notice something that's completely missing from all of this evidence — the whole notion that Lilith was the
  first wife of Adam is absent. Where did this come from?"* → the absence immediately **raises the next question**
  and the answer is a named, dated text (the *Alphabet of Ben Sira*, 8th–10th c.). Absence → question → new
  document. Never absence → shrug.
- **Milo, Altar Stone 9:38–10:10** — a chain of negatives that *narrows* rather than empties: *"There's also no
  evidence of glacial erratics on the Salisbury Plain. The Altar Stone shows no evidence of being transported by
  ice"* → *"It's possible glaciers at various times moved the rock some of the way… It's a possibility, but humans
  must have been involved in moving it some way if there's no evidence of glacial action on the Salisbury Plain.
  And there's actually a lot of really good evidence that they moved it all the way."* The negative **forces** the
  positive.
- **fig tree Göbekli 7:42** — the gap is stated flatly and then bounded: *"I'd like to make it very clear that we
  don't know the culture that created this place, we don't know the meaning behind these reliefs — but we can choose
  to see them from a very literal point of view or a more symbolic point of view."* Gap → **enumerate the legal
  interpretations** → carry on.

---

### 1.4 How do they steelman a camp they'll then correct? (MEASURED)

**Order.** Two forms in the sample, and they're for different jobs:

- **Steelman FIRST, per-claim, in one breath (the lane default).** Atun-Shei `nQTJgWkHAwI` 4:17–4:32:
  *"Confederate soldiers went to war for a variety of reasons. Were they defending their homes and families from
  invasion? **Yes.** But they also believed that preserving slavery was in the Confederacy's best interest."*
  Concede → pivot, **15 seconds**, and the concession is a full-throated yes.
- **Steelman LAST, as the humanising landing.** Same video, **7:37–8:05 = 87–94% of runtime**, the closing beat:
  *"I know it's hard to hear that your great grandpappy was all in for slave labor. It's a bummer — even taking into
  account his reasons for believing that, and to him they were good reasons… you want to think of him as this heroic
  defender of hearth and home, not as an enthusiastic foot soldier in the slavers army. But the truth is he was
  both. He was a complicated flawed human being just like you or me."*

**Length.** The per-claim concession runs **10–20 seconds**. The closing steelman runs **~28 seconds**. Neither
is a chapter.

**Attribution form.** The opposing camp is voiced in **its own actual published words** — real YouTube comments
(Atun-Shei), real headlines with the outlet named (RFB), real modern retellings (Premodernist's *"and by this I mean
modern day tellings of the history of the library"*, 1:08). Nobody paraphrases the opponent. *(Measured across all
four debunk videos in the sample.)*

**One thing nobody does:** none of the six adjudicates a *label*. Atun-Shei argues about what soldiers believed and
did; he never rules on a legal category. RFB rules on *"plateau, not revival"* — a description, not a verdict.
Premodernist's whole close is a refusal to assign a villain.

---

### 1.5 What do they NOT do? Where do they refuse to spend time? (MEASURED)

1. **They refuse to litigate adjacent debates, out loud, and outsource them.** Premodernist, twice in one video:
   *"I have reasons for thinking that but I don't want to derail the video by going into all of that"* (0:36) and
   *"You can probably guess what I think of the claim that the Muslims destroyed the Library of Alexandria. But I'm
   not going to talk about that here in this video… check out Al Muqaddimah's video."* **He declines the single most
   inflammatory sub-debate in his own topic, on camera, in nine seconds.** Milo does the small version: *"I don't
   wanna go down a rabbit hole"* (Altar Stone, ~5:10).
2. **They spend no VO on archival apparatus.** Zero call numbers, zero fond/opis/delo, zero tier language in 38k
   words. Provenance rides the card or a single plain clause ("this is directly from his diary").
3. **No scale comparisons. No sinister adverbs.** Confirmed by the prior study's regex over 30,810 words: 0 hits for
   `(quietly|conveniently|neatly) + (erased|buried|vanished)`, 3 incidental hits for scale comparison, none
   rhetorical.
4. **No minted verdict at the close.** Alexandria: *"historical processes usually have complex causes."* RFB Gen Z:
   *"the data leads us somewhere much less dramatic."* Milo: *"this is not the last time you've heard about this
   rock."* All three end on the flattest sentence in the video.
5. **They don't stack scholars.** The lane names **one** scholar per contested point and lets him carry it (Voas,
   Burge, Tony the geochronologist). Nobody runs a four-source credential dump.
6. **They don't re-open a closed question.** *(Inferred from absence — I found no instance in the sample of a
   channel restating an already-settled point later in the video. This is the lane face of your own open-question
   ledger.)*

---

## §2 — MY DESIGN (built from the ledger + §1, before opening the script)

**Target: 12:20, ~2,250 VO words at ~186 wpm.** Design constraints honoured: document-led referee; no legal-label
ruling; the neutrality double-move; ledger-only claims; **Klyachkivsky as the throughline, not Lebed.**

### The spine in one line
*A state is honouring men who cleared a region of Poles. Poland says it was ordered from the top. Ukraine says no
such order exists. Both are describing the same archive folio — and nobody can open it. So here is what the rest of
the paperwork says.*

### The beat sheet

| # | Beat | Question it answers | On screen | Time | Why it's there |
|---|---|---|---|---|---|
| **0** | **Cold open — the ally, not Russia** | Why is Ukraine's closest ally furious with it right now? | Decree, 26 May 2026, "Heroes of the UPA," Special Operations Center "North" (president.gov.ua screenshot) → White Eagle revoked 19 Jun 2026 → Zelensky returns the medal; three ex-presidents return theirs | **0:00–0:45** | Lane MOVE 1 setup. The paradox is the hook; the decree is a real document at 0:15, which is cheap and fast (RFB/Premodernist lead at 6–9%) |
| **1** | ⭐ **The test** | What would "ordered from the top" actually look like in an archive? | Plain card: three things — *an order · reports coming back up · coordination in time* | **0:45–1:25** | **The single biggest structural bet.** RFB's *"a real revival would leave a clear statistical footprint"*. Stating the test first is what turns "no signed order" from a shrug into a result. Also plants the Q→A ledger for the whole video |
| **2** | **The doctrine** | Why would anyone want Poles gone? | Kolodzinskyi, *Military Doctrine*, late 1930s — *"sweep away literally to the last man the Polish element from the Western Ukrainian Lands"* (Himka p.389 print; showable page = *Ukraina Moderna* 20, 2013 reprint, ACQUIRED) | **1:25–2:15** | The HOW: land full of someone else's people is land someone else can claim. Concrete named text, not "nationalism." Voice: mechanism, not adjective |
| **3** | ⭐ **The movement edits itself (the thesis in miniature)** | Can you actually watch a movement rewrite its own record? | **Side-by-side:** Stetsko-autograph facsimile of the 30 June 1941 Act with the *"collaborate closely with National Socialist Greater Germany… under the leadership of Adolf Hitler"* clause highlighted (Himka pp.208–209 / RL p.537 / Piotrowski p.212) **vs.** the post-war reprint with that clause deleted (RL fns ~2036, 2249) | **2:15–3:15** | fig tree's **fragment map**, applied. This is the only exhibit in the ledger where *the doctoring itself is visible in a single frame.* Placed early because it teaches the viewer to read the rest of the video's documents forensically. **One clause only on the German response** ("Berlin wanted a colony, not a client state, so it arrested them") — Sachsenhausen stays out of VO |
| **4** | **The doctrine gets an army** | How does a 1930s pamphlet become 1943? | Snyder p.166 (OUN-B moved to *"absorb the Ukrainian policemen likely to leave their posts after Stalingrad"*); ~5,000 auxiliary police deserted 19 Mar–14 Apr 1943; Siemaszko p.1045 — killing began *on the way to the assembly points* | **3:15–4:15** | HOW>WHY. **Includes the hedge in the same beat** (McBride pp.651–52: don't assume the Holocaust made them killers; the movement *"either found or created killers"*). Lane MOVE 5 discipline, applied to our own claim |
| **5** | ⭐⭐ **TEST 1 — the order** | Is there an order? | (a) Piotrowski p.247 page: *"a secret directive issued and signed by Klachkivskyi"*; (b) **custody diagram** — Piotrowski, Filar, Siemaszko, Motyka, Katchanovski all pointing at **one folio: HDA SBU spr.11315 t.1 ch.2 ark.16**; (c) McBride fn.63 on screen: *"I and other authors have not been able to review this file directly due to recent archival restrictions"*; (d) the published transcription of the **24 Jun 1943 Stelmashchuk→Lebed letter** (Katchanovski pp.15–16 EN; Motyka 2011 p.130 PL) with the inaccessibility caption; (e) Viatrovych's fabrication claim, spoken; (f) the 1963 archival copy photo + the Russian-published copy with Gorshkov's 24 Apr 1945 notations | **4:15–6:30** | The crux gets **2:15** — the most expensive beat in the video, and it should be. Built on lane MOVE 5 (claim → mechanism of doubt → independent test) and MOVE 6 (custody, not denial). **Landing:** what exists is testimony *about* an order, in a file nobody can open — and the letter reports an **oral** directive, so "signed" is a word only the secondary literature uses. Never "no evidence" |
| **6** | ⭐⭐ **TESTS 2 & 3 — the machinery** | If the order is unreachable, what *is* reachable? | Six converging exhibits: **Order No. 11, 4 Sep 1943** (T1 scan in hand — signed "Клим Савур," countersigned Honcharenko; village defence, logistics — show whole, **never crop "зліквідувати"**) · **Order No. 5, 15 Aug 1943** (logistics) · **Order No. 28, 24 Jan 1944** — his own year-summary: *"The armed actions of the Ukrainian insurgent units were a surprise not only for the enemy, but also for our doubting countrymen"* · **map:** 11–12 July 1943, ~100 localities (McBride p.640) / 167 (Snyder p.177), ~4,000 dead in a day; all July 520 localities · **Klymchak after-action report, 30 Aug 1943** — *"I liquidated all Poles from young to old. I burned all the buildings…"* (McBride p.648, framed as a UPA report preserved in a Soviet case file and reproduced by Polish and Ukrainian historians) · Motyka: the Third OUN Congress justified his actions *"though this was not reflected in the official resolutions"* | **6:30–8:30** | **Lane MOVE 2 (converging proxies), and the payoff of beat 1.** Two of three tests come back positive. Landing, plain: *they kept the order deniable; they left the machinery on paper.* Cross-camp seal: Motyka's own rebuttal that the apologists' "lack of UPA documents" is false — *"in reality, surprisingly many survived"* |
| **7** | **The scale, and the method behind the number** | How many, and how do we know? | Siemaszko registry Vol.1 p.208 — slow scroll of named dead with ages, each carrying a source-reference number. **36,543–36,750 documented by name**; 50,000–60,000 estimated for Volhynia 1943; Snyder p.204: ~70,000 Poles to ~20,000 Ukrainians across all contested lands | **8:30–9:20** | Milo's *"how we know"* as the credibility beat. One honest clause: the numbers are Polish scholarship's, and Ukraine's official position disputes the framing more than the arithmetic (Hrytsak accepts ~3:1) |
| **8** | **The other side, at its strongest** | What does the Ukrainian case actually say? | Viatrovych's *"Second Polish-Ukrainian War"*: Sahryń, 10 Mar 1944, ~237 killed incl. women and children (*Enemy Archives* doc 82, Anastazia Shufel's testimony); Chełm 1942–43; his UPA Oct-1943 tally 855:213 — **flagged on screen as UPA's own underground reporting**. Then the custody: the reprisals he leads with are largely **1944, and in the Chełm region** — response, and elsewhere. Then his own concessions: Hanachiv, Feb 1944, UPA *"went beyond the bounds of the permissible."* Then **Poland's own 2016 Sejm resolution**: *"Nor can one dismiss or downplay acts of Polish revenge on Ukrainian villages…"* and Operation Vistula 1947, **140,575** deported | **9:20–10:20** | Atun-Shei's structure exactly: the camp in its own words, then custody, then let the *other* side's own document carry the concession. The label question gets **one sentence and no ruling** — Poland says genocide, Ukraine rejects it, most Anglophone scholars say ethnic cleansing — then Premodernist's move: *this video isn't going to settle a legal category* |
| **9** | **Why it's buried, and why now** | Why is a state honouring them *in 2026*? | 1997 Kwaśniewski–Kuchma declaration → 2003 Pavlivka monument → 2023 Zelensky and Duda mourning together at Lutsk → **then** 2015 law #2538-1 → the 2026 decree → Pantheon bill 15360 | **10:20–11:15** | The acknowledgment→reversal arc is the mechanism, and it is *thesis-defence*: it forecloses "but Ukraine mourns this every year." War is the accelerant — a nation fighting Moscow needs heroes who fought Moscow. **Hard sequencing guard honoured: this cannot move earlier** |
| **10** | ⭐ **The firewall** | Does any of this make "Ukraine is a Nazi state" true? | Hania of Gaj (30 Aug 1943): the childless Ukrainian couple Fedor and Katerina Bojmistruk who took a Polish baby out of a barn of corpses, baptised her to hide her, and when UPA men came, Fedor said she was his daughter and they'd have to shoot him first. VO paraphrase, **no card quote** (PL, Check-A) | **11:15–11:45** | Non-negotiable. And the ledger's own observation is the sharpest version: **the bravest moral actors in this story are Ukrainian.** Second clause, evergreen and dateless: the Soviet state held the central files for fifty years while running anti-UPA propaganda, and never produced a signed order either — the absence is not Ukraine's editing |
| **11** | **Close — flat** | So what is the viewer left holding? | Sources card | **11:45–12:20** | Comprehension → mirror, one universalising example the audience owns (US Founders / Churchill / a statue at home; **Germany-as-inverse** is the hopeful variant). Flat close per lane T2 — answer the opener plainly (the ally is angry because a choice about which past to carry is being made in public), no aphorism, no minted verdict |

### What I deliberately excluded, and why

- **Lebed** — instructed, and correct: the 9 Apr 1943 *"cleanse the entire revolutionary territory"* order (McBride
  p.631) is a real exhibit, but running it as the spine makes the video about a man with no comparable paper trail.
  It appears once, inside beat 5, as the "two theses" fork — nowhere else.
- **The Hitler-question quote** — Row 3, demoted. Unnamed speaker, Polish-underground intelligence report.
- **"Disappear from the face of the earth"** — quarantined.
- **The FSB file dump** — dated; kills evergreen. Its only durable content (Russia never produced an order either)
  survives in beat 10 without a date.
- **Bandera / Sachsenhausen** — one clause maximum. It costs 40+ seconds to do honestly (honourable captivity →
  Berlin → 15 Sep arrest → Zellenbau 1942–43) and it belongs to #63.
- **The 1941 Holocaust strand** (Lenkavsky, Lviv pogrom, Himka's three phases) — grounded, but it is a second video.
  Including it forces either a superficial version or a 90-second detour that pulls the spine off Volhynia.
- **1944 re-collaboration with the Wehrmacht** — genuinely strong and genuinely on-thesis (they buried it *in real
  time*), but at ~30s it competes directly with the firewall beat. Flagged in §4 as a swap candidate, not designed in.

### RESEARCH GAPS my design would need (nothing invented)

1. **The custody diagram (beat 5b)** — every name and the folio locator are in `SOURCE-GENEALOGY.md` Row 5c; the
   *graphic* does not exist. Build as an HTML forensic card per the repo's zero-budget B-roll strategy.
2. **The side-by-side sanitisation graphic (beat 3)** — `EXHIBITS-INDEX.md` still flags the open TODO: a UA reader
   must label which acquired file is the **original** and which the **modified** version, and confirm the
   collaboration clause is legible in the autograph/hi-res scan. **Without that label the beat cannot be honestly
   built** — it would be the exact V5 promise-break the corpus already flags.
3. **Order No. 5 / No. 28 print page-pins** — `SOURCE-GENEALOGY.md` OUTSTANDING #2. If unpinned at lock, they are
   VO-narrated via Motyka with no card.
4. **Kolodzinskyi showable page** — book acquired (*Ukraina Moderna* 20); exact page choice + verbatim check against
   Himka p.389 still pending Check-A.
5. **The "three tests" framing (beat 1)** is *my rhetorical structure*, not a claim from the ledger. It asserts
   nothing new — but it does commit the video to answering all three, so if any test can't be run cleanly the frame
   has to change rather than the evidence.

---

# PHASE 2 — THE DIFF (written after opening `SCRIPT.md` v7.0 and `02-STRUCTURE-SYNTHESIS.md`)

## §3.0 Headline verdict

**The script is essentially sound. There is no missing act, no missing exhibit, and no structural hole.** I designed
independently and landed on the same spine: the ally paradox as the hook, Order No. 11 as the forensic contrast, the
letter framed as a published transcription of an *oral* directive, the Siemaszko named registry as the how-we-know,
Poland's own Sejm resolution carrying the concession, and no ruling on the legal label. A wholesale restructure is
**not** warranted and I am not going to propose one.

What the diff did surface is narrower and, I think, more useful: **four small things, three of which are already
sitting in the script's own ON-SCREEN notes but never reach the ear**, plus two repetitions that pay for them. The
whole package below is **runtime-negative** — about 38 words shorter than v7.0.

---

## §3.1 What my design has that the script does NOT

### ① The strongest rebuttal to Viatrovych is carded but never spoken — so CH8 lands on the opposition's claim ⭐

CH8's crux paragraph ends: *"And Ukraine's answer… is that none of it is real: the confession faked by the KGB, the
letter not even in the file it's cited from."* Then the paragraph stops. The ON-SCREEN note *does* carry the answer
— *"zoom Gorshkov's 24 Apr 1945 notations (the period date-stamp answers 'later KGB fabrication')"* — plus the 1963
HDA SBU e-archive copy.

**So the answer exists, on a card, silently.** The ear is left holding "none of it is real."

This is the one place where the lane's practice and the script visibly diverge. Milo's template
(`9fUAV4DcyD4` 8:39–8:58) is: doubt raised → **independent test with a number, spoken** → *"So you can see the
problem here."* He does not leave the strongest counter-datum on a graphic. And by the script's own open-question
ledger this is a **V3** (raise a question, don't answer it) — the loudest possible one, since it's the video's
central adjudication.

*Genuine omission, not a deliberate exclusion.* I checked `01-VERIFIED-RESEARCH.md` and `SOURCE-GENEALOGY.md`
Row 5b: nothing there argues against speaking it; the ledger's only constraints are "caption must say 1963 archival
copy, not the original" and "do NOT overclaim suppression."

### ② The evidentiary test is never stated — only a narrative one

The cold open says: *"each of these stories has a grain of truth. What we're going to do is look at which of those
grains the documents actually support."* That is a test of **narratives**. The lane's move (RFB `UdsPPxaGVUs` 0:22
— *"A real revival would leave a clear statistical footprint, and it's just not there"*) states what the **record**
should contain, before opening it.

The script does eventually raise it, at CH7's exit (9:50): *"That sounds an awful lot like an order from the top.
But is there any actual proof of that?"* — immediately before answering it. That's clean Q→A hygiene, but it means
the crux has ~15 seconds of setup rather than the whole video's.

*Genuine difference, and a defensible one — but cheap to close (see Rec 2).*

### ③ The custody fan-in exists as VO, not as a graphic

CH8 asks the ear to hold: two pieces of paper, one man, Poland's historians quoting the letter, some calling it a
signed order, the original inaccessible, the file identity `spr. 11315`, McBride unable to review it, and
Viatrovych's denial. The ON-SCREEN note lists all of it. But it lists it as *captions*, not as **one diagram**.

fig tree's move (`INokIVWNASQ`) is the model: the "which parts of this fresco are real and which are infill"
reconstruction map, on screen, resolving in a couple of seconds what a paragraph of VO can't. Here the equivalent is
a fan-in: **Piotrowski → Filar → Siemaszko → Motyka → Katchanovski, five arrows, one folio, one line from McBride's
fn.63, one word: CLOSED.** Every name and locator is already settled in `SOURCE-GENEALOGY.md` Row 5c.

*Genuine addition, zero VO cost.* And it's exactly what the script's own edit-stage note asks for ("documents as
active characters — no document on screen >5s without a zoom/highlight/overlay pointing at the word that matters").

### ④ Order No. 28 and Motyka's "surprisingly many survived" are absent

CH8 gives the forensic contrast as a clause — *"signed everything — orders on defending villages, on tribunals, on
land reform"* — with Order No. 11 on screen. Strong and economical. But two ledger items that would seal the
"absence of a signed order ≠ absence of evidence" landing don't appear anywhere:

- **Order No. 28, 24 Jan 1944** — Klyachkivsky's *own* year-summary: *"The armed actions of the Ukrainian insurgent
  units were a surprise not only for the enemy, but also for our doubting countrymen."* (Motyka, raw-verified
  2026-06-30.) This is his own paper conceding coordination.
- **Motyka's rebuttal** that the apologists' "lack of UPA documents" is false — *"in reality, surprisingly many
  survived."* Cross-camp seal on the whole crux.

*Genuine omission, but priced honestly:* ~35 and ~20 words respectively, into the script's already-longest chapter
(CH8, 522w). These are **fourth and fifth in line**, not top recommendations.

### ⑤ Deliberate exclusions I re-derived and am NOT re-litigating

I checked each against `01-VERIFIED-RESEARCH.md` before listing it:

| My design had | Script's reason for dropping — confirmed |
|---|---|
| Rescuers / Hania of Gaj as the human firewall | **Creator cut at T4**; script's own OPEN QUESTIONS #4 keeps it parked with a named re-entry point (CH7). Its firewall work is done geopolitically in CH10 instead. Not pressing. |
| Hitler-question quote | Row 3 DEMOTED — unnamed speaker, Polish-underground intelligence report. Correct. |
| "Disappear from the face of the earth" | Quarantined. Correct. |
| FSB file dump | Creator call 2026-07-08, evergreen discipline. Its durable content survives dateless in CH10. Correct — and CH10 does exactly what the ledger prescribed. |
| Hunka ovation | `CREATOR-INTENT.md` example guard, parked to #63. Correct. |
| 1941 Holocaust strand as its own beat | Not in the script either; CH4 carries it as one clause inside the police beat, which is the right dose. |

---

## §3.2 What the script has that my design doesn't — strength or bloat?

**STRENGTH, and I got this wrong.** The v7.0 restructure moves *"why does Ukraine honour them now"* from the last
act to CH1 (answered by ~2:30). My design left it at ~10:20, where the original 5-act plan had it. **The script's
choice is better and I'd concede it without argument:** the cold open raises a paradox at 0:30, and leaving it open
for ten minutes is precisely the V3 violation the corpus already names. My placement would have been worse.

**STRENGTH.** Opening cold on the Klymchak report — *"I liquidated all Poles from young to old"* — before the decree.
I had it at beat 6. The script's version puts a perpetrator's own sentence in the viewer's ear at 0:05 and makes the
decree land on top of it. That is a better use of the same exhibit than mine.

**STRENGTH.** CH8's self-burial tail (1944 German weapons deal + the sanitised reprints + the Bandera museum) placed
*late*, as the thesis rhyme. I had the sanitisation graphic early, at ~2:15, to teach forensic reading. The script is
right: spent early it's just a curiosity; spent after "the paper stops" it's the argument. **Do not move it.**

**BLOAT (mild, and the script already knows).** CH4 + CH5 = **483 words / ~2:35** on where the army came from. My
independent design allocated **~60 seconds** to the same ground. The script's own RUNTIME MENU names merging them as
*"the cleanest cut on the board"* (−150w). **Two independent passes landing on the same over-allocation is the
strongest convergent signal in this whole document.** If you take one structural cut, take Cut A.

**BLOAT (small, findable).** The Bandera arrest is stated **twice**. CH1: *"the Germans arrested the movement's
leader in 1941 and held him for three years, two of his brothers died in Auschwitz."* CH3: *"Within a week the
movement's leader, Stepan Bandera, was under guard, and by September he was formally arrested and on his way to
Sachsenhausen."* CH3's version adds the *causal* link (they refused to rescind → arrest), which CH1 lacks — so the
fix is to keep CH3's causation and drop its restatement of the facts CH1 already banked. ~35 words. This is a clean
V4 (re-answering a closed question).

**BLOAT (contested).** The close runs **three** universalising examples — Washington, Napoleon, Leopold II.
`CREATOR-INTENT.md` specifies *"ONE universalizing example."* Three is a list where the doc asks for a mirror, and
the lane's flat-close practice (Premodernist / RFB / Milo all end on the flattest sentence in the video) argues the
same way. Leopold is the one that's *his* — first person, Belgium, and the one a US/UK/CA/DE viewer can't file as
someone else's problem. ~50 words.

---

## §3.3 Where we independently converged (discount for the leakage in §0, but it's still signal)

These beats were reached twice, from different starting points. Treat them as **load-bearing — do not cut them for
runtime**:

1. **The ally paradox as the hook** *(heavily contaminated — `CREATOR-INTENT.md` told me it was locked; near-zero
   independent value)*.
2. **Order No. 11 shown whole as the forensic contrast**, with the "зліквідувати" crop landmine respected. *(Partly
   contaminated via `SOURCES.md`.)*
3. **The letter framed as a published transcription reporting an ORAL directive — never "signed."** Both of us
   landed on the exact same guard, from the genealogy ledger. Clean.
4. **The Siemaszko named registry as the credibility beat, with the method spoken** ("we can name over thirty-six
   thousand of them"). Clean convergence — and both of us reached for it as the *how-we-know*, which is the lane's
   single most consistent credibility device.
5. **Poland's own 2016 Sejm resolution carrying the concession about Polish reprisals.** Clean.
6. **One beat on the genocide/ethnic-cleansing label, no ruling.** Clean, and it matches the lane exactly: none of
   the six channels adjudicates a category.
7. **McBride's caution against the Holocaust→cleansing continuity as an in-beat hedge.** Clean — the script has it
   as a card note plus OPEN QUESTION #5; I put it in VO. Same instinct.
8. **Compressing the army's origins to roughly one minute.** Clean, and the strongest signal here (see §3.2).

---

# §4 — RANKED MENU (5 items, priced, runtime-negative as a package)

> Everything is IDEA tier. Net effect of taking all five: **≈ −38 words ≈ −12 seconds**, i.e. the package pays for
> itself. Take them in order; each stands alone.

### 1. Speak the answer to Viatrovych — don't leave it on a card ⭐ *(the one real gap)*
- **Adds:** closes the video's loudest open question. Right now CH8's crux paragraph ends on the Ukrainian state's
  denial and moves on; the rebuttal (a 1963 copy in the SBU's own electronic archive, and a copy published in
  *Russia* carrying a Soviet general's notations dated April 1945) is on the card, silent. Speaking it turns the
  crux from he-said-she-said into the lane's forensic three-step.
- **Shape (illustrative only — your words):** *"Except a copy of that confession sits in Ukraine's own archive,
  filed in 1963. And another one was published in Russia, with a Soviet general's notes on it dated April 1945 —
  twenty years before the KGB is supposed to have invented it."*
- **Cost:** **+25 words ≈ +8s.**
- **Displaces:** Rec 4 pays for it twice over.
- **Guard:** the caption must still say *1963 archival copy*, not "the original"; and it does not touch the "no
  signature" claim, which is about a different document.

### 2. Make the cold open's test evidentiary, not narrative
- **Adds:** the cold open already promises *"which of those grains the documents actually support."* Naming what the
  record *should* contain — an order, reports coming back up the chain, coordination in time — converts CH8's
  *"at a certain point the paper stops"* from a hole into a **result the viewer has been waiting nine minutes for**,
  and it gives CH6 (simultaneity) and CH8 (the reports) a job they currently do implicitly.
- **Cost:** **+22 words ≈ +7s.**
- **Displaces:** Rec 5 covers it.
- **Risk (state it plainly):** it commits the video to answering all three. It does answer all three — but if you
  don't want a promise on the record, this is the one to skip.

### 3. Build the custody fan-in graphic *(free)*
- **Adds:** CH8's densest paragraph asks the ear to hold five historians, one archive folio, and two contradictory
  characterisations. One HTML forensic card — five names, five arrows, `HDA SBU spr. 11315 t.1 ch.2 ark.16`,
  McBride's fn.63 line, and the word **CLOSED** — resolves it visually in about three seconds. Every element is
  already settled in `SOURCE-GENEALOGY.md` Row 5c.
- **Cost:** **0 words. One graphic build**, alongside the side-by-side reprint already in the production queue.
- **Displaces:** nothing.

### 4. De-duplicate the Bandera arrest (CH1 vs CH3)
- **Adds:** removes a V4. CH1 already banks the arrest, the three years, and Auschwitz. CH3 should keep only what
  CH1 doesn't have — the *causation* (Berlin demanded the proclamation be rescinded; they refused; that's what got
  him arrested) — and drop the restatement.
- **Cost:** **−35 words ≈ −11s.** Nothing is lost; the facts are already landed.
- **Displaces:** n/a — it's a funder.

### 5. Close: three universalising examples → one
- **Adds:** `CREATOR-INTENT.md` asks for **one** example so the viewer turns it on themselves. Three reads as a list
  and dilutes the mirror; the lane's flat-close practice points the same way. Leopold II is the one that's yours —
  first person, and the one a UK/DE/CA/US viewer can't file under someone else's history.
- **Cost:** **−50 words ≈ −16s.**
- **Displaces:** you lose the breadth-of-nations effect (three countries makes it feel like a law, one makes it feel
  like a confession). If the breadth is what you want, keep two and cut one.

---

### Considered and NOT ranked (so you can see what I passed over)
- **Katchanovski's own reliability caveat** (the letter's command titles match end-1943, not June 1943 — possibly a
  later Russian translation). It is the purest referee move available: a caveat from a scholar who *accepts* the
  order existed. But it weakens our own exhibit inside an already-522-word chapter, and CH8 is carrying enough
  forks. Ledger-grounded and available if you ever want it.
- **Order No. 28 + Motyka's "surprisingly many survived"** (§3.1 ④). Real omissions, ~55 words combined into the
  longest chapter. Worth it only if Cut A frees the room.
- **The rescuers / Hania beat.** You cut it at T4. Its lane case is strong (Atun-Shei's closing steelman runs 28
  seconds at 87–94% of runtime and is the beat that makes the correction survivable) — but you've made this call
  once and I'm not re-opening it.
- **Deadpan understatement.** The script header already flags it as below the lane floor, and my pull confirms the
  finding on all six channels (0.8–2.2 per 1k, and **every single instance is a complete sentence with a verb** —
  the fragment is not the lane move). The three places it could sit without touching the killing: the movement
  editing its own founding document, the archive nobody can check, and Russia holding the files for fifty years. It
  costs zero words. Untested on you, so it stays a suggestion, not a rec.
- **Cut A (merge CH4+CH5).** Not mine to recommend — it's already on the script's own menu. But I'll add the one
  thing the menu can't say about itself: **an independent design, built without seeing the script, allocated ~60
  seconds to that same ground against the script's 2:35.** That's convergent evidence Cut A is the right cut.

---

### Honest limits of this document
- **n is small.** 14 videos, 6 channels, ~38k words. The repo's own standard treats n<30 as noise. Rates and orders
  are directional.
- **What's MEASURED:** every timestamp, every verbatim from `tx/*.txt`, the runtime percentages in §1.1, the
  per-exhibit second counts in §1.2. **What's INFERRED:** every "the lane does X because Y," the fast-lead/slow-earn
  split, the mapping of any lane move onto #62, and the whole of §2.
- **`youtube_transcript_api` is IP-blocked** from this machine; timestamped text came from the prior study's cache,
  full text from the vidIQ MCP (no timestamps). No timestamp in this file is reconstructed or estimated.
- **My blindness was partial** — see §0. Convergence claims in §3.3 are discounted where marked; omission claims in
  §3.1 are not affected by the leakage.
- **Nothing here introduces a claim that isn't in `01-VERIFIED-RESEARCH.md` or `SOURCE-GENEALOGY.md`.** Where my
  design wanted evidence that doesn't exist, it's marked as a RESEARCH GAP in §2, not invented.
