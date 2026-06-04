# Thumbnail Replacement Concepts — SERP-Grounded

**Generated:** 2026-06-03
**Method:** Live YouTube SERP scan (scrapetube, quota-free) → downloaded top-8 ranking thumbnails per topic → visual shelf analysis → concepts designed to break the dominant pattern. NOT the static NotebookLM corpus.
**Targets:** 5 published underperformers diagnosed "SWAP TITLE + THUMBNAIL" by `/retitle --audit`.
**Next step per video:** render → `python -m tools.preflight.thumbnail_image_audit <thumb> --serp-ids <ids>` to confirm CLIP cosine < 0.55 (strong pattern-break) before swapping.

HvH rules applied: text overlay mandatory (2–4 words) · NO face (face-saturated shelves make no-face the break) · maps for territorial · declarative not question (shelves are question-heavy) · real materials, no AI.

---

## 1. Dark Ages Myth — `-QG8trhNsoM`
**SERP shelf:** big yellow/white block-caps on dark medieval imagery; knights, Colosseum, castles; **question framing dominates** ("HOW 'DARK' WERE THE DARK AGES?", "THE MIDDLE AGES NEVER HAPPENED?"). Everyone shows a medieval *figure*. Nobody shows *data*.
**Gap:** the quantitative proof (manuscript counts) — no competitor visualizes it.

- **TOP — VISUAL ANSWER (data-as-image).** A rising stack / climbing line of manuscripts, with a struck-through "DARK AGES" label. Overlay: **"THE DATA SAYS NO"** (3 words). Breaks the shelf two ways: declarative (not a question) and data (not a knight).
- **ALT — MECHANISM REFRAME.** Single bold count slammed on screen — e.g. **"+700% BOOKS"** beside a crossed-out torch/"darkness" motif. Operation = COMPRESSION. Differentiates from the yellow-text-on-knight pattern by leading with a number nobody else shows.
- Avoid: castles, monks-writing, any "?", the yellow-caps look (you'd blend straight into Captivating History / PragerU).

## 2. Tariff Myth — `JkH4XIHfnJU`
**SERP shelf:** **Trump face on 4+ of the top 8**, plus container ships, bananas, "TRADE WAR"/"TARIFFS" block text, red. The shelf is a Trump-and-ships monoculture.
**Gap:** nobody shows *who actually pays* — the wallet/receipt and the 200-year repetition.

- **TOP — MECHANISM REFRAME (no face = the break).** A worn historical receipt/price tag with a red **"YOU PAID THIS"** stamp (3 words). Zero Trump, zero ship. On a Trump-saturated shelf, the absence of his face IS the pattern interrupt, and it reframes tariff from politics → your wallet.
- **ALT — VISUAL ANSWER.** A 200-year price line spiking, arrow bending down into an open wallet. Overlay: **"THE BILL ALWAYS LANDS HERE"** (compress to **"WHO PAYS"** if cramped). Historical-pattern angle the news clips can't claim.
- Avoid: Trump, container ships, the literal word "TARIFFS" as the hero (that was the prior anti-pattern — TITLE REPETITION on an abstract).

## 3. Stalin Purged His Army — `Yx5oywZs-rk`
**SERP shelf:** sepia/B&W Stalin portraits, red-flag military rows, red "THE GREAT PURGE" / "RED ARMY" caps. **TIKhistory already owns the exact angle** (purge → WW2 east front). Pattern = Stalin face + red text + crowd.
**Gap:** the *self-inflicted* cause→effect shown in one frame — none do it.

- **TOP — VISUAL ANSWER (cause+effect single frame).** Red X-marks striking out a row of *his own* officer portraits, a Nazi advance-arrow pushing in from the right. Overlay: **"HE DID IT TO HIMSELF"** (compress: **"SELF-INFLICTED"**). No hero Stalin portrait — that's how you avoid blending into the 6 portrait thumbnails.
- **ALT — MECHANISM REFRAME.** Empty/redacted officer photos (rows of blanked faces) with overlay **"30,000 OFFICERS. GONE."** Operation = COMPRESSION. The scale number differentiates from the mood-portrait shelf.
- Avoid: a centered Stalin portrait, the word "PURGE" as hero in red caps (instant TIK/House-of-History blend).

## 4. South China Sea — `LrthC_8Hb2Y`  *(highest retention, 50.5% — best swap ROI)*
**SERP shelf:** maps + nine-dash line everywhere, red China shapes, **Xi face, warships, Johnny Harris face**, "THIS SEA IS MINE". The map IS the topic convention — can't ignore it.
**Gap:** the **2016 court ruling** — none of the top 8 show the legal "NO." That's your auditor's-edge.

- **TOP — VISUAL ANSWER (strategic-copy the map, add the verdict).** Keep the nine-dash map (topic convention) but stamp a red **"REJECTED"** / **"A COURT SAID NO"** across the dashes. You copy the one element you must (map) and differentiate on the single thing no competitor has (the ruling). Strongest concept in the batch.
- **ALT — LOCATION PROOF + document.** Split: nine-dash claim line vs the PCA tribunal ruling page, overlay **"NO LEGAL BASIS"** (the tribunal's own phrase). Document-on-map = HvH house style, absent from the shelf.
- Avoid: a face (Xi/host), a warship hero shot, "THIS SEA IS MINE"-type taunt text — all already taken.

## 5. Gibraltar — `WZnCxVPNF7A`
**SERP shelf:** Iberia maps with Gibraltar highlighted, UK + Spain flag pairs, Union Jack, **question framing** ("WHY DOES BRITAIN OWN GIBRALTAR?"), the Rock photo, Brexit framing. (HvH's own "CHAGOS 2.0?" is on this shelf.)
**Gap:** the **1713 Article X clause** — the document that actually traps them. No competitor foregrounds the text.

- **TOP — VISUAL ANSWER (document-on-map).** Treaty of Utrecht Article X text, **one clause circled in red**, over a faint UK/Spain Gibraltar map. Overlay: **"ONE CLAUSE TRAPS THEM"** (compress: **"THE TRAP CLAUSE"**). Declarative; foregrounds the document the whole shelf omits.
- **ALT — MECHANISM REFRAME.** A red reversionary-arrow: Gibraltar → (locked) → Spain, *not* → independence. Overlay **"THEY CAN'T CHOOSE"**. Shows the legal mechanism, not just the rock.
- Avoid: flag-pair + map + "?" (you'd vanish into History Matters / TLDR / Politics with Paint), and the Rock-from-the-sea photo.

---

### SERP IDs for post-render differentiation audit
- dark-ages: `g5NG6mo1zGY,d0Fbcc8uWEc,e9-l34TcV_U,LV801eQzUQ0,gnTMu4Ba17o,Cqzq01i2O3U,L2hi5Vh8Ig0,u3SS-KVdvYw`
- tariff: `_-eHOSq3oqI,xwZT_nisxsQ,VmClr-GkH7E,K0V8kZyl1T0,ErwIlvQ_RVk,lRV6U82vgjI,Iwa3vLoeNmQ,LKCMnCZyxiQ`
- stalin: `mcfn1eJPzEw,vcscm7TfuWo,EDOIzK8NuoU,IYFZawos3v0,s29Q9EIbDT8,jil4OCsxT_U,1dQBIqf8vEc,JnWNnI6YlQQ`
- south-china-sea: `luTPMHC7zHY,z9IiZkMKi68,f00V9MQBhg8,-2v6EJE3XKo,GGMTjsB5SVs,5jUMR_N0mNM,MoRgK9OcfBU,8eqtl0ym1p8`
- gibraltar: `LMTJW_eEYDs,zvyWCP2x1GU,y4ztC1BuDgI,7TDQFike-jg,q-UXpntPT1k,OAfSrE52eKg,ckAxBCKQF-M,ESuOaLSmi8M`
