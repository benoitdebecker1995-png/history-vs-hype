import json

videos = [
    ("bPTgUZuL4Uk", "4.1M — CurioStation / Graham Hancock 'Original World Map'"),
    ("ACEoMEZO17E", "117K — Beyond Secrets / Graham Hancock 2025"),
    ("PYm3b4KpXA0", "83K — Digital Explorer / AI Analysis 2026"),
]

output = []
for vid_id, label in videos:
    try:
        with open(f"{vid_id}.info.json", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        comments = data.get("comments", [])
        output.append(f"\n=== {label} ({vid_id}) ===")
        output.append(f"Total comments in file: {len(comments)}")
        for i, c in enumerate(comments[:50]):
            text = c.get("text", "").replace("\n", " ")[:300]
            likes = c.get("like_count", 0)
            output.append(f"  [{i+1}] ({likes} likes) {text}")
    except Exception as e:
        output.append(f"ERROR on {vid_id}: {e}")

result = "\n".join(output)
with open("comments-extracted.txt", "w", encoding="utf-8") as f:
    f.write(result)
print(f"Done. {len(output)} lines -> comments-extracted.txt")
