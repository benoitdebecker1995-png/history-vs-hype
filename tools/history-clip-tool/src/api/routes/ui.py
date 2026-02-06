"""
UI-friendly routes.
Provides simplified, presentation-focused endpoints for the wizard UI.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict
import json

from models.database import get_session, Project, Clip
from core.clip_detector import ClipDetector
from utils.logger import logger

router = APIRouter(prefix="/ui", tags=["ui"])

# Human-readable reason mapping
REASON_MAP = {
    "Contains primary source reference": "Mentions a primary source",
    "References specific date": "References a specific date",
    "Citation language detected": "Cites a scholar or study",
    "Quantitative data": "Includes specific numbers or statistics",
    "Legal/technical terminology": "Uses precise legal or historical terms",
    "Causal explanation": "Explains cause and effect",
    "Myth-debunking pattern": "Challenges a common misconception",
    "Comparative analysis": "Compares different perspectives or periods",
    "Conclusion signal": "Draws a clear conclusion",
    "Complete sentence": "Forms a complete thought",
    "Optimal duration": "Good length for a short video",
}


def translate_reasons(technical_reasons: List[str]) -> List[str]:
    """
    Convert technical scoring reasons to user-friendly language.

    Args:
        technical_reasons: List of technical reason strings

    Returns:
        List of human-readable reasons (only positive ones)
    """
    friendly_reasons = []

    for reason in technical_reasons:
        # Skip penalties and technical details
        if any(skip in reason.lower() for skip in ['(-', 'incomplete', 'too short', 'too long']):
            continue

        # Find matching pattern
        for pattern, friendly in REASON_MAP.items():
            if pattern.lower() in reason.lower():
                if friendly not in friendly_reasons:
                    friendly_reasons.append(friendly)
                break
        else:
            # If no exact match, try to extract positive aspects
            if '(+' in reason and 'detected' in reason.lower():
                # Generic positive detection
                if "Forms a complete thought" not in friendly_reasons:
                    friendly_reasons.append("Forms a complete thought")

    # Limit to 4-5 most important reasons
    return friendly_reasons[:5]


def selectivity_to_score(selectivity: str) -> tuple:
    """
    Convert selectivity level to min_score and max_clips.

    Args:
        selectivity: "low", "medium", or "high"

    Returns:
        Tuple of (min_score, max_clips)
    """
    mapping = {
        "low": (20, 30),      # Keep more clips
        "medium": (30, 20),   # Balanced (default)
        "high": (50, 10),     # Only the best
    }
    return mapping.get(selectivity, (30, 20))


@router.get("/clips/{project_id}")
def get_clips_for_ui(project_id: str, selectivity: str = "medium"):
    """
    Get clips formatted for UI display with human-readable reasons.

    Args:
        project_id: Project UUID
        selectivity: "low", "medium", or "high"

    Returns:
        List of clips with friendly formatting
    """
    try:
        # Verify project exists and is transcribed
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if not project.transcribed:
            raise HTTPException(status_code=400, detail="Project not transcribed yet")

        # Get selectivity parameters
        min_score, max_clips = selectivity_to_score(selectivity)

        # Re-run detection with new parameters
        detector = ClipDetector(project_id)
        detected_clips = detector.detect_clips(
            min_score=min_score,
            max_clips=max_clips,
            merge_nearby=True
        )

        # Format for UI
        ui_clips = []
        for clip in detected_clips:
            # Translate technical reasons to friendly language
            technical_reasons = clip.get('reasons', [])
            friendly_reasons = translate_reasons(technical_reasons)

            # Create preview text (first 100 chars)
            full_text = clip['text']
            preview_text = full_text[:100] + "..." if len(full_text) > 100 else full_text

            ui_clip = {
                "start": clip['start_time'],
                "end": clip['end_time'],
                "duration": round(clip['duration'], 1),
                "preview_text": preview_text,
                "full_text": full_text,
                "reasons": friendly_reasons,
                "score": clip['score'],  # Include for debugging, but don't show in UI
            }
            ui_clips.append(ui_clip)

        session.close()

        return {
            "clips": ui_clips,
            "total": len(ui_clips),
            "selectivity": selectivity
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting UI clips: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transcription-status/{project_id}")
def get_transcription_status(project_id: str):
    """
    Get transcription status for progress polling.

    Args:
        project_id: Project UUID

    Returns:
        Status and progress information
    """
    try:
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()
        session.close()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # For now, transcription is all-or-nothing
        # In future, could add real progress tracking
        if project.transcribed:
            return {
                "status": "complete",
                "progress": 1.0,
                "message": "Transcription complete"
            }
        else:
            # If not complete, assume in progress
            # This is a simplification - real implementation would track actual progress
            return {
                "status": "processing",
                "progress": 0.5,  # Assume 50% if we don't have real progress
                "message": "Transcribing..."
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting transcription status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clips/toggle/{project_id}/{clip_index}")
def toggle_clip_selection(project_id: str, clip_index: int, kept: bool):
    """
    Mark a clip as kept or discarded.

    This is for UI state management. The actual export happens later.

    Args:
        project_id: Project UUID
        clip_index: Index of clip in current detection results
        kept: True to keep, False to discard

    Returns:
        Updated state
    """
    # This is a simplified version
    # In a full implementation, we'd store selection state in database
    # For now, the frontend manages this state

    return {
        "project_id": project_id,
        "clip_index": clip_index,
        "kept": kept
    }


@router.get("/project-info/{project_id}")
def get_project_info(project_id: str):
    """
    Get project information for UI display.

    Args:
        project_id: Project UUID

    Returns:
        Project details with friendly formatting
    """
    try:
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()
        session.close()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Format duration nicely
        duration_min = int(project.duration // 60) if project.duration else 0
        duration_sec = int(project.duration % 60) if project.duration else 0

        return {
            "id": project.id,
            "name": project.name,
            "duration": project.duration,
            "duration_formatted": f"{duration_min}:{duration_sec:02d}",
            "transcribed": project.transcribed,
            "clips_detected": project.clips_detected,
            "resolution": project.resolution,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
