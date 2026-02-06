"""
Video processing using FFmpeg.
Handles video ingestion, audio extraction, and metadata extraction.
"""

import ffmpeg
import json
import os
from pathlib import Path
from typing import Dict, Tuple

from utils.logger import logger
from utils.config import DATA_DIR

# Configure portable ffmpeg if available
_PORTABLE_FFMPEG_CONFIG = Path(__file__).parent.parent.parent / "config" / "ffmpeg_path.txt"
if _PORTABLE_FFMPEG_CONFIG.exists():
    with open(_PORTABLE_FFMPEG_CONFIG, 'r') as f:
        ffmpeg_path = f.read().strip()
        if Path(ffmpeg_path).exists():
            os.environ['PATH'] = f"{ffmpeg_path}{os.pathsep}{os.environ['PATH']}"
            logger.info(f"Using portable ffmpeg from: {ffmpeg_path}")


class VideoProcessor:
    """FFmpeg wrapper for video operations."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = DATA_DIR / "projects" / project_id
        self.project_dir.mkdir(parents=True, exist_ok=True)

    def get_video_metadata(self, video_path: str) -> Dict:
        """
        Extract video metadata using FFprobe.

        Args:
            video_path: Path to video file

        Returns:
            Dictionary with duration, fps, resolution
        """
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next(
                (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                None
            )

            if not video_stream:
                raise ValueError("No video stream found in file")

            duration = float(probe['format']['duration'])
            # Safely parse frame rate (e.g., "30/1" -> 30.0)
            fps_str = video_stream['r_frame_rate']
            if '/' in fps_str:
                num, den = fps_str.split('/')
                fps = float(num) / float(den)
            else:
                fps = float(fps_str)
            width = int(video_stream['width'])
            height = int(video_stream['height'])

            metadata = {
                'duration': duration,
                'fps': fps,
                'resolution': f"{width}x{height}",
                'width': width,
                'height': height
            }

            logger.info(f"Video metadata extracted: {metadata}")
            return metadata

        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error extracting metadata: {e.stderr.decode()}")
            raise

    def extract_audio(self, video_path: str) -> Path:
        """
        Extract audio track from video to WAV format.

        Args:
            video_path: Path to source video

        Returns:
            Path to extracted audio file
        """
        audio_path = self.project_dir / "audio.wav"

        try:
            logger.info(f"Extracting audio from {video_path} to {audio_path}")

            # Extract audio as 16kHz mono WAV (optimal for Whisper)
            ffmpeg.input(video_path).output(
                str(audio_path),
                acodec='pcm_s16le',  # 16-bit PCM
                ac=1,  # Mono
                ar='16000'  # 16kHz sample rate
            ).overwrite_output().run(capture_stdout=True, capture_stderr=True)

            logger.info(f"Audio extracted successfully: {audio_path}")
            return audio_path

        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error extracting audio: {e.stderr.decode()}")
            raise

    def copy_source_video(self, source_path: str) -> Path:
        """
        Copy source video to project directory.

        Args:
            source_path: Original video file path

        Returns:
            Path to copied video in project directory
        """
        source = Path(source_path)
        destination = self.project_dir / f"source{source.suffix}"

        logger.info(f"Copying video from {source_path} to {destination}")

        # For now, just copy. In production, could use symlink or reference
        import shutil
        shutil.copy2(source, destination)

        return destination

    def extract_clip(
        self,
        source_video: str,
        start_time: float,
        end_time: float,
        output_path: Path,
        crop_to_vertical: bool = True,
        crop_mode: str = "center"
    ) -> Path:
        """
        Extract a video segment and optionally crop to 9:16 vertical.

        Args:
            source_video: Path to source video
            start_time: Start timestamp in seconds
            end_time: End timestamp in seconds
            output_path: Where to save the clip
            crop_to_vertical: Whether to crop to 9:16 aspect ratio
            crop_mode: "center" for center crop, "face" for face tracking (TODO)

        Returns:
            Path to exported clip
        """
        try:
            logger.info(f"Extracting clip: {start_time:.2f}s - {end_time:.2f}s")

            # Get source video dimensions
            probe = ffmpeg.probe(source_video)
            video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            width = int(video_stream['width'])
            height = int(video_stream['height'])

            # Build FFmpeg command
            input_stream = ffmpeg.input(source_video, ss=start_time, t=end_time - start_time)

            if crop_to_vertical:
                # Calculate 9:16 crop dimensions
                target_aspect = 9 / 16
                source_aspect = width / height

                if source_aspect > target_aspect:
                    # Video is wider than 9:16, crop width
                    crop_width = int(height * target_aspect)
                    crop_height = height
                    x_offset = (width - crop_width) // 2  # Center crop
                    y_offset = 0
                else:
                    # Video is taller than 9:16, crop height
                    crop_width = width
                    crop_height = int(width / target_aspect)
                    x_offset = 0
                    y_offset = (height - crop_height) // 2

                logger.info(f"Cropping to {crop_width}x{crop_height} from {x_offset},{y_offset}")

                # Apply crop filter
                stream = input_stream.video.crop(x_offset, y_offset, crop_width, crop_height)
            else:
                stream = input_stream.video

            # Output with H.264 encoding (mobile-optimized)
            output = ffmpeg.output(
                stream,
                input_stream.audio,
                str(output_path),
                vcodec='libx264',
                acodec='aac',
                preset='medium',
                crf=23,  # Quality (lower = better, 18-28 is good range)
                movflags='faststart'  # Enable streaming
            )

            output.overwrite_output().run(capture_stdout=True, capture_stderr=True)

            logger.info(f"Clip exported to {output_path}")
            return output_path

        except ffmpeg.Error as e:
            logger.error(f"FFmpeg error exporting clip: {e.stderr.decode()}")
            raise
