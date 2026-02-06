"""
Clip detection routes.
Analyze transcripts and identify high-value segments.
"""

from fastapi import APIRouter, HTTPException
from typing import List

from models.database import get_session, Project, Clip
from models.schemas import DetectedClipResponse, ClipResponse
from core.clip_detector import ClipDetector
from utils.logger import logger
import json

router = APIRouter(prefix="/clips", tags=["clips"])


@router.post("/{project_id}/detect")
def detect_clips(
    project_id: str,
    min_score: float = 30.0,
    max_clips: int = 20,
    merge_nearby: bool = True
):
    """
    Detect high-value clips from project transcript.

    Args:
        project_id: Project UUID
        min_score: Minimum score threshold (0-100)
        max_clips: Maximum number of clips to return
        merge_nearby: Whether to merge nearby high-scoring segments

    Returns:
        List of detected clips with scoring explanations
    """
    try:
        # Verify project exists and is transcribed
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if not project.transcribed:
            raise HTTPException(status_code=400, detail="Project must be transcribed first")

        # Run clip detection
        detector = ClipDetector(project_id)
        detected_clips = detector.detect_clips(
            min_score=min_score,
            max_clips=max_clips,
            merge_nearby=merge_nearby
        )

        # Save clips to database
        for clip_data in detected_clips:
            clip = Clip(
                project_id=project_id,
                start_time=clip_data['start_time'],
                end_time=clip_data['end_time'],
                duration=clip_data['duration'],
                transcript_text=clip_data['text'],
                score=clip_data['score'],
                score_reasons=json.dumps(clip_data['reasons'])
            )
            session.add(clip)

        project.clips_detected = True
        session.commit()
        session.close()

        logger.info(f"Saved {len(detected_clips)} clips to database")

        # Convert to response format
        return [
            DetectedClipResponse(
                start_time=c['start_time'],
                end_time=c['end_time'],
                duration=c['duration'],
                text=c['text'],
                score=c['score'],
                reasons=c['reasons']
            )
            for c in detected_clips
        ]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting clips: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=List[ClipResponse])
def get_project_clips(project_id: str):
    """
    Get all clips for a project.

    Args:
        project_id: Project UUID

    Returns:
        List of clips
    """
    try:
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        clips = session.query(Clip).filter(Clip.project_id == project_id).all()
        session.close()

        return [ClipResponse.from_orm(c) for c in clips]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting clips: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clip/{clip_id}", response_model=ClipResponse)
def get_clip(clip_id: int):
    """
    Get a specific clip by ID.

    Args:
        clip_id: Clip ID

    Returns:
        Clip data
    """
    try:
        session = get_session()
        clip = session.query(Clip).filter(Clip.id == clip_id).first()
        session.close()

        if not clip:
            raise HTTPException(status_code=404, detail="Clip not found")

        return ClipResponse.from_orm(clip)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting clip: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clip/{clip_id}")
def delete_clip(clip_id: int):
    """
    Delete a clip.

    Args:
        clip_id: Clip ID

    Returns:
        Success message
    """
    try:
        session = get_session()
        clip = session.query(Clip).filter(Clip.id == clip_id).first()

        if not clip:
            raise HTTPException(status_code=404, detail="Clip not found")

        session.delete(clip)
        session.commit()
        session.close()

        return {"message": "Clip deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting clip: {e}")
        raise HTTPException(status_code=500, detail=str(e))
