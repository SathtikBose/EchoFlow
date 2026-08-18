import sys

from PySide6.QtWidgets import QApplication

from app.audio.recorder import AudioRecorder
from app.input.hotkeys import HotkeyManager


class EchoFlowApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        # Initialize services
        self.hotkeys = HotkeyManager()
        self.recorder = AudioRecorder()

        # Wire up hotkeys to audio recording
        self.hotkeys.hotkey_pressed.connect(self.recorder.start_recording)
        self.hotkeys.hotkey_released.connect(self.recorder.stop_recording)

        # Handle audio ready
        self.recorder.audio_ready.connect(self._on_audio_ready)

        # Start hotkey listener
        self.hotkeys.start()

        # Cleanup on exit
        self.aboutToQuit.connect(self.shutdown)

    def _on_audio_ready(self, audio_data: bytes) -> None:
        # Placeholder for Phase 4: send to Speech-to-Text
        print(f"App: Received {len(audio_data)} bytes of audio data.")

    def shutdown(self) -> None:
        self.hotkeys.stop()
        self.recorder.stop_recording()


def run_app() -> int:
    app = EchoFlowApp(sys.argv)
    return app.exec()
