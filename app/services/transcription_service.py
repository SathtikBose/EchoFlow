import asyncio
import logging

from PySide6.QtCore import QThread, Signal

from app.speech.base import SpeechProvider

logger = logging.getLogger(__name__)


class TranscriptionService(QThread):
    # Signals for success and failure
    transcription_complete = Signal(str)
    transcription_error = Signal(str)

    def __init__(self, provider: SpeechProvider) -> None:
        super().__init__()
        self.provider = provider
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

            transcript = loop.run_until_complete(self.provider.transcribe(self.audio_data))
            loop.close()

            self.transcription_complete.emit(transcript)

        except Exception as e:
            logger.error(f"Transcription service error: {e}")
            self.transcription_error.emit(str(e))
