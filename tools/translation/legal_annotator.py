"""
Legal Term Annotator (TRAN-03)

Pure data processor. LLM calls handled by Claude Code via /translate command.

Identifies legal/technical terms with no direct English equivalent and provides
payload builders for annotation via Claude Code, plus response parsers.

Approach:
- Provides build_annotation_payload() for Claude Code to execute LLM annotation
- Provides parse_annotation_response() to parse Claude's structured response
- Focuses on terms with genuine translation difficulty (not every legal term)
- Formats as footnotes for clean split-screen display
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional, Callable


class LegalAnnotator:
    """
    Annotate legal/technical terms in translated documents.

    Pure data processor — no Anthropic SDK or API key needed.
    Claude Code executes LLM calls using payloads from build_annotation_payload().

    Identifies terms with no direct English equivalent and provides:
    - Source-language dictionary definition
    - Closest English equivalent used
    - Alternative English renderings
    - Historical context when relevant
    - Mistranslation flags for common errors
    """

    def build_annotation_payload(self, clause_text: str, translation: str,
                                 clause_id: str, source_language: str = 'unknown',
                                 document_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a Claude Code payload for legal term annotation.

        Claude Code executes the LLM call using this payload.

        Args:
            clause_text: Original source-language clause text
            translation: English translation of the clause
            clause_id: Clause identifier (e.g., 'article-1')
            source_language: Source language name (for prompt context)
            document_context: Optional document context (e.g., "1940 Vichy statute")

        Returns:
            {
                'clause_id': str,
                'system_prompt': str,
                'user_prompt': str
            }
        """
        system_prompt = """You are a legal and historical terminology expert.

Analyze the original-language legal text and its English translation.

Identify terms that have NO direct English equivalent — terms where the translation is an approximation or where the concept doesn't exist in English legal tradition.

For each such term, provide:
1. The original term in the source language
2. The dictionary definition in the source language (what it means in legal context)
3. The closest English equivalent used in the translation
4. Alternative English renderings (other ways this could be translated)
5. Historical context if the term had a different meaning in the historical period vs modern usage
6. Whether this term is commonly rendered DIFFERENTLY in English-language discussions (mistranslation flag)
7. A brief note explaining the translation difficulty

ONLY annotate terms with genuine translation difficulty — not every legal term. Focus on:
- Legal concepts unique to that jurisdiction
- Historical-period specific terms
- Terms that have evolved in meaning
- Terms commonly mistranslated or misunderstood

Respond in JSON format."""

        context_info = f"\n\nDocument context: {document_context}" if document_context else ""

        user_prompt = f"""Original ({source_language}):
{clause_text}

Translation (English):
{translation}{context_info}

Identify terms with no direct English equivalent. Respond in JSON:
{{
  "annotations": [
    {{
      "original_term": "term in source language",
      "source_language_definition": "dictionary definition in legal context",
      "english_equivalent": "the translation used",
      "alternatives": ["alternative 1", "alternative 2"],
      "historical_context": "if relevant, how historical meaning differs from modern",
      "commonly_mistranslated": true/false,
      "common_mistranslation": "if commonly mistranslated, what is the common error",
      "note": "1-2 sentence explanation of the translation difficulty"
    }}
  ]
}}

If no terms require annotation, return {{"annotations": []}}"""

        return {
            'clause_id': clause_id,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_annotation_response(self, response_text: str, clause_id: str) -> Dict[str, Any]:
        """
        Parse Claude Code's annotation response into a structured result.

        Args:
            response_text: Raw text response from Claude Code
            clause_id: Clause identifier

        Returns:
            {
                'clause_id': str,
                'annotations': List[Dict],
                'footnotes': List[str]
            }
            {'clause_id': str, 'error': str} on parse failure
        """
        # Extract JSON from response (may be wrapped in markdown code block)
        text = response_text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()

        try:
            result = json.loads(text)
        except json.JSONDecodeError as e:
            return {'clause_id': clause_id, 'error': f'Failed to parse response as JSON: {str(e)}'}

        if 'annotations' not in result:
            return {'clause_id': clause_id, 'error': 'Response missing annotations field'}

        annotations = result['annotations']
        footnotes = self.format_footnotes(annotations)

        return {
            'clause_id': clause_id,
            'annotations': annotations,
            'footnotes': footnotes
        }

    def format_footnotes(self, annotations: List[Dict]) -> List[str]:
        """
        Convert annotation dicts to numbered footnote strings.

        Args:
            annotations: List of annotation dicts

        Returns:
            List of formatted footnote strings
        """
        if not annotations:
            return []

        footnotes = []

        for i, ann in enumerate(annotations, 1):
            # Skip if missing required fields
            if not ann.get('original_term') or not ann.get('english_equivalent'):
                continue

            # Build footnote
            footnote = f"**{ann['english_equivalent']}**"

            # Original term
            if ann.get('original_term'):
                footnote += f" (original: *{ann['original_term']}*)"

            footnote += ": "

            # Definition
            if ann.get('source_language_definition'):
                footnote += ann['source_language_definition']
            else:
                footnote += "No direct English equivalent."

            # English equivalent
            footnote += f" English equivalent: \"{ann['english_equivalent']}\"."

            # Alternatives
            if ann.get('alternatives') and len(ann['alternatives']) > 0:
                alternatives_str = ", ".join(f"\"{alt}\"" for alt in ann['alternatives'])
                footnote += f" Alternatives: {alternatives_str}."

            # Historical context
            if ann.get('historical_context'):
                footnote += f" Historical note: {ann['historical_context']}"

            # Mistranslation warning
            if ann.get('commonly_mistranslated', False):
                common_error = ann.get('common_mistranslation', 'unknown')
                note = ann.get('note', '')
                footnote += f" **WARNING:** Commonly rendered as \"{common_error}\" in English-language sources"
                if note:
                    footnote += f" — this is misleading because {note.lower()}"
                footnote += "."

            footnotes.append(footnote)

        return footnotes
