"""
Round 2 comment mining — competitor debunk videos.
Round 1 mined topic-side (Asmongold/Hasanabi reaction + Africans Sold Their Own).
Round 2 mines competitor-side: who's already in our lane, what they got wrong,
where audience admits doubt.
"""
import json
import glob
import os
import sys

# Force UTF-8 stdout to survive Windows cp1252
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

videos = [
    ("UivhqdhcHNI", "1.7M — Matt Walsh: What Schools Don't Teach You About Slavery (Feb 2026, 3.41M subs) — PRO-talking-point"),
    ("R-1YoqWpzCM", "13K — The Conscious Lee: Debunking the Myth: Did Africans Really Sell Africans (Dec 2025, 133K subs) — CLOSEST-COMPETITOR debunk"),
    ("Z0Zhr4MnGLw", "13K — DGG_Clips: Destiny Reacts to Asmongold's Mental Gymnastics (Jan 2026, 7K subs) — DRAMA-LANE"),
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
        views = data.get("view_count")
        upload = data.get("upload_date")
        output.append(f"\n\n=== {label} ===")
        output.append(f"Video ID: {vid_id} | Views: {views} | Uploaded: {upload} | Comments pulled: {len(comments)}")
        output.append("-" * 80)
        # sort by like_count desc to surface signal first
        sorted_c = sorted(comments, key=lambda c: c.get("like_count", 0) or 0, reverse=True)
        for i, c in enumerate(sorted_c[:75]):
            text = (c.get("text") or "").replace("\n", " ")[:500]
            likes = c.get("like_count", 0) or 0
            author = c.get("author", "?")
            output.append(f"  [{i+1}] ({likes} likes | {author}) {text}")
    except Exception as e:
        output.append(f"ERROR on {vid_id}: {e}")

result = "\n".join(output)
out_path = "comments-extracted-round2.txt"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(result)
print(f"Done. {len(output)} lines, {len(result)} chars -> {out_path}")
