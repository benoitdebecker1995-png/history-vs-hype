# Comment-Mine Signal Analysis — #56

**Run:** 2026-05-12
**Videos mined:** 3 (yt-dlp, 50 comments cap each)
**Total comments collected:** 101 (V1=50, V2=50, V3=1)

## Source pools

| # | Channel / Title | Views | Comments pulled / Pool | Useful for angle? |
|---|---|---|---|---|
| V1 | Hasanabi Productions — *Asmongold's INSANELY RACIST RANT On Africans* | 59K | 50 / ~380 | ❌ Streamer-fight noise, no historical-substance signal |
| V2 | Africa Today — *"Africans Sold Their Own": What Really Happened* | 26K | 50 / ~667 | ✅ Dense engagement with the exact claim |
| V3 | The Ancients Tales — *The Day Lagos Was Taken: Oba Dosunmu and the British Betrayal (1861)* | 94 | 1 / ~1 | ❌ Pool too thin (single "Nice 👍") |

## Signal table by angle

| Angle | Signal count | Strength | Top comment |
|---|---|---|---|
| **Synthesis — concede-the-kernel** ("yes, Africans were complicit AND that doesn't exonerate Europe") | **6+** | ★★★★★ | V2#1 (8 likes): *"Africa was an accomplice in the trade. Admitting to this does not make the trade less egregious."* |
| **Beat 2 — Zurara / 1441 Portuguese raid + Henry the Navigator** | **2 strong** | ★★★★ | V2#9 (1 like): *"According to the Portuguese documents in 1441, they were already kidnapping Africans before they ever negotiated with any African rulers. In their own documents, they kidnapped 165 Africans and sold them in Lagos Market in Portugal. Prince Henry the Navigator, was involved."* |
| **Demand-shaping causal chain** ("who built the infrastructure, who supplied the weapons") | **2** | ★★★ | V2#32: *"Who built the enslavement and slave trading infrastructure and market? Who provided the incentives, weapons and ammo that created the African warlords and slave hunters?"* |
| **Beat 1 — 1861 Lagos / Dosunmu specific** | **0** | — | No commenter engaged with Dosunmu, 1861, or the Treaty of Cession |
| **Arab / Trans-Saharan slave trade (NOT covered by our video)** | **7** | ★★★★ unmet | V2#5: *"What of the trans sahara/sahel slave trade? Why is it been ignored?"* |
| Reparations political-tribal noise | 15+ | — | Out of scope, don't serve |
| Asmongold-personal insults | most of V1 | — | Out of scope, don't serve |

## Key findings

### 1. Concede-then-deploy is the dominant unmet demand (★★★★★)

Multiple Africa Today commenters volunteered the *exact* framing of our synthesis beat — "yes, kernel of truth, AND" — including the top-liked comment (8 likes). The Africa Today video itself appears to push a stronger anti-complicity line; its audience is doing the nuance work the video isn't. **This validates Rule 40 Baseline-Before-Exception (concede the easy fact, deploy the harder document) as the structural fit for the topic.**

Signal comments:
- V2#1 (8 likes) — concede + deploy
- V2#6 (1) — Yoruba commenter accepting partial responsibility
- V2#25, #35, #42 — degree-of-participation engagement
- V2#46 — engaging with the literal Asmongold claim text

### 2. Beat 2 (Zurara / 1441) is already a partial audience touchstone (★★★★)

V2#9 cites the Portuguese 1441 documents and Henry the Navigator by name and gets a like — the audience has *already* worked out the implication. Our edge: bring the *actual chronicle on screen* (Zurara Beazley/Prestage translation), not just the historical fact in a sentence. This is the Auditor's Edge advantage made concrete.

### 3. Beat 1 (1861 Lagos) is white space — opportunity AND risk

Zero comments engage with Dosunmu / 1861 / Treaty of Cession. Two reads:
- **Opportunity:** no competitor occupies this gap; the document layer is genuinely unowned
- **Risk:** topic may be too niche to drive volume

The two-beat structure lets Beat 2 (Zurara — validated demand) carry algorithmic volume while Beat 1 (1861 Lagos — differentiation) carries the documentary edge. This is the right shape.

### 4. Arab / Trans-Saharan slave trade is a significant unmet demand we don't serve (★★★★)

Seven V2 comments demanded coverage of the Arab/Trans-Saharan story. We're not covering this (scope is Atlantic). Two operational responses:
- **Pinned comment / script aside:** explicitly scope-bound the video to Atlantic, name the Arab/Trans-Saharan trade as a separate question worth its own treatment
- **Future video candidate:** "The Arab slave trade documents Europeans don't know" — note in `TOPIC-PIPELINE.md`

Not addressing this leaves ~14% of engaged audience unserved. Acceptable for a vibes test; flag in synthesis.

### 5. Streamer-reaction format has no historical-substance comment ecosystem

V1 (Hasanabi 59K) comments are tribal/insult-driven. Zero pull-through to historical engagement. This reinforces the channel-data finding that pure reaction-format underperforms — our video must be **more than reaction**. The Format C close-read body is the differentiation.

## Decisions surfaced

- **Concede-then-deploy structure:** LOCKED — validated by ★★★★★ demand
- **Beat 2 (Zurara) leads in title prominence over Beat 1 (1861 Lagos):** PROVISIONAL — V2#9 evidence suggests audience already half-knows the 1441 angle; foregrounding it serves search-anchor + recognition
- **Pinned comment:** scope-bound Atlantic; address Arab/Trans-Saharan as next video
- **Hasanabi reaction (V1):** NOT a useful comparable — different audience, different signal layer

## Title implications (provisional, scored at title_scorer.py step)

Order the 4 candidates from plan by audience-demand fit:

1. ✅ *Asmongold's Slavery Take Has a Kernel of Truth. Here's What's Missing.* — directly serves the ★★★★★ concede-the-kernel demand
2. ✅ *Asmongold Said Africans Sold Their Own. Here's What the 1453 Chronicle Says.* — directly serves the ★★★★ Beat 2 demand + V2#9 audience recognition of 1441 Portuguese
3. ⚠️ *Asmongold's Slavery Argument Met the 1861 Lagos Treaty* — serves Beat 1 (white space — risk on volume)
4. ❌ *The Documents Destiny Needed Against Asmongold's Slavery Claim* — per plan, avoid unless signal-tracking warrants channel-level repositioning

Title_scorer.py + thumbnail_checker.py will produce the final ranking.

## Pinned-comment draft (for use post-publish)

> Scope note: this video is about the **Atlantic** slave trade — Zurara 1453, the Portuguese 1441 raids, the 1861 Lagos Treaty. The **Arab / Trans-Saharan** slave trade is a separate story with separate documents (and lasted longer); it deserves its own video, which is on the channel pipeline. Comments asking about it are valid; the answer is "different documents, different video."
>
> Primary sources cited:
> - Zurara, *Crónica do Descobrimento e Conquista da Guiné* (1453), Beazley/Prestage trans. (Hakluyt 1896–99)
> - Treaty of Cession of Lagos, 6 August 1861 (British Foreign Office)
> - [scholarly citations with page numbers]
