import sys

from PySide6.QtWidgets import QApplication

from app.input.hotkeys import HotkeyManager


class EchoFlowApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)

        # Initialize and start global hotkey manager
        self.hotkeys = HotkeyManager()
        self.hotkeys.start()

        # Just for testing, connect signals to standard output
        self.hotkeys.hotkey_pressed.connect(lambda: print("App: Recording started..."))
        self.hotkeys.hotkey_released.connect(lambda: print("App: Recording stopped."))

        # Cleanup on exit
        self.aboutToQuit.connect(self.shutdown)

    def shutdown(self) -> None:
        self.hotkeys.stop()


def run_app() -> int:
    app = EchoFlowApp(sys.argv)
    return app.exec()
