"""
Video clip exporter.
Combines video processing, cropping, and caption rendering.
"""

import json
from pathlib import Path
from typing import Dict
import ffmpeg

from core.video_processor import VideoProcessor
from core.caption_renderer import CaptionRenderer
from utils.logger import logger
from utils.config import DATA_DIR


class ClipExporter:
    """
    Exports final video clips with captions burned in.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = DATA_DIR / "projects" / project_id
        self.export_dir = self.project_dir / "exports"
        self.export_dir.mkdir(exist_ok=True)

        self.video_processor = VideoProcessor(project_id)

    def export_clip(
        self,
        clip_data: Dict,
        clip_number: int,
        caption_preset: str = "academic",
        crop_mode: str = "center"
    ) -> Path:
        """
        Export a single clip with captions.

        Args:
            clip_data: Clip dictionary with start_time, end_time, text
            clip_number: Clip number for filename
            caption_preset: Caption style preset
            crop_mode: "center" or "face" (face not implemented yet)

        Returns:
            Path to exported video file
        """
        start_time = clip_data['start_time']
        end_time = clip_data['end_time']
        text = clip_data['text']

        logger.info(f"Exporting clip #{clip_number}: {start_time:.1f}s - {end_time:.1f}s")

        # Find source video
        source_video = self._find_source_video()

        # Step 1: Create temporary clip without captions
        temp_clip = self.export_dir / f"clip_{clip_number:03d}_temp.mp4"
        self.video_processor.extract_clip(
            source_video=str(source_video),
            start_time=start_time,
            end_time=end_time,
            output_path=temp_clip,
            crop_to_vertical=True,
            crop_mode=crop_mode
        )

        # Step 2: Create SRT subtitle file
        caption_renderer = CaptionRenderer(preset=caption_preset)
        srt_path = self.export_dir / f"clip_{clip_number:03d}.srt"
        caption_renderer.create_srt_file(
            text=text,
            duration=end_time - start_time,
            output_path=srt_path
        )

        # Step 3: Burn subtitles into video
        final_clip = self.export_dir / f"clip_{clip_number:03d}.mp4"
        self._burn_subtitles(temp_clip, srt_path, final_clip, caption_renderer)

        # Step 4: Clean up temp file
        temp_clip.unlink()

        # Step 5: Save export metadata
        self._save_export_metadata(clip_data, clip_number, final_clip, caption_preset)

        logger.info(f"✓ Clip exported successfully: {final_clip}")
        return final_clip

    def _find_source_video(self) -> Path:
        """Find the source video file in project directory."""
        # Look for source.* files
        candidates = list(self.project_dir.glob("source.*"))

        if not candidates:
            raise FileNotFoundError(f"Source video not found in {self.project_dir}")

        return candidates[0]

    def _burn_subtitles(
        self,
        video_path: Path,
        srt_path: Path,
        output_path: Path,
        caption_renderer: CaptionRenderer
    ) -> None:
        """
        Burn subtitles into video using FFmpeg.

        Args:
            video_path: Input video
            srt_path: Subtitle file
            output_path: Output video with burned subtitles
            caption_renderer: Caption renderer for styling
        """
        logger.info("Burning subtitles into video")

        try:
            # Build subtitle filter
            subtitle_filter = caption_renderer.get_ffmpeg_subtitle_filter(srt_path)

            # Apply subtitle filter
            input_stream = ffmpeg.input(str(video_path))
            video = input_stream.video.filter('subtitles', str(srt_path).replace('\\', '/').replace(':', '\\:'))
            audio = input_stream.audio

            output = ffmpeg.output(
                video,
                audio,
                str(output_path),
                vcodec='libx264',
                acodec='aac',
                preset='medium',
                crf=23
            )

            output.overwrite_output().run(capture_stdout=True, capture_stderr=True)

            logger.info("Subtitles burned successfully")

        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error burning subtitles: {e.stderr.decode()}")
            raise

    def _save_export_metadata(
        self,
        clip_data: Dict,
        clip_number: int,
        output_path: Path,
        caption_preset: str
    ) -> None:
        """
        Save export metadata for reference.

        Args:
            clip_data: Original clip data
            clip_number: Clip number
            output_path: Path to exported video
            caption_preset: Caption preset used
        """
        metadata = {
            "clip_number": clip_number,
            "output_path": str(output_path),
            "start_time": clip_data['start_time'],
            "end_time": clip_data['end_time'],
            "duration": clip_data['duration'],
            "text": clip_data['text'],
            "score": clip_data['score'],
            "score_reasons": clip_data['reasons'],
            "caption_preset": caption_preset
        }

        metadata_path = self.export_dir / f"clip_{clip_number:03d}_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"Export metadata saved: {metadata_path}")
