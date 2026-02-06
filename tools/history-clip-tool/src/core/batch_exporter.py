"""
Batch clip export with parallel processing support.
Exports multiple clips efficiently using multiprocessing.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

from core.exporter import ClipExporter
from utils.logger import logger
from utils.config import DATA_DIR


class BatchExporter:
    """
    Exports multiple clips in parallel for faster processing.
    Shows progress and handles errors gracefully.
    """

    def __init__(self, project_id: str, max_workers: Optional[int] = None):
        """
        Initialize batch exporter.

        Args:
            project_id: Project ID
            max_workers: Maximum parallel workers (default: CPU count - 1)
        """
        self.project_id = project_id
        self.project_dir = DATA_DIR / "projects" / project_id
        self.max_workers = max_workers or self._get_optimal_workers()

    @staticmethod
    def _get_optimal_workers() -> int:
        """
        Determine optimal number of worker processes.
        Video encoding is CPU-intensive, so use CPU count - 1.
        """
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        # Use CPU count - 1, minimum 1
        return max(1, cpu_count - 1)

    def export_all_clips(
        self,
        clips: List[Dict],
        caption_preset: str = "academic",
        caption_style: str = "sentence",  # "sentence", "word-by-word", or "karaoke"
        crop_mode: str = "center",
        parallel: bool = True
    ) -> Dict[str, any]:
        """
        Export all clips with optional parallel processing.

        Args:
            clips: List of clip dictionaries
            caption_preset: Caption style preset
            caption_style: Type of caption timing (sentence/word-by-word/karaoke)
            crop_mode: Crop mode for video
            parallel: Whether to use parallel processing

        Returns:
            Dictionary with export results and statistics
        """
        if not clips:
            logger.warning("No clips to export")
            return {"success": 0, "failed": 0, "total": 0, "duration": 0}

        start_time = time.time()
        total_clips = len(clips)

        logger.info(f"Starting batch export of {total_clips} clips")
        logger.info(f"Parallel processing: {'Enabled' if parallel else 'Disabled'}")
        logger.info(f"Max workers: {self.max_workers if parallel else 1}")
        logger.info(f"Caption style: {caption_style}")
        print()

        if parallel and total_clips > 1:
            results = self._export_parallel(
                clips, caption_preset, caption_style, crop_mode
            )
        else:
            results = self._export_sequential(
                clips, caption_preset, caption_style, crop_mode
            )

        # Calculate statistics
        successful = sum(1 for r in results if r['success'])
        failed = sum(1 for r in results if not r['success'])
        duration = time.time() - start_time

        stats = {
            "success": successful,
            "failed": failed,
            "total": total_clips,
            "duration": duration,
            "avg_time_per_clip": duration / total_clips if total_clips > 0 else 0,
            "results": results
        }

        # Print summary
        print()
        print("=" * 80)
        print("BATCH EXPORT COMPLETE")
        print("=" * 80)
        print(f"Total clips: {total_clips}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Total time: {duration:.1f}s ({duration/60:.1f} minutes)")
        print(f"Average time per clip: {stats['avg_time_per_clip']:.1f}s")
        print("=" * 80)

        # Log failures
        if failed > 0:
            print("\nFailed clips:")
            for result in results:
                if not result['success']:
                    print(f"  - Clip #{result['clip_number']}: {result['error']}")

        return stats

    def _export_parallel(
        self,
        clips: List[Dict],
        caption_preset: str,
        caption_style: str,
        crop_mode: str
    ) -> List[Dict]:
        """Export clips in parallel using multiprocessing."""
        results = []

        # Create tasks
        tasks = [
            (self.project_id, clip, i + 1, caption_preset, caption_style, crop_mode)
            for i, clip in enumerate(clips)
        ]

        # Progress tracking
        completed = 0
        total = len(tasks)

        print(f"Exporting {total} clips in parallel ({self.max_workers} workers)...\n")

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_clip = {
                executor.submit(_export_clip_worker, *task): task[2]
                for task in tasks
            }

            # Process as they complete
            for future in as_completed(future_to_clip):
                clip_num = future_to_clip[future]
                completed += 1

                try:
                    result = future.result()
                    results.append(result)

                    status = "✓" if result['success'] else "✗"
                    print(f"[{completed}/{total}] {status} Clip #{clip_num}: {result.get('output_path', result.get('error', 'Unknown'))}")

                except Exception as e:
                    logger.error(f"Unexpected error processing clip #{clip_num}: {e}")
                    results.append({
                        "clip_number": clip_num,
                        "success": False,
                        "error": str(e)
                    })
                    print(f"[{completed}/{total}] ✗ Clip #{clip_num}: {e}")

        return results

    def _export_sequential(
        self,
        clips: List[Dict],
        caption_preset: str,
        caption_style: str,
        crop_mode: str
    ) -> List[Dict]:
        """Export clips sequentially (one at a time)."""
        results = []
        total = len(clips)

        print(f"Exporting {total} clips sequentially...\n")

        for i, clip in enumerate(clips, 1):
            result = _export_clip_worker(
                self.project_id, clip, i, caption_preset, caption_style, crop_mode
            )
            results.append(result)

            status = "✓" if result['success'] else "✗"
            print(f"[{i}/{total}] {status} Clip #{i}: {result.get('output_path', result.get('error', 'Unknown'))}")

        return results


def _export_clip_worker(
    project_id: str,
    clip_data: Dict,
    clip_number: int,
    caption_preset: str,
    caption_style: str,
    crop_mode: str
) -> Dict:
    """
    Worker function for exporting a single clip.
    Designed to be called from multiprocessing pool.

    Args:
        project_id: Project ID
        clip_data: Clip dictionary
        clip_number: Clip number
        caption_preset: Caption preset
        caption_style: Caption style (sentence/word-by-word/karaoke)
        crop_mode: Crop mode

    Returns:
        Result dictionary with success status
    """
    try:
        # Import here to avoid issues with multiprocessing
        from core.exporter import ClipExporter
        from core.caption_renderer_enhanced import EnhancedCaptionRenderer
        from core.video_processor import VideoProcessor
        from pathlib import Path
        import ffmpeg

        project_dir = DATA_DIR / "projects" / project_id
        export_dir = project_dir / "exports"
        export_dir.mkdir(exist_ok=True)

        start_time = clip_data['start_time']
        end_time = clip_data['end_time']
        text = clip_data['text']
        duration = end_time - start_time

        # Find source video
        source_candidates = list(project_dir.glob("source.*"))
        if not source_candidates:
            raise FileNotFoundError("Source video not found")
        source_video = source_candidates[0]

        # Step 1: Extract clip without captions
        video_processor = VideoProcessor(project_id)
        temp_clip = export_dir / f"clip_{clip_number:03d}_temp.mp4"
        video_processor.extract_clip(
            source_video=str(source_video),
            start_time=start_time,
            end_time=end_time,
            output_path=temp_clip,
            crop_to_vertical=True,
            crop_mode=crop_mode
        )

        # Step 2: Create subtitle file based on caption style
        caption_renderer = EnhancedCaptionRenderer(preset=caption_preset)
        srt_path = export_dir / f"clip_{clip_number:03d}.srt"

        if caption_style == "word-by-word":
            caption_renderer.create_word_by_word_srt(
                text=text,
                duration=duration,
                output_path=srt_path,
                words_per_caption=3
            )
        elif caption_style == "karaoke":
            # Convert to ASS format
            ass_path = export_dir / f"clip_{clip_number:03d}.ass"
            caption_renderer.create_karaoke_ass(
                text=text,
                duration=duration,
                output_path=ass_path
            )
            srt_path = ass_path  # Use ASS file instead
        else:  # sentence (default)
            caption_renderer.create_sentence_srt(
                text=text,
                duration=duration,
                output_path=srt_path
            )

        # Step 3: Burn subtitles into video
        final_clip = export_dir / f"clip_{clip_number:03d}.mp4"
        input_stream = ffmpeg.input(str(temp_clip))

        # Use subtitles filter (works for both SRT and ASS)
        video = input_stream.video.filter('subtitles', str(srt_path).replace('\\', '/').replace(':', '\\:'))
        audio = input_stream.audio

        output = ffmpeg.output(
            video,
            audio,
            str(final_clip),
            vcodec='libx264',
            acodec='aac',
            preset='medium',
            crf=23
        )

        output.overwrite_output().run(capture_stdout=True, capture_stderr=True)

        # Step 4: Clean up temp file
        temp_clip.unlink()

        # Step 5: Save metadata
        metadata = {
            "clip_number": clip_number,
            "output_path": str(final_clip),
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "text": text,
            "score": clip_data.get('score', 0),
            "caption_preset": caption_preset,
            "caption_style": caption_style
        }

        metadata_path = export_dir / f"clip_{clip_number:03d}_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return {
            "clip_number": clip_number,
            "success": True,
            "output_path": str(final_clip)
        }

    except Exception as e:
        logger.error(f"Failed to export clip #{clip_number}: {e}")
        return {
            "clip_number": clip_number,
            "success": False,
            "error": str(e)
        }
