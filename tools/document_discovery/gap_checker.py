"""
Translation Gap Checker (DISC-01)

Verifies whether an English translation exists for a document across multiple source categories.
Returns structured search URLs for user verification, NOT automated web scraping.

Qualification criteria:
- Document qualifies if (a) no full English translation exists, OR
- (b) existing translations are misleading/distort the original
- Partial translations or summaries do not disqualify
"""

from typing import Dict, Any, List
from urllib.parse import quote_plus


class GapChecker:
    """
    Check for translation gaps across academic sourcebooks, databases, and archives.

    Language-agnostic: works for any document in any language.
    """

    def __init__(self):
        """Initialize gap checker."""
        pass

    def check_gap(self, query: str) -> Dict[str, Any]:
        """
        Check if English translation exists for a document.

        Args:
            query: Free-form document description (e.g., "Statut des Juifs 1940",
                   "Bartolome de las Casas Brevisima relacion")

        Returns:
            Dict with keys:
            - 'query': Original query
            - 'searches': List of search URLs by category
            - 'qualification_criteria': Explanation of what qualifies
            - 'instructions': How to use the results

            Or {'error': str} on failure
        """
        if not query or not query.strip():
            return {'error': 'Query cannot be empty'}

        query = query.strip()

        try:
            searches = []

            # Category 1: Academic sourcebooks
            searches.extend(self._build_academic_sourcebook_searches(query))

            # Category 2: Google Scholar + JSTOR
            searches.extend(self._build_scholar_searches(query))

            # Category 3: Government/institutional translation portals
            searches.extend(self._build_institutional_searches(query))

            # Category 4: General web search
            searches.extend(self._build_web_searches(query))

            return {
                'query': query,
                'searches': searches,
                'qualification_criteria': (
                    "Document qualifies for translation if:\n"
                    "  (a) No full English translation exists, OR\n"
                    "  (b) Existing translations are misleading or distort the original\n\n"
                    "Note: Partial translations or summaries do not disqualify the document."
                ),
                'instructions': (
                    "Open each search URL and verify results manually. "
                    "Look for:\n"
                    "  - Full-text translations (book publications, journal articles)\n"
                    "  - Academic sourcebook inclusions\n"
                    "  - Government/institutional translations\n"
                    "  - Quality of existing translations (check scholar reviews)\n\n"
                    "If no full English translation found across all sources, "
                    "document qualifies for Untranslated Evidence series."
                )
            }

        except Exception as e:
            return {'error': f'Gap check failed: {str(e)}'}

    def _build_academic_sourcebook_searches(self, query: str) -> List[Dict[str, Any]]:
        """Build searches for major academic sourcebook series."""
        encoded = quote_plus(query)

        searches = []

        # Medieval Sourcebook / Internet History Sourcebooks Project
        searches.append({
            'category': 'Academic Sourcebooks',
            'search_url': f'https://www.google.com/search?q="{encoded}"+English+translation+site:fordham.edu',
            'description': 'Internet History Sourcebooks Project (Fordham University)'
        })

        # General academic anthology search
        searches.append({
            'category': 'Academic Sourcebooks',
            'search_url': f'https://scholar.google.com/scholar?q="{encoded}"+English+translation+sourcebook+site:*.edu',
            'description': 'Academic sourcebooks and anthologies (.edu domains)'
        })

        return searches

    def _build_scholar_searches(self, query: str) -> List[Dict[str, Any]]:
        """Build Google Scholar and JSTOR searches."""
        encoded = quote_plus(query)

        searches = []

        # Google Scholar - English translation
        searches.append({
            'category': 'Academic Databases',
            'search_url': f'https://scholar.google.com/scholar?q="{encoded}"+English+translation',
            'description': 'Google Scholar: full translations and critical editions'
        })

        # Google Scholar - "translated by"
        searches.append({
            'category': 'Academic Databases',
            'search_url': f'https://scholar.google.com/scholar?q="{encoded}"+translated',
            'description': 'Google Scholar: published translations'
        })

        # JSTOR search
        searches.append({
            'category': 'Academic Databases',
            'search_url': f'https://www.jstor.org/action/doBasicSearch?Query="{encoded}"+English+translation',
            'description': 'JSTOR: peer-reviewed journal translations'
        })

        return searches

    def _build_institutional_searches(self, query: str) -> List[Dict[str, Any]]:
        """Build government/institutional translation portal searches."""
        encoded = quote_plus(query)

        searches = []

        # Legifrance English (French law)
        searches.append({
            'category': 'Government/Institutional',
            'search_url': f'https://www.google.com/search?q="{encoded}"+site:legifrance.gouv.fr+English',
            'description': 'Legifrance (official French legal translations)'
        })

        # EUR-Lex (EU law)
        searches.append({
            'category': 'Government/Institutional',
            'search_url': f'https://eur-lex.europa.eu/search.html?qid=&text={encoded}&lang=en',
            'description': 'EUR-Lex (EU official translations)'
        })

        # UN Official Documents
        searches.append({
            'category': 'Government/Institutional',
            'search_url': f'https://www.google.com/search?q="{encoded}"+site:un.org+English',
            'description': 'UN Official Documents (international treaties/agreements)'
        })

        return searches

    def _build_web_searches(self, query: str) -> List[Dict[str, Any]]:
        """Build general web searches for full translations."""
        encoded = quote_plus(query)

        searches = []

        # General Google search - full English translation
        searches.append({
            'category': 'General Web',
            'search_url': f'https://www.google.com/search?q="{encoded}"+full+English+translation',
            'description': 'General web: full translations (books, PDFs, websites)'
        })

        # Academic publisher search
        searches.append({
            'category': 'General Web',
            'search_url': f'https://www.google.com/search?q="{encoded}"+English+translation+Cambridge+OR+Oxford+OR+Harvard+OR+Yale',
            'description': 'University presses (Cambridge, Oxford, Harvard, Yale)'
        })

        return searches
