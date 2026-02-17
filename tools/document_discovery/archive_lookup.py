"""
Archive Lookup (DISC-03)

Locates digitized originals across major archives and scholarly edition databases.
Always prioritizes academic/critical editions over free archive versions.

Extensible ARCHIVE_REGISTRY design allows adding country-specific archives by appending to list.
"""

from typing import Dict, Any, List, Optional
from urllib.parse import quote_plus


# Archive Registry - Extensible design for country-specific archives
ARCHIVE_REGISTRY = [
    # Academic/Critical Editions (Priority 1)
    {
        'name': 'Google Scholar (Critical Editions)',
        'url_template': 'https://scholar.google.com/scholar?q="{query}"+critical+edition',
        'category': 'Academic Editions',
        'languages': ['all'],
        'description': 'Scholarly critical editions with academic apparatus'
    },
    {
        'name': 'WorldCat',
        'url_template': 'https://www.worldcat.org/search?q={query}',
        'category': 'Academic Editions',
        'languages': ['all'],
        'description': 'Global library catalog (find critical editions via university libraries)'
    },

    # French Archives
    {
        'name': 'Légifrance',
        'url_template': 'https://www.legifrance.gouv.fr/search/all?tab=all&searchField={query}',
        'category': 'Government Archives',
        'languages': ['french'],
        'description': 'Official French legal database (laws, decrees, regulations)'
    },
    {
        'name': 'Gallica (BnF)',
        'url_template': 'https://gallica.bnf.fr/services/engine/search/sru?operation=searchRetrieve&version=1.2&query={query}',
        'category': 'National Libraries',
        'languages': ['french'],
        'description': 'Bibliothèque nationale de France digital library'
    },

    # Wikisource (multilingual)
    {
        'name': 'Wikisource (French)',
        'url_template': 'https://fr.wikisource.org/wiki/Special:Search?search={query}',
        'category': 'Free Archives',
        'languages': ['french'],
        'description': 'Free library of source texts (French)'
    },
    {
        'name': 'Wikisource (Spanish)',
        'url_template': 'https://es.wikisource.org/wiki/Special:Search?search={query}',
        'category': 'Free Archives',
        'languages': ['spanish'],
        'description': 'Free library of source texts (Spanish)'
    },
    {
        'name': 'Wikisource (German)',
        'url_template': 'https://de.wikisource.org/wiki/Special:Search?search={query}',
        'category': 'Free Archives',
        'languages': ['german'],
        'description': 'Free library of source texts (German)'
    },
    {
        'name': 'Wikisource (Latin)',
        'url_template': 'https://la.wikisource.org/wiki/Special:Search?search={query}',
        'category': 'Free Archives',
        'languages': ['latin'],
        'description': 'Free library of source texts (Latin)'
    },
    {
        'name': 'Wikisource (Italian)',
        'url_template': 'https://it.wikisource.org/wiki/Special:Search?search={query}',
        'category': 'Free Archives',
        'languages': ['italian'],
        'description': 'Free library of source texts (Italian)'
    },

    # International Archives
    {
        'name': 'Internet Archive',
        'url_template': 'https://archive.org/search?query={query}',
        'category': 'Free Archives',
        'languages': ['all'],
        'description': 'Massive digital library (books, documents, government publications)'
    },
    {
        'name': 'Google Books',
        'url_template': 'https://books.google.com/books?q={query}',
        'category': 'Free Archives',
        'languages': ['all'],
        'description': 'Searchable book previews and full texts'
    },
    {
        'name': 'HathiTrust',
        'url_template': 'https://catalog.hathitrust.org/Search/Home?lookfor={query}',
        'category': 'Free Archives',
        'languages': ['all'],
        'description': 'Digital library partnership (universities, public domain works)'
    },
    {
        'name': 'Europeana',
        'url_template': 'https://www.europeana.eu/en/search?query={query}',
        'category': 'Free Archives',
        'languages': ['all'],
        'description': 'European cultural heritage collections'
    },
    {
        'name': 'Library of Congress',
        'url_template': 'https://www.loc.gov/search/?q={query}',
        'category': 'National Libraries',
        'languages': ['all'],
        'description': 'US national library and archives'
    },
]


class ArchiveLookup:
    """
    Locate digitized originals across major archives and scholarly editions.

    Always prioritizes academic/critical editions (scholarly apparatus, peer review).
    Free archive versions supplement but don't replace critical editions.
    """

    def __init__(self):
        """Initialize archive lookup."""
        self.registry = ARCHIVE_REGISTRY

    def lookup(self, query: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Locate digitized originals across archives.

        Args:
            query: Document description (e.g., "Statut des Juifs 1940")
            language: Optional language hint ('french', 'spanish', 'german', 'latin', etc.)
                     If not provided, returns all archives

        Returns:
            Dict with keys:
            - 'query': Original query
            - 'language': Language hint (or 'all' if not specified)
            - 'archives': List of archive search URLs
            - 'priority_note': Explanation of academic edition priority

            Or {'error': str} on failure
        """
        if not query or not query.strip():
            return {'error': 'Query cannot be empty'}

        query = query.strip()
        language = language.lower() if language else 'all'

        try:
            archives = []

            for archive in self.registry:
                # Filter by language if specified
                if language != 'all':
                    if 'all' not in archive['languages'] and language not in archive['languages']:
                        continue

                # Build search URL
                encoded_query = quote_plus(query)
                search_url = archive['url_template'].replace('{query}', encoded_query)

                archives.append({
                    'name': archive['name'],
                    'category': archive['category'],
                    'search_url': search_url,
                    'description': archive['description']
                })

            if not archives:
                return {
                    'error': f'No archives found for language "{language}". Try "all" or check spelling.'
                }

            return {
                'query': query,
                'language': language,
                'archives': archives,
                'priority_note': (
                    "Academic/critical editions listed first. These are preferred for:\n"
                    "  - Scholarly apparatus (annotations, context, commentary)\n"
                    "  - Peer review and verification\n"
                    "  - Professional translation (if bilingual edition)\n"
                    "  - Authoritative text with provenance\n\n"
                    "Free archive versions supplement but don't replace critical editions. "
                    "Use them for:\n"
                    "  - Initial access and preview\n"
                    "  - Cross-checking against critical edition\n"
                    "  - Public domain facsimiles"
                )
            }

        except Exception as e:
            return {'error': f'Archive lookup failed: {str(e)}'}

    def add_archive(self, name: str, url_template: str, category: str,
                   languages: List[str], description: str) -> None:
        """
        Add a new archive to the registry (for country-specific archives).

        Args:
            name: Archive name (e.g., "Biblioteca Nacional de España")
            url_template: URL with {query} placeholder
            category: One of 'Academic Editions', 'Government Archives',
                     'National Libraries', 'Free Archives'
            languages: List of language codes (e.g., ['spanish']) or ['all']
            description: Brief description of archive contents
        """
        self.registry.append({
            'name': name,
            'url_template': url_template,
            'category': category,
            'languages': languages,
            'description': description
        })

    def list_archives(self, language: Optional[str] = None) -> List[str]:
        """
        List all available archives.

        Args:
            language: Optional language filter

        Returns:
            List of archive names
        """
        if language:
            language = language.lower()
            return [
                archive['name'] for archive in self.registry
                if 'all' in archive['languages'] or language in archive['languages']
            ]
        return [archive['name'] for archive in self.registry]
