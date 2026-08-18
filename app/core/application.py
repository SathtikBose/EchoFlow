import sys

from PySide6.QtWidgets import QApplication


class EchoFlowApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)


def run_app() -> int:
    app = EchoFlowApp(sys.argv)
    return app.exec()
