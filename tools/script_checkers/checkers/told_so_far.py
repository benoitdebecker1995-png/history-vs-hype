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

        severity = 'warning' if issues else 'ok'

        return {
            'issues': issues,
            'stats': {
                'total_triggers': total_triggers,
                'flagged': len(issues),
                'severity': severity,
            },
        }
