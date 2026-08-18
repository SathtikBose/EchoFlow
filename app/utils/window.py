import win32gui


def get_active_window_title() -> str:
    """
    Returns the title of the currently active foreground window on Windows.
    Returns an empty string if it cannot be determined.
    """
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            return str(title)
    except Exception:
        pass

    return ""
