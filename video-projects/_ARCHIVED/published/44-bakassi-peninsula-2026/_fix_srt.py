"""Clean bakassi.srt for YouTube upload.

Fixes:
1. Strip <b> tags
2. Drop duplicate/artifact entries (duration < 300ms OR near-identical text to next entry)
3. Subtract 1 hour from all timestamps (01:00:00 → 00:00:00)
4. Fix transcription typos (name misspellings, hallucinated words)
5. Renumber sequentially
"""
import re
from pathlib import Path

SRC = Path(__file__).parent / "bakassi.srt"
OUT = Path(__file__).parent / "bakassi_youtube.srt"

TYPO_FIXES = {
    # Bakassi / place names
    r"\bBacchus\b": "Bakassi",
    r"\bBagasthi\b": "Bakassi",
    r"\bBaccasi\b": "Bakassi",
    r"\bPakistan Peninsula\b": "Bakassi Peninsula",
    r"\bPakistan\b": "Bakassi",
    r"\bPakua\b": "Akwa",
    r"\bCaparoon\b": "Cameroon",
    r"\bcamel them\b": "Cameroon",
    r"\bCanon\b": "Cameroon",
    # People
    r"\bPhouon\b": "Gowon",
    r"\bGowon\breached": "Gowon reached",
    r"\bEkanem Essin\b": "Ekanem Esin",
    r"\bHyde-Hewitt\b": "Hyde Hewett",
    r"\bPete Gornings\b": "Piet Konings",
    r"\bGornings\b": "Konings",
    r"\bOren Galu\b": "Odinkalu",
    r"\bChidi Oren Galu\b": "Chidi Odinkalu",
    r"\bNorth Salisbury\b": "Lord Salisbury",
    # Latin / legal terms
    r"\bPachta Sun Cervanda\b": "pacta sunt servanda",
    r"\bBaktesun Servanda\b": "pacta sunt servanda",
    # Transcription hallucinations
    r"\blions drawn by men\b": "lines drawn by men",
    r"\bepic city-states\b": "Efik city-states",
    r"\bepic city states\b": "Efik city-states",
    r"\b1933 Chinese States\b": "1913 treaty states",
    r"\bGreen Tree\b": "Greentree",
    r"\bLigolimba\b": "legal limbo",
    r"\bahead of state\b": "a head of state",
    r"\bhope myself responsible\b": "hold myself responsible",
    r"\bnotion boundary\b": "ocean boundary",
    r"\b\"I is cold\"\b": "ice cold",
    r"\bI is cold\b": "ice cold",
    r"\bplan inside\b": "plebiscite",
    r"\bbelow to\b": "belong to",
    r"\bancientists flirted\b": "HMS Flirt",
    r"\bmarch 1984\b": "March 1994",
    r"\bMarch 1984\b": "March 1994",
    r"\bDecember 1884, ten\b": "December 1894, 10",
    r"\beliminate the contract\b": "terminate the contract",
    r"\bgeometry stretch\b": "kilometer stretch",
    r"\bfavourite, protection\b": "favour and protection",
    r"\bfavorite, protection\b": "favour and protection",
    r"\belected Germany\b": "handed the land to Germany",
    r"\bno vote for sending\b": "without local consent",
    # Standalone fixes
    r"\bmoved a powerful federation\b": "ruled a powerful federation",
    r"\b3-4-3-3, goon\b": "3433, Gowon",
    r"\bthousands-word\b": "thousand square",
    # Single-word typos in split-line contexts
    r"\bwhen lions\b": "when lines",
    r"\bdetached deficiency\b": "detached efficiency",
    r"\balmost detached deficiency\b": "almost detached efficiency",
    r"\bepic city\b": "Efik city",
}


def parse_srt(text: str):
    """Parse SRT into list of (start_ms, end_ms, text) tuples."""
    entries = []
    blocks = re.split(r"\n\s*\n", text.strip())
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        time_match = re.match(
            r"(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)", lines[1]
        )
        if not time_match:
            continue
        h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, time_match.groups())
        start = h1 * 3600000 + m1 * 60000 + s1 * 1000 + ms1
        end = h2 * 3600000 + m2 * 60000 + s2 * 1000 + ms2
        content = "\n".join(lines[2:])
        entries.append([start, end, content])
    return entries


def strip_bold(text: str) -> str:
    return re.sub(r"</?b>", "", text)


def apply_typo_fixes(text: str) -> str:
    for pattern, replacement in TYPO_FIXES.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def text_similarity(a: str, b: str) -> float:
    """Rough word-overlap ratio."""
    wa = set(re.findall(r"\w+", a.lower()))
    wb = set(re.findall(r"\w+", b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


FRAGMENT_END_WORDS = {
    "a", "an", "the", "of", "to", "from", "in", "on", "at", "and", "or", "but",
    "for", "with", "as", "is", "was", "are", "were", "be", "been", "by",
    "that", "this", "these", "those", "he", "she", "it", "they", "we",
}


def word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


def ends_cleanly(text: str) -> bool:
    """True if text ends with terminal punctuation or has a complete feel."""
    stripped = text.strip().rstrip('"').rstrip("'").rstrip(",")
    if not stripped:
        return False
    if stripped[-1] in '.!?":':
        return True
    # Does it end with a fragment word?
    last_word = re.findall(r"\w+", stripped.lower())
    if last_word and last_word[-1] in FRAGMENT_END_WORDS:
        return False
    return True


def dedupe(entries):
    """Drop artifact entries. Rules:
    1. Drop standalone short entries (duration < 300ms).
    2. For consecutive near-duplicates (similarity >= 0.6, gap < 700ms),
       keep the entry with MORE WORDS (fuller transcription).
    3. For identical text back-to-back, keep the first occurrence only.
    """
    # Pass 1: drop short artifacts
    alive = [e for e in entries if (e[1] - e[0]) >= 300]

    # Pass 2: iteratively collapse near-duplicates
    changed = True
    while changed:
        changed = False
        kept = []
        i = 0
        while i < len(alive):
            cur = alive[i]
            if i + 1 < len(alive):
                nxt = alive[i + 1]
                sim = text_similarity(cur[2], nxt[2])
                gap = nxt[0] - cur[1]
                # Also check if first 3 words match — catches "Fast forward 30 years" + "Fast forward 30 years, removed from the"
                cur_words_list = re.findall(r"\w+", cur[2].lower())
                nxt_words_list = re.findall(r"\w+", nxt[2].lower())
                first_words_match = (
                    len(cur_words_list) >= 3
                    and len(nxt_words_list) >= 3
                    and cur_words_list[:3] == nxt_words_list[:3]
                )
                if (sim >= 0.6 or first_words_match) and gap < 700:
                    # Prefer entry that ends cleanly (not mid-fragment)
                    cur_clean = ends_cleanly(cur[2])
                    nxt_clean = ends_cleanly(nxt[2])
                    cur_words = word_count(cur[2])
                    nxt_words = word_count(nxt[2])

                    if cur_clean and not nxt_clean:
                        # Keep cur, drop nxt
                        kept.append(cur)
                        i += 2
                        changed = True
                        continue
                    if nxt_clean and not cur_clean:
                        # Drop cur, keep nxt
                        i += 1
                        changed = True
                        continue
                    # Both clean or both fragments — fall back to word count
                    if nxt_words > cur_words:
                        i += 1
                        changed = True
                        continue
                    elif cur_words > nxt_words:
                        kept.append(cur)
                        i += 2
                        changed = True
                        continue
                    else:
                        # Tie — prefer longer-duration entry
                        if (nxt[1] - nxt[0]) > (cur[1] - cur[0]):
                            i += 1
                            changed = True
                            continue
                        else:
                            kept.append(cur)
                            i += 2
                            changed = True
                            continue
            kept.append(cur)
            i += 1
        alive = kept
    return alive


def format_time(ms: int) -> str:
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    msec = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{msec:03d}"


def main():
    src_text = SRC.read_text(encoding="utf-8")
    entries = parse_srt(src_text)
    print(f"Parsed {len(entries)} raw entries")

    # Strip bold tags and normalize typos BEFORE dedup so variant spellings
    # of the same word (e.g. "Pachta Sun Cervanda" vs "Baktesun Servanda")
    # collapse and get caught by similarity check.
    for e in entries:
        e[2] = apply_typo_fixes(strip_bold(e[2]).strip())

    # Dedupe on normalized text
    entries = dedupe(entries)
    print(f"After dedup: {len(entries)} entries")

    # Subtract 1 hour (offset 3,600,000 ms)
    ONE_HOUR = 3600000
    for e in entries:
        e[0] -= ONE_HOUR
        e[1] -= ONE_HOUR

    # Write output
    out_lines = []
    for idx, (start, end, text) in enumerate(entries, 1):
        out_lines.append(str(idx))
        out_lines.append(f"{format_time(start)} --> {format_time(end)}")
        out_lines.append(text)
        out_lines.append("")

    OUT.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Wrote {OUT.name} with {len(entries)} entries")
    print(f"First entry: {format_time(entries[0][0])} - {entries[0][2][:60]}")
    print(f"Last entry:  {format_time(entries[-1][1])} - {entries[-1][2][:60]}")


if __name__ == "__main__":
    main()
