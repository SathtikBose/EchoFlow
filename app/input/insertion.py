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
            clipboard_success = False
            for attempt in range(5):
                try:
                    clipboard.setText(text)
                    clipboard_success = True
                    break
                except Exception as clip_err:
                    time.sleep(0.05)

            if clipboard_success:
                # Wait a tiny bit for the OS to register clipboard change
                time.sleep(0.05)

                # 3. Simulate Ctrl+V to paste
                with self.keyboard.pressed(Key.ctrl):
                    self.keyboard.press("v")
                    self.keyboard.release("v")

                logger.info(f"Inserted text via clipboard: {text[:20]}...")
                time.sleep(0.1)
            else:
                # Fallback to direct typing if clipboard is permanently locked
                logger.warning("Clipboard locked. Falling back to direct typing.")
                self.keyboard.type(text)
                logger.info(f"Inserted text via typing: {text[:20]}...")

        except Exception as e:
            logger.error(f"Failed to insert text: {e}")
            # Ultimate fallback
            self.keyboard.type(text)
        finally:
            # 4. Restore original clipboard content
            try:
                clipboard.setText(original_text)
            except Exception:
                pass
