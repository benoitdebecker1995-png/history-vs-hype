"""
Voice Lint — deterministic voice-violation scanner for History vs Hype scripts.

Flags the creator's known cringe patterns in a SCRIPT.md (or glob) BEFORE the
read-aloud gate, so the human read-aloud is freed to catch substance (logic,
structure, attribution) instead of surface tics.

⚠️  SOURCE OF TRUTH: the rules below are transcribed from
    `.claude/REFERENCE/VOICE-PROFILE.md` (the "Cringe no-list" + "NOT cringe"
    sections, picks-validated `/voice-discovery` 2026-06-05) AND from
    `VOICE-PROFILE.md` §"Adversarial drift audit (Fable Phase 2, 2026-06-11)"
    AND from `channel-data/calibration/FINGERPRINT-UNSCRIPTED.md` §9
    (quantitative thresholds, S12 2026-06-12 — single-sample start values, so
    everything fingerprint-derived ships WARN/REVIEW, never HARD).
    When the profile changes, update RULES here to match. This tool does NOT
    invent voice rules — it mechanizes the profile's hard "no" list so the
    linter stays in lockstep with the canonical fingerprint.

    2026-07-19 sync (LLM-CRAFT-UPGRADE-PLAN.md D1): applied the two
    corrections VOICE-PROFILE.md ~line 505 staged from the #62 generative
    (_adlib/) corpus — "understand-go-back" (T7) demoted HARD -> WARN-with-
    exception (scan_understand_go_back), and "Now," excepted from
    "youtuber-opener" (only the empty "Now —" camera-turn stays banned).

Severity:
    HARD   — a profile "hard no". Non-zero exit. Must be fixed before lock.
    WARN   — dispreferred device (profile: "use sparingly / 1x max"). Advisory.
    REVIEW — heuristic transition check. Never fails the run; flags handoffs
             for a human glance (transitions are the creator's #1 weakness).

Usage:
    python -m tools.voice_lint path/to/SCRIPT.md
    python -m tools.voice_lint "video-projects/**/SCRIPT.md"
    python -m tools.voice_lint SCRIPT.md --no-transitions   # skip transition audit
    python -m tools.voice_lint SCRIPT.md --quiet            # summary only

Exit code: 0 if no HARD findings, 1 if any HARD finding (CI / pre-lock gate).
"""

import argparse
import glob as globmod
import re
import sys
from pathlib import Path
from typing import Optional


# =============================================================================
# RULES — transcribed from VOICE-PROFILE.md "Cringe no-list" (hard "no")
# Each rule: id, severity, kind ('literal'|'regex'), pattern, fix.
# Literal patterns are matched case-insensitively with word boundaries.
# =============================================================================

HARD_LITERALS = [
    # (id, phrase, fix)
    ("buckle-up", "buckle up", "Cut — gimmick hype opener. Open famous-then-puncture instead."),
    ("guess-what", "guess what", 'RETIRED gimmick. Use "the part almost everyone gets wrong" / "Except none of that is the real story."'),
    ("guess-who", "guess who", 'RETIRED gimmick. Name the subject plainly in a full causal sentence.'),
    ("stay-with-me", "stay with me", "Cut — viewer-instruction filler. Trust the beat."),
    ("the-receipt", "the receipts?", 'Internet-era phrase. Say what the document shows: "the treaty says…".'),
    ("play-their-game", "let's play their game", "Cut — gimmick framing."),
    ("keep-both-in-head", "keep both in your head", "Cut viewer-instruction framing. State the two facts and let them hit."),
    ("dark-twist", "there's a dark twist", "Cut — telegraphs melodrama. Let the fact land plainly."),
    ("almost-no-video", "here's what almost no video", "Cut meta-framing opener. Open on the concrete thing itself."),
]

HARD_REGEXES = [
    # (id, pattern, fix, ignorecase)
    # ignorecase defaults to True; set False where letter-case is load-bearing
    # (e.g. a proper noun / place name distinguishes the anti-voice from innocent prose).
    ("compressed-reveal", r"\b(one|two) words?:", 'Compressed clever reveal — cringe. Use a full causal sentence: "…because there was something it wanted more: Mosul."', True),
    # Case-sensitive object: "erased the Kurds" / "erased the <ProperNoun>" — NOT "erased the one detail".
    ("erased-the", r"\b[Ee]rased the (Kurds|[A-Z]\w+)", 'Lexical flag — prefer "wrote them out" / "wrote them out of the story".', False),
    ("decade-scene-drop-goback", r"\bgo back to the \d{4}s\b", "Present-tense decade scene-drop is NOT his. Era-framing stays past tense (present only for a single dramatic MOMENT).", True),
    ("decade-scene-drop-its", r"\bit'?s the \d{4}s\b", "Present-tense decade scene-drop is NOT his. Era-framing stays past tense (present only for a single dramatic MOMENT).", True),
    # Case-sensitive place name after "the size of" — the RealLifeLore atlas move
    # ("the size of Texas"), NOT a relative comparison ("three times the size of his own").
    ("scale-size-of", r"\b[Tt]he size of (?:a |an |the )?[A-Z]\w+", "Forced scale comparison (RealLifeLore — his explicit anti-voice). State the plain figure.", False),
    ("scale-population-of", r"\broughly the population of\b", "Forced scale comparison (anti-voice). State the plain figure.", True),
    ("scale-more-people", r"\bmore people than (lived|live) in\b", "Forced scale comparison (anti-voice). State the plain figure.", True),
    ("scale-looking-back", r"\bthat'?s like looking back at\b", "Forced time comparison reflex. Drop it or make it do real argumentative work (article-side only).", True),
    ("melodrama-darker", r"\bit (gets?|got) darker\b", "Melodrama escalation-telegraph (same family as 'there's a dark twist'). State the next atrocity plainly; don't pre-announce the tone.", True),
    ("darkest-chapter", r"\bthe darkest (chapter|part|day)\b", "Melodrama telegraph. State the event plainly, let it land.", True),
    # --- Fable Phase 2 rules (2026-06-11): generic-AI tells ---
    ("agenda-announce", r"\bwe'?re going to (answer|explore|break down|dive into|look at)\b", "Agenda announcement — generic-AI opener. Start on the substance (bar-talk test #2); the question is shown by answering it.", True),
    ("changed-everything", r"\bchanged everything\b", '"X changed everything" — AI hinge cliché. Name what actually changed, concretely.', True),
    ("heres-the-thing", r"\bhere'?s the thing\b", "Meta-framing throat-clear. Delete; say the thing.", True),
    ("heres-why-standalone", r"\b[Aa]nd here'?s why\b|\bhere'?s why[.:]", "\"Here's why\" announcement — the zoom-out must be invisible (bar-talk #2). Walk into the cause with \"because/so\".", True),
    ("comment-bait", r"\blet me know in the comments\b", "Engagement-bait CTA — not his register. CTA = value-CTA (\"go to the document\"), earned by the prior beat.", True),
    ("love-your-thoughts", r"\bI'?d love to hear your thoughts\b", "Engagement-bait CTA. Cut.", True),
    ("tragedy-of", r"\bthe tragedy of\b", "Melodrama telegraph (family: dark-twist / darkest-chapter). State the event plainly, let it land.", True),
    ("isnt-just-its", r"\bisn'?t just [^.!?]{0,60}— it'?s\b", "\"isn't just X — it's Y\" escalation-correction tic (AI default). One claim, stated directly.", True),
    # "understand-go-back" DEMOTED from HARD to WARN-with-exception, 2026-07-19
    # (VOICE-PROFILE.md ~line 505: his 2026-07-15 _adlib/ ad-libs open causal
    # chains with exactly this phrasing, unprompted — the prerequisite-chain
    # doorway IS his native move. See scan_understand_go_back() below.)
    ("ghost-hangs", r"\b(ghost|shadow|weight) of [^.!?]{0,40}(hangs|hung|looms|loomed)\b", "Abstraction-as-agent poetry — purple prose, anti-voice. Cut or replace with a concrete fact.", True),
    ("population-compare", r"\bmore than the (entire )?population of\b", "Forced scale comparison (anti-voice family; closes a gap in the existing scale-* rules). State the plain figure.", True),
]

WARN_LITERALS = [
    # (id, phrase, fix, max_allowed) — flagged only when count exceeds max_allowed
    ("gets-interesting", "here's where it gets interesting", '"here\'s where it gets interesting" is OK 1x max — you have more than one.', 1),
]

WARN_ALWAYS = [
    # (id, phrase, fix) — dispreferred, flag every occurrence at WARN
    ("think-about-that", "think about that", "Dispreferred filler — prefer letting the fact carry its own weight."),
    ("honest-part", "here's the honest part", 'Meta-framing tic — use a plain emphasis insertion instead ("but — and this is important — …").'),
]

WARN_REGEXES = [
    # (id, pattern, fix, ignorecase) — dispreferred, flag every occurrence at WARN.
    # Fable Phase 2 drift-frequency tells (2026-06-11).
    (
        "sinister-adverb",
        r"\b(quietly|simply|conveniently|neatly|promptly) (erased|junked|vanished|disappeared|dropped|forgotten|ignored|buried)\b",
        "Knowing-narrator wink. State the act plainly and name the agent.",
        True,
    ),
    (
        "scholarly-hedge",
        r"\b(essentially|arguably|in many ways|at its core|in essence|considerable autonomy|considerable independence)\b",
        "Scholarly hedge = model fingerprint. His hedges are colloquial (basically/actually/kind of) — swap or delete.",
        True,
    ),
    # --- v18 calibration (2026-06-12): FINGERPRINT-UNSCRIPTED quantitative rules ---
    (
        "really-intensifier",
        r"\breally\b",
        'His intensifier is "very" (gold: very=9/741w, really=0). Swap or delete.',
        True,
    ),
    (
        # "Now," EXCEPTED 2026-07-19 (VOICE-PROFILE.md ~line 505): his own
        # _adlib/ ad-libs use "Now, it is important to mention…" naturally as a
        # relevance-scaffold opener — that form is his voice, not a tell. Only
        # the empty camera-turn "Now —" (dash, no follow-on content) is banned.
        "youtuber-opener",
        r"(?:^|[.!?]\s+)Look,\s|(?:^|[.!?]\s+)Listen\b[,.]|(?:^|[.!?]\s+)Now\s*(?:—|–|--)\s",
        "YouTuber-opener set (Look,/Listen/empty 'Now —' camera-turn) — absent in gold; he enters thoughts first-person (I/I'm) or with So/And. ('Now,' as a relevance-scaffold opener is his own voice per the _adlib/ corpus — not flagged.)",
        False,
    ),
]

WARN_REGEX_THRESHOLD = [
    # (id, pattern, fix, ignorecase, max_allowed) — flagged only when count exceeds max_allowed.
    # Fable Phase 2 threshold counters (2026-06-11).
    (
        "in-x-words",
        r"\bin (his|her|their|[A-Z][\w]*'?s?) words\b",
        "The 'in X's words' attribution formula ×3+ — the anonymous-attribution crutch (Standing dislike #2). Name the scholar once, let [SHOW] cards carry the rest, vary the frame.",
        True,
        2,  # max_allowed: flag when count > 2 (i.e. ≥3)
    ),
    (
        "triad-density",
        r",\s+[^,.!?]{2,40},\s+and\s+[^,.!?]{2,50}[.!?]",
        "Symmetric-triad garnish over budget (his enumeration is uneven/flowing; cap ~2 outside a declared ledger beat).",
        True,
        3,  # max_allowed: flag when count > 3
    ),
    (
        "colon-reveal-density",
        r'[a-z][^.!?:"]{10,}: [A-Z][^.!?:"]{0,40}[.!?]',
        "Colon-reveal device over budget. Vary the sentence structure.",
        True,
        4,  # max_allowed: ship at 4 to avoid quote-intro false positives
    ),
    # v18 calibration (2026-06-12): gold = 0 occurrences of either; writer's tools to ration.
    (
        "writer-connectors",
        r"\b(which is why|and that meant)\b",
        'Writer-connector density over budget (gold: 0; his causal stack is "so" >> "because"). Ration to <=2 per script.',
        True,
        2,  # max_allowed: flag when count > 2
    ),
]

# NOT cringe — never flag these as HARD (VOICE-PROFILE.md "NOT cringe" list).
# Kept here as documentation; the rules above deliberately exclude them.
NOT_CRINGE = [
    "basically",
    "the system worked exactly as designed",
    "here's where it gets interesting",  # 1x only (handled as WARN-over-threshold)
    "very",  # HIS intensifier (gold: 1.2/100w) — never flag; "really" is the tell
]

# Credential markers for the stacked-credentials detector.
CREDENTIAL_MARKERS = [
    r"\bas [^.]*historian\b",
    r"\bwrites\b",
    r"\bargues\b",
    r"\baccording to\b",
]

# Bridge connectors that signal a thesis-forward / causal transition (PASS heuristic).
BRIDGE_OPENERS = (
    "so", "but", "and", "except", "now", "because", "which", "yet", "still",
)

# Pronoun openers that, across a section reset, usually need a named antecedent.
VAGUE_OPENERS = ("this", "that", "it", "these", "those")


# =============================================================================
# Line / sentence model
# =============================================================================

_INLINE_NOTE = re.compile(r"\[[^\]]*\]")          # [SHOW: …] [SOURCE: …] [G1] etc.
_BOLD = re.compile(r"\*\*([^*]*)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"\w+")

# "To understand X, we/you have to go back…" — WARN-with-exception (demoted
# from HARD 2026-07-19, VOICE-PROFILE.md ~line 505). His own ad-libs open
# causal chains with this exact phrasing when a walked chain follows (a year
# or >=8 more words of the same sentence developing the explanation); it's
# only the AI tissue when the transition is bare/empty. See scan_understand_go_back().
_UNDERSTAND_GO_BACK_RX = re.compile(
    r"\b[Tt]o understand [^.!?]{0,60}[, ]+(you|we) (have|need) to go back\b",
    re.IGNORECASE,
)
_TRAILING_YEAR_RX = re.compile(r"\b\d{3,4}\b")


def _is_structural(raw: str) -> bool:
    """True for lines that are not spoken VO prose (headers, rules, tables, tags)."""
    s = raw.strip()
    if not s:
        return True
    if s.startswith("#") or s.startswith(">") or s.startswith("|"):
        return True
    if set(s) <= set("-= "):  # horizontal rule / divider
        return True
    # Pure stage-direction / metadata lines: strip notes + emphasis, see if empty.
    cleaned = clean_line(raw)
    if not cleaned.strip():
        return True
    # Front-matter style "**Key:** value" project-metadata lines at file top read
    # as prose otherwise; treat a line that is ONLY a bold label + colon as meta.
    if re.match(r"^\*\*[^*]+:\*\*", s):
        return True
    # Whole-line italic = editorial/voice-pass note (e.g. "*▶ VOICE PASS DONE …*",
    # "*B-roll, asset list …*"), not spoken VO. (Inline *a*/*the* emphasis is mid-line.)
    if s.startswith("*") and s.endswith("*") and not s.startswith("**"):
        return True
    return False


_COMMENT_OPEN = "<!--"
_COMMENT_CLOSE = "-->"


def mask_comments(lines: list) -> list:
    """Return lines with HTML-comment content blanked (preserving line indices)."""
    out = []
    in_comment = False
    for raw in lines:
        if in_comment:
            if _COMMENT_CLOSE in raw:
                in_comment = False
                out.append(raw.split(_COMMENT_CLOSE, 1)[1])
            else:
                out.append("")
            continue
        if _COMMENT_OPEN in raw:
            before = raw.split(_COMMENT_OPEN, 1)[0]
            rest = raw.split(_COMMENT_OPEN, 1)[1]
            if _COMMENT_CLOSE in rest:  # single-line comment
                after = rest.split(_COMMENT_CLOSE, 1)[1]
                out.append(before + " " + after)
            else:
                in_comment = True
                out.append(before)
            continue
        out.append(raw)
    return out


def clean_line(raw: str) -> str:
    """Strip inline stage directions + markdown emphasis, leaving spoken text."""
    s = _INLINE_NOTE.sub(" ", raw)
    s = _BOLD.sub(r"\1", s)
    s = _ITALIC.sub(r"\1", s)
    s = s.replace("~~", "")
    return s


def word_count(text: str) -> int:
    return len(_WORD.findall(text))


# =============================================================================
# Finding model
# =============================================================================

class Finding:
    __slots__ = ("file", "line", "severity", "rule", "text", "fix")

    def __init__(self, file, line, severity, rule, text, fix):
        self.file = file
        self.line = line
        self.severity = severity
        self.rule = rule
        self.text = text
        self.fix = fix


# =============================================================================
# Scanners
# =============================================================================

def scan_patterns(file: str, lines: list) -> list:
    """Literal + regex rules, per content line."""
    findings = []
    warn_counts: dict = {}

    # Pre-count WARN-over-threshold literals across the whole file.
    for rule_id, phrase, fix, _max in WARN_LITERALS:
        warn_counts[rule_id] = 0

    # Pre-count WARN-over-threshold regexes across the whole file.
    for rule_id, pat, fix, ic, _max in WARN_REGEX_THRESHOLD:
        warn_counts[rule_id] = 0

    for i, raw in enumerate(lines, 1):
        if _is_structural(raw):
            continue
        text = clean_line(raw)
        low = text.lower()

        # HARD literals
        for rule_id, phrase, fix in HARD_LITERALS:
            rx = re.compile(r"\b" + phrase.replace(" ", r"\s+") + r"\b", re.IGNORECASE)
            m = rx.search(text)
            if m:
                findings.append(Finding(file, i, "HARD", rule_id, m.group(0), fix))

        # HARD regexes
        for rule_id, pat, fix, ic in HARD_REGEXES:
            m = re.search(pat, text, re.IGNORECASE if ic else 0)
            if m:
                findings.append(Finding(file, i, "HARD", rule_id, m.group(0), fix))

        # WARN always (literals)
        for rule_id, phrase, fix in WARN_ALWAYS:
            rx = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
            m = rx.search(text)
            if m:
                findings.append(Finding(file, i, "WARN", rule_id, m.group(0), fix))

        # WARN always (regexes) — Fable Phase 2
        for rule_id, pat, fix, ic in WARN_REGEXES:
            m = re.search(pat, text, re.IGNORECASE if ic else 0)
            if m:
                findings.append(Finding(file, i, "WARN", rule_id, m.group(0), fix))

        # WARN over-threshold literals: record locations, decide after full pass
        for rule_id, phrase, fix, _max in WARN_LITERALS:
            if phrase.lower() in low:
                warn_counts[rule_id] += 1
                findings.append(Finding(file, i, "_WARN_THRESH:" + rule_id, rule_id, phrase, fix))

        # WARN over-threshold regexes: record locations, decide after full pass
        for rule_id, pat, fix, ic, _max in WARN_REGEX_THRESHOLD:
            m = re.search(pat, text, re.IGNORECASE if ic else 0)
            if m:
                warn_counts[rule_id] += 1
                findings.append(Finding(file, i, "_WARN_THRESH:" + rule_id, rule_id, m.group(0), fix))

    # Resolve threshold WARNs: keep only if count exceeds max, else drop.
    # Build a unified lookup: rule_id -> max_allowed
    thresh_cfg: dict = {}
    for rule_id, phrase, fix, max_allowed in WARN_LITERALS:
        thresh_cfg[rule_id] = max_allowed
    for rule_id, pat, fix, ic, max_allowed in WARN_REGEX_THRESHOLD:
        thresh_cfg[rule_id] = max_allowed

    resolved = []
    for f in findings:
        if f.severity.startswith("_WARN_THRESH:"):
            rule_id = f.severity.split(":", 1)[1]
            if warn_counts[rule_id] > thresh_cfg[rule_id]:
                f.severity = "WARN"
                resolved.append(f)
            # else: within allowance, drop silently
        else:
            resolved.append(f)
    return resolved


def _flatten_sentences(lines: list) -> list:
    """Return [(line_no, sentence_text)] over spoken content only."""
    out = []
    for i, raw in enumerate(lines, 1):
        if _is_structural(raw):
            continue
        text = clean_line(raw).strip()
        if not text:
            continue
        for sent in _SENTENCE_SPLIT.split(text):
            sent = sent.strip()
            if sent:
                out.append((i, sent))
    return out


def scan_staccato(file: str, lines: list) -> list:
    """Flag a run of 3+ consecutive sentences each <=4 words (fragment triplet)."""
    findings = []
    sents = _flatten_sentences(lines)
    run = []
    for line_no, sent in sents:
        if word_count(sent) <= 4:
            run.append((line_no, sent))
        else:
            if len(run) >= 3:
                findings.append(_staccato_finding(file, run))
            run = []
    if len(run) >= 3:
        findings.append(_staccato_finding(file, run))
    return findings


def _staccato_finding(file, run):
    first_line = run[0][0]
    joined = " / ".join(s for _, s in run)
    return Finding(
        file, first_line, "HARD", "staccato-triplet", joined,
        "3+ fragment sentences in a row. He picks dash-compound/full-sentence verdicts over staccato. Combine into a flowing sentence.",
    )


def scan_stacked_credentials(file: str, lines: list) -> list:
    """Flag 2+ credential markers within any 4-sentence window."""
    findings = []
    sents = _flatten_sentences(lines)
    rxs = [re.compile(p, re.IGNORECASE) for p in CREDENTIAL_MARKERS]
    reported_windows = set()
    for start in range(len(sents)):
        window = sents[start:start + 4]
        hits = []
        for line_no, sent in window:
            if any(rx.search(sent) for rx in rxs):
                hits.append((line_no, sent))
        if len(hits) >= 2:
            key = hits[0][0]
            if key in reported_windows:
                continue
            reported_windows.add(key)
            joined = " | ".join(f"L{ln}: {s[:50]}" for ln, s in hits)
            findings.append(Finding(
                file, hits[0][0], "HARD", "stacked-credentials", joined,
                'Credentials stacked close together. Bar-talk register names a scholar sparingly — attribute once, crisply, not every beat.',
            ))
    return findings


# =============================================================================
# Negation-correction density scanner (Fable Phase 2, 2026-06-11)
# =============================================================================

_NEG_DASH = re.compile(
    r"\b(wasn'?t|isn'?t|didn'?t|weren'?t)\b[^.!?—]{0,80}—\s*(it was|it'?s|they were|they built|he |she )",
    re.IGNORECASE,
)
_NEG_SENT_END = re.compile(
    r"\b(wasn'?t|isn'?t|didn'?t|weren'?t|never)\b[^.!?]{0,80}[.!?]$",
    re.IGNORECASE,
)
_NEG_SENT_START = re.compile(
    r"^(It|They|He|She|This|That)\s+(was|were|is|are|built|created|stopped|did)\b",
    re.IGNORECASE,
)


def scan_negation_pairs(file: str, lines: list) -> list:
    """Emit one summary WARN when negation-correction count > 4, listing line numbers.

    Counts two forms:
    - Same-sentence dash form: wasn't/isn't/didn't/weren't ... — it was/it's/they were/...
    - Cross-sentence form: sentence ending in negation followed by sentence starting
      with It/They/He/She/This/That + was/were/is/are/built/created/stopped/did.
    """
    sents = _flatten_sentences(lines)
    hit_lines = []

    for idx, (line_no, sent) in enumerate(sents):
        # Same-sentence dash form
        if _NEG_DASH.search(sent):
            hit_lines.append(line_no)
            continue
        # Cross-sentence form: current sentence ends with negation AND next starts with affirmation
        if _NEG_SENT_END.search(sent) and idx + 1 < len(sents):
            next_sent = sents[idx + 1][1]
            if _NEG_SENT_START.match(next_sent):
                hit_lines.append(line_no)

    if len(hit_lines) > 4:
        line_list = ", ".join(f"L{n}" for n in sorted(set(hit_lines)))
        return [Finding(
            file, hit_lines[0], "WARN", "negation-correction-density",
            f"negation-correction pairs × {len(hit_lines)} ({line_list})",
            "Negation-correction engine over budget (VOICE-PROFILE T1: A=0, scripts ≈9-15). Keep only EARNED pairs (live myth); state the rest directly.",
        )]
    return []


def scan_understand_go_back(file: str, lines: list) -> list:
    """WARN-with-exception for 'to understand X, we have to go back…' (T7).

    Demoted from HARD 2026-07-19 per VOICE-PROFILE.md ~line 505: his own
    2026-07-15 _adlib/ ad-libs open causal chains with exactly this phrasing,
    unprompted, when a walked chain actually follows — the prerequisite-chain
    doorway IS his native move. Only the bare/empty transition (nothing
    concrete follows) is the AI tissue this rule still catches.

    Exception test: does a year (3-4 digit number) appear within the rest of
    the sentence, OR does the sentence continue for >=8 more words past the
    match? Either signals a walked chain follows — suppress entirely (no
    finding, not even WARN), matching "keep such lines when they're his".
    """
    findings = []
    for line_no, sent in _flatten_sentences(lines):
        m = _UNDERSTAND_GO_BACK_RX.search(sent)
        if not m:
            continue
        tail = sent[m.end():]
        has_year = bool(_TRAILING_YEAR_RX.search(tail))
        tail_words = len(_WORD.findall(tail))
        if has_year or tail_words >= 8:
            continue  # walked chain follows — his voice, not the AI tissue
        findings.append(Finding(
            file, line_no, "WARN", "understand-go-back", m.group(0),
            "Obligatory-journey transition with no walked chain following — bare "
            "AI-tissue form. If it leads into an actual causal walk (a year, or "
            "the explanation continuing), it's his voice and won't fire here; "
            "if it's standing alone, bridge by consequence instead: \"So…\" / thesis-forward.",
        ))
    return findings


# =============================================================================
# v18 fingerprint scanners (S12 2026-06-12 — FINGERPRINT-UNSCRIPTED §9 start
# values; single-sample, so WARN/REVIEW only, never HARD)
# =============================================================================

def _sections_with_sentences(lines: list) -> list:
    """Return [(section_name, [(line_no, sent), ...])] split at ## headers."""
    sections = []
    current_name = "(preamble)"
    current = []
    for i, raw in enumerate(lines, 1):
        if re.match(r"^##[^#]", raw.lstrip()):
            if current:
                sections.append((current_name, current))
            current_name = raw.strip().lstrip("#").strip()
            current = []
            continue
        if _is_structural(raw):
            continue
        text = clean_line(raw).strip()
        if not text:
            continue
        for sent in _SENTENCE_SPLIT.split(text):
            sent = sent.strip()
            if sent:
                current.append((i, sent))
    if current:
        sections.append((current_name, current))
    return sections


def scan_sentence_band(file: str, lines: list) -> list:
    """WARN when a section's median sentence length falls outside 10–22 words.

    Band from FINGERPRINT-UNSCRIPTED §1 (gold: median 13, mean 19). Broadcast
    prior is 15–20 (CRAFT R3, IDEA tier) — noted, not enforced. Sections with
    fewer than 5 sentences are skipped as noise.
    """
    findings = []
    for name, sents in _sections_with_sentences(lines):
        if len(sents) < 5:
            continue
        counts = sorted(word_count(s) for _, s in sents)
        median = counts[len(counts) // 2]
        if median < 10 or median > 22:
            findings.append(Finding(
                file, sents[0][0], "WARN", "sentence-band",
                f"[{name[:40]}] median {median}w over {len(sents)} sentences",
                "Per-beat median outside 10-22w (gold median 13 / mean 19). <10 = clipped-gavel risk; >22 = run-on risk. Rebalance the section's rhythm.",
            ))
    return findings


def scan_fragment_share(file: str, lines: list) -> list:
    """One WARN when 1–5-word sentences exceed 20% of the script (gold: 13%)."""
    sents = _flatten_sentences(lines)
    if len(sents) < 30:
        return []
    frags = [(ln, s) for ln, s in sents if word_count(s) <= 5]
    share = len(frags) / len(sents)
    if share > 0.20:
        return [Finding(
            file, frags[0][0], "WARN", "fragment-share",
            f"{len(frags)}/{len(sents)} sentences are <=5 words ({share:.0%})",
            "Fragment share over 20% (gold 13%, functional not dramatic). Combine into flowing sentences; keep only earned fragments.",
        )]
    return []


def scan_questions(file: str, lines: list) -> list:
    """REVIEW-flag every question in VO (gold baseline: 0 questions / 39 sentences).

    Setup-questions immediately answered are the one acceptable scripted form
    (57-28); free-floating rhetorical questions baseline ~0 (GS-03). The
    chain-vs-zero tension (H3) is pending /voice — hence REVIEW, never HARD.
    """
    findings = []
    for line_no, sent in _flatten_sentences(lines):
        if sent.endswith("?"):
            findings.append(Finding(
                file, line_no, "REVIEW", "question",
                sent[:80],
                "Question in VO (gold baseline ~0). OK only as a setup-question answered in the NEXT sentence; cut staged rhetorical questions.",
            ))
    return findings


_HEDGE = re.compile(r"\b(I think|I guess|kind of|basically|at least|probably)\b", re.IGNORECASE)


def scan_verdict_hedge(file: str, lines: list) -> list:
    """Advisory nudge (REVIEW): closing section carries zero colloquial hedge.

    Hedge family (~1.5/100w) is constitutive of his verdict register (GS-05:
    clause-final "I guess", scope-back qualifiers). Optional check — never blocks.
    """
    sections = _sections_with_sentences(lines)
    if not sections:
        return []
    name, sents = sections[-1]
    if len(sents) < 3:
        return []
    if any(_HEDGE.search(s) for _, s in sents):
        return []
    return [Finding(
        file, sents[0][0], "REVIEW", "verdict-hedge",
        f"[{name[:40]}] closing section has zero colloquial hedge",
        "His verdict register hedges (I think / I guess / kind of / at least). Consider one — optional, aphorism-certainty closes are not him.",
    )]


# =============================================================================
# Transition audit (REVIEW only — never fails the run)
# =============================================================================

_OPENER_HEADERS = re.compile(r"\b(COLD ?OPEN|HOOK|INTRO|CTA|OUTRO|TITLE)\b", re.IGNORECASE)


def scan_transitions(file: str, lines: list) -> list:
    """For each ## section handoff, verdict PASS/REVIEW on the first sentence after.

    Skips the opener (first section / COLD OPEN / HOOK / CTA) — there is no prior
    beat to bridge from, so the famous-then-puncture hook is not a transition.
    """
    findings = []
    n = len(lines)
    seen_first = False
    for i, raw in enumerate(lines, 1):
        # Level-2 headers only = act/section boundaries (not ### subsections, which
        # are within-act beats and would double-count every transition).
        if not re.match(r"^##[^#]", raw.lstrip()):
            continue
        header = raw.strip().lstrip("#").strip()
        if not seen_first:
            seen_first = True  # first section header = the opener, skip it
            continue
        if _OPENER_HEADERS.search(header):
            continue
        # Find first spoken content line after the header.
        first = None
        first_line = None
        for j in range(i, n):
            cand = lines[j]
            if _is_structural(cand):
                continue
            txt = clean_line(cand).strip()
            if txt:
                first = txt
                first_line = j + 1
                break
        if not first:
            continue
        sent = _SENTENCE_SPLIT.split(first)[0].strip()
        verdict, reasons = _judge_transition(sent)
        if verdict == "REVIEW":
            findings.append(Finding(
                file, first_line, "REVIEW", "transition",
                f"[{header}] → \"{sent[:80]}\"",
                "; ".join(reasons),
            ))
    return findings


def _judge_transition(sent: str):
    reasons = []
    low = sent.lower()
    words = sent.split()
    first_word = re.sub(r"[^\w']", "", words[0].lower()) if words else ""

    # (c) common story called flatly "wrong"
    if re.search(r"\b(is|gets it|are all|just|flatly|simply) wrong\b", low) or "story is wrong" in low or "got it wrong" in low:
        reasons.append('calls the common story flatly "wrong" — prefer "oversimplified / tells only one part of the story"')

    # (b) vague referent opener with no antecedent on the same line
    if first_word in VAGUE_OPENERS:
        reasons.append(f'opens with vague referent "{words[0]}" after a section reset — name the subject')
    if "the very first one" in low or re.search(r"\bthe very first\b(?!\s+\w)", low):
        reasons.append('"the very first one" — the very first WHAT? name it')

    # (a) bare topic jump: no bridge connector AND no thesis-forward signal
    has_bridge = first_word in BRIDGE_OPENERS
    has_causal = bool(re.search(r"\b(because|so that|which is why|that meant|the real question|what comes next)\b", low))
    if not has_bridge and not has_causal and first_word not in VAGUE_OPENERS:
        reasons.append("bare topic jump — no causal/thesis bridge into the next beat's subject")

    return ("REVIEW" if reasons else "PASS"), (reasons or ["thesis-forward / bridged"])


# =============================================================================
# Driver + reporting
# =============================================================================

def lint_file(path: str, do_transitions: bool = True) -> list:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    lines = mask_comments(text.splitlines())
    findings = []
    findings += scan_patterns(path, lines)
    findings += scan_staccato(path, lines)
    findings += scan_stacked_credentials(path, lines)
    findings += scan_negation_pairs(path, lines)
    findings += scan_understand_go_back(path, lines)
    findings += scan_sentence_band(path, lines)
    findings += scan_fragment_share(path, lines)
    findings += scan_questions(path, lines)
    findings += scan_verdict_hedge(path, lines)
    if do_transitions:
        findings += scan_transitions(path, lines)
    findings.sort(key=lambda f: (f.line, f.severity))
    return findings


_SEV_ORDER = {"HARD": 0, "WARN": 1, "REVIEW": 2}


def format_report(path: str, findings: list, quiet: bool = False) -> str:
    out = []
    hard = [f for f in findings if f.severity == "HARD"]
    warn = [f for f in findings if f.severity == "WARN"]
    review = [f for f in findings if f.severity == "REVIEW"]

    out.append("=" * 64)
    out.append(f"  VOICE LINT — {path}")
    out.append("=" * 64)

    if not quiet:
        for label, group in (("HARD (must fix)", hard), ("WARN (dispreferred)", warn), ("REVIEW (advisory)", review)):
            if not group:
                continue
            out.append("")
            out.append(f"  {label}:")
            for f in group:
                out.append(f"    L{f.line}  [{f.rule}]  {f.text}")
                out.append(f"          → {f.fix}")

    out.append("")
    out.append(f"  Summary: {len(hard)} HARD · {len(warn)} WARN · {len(review)} REVIEW")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Voice Lint — flag creator-voice violations before the read-aloud gate (History vs Hype)",
        epilog=(
            "Examples:\n"
            "  python -m tools.voice_lint video-projects/_READY_TO_FILM/58-kurdistan-statelessness-2026/SCRIPT.md\n"
            '  python -m tools.voice_lint "video-projects/**/SCRIPT.md"\n'
            "  python -m tools.voice_lint SCRIPT.md --quiet --no-transitions\n"
            "\nRules are transcribed from .claude/REFERENCE/VOICE-PROFILE.md (canonical).\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", help="SCRIPT.md path(s) or glob pattern(s)")
    parser.add_argument("--no-transitions", action="store_true", help="Skip the transition audit (REVIEW checks)")
    parser.add_argument("--quiet", action="store_true", help="Print summary counts only")
    args = parser.parse_args()

    # Expand globs (and pass through literal paths).
    files = []
    for p in args.paths:
        matched = globmod.glob(p, recursive=True)
        if matched:
            files.extend(matched)
        elif Path(p).exists():
            files.append(p)
        else:
            print(f"WARNING: no match for {p}")
    files = [f for f in dict.fromkeys(files) if Path(f).is_file()]

    if not files:
        print("ERROR: no files to lint")
        sys.exit(2)

    total_hard = 0
    for f in files:
        findings = lint_file(f, do_transitions=not args.no_transitions)
        total_hard += sum(1 for x in findings if x.severity == "HARD")
        print(format_report(f, findings, quiet=args.quiet))
        print()

    sys.exit(1 if total_hard else 0)


if __name__ == "__main__":
    main()
