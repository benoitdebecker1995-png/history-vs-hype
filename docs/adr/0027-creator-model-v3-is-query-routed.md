# Creator model v3 is query-routed, with raw speech as primary voice evidence

The creator supplied `Benoit_Voice_and_Brain_Model_v3.docx` on 14 August 2026 and asked that it be
implemented across the project. The document combines an editorial operating synthesis with a large
verbatim appendix. Loading the entire artifact on every task would contradict the front-room migration's
small-context boundary and would make generalized doctrine compete with more relevant current speech.

**Decision:** preserve the supplied DOCX and its full raw appendix under
`channel-data/creator-model/`. Route only relevant sections of `OPERATING-MODEL.md` for collaboration,
decision, research, packaging, or production questions. Route voice requests through
`tools.front_room.select_voice_examples`, which prefers current-project ad-libs, then searches the v3
raw corpus and explicitly approved language. Never treat raw historical examples as factual sources.

This decision updates the active authority described by ADR-0006. The older profile remains provenance
for deterministic lint rules that are compatible with v3, but it is no longer the normal context source
or the final authority in a conflict. Direct spontaneous speech and later creator-approved wording win;
generalized lint rules must be weakened or removed when they disagree.

**Consequences:** the active instructions carry the compact collaboration and voice defaults; the large
raw corpus stays query-only; the linter may encode explicit v3 anti-examples as advisory or hard rules
according to the document's own strength of wording; and a future replacement model needs a new source
record plus regression tests rather than an invisible prompt edit.

**Status:** accepted by the creator's implementation request.
