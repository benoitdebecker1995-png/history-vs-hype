# ADR-0025: Read-only SQLite access tolerates lockless workspace drives

**Status:** Accepted
**Date:** 2026-08-10

## Context

The three live databases were readable as ordinary files on the current Windows workspace drive,
but every normal SQLite open failed with `OperationalError: unable to open database file` because
the mounted drive rejected SQLite's lock handle. A copied control opened normally, and the original
databases opened with SQLite's immutable read-only mode. This broke collision checks and silently
removed competitor, own-channel, and demand evidence from packaging.

Several readers independently constructed SQLite paths and URIs. Fixing each spelling would leave
the locking failure and allow the implementations to drift again. No existing cross-store surface
owned this narrow responsibility; the three store seams continue to own queries and writes.

## Decision

`tools.sqlite_access.connect_readonly()` owns read-only connection setup. It:

1. builds an encoded URI from `Path.as_uri()`;
2. attempts normal `mode=ro` first with a short read-only probe timeout and forces a schema read
   because Python may defer the physical file open until the first statement;
3. retries with `immutable=1` only for "unable to open database file" and only when no non-empty
   `-wal` or `-journal` sidecar exists; and
4. enables `PRAGMA query_only` on every returned connection.

Writers must not use this helper. They remain behind their owning store and normal transaction and
locking behavior.

## Consequences

Read-only checks work on ordinary filesystems and lockless workspace mounts without copying live
databases or weakening writes. A database with an active WAL/journal fails visibly instead of
returning a stale immutable view.
