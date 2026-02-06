"""
Enhanced caption rendering with word-by-word timing support.
Creates professional-looking captions similar to YouTube Shorts/TikTok.
"""

from pathlib import Path
from typing import Dict, List
import textwrap
import re

from utils.config import config
from utils.logger import logger


class EnhancedCaptionRenderer:
    """
    Advanced caption renderer with word-level timing support.
    Supports multiple caption styles optimized for short-form vertical video.
    """

    def __init__(self, preset: str = "academic"):
        """
        Initialize caption renderer with style preset.

        Args:
            preset: Caption style preset name
        """
        self.preset = config.get_caption_preset(preset)
        self.preset_name = preset

    def create_word_by_word_srt(
        self,
        text: str,
        duration: float,
        output_path: Path,
        words_per_caption: int = 3
    ) -> Path:
        """
        Create SRT file with word-by-word timing (viral short-form style).

        Args:
            text: Caption text
            duration: Video duration in seconds
            output_path: Where to save SRT file
            words_per_caption: Number of words to display at once (1-5)

        Returns:
            Path to created SRT file
        """
        # Split into words (preserving punctuation)
        words = self._split_into_words(text)

        if not words:
            logger.warning("No words found in text, creating single caption")
            return self._create_single_caption_srt(text, duration, output_path)

        # Calculate timing for each word group
        num_groups = len(words) // words_per_caption + (1 if len(words) % words_per_caption else 0)
        time_per_group = duration / num_groups if num_groups > 0 else duration

        # Build SRT content
        srt_content = []
        group_num = 0

        for i in range(0, len(words), words_per_caption):
            word_group = words[i:i + words_per_caption]
            caption_text = ' '.join(word_group)

            # Apply transformations
            if self.preset['all_caps']:
                caption_text = caption_text.upper()

            start_time = group_num * time_per_group
            end_time = (group_num + 1) * time_per_group

            # SRT format
            start_srt = self._seconds_to_srt_time(start_time)
            end_srt = self._seconds_to_srt_time(end_time)

            srt_content.append(f"{group_num + 1}\n")
            srt_content.append(f"{start_srt} --> {end_srt}\n")
            srt_content.append(f"{caption_text}\n")
            srt_content.append("\n")

            group_num += 1

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(srt_content)

        logger.info(f"Created word-by-word SRT with {group_num} captions: {output_path}")
        return output_path

    def create_sentence_srt(
        self,
        text: str,
        duration: float,
        output_path: Path
    ) -> Path:
        """
        Create SRT file with sentence-level timing (documentary style).

        Args:
            text: Caption text
            duration: Video duration in seconds
            output_path: Where to save SRT file

        Returns:
            Path to created SRT file
        """
        # Split into sentences
        sentences = self._split_into_sentences(text)

        if not sentences:
            return self._create_single_caption_srt(text, duration, output_path)

        # Calculate timing for each sentence
        num_sentences = len(sentences)
        time_per_sentence = duration / num_sentences if num_sentences > 0 else duration

        # Build SRT content
        srt_content = []
        for i, sentence in enumerate(sentences):
            # Apply transformations
            if self.preset['all_caps']:
                sentence = sentence.upper()

            # Wrap long sentences
            max_chars = self.preset['max_chars_per_line']
            wrapped_lines = textwrap.wrap(sentence, width=max_chars)
            caption_text = '\n'.join(wrapped_lines)

            start_time = i * time_per_sentence
            end_time = (i + 1) * time_per_sentence

            # SRT format
            start_srt = self._seconds_to_srt_time(start_time)
            end_srt = self._seconds_to_srt_time(end_time)

            srt_content.append(f"{i + 1}\n")
            srt_content.append(f"{start_srt} --> {end_srt}\n")
            srt_content.append(f"{caption_text}\n")
            srt_content.append("\n")

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(srt_content)

        logger.info(f"Created sentence-based SRT with {num_sentences} captions: {output_path}")
        return output_path

    def create_karaoke_ass(
        self,
        text: str,
        duration: float,
        output_path: Path
    ) -> Path:
        """
        Create ASS subtitle file with karaoke-style word highlighting.

        This creates professional word-by-word highlighting effect where
        each word changes color as it's spoken.

        Args:
            text: Caption text
            duration: Video duration in seconds
            output_path: Where to save ASS file

        Returns:
            Path to created ASS file
        """
        words = self._split_into_words(text)

        if not words:
            logger.warning("No words found, creating simple ASS file")
            return self._create_simple_ass(text, duration, output_path)

        # Calculate timing per word
        time_per_word = duration / len(words) if words else duration

        # Build ASS content
        ass_header = self._create_ass_header()

        # Build dialogue lines with karaoke effects
        ass_dialogues = []
        current_time = 0

        for word in words:
            start_time = current_time
            end_time = current_time + time_per_word

            # ASS timing format: 0:00:00.00
            start_ass = self._seconds_to_ass_time(start_time)
            end_ass = self._seconds_to_ass_time(end_time)

            # Karaoke effect: word gradually highlights
            # {\\k<duration>} makes word highlight for that duration (in centiseconds)
            duration_cs = int(time_per_word * 100)

            dialogue = f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{{\\k{duration_cs}}}{word} "
            ass_dialogues.append(dialogue)

            current_time = end_time

        ass_content = ass_header + '\n'.join(ass_dialogues)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)

        logger.info(f"Created karaoke ASS file with {len(words)} words: {output_path}")
        return output_path

    def _create_single_caption_srt(self, text: str, duration: float, output_path: Path) -> Path:
        """Fallback: create single caption spanning entire duration."""
        if self.preset['all_caps']:
            text = text.upper()

        wrapped_lines = textwrap.wrap(text, width=self.preset['max_chars_per_line'])
        caption_text = '\n'.join(wrapped_lines)

        start_srt = self._seconds_to_srt_time(0)
        end_srt = self._seconds_to_srt_time(duration)

        srt_content = f"1\n{start_srt} --> {end_srt}\n{caption_text}\n\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_content)

        return output_path

    def _create_simple_ass(self, text: str, duration: float, output_path: Path) -> Path:
        """Fallback: create simple ASS file without karaoke."""
        ass_header = self._create_ass_header()

        start_ass = self._seconds_to_ass_time(0)
        end_ass = self._seconds_to_ass_time(duration)

        dialogue = f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{text}"

        ass_content = ass_header + dialogue

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)

        return output_path

    def _create_ass_header(self) -> str:
        """Create ASS file header with styling."""
        font = self.preset['font']
        font_size = self.preset['font_size']
        font_color = self._color_to_ass_hex(self.preset['font_color'])
        bg_color = self._color_to_ass_hex(self.preset.get('background_color', 'black'))

        # ASS alignment: 1-3 = bottom, 4-6 = middle, 7-9 = top
        # Within each row: 1/4/7 = left, 2/5/8 = center, 3/6/9 = right
        position = self.preset['position']
        alignment_map = {
            'top': 8,      # Top center
            'center': 5,   # Middle center
            'bottom': 2    # Bottom center
        }
        alignment = alignment_map.get(position, 2)

        margin_v = self.preset['margin']

        header = f"""[Script Info]
Title: Enhanced Captions
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{font_size},&H{font_color},&H{font_color},&H00000000,&H{bg_color},-1,0,0,0,100,100,0,0,1,2,0,{alignment},10,10,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        return header

    @staticmethod
    def _split_into_words(text: str) -> List[str]:
        """Split text into words, preserving punctuation with words."""
        # Split on whitespace but keep punctuation with words
        words = text.split()
        return words

    @staticmethod
    def _split_into_sentences(text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def _seconds_to_srt_time(seconds: float) -> str:
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    @staticmethod
    def _seconds_to_ass_time(seconds: float) -> str:
        """Convert seconds to ASS timestamp format (H:MM:SS.cc)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centisecs = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{centisecs:02d}"

    @staticmethod
    def _color_to_ass_hex(color: str) -> str:
        """
        Convert color name to ASS hex format (AABBGGRR).

        Args:
            color: Color name (white, black, yellow, etc.)

        Returns:
            Hex color code in ASS format (with alpha)
        """
        color_map = {
            'white': '00FFFFFF',
            'black': '00000000',
            'yellow': '0000FFFF',  # ASS uses AABBGGRR
            'red': '000000FF',
            'blue': '00FF0000',
            'green': '0000FF00',
        }
        return color_map.get(color.lower(), '00FFFFFF')

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
            'top': 8,
            'center': 5,
            'bottom': 2
        }
        alignment = position_map.get(self.preset['position'], 2)

        # Margin from edge
        margin_v = self.preset['margin']

        # Build filter
        filter_str = f"subtitles='{srt_path_str}':force_style='FontName={font},FontSize={font_size},PrimaryColour=&H{self._color_to_srt_hex(font_color)},Alignment={alignment},MarginV={margin_v},Bold=-1,Outline=2'"

        return filter_str

    @staticmethod
    def _color_to_srt_hex(color: str) -> str:
        """Convert color name to SRT/ASS hex format (BGR order)."""
        color_map = {
            'white': 'FFFFFF',
            'black': '000000',
            'yellow': '00FFFF',  # BGR
            'red': '0000FF',
            'blue': 'FF0000',
            'green': '00FF00',
        }
        return color_map.get(color.lower(), 'FFFFFF')
