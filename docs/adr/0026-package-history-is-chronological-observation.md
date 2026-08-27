# ADR-0026: Package history is chronological observation

**Status:** Accepted — 2026-08-13

## Context

Analytics interpretation needs to know which title and thumbnail viewers actually encountered. The
existing keyword database records discovery and performance evidence but had no durable pre- and
post-publication package chronology. Project notes and current YouTube state cannot reconstruct a
superseded title or identify the exact thumbnail file after a swap.

## Decision

Add one append-only `package_versions` table to the existing keywords database. Each observation
records the project, optional YouTube ID, package kind, displayed value, effective and recorded times,
and optional reason or experiment identifier. Thumbnail observations also carry the source path and a
SHA-256 content hash. A new row may point to the previous row it supersedes.

The table stores observations, not quality judgments. It has no score, winner flag, policy gate or
generated recommendation. The conversational layer records a selected or changed package and later
joins those dated observations to metrics.

## Consequences

- Pre-publication choices and later swaps become attributable without a new database or platform
  adapter.
- Analytics can distinguish evidence gathered under different packages.
- The creator does not operate the table directly.
- The system still cannot infer exposure boundaries if a package change was not recorded; it must
  state that limitation rather than reconstructing a false chronology.
