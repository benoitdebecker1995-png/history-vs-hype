"""Tests for the topic-note miner's fabrication guard.

The guard is the whole reason bulk extraction can be dispatched to a cheap
model: nothing a model writes reaches `.brain/` unless code can prove it was
copied. These tests pin that property, so a future "let's be more lenient"
edit fails loudly.
"""

import json

import pytest

from tools.brain import topic_mine as tm


DOSSIER = """# 01 — Verified Research

## CORE FACTS

### F1 — Article text ✅
> "no pretext arising from religious opinions shall ever produce an interruption"

**Source:** Hunter Miller 1931, Vol. 2, p. 384.

### F2 — Timeline ✅
- Signed at **Tripoli, November 4, 1796** by Joel Barlow.
- Cathcart "did not read Arabic, although he seems to have been familiar with Turkish".

**Source:** Spellberg 2013, fn 69.
"""


def _claim(**over):
    base = {
        "claim": "The treaty was signed at Tripoli in November 1796.",
        "topics": ["treaty-timeline"],
        "verbatim": None,
        "source": "Hunter Miller 1931, Vol. 2, p. 384",
        "status": "verified",
        "anchor": "F2 — Timeline ✅",
    }
    base.update(over)
    return base


def run(claims, body=DOSSIER):
    report = tm.ValidationReport()
    rejects: list[dict] = []
    kept = tm.validate_claims(claims, body, "test-video", report, rejects)
    return kept, report, rejects


# --------------------------------------------------------------------------
# normalize — folds formatting, never words
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a,b",
    [
        ("**bold text here**", "bold text here"),
        ("smart “quotes”", 'smart "quotes"'),
        ("em — dash", "em - dash"),
        ("spaced\n\n  out", "spaced out"),
        ("`code`", "code"),
    ],
)
def test_normalize_folds_formatting(a, b):
    assert tm.normalize(a) == tm.normalize(b)


def test_normalize_does_not_fold_different_words():
    assert tm.normalize("Barlow did not read Arabic") != tm.normalize(
        "Barlow could not read Arabic"
    )


# --------------------------------------------------------------------------
# Rule 1 — verbatim must be an exact copy
# --------------------------------------------------------------------------


def test_exact_verbatim_survives_despite_markdown_bold():
    kept, report, _ = run([_claim(verbatim="Signed at Tripoli, November 4, 1796 by Joel Barlow.")])
    assert len(kept) == 1
    assert kept[0].verbatim_verified is True
    assert report.verbatim_ok == 1


def test_reworded_verbatim_is_stripped_and_logged():
    """A quote the model 'repaired' must not reach the note."""
    kept, report, rejects = run(
        [_claim(verbatim="Signed at Tripoli on the 4th of November 1796 by Mr Joel Barlow.")]
    )
    assert len(kept) == 1, "the claim survives"
    assert kept[0].verbatim is None, "but the unverifiable quote does not"
    assert report.verbatim_stripped == 1
    assert any(r["reason"] == "verbatim-not-in-dossier" for r in rejects)


def test_hallucinated_quote_from_model_knowledge_is_stripped():
    kept, _, rejects = run(
        [_claim(verbatim="The government of the United States is founded upon liberty alone.")]
    )
    assert kept[0].verbatim is None
    assert rejects[0]["reason"] == "verbatim-not-in-dossier"


def test_short_verbatim_is_dropped_not_flagged():
    kept, report, _ = run([_claim(verbatim="Tripoli")])
    assert kept[0].verbatim is None
    assert report.verbatim_stripped == 0


# --------------------------------------------------------------------------
# Rule 2 — attribution must already exist in the dossier
# --------------------------------------------------------------------------


def test_invented_source_drops_the_claim():
    kept, report, rejects = run([_claim(source="Gibbon 1776, Decline and Fall, p. 12")])
    assert kept == []
    assert report.reasons["source-not-in-dossier"] == 1
    assert rejects[0]["reason"] == "source-not-in-dossier"


def test_real_source_passes():
    kept, _, _ = run([_claim(source="Spellberg 2013, fn 69")])
    assert len(kept) == 1


def test_missing_source_drops_the_claim():
    for bad in ("", "unknown", "N/A"):
        kept, report, _ = run([_claim(source=bad)])
        assert kept == [], bad


# --------------------------------------------------------------------------
# Claim shape
# --------------------------------------------------------------------------


def test_non_atomic_claim_is_dropped():
    kept, report, _ = run([_claim(claim=" ".join(["word"] * (tm.MAX_CLAIM_WORDS + 1)))])
    assert kept == []
    assert report.reasons["claim-not-atomic"] == 1


def test_verbose_but_usable_claim_is_kept_and_flagged():
    """Verified research must not be lost to a word count."""
    words = tm.ATOMIC_CLAIM_WORDS + 3
    assert words < tm.MAX_CLAIM_WORDS
    kept, _, _ = run([_claim(claim=" ".join(["word"] * words))])
    assert len(kept) == 1
    assert "verbose" in kept[0].flags


def test_claim_without_topic_is_dropped():
    kept, report, _ = run([_claim(topics=[])])
    assert kept == []
    assert report.reasons["no-topic"] == 1


def test_topics_are_slugified_and_capped_at_three():
    kept, _, _ = run([_claim(topics=["Treaty Timeline", "A/B Concept", "c", "d"])])
    assert kept[0].topics == ["treaty-timeline", "ab-concept", "c"]


def test_non_object_claim_is_rejected():
    kept, report, _ = run(["not a dict", 42])
    assert kept == []
    assert report.reasons["not-an-object"] == 2


# --------------------------------------------------------------------------
# Quotation vs dossier prose — the laundering guard
# --------------------------------------------------------------------------


def test_blockquote_line_counts_as_a_quotation():
    kept, _, _ = run(
        [_claim(verbatim="no pretext arising from religious opinions shall ever produce an interruption")]
    )
    assert kept[0].verbatim_is_quote is True


def test_quoted_run_inside_a_bullet_counts_as_a_quotation():
    kept, _, _ = run(
        [_claim(verbatim='"did not read Arabic, although he seems to have been familiar with Turkish"')]
    )
    assert kept[0].verbatim_is_quote is True


def test_dossier_prose_is_verified_but_not_a_quotation():
    """Exact-match proves provenance, not utterance. Prose must not be quoted."""
    kept, _, _ = run([_claim(verbatim="Signed at Tripoli, November 4, 1796 by Joel Barlow.")])
    assert kept[0].verbatim_verified is True
    assert kept[0].verbatim_is_quote is False


def test_only_quotations_render_as_quotes():
    kept, _, _ = run(
        [
            _claim(verbatim="Signed at Tripoli, November 4, 1796 by Joel Barlow."),
            _claim(
                claim="The treaty barred religious pretexts.",
                verbatim="no pretext arising from religious opinions shall ever produce an interruption",
            ),
        ]
    )
    note = tm.render_topic_note("treaty-timeline", kept)
    assert "no pretext arising from religious opinions" in note
    assert "> \"Signed at Tripoli" not in note


# --------------------------------------------------------------------------
# Anchors
# --------------------------------------------------------------------------


def test_anchor_matches_with_or_without_hash_prefix():
    for anchor in ("F2 — Timeline ✅", "### F2 — Timeline ✅"):
        kept, _, _ = run([_claim(anchor=anchor)])
        assert kept[0].anchor is not None, anchor
        assert "anchor-unresolved" not in kept[0].flags


def test_invented_anchor_is_dropped_and_flagged():
    kept, _, _ = run([_claim(anchor="F99 — Something Invented")])
    assert kept[0].anchor is None
    assert "anchor-unresolved" in kept[0].flags


# --------------------------------------------------------------------------
# JSON scraping from model output
# --------------------------------------------------------------------------


def test_first_json_object_ignores_braces_inside_strings():
    text = 'prose before {"claims": [{"claim": "a } brace { in text"}]} trailing'
    blob = tm._first_json_object(text)
    assert json.loads(blob)["claims"][0]["claim"] == "a } brace { in text"


def test_first_json_object_handles_escaped_quotes():
    text = r'{"claims": [{"claim": "he said \"no\" firmly"}]}'
    assert json.loads(tm._first_json_object(text))["claims"][0]["claim"] == 'he said "no" firmly'


def test_strip_fence_removes_json_code_fence():
    assert tm._strip_fence('```json\n{"a": 1}\n```') == '{"a": 1}'


def test_first_json_object_returns_none_when_absent():
    assert tm._first_json_object("no object here") is None


# --------------------------------------------------------------------------
# Slugs
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,expected",
    [
        ("Hunter Miller 1931, Vol. 2, p. 384", "hunter-1931"),
        ("Spellberg 2013, fn 69", "spellberg-2013"),
    ],
)
def test_source_slug_is_stable(source, expected):
    assert tm.source_slug(source) == expected


def test_source_slug_survives_a_sourceless_string():
    assert tm.source_slug("the treaty itself") != ""


# --------------------------------------------------------------------------
# Source quality — an attribution that names no one
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,expected",
    [
        ("Wolpert, Jinnah of Pakistan, p. 333", "citable"),
        ("Multiple academic sources", "vacuous"),
        ("Multiple secondary sources give this date", "vacuous"),
        ("several scholars", "vacuous"),
        ("ibid.", "vacuous"),
        ("NotebookLM", "vacuous"),
        ("NotebookLM query on partition", "vacuous"),
        ("Wikipedia", "tertiary"),
        ("Encyclopaedia Britannica", "tertiary"),
    ],
)
def test_classify_source(source, expected):
    assert tm.classify_source(source) == expected


def test_tertiary_source_cannot_carry_a_verified_claim():
    """A Phase-1 Wikipedia brief must not read as verified research."""
    body = DOSSIER + "\n**Source:** Wikipedia\n"
    kept, _, _ = run([_claim(source="Wikipedia", status="verified")], body=body)
    assert kept[0].status == "partial"
    assert kept[0].source_quality == "tertiary"


def test_topic_note_only_links_source_notes_that_exist():
    kept, _, _ = run([_claim(source="Spellberg 2013, fn 69")])
    slug = tm.source_slug(kept[0].source)
    linked = tm.render_topic_note("t", kept, linkable={slug})
    unlinked = tm.render_topic_note("t", kept, linkable=set())
    assert f"[[src-{slug}]]" in linked
    assert "[[src-" not in unlinked
    assert "Spellberg 2013, fn 69" in unlinked, "attribution still shown as text"


# --------------------------------------------------------------------------
# Taxonomy fold — links must survive the rename
# --------------------------------------------------------------------------


def test_source_note_links_canonical_topic_not_raw_slug(tmp_path, monkeypatch):
    """Source notes link topics too. If the fold only renamed the topic dict,
    every source note would point at a note name that no longer exists."""
    taxonomy = {
        "canonical": {
            "map-as-evidence": {
                "title": "Map as Evidence",
                "aliases": ["columbus-cartography"],
            }
        }
    }
    (tmp_path / "_taxonomy.json").write_text(json.dumps(taxonomy), encoding="utf-8")
    extracted = tmp_path / "_extracted"
    extracted.mkdir()
    monkeypatch.setattr(tm, "TOPICS_DIR", tmp_path)
    monkeypatch.setattr(tm, "SOURCES_DIR", tmp_path / "sources")
    monkeypatch.setattr(tm, "EXTRACT_DIR", extracted)
    monkeypatch.setattr(tm, "TAXONOMY_PATH", tmp_path / "_taxonomy.json")
    monkeypatch.setattr(tm, "REJECT_LOG", extracted / "_rejected.jsonl")

    dossier = tmp_path / "d.md"
    dossier.write_text(DOSSIER, encoding="utf-8")
    monkeypatch.setattr(tm, "REPO", tmp_path)
    (extracted / "v.json").write_text(
        json.dumps(
            {
                "video": "v",
                "source_file": "d.md",
                "claims": [
                    _claim(topics=["columbus-cartography"]),
                    _claim(
                        claim="A second claim so the source note is written.",
                        topics=["columbus-cartography"],
                    ),
                ],
            }
        ),
        encoding="utf-8",
    )

    tm.build()
    assert (tmp_path / "map-as-evidence.md").exists()
    assert not (tmp_path / "columbus-cartography.md").exists()

    note = next((tmp_path / "sources").glob("src-*.md")).read_text(encoding="utf-8")
    assert "[[map-as-evidence]]" in note
    assert "[[columbus-cartography]]" not in note


# --------------------------------------------------------------------------
# Audit — catch tool-as-source at write time
# --------------------------------------------------------------------------


AUDIT_DOSSIER = """# Verified Research

**Phase:** 2 (Academic Verification — NotebookLM Complete)
**Status:** 100% verified

| Treaty signed | July 13, 1713 | NotebookLM verification | OK |
| Rooke's fleet | 52 English + 10 Dutch | NLM sources | OK |

**Sources:** Multiple academic sources confirm

- The map compiled from "Multiple older source maps which have not survived" — Inscription 6 names them.
- Casualty figure — Wikipedia
- Modern protest wave — [Wikipedia](https://en.wikipedia.org/wiki/X)
- Death toll ~14,500 (Tier 3) — Britannica
- Facsimile of the 1941 Act — Wikimedia Commons scan, PD-Ukraine
- The border fence — Jackson, *The Rock of the Gibraltarians*, p. 262
"""


def _audit(tmp_path, text=AUDIT_DOSSIER):
    f = tmp_path / "01-VERIFIED-RESEARCH.md"
    f.write_text(text, encoding="utf-8")
    return tm.audit_dossier(f, "test-video")


def test_audit_catches_tool_as_source_in_a_table_cell(tmp_path, monkeypatch):
    """The real corpus hides attributions in table cells, not bare fields."""
    monkeypatch.setattr(tm, "REPO", tmp_path)
    kinds = [(f.line_no, f.kind) for f in _audit(tmp_path)]
    blocking = [k for k in kinds if k[1] == "tool-or-vague-plural"]
    assert len(blocking) == 3, f"NotebookLM/NLM cells + Multiple-sources line, got {kinds}"


def test_audit_ignores_document_metadata_lines(tmp_path, monkeypatch):
    """`**Phase:** 2 (… NotebookLM Complete)` records the tool used, not a source."""
    monkeypatch.setattr(tm, "REPO", tmp_path)
    assert not [f for f in _audit(tmp_path) if f.line_no in (3, 4)]


def test_audit_ignores_quoted_myth_being_debunked(tmp_path, monkeypatch):
    monkeypatch.setattr(tm, "REPO", tmp_path)
    assert not [f for f in _audit(tmp_path) if "older source maps" in f.line]


def test_audit_respects_web_policy_url_and_tier_labels(tmp_path, monkeypatch):
    """WEB-POLICY allows tertiary WITH a URL; an explicit tier label is honesty."""
    monkeypatch.setattr(tm, "REPO", tmp_path)
    flagged = {f.line for f in _audit(tmp_path)}
    assert not any("en.wikipedia.org/wiki/X" in ln for ln in flagged), "URL cite is compliant"
    assert not any("Tier 3" in ln for ln in flagged), "tier-labelled is honest"
    assert not any("Wikimedia Commons scan" in ln for ln in flagged), "archive host, not source"


def test_audit_passes_a_real_attribution(tmp_path, monkeypatch):
    monkeypatch.setattr(tm, "REPO", tmp_path)
    assert not [f for f in _audit(tmp_path) if "Rock of the Gibraltarians" in f.line]


def test_audit_flags_bare_tertiary_without_url(tmp_path, monkeypatch):
    monkeypatch.setattr(tm, "REPO", tmp_path)
    assert [f for f in _audit(tmp_path)
            if f.kind == "unlabelled-tertiary" and "Casualty figure" in f.line]
