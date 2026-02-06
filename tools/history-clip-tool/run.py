#!/usr/bin/env python3
"""
Launch script for History Clip Tool.
Starts the FastAPI server on localhost.
"""

import uvicorn
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def main():
    """Start the FastAPI server."""
    print("="*80)
    print("History Clip Tool")
    print("="*80)
    print("Local-only video clipping for evidence-based historical content")
    print()
    print("Starting server at: http://localhost:8000")
    print("Press Ctrl+C to stop")
    print("="*80)
    print()

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",  # Local only - no external access
        port=8000,
        reload=False,  # Disable auto-reload in production
        log_level="info"
    )


if __name__ == "__main__":
    main()
