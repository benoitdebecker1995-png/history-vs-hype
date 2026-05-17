"""Build a web-lookup prompt for files where author OR title is missing/Unknown.
The user will paste this into a web-capable AI (ChatGPT, Perplexity, etc.) to resolve."""
import os, re, json
from collections import defaultdict

ROOT = r"D:\History vs Hype\library\by-topic"

categories = defaultdict(list)
for folder in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p): continue
    for f in os.listdir(p):
        if not os.path.isfile(os.path.join(p, f)): continue
        m = re.match(r'^(.+?)-(.+?)-(\d{4})-(.+?)(?:-v\d+)?\.[a-z0-9]+$', f)
        if not m: continue
        t, a, y, pub = m.groups()
        t_unk = t.lower() == 'unknown'
        a_unk = a.lower() == 'unknown'
        y_unk = y == '0000'
        p_unk = pub.lower() in ('unknown','zlib','libgen','annaarchive','z-library')
        # Skip files already in image-only-pdfs (separate workflow)
        if t_unk and a_unk:
            categories["BOTH_UNKNOWN_TITLE_AND_AUTHOR"].append((folder, f, t, a, y, pub))
        elif t_unk:
            categories["TITLE_UNKNOWN"].append((folder, f, t, a, y, pub))
        elif a_unk:
            # has title, missing author — best web-lookup candidate
            categories["AUTHOR_UNKNOWN"].append((folder, f, t, a, y, pub))

# Build the prompt
out_lines = []
out_lines.append("# Web Lookup Prompt — Missing Author/Title Files")
out_lines.append("")
out_lines.append("**Paste the prompt below into ChatGPT / Perplexity / any web-capable AI.**")
out_lines.append("")
out_lines.append("---")
out_lines.append("")
out_lines.append("## Prompt:")
out_lines.append("")
out_lines.append("```")
out_lines.append("You are helping me identify academic books and articles by partial metadata so I can rename them.")
out_lines.append("")
out_lines.append("For each entry below, search the web for the work and return: title, author, year, publisher.")
out_lines.append("")
out_lines.append("Each entry shows what I already know in the format:")
out_lines.append("  [folder] title_slug | a=author | y=year | p=publisher")
out_lines.append("where 'Unknown' or '0000' means I need you to find it.")
out_lines.append("")
out_lines.append("Output as a markdown table with columns: file_index | title_slug (verified) | author_surname | year | publisher_abbrev | source_url")
out_lines.append("")
out_lines.append("Use these publisher abbreviations: CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP, EdinburghUP,")
out_lines.append("NYUPress, UCPress, JohnsHopkinsUP, HooverPress, PlutoPress, Routledge, Palgrave, Bloomsbury, ITauris,")
out_lines.append("HurstCo, ZedBooks, VersoBooks, BasicBooks, RandomHouse, Penguin, Brill, Springer, DaCapo, FreePress,")
out_lines.append("Granta, WeidenfeldNicolson, CornellUP, StanfordUP, HarvardUP, LiverpoolUP, MacmillanUK, NortonCo.")
out_lines.append("")
out_lines.append("If you cannot find a work with high confidence, mark it 'UNRESOLVED' in the table and skip — do not guess.")
out_lines.append("")
out_lines.append("---")
out_lines.append("")

idx_counter = 1
for cat, entries in categories.items():
    if not entries: continue
    out_lines.append(f"### Section: {cat}  ({len(entries)} files)")
    out_lines.append("")
    for folder, f, t, a, y, pub in entries:
        out_lines.append(f"{idx_counter}. [{folder}] {t} | a={a} | y={y} | p={pub}")
        idx_counter += 1
    out_lines.append("")
out_lines.append("```")
out_lines.append("")
out_lines.append("---")
out_lines.append("")
out_lines.append("## Reference: original filenames (for ambiguous cases)")
out_lines.append("")
out_lines.append("If the slug above is ambiguous, the original filename may help. These are still on disk:")
out_lines.append("")

idx_counter = 1
for cat, entries in categories.items():
    for folder, f, t, a, y, pub in entries:
        out_lines.append(f"{idx_counter}. `library/by-topic/{folder}/{f}`")
        idx_counter += 1

out_lines.append("")
out_lines.append(f"**Total: {idx_counter-1} files to look up.**")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\WEB-LOOKUP-PROMPT.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print(f"Wrote WEB-LOOKUP-PROMPT.md with {idx_counter-1} files")
for cat, entries in categories.items():
    print(f"  {cat}: {len(entries)}")
