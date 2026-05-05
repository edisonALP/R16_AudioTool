import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QLoggingCategory
from src.main_window import MainWindow


def main():
    os.environ.setdefault("QT_LOGGING_RULES", "qt.qpa.fonts=false")
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("BZS Stem Tool")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
