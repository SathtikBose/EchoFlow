from unittest.mock import patch

from app.utils.window import get_active_window_title


def test_get_active_window_title_success() -> None:
    with patch("win32gui.GetForegroundWindow", return_value=12345):
        with patch("win32gui.GetWindowText", return_value="Visual Studio Code"):
            assert get_active_window_title() == "Visual Studio Code"


def test_get_active_window_title_failure() -> None:
    with patch("win32gui.GetForegroundWindow", return_value=0):
        assert get_active_window_title() == ""


def test_get_active_window_title_exception() -> None:
    with patch("win32gui.GetForegroundWindow", side_effect=Exception("API error")):
        assert get_active_window_title() == ""
