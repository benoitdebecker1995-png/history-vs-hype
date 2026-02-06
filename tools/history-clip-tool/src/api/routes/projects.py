"""
Project management routes.
Create, list, and manage video projects.
"""

import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from models.database import get_session, Project
from models.schemas import ProjectCreate, ProjectResponse
from core.video_processor import VideoProcessor
from utils.logger import logger
from utils.config import DATA_DIR

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
async def create_project(name: str, video: UploadFile = File(...)):
    """
    Create a new project by uploading a video file.

    Args:
        name: Project name
        video: Video file upload

    Returns:
        Created project data
    """
    try:
        # Generate unique project ID
        project_id = str(uuid.uuid4())

        logger.info(f"Creating project: {name} (ID: {project_id})")

        # Save uploaded video
        project_dir = DATA_DIR / "projects" / project_id
        project_dir.mkdir(parents=True, exist_ok=True)

        # Get file extension
        file_extension = Path(video.filename).suffix
        video_path = project_dir / f"source{file_extension}"

        # Save uploaded file
        with open(video_path, "wb") as f:
            content = await video.read()
            f.write(content)

        logger.info(f"Video saved to {video_path}")

        # Extract metadata
        video_processor = VideoProcessor(project_id)
        metadata = video_processor.get_video_metadata(str(video_path))

        # Create database entry
        session = get_session()
        project = Project(
            id=project_id,
            name=name,
            source_video_path=str(video_path),
            duration=metadata['duration'],
            fps=metadata['fps'],
            resolution=metadata['resolution']
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        session.close()

        logger.info(f"Project created: {project_id}")

        return ProjectResponse.from_orm(project)

    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ProjectResponse])
def list_projects():
    """
    List all projects.

    Returns:
        List of all projects
    """
    try:
        session = get_session()
        projects = session.query(Project).all()
        session.close()
        return [ProjectResponse.from_orm(p) for p in projects]

    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str):
    """
    Get a specific project by ID.

    Args:
        project_id: Project UUID

    Returns:
        Project data
    """
    try:
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()
        session.close()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return ProjectResponse.from_orm(project)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
def delete_project(project_id: str):
    """
    Delete a project and all its data.

    Args:
        project_id: Project UUID

    Returns:
        Success message
    """
    try:
        session = get_session()
        project = session.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Delete database entry
        session.delete(project)
        session.commit()
        session.close()

        # Delete files
        import shutil
        project_dir = DATA_DIR / "projects" / project_id
        if project_dir.exists():
            shutil.rmtree(project_dir)

        logger.info(f"Project deleted: {project_id}")

        return {"message": "Project deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail=str(e))
