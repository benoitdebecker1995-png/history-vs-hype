"""
Document Structure Assessor (DISC-02)

Analyzes document structure (articles, chapters, sections) and estimates video length.
Generates markdown outlines for planning video scope.

Document types supported:
- legal_code: Statutes, decrees (articles/clauses)
- treaty: Bilateral/multilateral agreements (articles/provisions)
- book: Monographs, chronicles (chapters/sections)
- letter: Diplomatic correspondence (short form)
- decree: Executive orders (sections/clauses)
- other: General documents
"""

from typing import Dict, Any, List, Optional


class StructureAssessor:
    """
    Assess document structure and estimate video production requirements.

    Channel philosophy: "As long as needed — optimize for completeness, not brevity"
    """

    # Video length estimation formulas
    TIMING_ESTIMATES = {
        'legal_code': {
            'per_section': 2,  # minutes per article (read + translate + explain)
            'intro': 2,
            'conclusion': 2
        },
        'treaty': {
            'per_section': 2.5,  # minutes per article (context + translation + analysis)
            'intro': 2,
            'conclusion': 2
        },
        'book': {
            'per_section': 6,  # minutes per chapter (summary + key passages + analysis)
            'intro': 3,
            'conclusion': 3
        },
        'letter': {
            'per_section': 1,  # minutes per paragraph
            'intro': 1,
            'conclusion': 1
        },
        'decree': {
            'per_section': 2,  # minutes per section
            'intro': 2,
            'conclusion': 2
        },
        'other': {
            'per_section': 3,  # default estimate
            'intro': 2,
            'conclusion': 2
        }
    }

    DOCUMENT_TYPE_TEMPLATES = {
        'legal_code': {
            'structure': 'Preamble + Numbered Articles + Clauses',
            'typical_sections': 'Articles with sub-clauses',
            'example': 'Statut des Juifs (1940) - French law with 10 articles'
        },
        'treaty': {
            'structure': 'Preamble + Numbered Articles + Annexes',
            'typical_sections': 'Articles with provisions and annexes',
            'example': 'Treaty of Utrecht (1713) - 29 articles'
        },
        'book': {
            'structure': 'Chapters + Sections',
            'typical_sections': 'Chapters with subsections',
            'example': 'Brevisima relacion (1552) - 16 chapters'
        },
        'letter': {
            'structure': 'Salutation + Body Paragraphs + Closing',
            'typical_sections': 'Paragraphs or sections',
            'example': 'Diplomatic correspondence'
        },
        'decree': {
            'structure': 'Preamble + Numbered Articles/Sections',
            'typical_sections': 'Articles or sections with clauses',
            'example': 'Executive order or royal decree'
        },
        'other': {
            'structure': 'Variable structure',
            'typical_sections': 'User-defined sections',
            'example': 'General documents'
        }
    }

    def __init__(self):
        """Initialize structure assessor."""
        pass

    def assess(self, document_name: str, description: Optional[str] = None,
              document_type: Optional[str] = None, section_count: Optional[int] = None,
              section_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Assess document structure and estimate video requirements.

        Args:
            document_name: Name of document (e.g., "Statut des Juifs 1940")
            description: Optional description or location/publication info
            document_type: One of: legal_code, treaty, book, letter, decree, other
            section_count: Number of sections/articles/chapters
            section_names: Optional list of section names

        Returns:
            Dict with keys:
            - 'document_name': Document name
            - 'document_type': Classified or provided type
            - 'section_count': Number of sections
            - 'structure_template': Expected structure
            - 'outline': Markdown outline
            - 'length_estimate': Video length estimate
            - 'scope_options': Explanation of full vs excerpt options

            Or {'error': str} on failure
        """
        if not document_name or not document_name.strip():
            return {'error': 'Document name cannot be empty'}

        document_name = document_name.strip()

        # Validate document type
        if document_type:
            if document_type not in self.DOCUMENT_TYPE_TEMPLATES:
                return {
                    'error': f'Invalid document type "{document_type}". '
                            f'Must be one of: {", ".join(self.DOCUMENT_TYPE_TEMPLATES.keys())}'
                }
        else:
            document_type = 'other'

        # Validate section count
        if section_count is not None:
            if section_count < 1:
                return {'error': 'Section count must be at least 1'}
        else:
            section_count = 1  # default

        try:
            # Generate outline
            outline = self.generate_outline(
                document_name, document_type, section_count, section_names
            )

            # Estimate video length
            length_estimate_full = self.estimate_video_length(
                section_count, document_type, scope='full'
            )
            length_estimate_excerpt = self.estimate_video_length(
                section_count, document_type, scope='excerpt'
            )

            return {
                'document_name': document_name,
                'document_type': document_type,
                'section_count': section_count,
                'structure_template': self.DOCUMENT_TYPE_TEMPLATES[document_type]['structure'],
                'outline': outline,
                'length_estimate_full': length_estimate_full,
                'length_estimate_excerpt': length_estimate_excerpt,
                'scope_options': (
                    "Two approaches available:\n\n"
                    "1. FULL DOCUMENT: Cover entire document article-by-article or chapter-by-chapter\n"
                    f"   Estimated length: {length_estimate_full['estimated_minutes']} minutes\n"
                    f"   Best for: Comprehensive analysis, legal precision, complete context\n\n"
                    "2. EXCERPT: Select key sections after reading original\n"
                    f"   Estimated per-section: {length_estimate_excerpt['per_section_minutes']} minutes\n"
                    f"   Best for: Focusing on surprising/controversial clauses, targeted myth-busting\n\n"
                    "Channel philosophy: As long as needed — optimize for completeness, not brevity.\n"
                    "Choose approach after seeing document structure and identifying key sections."
                )
            }

        except Exception as e:
            return {'error': f'Structure assessment failed: {str(e)}'}

    def estimate_video_length(self, section_count: int, document_type: str,
                             scope: str = 'full') -> Dict[str, Any]:
        """
        Estimate video length based on document structure.

        Args:
            section_count: Number of sections/articles/chapters
            document_type: Document type (legal_code, treaty, book, etc.)
            scope: 'full' (entire document) or 'excerpt' (user picks sections)

        Returns:
            Dict with estimated minutes and breakdown
        """
        if document_type not in self.TIMING_ESTIMATES:
            document_type = 'other'

        timing = self.TIMING_ESTIMATES[document_type]

        if scope == 'full':
            # Full document: intro + (sections × per_section) + conclusion
            content_minutes = section_count * timing['per_section']
            total_minutes = timing['intro'] + content_minutes + timing['conclusion']

            return {
                'estimated_minutes': total_minutes,
                'breakdown': {
                    'intro': timing['intro'],
                    'content': content_minutes,
                    'conclusion': timing['conclusion']
                },
                'scope': 'full',
                'note': (
                    f"As long as needed for complete coverage. "
                    f"Channel targets completeness over brevity."
                )
            }
        else:  # excerpt
            # Excerpt: show per-section estimate (user picks sections later)
            per_section = timing['per_section']

            return {
                'per_section_minutes': per_section,
                'scope': 'excerpt',
                'note': (
                    f"Each section takes ~{per_section} min (read + translate + explain). "
                    f"Add {timing['intro']} min intro + {timing['conclusion']} min conclusion. "
                    f"Total depends on sections selected."
                )
            }

    def generate_outline(self, document_name: str, document_type: str,
                        section_count: int, section_names: Optional[List[str]] = None) -> str:
        """
        Generate markdown outline with placeholder summaries.

        Args:
            document_name: Document name
            document_type: Document type
            section_count: Number of sections
            section_names: Optional list of section names

        Returns:
            Markdown outline string
        """
        outline_parts = [f"# {document_name} — Structure Outline\n"]

        # Add document type info
        template_info = self.DOCUMENT_TYPE_TEMPLATES[document_type]
        outline_parts.append(f"**Document Type:** {document_type}")
        outline_parts.append(f"**Expected Structure:** {template_info['structure']}\n")

        # Section labels based on type
        if document_type in ['legal_code', 'treaty', 'decree']:
            section_label = "Article"
        elif document_type == 'book':
            section_label = "Chapter"
        elif document_type == 'letter':
            section_label = "Paragraph"
        else:
            section_label = "Section"

        # Generate outline
        outline_parts.append("## Outline\n")

        # Intro section
        outline_parts.append("### Introduction")
        outline_parts.append("- Context: [TBD — fill after reading original]")
        outline_parts.append("- Modern relevance: [TBD — connect to current events]\n")

        # Main sections
        for i in range(1, section_count + 1):
            if section_names and i - 1 < len(section_names):
                section_name = section_names[i - 1]
                outline_parts.append(f"### {section_label} {i}: {section_name}")
            else:
                outline_parts.append(f"### {section_label} {i}")

            outline_parts.append(f"- Summary: [TBD — fill after reading original]")
            outline_parts.append(f"- Key provisions: [TBD]")
            outline_parts.append(f"- Modern interpretation: [TBD]\n")

        # Conclusion section
        outline_parts.append("### Conclusion")
        outline_parts.append("- Why accurate history matters: [TBD]")
        outline_parts.append("- Impact on current understanding: [TBD]\n")

        return "\n".join(outline_parts)
