"""
Translation Data Processor (TRAN-01)

Pure data processor for translation payloads. LLM calls handled by Claude Code via /translate command.

Builds structured payloads (system_prompt, user_prompt, clause_id) for Claude Code to execute natively.
Parses raw LLM response text into structured translation results.

No Anthropic SDK. No API keys. No LLM calls.
"""

from typing import Dict, Any, List, Optional, Callable


# System prompt kept in Python (domain knowledge stays with the data layer per RESEARCH.md Pitfall 1 option b)
TRANSLATION_SYSTEM_PROMPT = """You are a legal and historical document translator specializing in faithful clause-by-clause translation.

Your priorities:
1. Accuracy and precision over readability
2. Preserve the original's register and formality
3. Do not paraphrase or simplify
4. If a term has no direct English equivalent, translate it as closely as possible and note the difficulty
5. Flag any ambiguous passages or alternative renderings

Output format:
TRANSLATION:
[Your faithful translation here]

NOTES:
- [Any observations about ambiguous terms, alternative renderings, or translation difficulties]
- [One note per line, or "None" if no issues]"""


class TranslationDataBuilder:
    """
    Pure data processor for translation payloads. No LLM calls. No API keys.

    Usage pattern (via /translate slash command):
        builder = TranslationDataBuilder()
        payload = builder.build_translation_payload(clause_text, full_document, source_language, clause_id)
        # Claude Code executes: payload['system_prompt'] + payload['user_prompt'] with claude-sonnet-4-6
        result = builder.parse_response(response_text, clause_id, original_text)
    """

    def __init__(self):
        """No arguments needed — no model, no API key, no client."""
        pass

    def build_translation_payload(self, clause_text: str, full_document: str,
                                   source_language: str, clause_id: str,
                                   document_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a structured payload for Claude Code to execute natively.

        Args:
            clause_text: The clause text to translate
            full_document: Full document text for context
            source_language: Source language (e.g., 'french', 'spanish', 'german')
            clause_id: Clause identifier (e.g., 'article-1')
            document_context: Optional context (e.g., "1940 French statute defining Jewish status")

        Returns:
            Dict with keys:
            - 'clause_id': Clause identifier
            - 'original': Original clause text
            - 'system_prompt': TRANSLATION_SYSTEM_PROMPT constant
            - 'user_prompt': Fully built user prompt string
        """
        if not clause_text or not clause_text.strip():
            return {'error': 'Clause text cannot be empty'}

        if not source_language:
            return {'error': 'Source language required'}

        # Build highlighted document context
        highlighted_doc = self._highlight_clause(full_document, clause_text)

        # Build user prompt
        user_prompt = self._build_translation_prompt(
            highlighted_doc, source_language, clause_id, document_context
        )

        return {
            'clause_id': clause_id,
            'original': clause_text,
            'system_prompt': TRANSLATION_SYSTEM_PROMPT,
            'user_prompt': user_prompt
        }

    def parse_response(self, response_text: str, clause_id: str,
                       original_text: str) -> Dict[str, Any]:
        """
        Parse Claude's response text into a structured translation result.

        Args:
            response_text: Raw text response from Claude
            clause_id: Clause identifier (passed through to result)
            original_text: Original clause text (passed through to result)

        Returns:
            Dict with keys:
            - 'clause_id': Clause identifier
            - 'original': Original clause text
            - 'translation': Extracted English translation
            - 'notes': List of translator observations
        """
        translation, notes = self._parse_translation_response(response_text)
        return {
            'clause_id': clause_id,
            'original': original_text,
            'translation': translation,
            'notes': notes
        }

    def _highlight_clause(self, full_document: str, clause_text: str) -> str:
        """
        Highlight the active clause within full document.

        Returns:
            Document with active clause wrapped in >>> TRANSLATE THIS CLAUSE <<< markers
        """
        # Find clause in document
        clause_start = full_document.find(clause_text)

        if clause_start == -1:
            # Clause not found - return document with clause appended
            return f"{full_document}\n\n>>> TRANSLATE THIS CLAUSE <<<\n{clause_text}\n>>> END CLAUSE <<<"

        # Insert markers
        before = full_document[:clause_start]
        after = full_document[clause_start + len(clause_text):]
        return f"{before}>>> TRANSLATE THIS CLAUSE <<<\n{clause_text}\n>>> END CLAUSE <<<{after}"

    def _build_translation_prompt(self, highlighted_doc: str, source_language: str,
                                  clause_id: str,
                                  document_context: Optional[str]) -> str:
        """Build user prompt for translation."""
        prompt_parts = [
            f"Translate the highlighted clause from {source_language.capitalize()} to English.\n"
        ]

        if document_context:
            prompt_parts.append(f"Document context: {document_context}\n")

        prompt_parts.append(f"Clause ID: {clause_id}\n")
        prompt_parts.append("Full document for context:\n")
        prompt_parts.append("---")
        prompt_parts.append(highlighted_doc)
        prompt_parts.append("---\n")
        prompt_parts.append(
            "Translate the highlighted clause faithfully. "
            "Preserve legal/technical meaning. Do not paraphrase or simplify. "
            "If a term has no direct English equivalent, translate it as closely as possible and note the difficulty."
        )

        return '\n'.join(prompt_parts)

    def _parse_translation_response(self, content: str) -> tuple:
        """
        Parse Claude response into translation and notes.

        Returns:
            (translation_text, notes_list)
        """
        # Split on NOTES: marker
        if 'NOTES:' in content:
            parts = content.split('NOTES:', 1)
            translation_part = parts[0]
            notes_part = parts[1] if len(parts) > 1 else ''
        else:
            translation_part = content
            notes_part = ''

        # Extract translation (after TRANSLATION: marker if present)
        if 'TRANSLATION:' in translation_part:
            translation = translation_part.split('TRANSLATION:', 1)[1].strip()
        else:
            translation = translation_part.strip()

        # Parse notes
        notes = []
        if notes_part.strip() and notes_part.strip().lower() != 'none':
            for line in notes_part.strip().split('\n'):
                line = line.strip()
                # Remove leading dash/bullet
                if line.startswith('-'):
                    line = line[1:].strip()
                if line and line.lower() != 'none':
                    notes.append(line)

        return translation, notes
