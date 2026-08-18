import logging
import time

from pynput.keyboard import Controller, Key
from PySide6.QtGui import QGuiApplication

logger = logging.getLogger(__name__)


class TextInserter:
    def __init__(self) -> None:
        self.keyboard = Controller()

    def insert_text(self, text: str) -> None:
        if not text:
            return

        clipboard = QGuiApplication.clipboard()
        if clipboard is None:
            logger.error("Failed to access system clipboard.")
            return

        # 1. Save current clipboard content
        original_text = clipboard.text()

        try:
            # 2. Set new text to clipboard (retry if another app holds it)
            for attempt in range(5):
                try:
                    clipboard.setText(text)
                    break
                except Exception as clip_err:
                    if attempt == 4:
                        raise clip_err
                    time.sleep(0.05)

            # Wait a tiny bit for the OS to register clipboard change
            time.sleep(0.05)

            # 3. Simulate Ctrl+V to paste
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press("v")
                self.keyboard.release("v")

            logger.info(f"Inserted text: {text[:20]}...")

            # Wait a tiny bit for the paste operation to complete
            time.sleep(0.1)
        except Exception as e:
            logger.error(f"Failed to insert text: {e}")
        finally:
            # 4. Restore original clipboard content
            clipboard.setText(original_text)
