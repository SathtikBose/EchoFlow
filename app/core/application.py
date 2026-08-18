import sys

from PySide6.QtWidgets import QApplication

from app.audio.recorder import AudioRecorder
from app.input.hotkeys import HotkeyManager
from app.input.insertion import TextInserter
from app.llm.nvidia import NvidiaLlmProvider
from app.services.transcription_service import TranscriptionService
from app.speech.nvidia import NvidiaSpeechProvider


class EchoFlowApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        # Initialize services
        self.hotkeys = HotkeyManager()
        self.inserter = TextInserter()
        self.recorder = AudioRecorder()

        # Use try/except or lazy init if settings are missing?
        # For now, initialize the provider
        self.speech_provider = NvidiaSpeechProvider()
        self.llm_provider = NvidiaLlmProvider()
        self.transcriber = TranscriptionService(self.speech_provider, self.llm_provider)

        # Wire up hotkeys to audio recording
        self.hotkeys.hotkey_pressed.connect(self.recorder.start_recording)
        self.hotkeys.hotkey_released.connect(self.recorder.stop_recording)

        # Handle audio ready
        self.recorder.audio_ready.connect(self.transcriber.start_transcription)

        # Handle transcription results
        self.transcriber.transcription_complete.connect(self._on_transcription_complete)
        self.transcriber.transcription_error.connect(self._on_transcription_error)

        # Start hotkey listener
        self.hotkeys.start()

        # Cleanup on exit
        self.aboutToQuit.connect(self.shutdown)

    def _on_transcription_complete(self, text: str) -> None:
        print(f"App: Transcription complete: {text}")
        self.inserter.insert_text(text)

    def _on_transcription_error(self, error: str) -> None:
        print(f"App: Transcription failed: {error}")

    def shutdown(self) -> None:
        self.hotkeys.stop()
        self.recorder.stop_recording()


def run_app() -> int:
    app = EchoFlowApp(sys.argv)
    return app.exec()
