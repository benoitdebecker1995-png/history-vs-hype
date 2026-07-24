# Continuation prompt — build the project around primary-source hunting

> Paste the block below into a fresh session to pick this up. Created 2026-07-04.

---

Strategic build: **make primary-source hunting the spine of the History vs Hype project.**

**Why this matters (internalize, don't re-derive).** This channel's product is the *trust that we're the ones who actually opened the primary document.* The format is a document-led referee where the primary carries the verdict; the subscriber trigger is intellectual competence. On the most contested topics on earth (Israel/Palestine, colonial history, ideological narratives), a single mis-sourced on-screen claim is *self-refuting* — it proves the referee is doing the exact thing the channel exists to expose (hype dressed as fact) and collapses the trust the whole catalogue runs on. The creator is effectively a one-person research desk, so the rigour has to be **institutionalised**, not dependent on a lucky deep-dive. Primary-source rigour here is simultaneously the differentiation nobody can copy and the insurance against the one class of mistake that ends the channel.

**What already exists — READ THESE FIRST, don't rebuild:**
- `.claude/agents/primary-source-hunter.md` — agent (built 2026-07-04). Traces ONE claim DOWN its citation ladder to the most-primary *showable* source: raw-reads the cited source (never `notebook_query` synthesis — it fabricates), follows footnotes down, tiers provenance (primary doc > participant testimony > secondary scholar > advocacy), leaves the notebook for the open primary record when it bottoms out, works an **access-route repertoire** (owned-library → free-reproduction-of-same-doc → free repos → the-one-page → OA/author → ILL/e-access → archive scan-order → press-proxy → FOIA → purchase), retrieves/renders the actual document, and reports **the rung reached + the route + what climbing one rung higher costs**. Canonical baselines in the file: #59 Liberia→Forrestal Diaries p.331, Philippines→FRUS d910, 84%→Kattan→Khan's A/PV.126 speech→a UK-delegation paper.
- Infra to WIRE INTO (not rebuild): the Drive Source Library project (~2,000 PDFs), `library/by-topic/` + the OWNED/ACQUIRE tagging (`feedback-check-owned-library`), the NLM ingest pipeline (`notebook-researcher` agent), `/translate` (clause-by-clause + cross-check — for foreign-language primaries), `/verify` (claim-vs-notebook + the 7.7/7.8 attribution audit + Step-0 coverage gate).
- Discipline in memory: `reference-nlm-raw-read-verification`, `feedback-notebook-before-web-for-provenance`, `feedback-primary-source-ladder`, `feedback-auditors-edge`, `feedback-attribution-audit`.

**The model to HOLD (do NOT collapse to a tidy taxonomy):**
- Two layers, different access profiles: the ON-SCREEN layer (gov/UN/archival primaries — mostly public-domain, free) vs the BEHIND-CAMERA scholarly layer (paywalled monographs, used to *trace to* the primary and *tier* the evidence).
- Access is a **repertoire, not three buckets**: per claim, try the routes cheapest-first and report the best rung reached + the move to climb higher. **Foreign-language primaries are a STRENGTH** (untranslated evidence = the channel's moat); multilingual official texts where the *version-discrepancy itself is the evidence* (Treaty of Tripoli Art.11, Sabah, Wuchale/Adwa) are a target for *two originals side-by-side*. **Gated primaries:** split the document from its container — hunt a free reproduction of the *same* document first; a PD record trapped in a paid edition can be shown and cited to its archival origin.

**Boundary:** help locate + legitimately access + organise sources; do NOT automate downloading copyrighted works from shadow libraries — that's the creator's manual call.

**The build — open fork. Propose the architecture, then build the slice the creator picks:**
1. **Acquisition/library engine** — given a citation: check the owned library first, resolve the exact edition (DOI/ISBN), surface legitimate access routes.
2. **Hunter as the mandatory `/research` spine** — every load-bearing claim gets a source-genealogy (root primary + showable file + provenance tier) before it can be filed in `01-VERIFIED-RESEARCH.md`.
3. **Retrofit #59 first** — run the hunter across every load-bearing claim in the #59 script, produce the showable-primary set, learn what breaks, then generalise.
4. **Map the full engine** — write the architecture doc for the acquisition→hunt→ingest→tier→show loop, then build slice by slice.

**Start by:** reading `.claude/agents/primary-source-hunter.md` + `CLAUDE.md`, restating the vision in one paragraph to confirm alignment, then proposing the engine architecture and asking the creator which slice to build first.
