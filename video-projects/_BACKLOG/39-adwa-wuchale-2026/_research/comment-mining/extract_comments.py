"""Extract top 50 comments per video into a single text file."""
import json
import glob

videos = [
    ("1Hln0GjuUQk", "1.68M — Armchair Historian, military-tactics"),
    ("DzclxJ3xMbc", "338K — History Journo, mainstream-doc"),
    ("HI5A_2DKm_0", "297K — Extra History, history-survey"),
    ("HNQGzlI1N5M", "39K — HomeTeam History, revisionist"),
]

output = []
for vid_id, label in videos:
    matches = glob.glob(f"*{vid_id}*.info.json")
    if not matches:
        output.append(f"\n=== {label} ({vid_id}) ===\nERROR: file not found")
        continue
    try:
        with open(matches[0], encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        comments = data.get("comments", []) or []
        output.append(f"\n=== {label} ({vid_id}) ===")
        output.append(f"Total comments in file: {len(comments)}")
        for i, c in enumerate(comments[:50]):
            text = (c.get("text", "") or "").replace("\n", " ")[:300]
            likes = c.get("like_count", 0)
            output.append(f"  [{i+1}] ({likes} likes) {text}")
    except Exception as e:
        output.append(f"ERROR on {vid_id}: {e}")

result = "\n".join(output)
with open("comments-extracted.txt", "w", encoding="utf-8", errors="replace") as f:
    f.write(result)
print(f"Done. {len(output)} lines, {len(result)} chars -> comments-extracted.txt")
