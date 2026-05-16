import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QLoggingCategory
from src.main_window import MainWindow
from src import settings
from src import gpu as gpu_module
from src.gpu_setup_dialog import GpuSetupDialog


def main():
    os.environ.setdefault("QT_LOGGING_RULES", "qt.qpa.fonts=false")
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("BZS Stem Tool")

    s = settings.load()
    gpu_info = gpu_module.detect_gpu()

    if not s.get("gpu_setup_done"):
        dlg = GpuSetupDialog(gpu_info)
        if dlg.exec_() == GpuSetupDialog.Accepted:
            s["gpu_mode"] = dlg.chosen_mode
            s["gpu_setup_done"] = True
            settings.save(s)
        # Rejected: leave gpu_setup_done=False → dialog shows again next launch

    gpu_available = (
        s.get("gpu_mode") != "cpu"
        and gpu_info["available"]
    )

    window = MainWindow(gpu_available=gpu_available)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
