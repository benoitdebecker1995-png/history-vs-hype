"""
Document Discovery Toolkit

Tools for verifying translation gaps, assessing document structure,
and locating digitized originals across academic archives.

Foundation for the Untranslated Evidence Pipeline (v4.0).

Modules:
    - gap_checker: Verify whether English translations exist
    - structure_assessor: Analyze document structure and estimate video length
    - archive_lookup: Locate digitized originals across archives

Usage:
    from document_discovery import GapChecker, StructureAssessor, ArchiveLookup

    # Check for existing translations
    gc = GapChecker()
    result = gc.check_gap("Statut des Juifs 1940")

    # Assess document structure
    sa = StructureAssessor()
    outline = sa.assess("Statut des Juifs 1940", description="French law")

    # Find digitized originals
    al = ArchiveLookup()
    archives = al.lookup("Statut des Juifs 1940", language="french")
"""

__version__ = "0.1.0"

from .gap_checker import GapChecker
from .structure_assessor import StructureAssessor
from .archive_lookup import ArchiveLookup

__all__ = ["GapChecker", "StructureAssessor", "ArchiveLookup"]
