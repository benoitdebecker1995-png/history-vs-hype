"""
Export routes.
Handle final video clip export with captions.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import json

from models.database import get_session, Clip
from models.schemas import ClipExportRequest
from core.exporter import ClipExporter
from core.clip_detector import ClipDetector
from utils.logger import logger

router = APIRouter(prefix="/export", tags=["export"])


@router.post("/clip/{clip_id}")
def export_clip(clip_id: int, request: ClipExportRequest):
    """
    Export a clip as a final video file with captions.

    Args:
        clip_id: Clip ID
        request: Export configuration

    Returns:
        Path to exported video file
    """
    try:
        # Get clip from database
        session = get_session()
        clip = session.query(Clip).filter(Clip.id == clip_id).first()

        if not clip:
            raise HTTPException(status_code=404, detail="Clip not found")

        project_id = clip.project_id

        # Prepare clip data
        clip_data = {
            'start_time': clip.start_time,
            'end_time': clip.end_time,
            'duration': clip.duration,
            'text': clip.transcript_text,
            'score': clip.score,
            'reasons': json.loads(clip.score_reasons) if clip.score_reasons else []
        }

        # Export
        exporter = ClipExporter(project_id)
        output_path = exporter.export_clip(
            clip_data=clip_data,
            clip_number=clip_id,
            caption_preset=request.caption_preset,
            crop_mode=request.crop_mode
        )

        # Update database
        clip.exported = True
        clip.export_path = str(output_path)
        clip.caption_preset = request.caption_preset
        session.commit()
        session.close()

        logger.info(f"Clip {clip_id} exported to {output_path}")

        return {
            "message": "Clip exported successfully",
            "clip_id": clip_id,
            "output_path": str(output_path),
            "caption_preset": request.caption_preset
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting clip: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clip/{clip_id}/download")
def download_clip(clip_id: int):
    """
    Download an exported clip.

    Args:
        clip_id: Clip ID

    Returns:
        Video file download
    """
    try:
        session = get_session()
        clip = session.query(Clip).filter(Clip.id == clip_id).first()
        session.close()

        if not clip:
            raise HTTPException(status_code=404, detail="Clip not found")

        if not clip.exported or not clip.export_path:
            raise HTTPException(status_code=400, detail="Clip not exported yet")

        # Return file
        return FileResponse(
            path=clip.export_path,
            media_type="video/mp4",
            filename=f"clip_{clip_id:03d}.mp4"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading clip: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/project/{project_id}/batch")
def batch_export_all_clips(project_id: str, caption_preset: str = "academic"):
    """
    Export all clips for a project.

    Args:
        project_id: Project UUID
        caption_preset: Caption style preset

    Returns:
        Summary of exported clips
    """
    try:
        session = get_session()
        clips = session.query(Clip).filter(Clip.project_id == project_id).all()

        if not clips:
            raise HTTPException(status_code=404, detail="No clips found for project")

        exported_paths = []
        exporter = ClipExporter(project_id)

        for clip in clips:
            clip_data = {
                'start_time': clip.start_time,
                'end_time': clip.end_time,
                'duration': clip.duration,
                'text': clip.transcript_text,
                'score': clip.score,
                'reasons': json.loads(clip.score_reasons) if clip.score_reasons else []
            }

            output_path = exporter.export_clip(
                clip_data=clip_data,
                clip_number=clip.id,
                caption_preset=caption_preset
            )

            clip.exported = True
            clip.export_path = str(output_path)
            clip.caption_preset = caption_preset

            exported_paths.append(str(output_path))

        session.commit()
        session.close()

        logger.info(f"Batch exported {len(exported_paths)} clips")

        return {
            "message": "Batch export complete",
            "clips_exported": len(exported_paths),
            "output_paths": exported_paths
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch export: {e}")
        raise HTTPException(status_code=500, detail=str(e))
