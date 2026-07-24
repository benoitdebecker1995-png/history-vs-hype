# StatusDoc: one owner for the AUTO-zone fence grammar

**Date:** 2026-07-01
**Status:** accepted

Peer to ADR-0008/0009/0010/0011 (the seam ADRs). This ADR exists because the
fenced-block surgery on `PROJECT-STATUS.md` was implemented **three times**
(`reconcile.write_auto_block`, `reconcile.write_root_status`,
`packaging_lock.write_lock_block`) and `packaging_lock.py` **hardcoded
reconcile's private close marker** (`RECON_CLOSE = '<!-- /AUTO:reconcile -->'`)
to position its own zone — the clearest cross-seam leak found by the
2026-07-01 `/improve-codebase-architecture` pass. ADR-0008 had already named a
typed status reader as a candidate ("`.status` / `.research` await their own
typed readers"); this builds the status half.

## What the seam is

`tools/video_projects/status_doc.py` — stdlib only, no imports from
reconcile/preflight (so both can import it without cycles).

- **`AutoZone`** — one named fence (`<!-- AUTO:<name> <note> -->` …
  `<!-- /AUTO:<name> -->`) with its placement policy and the single surgery
  implementation (`read`, `fields`, `wrap`, `write`). Three registered zones:
  - `RECONCILE_ZONE` — *claims the top* of a per-project PROJECT-STATUS.md: a
    rewrite replaces everything above its close marker (hand-written narrative
    lives below). This preserves reconcile's historical contract.
  - `PACKAGING_LOCK_ZONE` — replaced in place; when absent, inserted just
    below the reconcile zone; else prepended. The "sits below reconcile" rule
    is now zone metadata (`insert_after`), not a foreign marker string.
  - `RECONCILE_DASHBOARD_ZONE` — the root `video-projects/PROJECT_STATUS.md`
    variant (claims the top there).
- **`StatusDoc`** — the typed per-project reader/writer: `load` (missing or
  unreadable file → empty doc), `zone` / `zone_fields` / `write_zone` /
  `save` (returns previous content — the backup contract the old writers had),
  plus the shared field reads `working_title` and `status_label` (the fuzzy
  `Status:` head-of-doc read both discovery scanners had duplicated).
- **`VideoProject.status`** now composes `StatusDoc` lazily (same pattern as
  `.script` / `.post_publish`). `.research` still awaits its reader.

## Division of labor — zone bodies stay with their owners

StatusDoc owns **where zones sit and how they're replaced**; the zone owners
keep **rendering their own body lines and parsing their own semantics**.
`reconcile.render_auto_block` / `render_root_status_block` and
`packaging_lock.render_lock_block` now return marker-less bodies;
`packaging_lock._parse_block` still applies its FILTERS regexes, but to
`doc.zone(PACKAGING_LOCK_ZONE)` instead of hand-sliced text. Merging the body
semantics into StatusDoc was rejected — it would couple the seam to every
zone's schema and reintroduce the god-module shape the fence split avoids.

## Migration — verified byte-identical

All surgery and read paths were snapshotted before the refactor and compared
after, on copies of real files (#62 with both zones, #58 reconcile-only, a
synthetic no-zone doc, a missing file, and the root dashboard): 14/14 outputs
byte-identical, `packaging_lock --validate` on #62 still returns VALID.
Migrated in this pass:

- `reconcile.py` — `read_auto_block` / `write_auto_block` / `write_root_status`
  delegate; the four marker constants deleted (markers live once now).
- `packaging_lock.py` — `resolve_title` / `write_lock_block` / `_parse_block`
  delegate; `PL_OPEN` / `PL_CLOSE` / `RECON_CLOSE` deleted. One deliberate
  tightening: `resolve_title` now reads the title line *inside the lock zone
  only* (the old code scanned from the open marker to end-of-file, so a stray
  `title:` line in the narrative could have masqueraded as the lock title).
- `news_hook_monitor.py` / `news_scanner.py` — the duplicated fuzzy status
  regex → `status_label` (news_scanner gained the standard entry-point
  `sys.path` bootstrap; it was stdlib-only before).

**Known quirks preserved, deliberately:** `working_title` keeps the `**`
prefix on bold-style lines (the historical packaging_lock regex behavior;
pinned by a test comment), and `status_label` still truncates at the first
non-`[A-Z ]` character ("FACT-CHECK" reads as "FACT") — both scanners always
did this and agree with each other; fix at the seam if it ever bites.

## Considered alternatives

- **A neutral top-level `tools/auto_zone.py`** (grammar separate from the
  status reader). Rejected — one concept home; the root-dashboard doc uses
  `AutoZone` directly and that's fine from the same module.
- **Prefix-based marker detection** (match `<!-- AUTO:name` regardless of
  note text). Rejected for now — exact-string matching is what every existing
  file round-trips against; loosening it is a behavior change with no
  motivating defect.
- **Migrating `prompt_generator`'s `## Concept` read and the video-ID scans**
  (`match.extract_video_id_from_folder`, `backfill_high_impact.
  find_video_id_for_project`). Deferred — the ID scans read *three* files, not
  the status doc; the Concept read is bespoke to one consumer. Widen
  `StatusDoc` only when a second consumer needs the field (ADR-0005 precedent).

## Consequences

- **Test surface.** `tests/test_status_doc.py` (18 tests) — the fence surgery
  had zero direct tests in any of its three copies; reconcile's AUTO-block
  writes and packaging_lock's zone writes are now pinned through the seam.
- **Leverage.** One fence implementation, N zones: the next managed zone is a
  registry entry, not a fourth copy of the surgery.
- **Re-litigation guard.** Future `/improve-codebase-architecture` runs that
  surface "duplicate PROJECT-STATUS parsers" should be answered with this ADR,
  including the deliberately-deferred readers above. Supersede rather than
  re-fork.
