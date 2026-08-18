import logging
import sys

from app.core.application import EchoFlowApp
from app.core.logger import setup_logging
from app.ui.tray import TrayManager


def main() -> int:
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info("Starting EchoFlow")

    app = EchoFlowApp(sys.argv)

    # Keep a reference to the tray manager so it doesn't get garbage collected
    tray_manager = TrayManager(app)

    # Prevent tray_manager from being unused warning
    _ = tray_manager

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
