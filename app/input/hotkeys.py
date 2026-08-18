import logging
import threading
import time

from pynput import keyboard
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class HotkeyManager(QObject):
    # Signals to be emitted when the hotkey is pressed or released
    hotkey_pressed = Signal()
    hotkey_released = Signal()
    # Emitted when the user successfully double-clicks to lock
    hotkey_locked = Signal()

    def __init__(self) -> None:
        super().__init__()
        from app.core.config import settings

        # Parse hotkey string from settings (e.g. "ctrl+alt+space" -> "<ctrl>+<alt>+<space>")
        raw_keys = settings.echoflow_hotkey.split("+")
        formatted_keys = []
        for k in raw_keys:
            k = k.strip().lower()
            if len(k) > 1 and not k.startswith("<"):
                formatted_keys.append(f"<{k}>")
            else:
                formatted_keys.append(k)
        
        parsed_hotkey_str = "+".join(formatted_keys)
        logger.info(f"Configured hotkey: {parsed_hotkey_str}")

        self.hotkey = keyboard.HotKey(keyboard.HotKey.parse(parsed_hotkey_str), self._on_activate)

        self.listener: keyboard.Listener | None = None
        self._is_active = False
        self._is_locked = False
        self._press_time: float = 0.0
        
        self._stop_timer: threading.Timer | None = None

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
        pass  # Handled manually

    def _trigger_release(self) -> None:
        """Called by the timer if a second click doesn't arrive in time."""
        if self._is_active and not self._is_locked:
            self._is_active = False
            logger.info("Hotkey released (single tap/hold)")
            self.hotkey_released.emit()

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if key is None or not self.listener:
            return

        self.hotkey.press(self.listener.canonical(key))  # type: ignore
        is_combo_active = len(self.hotkey._state) == len(self.hotkey._keys)

        if is_combo_active:
            if self._is_locked:
                # If we were locked, ANY full press sequence un-locks and stops it
                logger.info("Unlocked recording")
                self._is_locked = False
                self._is_active = False
                self.hotkey_released.emit()
                return

            if self._stop_timer and self._stop_timer.is_alive():
                # We pressed the combo AGAIN before the release timer fired! Double click!
                self._stop_timer.cancel()
                self._stop_timer = None
                self._is_locked = True
                logger.info("Hotkey double clicked! Recording locked.")
                self.hotkey_locked.emit()
                return

            if not self._is_active:
                # First normal press
                self._is_active = True
                self._press_time = time.time()
                logger.info("Hotkey pressed")
                self.hotkey_pressed.emit()

    def _on_release(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if key is None or not self.listener:
            return

        if self._is_active:
            canonical_key = self.listener.canonical(key)  # type: ignore
            if canonical_key in self.hotkey._keys:
                # The user released one of the combo keys
                if self._is_locked:
                    # Ignore releases if we are locked
                    pass
                else:
                    press_duration = time.time() - self._press_time
                    if press_duration < 0.35:
                        # Short tap. Might be the first half of a double click!
                        # Give them 350ms to press again before we stop recording.
                        self._stop_timer = threading.Timer(0.35, self._trigger_release)
                        self._stop_timer.start()
                    else:
                        # Long hold. Stop immediately.
                        self._is_active = False
                        logger.info("Hotkey released (long hold)")
                        self.hotkey_released.emit()

        self.hotkey.release(self.listener.canonical(key))  # type: ignore
