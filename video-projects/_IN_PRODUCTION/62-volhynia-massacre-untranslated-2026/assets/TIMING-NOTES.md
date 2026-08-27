# Volhynia Resolve timing notes

**Authority:** `rough cut.srt`, normalized by subtracting its 01:00:00 offset. Runtime preserved: **13:11.566**. Cue sheet: `VOLHYNIA-ASSET-TIMING.csv`.

## Conform notes

- The supplied SRT has 399 subtitle cues and starts at 01:00:00.366. In Resolve, use timeline-relative 00:00:00.366 (or retain the one-hour timeline offset consistently); do not mix bases.
- Cue boundaries are editorial ranges from `06-SOURCED-EDITING-AND-BROLL-PLAN.md`, not frame-accurate shot trims. Check against the next DaVinci export before picture lock.
- First-90 priority is V01–V07. The visual chain is report → Ukrainian decree → Polish revocation → attributed reaction → taxonomy → thesis → Crimea/UPA bridge.
- Priority 08:50–11:31 is V19–V24: directive callback → full Order No.11 → confession copy → 1963 copy → June 1943 letter → unavailable-original stop.
- V11 contains the known ~2.43 s spoken/subtitle gap at 03:29.40–03:31.83 (absolute SRT 01:03:29.40–01:03:31.83). Remove or bridge with the estimate card; do not leave a dead visual hold.
- All estimate cards must retain qualifiers: “50–60k,” “around,” “about 36,000 names,” and “Snyder’s synthesis.” Do not animate false precision.
- V20 must show the complete grammatical object on Order No.11. Never crop the scan to imply the “liquidate” verb targets Polish civilians.
- V21/V22/V23 require permanent evidence-status labels. The confession is testimony under Soviet interrogation; the letter reports an oral order and is not the order itself.
- Recommended transitions are defaults only: hard cuts for factual turns, restrained dissolves for archival page changes, and no sensational impact SFX.
- Track convention: V0 = host/talking head, V1 = primary/document/map visual, V2 = attributed reaction/context card. If Resolve uses different track numbering, preserve the host-over-visual relationship.
- Timecode ambiguity: SRT uses an artificial one-hour start; asset sheet uses relative 00:00. The original camera MP4 is 22:14, but this cue sheet intentionally preserves the 13:11 edited sequence and must not be stretched to the camera-original duration.

