import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging() -> None:
    """Configures application-wide logging to console and rotating file."""
    # Determine log directory (App Data)
    app_data = os.getenv("APPDATA")
    if app_data:
        log_dir = Path(app_data) / "EchoFlow" / "logs"
    else:
        # Fallback to local directory if APPDATA is somehow not set
        log_dir = Path("logs")

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "echoflow.log"

    # Set up root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # File Handler (10 MB max size, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    logger.info(f"Logging initialized. Log file: {log_file}")


def get_log_dir() -> Path:
    """Returns the configured log directory."""
    app_data = os.getenv("APPDATA")
    if app_data:
        return Path(app_data) / "EchoFlow" / "logs"
    return Path("logs")
