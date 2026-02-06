"""
Clip detection orchestrator.
Analyzes transcripts and identifies high-value segments for clipping.
"""

import json
from pathlib import Path
from typing import List, Dict

from scoring.rules import ClipScorer
from utils.logger import logger, log_clip_score
from utils.config import DATA_DIR


class ClipDetector:
    """
    Orchestrates clip detection from transcripts.
    Uses heuristic scoring to identify academically valuable segments.
    """

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = DATA_DIR / "projects" / project_id
        self.scorer = ClipScorer()

    def detect_clips(
        self,
        min_score: float = 30.0,
        max_clips: int = 20,
        merge_nearby: bool = True,
        merge_gap: float = 2.0
    ) -> List[Dict]:
        """
        Detect high-value clips from project transcript.

        Args:
            min_score: Minimum score threshold (0-100)
            max_clips: Maximum number of clips to return
            merge_nearby: Whether to merge nearby high-scoring segments
            merge_gap: Maximum gap (seconds) to merge segments

        Returns:
            List of detected clips with scoring explanations
        """
        # Load transcript
        transcript_path = self.project_dir / "transcript.json"
        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript not found. Run transcription first.")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = json.load(f)

        logger.info(f"Analyzing {len(transcript['segments'])} transcript segments")

        # Score each segment
        scored_clips = self.scorer.score_transcript_segments(
            segments=transcript['segments'],
            min_score=min_score,
            max_clips=max_clips * 2  # Get more candidates before merging
        )

        logger.info(f"Found {len(scored_clips)} segments above score threshold {min_score}")

        # Optionally merge nearby segments
        if merge_nearby and len(scored_clips) > 0:
            scored_clips = self._merge_nearby_clips(scored_clips, merge_gap)
            logger.info(f"After merging nearby segments: {len(scored_clips)} clips")

        # Take top N after merging
        final_clips = scored_clips[:max_clips]

        # Log all final clips
        for i, clip in enumerate(final_clips, 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"CLIP #{i}/{len(final_clips)}")
            log_clip_score(logger, clip)

        # Save clips to file
        clips_path = self.project_dir / "clips.json"
        with open(clips_path, 'w', encoding='utf-8') as f:
            json.dump(final_clips, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(final_clips)} clips to {clips_path}")

        return final_clips

    def _merge_nearby_clips(self, clips: List[Dict], max_gap: float) -> List[Dict]:
        """
        Merge clips that are close together in time.

        This handles cases where multiple high-scoring sentences are adjacent.
        Instead of creating separate 20s clips, merge them into one coherent clip.

        Args:
            clips: List of scored clips
            max_gap: Maximum gap (seconds) between clips to merge

        Returns:
            List of merged clips
        """
        if not clips:
            return clips

        # Sort by start time
        sorted_clips = sorted(clips, key=lambda x: x['start_time'])

        merged = []
        current = sorted_clips[0].copy()

        for next_clip in sorted_clips[1:]:
            gap = next_clip['start_time'] - current['end_time']

            if gap <= max_gap:
                # Merge: extend current clip to include next clip
                current['end_time'] = next_clip['end_time']
                current['duration'] = current['end_time'] - current['start_time']
                current['text'] += " " + next_clip['text']

                # Combine reasons (keep unique)
                current['reasons'].extend(
                    r for r in next_clip['reasons']
                    if r not in current['reasons']
                )

                # Average scores weighted by duration
                total_duration = current['duration']
                current['score'] = (
                    (current['score'] + next_clip['score']) / 2
                )

                logger.debug(f"Merged clips: gap={gap:.1f}s, new duration={current['duration']:.1f}s")

            else:
                # Gap too large, save current and start new
                merged.append(current)
                current = next_clip.copy()

        # Add the last clip
        merged.append(current)

        # Re-sort by score
        merged.sort(key=lambda x: x['score'], reverse=True)

        return merged

    @staticmethod
    def load_clips(project_id: str) -> List[Dict]:
        """
        Load previously detected clips from file.

        Args:
            project_id: Project ID

        Returns:
            List of clip dictionaries
        """
        clips_path = DATA_DIR / "projects" / project_id / "clips.json"

        if not clips_path.exists():
            raise FileNotFoundError(f"No clips found. Run detection first.")

        with open(clips_path, 'r', encoding='utf-8') as f:
            return json.load(f)
