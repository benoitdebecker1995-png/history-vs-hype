# SRT Fix Log — finished cut.srt

**Date:** 2026-06-04
**Run by:** /fix skill (one-shot Python fixer, cross-referenced against SCRIPT.md v5)

## Fixes applied

### Names / proper nouns
- `Pirioureis → Piri Reis` × 5
- `P.D. Reyes → Piri Reis` × 3
- `P.D. Reyes' → Piri Reis's` × 1
- `Piri Reis' other → Piri Reis's other` × 1
- `Mäkingdös → McIntosh` × 1
- `Macintosh → McIntosh` × 1
- `Svaat Süzegh → Svat Soucek` × 1
- `Süzegh → Soucek` × 2
- `Paul Kalle → Paul Kahle` × 1
- `Paul Calle → Paul Kahle` × 1
- `Claudius Petolomeis Atlas → Claudius Ptolemy's atlas` × 1
- `Claudius Petolomeis → Claudius Ptolemy` × 1
- `two famous Petolomeis → two famous Ptolemys` × 1
- `Petolomei I → Ptolemy the First` × 2
- `Petolomeis → Ptolemy` × 1
- `Hankook → Hancock` × 1
- `Hanka calls → Hancock calls` × 1
- `Henco can → Hancock and` × 1
- `Tokapi Palace → Topkapı Palace` × 1
- `Calanea → Cananéia` × 1

### Foreign terms
- `cafegares → cağferiyes` × 1
- `Cafiria → Cağferiye` × 2
- `Giafaria → Cağferiye` × 1
- `Kafirgia → cağferiye` × 1
- `Kafirias → cağferiyes` × 1
- `Tughrafia → jughrafiya` × 3
- `Mapamundi → mappaemundi` × 1
- `Porta Gande → Porta Ghande` × 1
- `Kao Punta Orafai → Kaw Punta Orofay` × 1

### Wrong words (homophones / mishears — confirmed against script, meaning-critical)
- `his stone cut out → his tongue cut out` × 1
- `that ghost himself → that coast himself` × 1
- `The first skull to make sense → The first scholar to make sense` × 1
- `kept talk with → kept up with` × 1
- `surviving charge → surviving chart` × 1
- `Proof of its seafaring → Proof of a seafaring` × 1
- `came of a Spanish → came off a Spanish` × 1
- `stone blocks of the Bahamas → stone blocks off the Bahamas` × 1
- `The Portuguese name's → The Portuguese names` × 1
- `a strange map, used mutilated remains → a strange map whose mutilated remains` × 1
- `have good readers Antarctica → Hapgood read as Antarctica` × 1
- `Excription → inscription` × 1
- `in description 6 → inscription 6` × 1

### Timestamps
- `Timestamp hour offset (01:XX → 00:XX)` × 293

## Validation

All 293 timestamps pass (end > start). Track runs 00:00:00,099 → 00:10:27,066.

## Notes

- Finished cut diverged from SCRIPT.md v5 by design (cold-open Hancock clip inserted, closer reordered, execution line softened, "Kahle got plenty wrong" cut). Cross-reference fixed transcription only — delivered ad-libs/reorderings left as spoken. Per /fix rule: never changed the actual words spoken.
- Foreign-term *spellings* (cağferiye, jughrafiya, Topkapı, Cananéia) use SCRIPT.md canonical forms since audio wasn't available to confirm pronunciation. `ğ`/`ı`/`é` are UTF-8 — render fine on YouTube.
- Generalizable fixes worth adding to the auto-fixer's recurring set: `stone↔tongue`, `skull↔scholar`, `charge↔chart`, `came of↔came off`, `blocks of↔blocks off`. The rest are #57-specific proper nouns.
- Backup of pre-fix SRT: `finished cut.srt.pre-fix` (delete after upload confirmed).
