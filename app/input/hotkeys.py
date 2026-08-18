import logging

from pynput import keyboard
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class HotkeyManager(QObject):
    # Signals to be emitted when the hotkey is pressed or released
    hotkey_pressed = Signal()
    hotkey_released = Signal()

    def __init__(self) -> None:
        super().__init__()
        # Define the hotkey combination. Default: Ctrl + Space
        # We parse it into a set of keys that need to be active.
        self.hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+<space>"), self._on_activate)

        self.listener: keyboard.Listener | None = None
        self._is_active = False

    def start(self) -> None:
        if self.listener is not None:
            return

        logger.info("Starting global hotkey listener...")
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.listener.start()

    def stop(self) -> None:
        if self.listener is not None:
            logger.info("Stopping global hotkey listener...")
            self.listener.stop()
            self.listener = None

    def _on_activate(self) -> None:
        pass  # Not used directly because we track state manually for release

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if key is None:
            return

        # Update the HotKey instance state
        self.hotkey.press(self.listener.canonical(key))  # type: ignore

        # Check if the full combination is active
        # The internal _state of HotKey is a set of currently pressed keys from the combination
        is_combo_active = len(self.hotkey._state) == len(self.hotkey._keys)

        if is_combo_active and not self._is_active:
            self._is_active = True
            logger.info("Hotkey pressed")
            self.hotkey_pressed.emit()

    def _on_release(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if key is None:
            return

        if self._is_active:
            # If the combo was active, and any key in the combo is released, it's no longer active
            canonical_key = self.listener.canonical(key)  # type: ignore
            if canonical_key in self.hotkey._keys:
                self._is_active = False
                logger.info("Hotkey released")
                self.hotkey_released.emit()

        self.hotkey.release(self.listener.canonical(key))  # type: ignore
