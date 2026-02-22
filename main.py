import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
import logging
import faulthandler
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import qInstallMessageHandler, QTimer, Qt
from PyQt6.QtGui import QGuiApplication
from app.main_window import MainWindow
from pathlib import Path
from app.core.logging_setup import setup_logging

PROJECT_ROOT = Path(__file__).resolve().parent
LOG_PATH = setup_logging(PROJECT_ROOT, level=logging.INFO)

try:
    crash_dir = PROJECT_ROOT / "logs"
    crash_dir.mkdir(parents=True, exist_ok=True)
    crash_path = crash_dir / "crash.log"
    crash_f = open(crash_path, "a", encoding="utf-8")
    faulthandler.enable(crash_f)
except Exception:
    crash_f = None

def _qt_message_handler(mode, context, message):
    try:
        msg = str(message or "")
        low = msg.lower()
        if "qwindowswindow::setgeometry" in low and "unable to set geometry" in low:
            logging.info("Qt: %s", msg)
        elif "no qtmultimedia backends found" in low:
            logging.info("Qt: %s", msg)
        else:
            logging.error("Qt: %s", msg)
    except Exception:
        pass

try:
    qInstallMessageHandler(_qt_message_handler)
except Exception:
    pass

if __name__ == "__main__":
    logging.info("Application starting...")
    try:
        app = QApplication(sys.argv)
        main_win = MainWindow()
        try:
            screen = QGuiApplication.primaryScreen()
            if screen is not None:
                geom = screen.availableGeometry()
                w = max(900, min(1500, int(geom.width() * 0.90)))
                h = max(650, min(980, int(geom.height() * 0.85)))
                x = int(geom.x() + (geom.width() - w) / 2)
                y = int(geom.y() + (geom.height() - h) / 2)
                main_win.setGeometry(x, y, w, h)
        except Exception:
            pass
        try:
            main_win.show()
        except Exception:
            pass

        def _bring_to_front():
            try:
                main_win.show()
            except Exception:
                pass
            try:
                main_win.raise_()
            except Exception:
                pass
            try:
                main_win.activateWindow()
            except Exception:
                pass
            try:
                main_win.setWindowState(main_win.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
            except Exception:
                pass
            try:
                QApplication.alert(main_win, 2000)
            except Exception:
                pass

        def _ensure_on_screen():
            try:
                screen = QGuiApplication.primaryScreen()
                if screen is None:
                    return
                geom = screen.availableGeometry()
                w = max(900, min(1600, int(geom.width() * 0.85)))
                h = max(650, min(1000, int(geom.height() * 0.85)))
                x = int(geom.x() + (geom.width() - w) / 2)
                y = int(geom.y() + (geom.height() - h) / 2)
                main_win.setGeometry(x, y, w, h)
            except Exception:
                pass

        try:
            QTimer.singleShot(80, _ensure_on_screen)
            QTimer.singleShot(250, _bring_to_front)
            QTimer.singleShot(600, _ensure_on_screen)
            QTimer.singleShot(1200, _bring_to_front)
            QTimer.singleShot(2200, _bring_to_front)
        except Exception:
            pass
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"Critical error: {e} (log: {LOG_PATH})")
        logging.critical("Critical error during application startup:", exc_info=True)
