import asyncio
import logging

from PySide6.QtCore import QThread, Signal

from app.input.commands import CommandProcessor
from app.input.dictionary import DictionaryProcessor
from app.input.snippets import SnippetProcessor
from app.llm.base import LlmProvider
from app.speech.base import SpeechProvider

logger = logging.getLogger(__name__)


class TranscriptionService(QThread):
    # Signals for success and failure
    transcription_complete = Signal(str)
    transcription_error = Signal(str)
    command_executed = Signal(str)

    def __init__(
        self, speech_provider: SpeechProvider, llm_provider: LlmProvider | None = None
    ) -> None:
        super().__init__()
        self.speech_provider = speech_provider
        self.llm_provider = llm_provider
        self.command_processor = CommandProcessor()
        self.dictionary_processor = DictionaryProcessor()
        self.snippet_processor = SnippetProcessor()
        self.audio_data: bytes | None = None
        self.mode: str = "default"

    def start_transcription(self, audio_data: bytes, mode: str = "default") -> None:
        """Called by the main thread to begin transcription."""
        if self.isRunning():
            logger.warning("Transcription already in progress.")
            return

        self.audio_data = audio_data
        self.mode = mode
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
            original_transcript = loop.run_until_complete(
                self.speech_provider.transcribe(self.audio_data)
            )
            transcript = original_transcript

            # Step 1.2: Dictionary Replacement
            if transcript:
                transcript = self.dictionary_processor.process(transcript)

            # Step 1.5: Voice Command check
            if transcript and self.command_processor.process(transcript):
                loop.close()
                self.command_executed.emit(f"Command: {transcript.strip()}")
                return

            # Step 1.8: Snippet expansion
            if transcript:
                snippet = self.snippet_processor.process(transcript)
                if snippet:
                    loop.close()
                    # Skip LLM and just return the expanded snippet
                    self.transcription_complete.emit(f"{original_transcript}|{snippet}")
                    return

            # Step 2: LLM Transformation (if configured)
            if self.llm_provider and transcript:
                transcript = loop.run_until_complete(
                    self.llm_provider.transform_text(transcript, mode=self.mode)
                )

            loop.close()

            self.transcription_complete.emit(f"{original_transcript}|{transcript}")

        except Exception as e:
            logger.error(f"Transcription service error: {e}")
            self.transcription_error.emit(str(e))
