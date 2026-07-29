<!-- AUTO:reconcile — do not edit manually, regenerated each run -->
Status: RESEARCH
Lifecycle: _IN_PRODUCTION
Last reconciled: 2026-05-11
<!-- /AUTO:reconcile -->

<!-- AUTO:packaging-lock — managed by packaging_lock.py, do not hand-edit -->
## Packaging Lock (2026-07-28)
title: "Britain and Argentina Claim the Falklands. Both Kept It Out of Court."
FILTERS (pass/fail — all must PASS to advance; PENDING allowed for thumbnail):
  search-anchor:        PASS  (anchors "Argentina")
  clickbait brand-gate: PASS  (no hard_rejects (clickbait tone clean))
  title<->thumb gap:    PASS  (Title carries the searched keyword + the charge: both governments claim the Falklands and both kept it out of court. Thumbnail carries a DIFFERENT fact the title never mentions — the Dependencies split. Concept C maps the South Atlantic with the Falkland Islands Dependencies shaded green + gavel icon (Britain DID litigate there, 1955) against the Falkland Islands in red with the gavel crossed out, overlay 'ONE WENT. ONE DIDN'T.' The title implies nobody ever went to court; the thumbnail reveals Britain went to court over the neighbouring territory and excluded the islands. That contradiction is new information, raises 'which one, and why the difference?', and does not restate any title phrase.)
  thumbnail conditions: PENDING  (no thumbnail concept yet — generate 3 via /thumbnail; not a blocker for research)
ENRICHMENT (recorded, non-binding — cannot override a FILTER FAIL):
  title_scorer:  88/100 (grade A)
  /curiosity:    83/100
  VidIQ MCP:     seed phrase 'falklands malvinas sovereignty dispute' = 0 vol (contradicts keywords.db 1400 — DB figure UNRELIABLE). Real anchors: 'falkland islands' 192,675/mo global / 23,754 GB, comp 58, Overall 64.1; 'falklands war' 185,659/mo; 'malvinas' 98,056/mo but top markets AR/ES/MX (Spanish-language — title deliberately omits Malvinas)   (clickbait-guard: rejected if it pushes a kill-list title)
  NLM P5:        P5 run on Packaging Intelligence nb. (a) Highest differentiation risk = 'Britain Took the Falklands Dispute to Court' (mirrors own #2 'Guatemala vs Belize: What 3 ICJ Cases Show'). (b) two_sentence = 11% outlier rate / 1.51x, best of any formula (n=80); versus = 0/8 outliers niche-wide despite 3.7% channel CTR (n=2). (c) REAL RISK FLAGGED: abstract/academic 2nd clauses underperform — '1922 Treaty Loophole' 0.70% CTR vs 'Turkey and Greece' 3.10%. Dropped 'No Court Has Ruled' (absence) for 'Both Kept It Out of Court' (active agency, falsifiable, document-backed) on that basis.
VERDICT: LOCK VALID
<!-- /AUTO:packaging-lock -->

# Project Status — #55 Falklands/Malvinas

**Working title:** ⚠️ UNLOCKED — see Angle status. The old working title
*"Argentina vs Britain. The Islands Nobody Can Legally Claim."* is **retired**: it delivers the
referee's verdict before the documents do. A title may pose the question; the documents answer it.

**Hook type:** Territorial
**Phase:** 1 — Research (resumed 2026-07-25 from `_BACKLOG`)

## Demand — CORRECTED 2026-07-25

The figure that parked this project was wrong by two orders of magnitude.

| keyword | global/mo | GB/mo | comp | note |
|---|---|---|---|---|
| `falklands war` | 183,312 | **58,447** | 55 | strongest GB anchor |
| `falkland islands` | 180,962 | 18,628 | 58 | |
| `falklands` | 32,550 | 13,563 | 70 | 45% GB / 18% CA |
| `malvinas` | 95,503 | — | 60 | AR/ES/CO/MX/PE — desc+tags, NOT title |
| `de quien son las malvinas` | 4,701 | — | **24.8** | ES searches the sovereignty question directly |
| ~~`falklands malvinas sovereignty dispute`~~ | **1,400** | — | — | ❌ the bad narrow term that caused the `_BACKLOG` park |

**Dead anchors — do not build on these:** `falkland islands history` (0 vol) ·
`falklands oil` (0 vol) · `sea lion oil field` (0 vol, comp 96) · `who owns the falkland islands` (0 vol).
→ **The oil/petrostate angle has no search demand.** If it appears, it is a body beat, never the anchor.

## Angle status — 🔓 OPEN (deliberate, creator directive 2026-07-26)

**The hook and scope are NOT locked and will not be locked until Phase 2 surfaces what the sources
actually carry.** Everything below is a *hypothesis from a Wikipedia-tier brief*, not a finding.
Per `feedback-topic-vs-angle-ordering.md` the angle locks AT research, not before it; per
`feedback-open-research-prompts.md` a brief supplies criteria, not pre-selected candidates.

Candidate directions carried into Stage B (ranked by current interest, NOT by confidence):

| # | Candidate | Status | What would confirm it |
|---|---|---|---|
| 1 | **Mutual abandonment** — Britain withdrew 1774 (plaque, no garrison), Spain 1811, Argentina silent 1850–84; each side's best evidence is another's departure | hypothesis | Goebel on 1774; treaty text on 1850; diplomatic record on the 34-year silence |
| 2 | **USS *Lexington* reversal** — the US wrecked Puerto Luis in 1831, so what Onslow displaced in 1833 was already a ruin | hypothesis, **highest interest** | US naval records / Duncan's report; Goebel. Must establish what was actually standing in Jan 1833 |
| 3 | **The 1850 acquiescence question** — does the Arana–Southern Treaty mention the islands at all? | directly answerable | Read the treaty text (EN/ES, published) |
| 4 | **Jewett's nationality** — Argentina's first flag raised by an American-born privateer | supporting detail | Goebel; US privateer records |
| 5 | **The 1771 paradox** — both sides returned while formally reserving sovereignty; the template for 250 years of non-resolution | hypothesis | 1771 declaration text |
| 6 | **Self-determination vs *uti possidetis*** — the two principles collide and the UN cannot rule without unsettling Gibraltar and Chagos | framing, not a finding | Beck, Laver; ICJ case law |

**Scope also open:** the video may run pre-1833 only, 1833→present, or the legal-mechanism cut.
Do not pre-commit the runtime window.

**Standing constraint:** whatever surfaces, the verdict is carried by documents and both camps get an
affirmative defender (`feedback-referee-steelman-sourcing.md`). No camp is pre-assigned the loss.

## Phase tracking
- [x] Demand validated (re-scored 2026-07-25 — see correction above)
- [x] Preliminary brief (wiki-researcher, 2026-05-10)
- [x] Competitor landscape + comment mining (2026-07-25 — 10 videos, 700 comments)
- [x] Topic viability gate → **PROCEED** (`RESEARCH-VIABILITY.md`, 2026-07-25)
- [ ] Stage B — source sweep + library intersection + NLM notebook
- [ ] Phase 2 sources (NotebookLM) — **the step never started**
- [ ] Angle lock (blocked until Phase 2)
- [ ] 90% claims verified → script unlocks

## Historian Stage State
**Current stage:** Stage A — Historiographical Baseline (locked 2026-07-26)
**Next stage:** Stage B — Source Criticism
**Outstanding flags:**
- Brief Step 2 never completed (Gemini quota throttle 2026-05-10) — 3 Wikipedia articles unfetched:
  `Re-establishment_of_British_rule_on_the_Falklands_(1833)`, `Falkland_Crisis_of_1770`,
  `History_of_the_Falkland_Islands`. Covers the 1833 event, the 1771 paradox, and the two timeline
  gaps (1835–1884, 1884–1965). Low priority — Stage B academic sources supersede.
- Goebel (1927, Yale UP) is the load-bearing acquisition; 4 T2 claims route through it. If
  inaccessible, re-run the Check A T-tier projection.
**Stage A locked:** 2026-07-26
**Stage B locked:** pending
**Stage C locked:** pending

## Notes
- Live window (hook material only, not the spine — `feedback-evergreen-not-news.md`): World Cup
  banner 2026-07-20 · leaked Pentagon memo on US support Apr 2026 · Chile backing Argentina Apr 2026 ·
  Sea Lion oilfield approval Jul 2026.
- Competitor + comment-mining evidence: **`_research/comment-mining/`** (filed 2026-07-26) —
  `COMPETITOR-AND-COMMENT-FINDINGS.md` (the analysis), `comments-extracted.txt` (700 comments,
  10 videos, like-sorted), `extract_comments.py` (reusable), plus the 10 raw yt-dlp `.info.json`
  files as source of truth.
- **NLM notebook CREATED + LOADED 2026-07-26:** `cc7b41e9-79ef-4244-88f7-3dcfce3af89f` —
  https://notebooklm.google.com/notebook/cc7b41e9-79ef-4244-88f7-3dcfce3af89f
  (confirmed via `notebook_list` first — no pre-existing Falklands notebook among the 72 owned).
  **25 sources uploaded.** Academic: Goebel · Pascoe&Pepper · Kohen&Rodríguez · Trinidad(2018) ·
  Gustafson · Beck · Dolzer · Mira&Pedrosa(2021) · Freedman Vol.1 · Hoffmann&Hoffmann · Perl
  sourcebook · Calvert · Gough · Filmus et al.(2021,ES) · Lorton · Chagossians/self-determination
  article. Primary: 1771 Agreement · 1850 Arana–Southern · UNGA Res.2065 · Argentine Constitution
  1994 · Jewett 1820 declaration · **Duncan USS *Lexington* report** · Shackleton 1976.
  Framework (owned library): Benton · Anghie.

- **⚠ FLAGGED — creator must download manually (ICJ returns 403 to all automated fetching;
  URLs verified valid via WebFetch):**
  - `https://www.icj-cij.org/sites/default/files/case-related/169/169-20190225-ADV-01-00-EN.pdf`
    — **Chagos Advisory Opinion 2019** (highest priority; the live precedent)
  - `https://www.icj-cij.org/sites/default/files/case-related/69/069-19861222-JUD-01-00-EN.pdf`
    — Burkina Faso/Mali 1986 (*uti possidetis*)
  - `https://www.icj-cij.org/sites/default/files/case-related/120/120-20071008-JUD-01-00-EN.pdf`
    — Nicaragua/Honduras 2007

- **ABANDONED (searched, not obtainable / not worth further cost):** HMS *Clio* log + Onslow
  despatch (TNA paid order only — Goebel/Perl/Lorton quote it) · Laver · Cawkell · Tatham ·
  Caillet-Bois · Destéfani · Kohen *Possession contestée* · Springer "Distant Sovereignty" chapter
  (chapter-only, not worth a volume). None load-bearing; camp balance survives via
  Kohen+Filmus (AR) vs Pascoe+Lorton+Freedman (UK) and Dolzer+Hoffmann+Trinidad (third-country).

- **IDENTIFIED 2026-07-26** (scanned, no OCR layer — identified by uploading and querying NLM's
  vision, then renamed in-notebook):
  - `The question of the malvinas.pdf` = **[P9] Argentine MFA, *"The Question of the Malvinas
    Islands: A story of colonialism. A United Nations cause"*, Sept 2012** — the official Argentine
    government dossier. This was [P9] on the sweep list; creator obtained it without it being named.
  - `bilpai4751m.pdf` = **[P2b] Arana–Southern Convention 1849, full bilingual EN/ES text**
    ("Convention for reestablishing the perfect relations of friendship between Her Britannick
    Majesty and the Argentine Confederation"), signed Buenos Aires 24 Nov 1849 by Felipe Arana and
    Henry Southern. Argentine-scanned 2005. Complements the other 1850 copy already uploaded.
  - `Treaties_and_Other_International_Acts_of*.pdf` = Hunter Miller, *Treaties and Other
    International Acts of the United States* (1,376pp + 1,159pp). **NOT uploaded** — almost certainly
    belongs to #51 Treaty of Tripoli. Creator to confirm before it enters this corpus.

- **🔎 FIRST RESEARCH FINDING (PRELIMINARY — needs raw-read confirmation):** querying [P2b],
  NotebookLM reports the Arana–Southern text *"focuses on the restoration of peace and commercial
  relations **without explicitly mentioning the Malvinas sovereignty issue**."* If that holds, it
  directly answers **candidate angle #3** ("does the 1850 treaty mention the islands at all?").
  ⚠️ **Do NOT script this yet.** It is (a) a synthesis, not a raw read, and (b) an *absence* claim —
  the most dangerous kind to take from an LLM summary. Per `reference-nlm-raw-read-verification.md`,
  confirm by reading the full clause list in the raw source before this becomes load-bearing.

---

## Session log — 2026-07-27 (collection pass, ledger C44–C47)

**Mode:** collection only, per creator directive. No scripting. Angle still formally OPEN.
**Ledger:** 43 → **50 claims**. 8 new exhibits, all free, **£0 spent**.

**Creator steer received mid-session:** *"I feel like we are going more in a law direction rather
than history."* Accepted and applied. **Standing boundary from here: international case law is
behind-camera only — it exists to stop us saying something false, never to be explained on screen.
Zero doctrine in VO.** The three case reports were read for that purpose and are filed as guards,
not as beats.

### What was collected
- **C44** — *Antarctica (UK v. Argentina)*, **UK Application to the ICJ, 4 May 1955**, read directly.
  Britain's own footnote limits its consent to nothing "outside the Dependencies"; Britain lists
  "actively seeking to bring the dispute to arbitration or judicial settlement" among the marks of a
  maintained title. Character-verified against page images. Also *Clipperton* (1931), *Eastern
  Greenland* (1933), *Minquiers* (1953) read directly — **all three cut against our abandonment
  reading**, and *Minquiers* weakens the C40 analogy in Britain's favour.
- **C45** — **G. G. Fitzmaurice** appears in the *Minquiers* judgment as UK counsel and spoke; the
  Court found unanimously for Britain. Filed with a hard guard: **this is not hypocrisy.**
- **C46** — **Charlton** whole-book sweep. Five senior Argentines, 609K chars, **zero** instances of
  Argentine internal doubt → **C39a hardens**. The real mirror is **Hugh Carless on the Beagle
  Channel**: Argentina *asked for* arbitration with Chile from 1902, and repudiated the 1978 award.
- **C48** — **Written answers CLOSED** (see below). Recovered **Macmillan, 6 May 1955**.
- **C47** — **Hansard arbitration limb CLOSED** (3,141 contributions; `arbitration`/`arbitral`/
  `The Hague`/`Malvinas`). Recovered **McNeil, HC Deb 16 Feb 1948 vol 447 cc822-3**: *"we can only
  regard this as evidence that they have no confidence in their ability to dispute our legal title."*
  All quotes exact-substring verified on independent refetch.

### What changed in the thesis (both narrowings, both against us)
1. **"Britain refused because it knew it would lose" is dead** — not on our reasoning, on Britain's.
   In 1955 Britain told the Court the case law *negatived* Argentina's claim.
2. **The doubt chain cannot be scripted as a single accumulating 1829→1946 verdict.** C37b flagged
   it, C41d softened it, C44f closes it.

### Money saved
**`SOURCE-ACQUISITION-QUEUE.md` Priority 1 is now empty.** Both queued items (Moore's AJIL letter;
Jennings 1963) existed only to license the "refusal implies weak title" inference. **McNeil 1948 and
Britain's 1955 filing both say it, free and on the record. Do not buy either.**

### Corrections made to our own prior work
- **C43d amended** — the "twelve-year silence" was vocabulary-bounded; Boyd-Carpenter/White,
  7 Nov 1966, sits inside it. Finding survives and strengthens; the phrasing does not.
- **C43g / agent report annotated** — the earlier "zero written answers" figure is meaningless. The
  Hansard `Written` search index returns zero for every term in every period; it is a **dead index**.

### Biggest remaining hole — CLOSED same session (C48)
~~Written answers 1948–68 unswept.~~ **Done.** Built the day-index walk (the search API's `Written`
index is dead — returns 0 for every term in every period). **3,097 sitting days walked, 123 relevant
written answers fetched and read; 6 mention the Court/arbitration/Hague and all six are Dependencies-
or Antarctic-scoped.** The negative holds in the written record with no exceptions.

→ Recovered **Macmillan, `HC Deb 06 May 1955 vol 540 cc178-80W`**: the arbitration offer was made in
identical Notes of **21 December 1954**, as the alternative to the Court, and Argentina and Chile both
rejected it. Britain filed at the Court **4 May 1955** — two days before Macmillan spoke, and the same
filing whose footnote excludes everything outside the Dependencies (C44a). **Two independent primaries,
one event, one week.**

→ **C48c: the conflation is now fully decomposed — four limbs, all true, all mislabelled.** Inglewood's
June 1968 arbitration limb (C43c's "real remaining gap") was the last unexplained element; it traces to
21 Dec 1954. ⚠ This is the *anatomy*, not the *transmission* — C43e(3) still binds: no causal story, and
never say the conflation "began" anywhere.

**Standing method note for this repo:** never use `search/contributions/Written.json` for the historic
corpus. Walk `historic-hansard`'s own `sittings/YYYY/mon/DD` day indexes.

### C49 — Groussac was unreachable; a better route closed instead
Groussac 1910 is not in the library, not on archive.org, and Google Books' API quota is exhausted —
**not acquired.** But chasing **Greig's footnote 63** (never opened before) led to the
**Argentine MFA note of 4 May 1955** in the ICJ Antarctica Pleadings pp.91–93, free, read directly:

- **Argentina refuses the Court and arbitration *because* Britain won't address the Malvinas** — the
  exact counterpart to Britain's footnote excluding them (C44a). **Both documents are dated 4 May 1955.**
- **Argentina names Britain's pre-1930 jurisdictional reservation, publicly, in 1955** — the same
  reservation this project recovered from British internal files via Beck/Greig (C24d, C30d). ⚠ Argentina
  asserts the reservation's *existence*, never Hurst's *intent*; that stays attributed to C30d.
- The **21 Dec 1954 arbitration offer** is now confirmed by three primaries and both governments, and
  its scope — "dependencies of the Malvinas" — is attested in Argentine words too.

**1844: flag stands, and route (a) has now failed twice.** Greig's n.63 resolves back to the same Godwin
memorandum; Argentina's own 1955 note never cites 1844. **Do not restore it.** Cold open should move to
**McNeil 1948** or the **4 May 1955 pairing** — both free, both primary, both stronger.

### C50 — Freedman's Official History. The counter-evidence pass, and it paid the most.
Ran target 4 by asking what argues *against* the thesis. Freedman (archive-privileged official history,
755K chars, ~unmined) produced more counter-evidence than new supporting material — which is the point.

- 🛑 **C50a — the official historian rejects the private-doubt motive in terms** (p.19): transfer was
  contemplated "not because of a lack of confidence in the claim but more in their ability to sustain the
  Islands." **Must be carried in any motive beat, same footing as Greig C38a.** ⚠ Official ≠ neutral —
  label him.
- 🛑 **C50c — Thatcher personally proposed going to the ICJ, late March 1982** (p.180); Carrington
  redirected it to South Georgia legality and it died on Argentine consent. **The hardest fact against
  the spine.** Survives as behaviour (nothing submitted on sovereignty) — and it makes her 29 Apr 1982
  Commons line (C33a) sharper, four weeks after the fact. **Never script as "Thatcher lied." She didn't.**
- ⭐ **C50b — the doubt chain now reaches late 1981** (p.29): FCO Research Department found the case rested
  "almost entirely on 148 years of continuous settlement", untested given the "probable in-built
  anti-colonial bias" of the institutions. **That is a THIRD motive** — not weak case, not
  non-justiciable, but *biased forum* — and it mirrors Argentina's 1955 complaint exactly (C49b).
  **C38c's table amended to three columns.**
- ✅ **C50d — C37a's flag ANSWERED and the suppression reading is dead** (p.18): the 1983 Select Committee
  was about to conclude when **the general election intervened**; the reconstituted Committee was "unable
  to reach a categorical conclusion." **A dissolution, not a hand on a file.**
- 🎯 **C50e — Freedman states the behavioural spine himself** (p.18): "there has never been any formal
  presentation of the British claim before any international or judicial" body; "law has mattered less
  than power and determination." **The spine no longer rests only on Hansard.**
- Negatives: **no Argentine internal doubt in Freedman either** (C39a holds after a fourth source);
  **Minquiers contrast made by nobody** in the ten-source corpus (Gustafson 0, Freedman 0, Hoffmann 0,
  Calvert 1 on the merits) and **`Optional Clause` appears only once in ten sources** (Beck). C40f's flag
  stays open but is well-bounded — corpus statement, not a novelty claim.
- 1884 gains a fourth scholar (p.26). **1844 now outnumbered four to one.**

### Not run this session
~~Target 4~~ — **Freedman done (C50); Gustafson/Hoffmann/Calvert term-swept only, not read through** ·
~~Target 5 (Groussac)~~ — **attempted, unreachable free; superseded by C49** ·
Charlton remains ~80% unmined on the 1970s leaseback chapters (the *forum* question in it is
exhausted — C46a is the answer and it is a negative).

### Flags unchanged
1 DIRECTION NEEDED (Beck vs Greig, 1844) · 4 LIBRARY ACQUISITION · 2 NEED SOURCES.
**The 1844 arbitration request remains demoted and must not return to the cold open** without a
second witness.

---

## GREENLIGHT — 2026-07-28. VERDICT: **GO**. Angle LOCKED (reframed).

Run as `/greenlight --full`. Packaging lock written above (VALID). This closes the gate the project
skipped: five research passes and 50 claims had accumulated with **no packaging artifacts and the angle
formally open**.

### The reframe, and why
Research spine (forum avoidance) is a **`legal`** video. Channel record: `legal` median 57 views, n=5,
**ceiling never broken above 300**. `territorial` median 155 — but **all five of the channel's breakouts
are territorial, without exception**. (Means are useless here: Guatemala is 71% of all territorial views.)

The 25-July comment-mine — 700 comments, 13% legal-signal, 22% on the one sovereignty video — asks for
**the claim adjudicated**, not for the forum question. Not one demand quote asks why no court has ruled.

→ **Decision: do not switch the angle — switch the promise.** Territorial framing ("both claim it"),
forum research as the payload. Zero new research required; all 50 claims stay load-bearing. The 1833
material stays where the triage doc put it (the reason the question is hard, not its own act).

### The template is already on the channel
Authoritative Studio export (2026-07-23, lifetime — `studio_ctr_rows`, NOT `videos.impressions` which
is garbage):

| impressions | CTR | video |
|---:|---:|---|
| 44,295 | **9.18%** | Guatemala vs Belize Dispute: **What 3 ICJ Cases Show** |
| 292,398 | 7.66% | The Country That Might Disappear: Guatemala vs Belize |
| 36,263 | 4.30% | Venezuela vs Guyana: Essequibo |
| 22,034 | 3.20% | Turkey Claims 152 Greek Islands |

**The ICJ-framed territorial dispute is the channel's highest-CTR video at meaningful volume.** Territorial
framing + court payload is a proven combination here, not a hypothesis.

### Locked working title
> **Britain and Argentina Claim the Falklands. Both Kept It Out of Court.**

69 chars · two-sentence declarative · `title_scorer` 88 · `/curiosity` 83 · anchors "Argentina" in the
first 40 chars.

**Why not the higher scorers.** `"…Read the Documents."` scored 98 but "Read" is homework framing (CTR
kill-list). `"Britain vs Argentina: Both Kept the Falklands Out of Court."` scored 96 but "Britain vs
Argentina" reads as a **war** video — and 9 of the top 10 competitors are combat, so it walks into the
saturated lane and then disappoints. **Scores are enrichment; both were rejected on judgment.**

**Why "Both Kept It Out of Court" and not "No Court Has Ruled".** The packaging notebook (P5) surfaced a
documented failure mode: abstract/academic second clauses collapse — *"The 1922 Treaty Loophole"* **0.70%
CTR** vs *"Why TURKEY and GREECE Can't Agree"* **3.10%**. "No court has ruled" is an *absence*; "both kept
it out of court" is an *act* by named parties, falsifiable and document-backed. Traded 5 mechanical points
for that fix.

### Live SERP shelf (12 titles, `channel-data/serp-studies/titles/falklands-malvinas-2026-07-28.md`)
`how_why` 6/12 saturated · **evidence-promise 0/12** · **two-sentence "Claim. Evidence." 0/12** · years
0/12. The chosen title occupies the two-sentence whitespace and avoids the saturated pattern.
⚠ Closest competitor to beat: **"Does Argentina's Claim to the Falklands Actually Hold Up?" — 152,777
views.** Adjudication framing works and is already occupied by a question-framed video; ours is declarative.

### Demand — GO, but the DB figure is WRONG and must not be reused
🛑 **`keywords.db` says `falklands malvinas sovereignty dispute` = 1,400/mo. VidIQ says 0.** The long-tail
phrase is a description, not a search target. **This is the same class of error the project was parked for
(a demand figure wrong by 100×) — do not cite the 1,400 again.**
✅ The GO rests on the **parent** keyword: `falkland islands` **192,675/mo global, 23,754/mo GB**,
competition 58, Overall 64.1 · `falklands war` 185,659/mo. Keyword-ladder satisfied: famous parent
anchored, the court finding delivered as the reveal.
⚠ `malvinas` is 98,056/mo but top markets are AR/ES/MX — **the title deliberately omits "Malvinas"** to
avoid pulling Spanish-language searchers who won't retain on an English video.

### Signals
- **Cluster: EXTEND** — `13-belize-icj-endgame`, `35-gibraltar-treaty-utrecht`, `6-bir-tawil` published;
  the nearest sibling is the channel's #2 video *and* its highest CTR. Inherits Suggested adjacency.
- **Outlier: NO** — competitor cache returns 0 similar videos (stale scrape, not a real negative).
  Relying on demand + hook, which is acceptable but noted.
- **Audience:** both segments — Correctionist (document-driven debunk → sub conversion) and Lifelong
  Learner (territorial → views). The corpus names this combination as the ideal and says Essequibo only
  partially achieved it.

### Thumbnail — PENDING (not a blocker)
Three concepts drafted, **all PASS `thumbnail_checker`** (territorial, no face, map element, ≤3 words).
Lead is **Concept C**: South Atlantic map, Dependencies green + gavel, Falklands red + gavel crossed out,
overlay **"ONE WENT. ONE DIDN'T."** ⚠ Concept B (the 1955 footnote as hero) is deprioritised —
document-as-focal-point is the channel's CTR floor on famous topics (−2.11). Render + `/thumbnail` next.

### ⚠ The one real risk, carried forward
If the title promises adjudication and the video concludes "nobody can adjudicate it," that is a
bait-and-switch. **The video must deliver a verdict on the evidence** — Dolzer concludes for Argentina,
Trinidad says the referendum cannot settle title, the 1946 FO memorandum calls 1833 "an act of
unjustifiable aggression," and *Palmas* arms both sides — with the forum failure as the reason it is still
open. **Not a shrug.**

### Next
`/script`. Runtime and beat order per `TRIAGE-AND-OPENER-DECISION.md`, **but the cold open must be
re-decided**: the 1844 arbitration quote it currently specifies is the demoted single-source claim
(C36 → C49e). Replacements, both free and primary: **McNeil, HC 16 Feb 1948** (C47a) or the **4 May 1955
pairing** (C44a + C49a).
