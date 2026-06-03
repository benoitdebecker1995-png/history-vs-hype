"""Extract YouTube comments from yt-dlp .info.json files into a categorization-ready text dump.

UTF-8 with errors='replace' is mandatory — emoji and non-ASCII crash cp1252 on Windows.
Filenames written by yt-dlp follow the pattern: "<title> [<video_id>].info.json"
"""
import json
from pathlib import Path

videos = [
    ("_J5bDhMP9lQ", "TEDxUniversityofNevada - Samina Ali - What does the Quran really say (6.8M, 2017)"),
    ("DegnK-3H3_s", "Nabi Asli - Origin of Hijab / Mahsa Amini (319K, 2022)"),
    ("lt-ee2hdbqY", "Brut India - Hijab History and Histrionics (166K, 2022)"),
    ("ZVtUfG5kciQ", "Imam Hussein TV 3 - Hijab in Islam Full Documentary (16K, 2019)"),
    # Amaliah colonialism video unavailable — dropped
]

# Add IDs added later
EXTRA_VIDEOS_FILE = Path("extra_videos.txt")
if EXTRA_VIDEOS_FILE.exists():
    for line in EXTRA_VIDEOS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 1)
        if len(parts) == 2:
            videos.append((parts[0].strip(), parts[1].strip()))

cwd = Path(".")
out_lines = []
total_comments = 0

for vid_id, label in videos:
    matches = list(cwd.glob(f"*[[]{vid_id}[]].info.json"))
    if not matches:
        out_lines.append(f"\n=== {label} ({vid_id}) ===")
        out_lines.append("ERROR: .info.json file not found (yt-dlp pull may have failed)")
        continue
    path = matches[0]
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        comments = data.get("comments") or []
        out_lines.append(f"\n=== {label} ({vid_id}) ===")
        out_lines.append(f"Source file: {path.name}")
        out_lines.append(f"Total comments returned: {len(comments)}")
        for i, c in enumerate(comments):
            text = (c.get("text") or "").replace("\n", " ").replace("\r", " ")
            text = text[:500]
            likes = c.get("like_count") or 0
            author = (c.get("author") or "").replace("\n", " ")[:40]
            out_lines.append(f"  [{i+1}] (likes={likes}) [{author}] {text}")
            total_comments += 1
    except Exception as e:
        out_lines.append(f"\n=== {label} ({vid_id}) ===")
        out_lines.append(f"ERROR reading {path.name}: {e}")

result = "\n".join(out_lines)
with open("comments-extracted.txt", "w", encoding="utf-8", errors="replace") as f:
    f.write(result)

print(f"Done. {len(out_lines)} lines, {len(result)} chars, {total_comments} comments extracted to comments-extracted.txt")
