# Adwa #39 — Research Synthesis (Comment-Mine + VidIQ + Gap Analysis)

**Date:** 2026-05-10
**Status:** Pre-comment-mine (competitor list locked, VidIQ done, yt-dlp run pending)
**Slot:** 4 in plan `~/.claude/plans/jiggly-sniffing-shamir.md`. Title locks AFTER post-Slot-1 learning gate (Mon ~05-25).
**Scope:** Inputs needed for ADR-0003-compliant title lock + script-pass refinements.

---

## 1. Competitor video set (Gemini Flash output)

Top 4 videos covering Treaty of Wuchale / Battle of Adwa space. Mix of angles per `/comment-mine` step 1.

| # | Title | Channel | Video ID | Views | Angle |
|---|---|---|---|---|---|
| 1 | How did Italy Lose to Ethiopia? (1895) \| Animated History | The Armchair Historian | `1Hln0GjuUQk` | 1,682,721 | military-tactics |
| 2 | The Battle of Adwa - Africa's Unbreakable Victory (Ethiopia) | History Journo | `DzclxJ3xMbc` | 338,159 | mainstream-documentary |
| 3 | Kings of Solomon - The Battle of Adwa - Ethiopian Empire - Part 6 | Extra History | `HI5A_2DKm_0` | 297,086 | history-survey |
| 4 | The Ethiopian Empress Behind Ethiopia's Victory Over Italy | HomeTeam History | `HNQGzlI1N5M` | 39,016 | revisionist |

**Gap identified by Gemini:**
> "While these videos cover the tactical blunders and the symbolic victory, none offer a forensic, 'legal-thriller' style debunking that treats the Article 17 mistranslation specifically as a case of intentional diplomatic forgery and explores the ensuing political trials in Italy."

**Differentiation lane for #39:** Forensic close-read of Article 17 (Italian vs. Amharic side-by-side) + the Italian political fallout (Crispi government collapse). The script's existing HEIST framing already aligns with this lane. Reinforces the slot 4 title direction.

---

## 2. VidIQ keyword findings

Two terms carry the discoverable search volume; everything else zero-volume. Per playbook, rank on broad term, deliver mechanism reveal in script.

| Keyword | Monthly Volume | Competition | Overall Score | Tier | Role |
|---|---|---|---|---|---|
| **battle of adwa** | **7,877** | 29.5 | **63** | 1 | **Title anchor** (lead) |
| first italo ethiopian war | 4,501 | 33.3 | 59 | 3 | Description/tags secondary |
| menelik ii ethiopia | 0 | 7.0 | 37 | 3 | Tag — near-zero competition |
| treaty of wuchale | 0 | 19.8 | 32 | 1 | Tag |
| article 17 wuchale | 0 | 23.3 | 31 | 4 | Tag (semantic depth signal) |
| adwa 1896 | 0 | 25.5 | 30 | 1 | Tag |
| ethiopia defeats italy | 0 | 33.5 | 27 | 3 | Tag |
| italo ethiopian war | 0 | 36.7 | 25 | 1 | Tag |

ADR-0003 mechanism candidates (Tier 2: treaty mistranslation / treaty fraud / two languages / etc.) all returned zero volume with no competition data. Use verbatim in **script narration and description prose** — semantic depth signal to algorithm, not discovery anchor.

---

## 3. Title decision constraints

**Must satisfy:**

- ADR-0003: explicit mechanism word for non-specialist
- Auditor's Edge: technically defensible (no "forged" — primary issue is *deliberate translation discrepancy + false-equivalence clause*, not document fabrication)
- VidIQ: front-load search anchor "battle of adwa" or pair "battle of adwa" + "wuchale" so YouTube indexes both
- Channel pattern: 1-2 sentences, no colon, no year in title, mechanism word does the work
- Script alignment: HEIST framing already locked in `ROUGH-STRUCTURE.md`

**Three candidates that hit all four constraints:**

| # | Candidate | Anchor placement | Mechanism word | 2-sentence pattern |
|---|---|---|---|---|
| **A** | **"The Battle of Adwa Started With a Translation Italy Wrote on Purpose."** | front | "Wrote on purpose" (implicit forgery via deliberateness) | single sentence — VARIANT of Somaliland-style |
| **B** | **"Italy Rigged the Wuchale Treaty. Ethiopia Won the Battle of Adwa."** | back (2nd sentence) | "Rigged" (sharp + accurate) | classic 2-sentence pattern matching 2026 winners |
| **C** | **"The Battle of Adwa Was Caused by a Treaty Italy Wrote in Two Different Languages."** | front | implicit (two languages — most accurate, plain-English) | single sentence |

**My recommendation:** **B**. Two-sentence pattern matches the 2026 winners (Berlin Conference 439v / Tordesillas 788v / 229 Ethnic Groups 439v all 2-sentence with mechanism leading). "Rigged" is technically defensible (deliberate textual divergence is a form of rigging the deal) and sharper than "translation discrepancy." "Battle of Adwa" anchor lands in the second sentence — YouTube will index both segments. "Wuchale Treaty" rounds out the topic-tag set.

**Risk on B:** "Rigged" is an English idiom; some viewers may parse it as colloquial. Mitigation: in the script, the on-screen Article 17 split-screen does the technical heavy-lifting — the title's job is to get the click, the script's job is to deliver the proof.

**Backup if B feels off:** A. "Wrote on Purpose" is more documentary-channel voice but pushes the search anchor to position #1 which is the conservative VidIQ play.

---

## 4. Comment-mine kickoff (yt-dlp commands ready to run)

Per `/comment-mine` step 2. Run these from the project comment-mining folder.

**Setup (once):**
```powershell
cd "D:\History vs Hype\video-projects\_IN_PRODUCTION\39-adwa-wuchale-2026\_research"
mkdir comment-mining -Force
cd comment-mining
```

**Run yt-dlp on 4 videos sequentially (avoid rate limits):**
```powershell
$videos = @("1Hln0GjuUQk", "DzclxJ3xMbc", "HI5A_2DKm_0", "HNQGzlI1N5M")
foreach ($id in $videos) {
    yt-dlp --skip-download --write-comments --write-info-json `
      --extractor-args "youtube:max_comments=50" `
      "https://www.youtube.com/watch?v=$id"
    Start-Sleep -Seconds 2
}
```

**Then extract to plain text (per `/comment-mine` step 3):**
```python
# Save as extract_comments.py in the comment-mining folder
import json

videos = [
    ("1Hln0GjuUQk", "1.68M — Armchair Historian, military-tactics"),
    ("DzclxJ3xMbc", "338K — History Journo, mainstream-doc"),
    ("HI5A_2DKm_0", "297K — Extra History, history-survey"),
    ("HNQGzlI1N5M", "39K — HomeTeam History, revisionist"),
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

with open("comments-extracted.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
print(f"Done → comments-extracted.txt ({len(output)} lines)")
```

```powershell
python extract_comments.py
```

---

## 5. Comment categorization angles to test (per `/comment-mine` step 4)

When you have `comments-extracted.txt`, count signal occurrences for these angles. Decision rule: angle with most signals wins, but channel-formula-repeat risk is a soft veto.

| Angle | Description | Signals to count |
|---|---|---|
| **Forensic close-read** (current locked angle) | Article 17 split-screen, deliberate mistranslation, intentional forgery framing | comments asking "what did Article 17 actually say?", "translation difference?", "did Italy do it on purpose?" |
| **Italian political fallout** | Crispi government collapse, Italian press response, public trials | comments about "what happened to Crispi", "did anyone go to jail in Italy?", "how Italians reacted" |
| **African pride / symbolic victory** | Adwa as anti-colonial pride moment, Pan-Africanism inheritance | comments centering Black/African pride, Marcus Garvey references, "first African victory" |
| **Menelik II tactical genius** | Diplomatic playbook (France/Russia weapons), military strategy | comments about Menelik's playing-Europeans-off, weapons procurement, military tactics |
| **Empress Taitu** | Often-erased role of Empress Taitu Betul in negotiation + battle | comments specifically calling out Taitu, surprise that she's not more famous |

**Expected outcome:** Forensic close-read (current locked angle) should win OR tie with one other. If Italian political fallout has 2x+ signals over forensic, expand the script's §6/§7 (currently light on Italian-side fallout) before lock. If Empress Taitu has 2x+ signals, that's a separate-video signal, not a script revision — note for slot 5+ planning.

---

## 6. Decision gates (in order)

1. **Run yt-dlp + extract_comments.py** (~5 min)
2. **Categorize 200 comments** (~30 min, manual or assisted)
3. **Apply angle decision** to script — keep current HEIST framing if forensic wins, augment if other angle has signal cluster
4. **Wait for post-Slot-1 learning gate** (Mon ~05-25) — Inquisition's 48-72h retention/CTR data
5. **Lock title** — apply ADR-0003 + Auditor's Edge + VidIQ anchor + comment-mine angle output. Document rationale in `PROJECT-STATUS.md`
6. **Move rough structure → full script**, run 90% verified-research gate
7. **Modern-claim freshness check** (Tigray war 2020-22 / AU on colonial-era treaty validity / Italy-Ethiopia bilateral 2024-2026) — defer to film time, similar to how Hijab #52 was handled
8. **Film, edit, B-roll**, ship target ~2026-06-06

---

## 7. Recommended metadata stack (post-title-lock)

Based on VidIQ findings:

- **Title anchor:** `battle of adwa` (front or second sentence)
- **Description first paragraph:** include `first italo ethiopian war` + `treaty of wuchale` + `article 17` verbatim
- **Tags:** `battle of adwa`, `first italo ethiopian war`, `menelik ii ethiopia`, `treaty of wuchale`, `article 17 wuchale`, `ethiopia defeats italy`, `adwa 1896`, `italo ethiopian war`
- **ADR-0003 / Auditor's Edge phrasing in description prose:** "treaty mistranslation," "two languages said different things," "false-equivalence clause," "rigged"

---

## Cross-references

- Plan: `~/.claude/plans/jiggly-sniffing-shamir.md` (slot 4)
- ADR: `D:\History vs Hype\docs\adr\0003-parties-with-mechanism-title-rule.md`
- Project status: `PROJECT-STATUS.md` (working title currently OPEN)
- Rough structure: `ROUGH-STRUCTURE.md` (heist framing, Article 17 split-screen centerpiece)
- Verified research: `01-VERIFIED-RESEARCH.md`
- Script draft: `02-SCRIPT-DRAFT.md`
- Tooling: `.claude/commands/comment-mine.md`, `tools/discovery/vidiq_workflow.py`
