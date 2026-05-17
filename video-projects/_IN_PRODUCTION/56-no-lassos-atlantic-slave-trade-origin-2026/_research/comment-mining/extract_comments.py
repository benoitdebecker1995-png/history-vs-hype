import json
import glob
import os

videos = [
    ("cpT7VBoddns", "59K — Asmongold's INSANELY RACIST RANT On Africans | Hasanabi reacts (Dec 2025)"),
    ("a51O29TM78Q", "26K — \"Africans Sold Their Own\": What Really Happened (Africa Today, Mar 2026)"),
    ("CnIXdJ7vogc", "94 — The Day Lagos Was Taken: Oba Dosunmu and the British Betrayal (1861) (Ancients Tales, May 2025)"),
]

output = []
for vid_id, label in videos:
    matches = glob.glob(f"*{vid_id}*.info.json")
    if not matches:
        output.append(f"\n=== {label} ({vid_id}) === NO FILE FOUND")
        continue
    try:
        with open(matches[0], encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        comments = data.get("comments", [])
        output.append(f"\n=== {label} ({vid_id}) ===")
        output.append(f"Total comments in file: {len(comments)}")
        # sort by like_count desc to surface signal first
        sorted_c = sorted(comments, key=lambda c: c.get("like_count", 0) or 0, reverse=True)
        for i, c in enumerate(sorted_c[:50]):
            text = (c.get("text") or "").replace("\n", " ")[:400]
            likes = c.get("like_count", 0)
            output.append(f"  [{i+1}] ({likes} likes) {text}")
    except Exception as e:
        output.append(f"ERROR on {vid_id}: {e}")

result = "\n".join(output)
with open("comments-extracted.txt", "w", encoding="utf-8") as f:
    f.write(result)
print(f"Done. {len(output)} lines, {len(result)} chars -> comments-extracted.txt")
