from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt


class GpuSetupDialog(QDialog):
    def __init__(self, gpu_info: dict, parent=None):
        super().__init__(parent)
        self.chosen_mode = "cpu"
        self.setWindowTitle("GPU Setup")
        self.setModal(True)
        self.setMinimumWidth(380)
        self.setStyleSheet("""
            QDialog { background: #1a1a1a; color: #dddddd; }
            QLabel  { color: #dddddd; }
        """)
        self._build_ui(gpu_info)

    def _build_ui(self, info: dict):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("GPU Setup")
        title.setStyleSheet("font-size: 15px; font-weight: 700; color: #ffffff;")
        layout.addWidget(title)

        if info["available"]:
            vram = f" ({info['vram_gb']} GB)" if info["vram_gb"] else ""
            status_text = f"GPU erkannt: {info['name']}{vram}"
            status_color = "#5cb85c"
        else:
            status_text = "Kein GPU erkannt"
            status_color = "#aaaaaa"

        status = QLabel(status_text)
        status.setStyleSheet(f"font-size: 12px; color: {status_color};")
        layout.addWidget(status)

        desc = QLabel(
            "Wähle den Modus für GPU-intensive Features\n"
            "(Stem Separation, Restoration):"
        )
        desc.setStyleSheet("font-size: 12px; color: #888888;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_style = """
            QPushButton {
                background: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                color: #cccccc;
                font-size: 12px;
                padding: 0 12px;
            }
            QPushButton:hover {
                background: #333333;
                border-color: #cc0000;
                color: #ffffff;
            }
        """
        btn_auto_style = """
            QPushButton {
                background: #3a1a1a;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                color: #ffffff;
                font-size: 12px;
                padding: 0 12px;
            }
            QPushButton:hover {
                background: #4a2020;
                border-color: #cc0000;
                color: #ffffff;
            }
        """

        btn_auto = QPushButton("Auto (empfohlen)")
        btn_gpu  = QPushButton("GPU verwenden")
        btn_cpu  = QPushButton("CPU Only")

        for btn in (btn_auto, btn_gpu, btn_cpu):
            btn.setFixedHeight(34)
            btn.setCursor(Qt.PointingHandCursor)

        btn_auto.setStyleSheet(btn_auto_style)
        btn_gpu.setStyleSheet(btn_style)
        btn_cpu.setStyleSheet(btn_style)

        btn_auto.clicked.connect(lambda: self._choose("auto"))
        btn_gpu.clicked.connect(lambda: self._choose("gpu"))
        btn_cpu.clicked.connect(lambda: self._choose("cpu"))

        btn_row.addWidget(btn_auto)
        btn_row.addWidget(btn_gpu)
        btn_row.addWidget(btn_cpu)
        layout.addLayout(btn_row)

    def _choose(self, mode: str):
        self.chosen_mode = mode
        self.accept()
