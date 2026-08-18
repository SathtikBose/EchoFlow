import sys

from PySide6.QtWidgets import QApplication

from app.audio.recorder import AudioRecorder
from app.db.history import HistoryDB
from app.input.hotkeys import HotkeyManager
from app.input.insertion import TextInserter
from app.llm.nvidia import NvidiaLlmProvider
from app.services.transcription_service import TranscriptionService
from app.speech.google_sr import GoogleSpeechProvider
from app.ui.tray import TrayManager


class EchoFlowApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        # Initialize services
        self.hotkeys = HotkeyManager()
        self.inserter = TextInserter()
        self.recorder = AudioRecorder()
        self.history_db = HistoryDB()

        # State
        self.current_mode = "default"

        # Audio Recorder
        self.recorder = AudioRecorder()
        self.recorder.audio_ready.connect(self._on_audio_ready)
        self.recorder.error_occurred.connect(self._on_recorder_error)

        # UI Overlay
        from app.ui.overlay import RecordingOverlay
        self.overlay = RecordingOverlay()

        # UI Tray
        self.tray = TrayManager(self)
        self.tray.mode_changed.connect(self._on_mode_changed)

        # Hotkeys
        self.hotkey_manager = HotkeyManager()
        self.hotkey_manager.hotkey_pressed.connect(self._on_hotkey_pressed)
        self.hotkey_manager.hotkey_released.connect(self._on_hotkey_released)
        self.hotkey_manager.hotkey_locked.connect(self._on_hotkey_locked)

        # Use try/except or lazy init if settings are missing?
        # For now, initialize the provider
        self.speech_provider = GoogleSpeechProvider()
        self.transcriber = TranscriptionService(self.speech_provider)

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
        from app.utils.window import get_active_window_title

        app_context = get_active_window_title()
        self.transcriber.start_transcription(audio_data, self.current_mode, app_context)

    def _on_transcription_complete(self, data: str) -> None:
        try:
            original, final = data.split("|", 1)
        except ValueError:
            original, final = data, data

        print(f"App: Transcription complete: {final}")
        self.inserter.insert_text(final)

        # Save to DB
        if final.strip():
            self.history_db.add_record(original, final, self.current_mode, True)

    def _on_transcription_error(self, error: str) -> None:
        print(f"App: Transcription failed: {error}")

    def _on_hotkey_pressed(self) -> None:
        """Triggered when the hotkey is initially pressed."""
        self.overlay.show_overlay(locked=False)
        self.recorder.start_recording()

    def _on_hotkey_locked(self) -> None:
        """Triggered when the hotkey is double-clicked to lock."""
        self.overlay.set_locked(True)

    def _on_hotkey_released(self) -> None:
        """Triggered when the hotkey is released (or double-click lock is stopped)."""
        self.overlay.hide_overlay()
        self.recorder.stop_recording()

    def _on_recorder_error(self, error: str) -> None:
        print(f"App: Recorder error: {error}")

    def _on_command_executed(self, command: str) -> None:
        print(f"App: {command}")
        self.tray.notify("Command Executed", command)

    def shutdown(self) -> None:
        self.hotkeys.stop()
        self.recorder.stop_recording()


def run_app() -> int:
    app = EchoFlowApp(sys.argv)
    return app.exec()
