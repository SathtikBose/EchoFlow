from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon


class TrayManager(QObject):
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app

        self.tray_icon = QSystemTrayIcon(self)

        # We need an icon. For now, we'll create a basic temporary icon or skip it.
        # Without an icon, the tray icon might not appear on Windows.
        # We will set a temporary text-based icon or leave it empty for now,
        # but PySide6 requires a valid icon to show in the tray.
        # Let's use a standard icon available in PySide6 as a placeholder.
        self.tray_icon.setIcon(
            self.app.style().standardIcon(self.app.style().StandardPixmap.SP_ComputerIcon)
        )

        self.tray_menu = QMenu()

        self.start_action = QAction("Start EchoFlow")
        self.settings_action = QAction("Settings")
        self.history_action = QAction("History")
        self.quit_action = QAction("Quit")

        self.quit_action.triggered.connect(self.quit_app)

        self.tray_menu.addAction(self.start_action)
        self.tray_menu.addAction(self.settings_action)
        self.tray_menu.addAction(self.history_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.setToolTip("EchoFlow: Idle")
        self.tray_icon.show()

        # Connect to app signals for UI updates
        # Check if the app has these properties (for type checker and runtime safety)
        if hasattr(self.app, "hotkeys"):
            self.app.hotkeys.hotkey_pressed.connect(self._on_recording_start)
            self.app.hotkeys.hotkey_released.connect(self._on_recording_stop)

        if hasattr(self.app, "transcriber"):
            self.app.transcriber.transcription_complete.connect(self._on_transcription_complete)
            self.app.transcriber.transcription_error.connect(self._on_transcription_error)

    def _on_recording_start(self) -> None:
        self.tray_icon.setToolTip("EchoFlow: ● Listening...")

    def _on_recording_stop(self) -> None:
        self.tray_icon.setToolTip("EchoFlow: ◌ Transcribing...")

    def _on_transcription_complete(self, text: str) -> None:
        self.tray_icon.setToolTip("EchoFlow: ✓ Idle")

    def _on_transcription_error(self, error: str) -> None:
        self.tray_icon.setToolTip("EchoFlow: ✗ Error")

    def quit_app(self) -> None:
        self.app.quit()
