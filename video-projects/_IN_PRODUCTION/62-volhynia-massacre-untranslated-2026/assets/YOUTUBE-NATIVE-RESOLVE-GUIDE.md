# YouTube-Native Resolve/Fusion Treatment — Volhynia #62

This is the visual treatment layer for the existing evidence pack. The rule is **footage first, source second, text last**: keep the host, landscape, archive texture, or moving map underneath; bring documents in as brief, animated interventions. Avoid PowerPoint-style full-screen slides except for the title and final verdict.

## Evidence basis and limits

This treatment is **not presented as a proven History vs Hype house style**. It is a practical synthesis from sampled public storyboards of three relevant YouTube benchmarks: *A Brief History of Ukraine* (3.78M views: continuous kinetic maps, location footage, minimal text), *Borderlands: The Animated History of Ukraine* (1.71M: cohesive custom animation, but unrealistic for a solo weekly workflow), and a recent Volhynia documentary (153K: archive/landscape footage, tight source crops, maps and occasional single-word red text). The tactics are observational, not causal proof of retention. The safe conclusion is narrower: do not stop the video for a designed information slide when the same point can be carried by you, a moving map or the evidence itself.

**Master:** 1920×1080, match timeline fps, 48 kHz. Title-safe: x=120–1800, y=80–1000. Use 42–50 px body text, 24–28 px source labels, and one restrained red accent (#C53B32). No external plugin is needed.

## Visual grammar

- **Host punch-in:** 100%→108% over 14 frames, Ease In/Out, then return over 10 frames; use at a turn point, not every sentence.
- **Source intervention:** 1.5–4 s over the moving shot, with a 3–6% push, one tracked highlight, and a source bug. Never leave a static page untouched for more than 5 s.
- **Transitions:** 6-frame dip-to-black for a chapter break; 8-frame whip-pan only between maps/locations; 4-frame paper-wipe from a real page edge. No glitch, explosion, blood, or “war” stock transition.
- **Text:** one red word or short phrase at a time (`GENOCIDE?`, `ORAL DIRECTIVE`, `NOT PRODUCED`), never a paragraph over footage.

## Recipe A — Document push-in with tracked highlight

**Use:** 00:00 Klymchak; 04:42 Act of Restoration; 09:21 Order No.11; 10:20 Litopys/McBride.

Fusion nodes: `MediaIn(page)` → `ColorCorrector` → `Transform(push)` → `PlanarTracker` (page corner/line) → `Polygon(mask)` → `SoftGlow` (0.15) → `Merge(highlight)` → `Text+ source bug` → `Merge over footage` → `MediaOut`.

1. Start with host/landscape or the complete page full frame. Establish the whole page for 1–2 s, then match-push into the relevant clause. Avoid a floating presentation window; the archive page is the scene.
2. Transform page Size 1.00→1.10 over 3.2 s; center on the sentence that matters. Ease In/Out; add 0.15 motion blur.
3. Track a 4-point Polygon around the sentence with PlanarTracker. Attach the Polygon to the tracker; animate fill opacity 0→0.22 over 8 frames, hold, then fade.
4. Source bug: 24 px at bottom-left, `McBride p.648 · reproduced primary` or exact ledger wording. Keep it on screen while the highlight is visible.
5. For Order No.11, the tracked region must include “This applies to the Germans as well as the Bolshevik partisans.” Never isolate `зліквідувати`; keep its object in the same frame.

## Recipe B — Translation split-screen without a card wall

**Use:** 09:21 Order No.11; 10:20 Stelmashchuk; Sejm clause.

1. Keep a blurred, darkened version of the host/landscape underneath (`Gaussian Blur` 12, opacity 35%). Place the source page at left x=.05–.52 and a translucent right panel x=.58–.95, opacity 0.90.
2. Use `Text+` heading 30 px `EDITOR'S TRANSLATION`; body 38 px, maximum four lines. Animate panel X .04→0 over 12 frames and text opacity 0→1 over 6.
3. Order No.11 text must read: “If possible—liquidate him. This applies to the Germans as well as the Bolshevik partisans.” For §6, include the self-defence context before “The houses may be burned.”
4. Keep the records separate. The 1963 Stelmashchuk copy says “Klym Savur” conveyed an oral secret directive. The different Litopys p.442 interrogation record attributes its alleged operation to “Oleh.” Both carry a persistent `TESTIMONY UNDER SOVIET INTERROGATION` label.
5. Sejm English is `EDITOR'S TRANSLATION`, not official English. Polish original remains visible.

## Recipe C — Parallax archival photo

**Use:** Bandera/Sachsenhausen ~01:52, Dontsov ~04:05, reconciliation/exhumation close.

1. `MediaIn(photo)` → `Polygon` foreground subject → `Transform(fg)`; duplicate photo for background → `Transform(bg)` → `Blur` 8 → `Merge`.
2. Background Scale 1.00→1.05; foreground 1.02→1.11 over 4 s, opposite X drift (±18 px). Ease In/Out. Add a subtle paper grain only if it is an actual scan texture; never manufacture aging.
3. Lower third appears after 8 frames: `Yaroslav Stetsko · 1941` or `Bandera · held in Sachsenhausen throughout the 1943 massacres`. Keep the fairness caption verbatim and legible.
4. Historical photos remain neutral/grayscale. Do not colorize, AI-reconstruct faces, or pair an unrelated atrocity photo as if it depicts Volhynia.

## Recipe D — Kinetic map movement

**Use:** orientation 03:37–04:00; Poryck 06:55–07:20; reconciliation route.

1. `MediaIn(map PNG/SVG)` → `Transform` → `Polyline` route → `Text+ labels` → `Merge` over host/terrain footage. Put a 30 px `SCHEMATIC / NOT TO SCALE` label in the corner.
2. Begin wide (Scale .90), then move to the verified location (Scale 1.12, Position X/Y over 36 frames). Add 8 px red dots and 30 px labels. Use solid stroke only for documented movement; dashed for intended/uncertain routes.
3. For multiple villages, stagger dot opacity at frames 0, 12, 24, 36. Keep the map moving under narration; no full-screen still-map pause.
4. Do not invent borders or synchronized attacks. If geography is approximate, say so on screen. QGIS/MapChart/Earth Studio are optional; Fusion can animate a supplied PNG.

## Recipe E — Host punch-ins and evidence handoffs

1. On the Edit page, cut host at a clause turn. Add Dynamic Zoom or Fusion Transform 100%→108% over 14 frames. Ease In/Out; no artificial camera shake.
2. At “It reads,” cut from host to the Klymchak page for roughly 4–6 s: whole page → matching quote detail → back to host. At “the documents actually support,” use a restrained push toward the source ledger.
3. At “the disagreement is what kind of campaign,” punch in 5% and bring one red keyword (`WAR`, `CLEANSING`, `GENOCIDE`) beside the host for ≤1.2 s each.

## Recipe F — Missing-document / verdict treatment

**Use:** 10:50–11:10 and the close. Keep the absence visible without fabricating a page.

1. Over a moving archive/desk shot, place an empty file frame (not a fake scan). `Text+` types in `HDA SBU spr.11315 — not directly reviewed` at 36 px; cursor blink 2 cycles.
2. Add a red stamp `NOT PRODUCED` (44 px, 18° rotation, opacity 0.85) with a 6-frame impact and no sound hit. Source strip stays visible.
3. Verdict is a host punch-in plus three short red words appearing on beats: `COORDINATION`, `INTENT`, `CHAIN OF COMMAND?` The question mark is intentional; do not present an unsupported legal conclusion.

## Audio and texture handoff

Keep room tone under every source intervention. Lower music 8–12 dB under documents and Poryck numbers; near-silence 00:00–00:14 and 06:55–07:20. Fairlight: VO high-pass 70 Hz, compressor 3:1 at -18 dB threshold, limiter -1 dBTP; target approximately -14 LUFS integrated. Never synthesize screams, gunfire, or “archival” battlefield sound.

## Sensitive-material stop flags

- Never generate or stage massacre photographs, bodies, uniforms, signatures, or an “authenticated” kill order.
- Keep `liquidate` paired with Germans/Bolshevik partisans; keep “houses may be burned” paired with village self-defence context.
- Litopys p.441 is organizational structure, not a kill order; p.442 is “Oleh” testimony under Soviet interrogation and >15,000 applies to that operation only.
- “Death to Poles” uses Rossoliński-Liebe’s English + transliteration only; do not reconstruct Cyrillic or conflate *poliakam* with *liakham*.
- Any editor’s translation is labelled as such; published English credits Himka/McBride where applicable.

## Solo pass order

1. Cut host punch-ins and footage-first transitions.
2. Add moving maps and parallax stills.
3. Add document pushes/highlights only at the exact evidence words.
4. Add translation panels, source bugs, and three-word verdict beats.
5. Run safety/source QC, then Fairlight loudness pass and mobile legibility check.
