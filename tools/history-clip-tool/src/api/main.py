"""
Main FastAPI application.
Local-only video clipping tool for academic historical content.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api.routes import projects, transcribe, clips, export, ui
from models.database import init_db
from utils.logger import logger

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="History Clip Tool",
    description="Local-only video clipping tool optimized for evidence-based historical content",
    version="1.0.0"
)

# CORS middleware (allow local frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(transcribe.router)
app.include_router(clips.router)
app.include_router(export.router)
app.include_router(ui.router)  # UI-friendly routes for wizard

# Serve static frontend files
frontend_dir = Path(__file__).parent.parent.parent / "frontend" / "public"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="static")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "History Clip Tool API is running",
        "version": "1.0.0"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("="*80)
    logger.info("History Clip Tool API Starting")
    logger.info("="*80)
    logger.info("Local-only video clipping for academic historical content")
    logger.info("100% free to run | No cloud inference | No paid APIs")
    logger.info("="*80)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("History Clip Tool API shutting down")
