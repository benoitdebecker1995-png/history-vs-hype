"""
Audio transcription using faster-whisper.
Local-only, no API calls, CPU-friendly.
"""

import json
from pathlib import Path
from typing import List, Dict
from faster_whisper import WhisperModel

from utils.logger import logger
from utils.config import MODELS_DIR, DATA_DIR


class Transcriber:
    """
    Wrapper for faster-whisper transcription.
    Runs entirely locally on CPU.
    """

    def __init__(self, model_size: str = "base", device: str = "cpu"):
        """
        Initialize transcriber with specified model.

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
                       - tiny: fastest, least accurate (~1GB)
                       - base: good balance (~1GB) [DEFAULT]
                       - small: better accuracy (~2GB)
                       - medium: high accuracy (~5GB)
                       - large: best accuracy (~10GB)
            device: "cpu" or "cuda" (GPU)
        """
        self.model_size = model_size
        self.device = device

        logger.info(f"Loading faster-whisper model: {model_size} on {device}")

        # Download model to local models directory if not present
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type="int8",  # Quantized for faster CPU inference
            download_root=str(MODELS_DIR / "whisper")
        )

        logger.info("Model loaded successfully")

    def transcribe(self, audio_path: Path, project_id: str) -> Dict:
        """
        Transcribe audio file and save results.

        Args:
            audio_path: Path to audio WAV file
            project_id: Project ID for saving transcript

        Returns:
            Dictionary with segments and metadata
        """
        logger.info(f"Transcribing audio: {audio_path}")

        # Run transcription
        # word_timestamps=True gives word-level timing for better clip boundaries
        segments, info = self.model.transcribe(
            str(audio_path),
            language="en",  # Force English (adjust if needed)
            word_timestamps=True,
            vad_filter=True,  # Voice activity detection filters silence
            beam_size=5  # Beam search size (higher = more accurate but slower)
        )

        # Convert generator to list and format
        transcript_data = {
            "language": info.language,
            "duration": info.duration,
            "segments": []
        }

        for segment in segments:
            segment_dict = {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "words": []
            }

            # Include word-level timestamps if available
            if segment.words:
                for word in segment.words:
                    segment_dict["words"].append({
                        "start": word.start,
                        "end": word.end,
                        "word": word.word,
                        "probability": word.probability
                    })

            transcript_data["segments"].append(segment_dict)

            logger.info(f"Segment {len(transcript_data['segments'])}: "
                       f"{segment.start:.1f}s - {segment.end:.1f}s | "
                       f"{segment.text[:50]}...")

        # Save to project directory
        project_dir = DATA_DIR / "projects" / project_id
        transcript_path = project_dir / "transcript.json"

        with open(transcript_path, 'w', encoding='utf-8') as f:
            json.dump(transcript_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Transcription complete: {len(transcript_data['segments'])} segments")
        logger.info(f"Saved to: {transcript_path}")

        return transcript_data

    @staticmethod
    def load_transcript(project_id: str) -> Dict:
        """
        Load existing transcript from project directory.

        Args:
            project_id: Project ID

        Returns:
            Transcript data dictionary
        """
        transcript_path = DATA_DIR / "projects" / project_id / "transcript.json"

        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript not found: {transcript_path}")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            return json.load(f)
