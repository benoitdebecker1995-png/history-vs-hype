"""Round 3: build Gemini Flash batch input files with PDF content excerpts.

For each entry in round3-incomplete-inventory.json, extract first 2 pages
via PyMuPDF, then write per-folder batch files with prompt header + entries.

Output: round3-input-{folder}[-N].txt
"""
import json, re, sys
from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path(r"D:\History vs Hype\library\by-topic")
OUT_DIR = Path(r"D:\History vs Hype\_gemini-output\layer2-rename")
INVENTORY_JSON = OUT_DIR / "round3-incomplete-inventory.json"

MAX_TEXT_CHARS = 1500           # text excerpt per file (~375 tokens)
MAX_ENTRIES_PER_BATCH = 60      # cap batch size for stable Gemini output

PROMPT_HEADER = """\
You are identifying academic books, journal articles, treaties, and primary
documents from partial metadata + an excerpt of the first two pages of the
PDF. For each entry below, search the web (Google Search grounding) to verify
the work and return its full metadata.

Each entry shows:
  - The current filename (after prior parsing)
  - Known fields: title slug, author surname, year, publisher
  - 'Unknown' / '0000' = unresolved field
  - A short excerpt from the first two pages of the PDF (may be empty if the
    document is scanned image-only — proceed using the filename in that case)

INSTRUCTIONS
- Resolve EVERY missing field where you can find authoritative evidence.
- Use Google Search grounding; cross-reference excerpt content + filename.
- Do NOT guess. Mark UNRESOLVED if no high- or medium-confidence answer.
- Confidence levels:
    high   — primary source (publisher page, library catalogue, JSTOR)
    medium — secondary source (Wikipedia, Google Books snippet)
    low    — inference from excerpt only (rarely use; usually UNRESOLVED)
- source_url is REQUIRED for any non-UNRESOLVED row.
- publisher_abbrev MUST come from this list (use the closest match):
  CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP,
  EdinburghUP, NYUPress, UCPress, JohnsHopkinsUP, HooverPress, PlutoPress,
  Routledge, Palgrave, Bloomsbury, ITauris, HurstCo, ZedBooks, VersoBooks,
  BasicBooks, RandomHouse, Penguin, Brill, Springer, DaCapo, FreePress,
  Granta, WeidenfeldNicolson, CornellUP, StanfordUP, HarvardUP, LiverpoolUP,
  MacmillanUK, NortonCo, HMSO, UN, ICJ, OECD, LHarmattan, Macmillan,
  HoughtonMifflin, Serif.
  If publisher is a journal article, use the journal abbreviation
  (e.g. JModernHistory, IntlAffairs). If it is a government / IGO document,
  use the issuer abbreviation (HMSO, UN, ICJ, FCO, etc.).

OUTPUT
Return a single markdown table with exactly these columns:

| idx | title_slug | author_surname | year | publisher_abbrev | confidence | source_url |

- idx: the integer from the entry header below.
- title_slug: CamelCase, no spaces, no punctuation, ≤45 chars.
- author_surname: surname only (e.g. Zinn, Akcam, Martinez — strip diacritics).
- year: 4 digits, or 0000 if truly unknown.
- All UNRESOLVED rows: put UNRESOLVED in every field except idx.

Do NOT include any prose before or after the table.

---

ENTRIES:

"""


def extract_pdf_text(pdf_path: Path, max_chars: int = MAX_TEXT_CHARS) -> str:
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return f"[EXTRACT-FAILED: {type(e).__name__}]"
    out = []
    for page_idx in range(min(2, len(doc))):
        try:
            text = doc[page_idx].get_text() or ""
        except Exception:
            text = ""
        if text.strip():
            out.append(text.strip())
    doc.close()
    blob = "\n---PAGE---\n".join(out)
    # Collapse whitespace.
    blob = re.sub(r"[ \t]+", " ", blob)
    blob = re.sub(r"\n{3,}", "\n\n", blob)
    return blob[:max_chars].strip()


def render_entry(e: dict, text: str) -> str:
    return (
        f"{e['idx']}. [{e['folder']}] {e['filename']}\n"
        f"   known: t={e['title']} | a={e['author']} | y={e['year']} | p={e['publisher']}\n"
        f"   missing: {','.join(e['missing_fields'])}\n"
        f"   excerpt: {text!r}\n"
    )


def write_batch(folder_label: str, entries_with_text: list, out_path: Path) -> None:
    body = "\n".join(render_entry(e, t) for e, t in entries_with_text)
    out_path.write_text(PROMPT_HEADER + body + "\n", encoding="utf-8")
    print(f"  -> {out_path.name}  ({len(entries_with_text)} entries, {out_path.stat().st_size} bytes)")


def main():
    with open(INVENTORY_JSON, encoding="utf-8") as f:
        inv = json.load(f)
    entries = inv["inventory"]

    by_folder = {}
    for e in entries:
        by_folder.setdefault(e["folder"], []).append(e)

    summary = {}
    extract_failed_count = 0

    for folder, items in by_folder.items():
        print(f"\n[{folder}] {len(items)} entries")
        # Extract text once per entry.
        items_with_text = []
        for e in items:
            pdf_path = ROOT / folder / e["filename"]
            if pdf_path.exists():
                txt = extract_pdf_text(pdf_path)
                if txt.startswith("[EXTRACT-FAILED"):
                    extract_failed_count += 1
            else:
                txt = "[FILE-NOT-FOUND]"
                extract_failed_count += 1
            items_with_text.append((e, txt))

        # Sub-batch if needed.
        if len(items_with_text) <= MAX_ENTRIES_PER_BATCH:
            out_path = OUT_DIR / f"round3-input-{folder}.txt"
            write_batch(folder, items_with_text, out_path)
            summary[folder] = [out_path.name]
        else:
            chunks = [
                items_with_text[i : i + MAX_ENTRIES_PER_BATCH]
                for i in range(0, len(items_with_text), MAX_ENTRIES_PER_BATCH)
            ]
            summary[folder] = []
            for n, chunk in enumerate(chunks, start=1):
                out_path = OUT_DIR / f"round3-input-{folder}-batch{n}.txt"
                write_batch(folder, chunk, out_path)
                summary[folder].append(out_path.name)

    print("\n=== SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"Extract-failed (no PDF text): {extract_failed_count}")


if __name__ == "__main__":
    main()
