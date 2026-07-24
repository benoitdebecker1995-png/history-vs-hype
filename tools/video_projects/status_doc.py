"""StatusDoc — the one owner of the AUTO-zone fence grammar and the shared
PROJECT-STATUS.md field reads.

Before this module, three copies of the same fenced-block surgery lived in
`reconcile.write_auto_block`, `reconcile.write_root_status`, and
`packaging_lock.write_lock_block` — and packaging_lock hardcoded reconcile's
private close marker to position its own zone. Now the fence grammar, the
zone placement rules, and the replace surgery live once, here; the zone
OWNERS keep rendering their own body lines and parsing their own semantics.

Grammar:  '<!-- AUTO:<name> <note> -->' ... '<!-- /AUTO:<name> -->'

Placement rules (canonical order, top of file downward):
  reconcile            — claims the top of the file: a rewrite replaces
                         everything above its close marker; hand-written
                         narrative lives BELOW the zone.
  packaging-lock       — replaced in place if present, else inserted just
                         below the reconcile zone, else prepended.
  reconcile-dashboard  — the root video-projects/PROJECT_STATUS.md variant
                         of the reconcile zone (claims the top there).

See ADR-0014.
"""
from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path
from typing import Dict, Optional


class StatusDocError(Exception):
    """Raised when a StatusDoc write would clobber an existing file that could
    not be read/decoded — fail closed instead of overwriting it with an empty
    or partial AUTO block."""


class AutoZone:
    """One named AUTO fence: markers, read, and the single write surgery."""

    def __init__(self, name: str, note: str, *,
                 claims_top: bool = False,
                 insert_after: Optional["AutoZone"] = None) -> None:
        self.name = name
        self.open_marker = f'<!-- AUTO:{name} {note} -->'
        self.close_marker = f'<!-- /AUTO:{name} -->'
        #: On rewrite, discard anything above the zone (it owns the file top).
        self.claims_top = claims_top
        #: When absent, insert just below this zone's close marker (if present).
        self.insert_after = insert_after

    # --- read ----------------------------------------------------------------

    def read(self, text: str) -> Optional[str]:
        """Inner text of the zone, or None if the zone is absent."""
        if self.open_marker not in text or self.close_marker not in text:
            return None
        start = text.index(self.open_marker) + len(self.open_marker)
        return text[start:text.index(self.close_marker)]

    def fields(self, text: str) -> Optional[Dict[str, str]]:
        """'Key: value' lines of the zone, inline '(...)' comments stripped.
        None if the zone is absent."""
        block = self.read(text)
        if block is None:
            return None
        result: Dict[str, str] = {}
        for line in block.splitlines():
            line = line.strip()
            if not line or ':' not in line:
                continue
            key, _, value = line.partition(':')
            value = value.split('(', 1)[0].strip()
            result[key.strip()] = value
        return result

    # --- write ---------------------------------------------------------------

    def wrap(self, body: str) -> str:
        """Frame a marker-less body with this zone's fence. Ends with '\\n'."""
        return f'{self.open_marker}\n{body}\n{self.close_marker}\n'

    def write(self, text: str, body: str) -> str:
        """Replace or insert this zone in `text`; returns the new text.

        Replace in place if present (claims_top zones also discard anything
        above the zone); else insert below `insert_after`'s close marker when
        that zone exists; else prepend, preserving all existing content.
        """
        block = self.wrap(body)

        if self.open_marker in text and self.close_marker in text:
            end = text.index(self.close_marker) + len(self.close_marker)
            if end < len(text) and text[end] == '\n':
                end += 1
            if self.claims_top:
                return block + text[end:]
            return text[:text.index(self.open_marker)] + block + text[end:]

        if self.insert_after is not None and self.insert_after.close_marker in text:
            idx = text.index(self.insert_after.close_marker) + len(self.insert_after.close_marker)
            if idx < len(text) and text[idx] == '\n':
                idx += 1
            return text[:idx] + '\n' + block + text[idx:]

        sep = '\n' if text and not text.startswith('\n') else ''
        return block + sep + text


RECONCILE_ZONE = AutoZone(
    'reconcile', '— do not edit manually, regenerated each run',
    claims_top=True,
)
PACKAGING_LOCK_ZONE = AutoZone(
    'packaging-lock', '— managed by packaging_lock.py, do not hand-edit',
    insert_after=RECONCILE_ZONE,
)
RECONCILE_DASHBOARD_ZONE = AutoZone(
    'reconcile-dashboard', '— regenerated each run, do not edit',
    claims_top=True,
)


# The fuzzy status-line read shared by the discovery scanners: matches
# 'Status: PUBLISHED' and '**Status:** IN PRODUCTION' near the top of the doc.
_STATUS_RE = re.compile(r'Status[:\s]*\*?\*?([A-Z ]+)')
_WORKING_TITLE_RE = re.compile(r'(?im)^.*working title:\s*"?(.+?)"?\s*$')


class StatusDoc:
    """A per-project PROJECT-STATUS.md: zones + the shared field reads."""

    def __init__(self, text: str, path: Optional[Path] = None) -> None:
        self.text = text
        self.path = path
        # A directly-constructed doc is trusted/writable. load() flips this off
        # when an EXISTING file could not be read, so a write can't clobber it.
        self._load_ok = True
        self._load_error: Optional[BaseException] = None

    @classmethod
    def load(cls, path: Path | str) -> "StatusDoc":
        """Read the doc. An ABSENT file loads as empty text (a legitimate new
        doc, writable). An EXISTING file that cannot be read or decoded loads
        with empty text but is marked UNWRITABLE: write_zone/save then refuse
        rather than overwrite the unreadable original with an empty AUTO block
        (the fail-open data-loss the 2026-07 audit found). Read-only field
        access still degrades gracefully to None/empty. Decoding is strict — a
        damaged byte fails closed instead of being silently dropped."""
        path = Path(path)
        doc = cls('', path)
        if path.exists():
            try:
                doc.text = path.read_text(encoding='utf-8')
            except (OSError, UnicodeDecodeError) as exc:
                doc._load_ok = False
                doc._load_error = exc
        return doc

    # --- zones ---------------------------------------------------------------

    def zone(self, zone: AutoZone) -> Optional[str]:
        return zone.read(self.text)

    def zone_fields(self, zone: AutoZone) -> Optional[Dict[str, str]]:
        return zone.fields(self.text)

    def write_zone(self, zone: AutoZone, body: str) -> None:
        self._guard_writable()
        self.text = zone.write(self.text, body)

    def _guard_writable(self) -> None:
        if not self._load_ok:
            raise StatusDocError(
                f'refusing to modify {self.path}: its existing content could not '
                f'be read ({self._load_error!r}); writing now would overwrite it. '
                f'Resolve the read error before regenerating its AUTO block.'
            )

    def save(self) -> str:
        """Write the doc back to its path via an atomic temp-file replace (a
        crash mid-write can't truncate the file). Returns the previous on-disk
        content (the backup contract the fence writers had). Refuses to write
        when the source file existed but could not be read (see load())."""
        if self.path is None:
            raise ValueError('StatusDoc has no path to save to')
        self._guard_writable()
        previous = ''
        if self.path.exists():
            try:
                previous = self.path.read_text(encoding='utf-8')
            except (OSError, UnicodeDecodeError):
                previous = ''
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write: same-dir temp file + os.replace (atomic on one volume),
        # matching write_text's encoding/newline handling for byte-parity.
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as fh:
                fh.write(self.text)
            os.replace(tmp, self.path)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
        return previous

    # --- shared field reads ----------------------------------------------------

    @property
    def working_title(self) -> Optional[str]:
        """The hand-written 'Working title:' line, unquoted. None if absent."""
        m = _WORKING_TITLE_RE.search(self.text)
        if m:
            return m.group(1).strip().strip('"')
        return None

    @property
    def status_label(self) -> Optional[str]:
        """Fuzzy 'Status:' label near the top of the doc (first 500 chars),
        as the discovery scanners read it. None if absent."""
        m = _STATUS_RE.search(self.text[:500])
        if m:
            return m.group(1).strip()
        return None
