# DaVinci Studio / Fusion Build Guide — Volhynia #62

**Master:** 1920×1080, 25 fps (match the edit timeline). All times below are real video time (`rough cut.srt` is +01:00:00). No external plugin is required: use Fusion, Edit, Fairlight, PowerPoint/Slides exports, and local PNG/SVG files.

## Global setup and safe areas

1. In Project Settings → Master Settings set 1920×1080, frame rate to the existing timeline, and 48 kHz audio. Deliver H.264/H.265 only after the timeline is locked.
2. Fusion composition coordinates are 0–1. Keep all essential text inside x=120–1800 and y=80–1000 (120 px horizontal / 80 px vertical title-safe). Keep lower thirds above y=900 and subtitles clear of y=930.
3. Use `Noto Sans`/`Arial` for UI and `Libre Baskerville`/`Georgia` for quotations. At 1080p: title 64–76 px, card quote 42–50 px, source line 24–28 px, lower-third name 34 px and role 24 px. Minimum mobile-safe text is 32 px.
4. Import PNG: Media Pool → right-click bin → Import Media. Import SVG through Fusion’s `SVG` node (or rasterize in PowerPoint at 1920×1080 if the SVG parser fails). For a scan, use `MediaIn` → `Transform` → `ColorCorrector` → `Merge` over a background. Never bake translation onto the evidence image itself.
5. Add a `Background` node (near-black #111318 or paper #EEE7D8), then `Merge` all elements over it. Name every node (`DOC_SCAN`, `TRANSLATION`, `SOURCE`, `HIGHLIGHT`, `SAFE_FRAME`).

## Recipe 1 — Document card with active highlight (00:00–00:15; 09:21–09:55)

**Nodes:** `MediaIn(scan)` → `Transform(scan)` → `ColorCorrector(scan)` → `Merge(scan over BG)` → `Polygon(highlight)` → `SoftGlow` (subtle) → `Merge(highlight)` → `Text+` (caption) → `Merge` → `MediaOut`.

1. Place scan at x=.06, y=.07, width=.54, height=.86. Set Transform filter to Mitchell, motion blur off for stills.
2. Add `Polygon` around the exact sentence; fill amber at 0.18 opacity, border 2 px. Animate `Write On` 0→1 over 12 frames, then hold; never highlight a word without its grammatical object.
3. Add Text+ at x=.64, y=.16, width=.30: quote 46 px, line spacing 1.05, left aligned. Source strip at y=.88, 26 px.
4. At 00:00 Klymchak: caption “UPA after-action report, preserved in a Soviet case file, reproduced by historians.” At 09:21 Order No.11 show the whole scan; do not crop `зліквідувати`. Keep “This applies to the Germans as well as the Bolshevik partisans” in the same card.
5. Keyframe Transform Size 1.00→1.08 over 4 s, Ease In/Out. Do not leave an unmoving document on screen longer than 5 s.

## Recipe 2 — Translation split-screen

**Nodes:** scan branch above; `Text+ (editor translation)` → `Background(side panel)` → `Merge(side panel)` → `Text+(translation)` → `Text+(provenance)`.

1. Scan occupies left 56%; right panel x=.61–.95, y=.10–.89, paper white at 0.96 alpha.
2. Heading 30 px uppercase: `EDITOR'S TRANSLATION` (or credit Himka/McBride when published translation). Body 38–42 px; source/folio 24 px.
3. For Order No.11 §2 place the full paired lines: “If possible—liquidate him. This applies to the Germans as well as to the Bolshevik partisans.” For §6 include the self-defence context before “The houses may be burned.” Never isolate either phrase.
4. For Sejm use Polish image plus English marked `EDITOR'S TRANSLATION`; never call it official English. For Stelmashchuk keep `TESTIMONY UNDER SOVIET INTERROGATION` in red 28 px.
5. Animate side panel Position X .03→0 over 14 frames with Ease Out; text opacity 0→1 over 8 frames.

## Recipe 3 — Lower third / source bug

**Nodes:** `Background(rectangle)` → `Text+(name)` → `Text+(role/date)` → `Text+(source ID)` → `Merge`.

1. Safe position x=.06, y=.78; rectangle width=.46, height=.14, color #111318 at 0.90 alpha with a 5 px amber left rule.
2. Name 34 px bold; role/date 24 px; source ID 20 px. Animate X -0.05→.06 over 10 frames, Ease Out; hold 4 s; reverse over 8 frames.
3. Examples: `Yaroslav Stetsko · OUN faction · 1941`; `Gregor Motyka · historian`; `Stelmashchuk · testimony under Soviet interrogation`. Do not write “UPA commander ordered…” unless the cited source says it.

## Recipe 4 — Animated locator map (03:37–04:00; 06:55–07:20)

**Nodes:** `MediaIn(map PNG/SVG)` → `Transform` → `Polygon/Polyline routes` → `Text+ labels` → `Merge` → `MediaOut`.

1. Import a verified base (`map-volhynia-1943-44.png`), crop to x=.04–.96/y=.06–.90. Add title 42 px: `SCHEMATIC ORIENTATION — NOT TO SCALE`.
2. Add dots only for verified locations (Volhynia, Poryck, named villages). Dot radius 8–12 px; labels 30 px with 3 px shadow. Use red for attack locations, blue for boundary/context, white for route.
3. For a wave animation duplicate Polyline nodes: wave 1 opacity 0 at frame 0, 1 at frame 12; wave 2 starts frame 18; wave 3 starts frame 36. Ease Out; hold 2 s. Do not imply simultaneous attacks unless the research card explicitly supports it.
4. For a route, use dashed stroke for intended/uncertain route and solid for documented movement. Never redraw historical borders from memory; label modern overlays.
5. If using SVG, `SVG` → `Transform` → `Merge`; if MapChart export is raster, use `MediaIn` and add labels in Fusion. Google Earth Studio/QGIS are optional, not prerequisites.

## Recipe 5 — Evidence ladder / forensic contrast (09:21–10:55)

**Nodes:** three `MediaIn` scans → three `Transform` nodes → `Merge` stack → `Text+` tier labels → `Rectangle` provenance bar.

1. Build a three-rung vertical ladder: `T1 — signed Order No.11 (anti-German village defence)`; `T2 — scholar-reproduced testimony (duress)`; `UNREACHED — alleged massacre folio`. Each rung is 0.28 height with 24 px source line.
2. Animate rung 1 at 09:21, rung 2 at 10:20, rung 3 at 10:50 with 12-frame fades. Add a red `NOT PRODUCED` stamp only to the missing folio; do not fabricate it.
3. For Stelmashchuk p.442 caption alleged commander as `“Oleh”`, not Klym Savur; `>15,000` applies to the 29–30 Aug operation, not total Volhynia casualties.

## Recipe 6 — Estimate bars and named-dead scale (07:20–08:00)

**Nodes:** `Background` → `Rectangle(Poles)` / `Rectangle(Ukrainians)` → `Text+ labels` → `Text+ Snyder source`.

1. Place bars x=.20–.82, y=.35 and .55. Animate width 0→target over 20 frames, Ease In/Out. Use muted red/blue, not blood red.
2. Text: `about 70,000 Poles` and `perhaps 20,000 Ukrainians`; source line `Snyder, Reconstruction of Nations, p.204 (verbatim)` and narration qualifier `working from Motyka's research`.
3. For the Siemaszko registry, use the actual page PNG as a slow vertical scroll (Transform Y over 8 s) with caption `named entries; not a complete census`. Do not turn Vol.2 source-index pages into a victim chart.

## Recipe 7 — Verdict card and timeline

**Verdict (02:57–03:26 or close):** `Text+` heading `WHAT THE LABEL CHANGES`, three stacked rows: `war = two sides fighting`, `ethnic cleansing = removal`, `genocide = destruction`. Rows appear every 10 frames, Ease Out; 42 px body, 28 px source/definition line. Avoid declaring a legal verdict beyond the script’s cited scholarly positions.

**Timeline (03:37–04:42):** `Background` → horizontal `Rectangle(line)` → `Ellipse` markers → `Text+` date/event. Events: 1918 border settlement; 30 Jun 1941 Act; 1943 killings; 1945–50s Soviet fighting; 2015 law; 2026 decree. Mark approximate dates with `c.`; animate line Scale X 0→1 over 30 frames and markers opacity in sequence. Verify 2026 facts at upload.

## Recipe 8 — Archival still treatment and title/thumbnail exports

1. Still treatment: `MediaIn` → `ColorSpace` (if needed) → `ColorCorrector` saturation -20, contrast +5 → `Transform` scale 1.00→1.05 over 5 s → `FilmGrain` disabled (do not fake age) → `Merge`.
2. Keep seals, margins, page numbers, signatures unchanged. No AI restoration, colorization, invented damage, or unrelated atrocity photo.
3. Title card: 64 px title within x=120–1800/y=180–500; subtitle 34 px. Thumbnail render a separate 1280×720 timeline: real decree/header or portrait + map seam, 2–4 words (`HEROES? MASSACRE?`), no generated bodies, Nazi uniforms, or fake signatures.

## Recipe 9 — Fairlight cue chain

1. VO track: High-pass 70 Hz; compressor threshold -18 dB, ratio 3:1, attack 10 ms, release 100 ms; limiter ceiling -1 dBTP. Use clip gain before compression, not a flat +18 dB boost.
2. Music/drone bus: compressor sidechain from VO, ratio 4:1, threshold -28 dB, attack 5 ms, release 250 ms; automate music -8 to -12 dB under quoted documents and Poryck numbers.
3. Cues: 00:00 silence/low drone; 06:55 near-silence; 09:21 quiet room/paper tone; 12:45 restrained lift after “in the Congo.” No gunfire, screams, or synthetic “archival” ambience.
4. Fairlight loudness meter: target approximately -14 LUFS integrated, true peak ≤ -1 dBTP; render a 30-second test and remeasure before final export.

## Fusion delivery checklist

- [ ] Every Fusion comp is 1920×1080 and inside title-safe bounds.
- [ ] Nodes are named and scans retain source pages/folios.
- [ ] Translation cards say `editor's translation` unless a published scholar translation is credited.
- [ ] `liquidate` and `houses may be burned` retain self-defence context; Litopys p.441 is never labelled a kill order.
- [ ] “Death to Poles” uses RL English + transliteration only; no reconstructed Cyrillic.
- [ ] Missing signed massacre folio is represented as missing, never generated.
- [ ] All stills have motion/highlight within 5 s; all map routes are labelled schematic where uncertain.
