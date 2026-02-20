"""
Translation Cross-Checker (TRAN-02)

Validates Claude translations against independent sources (DeepL API, googletrans, deep_translator)
and identifies semantic discrepancies that affect meaning or legal implications.

Approach:
- Uses DeepL API if DEEPL_AUTH_KEY available (priority)
- Falls back to googletrans or deep_translator (free alternatives)
- Compares translations using Claude API for semantic difference detection
- Filters out stylistic differences (shall/will, word order variations)
- Produces both inline flags per clause and summary report
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional, Callable

try:
    import anthropic
except ImportError:
    anthropic = None

from env_loader import load_api_key, wrap_api_error

try:
    import requests
except ImportError:
    requests = None

# Try optional translation backends
try:
    from googletrans import Translator as GoogleTranslator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False

try:
    from deep_translator import GoogleTranslator as DeepTranslatorGoogle
    DEEP_TRANSLATOR_AVAILABLE = True
except ImportError:
    DEEP_TRANSLATOR_AVAILABLE = False


class CrossChecker:
    """
    Cross-check Claude translations against independent sources.

    Priority order:
    1. DeepL API (if DEEPL_AUTH_KEY set)
    2. googletrans library (free)
    3. deep_translator library (free)

    Semantic comparison uses Claude API to filter stylistic differences.
    """

    def __init__(self, deepl_api_key: Optional[str] = None):
        """
        Initialize cross-checker with optional DeepL API key.

        Args:
            deepl_api_key: DeepL API key (or reads from DEEPL_AUTH_KEY env var)
        """
        # Check for DeepL API key
        self.deepl_key = deepl_api_key or os.environ.get('DEEPL_AUTH_KEY')

        # Initialize Claude client for semantic comparison
        self.client = None
        self.error = None

        if anthropic is None:
            self.error = "anthropic package not installed. Run: pip install anthropic>=0.40.0"
            return

        # Check for API key (reads from .env file or environment variable)
        key_result = load_api_key()
        if 'error' in key_result:
            self.error = key_result['error']
            return
        api_key = key_result['key']

        try:
            self.client = anthropic.Anthropic(api_key=api_key)
        except Exception as e:
            self.error = f"Failed to initialize Anthropic client: {str(e)}"

    def _get_available_backends(self) -> List[str]:
        """
        Get list of available translation backends.

        Returns:
            List of backend names in priority order
        """
        backends = []

        # DeepL (priority if API key available)
        if self.deepl_key and requests:
            backends.append('deepl')

        # googletrans
        if GOOGLETRANS_AVAILABLE:
            backends.append('googletrans')

        # deep_translator
        if DEEP_TRANSLATOR_AVAILABLE:
            backends.append('deep_translator')

        return backends

    def _map_language_code(self, language: str, backend: str) -> str:
        """
        Map language name to backend-specific code.

        Args:
            language: Language name (e.g., 'french', 'spanish')
            backend: Backend name ('deepl', 'googletrans', 'deep_translator')

        Returns:
            Backend-specific language code
        """
        language = language.lower()

        # DeepL codes (uppercase, specific format)
        if backend == 'deepl':
            deepl_map = {
                'french': 'FR',
                'spanish': 'ES',
                'german': 'DE',
                'italian': 'IT',
                'portuguese': 'PT',
                'dutch': 'NL',
                'polish': 'PL',
                'russian': 'RU',
                'chinese': 'ZH',
                'japanese': 'JA'
            }
            return deepl_map.get(language, 'EN')

        # Google Translate codes (lowercase, ISO 639-1)
        else:
            google_map = {
                'french': 'fr',
                'spanish': 'es',
                'german': 'de',
                'italian': 'it',
                'portuguese': 'pt',
                'dutch': 'nl',
                'polish': 'pl',
                'russian': 'ru',
                'chinese': 'zh',
                'japanese': 'ja',
                'latin': 'la'
            }
            return google_map.get(language, 'en')

    def _translate_with_backend(self, text: str, source_lang: str,
                               target_lang: str = 'en', backend: str = 'deepl') -> Dict[str, Any]:
        """
        Translate text using specified backend.

        Args:
            text: Text to translate
            source_lang: Source language name
            target_lang: Target language (default 'en')
            backend: Backend to use ('deepl', 'googletrans', 'deep_translator')

        Returns:
            {'translation': str, 'backend': str} on success
            {'error': msg} on failure
        """
        if not text or not text.strip():
            return {'error': 'Text cannot be empty'}

        try:
            if backend == 'deepl':
                # DeepL API
                if not self.deepl_key:
                    return {'error': 'DeepL API key not available'}

                if not requests:
                    return {'error': 'requests library not installed'}

                # Determine API endpoint (free vs paid)
                endpoint = 'https://api-free.deepl.com/v2/translate'
                if not self.deepl_key.endswith(':fx'):
                    endpoint = 'https://api.deepl.com/v2/translate'

                source_code = self._map_language_code(source_lang, 'deepl')

                response = requests.post(
                    endpoint,
                    headers={'Authorization': f'DeepL-Auth-Key {self.deepl_key}'},
                    data={
                        'text': text,
                        'source_lang': source_code,
                        'target_lang': 'EN-US'
                    }
                )

                if response.status_code != 200:
                    return {'error': f'DeepL API error: {response.status_code} - {response.text}'}

                result = response.json()
                translation = result['translations'][0]['text']
                return {'translation': translation, 'backend': 'deepl'}

            elif backend == 'googletrans':
                # googletrans library
                if not GOOGLETRANS_AVAILABLE:
                    return {'error': 'googletrans not installed'}

                source_code = self._map_language_code(source_lang, 'googletrans')
                translator = GoogleTranslator()
                result = translator.translate(text, src=source_code, dest='en')
                return {'translation': result.text, 'backend': 'googletrans'}

            elif backend == 'deep_translator':
                # deep_translator library
                if not DEEP_TRANSLATOR_AVAILABLE:
                    return {'error': 'deep_translator not installed'}

                source_code = self._map_language_code(source_lang, 'deep_translator')
                translator = DeepTranslatorGoogle(source=source_code, target='en')
                translation = translator.translate(text)
                return {'translation': translation, 'backend': 'deep_translator'}

            else:
                return {'error': f'Unknown backend: {backend}'}

        except Exception as e:
            return {'error': f'{backend} translation failed: {str(e)}'}

    def _compare_translations(self, original: str, claude_translation: str,
                            independent_translation: str, source_language: str,
                            backend: str) -> Dict[str, Any]:
        """
        Compare two translations using Claude API for semantic difference detection.

        Args:
            original: Original text
            claude_translation: Claude's translation
            independent_translation: Independent backend's translation
            source_language: Source language name
            backend: Backend name used

        Returns:
            {'has_discrepancy': bool, 'severity': str, 'explanation': str, 'recommendation': str}
            {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

        system_prompt = """You are a translation quality assessor. Compare two translations of the same text.

Identify SEMANTIC differences only — changes in meaning, missing information, altered legal implications.

IGNORE stylistic differences:
- "shall" vs "will" when they mean the same obligation
- "may" vs "can" when synonymous
- Word order variations that don't change meaning
- Passive vs active voice when meaning unchanged
- "the" vs "a" when not legally significant

Respond in JSON format."""

        user_prompt = f"""Original ({source_language}):
{original}

Translation A (Claude):
{claude_translation}

Translation B ({backend}):
{independent_translation}

Are there semantic differences? Respond in JSON:
{{
  "has_discrepancy": true/false,
  "severity": "none"|"minor"|"significant",
  "explanation": "1-2 sentence description of the difference",
  "recommendation": "what to do about it (accept Claude/accept {backend}/needs review)"
}}"""

        try:
            response = self.client.messages.create(
                model='claude-sonnet-4-20250514',
                max_tokens=500,
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

            # Validate required fields
            if not all(k in result for k in ['has_discrepancy', 'severity', 'explanation', 'recommendation']):
                return {'error': 'Invalid response format from Claude API'}

            return result

        except json.JSONDecodeError as e:
            return {'error': f'Failed to parse Claude response as JSON: {str(e)}'}
        except Exception as e:
            return {'error': wrap_api_error(e)}

    def check_clause(self, original: str, claude_translation: str,
                    source_language: str, clause_id: str) -> Dict[str, Any]:
        """
        Cross-check a single clause translation.

        Args:
            original: Original text
            claude_translation: Claude's translation
            source_language: Source language name
            clause_id: Clause identifier (e.g., 'article-1')

        Returns:
            {
                'clause_id': str,
                'has_discrepancy': bool,
                'severity': str,
                'claude_translation': str,
                'independent_translation': str,
                'backend': str,
                'explanation': str,
                'recommendation': str
            }
            {'error': msg} on failure
        """
        if self.error:
            return {'error': self.error}

        # Get available backends
        backends = self._get_available_backends()
        if not backends:
            return {'error': 'No cross-check backends available'}

        # Use first available backend
        backend = backends[0]

        # Get independent translation
        translation_result = self._translate_with_backend(original, source_language, 'en', backend)

        if 'error' in translation_result:
            return translation_result

        independent_translation = translation_result['translation']

        # Compare translations
        comparison_result = self._compare_translations(
            original, claude_translation, independent_translation,
            source_language, backend
        )

        if 'error' in comparison_result:
            return comparison_result

        # Combine results
        return {
            'clause_id': clause_id,
            'has_discrepancy': comparison_result['has_discrepancy'],
            'severity': comparison_result['severity'],
            'claude_translation': claude_translation,
            'independent_translation': independent_translation,
            'backend': backend,
            'explanation': comparison_result['explanation'],
            'recommendation': comparison_result['recommendation']
        }

    def check_document(self, sections: List[Dict], source_language: str,
                      on_progress: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Cross-check all translated sections.

        Args:
            sections: List of section dicts with 'id', 'original', 'translation' keys
            source_language: Source language name
            on_progress: Optional callback(current, total, clause_id)

        Returns:
            {
                'results': List[Dict],
                'summary': {
                    'total_clauses': int,
                    'discrepancies_found': int,
                    'significant_count': int,
                    'minor_count': int
                },
                'backend_used': str
            }
            {'error': msg, 'skipped': True} if no backends available
        """
        if self.error:
            return {'error': self.error}

        # Check available backends
        backends = self._get_available_backends()
        if not backends:
            return {
                'error': 'No cross-check backends available. Install googletrans (pip install googletrans==4.0.0-rc1) or set DEEPL_AUTH_KEY.',
                'skipped': True
            }

        backend_used = backends[0]
        results = []
        total = len(sections)

        discrepancies_found = 0
        significant_count = 0
        minor_count = 0

        for i, section in enumerate(sections, 1):
            if on_progress:
                on_progress(i, total, section.get('id', f'section-{i}'))

            # Check clause
            check_result = self.check_clause(
                section.get('original', ''),
                section.get('translation', ''),
                source_language,
                section.get('id', f'section-{i}')
            )

            if 'error' in check_result:
                # Individual clause failure - record but continue
                check_result = {
                    'clause_id': section.get('id', f'section-{i}'),
                    'has_discrepancy': False,
                    'severity': 'error',
                    'explanation': check_result['error'],
                    'recommendation': 'Manual review required'
                }

            results.append(check_result)

            # Update counts
            if check_result.get('has_discrepancy', False):
                discrepancies_found += 1
                if check_result.get('severity') == 'significant':
                    significant_count += 1
                elif check_result.get('severity') == 'minor':
                    minor_count += 1

        summary = {
            'total_clauses': total,
            'discrepancies_found': discrepancies_found,
            'significant_count': significant_count,
            'minor_count': minor_count
        }

        return {
            'results': results,
            'summary': summary,
            'backend_used': backend_used
        }

    def format_report(self, check_results: Dict) -> str:
        """
        Format cross-check results as markdown.

        Args:
            check_results: Output from check_document()

        Returns:
            Markdown-formatted report
        """
        if 'error' in check_results:
            return f"# Cross-Check Report\n\nERROR: {check_results['error']}\n"

        summary = check_results['summary']
        results = check_results['results']
        backend = check_results.get('backend_used', 'unknown')

        # Header
        report = "# Cross-Check Summary\n\n"
        report += f"**Backend Used:** {backend}\n"
        report += f"**Total Clauses:** {summary['total_clauses']}\n"
        report += f"**Discrepancies Found:** {summary['discrepancies_found']} "
        report += f"({summary['significant_count']} significant, {summary['minor_count']} minor)\n\n"

        # Per-clause results
        report += "## Clause-by-Clause Results\n\n"

        for result in results:
            clause_id = result.get('clause_id', 'unknown')
            has_discrepancy = result.get('has_discrepancy', False)

            if has_discrepancy:
                severity = result.get('severity', 'unknown')
                report += f"### {clause_id} — DISCREPANCY ({severity})\n\n"
                report += f"**Claude:**\n{result.get('claude_translation', 'N/A')}\n\n"
                report += f"**{backend}:**\n{result.get('independent_translation', 'N/A')}\n\n"
                report += f"**Difference:** {result.get('explanation', 'N/A')}\n\n"
                report += f"**Recommendation:** {result.get('recommendation', 'N/A')}\n\n"
            else:
                report += f"**{clause_id}** — ✓ No discrepancy\n\n"

        return report
