"""Compute weighted scores per bucket from manual categorization.

Categorization format: (video_id, comment_idx, likes, tier, bucket)
- tier: 1 (unmet demand) | 2 (validating engagement); Tier 0 = filtered, not in list
- bucket: '1', '2', '3', '4', '5a', '5b', '5c', '5d', '5e'
"""
import json

# Like multiplier
def like_mult(likes):
    if likes <= 2: return 1.0
    if likes <= 9: return 1.5
    if likes <= 49: return 2.0
    return 3.0

# Tier weight
def tier_weight(tier):
    return 2 if tier == 1 else 1

# (video, idx, likes, tier, bucket)
# Manual categorizations from reading comments-extracted.txt
data = [
    # === Samina Ali (TEDx) — 200 comments ===
    ("samina", 2, 1, 1, "5a"),
    ("samina", 3, 0, 2, "5b"),
    ("samina", 17, 0, 2, "5a"),
    ("samina", 21, 0, 1, "5b"),
    ("samina", 22, 0, 2, "5a"),
    ("samina", 23, 1, 1, "5a"),
    ("samina", 24, 0, 1, "5a"),
    ("samina", 26, 0, 1, "5d"),
    ("samina", 28, 0, 2, "5b"),
    ("samina", 31, 0, 2, "5a"),
    ("samina", 32, 0, 2, "5a"),
    ("samina", 33, 0, 2, "5a"),
    ("samina", 38, 1, 2, "2"),
    ("samina", 42, 0, 1, "5d"),
    ("samina", 43, 0, 2, "3"),
    ("samina", 45, 0, 1, "5b"),
    ("samina", 50, 0, 1, "5d"),
    ("samina", 51, 1, 1, "4"),
    ("samina", 52, 0, 2, "5d"),
    ("samina", 54, 0, 1, "5a"),
    ("samina", 55, 0, 2, "5a"),
    ("samina", 56, 0, 1, "5d"),
    ("samina", 58, 0, 2, "3"),
    ("samina", 59, 0, 1, "5d"),
    ("samina", 61, 0, 1, "5a"),
    ("samina", 64, 0, 2, "2"),
    ("samina", 66, 0, 1, "2"),
    ("samina", 68, 2, 2, "5a"),
    ("samina", 69, 0, 2, "2"),
    ("samina", 73, 1, 1, "4"),
    ("samina", 75, 0, 2, "5a"),
    ("samina", 78, 0, 1, "5a"),
    ("samina", 79, 0, 2, "5a"),
    ("samina", 82, 2, 1, "5a"),
    ("samina", 83, 0, 2, "5a"),
    ("samina", 85, 1, 1, "5a"),
    ("samina", 86, 0, 2, "5b"),
    ("samina", 87, 1, 1, "5a"),
    ("samina", 89, 0, 1, "3"),
    ("samina", 91, 2, 1, "3"),
    ("samina", 93, 3, 1, "5a"),
    ("samina", 99, 0, 1, "5a"),
    ("samina", 102, 1, 2, "5a"),
    ("samina", 104, 0, 1, "5a"),
    ("samina", 105, 0, 1, "5a"),
    ("samina", 106, 0, 1, "2"),
    ("samina", 112, 1, 1, "5d"),
    ("samina", 113, 0, 2, "5d"),
    ("samina", 119, 0, 2, "5b"),
    ("samina", 120, 26, 1, "3"),
    ("samina", 122, 2, 1, "3"),
    ("samina", 123, 0, 2, "5d"),
    ("samina", 126, 1, 1, "5d"),
    ("samina", 131, 3, 1, "5a"),
    ("samina", 132, 3, 1, "3"),
    ("samina", 133, 0, 1, "5b"),
    ("samina", 135, 0, 1, "5d"),
    ("samina", 136, 0, 2, "5b"),
    ("samina", 137, 1, 2, "5a"),
    ("samina", 139, 0, 2, "2"),
    ("samina", 140, 0, 1, "5b"),
    ("samina", 144, 2, 2, "5b"),
    ("samina", 147, 1, 2, "5a"),
    ("samina", 148, 0, 1, "5a"),
    ("samina", 149, 1, 1, "3"),
    ("samina", 153, 6, 1, "3"),
    ("samina", 154, 4, 2, "3"),
    ("samina", 157, 1, 1, "5a"),
    ("samina", 158, 1, 1, "3"),
    ("samina", 159, 1, 1, "3"),
    ("samina", 163, 0, 1, "5a"),
    ("samina", 164, 0, 1, "5a"),
    ("samina", 165, 0, 2, "3"),
    ("samina", 172, 0, 1, "5b"),
    ("samina", 174, 0, 1, "5a"),
    ("samina", 179, 2, 1, "5a"),
    ("samina", 186, 0, 1, "2"),
    ("samina", 187, 0, 1, "3"),
    ("samina", 190, 0, 2, "5b"),
    ("samina", 193, 0, 1, "5b"),
    ("samina", 194, 0, 1, "5d"),
    ("samina", 196, 1, 1, "5a"),
    ("samina", 198, 0, 1, "5d"),

    # === Mahsa Amini (Nabi Asli) — 200 comments ===
    ("mahsa", 3, 41, 2, "5a"),  # alt origin hadith story
    ("mahsa", 6, 2, 2, "5a"),
    ("mahsa", 10, 7, 2, "2"),  # Surah al-Ahzab quoted
    ("mahsa", 18, 1, 2, "5a"),
    ("mahsa", 50, 0, 1, "5a"),  # linguistic etymology jilbab/khimar
    ("mahsa", 59, 2, 2, "5a"),
    ("mahsa", 60, 3, 2, "5a"),
    ("mahsa", 63, 11, 2, "5a"),
    ("mahsa", 69, 0, 1, "5b"),  # ex-Muslim mom
    ("mahsa", 84, 0, 1, "1"),  # "origin is Judaism" — pre-Islamic pattern
    ("mahsa", 86, 1, 1, "2"),  # "due to Umar"
    ("mahsa", 90, 0, 2, "1"),  # Zoroastrian Makhbana
    ("mahsa", 118, 2, 1, "2"),  # Q. 33:59 + Umar critique
    ("mahsa", 129, 1, 2, "5a"),  # alt origin theory
    ("mahsa", 143, 0, 2, "5a"),  # Bukhari critique
    ("mahsa", 144, 2, 1, "5a"),  # hadith demand
    ("mahsa", 150, 2, 2, "5b"),  # ex-Muslim
    ("mahsa", 171, 2, 2, "1"),  # French archaeology Mecca
    ("mahsa", 182, 0, 1, "1"),  # pre-Islamic Arab burial of girls + hijab

    # === Histrionics (Brut India) — 200 comments ===
    ("hist", 1, 1, 2, "2"),  # Sahih Bukhari 146 — Umar + Q. 33:59
    ("hist", 4, 0, 2, "2"),  # same
    ("hist", 10, 0, 1, "5b"),
    ("hist", 11, 0, 1, "5a"),  # "no hijab in golden age" + linguistic
    ("hist", 14, 1, 2, "2"),
    ("hist", 17, 0, 1, "5a"),  # "1980 forced... Whole Decency not Taboo Head Scarf"
    ("hist", 18, 0, 1, "5b"),
    ("hist", 31, 0, 1, "1"),  # "Persians veiling long before Islam"
    ("hist", 33, 0, 2, "2"),  # Q. 33:59 + Umar peeping
    ("hist", 37, 1, 1, "1"),  # "creation of patriarchy... slave/free distinction" — EXACT thesis match!
    ("hist", 39, 0, 1, "5b"),
    ("hist", 44, 1, 1, "5d"),
    ("hist", 46, 1, 1, "1"),  # repost of [37]
    ("hist", 55, 0, 1, "5d"),
    ("hist", 56, 0, 1, "5d"),
    ("hist", 71, 1, 2, "5b"),
    ("hist", 73, 1, 1, "1"),  # "Mary wearing Hijab before Islam... Abrahamic"
    ("hist", 78, 0, 1, "3"),  # defends named-scholar tradition
    ("hist", 81, 3, 2, "5b"),
    ("hist", 82, 0, 2, "5b"),
    ("hist", 87, 1, 1, "5a"),  # Q. 24:30, 24:31 + khimar
    ("hist", 97, 0, 2, "5a"),
    ("hist", 100, 1, 2, "5b"),
    ("hist", 101, 0, 1, "1"),  # Rig Veda + Hindu cross-religion pattern
    ("hist", 105, 2, 1, "4"),  # Afghan vs India modern parallel
    ("hist", 111, 1, 2, "2"),
    ("hist", 114, 9, 1, "5b"),  # "not all choose hijab, some forced"
    ("hist", 117, 1, 2, "2"),  # Q. 33:59 quoted
    ("hist", 141, 20, 1, "1"),  # "2000 yrs old, Mary, Indian + European, khimar" — HUGE
    ("hist", 154, 0, 1, "5b"),
    ("hist", 173, 2, 2, "5a"),  # Q. 24:31
    ("hist", 175, 153, 1, "2"),  # Q. 33:59 + jilbab full defense — VIRAL!
    ("hist", 176, 7, 1, "5b"),
    ("hist", 183, 7, 1, "5b"),
    ("hist", 184, 28, 2, "5b"),
    ("hist", 189, 16, 1, "5b"),
    ("hist", 193, 11, 2, "5b"),  # off-topic patriotism but agency-related

    # === Imam Hussein TV — 47 comments ===
    ("imam", 1, 0, 1, "5d"),  # "men tighten hijab as control + duplicity" — KEY
    ("imam", 3, 1, 2, "2"),  # Sahih Bukhari 146
    ("imam", 6, 0, 2, "1"),  # 1 Corinthians 11:5-6
    ("imam", 7, 0, 2, "1"),
    ("imam", 9, 1, 1, "1"),  # "copied from Hinduism"
    ("imam", 15, 2, 1, "2"),  # Q. 33:59 + Umar + slave/free DEEP — exact Beat 1!
    ("imam", 28, 3, 1, "5a"),  # "no veiling in Quran or Hadiths"
    ("imam", 29, 0, 2, "2"),
    ("imam", 32, 1, 1, "2"),  # "designed by Umar (Bukhari 146)"
]

# Aggregate
buckets = {"1": [], "2": [], "3": [], "4": [], "5a": [], "5b": [], "5c": [], "5d": [], "5e": []}
for vid, idx, likes, tier, bucket in data:
    score = tier_weight(tier) * like_mult(likes)
    buckets[bucket].append({"video": vid, "idx": idx, "likes": likes, "tier": tier, "score": score})

# Per-bucket summary
print("\n=== BUCKET SCORES ===")
print(f"{'Bucket':<6} {'T1#':>4} {'T2#':>4} {'WeightedScore':>15}")
print("-" * 32)
totals = {}
for bk, items in buckets.items():
    t1 = sum(1 for i in items if i["tier"] == 1)
    t2 = sum(1 for i in items if i["tier"] == 2)
    wsum = sum(i["score"] for i in items)
    totals[bk] = {"t1": t1, "t2": t2, "score": wsum}
    print(f"{bk:<6} {t1:>4} {t2:>4} {wsum:>15.1f}")

in_scope_score = totals["1"]["score"] + totals["2"]["score"] + totals["3"]["score"] + totals["4"]["score"]
out_scope_score = totals["5a"]["score"] + totals["5b"]["score"] + totals["5c"]["score"] + totals["5d"]["score"]
total_score = in_scope_score + out_scope_score + totals["5e"]["score"]

print(f"\n=== TOTALS ===")
print(f"In-scope (1+2+3+4): {in_scope_score:.1f}")
print(f"Out-scope (5a+5b+5c+5d): {out_scope_score:.1f}")
print(f"5e (filtered debate-bait): {totals['5e']['score']:.1f}")
print(f"Grand total weighted score: {total_score:.1f}")

# === VERDICT TRIGGERS ===
print(f"\n=== VERDICT TRIGGERS ===")

# T1: any 5a/5b/5c/5d sub-bucket >=12 AND >=2x lowest in-scope bucket
in_scope_buckets = ["1", "2", "3", "4"]
lowest_in_scope_score = min(totals[b]["score"] for b in in_scope_buckets)
print(f"Lowest in-scope bucket score: {lowest_in_scope_score:.1f}")

t1_fires = []
for sub in ["5a", "5b", "5c", "5d"]:
    sub_score = totals[sub]["score"]
    if sub_score >= 12 and sub_score >= 2 * lowest_in_scope_score:
        t1_fires.append((sub, sub_score))
print(f"T1 fires: {t1_fires if t1_fires else 'NO'}")

# T2: out-scope >= in-scope
t2_fires = out_scope_score >= in_scope_score
print(f"T2 fires (out>=in): {t2_fires} (out={out_scope_score:.1f} vs in={in_scope_score:.1f})")

# Inconclusive
inconclusive = total_score < 25
print(f"Inconclusive (total<25): {inconclusive}")

# Confirm
confirm = in_scope_score >= 2 * out_scope_score
print(f"Confirm (in>=2*out): {confirm}")

# Save data for report
with open("scoring_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "buckets": buckets,
        "totals": totals,
        "in_scope_score": in_scope_score,
        "out_scope_score": out_scope_score,
        "total_score": total_score,
        "lowest_in_scope_score": lowest_in_scope_score,
        "t1_fires": t1_fires,
        "t2_fires": t2_fires,
        "inconclusive": inconclusive,
        "confirm": confirm,
    }, f, indent=2)

print("\nSaved scoring_results.json")
