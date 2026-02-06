"""
Caption/subtitle rendering for video clips.
Burns captions directly into video using FFmpeg.
"""

from pathlib import Path
from typing import Dict, List
import textwrap

from utils.config import config
from utils.logger import logger


class CaptionRenderer:
    """
    Renders captions for video clips using configured presets.
    Generates SRT subtitle files and FFmpeg burn-in commands.
    """

    def __init__(self, preset: str = "academic"):
        """
        Initialize caption renderer with style preset.

        Args:
            preset: Caption style preset name (academic, minimal, shorts_friendly, documentary)
        """
        self.preset = config.get_caption_preset(preset)
        self.preset_name = preset

    def create_srt_file(
        self,
        text: str,
        duration: float,
        output_path: Path
    ) -> Path:
        """
        Create SRT subtitle file from text.

        Args:
            text: Caption text
            duration: Video duration in seconds
            output_path: Where to save SRT file

        Returns:
            Path to created SRT file
        """
        # Wrap text to max chars per line
        max_chars = self.preset['max_chars_per_line']
        wrapped_lines = textwrap.wrap(text, width=max_chars)

        # Apply transformations
        if self.preset['all_caps']:
            wrapped_lines = [line.upper() for line in wrapped_lines]

        # Calculate timing for each line
        # Simple approach: divide duration equally among lines
        num_lines = len(wrapped_lines)
        time_per_line = duration / num_lines if num_lines > 0 else duration

        # Build SRT content
        srt_content = []
        for i, line in enumerate(wrapped_lines):
            start_time = i * time_per_line
            end_time = (i + 1) * time_per_line

            # SRT format: HH:MM:SS,mmm
            start_srt = self._seconds_to_srt_time(start_time)
            end_srt = self._seconds_to_srt_time(end_time)

            srt_content.append(f"{i + 1}\n")
            srt_content.append(f"{start_srt} --> {end_srt}\n")
            srt_content.append(f"{line}\n")
            srt_content.append("\n")

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(srt_content)

        logger.info(f"Created SRT file with {num_lines} caption lines: {output_path}")
        return output_path

    def get_ffmpeg_subtitle_filter(self, srt_path: Path) -> str:
        """
        Generate FFmpeg subtitle filter string for burning captions.

        Args:
            srt_path: Path to SRT subtitle file

        Returns:
            FFmpeg filter string
        """
        # Convert Windows path to Unix-style for FFmpeg
        srt_path_str = str(srt_path).replace('\\', '/').replace(':', '\\:')

        # Build subtitle filter with styling
        font = self.preset['font'].replace(' ', '\\ ')
        font_size = self.preset['font_size']
        font_color = self.preset['font_color']

        # Position mapping
        position_map = {
            'top': 2,
            'center': 5,
            'bottom': 2  # Bottom with margin
        }
        alignment = position_map.get(self.preset['position'], 2)

        # Margin from edge
        margin_v = self.preset['margin']

        # Build filter
        # Note: subtitles filter doesn't support background easily
        # For background, we'd need to use drawtext or ass format
        # For MVP, using simple subtitles filter
        filter_str = f"subtitles='{srt_path_str}':force_style='FontName={font},FontSize={font_size},PrimaryColour=&H{self._color_to_hex(font_color)},Alignment={alignment},MarginV={margin_v}'"

        return filter_str

    @staticmethod
    def _seconds_to_srt_time(seconds: float) -> str:
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def _color_to_hex(color: str) -> str:
        """
        Convert color name to ASS hex format (BGR order).

        Args:
            color: Color name (white, black, yellow, etc.)

        Returns:
            Hex color code in ASS format
        """
        color_map = {
            'white': 'FFFFFF',
            'black': '000000',
            'yellow': '00FFFF',  # BGR: yellow is 00FFFF
            'red': '0000FF',
            'blue': 'FF0000',
        }
        return color_map.get(color.lower(), 'FFFFFF')
