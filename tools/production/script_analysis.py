"""
ScriptAnalysis — unified seam for parser → entities → metadata (PROD-SA)

Replaces the leaky 3-import pattern used by callers that need the full analysis.
Single-purpose callers (only parsing, only metadata) keep their narrow imports.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

from .parser import ScriptParser, Section
from .entities import EntityExtractor, Entity
from .editguide import EditGuideGenerator, SectionTiming
from .metadata import MetadataGenerator


@dataclass
class ScriptAnalysisResult:
    """Cohesive output from a full script analysis run."""
    sections: List[Section] = field(default_factory=list)
    entities: List[Entity] = field(default_factory=list)
    timings: List[SectionTiming] = field(default_factory=list)
    metadata: str = ""
    project_name: str = ""


class ScriptAnalysis:
    """
    Unified script analysis seam.

    Orchestrates ScriptParser → EntityExtractor → MetadataGenerator.
    Callers that need the full pipeline import this; narrow callers keep their imports.

    Usage:
        sa = ScriptAnalysis("path/to/script.md", project_name="14-chagos-2025")
        sections = sa.parse()
        entities = sa.extract_entities()
        metadata = sa.generate_metadata()
        result = sa.run()   # all three stages, returns ScriptAnalysisResult
    """

    def __init__(
        self,
        script: Union[str, Path],
        project_name: str = "",
        use_spacy: bool = False,
    ):
        """
        Args:
            script: Path to markdown script file, or raw markdown string.
            project_name: Used by MetadataGenerator and EditGuideGenerator.
            use_spacy: Pass True to enable spaCy NER in EntityExtractor.
        """
        self._script = script
        self._project_name = project_name
        self._use_spacy = use_spacy

        self._parser = ScriptParser()
        self._extractor = EntityExtractor(use_spacy=use_spacy)
        self._edit_gen = EditGuideGenerator(project_name=project_name)
        self._meta_gen = MetadataGenerator(project_name=project_name)

        # Cached stage results
        self._sections: Optional[List[Section]] = None
        self._entities: Optional[List[Entity]] = None
        self._timings: Optional[List[SectionTiming]] = None

    def parse(self) -> List[Section]:
        """Parse the script into sections. Cached after first call."""
        if self._sections is None:
            path = Path(self._script)
            if path.exists():
                self._sections = self._parser.parse_file(str(path))
            else:
                self._sections = self._parser.parse_text(str(self._script))
        return self._sections

    def extract_entities(self) -> List[Entity]:
        """Extract named entities from parsed sections. Cached after first call."""
        if self._entities is None:
            sections = self.parse()
            self._entities = self._extractor.extract_from_sections(sections)
        return self._entities

    def generate_metadata(
        self,
        entities: Optional[List[Entity]] = None,
    ) -> str:
        """
        Generate metadata draft from parsed sections.

        Args:
            entities: Optional pre-computed entities. If None, runs extract_entities().
        """
        sections = self.parse()
        if entities is None:
            entities = self.extract_entities()
        if self._timings is None:
            self._timings = self._edit_gen.calculate_timing(sections)
        return self._meta_gen.generate_metadata_draft(
            sections=sections,
            entities=entities,
            timings=self._timings,
        )

    def run(self) -> ScriptAnalysisResult:
        """Run all three stages and return a cohesive result object."""
        sections = self.parse()
        entities = self.extract_entities()
        metadata = self.generate_metadata(entities=entities)
        return ScriptAnalysisResult(
            sections=sections,
            entities=entities,
            timings=self._timings or [],
            metadata=metadata,
            project_name=self._project_name,
        )
