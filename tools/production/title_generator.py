"""
Title Generation Engine

Extracts material from scripts/SRTs and generates scored, ranked title candidates.

Replaces the opening-only, fixed-3-variant title generation with a script-grounded
engine that reads numbers, documents, contradictions, and entity pairs from the full
script and produces title candidates auto-scored via title_scorer.score_title().

Usage:
    from tools.production.title_generator import (
        TitleMaterialExtractor,
        TitleCandidateGenerator,
        detect_versus_signal,
        generate_title_candidates,
        format_title_candidates,
    )

    parser = ScriptParser()
    sections = parser.parse_file(path)
    candidates = generate_title_candidates(sections=sections)
    print(format_title_candidates(candidates))
"""

import re
from typing import List, Tuple, Optional, Dict, Any

from tools.production.entities import Entity, EntityExtractor
from tools.production.parser import ScriptParser, Section, strip_for_teleprompter
from tools.title_scorer import score_title


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Position multipliers for section types
POSITION_WEIGHTS = {
    "intro": 2.0,
    "conclusion": 1.5,
    "body": 1.0,
}

# Conflict language that indicates versus framing
CONFLICT_MARKERS = [
    "against", "disputed", "competed", "rivalry", "divided", "vs", "versus",
    "conflict", "war", "battle", "claim", "claimed", "rejected", "contested",
    "opposed", "split", "tension", "fight", "fought", "clash", "clashed",
    "compete", "dispute", "challenge", "challenged", "standoff",
]

# Negation/contradiction trigger phrases
CONTRADICTION_TRIGGERS = [
    r"contrary to popular belief",
    r"despite (?:what|the)",
    r"the myth (?:is|claims?|says?)",
    r"(?:never|not) actually",
    r"in (?:fact|reality)",
    r"but (?:in )?(?:reality|actually|in fact)",
    r"actually[,\s]",
    r"weren'?t actually",
    r"didn'?t actually",
    r"wasn'?t actually",
    r"the truth is",
    r"what (?:really|actually) happened",
]

# Maximum title length per YouTube guidelines
MAX_TITLE_LENGTH = 70

# Year range to exclude from number extraction
_YEAR_RE = re.compile(r'\b(1[0-9]{3}|20[0-2][0-9])\b')


# ---------------------------------------------------------------------------
# TitleMaterialExtractor
# ---------------------------------------------------------------------------

class TitleMaterialExtractor:
    """
    Scans full script or SRT to extract material suitable for title generation.

    Produces a dict with keys:
        numbers       -> list of (number_str, weight) sorted by weight desc
        documents     -> list of (Entity, weight) sorted by weight desc
        entities      -> list of (Entity, weight) sorted by weight desc
        contradictions-> list of (myth_phrase, reality_phrase, weight) sorted by weight desc
    """

    def __init__(self):
        self._entity_extractor = EntityExtractor(use_spacy=False)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract_from_sections(self, sections: List[Section]) -> Dict[str, List]:
        """
        Full script scan over parsed sections.

        For each section:
          - Apply position weight (intro=2.0, conclusion=1.5, body=1.0)
          - Extract entities with EntityExtractor on strip_for_teleprompter(content)
          - Extract numbers and contradictions from cleaned text

        Returns merged, sorted material dict.
        """
        # Accumulators
        number_acc: Dict[str, float] = {}   # number_str -> weight
        entity_acc: Dict[str, Tuple[Entity, float]] = {}   # normalized -> (entity, weight)
        doc_acc: Dict[str, Tuple[Entity, float]] = {}       # normalized -> (doc_entity, weight)
        contradiction_list: List[Tuple[str, str, float]] = []

        for section in sections:
            w = POSITION_WEIGHTS.get(section.section_type, 1.0)
            clean = strip_for_teleprompter(section.content)

            # Numbers
            for num_str in self._extract_numbers_with_context(clean):
                number_acc[num_str] = number_acc.get(num_str, 0.0) + w

            # Entities (all types)
            entities = self._entity_extractor.extract(clean, section.start_line)
            for ent in entities:
                if ent.entity_type == "document":
                    if ent.normalized in doc_acc:
                        old_ent, old_w = doc_acc[ent.normalized]
                        doc_acc[ent.normalized] = (old_ent, old_w + w * ent.mentions)
                    else:
                        doc_acc[ent.normalized] = (ent, w * ent.mentions)
                else:
                    if ent.normalized in entity_acc:
                        old_ent, old_w = entity_acc[ent.normalized]
                        entity_acc[ent.normalized] = (old_ent, old_w + w * ent.mentions)
                    else:
                        entity_acc[ent.normalized] = (ent, w * ent.mentions)

            # Supplementary document extraction (handles "Treaty of X" patterns
            # that entities.py misses due to its suffix-based regex approach)
            for doc_name in self._extract_named_documents(clean):
                normalized_doc = doc_name.lower().strip()
                # Count occurrences in the clean text for weighting
                mentions = len(re.findall(re.escape(doc_name), clean, re.IGNORECASE)) or 1
                synthetic_ent = Entity(
                    text=doc_name,
                    entity_type="document",
                    mentions=mentions,
                    positions=[section.start_line],
                    normalized=normalized_doc,
                )
                if normalized_doc in doc_acc:
                    old_ent, old_w = doc_acc[normalized_doc]
                    doc_acc[normalized_doc] = (old_ent, old_w + w * mentions)
                else:
                    doc_acc[normalized_doc] = (synthetic_ent, w * mentions)

            # Contradictions
            for myth, reality in self._extract_contradictions(clean):
                contradiction_list.append((myth, reality, w))

        return self._build_material(number_acc, entity_acc, doc_acc, contradiction_list)

    def extract_from_srt(self, srt_path_or_text: str) -> Dict[str, List]:
        """
        Extract material from SRT subtitle text (or a file path to an SRT).

        Strips sequence numbers, timestamps, and HTML tags (per retitle_gen.py pattern).
        Applies positional heuristic:
          - First 20% of words -> intro weight (2.0)
          - Last 20% of words -> conclusion weight (1.5)
          - Middle -> body weight (1.0)
        """
        import os
        # If it looks like a file path and the file exists, read it
        if len(srt_path_or_text) < 500 and os.path.exists(srt_path_or_text):
            text = open(srt_path_or_text, encoding="utf-8").read()
        else:
            text = srt_path_or_text

        # Clean SRT: strip sequence numbers, timestamps, HTML tags
        cleaned_lines = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if re.match(r'^\d+$', line):
                continue  # sequence number
            if re.match(r'\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->', line):
                continue  # timestamp
            line = re.sub(r'<[^>]+>', '', line)  # HTML tags
            if line:
                cleaned_lines.append(line)

        full_text = ' '.join(cleaned_lines)
        words = full_text.split()
        total = len(words)

        if total == 0:
            return {"numbers": [], "documents": [], "entities": [], "contradictions": []}

        intro_end = max(1, int(total * 0.20))
        body_end = max(intro_end + 1, int(total * 0.80))

        intro_text = ' '.join(words[:intro_end])
        body_text = ' '.join(words[intro_end:body_end])
        conclusion_text = ' '.join(words[body_end:])

        # Create synthetic sections for unified processing
        synthetic_sections = []
        if intro_text.strip():
            synthetic_sections.append(Section(
                heading="Intro",
                content=intro_text,
                word_count=intro_end,
                start_line=1,
                section_type="intro",
            ))
        if body_text.strip():
            synthetic_sections.append(Section(
                heading="Body",
                content=body_text,
                word_count=body_end - intro_end,
                start_line=intro_end + 1,
                section_type="body",
            ))
        if conclusion_text.strip():
            synthetic_sections.append(Section(
                heading="Conclusion",
                content=conclusion_text,
                word_count=total - body_end,
                start_line=body_end + 1,
                section_type="conclusion",
            ))

        return self.extract_from_sections(synthetic_sections)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _extract_named_documents(self, text: str) -> List[str]:
        """
        Extract document names that entity extractor may miss.

        Specifically handles "Treaty of X", "Act of X", "Convention of X" patterns
        where X is a proper name (not captured by entities.py's suffix-based regex).

        Returns list of document name strings.
        """
        results = []
        doc_keywords = [
            "treaty", "act", "agreement", "accord", "convention", "protocol",
            "declaration", "resolution", "constitution", "charter", "statute",
            "memorandum", "ordinance", "covenant", "order",
        ]
        kw_pattern = "|".join(doc_keywords)

        # "Treaty of Utrecht", "Convention of Vienna", etc.
        pattern = re.compile(
            rf'\b({kw_pattern})\s+of\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)',
            re.IGNORECASE,
        )
        for m in pattern.finditer(text):
            doc_name = f"{m.group(1).title()} of {m.group(2)}"
            results.append(doc_name)

        # "Paris Agreement", "Kyoto Protocol" (proper noun + doc keyword)
        proper_doc_pattern = re.compile(
            rf'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+({kw_pattern})\b',
            re.IGNORECASE,
        )
        for m in proper_doc_pattern.finditer(text):
            first = m.group(1).strip()
            # Skip known false positives (generic phrases)
            if first.lower() in {"the", "an", "a", "this", "that"}:
                continue
            doc_name = f"{first} {m.group(2).title()}"
            results.append(doc_name)

        # Deduplicate preserving order
        seen = set()
        unique = []
        for r in results:
            key = r.lower()
            if key not in seen:
                seen.add(key)
                unique.append(r)
        return unique

    def _extract_numbers_with_context(self, text: str) -> List[str]:
        """
        Regex for integers and percentages. Skip years (1000-2099).
        Returns list of number strings (with context like '%' or '-').

        Per research Pattern 5: specific numbers are title material.
        """
        results = []

        # Range percentages: "10-15%" or "10–15%"
        range_pct = re.finditer(r'\b(\d+[-\u2013]\d+%)', text)
        for m in range_pct:
            results.append(m.group(1))

        # Single percentages: "42%"
        single_pct = re.finditer(r'\b(\d+(?:\.\d+)?%)', text)
        for m in single_pct:
            # Skip if already captured in range
            if m.group(1) not in results:
                results.append(m.group(1))

        # Plain integers (not years, not already captured as percentage)
        # Context: number must be in a non-year context
        plain_int = re.finditer(r'\b(\d+)\b', text)
        already = set(r.rstrip('%') for r in results)
        for m in plain_int:
            num = m.group(1)
            if _YEAR_RE.match(num):
                continue  # skip years
            if num in already:
                continue
            # Only include numbers that seem meaningful (>= 2 unless it's tiny factoid)
            if int(num) >= 2:
                results.append(num)

        return results

    def _extract_contradictions(self, text: str) -> List[Tuple[str, str]]:
        """
        Regex for negation/contradiction patterns.
        Returns list of (myth_phrase, reality_phrase) tuples.

        Per research Pattern 6: contradictions are powerful title material.
        """
        results = []
        sentences = re.split(r'(?<=[.!?])\s+', text)

        for i, sent in enumerate(sentences):
            sent_lower = sent.lower()

            for trigger in CONTRADICTION_TRIGGERS:
                if re.search(trigger, sent_lower):
                    # This sentence contains a contradiction marker
                    # myth = the sentence before (or phrase before the trigger)
                    # reality = the sentence itself (or remainder after trigger)
                    myth = sentences[i - 1].strip() if i > 0 else ""
                    reality = sent.strip()

                    if myth or reality:
                        results.append((myth, reality))
                    break  # one match per sentence is enough

        return results

    @staticmethod
    def _build_material(
        number_acc: Dict[str, float],
        entity_acc: Dict[str, Tuple[Entity, float]],
        doc_acc: Dict[str, Tuple[Entity, float]],
        contradiction_list: List[Tuple],
    ) -> Dict[str, List]:
        """Assemble and sort the material dict."""
        numbers_sorted = sorted(
            [(num, w) for num, w in number_acc.items()],
            key=lambda x: -x[1],
        )
        entities_sorted = sorted(
            list(entity_acc.values()),
            key=lambda x: -x[1],
        )
        docs_sorted = sorted(
            list(doc_acc.values()),
            key=lambda x: -x[1],
        )
        contras_sorted = sorted(
            contradiction_list,
            key=lambda x: -x[2],
        )

        return {
            "numbers": numbers_sorted,
            "documents": docs_sorted,
            "entities": entities_sorted,
            "contradictions": contras_sorted,
        }


# ---------------------------------------------------------------------------
# detect_versus_signal (module-level function)
# ---------------------------------------------------------------------------

def detect_versus_signal(
    entities: List[Entity],
    full_text: str,
) -> Tuple[str, str, float]:
    """
    Detect whether two entities co-occur with conflict language, indicating
    versus framing is appropriate for a title.

    Args:
        entities:  Entities extracted from the script.
        full_text: Full cleaned script/SRT text.

    Returns:
        (entity_a_text, entity_b_text, signal_strength)
        Returns ('', '', 0.0) if no signal found.

    Signal score: conflict_marker_hits / 3.0, capped at 1.0.
    """
    if len(entities) < 2:
        return ("", "", 0.0)

    # Only consider place / person / organization entities for versus framing
    candidates = [
        e for e in entities
        if e.entity_type in ("place", "person", "organization")
    ]

    if len(candidates) < 2:
        return ("", "", 0.0)

    # Sort by mentions descending to get top candidates
    candidates_sorted = sorted(candidates, key=lambda e: -e.mentions)

    words = full_text.lower().split()

    best_pair: Tuple[str, str, float] = ("", "", 0.0)

    # Check top pairs (limit to top-6 candidates to keep O(n) reasonable)
    top = candidates_sorted[:6]
    for i in range(len(top)):
        for j in range(i + 1, len(top)):
            ea = top[i]
            eb = top[j]
            hits = _count_conflict_hits(ea.text, eb.text, full_text, words)
            strength = min(1.0, hits / 3.0)
            if strength > best_pair[2]:
                best_pair = (ea.text, eb.text, strength)

    return best_pair


def _count_conflict_hits(
    entity_a: str,
    entity_b: str,
    full_text: str,
    words: List[str],
) -> int:
    """
    Count how many times entity_a and entity_b co-occur within a 100-word window
    alongside at least one conflict marker.
    """
    ea_lower = entity_a.lower()
    eb_lower = entity_b.lower()
    text_lower = full_text.lower()
    hits = 0

    # Find all positions of entity_a in word list
    ea_positions = []
    for idx, word in enumerate(words):
        if ea_lower in word:
            ea_positions.append(idx)

    # For each occurrence of entity_a, check 100-word window for entity_b + conflict marker
    for pos in ea_positions:
        window_start = max(0, pos - 50)
        window_end = min(len(words), pos + 50)
        window_words = words[window_start:window_end]
        window_text = " ".join(window_words)

        has_eb = eb_lower in window_text
        has_conflict = any(marker in window_text for marker in CONFLICT_MARKERS)

        if has_eb and has_conflict:
            hits += 1

    return hits


# ---------------------------------------------------------------------------
# TitleCandidateGenerator
# ---------------------------------------------------------------------------

class TitleCandidateGenerator:
    """
    Generates scored title candidates from extracted script material.

    Always produces at least one declarative variant.
    Adds versus, how_why, and curiosity variants when signals are present.
    Each candidate is auto-scored via score_title() and contains score, grade, pattern.
    """

    def generate(
        self,
        material: Dict[str, List],
        versus_signal: Tuple,
        topic_type: Optional[str] = None,
        db_path: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Generate title candidates from material dict and versus signal.

        Args:
            material:      Output of TitleMaterialExtractor.extract_*()
            versus_signal: (entity_a, entity_b, signal_strength) from detect_versus_signal()
            topic_type:    Optional topic type for grade thresholds
            db_path:       Optional path to keywords.db for DB-enriched scoring

        Returns:
            List of candidate dicts (score, grade, pattern, title, ...) sorted by score desc.
        """
        candidates = []
        entity_a, entity_b, signal_strength = versus_signal

        # Resolve primary entity/document for titles
        primary_entity = self._primary_entity(material)
        primary_doc = self._primary_doc(material)
        primary_number = self._primary_number(material)
        has_contradictions = len(material.get("contradictions", [])) > 0

        # --- 1. Declarative variant (ALWAYS generated) ---
        declarative_titles = self._build_declarative_titles(
            primary_entity, primary_doc, primary_number
        )
        for title in declarative_titles:
            candidates.append(self._score(title, topic_type, db_path))

        # --- 2. How/Why variant (when documents or contradictions present) ---
        if primary_doc or has_contradictions:
            how_titles = self._build_how_why_titles(
                primary_entity, primary_doc, has_contradictions
            )
            for title in how_titles:
                candidates.append(self._score(title, topic_type, db_path))

        # --- 3. Versus variant (when signal > 0) ---
        if signal_strength > 0 and entity_a and entity_b:
            vs_title = self._build_versus_title(entity_a, entity_b, primary_doc)
            if vs_title:
                candidates.append(self._score(vs_title, topic_type, db_path))

        # --- 4. Curiosity/paradox variant (when contradictions present) ---
        if has_contradictions:
            curiosity_titles = self._build_curiosity_titles(
                material["contradictions"], primary_entity
            )
            for title in curiosity_titles:
                candidates.append(self._score(title, topic_type, db_path))

        # Deduplicate and sort by score descending
        seen = set()
        unique_candidates = []
        for c in candidates:
            if c["title"] not in seen:
                seen.add(c["title"])
                unique_candidates.append(c)

        return sorted(unique_candidates, key=lambda x: -x["score"])

    # ------------------------------------------------------------------
    # Title builders
    # ------------------------------------------------------------------

    def _build_declarative_titles(
        self,
        primary_entity: Optional[str],
        primary_doc: Optional[str],
        primary_number: Optional[str],
    ) -> List[str]:
        """Build 1-2 declarative title variants."""
        titles = []

        if primary_entity and primary_number:
            t = f"The {primary_number} Secret {primary_entity} Never Tells"
            titles.append(self._truncate(t))

        if primary_entity:
            t = f"{primary_entity} Changed History"
            titles.append(self._truncate(t))
        elif primary_doc:
            t = f"{primary_doc} Changed Everything"
            titles.append(self._truncate(t))
        else:
            titles.append("The History They Got Wrong")

        return titles

    def _build_how_why_titles(
        self,
        primary_entity: Optional[str],
        primary_doc: Optional[str],
        has_contradictions: bool,
    ) -> List[str]:
        """Build how/why title variants."""
        titles = []

        if has_contradictions and primary_entity:
            t = f"Why {primary_entity} History Is Wrong"
            titles.append(self._truncate(t))

        if primary_doc:
            t = f"How {primary_doc} Divided the World"
            titles.append(self._truncate(t))

        return titles

    def _build_versus_title(
        self,
        entity_a: str,
        entity_b: str,
        primary_doc: Optional[str],
    ) -> str:
        """Build a versus title from detected entity pair."""
        title = f"{entity_a} vs {entity_b}"
        if primary_doc:
            suffix = f" and {primary_doc}"
            candidate = title + suffix
            if len(candidate) <= MAX_TITLE_LENGTH:
                title = candidate
        return self._truncate(title)

    def _build_curiosity_titles(
        self,
        contradictions: List[Tuple],
        primary_entity: Optional[str],
    ) -> List[str]:
        """Build curiosity/paradox title variants from contradictions."""
        titles = []

        for contradiction in contradictions[:1]:  # Use only the strongest
            myth, reality, _w = contradiction[0], contradiction[1], contradiction[2]

            if primary_entity and reality:
                # Extract key phrase from reality
                reality_words = reality.split()
                # Grab first 4-5 content words
                content = " ".join(reality_words[:5]).rstrip(".,;:")
                t = f"{primary_entity} and the {content}"
                if len(t) <= MAX_TITLE_LENGTH:
                    titles.append(self._truncate(t))

            if myth:
                t = f"The Myth of {primary_entity}" if primary_entity else "The Myth Historians Missed"
                titles.append(self._truncate(t))

        return titles

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _primary_entity(self, material: Dict) -> Optional[str]:
        """Return highest-weight non-date entity text, or None."""
        for entity, _w in material.get("entities", []):
            if hasattr(entity, "entity_type") and entity.entity_type != "date":
                return entity.text
            elif isinstance(entity, str):
                return entity
        return None

    def _primary_doc(self, material: Dict) -> Optional[str]:
        """Return highest-weight document entity text, or None."""
        docs = material.get("documents", [])
        if docs:
            doc, _w = docs[0]
            if hasattr(doc, "text"):
                return doc.text
            return str(doc)
        return None

    def _primary_number(self, material: Dict) -> Optional[str]:
        """Return highest-weight number string, or None."""
        numbers = material.get("numbers", [])
        if numbers:
            return numbers[0][0]
        return None

    def _score(
        self,
        title: str,
        topic_type: Optional[str],
        db_path: Optional[str],
    ) -> Dict[str, Any]:
        """Score a title via score_title() and return merged result dict."""
        result = score_title(title, db_path=db_path, topic_type=topic_type)
        # Ensure 'title' key matches the generated title (score_title strips whitespace)
        result["title"] = title
        return result

    @staticmethod
    def _truncate(title: str) -> str:
        """Truncate title to MAX_TITLE_LENGTH characters."""
        if len(title) > MAX_TITLE_LENGTH:
            return title[:MAX_TITLE_LENGTH - 1].rstrip() + "…"
        return title


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def format_title_candidates(candidates: List[Dict[str, Any]]) -> str:
    """
    Format a list of scored title candidates into a ranked markdown table.

    Candidates are sorted by score descending. The output includes:
      - A header "## Title Candidates (ranked by score)"
      - A markdown table with columns: #, Title, Score, Grade, Pattern
      - Warning lines below the table for any candidate with hard_rejects

    Args:
        candidates: List of score_title() result dicts (each must have
                    'title', 'score', 'grade', 'pattern', 'hard_rejects').

    Returns:
        Complete markdown string with ranked table and penalty warnings.
    """
    # Sort descending by score (candidates may already be sorted, but enforce it)
    sorted_candidates = sorted(candidates, key=lambda c: -c.get("score", 0))

    lines = [
        "## Title Candidates (ranked by score)",
        "",
        "| # | Title | Score | Grade | Pattern |",
        "|---|-------|-------|-------|---------|",
    ]

    for rank, candidate in enumerate(sorted_candidates, start=1):
        title = candidate.get("title", "")
        score = candidate.get("score", 0)
        grade = candidate.get("grade", "?")
        pattern = candidate.get("pattern", "unknown")
        lines.append(f"| {rank} | {title} | {score} | {grade} | {pattern} |")

    # Append warning lines for penalized candidates
    warnings = []
    for rank, candidate in enumerate(sorted_candidates, start=1):
        hard_rejects = candidate.get("hard_rejects", [])
        if hard_rejects:
            for reason in hard_rejects:
                warnings.append(f"\n[warning] #{rank} penalized: {reason}")

    if warnings:
        lines.append("")
        lines.extend(warnings)

    return "\n".join(lines)


def generate_title_candidates(
    sections: Optional[List[Section]] = None,
    srt_text: Optional[str] = None,
    topic_type: Optional[str] = None,
    db_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Orchestrate extract -> detect_versus -> generate -> sort pipeline.

    Args:
        sections:   Parsed script sections (from ScriptParser). Mutually exclusive with srt_text.
        srt_text:   Raw SRT subtitle text. Mutually exclusive with sections.
        topic_type: Optional topic type for grade thresholds.
        db_path:    Optional path to keywords.db for DB-enriched scoring.

    Returns:
        List of scored title candidates, sorted by score descending.
    """
    if sections is None and srt_text is None:
        raise ValueError("Provide either 'sections' or 'srt_text'.")

    extractor = TitleMaterialExtractor()

    if sections is not None:
        material = extractor.extract_from_sections(sections)
        full_text = " ".join(
            strip_for_teleprompter(s.content) for s in sections
        )
    else:
        material = extractor.extract_from_srt(srt_text)
        # Rebuild clean text for versus detection
        clean_lines = []
        for line in srt_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if re.match(r'^\d+$', line):
                continue
            if re.match(r'\d{2}:\d{2}:\d{2}[,\.]\d{3}\s*-->', line):
                continue
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                clean_lines.append(line)
        full_text = ' '.join(clean_lines)

    # Extract entity list for versus detection
    all_entities = [e for e, _w in material.get("entities", [])]
    all_entities += [e for e, _w in material.get("documents", [])]

    versus_signal = detect_versus_signal(all_entities, full_text)

    generator = TitleCandidateGenerator()
    candidates = generator.generate(
        material, versus_signal, topic_type=topic_type, db_path=db_path
    )

    return candidates
