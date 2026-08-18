import asyncio
import logging

from PySide6.QtCore import QThread, Signal

from app.llm.base import LlmProvider
from app.speech.base import SpeechProvider

logger = logging.getLogger(__name__)


class TranscriptionService(QThread):
    # Signals for success and failure
    transcription_complete = Signal(str)
    transcription_error = Signal(str)

    def __init__(
        self, speech_provider: SpeechProvider, llm_provider: LlmProvider | None = None
    ) -> None:
        super().__init__()
        self.speech_provider = speech_provider
        self.llm_provider = llm_provider
        self.audio_data: bytes | None = None

    def start_transcription(self, audio_data: bytes) -> None:
        """Called by the main thread to begin transcription."""
        if self.isRunning():
            logger.warning("Transcription already in progress.")
            return

        self.audio_data = audio_data
        self.start()

    def run(self) -> None:
        """Executes in a background QThread."""
        if not self.audio_data:
            self.transcription_error.emit("No audio data provided.")
            return

        try:
            # Run the async provider function synchronously within this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Step 1: Speech to Text
            transcript = loop.run_until_complete(self.speech_provider.transcribe(self.audio_data))

            # Step 2: LLM Transformation (if configured)
            if self.llm_provider and transcript:
                transcript = loop.run_until_complete(self.llm_provider.transform_text(transcript))

            loop.close()

            self.transcription_complete.emit(transcript)

        except Exception as e:
            logger.error(f"Transcription service error: {e}")
            self.transcription_error.emit(str(e))
