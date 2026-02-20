"""
Translation Cross-Checker (TRAN-02)

Pure data processor. LLM calls handled by Claude Code via /translate command.

Validates Claude translations against independent sources (DeepL API, googletrans, deep_translator)
and provides payload builders for semantic discrepancy detection via Claude Code.

Approach:
- Uses DeepL API if DEEPL_AUTH_KEY available (priority)
- Falls back to googletrans or deep_translator (free alternatives)
- Provides build_comparison_payload() for Claude Code to execute semantic comparison
- Provides parse_comparison_response() to parse Claude's structured response
- Filters out stylistic differences (shall/will, word order variations)
- Produces both inline flags per clause and summary report
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional, Callable

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

    Priority order for independent translation:
    1. DeepL API (if DEEPL_AUTH_KEY set)
    2. googletrans library (free)
    3. deep_translator library (free)

    Semantic comparison is done by Claude Code via build_comparison_payload().
    This class is a pure data processor — no Anthropic SDK or API key needed.
    """

    def __init__(self, deepl_api_key: Optional[str] = None):
        """
        Initialize cross-checker with optional DeepL API key.

        Args:
            deepl_api_key: DeepL API key (or reads from DEEPL_AUTH_KEY env var)
        """
        # Check for DeepL API key (not Anthropic — DeepL is the independent backend)
        self.deepl_key = deepl_api_key or os.environ.get('DEEPL_AUTH_KEY')

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
                               target_lang: str = 'en', backend: str = None) -> Dict[str, Any]:
        """
        Translate text using specified backend (DeepL/googletrans — NOT Anthropic).

        This is the independent translation source for cross-checking.

        Args:
            text: Text to translate
            source_lang: Source language name
            target_lang: Target language (default 'en')
            backend: Backend to use ('deepl', 'googletrans', 'deep_translator').
                     If None, uses first available backend.

        Returns:
            {'translation': str, 'backend': str} on success
            {'error': msg} on failure
        """
        if not text or not text.strip():
            return {'error': 'Text cannot be empty'}

        # Auto-select backend if not specified
        if backend is None:
            backends = self._get_available_backends()
            if not backends:
                return {'error': 'No translation backends available'}
            backend = backends[0]

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

    def build_comparison_payload(self, claude_translation: str, backend_translation: str,
                                 original_text: str, clause_id: str,
                                 source_language: str = 'unknown',
                                 backend: str = 'independent') -> Dict[str, Any]:
        """
        Build a Claude Code payload for semantic comparison of two translations.

        Claude Code executes the LLM call using this payload.

        Args:
            claude_translation: Claude's translation of the clause
            backend_translation: Independent backend's translation
            original_text: The original source-language text
            clause_id: Clause identifier (e.g., 'article-1')
            source_language: Source language name (for prompt context)
            backend: Backend name used for independent translation (for prompt context)

        Returns:
            {
                'clause_id': str,
                'system_prompt': str,
                'user_prompt': str
            }
        """
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
{original_text}

Translation A (Claude):
{claude_translation}

Translation B ({backend}):
{backend_translation}

Are there semantic differences? Respond in JSON:
{{
  "has_discrepancy": true/false,
  "severity": "none"|"minor"|"significant",
  "explanation": "1-2 sentence description of the difference",
  "recommendation": "what to do about it (accept Claude/accept {backend}/needs review)"
}}"""

        return {
            'clause_id': clause_id,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def parse_comparison_response(self, response_text: str, clause_id: str) -> Dict[str, Any]:
        """
        Parse Claude Code's comparison response into a structured result.

        Args:
            response_text: Raw text response from Claude Code
            clause_id: Clause identifier

        Returns:
            {
                'clause_id': str,
                'has_discrepancy': bool,
                'severity': str,  # 'none'|'minor'|'significant'
                'explanation': str,
                'recommendation': str
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

        # Validate required fields
        required = ['has_discrepancy', 'severity', 'explanation', 'recommendation']
        if not all(k in result for k in required):
            return {'clause_id': clause_id, 'error': 'Response missing required fields'}

        return {
            'clause_id': clause_id,
            'has_discrepancy': result['has_discrepancy'],
            'severity': result['severity'],
            'explanation': result['explanation'],
            'recommendation': result['recommendation']
        }

    def format_report(self, check_results: Dict) -> str:
        """
        Format cross-check results as markdown.

        Args:
            check_results: Dict with 'results', 'summary', 'backend_used' keys

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
                report += f"**{clause_id}** — No discrepancy\n\n"

        return report
