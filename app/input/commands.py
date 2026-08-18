import logging
import re

from pynput.keyboard import Controller, Key

logger = logging.getLogger(__name__)


class CommandProcessor:
    def __init__(self) -> None:
        self.keyboard = Controller()

        # Simple regex-based command matching
        self.commands = {
            re.compile(r"^\s*press enter\s*$", re.IGNORECASE): self._cmd_enter,
            re.compile(r"^\s*press tab\s*$", re.IGNORECASE): self._cmd_tab,
            re.compile(r"^\s*undo(?: that)?\s*$", re.IGNORECASE): self._cmd_undo,
            re.compile(r"^\s*delete line\s*$", re.IGNORECASE): self._cmd_delete_line,
        }

    def process(self, text: str) -> bool:
        """
        Processes text to see if it matches a voice command.
        Returns True if a command was executed, False otherwise.
        """
        # Clean text
        clean_text = text.lower().strip()
        # Remove trailing punctuation often added by ASR
        clean_text = re.sub(r"[.!?]$", "", clean_text).strip()

        for pattern, handler in self.commands.items():
            if pattern.match(clean_text):
                logger.info(f"Voice command recognized: '{clean_text}'")
                try:
                    handler()
                    return True
                except Exception as e:
                    logger.error(f"Error executing command '{clean_text}': {e}")
                    return False

        return False

    def _cmd_enter(self) -> None:
        self.keyboard.tap(Key.enter)

    def _cmd_tab(self) -> None:
        self.keyboard.tap(Key.tab)

    def _cmd_undo(self) -> None:
        # Ctrl+Z
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.tap("z")

    def _cmd_delete_line(self) -> None:
        # End, Shift+Home, Backspace
        self.keyboard.tap(Key.end)
        with self.keyboard.pressed(Key.shift):
            self.keyboard.tap(Key.home)
        self.keyboard.tap(Key.backspace)
