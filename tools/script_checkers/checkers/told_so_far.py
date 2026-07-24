"""
SCRIPT-06: Told-So-Far Ledger

Flags rebuttal/callback sentences whose antecedent claim has not appeared
earlier in the script. Mechanizes .claude/REFERENCE/VOICE-PROFILE.md's #62
T1-T3 read-aloud finding (~line 512): "a rebuttal is a referent too — its
antecedent claim must exist on screen first." His ~30 read-aloud flags on
that pass reduced to this one failure class — the script rebutting or
calling back to a claim never stated on screen yet ("which massacre?",
"what case?", "a callback to something that doesn't exist").

Heuristic v1 (deliberately imperfect — see docs/LLM-CRAFT-UPGRADE-PLAN.md D2):
tracks a running bag of content words already spoken, and for each detected
rebuttal/callback sentence, checks whether its content words overlap with
anything already said. No overlap = a candidate forward-referencing rebuttal.
False positives are expected and acceptable — this is a first pass surfacing
candidates for the human read-aloud, not a coreference-complete detector.
"""

import re
from typing import Dict, List, Any, Set, Tuple
from . import BaseChecker


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD_RX = re.compile(r"[A-Za-z]{3,}")
_STAGE_DIRECTION_RX = re.compile(r"\[[^\]]*\]")
_BOLD_RX = re.compile(r"\*\*([^*]*)\*\*")
_ITALIC_RX = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")

_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with",
    "that", "this", "these", "those", "is", "was", "were", "are", "be", "been",
    "it", "its", "he", "she", "they", "them", "his", "her", "their", "not", "no",
    "so", "as", "at", "by", "from", "into", "than", "then", "there", "here",
    "which", "what", "who", "whom", "whose", "when", "where", "why", "how",
    "just", "only", "also", "still", "even", "own", "same", "again", "you",
    "your", "one", "all", "some", "any", "had", "has", "have", "did", "does",
}

# Rebuttal: negation-correction ("wasn't X", "isn't whole", "didn't...").
_NEGATION_RX = re.compile(
    r"\b(wasn'?t|isn'?t|weren'?t|didn'?t|hadn'?t|haven'?t|doesn'?t)\b",
    re.IGNORECASE,
)

# Callback: refers to a prior claim without restating it ("that same X",
# "as we saw", "only half of it", "which X" mid-narration).
_CALLBACK_RX = re.compile(
    r"\b(that same \w+|the same \w+ (?:from|as)|as we saw|as mentioned earlier|"
    r"like we said|isn'?t whole either|only half of it|that'?s only half)\b",
    re.IGNORECASE,
)


def _clean(raw: str) -> str:
    s = _STAGE_DIRECTION_RX.sub(" ", raw)
    s = _BOLD_RX.sub(r"\1", s)
    s = _ITALIC_RX.sub(r"\1", s)
    return s


def _is_structural(raw: str) -> bool:
    s = raw.strip()
    if not s:
        return True
    if s.startswith("#") or s.startswith(">") or s.startswith("|"):
        return True
    if set(s) <= set("-= "):
        return True
    if not _clean(raw).strip():
        return True
    if re.match(r"^\*\*[^*]+:\*\*", s):
        return True
    if s.startswith("*") and s.endswith("*") and not s.startswith("**"):
        return True
    return False


def _content_words(text: str) -> Set[str]:
    return {w.lower() for w in _WORD_RX.findall(text)} - _STOPWORDS


# --- V5: enumerated promises -------------------------------------------------
# "…it would have left three things behind — attacks going off everywhere at
# once, reports coming back up the chain, and the order itself."
# Only the ENUMERATED form is detected. A promise the script makes in prose
# ("we'll come back to this") is not mechanizable and is not attempted.
_NUMBER_WORDS = {"two": 2, "three": 3, "four": 4, "five": 5}
_PROMISE_RX = re.compile(
    r"\b(two|three|four|five)\s+(?:things|reasons|questions|parts|pieces|ways|"
    r"tests|conditions|documents|claims)\b[^—:.]*[—:]\s*(.+)$",
    re.IGNORECASE,
)


def _split_promise_items(tail: str) -> List[str]:
    """Split the list after the dash/colon into its items."""
    tail = re.split(r"(?<=[.!?])\s", tail)[0]
    tail = re.sub(r"\band\s+", ", ", tail, flags=re.IGNORECASE)
    return [p.strip(" .;") for p in tail.split(",") if p.strip(" .;")]


def _head_noun(item: str) -> str:
    """First content word of a promise item — its handle for later mentions."""
    for w in _WORD_RX.findall(item):
        if w.lower() not in _STOPWORDS:
            return w.lower()
    return ""


# --- V4: near-duplicate claims -----------------------------------------------
# Overlap coefficient, not Jaccard: a restatement is usually SHORTER than the
# original ("the toll had run to somewhere between fifty and sixty thousand"
# vs the fuller first statement), and Jaccard punishes that asymmetry.
_V4_MIN_CONTENT_WORDS = 5
_V4_OVERLAP_THRESHOLD = 0.7

_POSITION_GUARD = (
    "REVIEW ONLY — a restated fact is not automatically repetition. Ask what this "
    "restatement's POSITION is doing before cutting it: #62 states the death toll "
    "twice on purpose, so the scale lands BEFORE the honoring is explained, and a "
    "previous pass cut the first instance as V4 and broke the sequencing guard. "
    "If you cannot say what the position is doing, leave it and flag it."
)


def _flatten_sentences(text: str) -> List[Tuple[int, str]]:
    """Return [(line_no, sentence_text)] over spoken content only."""
    out = []
    for i, raw in enumerate(text.splitlines(), 1):
        if _is_structural(raw):
            continue
        clean = _clean(raw).strip()
        if not clean:
            continue
        for sent in _SENTENCE_SPLIT.split(clean):
            sent = sent.strip()
            if sent:
                out.append((i, sent))
    return out


class ToldSoFarChecker(BaseChecker):
    """Detect rebuttals/callbacks with no antecedent earlier in the script."""

    def __init__(self, config):
        super().__init__(config)

    @property
    def name(self) -> str:
        return "told_so_far"

    def check(self, text: str) -> Dict[str, Any]:
        """
        Scan for rebuttal/callback sentences and check each against the
        running bag of content words spoken so far.

        Returns:
            {
                'issues': [
                    {
                        'type': 'rebuttal' | 'callback',
                        'line': int,
                        'sentence': str,
                        'severity': 'warning',
                        'suggestion': str,
                    }
                ],
                'stats': {
                    'total_triggers': N,
                    'flagged': N,
                    'severity': 'ok' | 'warning',
                }
            }
        """
        sentences = _flatten_sentences(text)
        seen_words: Set[str] = set()
        issues: List[Dict[str, Any]] = []
        total_triggers = 0

        for line_no, sent in sentences:
            is_negation = bool(_NEGATION_RX.search(sent))
            is_callback = bool(_CALLBACK_RX.search(sent))

            if is_negation or is_callback:
                total_triggers += 1
                sent_words = _content_words(sent)
                overlap = sent_words & seen_words
                if not overlap:
                    kind = "rebuttal" if is_negation else "callback"
                    issues.append({
                        'type': kind,
                        'line': line_no,
                        'sentence': sent,
                        'severity': 'warning',
                        'suggestion': (
                            f"No earlier content word overlaps with this {kind} — "
                            "possible forward-referencing rebuttal (VOICE-PROFILE.md "
                            "~line 512: 'a rebuttal is a referent too, its antecedent "
                            "claim must exist on screen first'). Verify the claim being "
                            "negated/called back to was actually stated earlier."
                        ),
                    })

            seen_words |= _content_words(sent)

        # V1 alone decides pass/fail severity. V4/V5 are REVIEW-only and must
        # never turn a clean script into a warning — this project gates on
        # `0 HARD`, so an uncertain checker that escalates is worse than none.
        severity = 'warning' if issues else 'ok'

        promises, broken = self._check_promises(sentences)
        issues.extend(promises)
        issues.extend(broken)
        issues.extend(self._check_reanswers(sentences))

        return {
            'issues': issues,
            'stats': {
                'total_triggers': total_triggers,
                'flagged': len(issues) - len(promises) - len(broken)
                           - sum(1 for i in issues if i['type'] == 'possible_reanswer'),
                'severity': severity,
                'promises_found': len(promises),
                'broken_promises': len(broken),
                'not_mechanized': ['V2', 'V3'],
            },
        }

    def _check_promises(self, sentences):
        """V5: find enumerated promises; break one only on a ZERO later mention.

        Deliberately weak. Deciding whether a payoff actually *satisfies* a
        promise needs to tell "an order we can inspect" (the payoff) from
        "Germany ordered them to withdraw" (an unrelated verb) and from "is
        there proof of an order from the top?" (the question that RAISES it).
        Measured on #62: the noun `order` appears three times before its payoff
        chapter, all in those other senses. So partial-payoff detection is not
        honestly mechanizable and is not attempted — only the unambiguous case
        where a promised item is never mentioned again at all, which is exactly
        what happens when a beat gets cut for runtime.
        """
        promises, broken = [], []
        for idx, (line_no, sent) in enumerate(sentences):
            m = _PROMISE_RX.search(sent)
            if not m:
                continue
            expected = _NUMBER_WORDS[m.group(1).lower()]
            items = _split_promise_items(m.group(2))
            if len(items) != expected:
                continue  # not a real enumeration; don't guess
            later = " ".join(s for _, s in sentences[idx + 1:])
            unsatisfied = [
                it for it in items
                if (h := _head_noun(it))
                and not re.search(r"\b" + re.escape(h) + r"\b", later, re.IGNORECASE)
            ]
            promises.append({
                'type': 'promise', 'line': line_no, 'sentence': sent,
                'severity': 'review', 'items': items,
                'suggestion': (
                    f"The script promises {expected} things here: {items}. Each must be "
                    "dealt with later, in this order. If a beat answering one is ever cut "
                    "for runtime, this sentence has to change with it."
                ),
            })
            if unsatisfied:
                broken.append({
                    'type': 'broken_promise', 'line': line_no, 'sentence': sent,
                    'severity': 'review', 'unsatisfied': unsatisfied,
                    'suggestion': (
                        f"Never mentioned again after this promise: {unsatisfied}. Either the "
                        "payoff beat was cut, or the promise needs rewording to match what "
                        "the script actually delivers."
                    ),
                })
        return promises, broken

    def _check_reanswers(self, sentences):
        """V4: near-duplicate claims, REVIEW-only, always carrying the position guard."""
        out, prepared = [], []
        for line_no, sent in sentences:
            words = _content_words(sent)
            if len(words) >= _V4_MIN_CONTENT_WORDS:
                prepared.append((line_no, sent, words))
        for i, (ln_a, sent_a, wa) in enumerate(prepared):
            for ln_b, sent_b, wb in prepared[i + 1:]:
                overlap = len(wa & wb) / min(len(wa), len(wb))
                if overlap >= _V4_OVERLAP_THRESHOLD:
                    out.append({
                        'type': 'possible_reanswer', 'line': ln_b, 'sentence': sent_b,
                        'severity': 'review', 'echoes_line': ln_a, 'echoes': sent_a,
                        'overlap': round(overlap, 2), 'suggestion': _POSITION_GUARD,
                    })
        return out
