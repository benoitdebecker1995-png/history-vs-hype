"""
Document Discovery Toolkit

Foundation for the Untranslated Evidence Pipeline. Provides tools to:
1. Verify translation gaps (check if English translation exists)
2. Assess document structure (article count, video length estimation)
3. Locate digitized originals (academic editions + free archives)

Usage:
    from document_discovery.gap_checker import GapChecker
    from document_discovery.structure_assessor import StructureAssessor
    from document_discovery.archive_lookup import ArchiveLookup

CLI:
    python tools/document_discovery/cli.py gap "Statut des Juifs 1940"
    python tools/document_discovery/cli.py structure "Document name" --type legal_code --sections 10
    python tools/document_discovery/cli.py archive "Document name" --language french
"""

__version__ = "1.0.0"

from .gap_checker import GapChecker
from .structure_assessor import StructureAssessor
from .archive_lookup import ArchiveLookup

__all__ = ['GapChecker', 'StructureAssessor', 'ArchiveLookup']
