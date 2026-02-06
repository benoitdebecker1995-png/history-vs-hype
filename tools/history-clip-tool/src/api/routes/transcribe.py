"""
Transcription routes.
Handle audio extraction and transcription with faster-whisper.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional

from models.database import get_session, Project
from models.schemas import TranscriptionResponse, TranscriptSegment
from core.video_processor import VideoProcessor
from core.transcriber import Transcriber
from utils.logger import logger

router = APIRouter(prefix="/transcribe", tags=["transcription"])


def run_transcription_task(project_id: str, model_size: str):
    """
    Background task for transcription.
    This can take several minutes for long videos.

    Args:
        project_id: Project UUID
        model_size: Whisper model size
    """
    try:
        logger.info(f"Starting transcription for project {project_id}")

        # Step 1: Extract audio
        video_processor = VideoProcessor(project_id)

        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()

        if not project:
            logger.error(f"Project not found: {project_id}")
            return

        audio_path = video_processor.extract_audio(project.source_video_path)
        logger.info(f"Audio extracted: {audio_path}")

        # Step 2: Transcribe
        transcriber = Transcriber(model_size=model_size)
        transcript = transcriber.transcribe(audio_path, project_id)

        # Step 3: Update project status
        project.transcribed = True
        session.commit()
        session.close()

        logger.info(f"Transcription complete for project {project_id}")

    except Exception as e:
        logger.error(f"Transcription task failed: {e}")
        # Update project status to indicate failure
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()
        if project:
            project.transcribed = False
            session.commit()
        session.close()


@router.post("/{project_id}")
async def transcribe_project(
    project_id: str,
    background_tasks: BackgroundTasks,
    model_size: str = "base"
):
    """
    Start transcription for a project.

    This is a long-running task that runs in the background.
    Poll the project status to check when it's complete.

    Args:
        project_id: Project UUID
        model_size: Whisper model size (tiny, base, small, medium, large)

    Returns:
        Status message
    """
    try:
        # Verify project exists
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()
        session.close()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if project.transcribed:
            raise HTTPException(status_code=400, detail="Project already transcribed")

        # Start background task
        background_tasks.add_task(run_transcription_task, project_id, model_size)

        logger.info(f"Transcription task started for project {project_id}")

        return {
            "message": "Transcription started",
            "project_id": project_id,
            "model_size": model_size,
            "status": "Check project.transcribed field for completion"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=TranscriptionResponse)
def get_transcription(project_id: str):
    """
    Get transcription results for a project.

    Args:
        project_id: Project UUID

    Returns:
        Transcription data with segments
    """
    try:
        # Verify project exists and is transcribed
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()
        session.close()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if not project.transcribed:
            raise HTTPException(status_code=400, detail="Project not transcribed yet")

        # Load transcript
        transcript = Transcriber.load_transcript(project_id)

        # Convert to response format
        segments = [
            TranscriptSegment(
                start=seg['start'],
                end=seg['end'],
                text=seg['text']
            )
            for seg in transcript['segments']
        ]

        return TranscriptionResponse(
            segments=segments,
            language=transcript['language'],
            duration=transcript['duration']
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))
