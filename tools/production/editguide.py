"""
Edit Guide Generation Module

Generates timing-aware edit guides from parsed scripts, integrating section durations
(at 150 WPM), B-roll markers from Phase 23, and cumulative timing sheets in the
existing EDITING-GUIDE.md format.

Purpose: Enable users to generate complete edit guides in seconds instead of hours
of manual work.

Usage:
    from tools.production import EditGuideGenerator, SectionTiming

    generator = EditGuideGenerator(project_name="14-chagos-islands-2025")
    guide = generator.generate_edit_guide(sections, shots, entities)
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import date
from .parser import Section
from .broll import Shot
from .entities import Entity


def calculate_duration_seconds(word_count: int) -> int:
    """Calculate estimated duration from word count at 150 WPM."""
    if word_count < 30:
        return 10  # Minimum 10 seconds for very short sections
    return round((word_count / 150) * 60)


def format_time(seconds: int) -> str:
    """Format seconds as MM:SS string."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


@dataclass
class SectionTiming:
    """Timing information for a script section."""
    section: Section           # Original section
    duration_seconds: int      # Estimated duration at 150 WPM
    start_time: int           # Cumulative start time in seconds
    end_time: int             # Cumulative end time in seconds
    shots: List[Shot]         # B-roll shots for this section


class EditGuideGenerator:
    """
    Generates timing-aware edit guides from parsed scripts.

    Converts sections, shots, and entities into production-ready editing guides
    matching existing EDITING-GUIDE.md format with shot-by-shot breakdown,
    timing estimates, and visual asset checklists.
    """

    def __init__(self, project_name: str = "Untitled"):
        """
        Initialize the edit guide generator.

        Args:
            project_name: Project identifier (e.g., "14-chagos-islands-2025")
        """
        self.project_name = project_name

    def calculate_timing(self, sections: List[Section], shots: List[Shot] = None) -> List[SectionTiming]:
        """
        Calculate cumulative timing for all sections.

        Args:
            sections: List of Section objects from ScriptParser
            shots: Optional list of Shot objects from BRollGenerator

        Returns:
            List of SectionTiming objects with cumulative times
        """
        if shots is None:
            shots = []

        # Map shots to sections using section_references
        section_shots_map = {section.heading: [] for section in sections}

        for shot in shots:
            # Add shot to each section it references
            if shot.section_references:
                for section_heading in shot.section_references:
                    if section_heading in section_shots_map:
                        section_shots_map[section_heading].append(shot)

        # Calculate cumulative timing
        timings = []
        cumulative_time = 0

        for section in sections:
            duration = calculate_duration_seconds(section.word_count)
            start_time = cumulative_time
            end_time = cumulative_time + duration

            timing = SectionTiming(
                section=section,
                duration_seconds=duration,
                start_time=start_time,
                end_time=end_time,
                shots=section_shots_map.get(section.heading, [])
            )

            timings.append(timing)
            cumulative_time = end_time

        return timings

    def generate_timing_sheet(self, timings: List[SectionTiming]) -> str:
        """
        Generate markdown timing sheet with section names and cumulative times.

        Args:
            timings: List of SectionTiming objects

        Returns:
            Markdown-formatted timing sheet
        """
        lines = ["## TIMING SHEET", ""]

        for i, timing in enumerate(timings, 1):
            start = format_time(timing.start_time)
            end = format_time(timing.end_time)
            lines.append(f"{i}. **{timing.section.heading}** ({start} - {end})")

        total_duration = timings[-1].end_time if timings else 0
        lines.append("")
        lines.append(f"**Total Runtime:** ~{format_time(total_duration)} (estimated at 150 WPM)")

        return '\n'.join(lines)

    def generate_edit_guide(
        self,
        sections: List[Section],
        shots: List[Shot] = None,
        entities: List[Entity] = None
    ) -> str:
        """
        Generate complete EDITING-GUIDE.md matching existing format.

        Args:
            sections: List of Section objects from ScriptParser
            shots: Optional list of Shot objects from BRollGenerator
            entities: Optional list of Entity objects from EntityExtractor

        Returns:
            Markdown-formatted edit guide
        """
        if shots is None:
            shots = []
        if entities is None:
            entities = []

        # Calculate timing
        timings = self.calculate_timing(sections, shots)
        total_duration = timings[-1].end_time if timings else 0

        # Start building the guide
        today = date.today().strftime('%Y-%m-%d')
        md = [
            f"# {self.project_name} - EDITING GUIDE",
            "",
            f"**Project:** {self.project_name}",
            f"**Video Length:** ~{format_time(total_duration)} (estimated at 150 WPM)",
            f"**Format:** Hybrid talking head + B-roll evidence",
            f"**Target Ratio:** 65% talking head, 35% B-roll",
            f"**Date Created:** {today}",
            "",
            "---",
            ""
        ]

        # Editing philosophy
        md.extend(self._generate_editing_philosophy())

        # Shot-by-shot breakdown
        md.extend(self._generate_shot_breakdown(timings, shots))

        # Visual assets checklist
        md.extend(self._generate_visual_assets_checklist(shots))

        # Retention optimization
        md.extend(self._generate_retention_optimization(timings))

        # Quality checklist
        md.extend(self._generate_quality_checklist())

        # Change log
        md.extend(self._generate_change_log(today))

        return '\n'.join(md)

    def _generate_editing_philosophy(self) -> List[str]:
        """Generate the editing philosophy section."""
        return [
            "## EDITING PHILOSOPHY",
            "",
            "**The Golden Rule:** If the B-roll doesn't make your argument stronger, stay on camera.",
            "",
            "**B-roll is EVIDENCE, not decoration.**",
            "",
            "Use B-roll when:",
            "- Showing PRIMARY SOURCE DOCUMENTS (treaties, memos, rulings)",
            "- Displaying geographic locations (maps, strategic positions)",
            "- Providing visual proof (testimony quotes, eyewitness accounts)",
            "- Showing historical photos (key figures, events)",
            "- Displaying institutional evidence (court buildings, official documents)",
            "",
            "Stay on camera when:",
            "- Making arguments and interpretations",
            "- Explaining causation and connecting events",
            "- Presenting steelman arguments",
            "- Building emotional weight",
            "- Delivering rhetorical questions and pivots",
            "",
            "---",
            ""
        ]

    def _generate_shot_breakdown(self, timings: List[SectionTiming], all_shots: List[Shot]) -> List[str]:
        """Generate shot-by-shot breakdown grouped by section."""
        md = ["## SHOT-BY-SHOT BREAKDOWN", ""]

        shot_counter = 1

        for section_num, timing in enumerate(timings, 1):
            # Section header
            section_start = format_time(timing.start_time)
            section_end = format_time(timing.end_time)

            md.append(f"### [SECTION {section_num}: {timing.section.heading.upper()}] ({section_start} - {section_end})")
            md.append("")

            # Section purpose
            purpose = self._get_section_purpose(timing.section.section_type)
            md.append(f"**Purpose:** {purpose}")
            md.append("")
            md.append("---")
            md.append("")

            # Get shots for this section
            section_shots = timing.shots

            # If no shots, create talking head entries
            if not section_shots:
                # Split section content into smaller talking head shots
                shot_md = self._generate_talking_head_shot(
                    shot_counter,
                    timing.section.content[:200] + "..." if len(timing.section.content) > 200 else timing.section.content,
                    timing.section.word_count,
                    section_start,
                    section_end
                )
                md.extend(shot_md)
                md.append("")
                shot_counter += 1
            else:
                # Interleave talking head and B-roll shots
                # For now, create shots for each B-roll item
                for shot in section_shots:
                    shot_md = self._generate_broll_shot(
                        shot_counter,
                        shot,
                        section_start,
                        section_end
                    )
                    md.extend(shot_md)
                    md.append("")
                    shot_counter += 1

        return md

    def _get_section_purpose(self, section_type: str) -> str:
        """Get purpose description based on section type."""
        purposes = {
            'intro': 'Hook viewer and establish topic',
            'body': 'Develop argument with evidence',
            'conclusion': 'Synthesize and call to action'
        }
        return purposes.get(section_type, 'Develop narrative')

    def _generate_talking_head_shot(
        self,
        shot_num: int,
        content_excerpt: str,
        word_count: int,
        start_time: str,
        end_time: str
    ) -> List[str]:
        """Generate talking head shot entry."""
        duration = calculate_duration_seconds(word_count)

        # Clean excerpt for display
        excerpt = content_excerpt.replace('\n', ' ').strip()
        if len(excerpt) > 150:
            excerpt = excerpt[:150] + "..."

        return [
            f"#### SHOT {shot_num}: TALKING HEAD - Narrative delivery ({start_time} - {end_time})",
            f"**Duration: {duration} sec** | **Est. Words: {word_count}**",
            "",
            f'> "{excerpt}"',
            "",
            "**VISUAL:** Direct to camera",
            "",
            "**WHY TALKING HEAD:** Narrative delivery. Your face sells the importance.",
            "",
            "**CAMERA NOTES:** [To be added after recording]",
            "",
            "---"
        ]

    def _generate_broll_shot(
        self,
        shot_num: int,
        shot: Shot,
        start_time: str,
        end_time: str
    ) -> List[str]:
        """Generate B-roll shot entry."""
        # Estimate duration (placeholder - would need content to calculate)
        duration = 15  # Default B-roll duration

        lines = [
            f"#### SHOT {shot_num}: B-ROLL - {shot.entity} ({start_time} - {end_time})",
            f"**Duration: ~{duration} sec**",
            "",
            f'> "{shot.entity}"',
            "",
            f"**VISUAL:** {shot.entity}",
            "",
            f"**WHY B-ROLL:** PRIMARY SOURCE/EVIDENCE. {shot.entity} supports the argument.",
            "",
            "**CAMERA NOTES:** N/A (B-roll)",
            ""
        ]

        # Add sources if available
        if shot.source_urls:
            lines.append("**SOURCES:**")
            for url in shot.source_urls:
                lines.append(f"- {url}")
            lines.append("")

        # Add DIY instructions if available
        if shot.diy_instructions:
            first_instruction = shot.diy_instructions.split('\n')[0]
            lines.append(f"**CREATE IN:** {first_instruction}")
        else:
            lines.append("**CREATE IN:** N/A")

        lines.append("")
        lines.append("---")

        return lines

    def _generate_visual_assets_checklist(self, shots: List[Shot]) -> List[str]:
        """Generate visual assets checklist from shots."""
        md = [
            "## VISUAL ASSETS CHECKLIST",
            ""
        ]

        # Group by priority
        priority_shots = {1: [], 2: [], 3: []}
        for shot in shots:
            priority_shots[shot.priority].append(shot)

        # Priority 1
        if priority_shots[1]:
            md.append("### Priority 1: CRITICAL (Must have)")
            md.append("")
            for shot in priority_shots[1]:
                md.append(f"- [ ] {shot.entity} ({shot.visual_type})")
            md.append("")

        # Priority 2
        if priority_shots[2]:
            md.append("### Priority 2: Important")
            md.append("")
            for shot in priority_shots[2]:
                md.append(f"- [ ] {shot.entity} ({shot.visual_type})")
            md.append("")

        # Priority 3
        if priority_shots[3]:
            md.append("### Priority 3: Nice to have")
            md.append("")
            for shot in priority_shots[3]:
                md.append(f"- [ ] {shot.entity} ({shot.visual_type})")
            md.append("")

        md.append("---")
        md.append("")

        return md

    def _generate_retention_optimization(self, timings: List[SectionTiming]) -> List[str]:
        """Generate retention optimization section with pattern interrupts."""
        md = [
            "## RETENTION OPTIMIZATION",
            "",
            "### Pattern Interrupts (Target: every 60-90 seconds)",
            "",
            "| Timestamp | Type | Description |",
            "|-----------|------|-------------|"
        ]

        # Generate interrupt markers for each section transition
        for i, timing in enumerate(timings):
            timestamp = format_time(timing.start_time)
            interrupt_type = "TALKING HEAD" if not timing.shots else "B-ROLL"
            description = timing.section.heading
            md.append(f"| {timestamp} | {interrupt_type} | {description} |")

        md.append("")

        # Calculate total runtime and ratio
        total_seconds = timings[-1].end_time if timings else 0
        total_runtime = format_time(total_seconds)

        md.append("### Talking Head vs. B-roll Ratio")
        md.append("")
        md.append(f"**Total runtime:** ~{total_runtime}")
        md.append("**Estimated talking head:** TBD (based on actual filming)")
        md.append("**Estimated B-roll:** TBD (based on actual filming)")
        md.append("")
        md.append("**Target (65/35):** Measure after editing")
        md.append("")
        md.append("---")
        md.append("")

        return md

    def _generate_quality_checklist(self) -> List[str]:
        """Generate quality checklist template."""
        return [
            "## QUALITY CHECKLIST (Before Export)",
            "",
            "### Visual Consistency",
            "- [ ] All document graphics use consistent styling",
            "- [ ] All quotes attributed with source",
            "- [ ] Map styling consistent throughout",
            "- [ ] Text overlays readable at YouTube resolution",
            "",
            "### Pacing",
            "- [ ] Emotional sections have appropriate slower pacing",
            "- [ ] B-roll transitions smooth",
            "- [ ] Final question has pause before delivery",
            "",
            "### Audio",
            "- [ ] All pronunciations verified",
            "- [ ] No audio errors requiring re-recording",
            "",
            "---",
            ""
        ]

    def _generate_change_log(self, today: str) -> List[str]:
        """Generate change log section."""
        return [
            "## CHANGE LOG",
            "",
            "| Date | Changes |",
            "|------|---------|",
            f"| {today} | Initial guide created from script parser |",
            "",
            "---",
            "",
            "**Guide Status:** ✅ GENERATED - Review and refine as needed",
            "",
            "**Next Steps:**",
            "1. Review shot breakdown for accuracy",
            "2. Adjust timing estimates based on actual delivery pace",
            "3. Add specific camera notes during filming",
            "4. Update visual assets checklist with download links"
        ]


if __name__ == "__main__":
    # Simple test
    print("EditGuideGenerator module loaded successfully")
    print(f"150 words = {calculate_duration_seconds(150)} seconds ({format_time(calculate_duration_seconds(150))})")
    print(f"300 words = {calculate_duration_seconds(300)} seconds ({format_time(calculate_duration_seconds(300))})")
    print(f"25 words = {calculate_duration_seconds(25)} seconds ({format_time(calculate_duration_seconds(25))})")
