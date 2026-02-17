"""
Legal Term Annotator (TRAN-03)

Identifies legal/technical terms with no direct English equivalent and provides
dictionary definitions, historical context, and mistranslation flags.

Approach:
- Uses Claude API to identify terms requiring annotation
- Focuses on terms with genuine translation difficulty (not every legal term)
- Provides source-language definitions and English equivalents
- Notes when historical meaning differs from modern usage
- Flags common mistranslations in English-language sources
- Formats as footnotes for clean split-screen display
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional, Callable

try:
    import anthropic
except ImportError:
    anthropic = None


class LegalAnnotator:
    """
    Annotate legal/technical terms in translated documents.

    Identifies terms with no direct English equivalent and provides:
    - Source-language dictionary definition
    - Closest English equivalent used
    - Alternative English renderings
    - Historical context when relevant
    - Mistranslation flags for common errors
    """

    def __init__(self, model: str = 'claude-sonnet-4-20250514'):
        """
        Initialize annotator with Claude API client.

        Args:
            model: Claude model to use for annotation
        """
        self.model = model
        self.client = None
        self.error = None

        # Check for anthropic SDK
        if anthropic is None:
            self.error = "anthropic package not installed. Run: pip install anthropic>=0.40.0"
            return

        # Check for API key
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            self.error = "ANTHROPIC_API_KEY not set. Export your API key: export ANTHROPIC_API_KEY=sk-..."
            return

        # Initialize client
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            self.error = f"Failed to initialize Anthropic client: {str(e)}"

    def annotate_clause(self, original: str, translation: str, source_language: str,
                       clause_id: str, document_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Annotate legal/technical terms in a single clause.

        Args:
            original: Original text
            translation: English translation
            source_language: Source language name
            clause_id: Clause identifier
            document_context: Optional document context (e.g., "1940 Vichy statute")

        Returns:
            {
                'clause_id': str,
                'annotations': List[{
                    'original_term': str,
                    'source_language_definition': str,
                    'english_equivalent': str,
                    'alternatives': List[str],
                    'historical_context': str|None,
                    'commonly_mistranslated': bool,
                    'common_mistranslation': str|None,
                    'note': str
                }],
                'annotation_count': int
            }
            {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

        if not original or not original.strip():
            return {'error': 'Original text cannot be empty'}

        if not translation or not translation.strip():
            return {'error': 'Translation text cannot be empty'}

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
{original}

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                system=system_prompt,
                messages=[{'role': 'user', 'content': user_prompt}]
            )

            # Parse JSON response
            result_text = response.content[0].text

            # Extract JSON from response (may be wrapped in markdown code block)
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()

            result = json.loads(result_text)

            # Validate format
            if 'annotations' not in result:
                return {'error': 'Invalid response format from Claude API'}

            annotations = result['annotations']

            return {
                'clause_id': clause_id,
                'annotations': annotations,
                'annotation_count': len(annotations)
            }

        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse Claude response as JSON: {str(e)}'}
        except Exception as e:
            return {'error': f'Annotation failed: {str(e)}'}

    def annotate_document(self, sections: List[Dict], source_language: str,
                         document_context: Optional[str] = None,
                         on_progress: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Annotate all translated sections.

        Args:
            sections: List of section dicts with 'id', 'original', 'translation' keys
            source_language: Source language name
            document_context: Optional document context
            on_progress: Optional callback(current, total, clause_id)

        Returns:
            {
                'sections': List[Dict],  # sections with 'footnotes' field added
                'total_annotations': int,
                'mistranslation_flags': int
            }
            {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

        annotated_sections = []
        total = len(sections)
        total_annotations = 0
        mistranslation_flags = 0

        for i, section in enumerate(sections, 1):
            if on_progress:
                on_progress(i, total, section.get('id', f'section-{i}'))

            # Annotate clause
            annotation_result = self.annotate_clause(
                section.get('original', ''),
                section.get('translation', ''),
                source_language,
                section.get('id', f'section-{i}'),
                document_context
            )

            # Copy section data
            annotated_section = section.copy()

            if 'error' in annotation_result:
                # Individual clause failure - record but continue
                annotated_section['footnotes'] = [f"ERROR: {annotation_result['error']}"]
                annotated_section['annotation_count'] = 0
            else:
                # Format footnotes
                footnotes = self.format_footnotes(annotation_result['annotations'])
                annotated_section['footnotes'] = footnotes
                annotated_section['annotation_count'] = annotation_result['annotation_count']

                # Update totals
                total_annotations += annotation_result['annotation_count']
                mistranslation_flags += sum(
                    1 for a in annotation_result['annotations']
                    if a.get('commonly_mistranslated', False)
                )

            annotated_sections.append(annotated_section)

        return {
            'sections': annotated_sections,
            'total_annotations': total_annotations,
            'mistranslation_flags': mistranslation_flags
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
