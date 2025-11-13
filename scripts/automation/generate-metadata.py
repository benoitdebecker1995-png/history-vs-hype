#!/usr/bin/env python3
"""
Video Metadata Generator for History vs Hype
Generates YouTube metadata from markdown script files

Usage:
    python generate-metadata.py path/to/script.md

Output:
    - Video duration estimate
    - YouTube title
    - Description with sources
    - Tags
    - Timestamps
"""

import sys
import re
from pathlib import Path
from datetime import timedelta


class MetadataGenerator:
    def __init__(self, script_path):
        self.script_path = Path(script_path)
        self.script_content = self.script_path.read_text(encoding='utf-8')
        self.words_per_minute = 105  # Conservative estimate

    def count_words(self):
        """Count total words in script (excluding markdown formatting)"""
        # Remove markdown headers, links, and formatting
        clean_text = re.sub(r'#+ .*\n', '', self.script_content)
        clean_text = re.sub(r'\[.*?\]\(.*?\)', '', clean_text)
        clean_text = re.sub(r'[*_`]', '', clean_text)
        clean_text = re.sub(r'\[.*?\]', '', clean_text)

        # Count words
        words = clean_text.split()
        return len(words)

    def estimate_duration(self):
        """Calculate estimated video duration"""
        word_count = self.count_words()
        minutes = word_count / self.words_per_minute
        seconds = int((minutes % 1) * 60)
        minutes = int(minutes)

        return minutes, seconds, word_count

    def extract_title(self):
        """Extract or generate title from script"""
        # Look for title in first header
        match = re.search(r'^# (.+)$', self.script_content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Use filename as fallback
        return self.script_path.stem.replace('_', ' ').replace('-', ' ').title()

    def extract_sources(self):
        """Extract source citations from script"""
        sources = []

        # Pattern 1: [Source text](URL)
        markdown_links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', self.script_content)
        for text, url in markdown_links:
            sources.append(f"{text}: {url}")

        # Pattern 2: Look for "Sources:" section
        sources_section = re.search(r'##\s+Sources?:?\s*\n(.*?)(?=\n##|\Z)',
                                   self.script_content, re.DOTALL | re.IGNORECASE)
        if sources_section:
            source_lines = sources_section.group(1).strip().split('\n')
            for line in source_lines:
                line = line.strip('- ').strip()
                if line and line not in sources:
                    sources.append(line)

        return sources

    def generate_timestamps(self):
        """Generate timestamp estimates from section headers"""
        headers = re.findall(r'^##\s+(.+)$', self.script_content, re.MULTILINE)

        if not headers:
            return []

        # Estimate time per section based on total duration
        minutes, seconds, _ = self.estimate_duration()
        total_seconds = minutes * 60 + seconds

        timestamps = [(0, "Introduction")]

        if len(headers) > 1:
            seconds_per_section = total_seconds / len(headers)

            for i, header in enumerate(headers[1:], 1):
                time_seconds = int(i * seconds_per_section)
                timestamp = str(timedelta(seconds=time_seconds))[2:]  # Remove leading "0:"
                if timestamp.startswith('0'):
                    timestamp = timestamp[1:]  # Remove leading 0 from minutes
                timestamps.append((time_seconds, header))

        return timestamps

    def generate_description(self, title):
        """Generate YouTube description"""
        description = []

        # Add title/hook
        description.append(title)
        description.append("")

        # Add timestamps
        timestamps = self.generate_timestamps()
        if timestamps:
            description.append("⏱️ TIMESTAMPS:")
            for seconds, label in timestamps:
                mins = seconds // 60
                secs = seconds % 60
                description.append(f"{mins}:{secs:02d} - {label}")
            description.append("")

        # Add sources
        sources = self.extract_sources()
        if sources:
            description.append("📚 SOURCES:")
            for source in sources:
                description.append(f"• {source}")
            description.append("")

        # Add channel boilerplate
        description.append("🎯 ABOUT HISTORY VS HYPE:")
        description.append("Evidence-based analysis of historical myths affecting modern geopolitics.")
        description.append("Primary sources. Academic research. No oversimplification.")
        description.append("")
        description.append("#history #geopolitics #factcheck")

        return '\n'.join(description)

    def suggest_tags(self, title):
        """Generate SEO tags"""
        tags = [
            "history",
            "geopolitics",
            "fact check",
            "historical myths",
            "primary sources",
            "educational",
            "documentary"
        ]

        # Extract key terms from title
        title_words = re.findall(r'\w+', title.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'are', 'was', 'were'}

        for word in title_words:
            if len(word) > 4 and word not in stop_words and word not in tags:
                tags.append(word)

        return tags

    def generate_metadata(self):
        """Generate complete metadata package"""
        minutes, seconds, word_count = self.estimate_duration()
        title = self.extract_title()
        description = self.generate_description(title)
        tags = self.suggest_tags(title)
        timestamps = self.generate_timestamps()

        return {
            'title': title,
            'duration_estimate': f"{minutes}:{seconds:02d}",
            'word_count': word_count,
            'description': description,
            'tags': tags,
            'timestamps': timestamps,
            'sources': self.extract_sources()
        }

    def print_metadata(self):
        """Print formatted metadata output"""
        metadata = self.generate_metadata()

        print("=" * 60)
        print("VIDEO METADATA GENERATOR - History vs Hype")
        print("=" * 60)
        print()

        print(f"📄 SCRIPT: {self.script_path.name}")
        print(f"📊 WORD COUNT: {metadata['word_count']} words")
        print(f"⏱️  ESTIMATED DURATION: {metadata['duration_estimate']}")
        print()

        print("📺 SUGGESTED TITLE:")
        print(f"   {metadata['title']}")
        print()

        print("📝 DESCRIPTION (copy to YouTube):")
        print("-" * 60)
        print(metadata['description'])
        print("-" * 60)
        print()

        print("🏷️  TAGS (copy to YouTube):")
        print(f"   {', '.join(metadata['tags'])}")
        print()

        if metadata['timestamps']:
            print("⏱️  TIMESTAMPS (for description):")
            for seconds, label in metadata['timestamps']:
                mins = seconds // 60
                secs = seconds % 60
                print(f"   {mins}:{secs:02d} - {label}")
            print()

        if metadata['sources']:
            print(f"📚 SOURCES FOUND: {len(metadata['sources'])}")
            for i, source in enumerate(metadata['sources'][:5], 1):
                print(f"   {i}. {source[:70]}...")
            if len(metadata['sources']) > 5:
                print(f"   ... and {len(metadata['sources']) - 5} more")
            print()

        print("=" * 60)
        print("✅ Metadata generated successfully!")
        print("=" * 60)


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate-metadata.py path/to/script.md")
        sys.exit(1)

    script_path = sys.argv[1]

    if not Path(script_path).exists():
        print(f"Error: File not found: {script_path}")
        sys.exit(1)

    generator = MetadataGenerator(script_path)
    generator.print_metadata()


if __name__ == '__main__':
    main()
