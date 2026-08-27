# Volhynia Resolve asset pack

> **Superseded for visual style on 2026-08-10.** The numbered full-screen cards below were rejected as too presentation-like. Use the footage-first replacements in [`youtube-native/README.md`](youtube-native/README.md) and the motion clips in that folder. The older cards remain only as text/provenance references and should not define the final edit.

Built 2026-08-10 for the **13:11 current cut**. All cue times are relative to the start of that cut, not the 22:14 camera original. PNG exports are 3840×2160 unless noted; editable SVG masters sit beside them.

## Drop into Resolve first

| File | Suggested time | Use | Evidence status |
|---|---:|---|---|
| `14-klymchak-report-card.png` | 00:00–00:14 and 08:50–09:21 | Evidence-first cold open; later callback | Published reproduction of a reported UPA document; underlying HDA SBU folio was unavailable to McBride. Do not label this a signed original. |
| `01-historiography-card.png` | 00:46–01:10 | Keep massacre / ethnic cleansing / genocide labels attributed rather than presented as interchangeable facts | Interpretation card; not evidence by itself. |
| `09-first-90-document-sequence.png` | 00:14–00:46 | Timing/layout guide for the decree and Polish response | Two grey panels are placeholders, not facsimiles. Replace with real browser captures from the official pages. |
| `10-volhynia-1939-locator.png` | 03:31–04:04 | Geographic orientation | Base map by Poeticbent, 2009, public domain; derived from Siemaszko data. Treat borders/locations as orientation, not a complete attack map. |
| `16-kolodzinskyi-card.png` | 04:04–04:42 | Prewar doctrine passage | Published manuscript reproduction and Himka English translation. Label as doctrine, not a 1943 operational order. |
| `02-snyder-estimates.png` | 05:55–06:30 or 07:30–08:00 | Polish/Ukrainian victim-estimate comparison | Secondary scholarly estimates. Keep “estimates” and Snyder attribution visible. |
| `11-poryck-location-diagram.png` | 06:50–07:15 | Poryck locator during 11 July discussion | Poryck coordinate from Wikidata. One verified location only; not every attack on that date. |
| `03-evidence-ladder.png` | 09:45–10:20 | Explain the gap between signed record, testimony and missing written order | Editorial synthesis; every rung must remain labelled. |
| `15-order11-card.png` | 09:21–09:55 | Whole-page Order No.11 forensic contrast | Primary document reproduction. “Liquidate” applies to Germans and Bolshevik partisans. Keep the grammatical object visible. |
| `17-stelmashchuk-card.png` | 10:20–10:40 | 1963 archival-copy testimony | Separate record claiming an oral secret directive from Klym Savur. Soviet-interrogation, copy-status and authenticity cautions stay on screen. |
| `18-litopys-p442-card.png` | 09:55–10:20 | Distinguish the published interrogation record from the 1963 copy | Litopys p.442 attributes the alleged operation to “Oleh,” not Klym Savur. Duress/reliability warning is mandatory. |
| `04-verdict-card.png` | 11:10–11:31 or conclusion | Summarize what the records prove and do not prove | Editorial conclusion; do not imply a missing written order was found. |
| `05-master-timeline.png` | Use in sections, not as one long hold | 1938 doctrine → 1941 collaboration → 1943 violence → later testimony | Context graphic. Check every date against the locked narration before final export. |
| `13-title-card.png` | Optional 00:00 or chapter break | Series/episode title | Original channel graphic. |
| `12-thumbnail-dossier.png` | Promotion only | Editable thumbnail starting point | Uses Order No.11 scan as evidence texture; do not imply it is a Polish-civilian kill order. |

## Templates to customize in Fusion

| File | Purpose |
|---|---|
| `06-document-card-template.svg/.png` | Source-document card with title, date, provenance and one highlighted clause. |
| `07-translation-split-template.svg/.png` | Original-language passage beside checked English. Keep clause boundaries aligned. |
| `08-lower-thirds.svg/.png` | Institution, scholar and provenance lower-thirds. |

The exact Fusion node recipes, safe areas, type sizes, easing and Fairlight treatment are in `DAVINCI-FUSION-BUILD-GUIDE.md`.

## Still required

1. Capture the rendered official **Ukrainian Decree 440/2026** page in a browser, with institution, decree number and date visible. Do not recreate it.
2. Capture the rendered official **Polish presidential revocation statement** page, with headline and date visible. Do not recreate it.
3. Replace the two grey placeholders in `09-first-90-document-sequence` with those captures.
4. Conform all cues to the next Resolve SRT/export. The current SRT starts at `01:00:00.366`; `VOLHYNIA-ASSET-TIMING.csv` subtracts one hour.
5. Remove the known silent/dead interval around 03:29.40–03:31.83 if it survives the Resolve timeline.

## Tools and plugins

- **Required:** DaVinci Resolve Studio only. Fusion can build every animation; Fairlight can do the sound pass. No paid plugin is required.
- **Required external workflow:** a normal browser for the two official-page captures above.
- **Optional:** Canva only for rapid thumbnail variants or social crops. It is not needed for the documentary edit and should not be used to reconstruct historical documents.
- **Not suitable here:** image generation for photographs, documents, eyewitness scenes, maps presented as historical evidence, or massacre imagery.

## Key files

- `VOLHYNIA-ASSET-TIMING.csv` — 24 cue rows for the 13:11 cut.
- `TIMING-NOTES.md` — conform notes and known subtitle gap.
- `SOURCE-MANIFEST.md` — URLs, rights, provenance and unresolved access issues.
- `DAVINCI-FUSION-BUILD-GUIDE.md` — build instructions for motion, lower-thirds and sound.
- `render-assets.cjs` / `render-composites.cjs` — reproducible export scripts for later corrections.

## Ethical lock

Use documents, maps, restrained atmosphere and host presence. Do not use corpse imagery, reenacted killings, AI “archive” photography, decorative Nazi footage or unverified social-media images. A testimony card is testimony; an estimate card is an estimate; a scholarly interpretation card is interpretation.
