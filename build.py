from pathlib import Path

import PyInstaller.__main__


def build() -> None:
    PyInstaller.__main__.run(
        [
            "app/main.py",
            "--name=EchoFlow",
            "--windowed",  # No console window
            "--noconfirm",
            "--clean",
            "--hidden-import=app.audio.recorder",
            "--hidden-import=app.input.hotkeys",
            "--hidden-import=app.speech.nvidia",
            "--hidden-import=app.services.transcription_service",
            "--hidden-import=app.ui.tray",
            "--hidden-import=app.input.insertion",
            "--hidden-import=pynput.keyboard._win32",
            "--hidden-import=pynput.mouse._win32",
            "--log-level=INFO",
        ]
    )


if __name__ == "__main__":
    build()
