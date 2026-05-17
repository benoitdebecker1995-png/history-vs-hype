"""Build manual review list for image-only PDFs.
These cannot be auto-identified (no extractable text, no useful PDF metadata).
User must open each and decide: keep + rename / stash."""
import json, os

ROOT = r"D:\History vs Hype\library\by-topic"
STASH = r"D:\History vs Hype\library\_stash-offtopic"

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\image-only-pdfs.json", encoding="utf-8") as f:
    image_only = json.load(f)

# Check which still exist at original path (some renamed in later passes, some stashed)
still_present = []
stashed = []
renamed = []
for d in image_only:
    folder = d["folder"]; fname = d["f"]
    orig_path = os.path.join(ROOT, folder, fname)
    if os.path.exists(orig_path):
        still_present.append({"folder":folder,"fname":fname,"size_mb":d["size"]/(1024*1024)})
        continue
    # Check stash (folder-prefix naming convention from earlier stash ops)
    candidates = [f for f in os.listdir(STASH) if f.endswith(fname) or fname in f]
    if candidates:
        stashed.append({"folder":folder,"orig":fname,"in_stash":candidates[0]})
        continue
    # Probably renamed by metadata pass — track separately
    renamed.append({"folder":folder,"orig":fname})

print(f"Still present (need manual review): {len(still_present)}")
print(f"Already stashed:                    {len(stashed)}")
print(f"Renamed by later pass:              {len(renamed)}")
print()

lines = []
lines.append("# Manual Review — Image-Only PDFs")
lines.append("")
lines.append(f"These {len(still_present)} PDFs are scanned image-only — no extractable text, no useful PDF metadata.")
lines.append("Auto-identification failed. You need to open each and decide.")
lines.append("")
lines.append("For each file, click the path link, glance at the cover/first page, then mark:")
lines.append("- **KEEP** → fill in: title slug, author surname, year, publisher abbreviation")
lines.append("- **STASH** → if off-topic / personal doc / not channel-relevant")
lines.append("- **DELETE** → if obvious junk / duplicate")
lines.append("")
lines.append("Format: paste this filled table back to Claude:")
lines.append("```")
lines.append("| # | verdict | new_title_slug | author | year | publisher |")
lines.append("| - | ------- | -------------- | ------ | ---- | --------- |")
lines.append("| 1 | KEEP    | RealTitleHere  | Author | 2010 | OxfordUP  |")
lines.append("| 2 | STASH   |                |        |      |           |")
lines.append("```")
lines.append("")
lines.append("---")
lines.append("")

for idx, d in enumerate(still_present, 1):
    abs_path = os.path.join(ROOT, d["folder"], d["fname"]).replace("\\", "/")
    lines.append(f"### {idx}. `[{d['folder']}]` {d['fname']}  ({d['size_mb']:.1f} MB)")
    lines.append(f"   Open: `{abs_path}`")
    lines.append("")

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\MANUAL-REVIEW-IMAGE-ONLY.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote MANUAL-REVIEW-IMAGE-ONLY.md ({len(still_present)} entries)")
