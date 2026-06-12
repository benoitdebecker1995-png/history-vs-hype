import json, glob, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Dedupe by video id (read from JSON, not filename), prefer newest file
files = {}
for path in glob.glob("*.info.json"):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
    except Exception:
        continue
    vid = data.get("id")
    if not vid:
        continue
    if vid not in files or os.path.getmtime(path) > files[vid][0]:
        files[vid] = (os.path.getmtime(path), path, data)

out = []
summary = []
total = 0
for vid, (_, path, data) in sorted(files.items(), key=lambda kv: -(kv[1][2].get("view_count") or 0)):
    comments = data.get("comments") or []
    total += len(comments)
    title = data.get("title", "?")
    views = data.get("view_count", 0)
    chan = data.get("channel", "?")
    n_total = data.get("comment_count", "?")
    summary.append(f"{vid} | {chan} | views={views} | fetched={len(comments)} | total_on_video={n_total} | {title[:70]}")
    out.append(f"\n\n=== {vid} | {chan} | {views} views | {len(comments)} comments fetched (of {n_total} on video) ===")
    out.append(f"TITLE: {title}")
    comments = sorted(comments, key=lambda c: -(c.get("like_count") or 0))
    for i, c in enumerate(comments):
        text = (c.get("text") or "").replace("\n", " ").strip()[:400]
        likes = c.get("like_count") or 0
        out.append(f"[{vid[:4]}-{i+1}] ({likes}L) {text}")

with open("comments-extracted.txt", "w", encoding="utf-8", errors="replace") as f:
    f.write("\n".join(out))
with open("extract-summary.txt", "w", encoding="utf-8", errors="replace") as f:
    f.write("\n".join(summary))
print("\n".join(summary))
print(f"\nWrote {total} comments to comments-extracted.txt")
