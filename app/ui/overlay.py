import logging

from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PySide6.QtGui import QColor, QPainter, QBrush, QPen
from PySide6.QtWidgets import QWidget, QApplication

logger = logging.getLogger(__name__)


class RecordingOverlay(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Make it a frameless, transparent, always-on-top tooltip-like window
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(100, 100)
        self.is_locked = False

        # Animation logic for the pulsating circle
        self.pulse_radius = 20.0
        self.pulse_growing = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pulse)
        self.timer.start(30)

    def show_overlay(self, locked: bool = False) -> None:
        """Position the overlay on the active screen and show it."""
        self.is_locked = locked
        
        screen = QApplication.primaryScreen()
        cursor_pos = QApplication.primaryScreen().cursor().pos()
        # Find which screen the cursor is currently on
        for s in QApplication.screens():
            if s.geometry().contains(cursor_pos):
                screen = s
                break

        # Position it at the bottom center of the active screen
        screen_geo = screen.geometry()
        x = screen_geo.x() + (screen_geo.width() - self.width()) // 2
        y = screen_geo.y() + screen_geo.height() - self.height() - 50  # 50px from bottom

        self.move(x, y)
        self.show()

    def hide_overlay(self) -> None:
        self.hide()
        self.is_locked = False

    def set_locked(self, locked: bool) -> None:
        self.is_locked = locked
        self.update()

    def update_pulse(self) -> None:
        if not self.isVisible():
            return

        # Simple pulsating animation logic
        speed = 1.0 if not self.is_locked else 1.5
        if self.pulse_growing:
            self.pulse_radius += speed
            if self.pulse_radius >= 40:
                self.pulse_growing = False
        else:
            self.pulse_radius -= speed
            if self.pulse_radius <= 20:
                self.pulse_growing = True

        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() / 2
        center_y = self.height() / 2

        # Color: Red for normal recording, Blue/Green for locked? 
        # Let's use a nice glowing red for recording, and a glowing cyan for locked.
        base_color = QColor(0, 200, 255) if self.is_locked else QColor(255, 50, 50)
        
        # Draw the outer pulse
        pulse_color = QColor(base_color)
        pulse_color.setAlpha(80)
        painter.setBrush(QBrush(pulse_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - self.pulse_radius, center_y - self.pulse_radius, 
                            self.pulse_radius * 2, self.pulse_radius * 2)

        # Draw the inner solid circle
        painter.setBrush(QBrush(base_color))
        painter.drawEllipse(center_x - 15, center_y - 15, 30, 30)

        painter.end()
