"""
Structured logging utility.
All clip detection reasoning is logged for transparency.
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

from utils.config import LOGS_DIR


def setup_logger(name: str = "history-clip-tool") -> logging.Logger:
    """
    Set up a logger with both file and console handlers.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # File handler with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOGS_DIR / f"clip_detection_{timestamp}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_clip_score(logger: logging.Logger, clip_data: Dict[str, Any]) -> None:
    """
    Log clip scoring decision with full reasoning.

    Args:
        logger: Logger instance
        clip_data: Dictionary containing score, reasons, duration, text
    """
    logger.info("=" * 80)
    logger.info(f"CLIP SCORE: {clip_data['score']}/100")
    logger.info(f"Duration: {clip_data['duration']:.1f}s")
    logger.info(f"Text preview: {clip_data['text'][:100]}...")
    logger.info("Scoring reasons:")
    for reason in clip_data['reasons']:
        logger.info(f"  - {reason}")
    logger.info("=" * 80)


# Global logger instance
logger = setup_logger()
