import sys

from PySide6.QtWidgets import QApplication

from app.audio.recorder import AudioRecorder
from app.input.hotkeys import HotkeyManager
from app.input.insertion import TextInserter
from app.llm.nvidia import NvidiaLlmProvider
from app.services.transcription_service import TranscriptionService
from app.speech.nvidia import NvidiaSpeechProvider
from app.ui.tray import TrayManager


class EchoFlowApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        # Initialize services
        self.hotkeys = HotkeyManager()
        self.inserter = TextInserter()
        self.recorder = AudioRecorder()

        # State
        self.current_mode = "default"

        # Use try/except or lazy init if settings are missing?
        # For now, initialize the provider
        self.speech_provider = NvidiaSpeechProvider()
        self.llm_provider = NvidiaLlmProvider()
        self.transcriber = TranscriptionService(self.speech_provider, self.llm_provider)

        # UI
        self.tray = TrayManager(self)
        self.tray.mode_changed.connect(self._on_mode_changed)

        # Wire up hotkeys to audio recording
        self.hotkeys.hotkey_pressed.connect(self.recorder.start_recording)
        self.hotkeys.hotkey_released.connect(self.recorder.stop_recording)

        # Handle audio ready
        self.recorder.audio_ready.connect(self._on_audio_ready)

        # Handle transcription results
        self.transcriber.transcription_complete.connect(self._on_transcription_complete)
        self.transcriber.transcription_error.connect(self._on_transcription_error)
        self.transcriber.command_executed.connect(self._on_command_executed)

        # Start hotkey listener
        self.hotkeys.start()

        # Cleanup on exit
        self.aboutToQuit.connect(self.shutdown)

    def _on_mode_changed(self, mode: str) -> None:
        self.current_mode = mode

    def _on_audio_ready(self, audio_data: bytes) -> None:
        self.transcriber.start_transcription(audio_data, self.current_mode)

    def _on_transcription_complete(self, text: str) -> None:
        print(f"App: Transcription complete: {text}")
        self.inserter.insert_text(text)

    def _on_transcription_error(self, error: str) -> None:
        print(f"App: Transcription failed: {error}")

    def _on_command_executed(self, command: str) -> None:
        print(f"App: {command}")
        self.tray.notify("Command Executed", command)

    def shutdown(self) -> None:
        self.hotkeys.stop()
        self.recorder.stop_recording()


def run_app() -> int:
    app = EchoFlowApp(sys.argv)
    return app.exec()
