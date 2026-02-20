"""
Claude-based Document Translator (TRAN-01)

Clause-by-clause translation with full document context for legal/historical accuracy.
Uses Anthropic Claude API for faithful translation preserving legal register.
"""

import os
import sys
from typing import Dict, Any, List, Optional, Callable

try:
    import anthropic
except ImportError:
    anthropic = None

from env_loader import load_api_key, wrap_api_error


class Translator:
    """
    Translate legal/historical documents clause-by-clause using Claude API.

    Approach:
    - Each clause translated with full document context (active clause highlighted)
    - Preserves legal/technical meaning and formal register
    - Flags terms with no direct English equivalent
    - Notes ambiguous passages
    """

    def __init__(self, model: str = 'claude-sonnet-4-20250514'):
        """
        Initialize translator with Claude API client.

        Args:
            model: Claude model to use for translation

        Returns error dict if anthropic SDK not installed or API key missing.
        """
        self.model = model
        self.client = None
        self.error = None

        # Check for anthropic SDK
        if anthropic is None:
            self.error = "anthropic package not installed. Run: pip install anthropic>=0.40.0"
            return

        # Check for API key (reads from .env file or environment variable)
        key_result = load_api_key()
        if 'error' in key_result:
            self.error = key_result['error']
            return
        api_key = key_result['key']

        # Initialize client
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            self.error = f"Failed to initialize Anthropic client: {str(e)}"

    def translate_clause(self, clause_text: str, full_document: str,
                        source_language: str, clause_id: str,
                        document_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Translate a single clause with full document context.

        Args:
            clause_text: The clause text to translate
            full_document: Full document text for context
            source_language: Source language (e.g., 'french', 'spanish', 'german')
            clause_id: Clause identifier (e.g., 'article-1')
            document_context: Optional context (e.g., "1940 French statute defining Jewish status")

        Returns:
            Dict with keys:
            - 'clause_id': Clause identifier
            - 'original': Original text
            - 'translation': English translation
            - 'notes': List of translator observations
            - 'model': Model used

            Or {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

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

        # System prompt
        system_prompt = """You are a legal and historical document translator specializing in faithful clause-by-clause translation.

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

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,  # Lower temperature for consistency
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Parse response
            content = response.content[0].text
            translation, notes = self._parse_translation_response(content)

            return {
                'clause_id': clause_id,
                'original': clause_text,
                'translation': translation,
                'notes': notes,
                'model': self.model
            }

        except Exception as e:
            return {'error': wrap_api_error(e)}

    def translate_document(self, sections: List[Dict], source_language: str,
                          full_text: str, document_context: Optional[str] = None,
                          on_progress: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Translate all document sections sequentially.

        Args:
            sections: List of section dicts from structure_detector (id, heading, body)
            source_language: Source language
            full_text: Full document text for context
            document_context: Optional document context
            on_progress: Optional callback(current_index, total_count, clause_id)

        Returns:
            Dict with keys:
            - 'sections': List of translated section dicts
            - 'source_language': Source language
            - 'model': Model used
            - 'clause_count': Number of clauses translated

            Or {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

        if not sections:
            return {'error': 'No sections provided'}

        translated_sections = []
        total_count = len(sections)

        for i, section in enumerate(sections):
            clause_id = section.get('id', f'section-{i+1}')
            heading = section.get('heading', clause_id)
            body = section.get('body', '')

            # Skip empty sections
            if not body.strip():
                translated_sections.append({
                    'id': clause_id,
                    'heading': heading,
                    'original': body,
                    'translation': '',
                    'notes': []
                })
                continue

            # Progress callback
            if on_progress:
                on_progress(i + 1, total_count, clause_id)

            # Translate clause
            result = self.translate_clause(
                body, full_text, source_language, clause_id, document_context
            )

            if 'error' in result:
                # Include error but continue with other sections
                translated_sections.append({
                    'id': clause_id,
                    'heading': heading,
                    'original': body,
                    'translation': f"[Translation failed: {result['error']}]",
                    'notes': [],
                    'error': result['error']
                })
            else:
                translated_sections.append({
                    'id': clause_id,
                    'heading': heading,
                    'original': result['original'],
                    'translation': result['translation'],
                    'notes': result['notes']
                })

        return {
            'sections': translated_sections,
            'source_language': source_language,
            'model': self.model,
            'clause_count': len(translated_sections)
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
                                 clause_id: str, document_context: Optional[str]) -> str:
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
