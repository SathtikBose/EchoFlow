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
            "--hidden-import=app.llm.nvidia",
            "--hidden-import=app.services.transcription_service",
            "--hidden-import=app.ui.tray",
            "--hidden-import=app.input.insertion",
            "--hidden-import=app.input.commands",
            "--hidden-import=app.input.dictionary",
            "--hidden-import=app.input.snippets",
            "--hidden-import=app.utils.window",
            "--hidden-import=app.core.logger",
            "--hidden-import=app.db.history",
            "--hidden-import=pynput.keyboard._win32",
            "--hidden-import=pynput.mouse._win32",
            "--hidden-import=sqlmodel",
            "--hidden-import=sqlalchemy",
            "--log-level=INFO",
        ]
    )


if __name__ == "__main__":
    build()
