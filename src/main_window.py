import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QFileDialog,
    QProgressBar, QHeaderView, QAbstractItemView, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QDropEvent, QDragEnterEvent, QColor, QPixmap

from src.analyzer import analyze_file
from src.renamer import build_filename, rename_file
from src.styles import DARK

SUPPORTED = {'.wav', '.mp3', '.flac', '.aiff', '.aif', '.ogg'}

COL_ORIG    = 0
COL_KEY     = 1
COL_BPM     = 2
COL_TAG     = 3
COL_PREVIEW = 4


class AnalyzeWorker(QThread):
    progress = pyqtSignal(int, str, float, str)  # row, key, bpm, filename
    error    = pyqtSignal(int, str)
    finished = pyqtSignal()

    def __init__(self, rows: list):
        super().__init__()
        self.rows = rows

    def run(self):
        for row, path in self.rows:
            try:
                result = analyze_file(path)
                self.progress.emit(row, result['key'], result['bpm'], os.path.basename(path))
            except Exception as e:
                self.error.emit(row, str(e))
        self.finished.emit()


class StatusBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(6)

        # Row: label left, percentage right
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("Ready.")
        self.label.setStyleSheet("color: #666; font-size: 11px;")
        self.pct_label = QLabel("")
        self.pct_label.setStyleSheet("color: #cc0000; font-size: 11px; font-weight: bold;")
        self.pct_label.setAlignment(Qt.AlignRight)
        row.addWidget(self.label)
        row.addWidget(self.pct_label)

        self.bar = QProgressBar()
        self.bar.setFixedHeight(8)
        self.bar.setTextVisible(False)
        self.bar.setVisible(False)
        self.bar.setStyleSheet("""
            QProgressBar {
                background: #2a2a2a;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #cc0000, stop:1 #e60000);
                border-radius: 4px;
            }
        """)

        layout.addLayout(row)
        layout.addWidget(self.bar)

    def set_text(self, text: str, color: str = "#666"):
        self.label.setText(text)
        self.label.setStyleSheet(f"color: {color}; font-size: 11px;")
        self.pct_label.setText("")

    def start(self, total: int, text: str = ""):
        self._total = total
        self.bar.setMaximum(total)
        self.bar.setValue(0)
        self.bar.setVisible(True)
        self.pct_label.setText("0%")
        if text:
            self.label.setText(text)
            self.label.setStyleSheet("color: #aaa; font-size: 11px;")

    def update(self, value: int, text: str = ""):
        self.bar.setValue(value)
        total = getattr(self, '_total', 1) or 1
        pct = int(value / total * 100)
        self.pct_label.setText(f"{pct}%")
        if text:
            self.label.setText(text)
            self.label.setStyleSheet("color: #aaa; font-size: 11px;")

    def pulse(self):
        self.bar.setMaximum(0)
        self.bar.setVisible(True)

    def done(self, text: str, color: str = "#5cb85c"):
        self.bar.setVisible(False)
        self.set_text(text, color)

    def error(self, text: str):
        self.bar.setVisible(False)
        self.set_text(text, "#ff4444")


class DropZone(QLabel):
    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self._set_idle()
        self.setCursor(Qt.PointingHandCursor)

    def _set_idle(self):
        self.setText("Drop Stem Folder or Files here   ·   or click to browse")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #383838;
                border-radius: 8px;
                color: #4a4a4a;
                font-size: 13px;
                padding: 28px;
                background: #1c1c1c;
            }
            QLabel:hover {
                border-color: #cc0000;
                color: #777;
                background: #202020;
            }
        """)

    def _set_hover(self):
        self.setText("Release to load files")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #cc0000;
                border-radius: 8px;
                color: #cc0000;
                font-size: 13px;
                padding: 28px;
                background: #1e0808;
            }
        """)

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            self._set_hover()

    def dragLeaveEvent(self, e):
        self._set_idle()

    def dropEvent(self, e: QDropEvent):
        self._set_idle()
        paths = [u.toLocalFile() for u in e.mimeData().urls()]
        self.files_dropped.emit(self._resolve(paths))

    def mousePressEvent(self, e):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Stem Files", "",
            "Audio Files (*.wav *.mp3 *.flac *.aiff *.aif *.ogg)"
        )
        if paths:
            self.files_dropped.emit(paths)

    def _resolve(self, paths: list) -> list:
        files = []
        for p in paths:
            if os.path.isdir(p):
                for f in sorted(os.listdir(p)):
                    if os.path.splitext(f)[1].lower() in SUPPORTED:
                        files.append(os.path.join(p, f))
            elif os.path.splitext(p)[1].lower() in SUPPORTED:
                files.append(p)
        return files


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BZS Stem Tool")
        self.setMinimumSize(960, 620)
        self.setStyleSheet(DARK)
        self._file_paths: dict = {}
        self._worker = None
        self._analyzed = 0
        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 18, 20, 16)

        # ── Header ──────────────────────────────────────────────────────
        header = QHBoxLayout()

        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'logomascott.png')
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pix = QPixmap(logo_path).scaledToHeight(48, Qt.SmoothTransformation)
            logo_label.setPixmap(pix)
            logo_label.setFixedSize(pix.width(), 48)
            header.addWidget(logo_label)
            header.addSpacing(10)

        title = QLabel("BZS STEM TOOL")
        title.setObjectName("title")
        sub = QLabel("Key · BPM · Metadata Renamer")
        sub.setObjectName("subtitle")
        sub.setAlignment(Qt.AlignBottom)
        header.addWidget(title)
        header.addSpacing(10)
        header.addWidget(sub)
        header.addStretch()

        tag_box = QHBoxLayout()
        tag_box.setSpacing(6)
        lbl = QLabel("Producer Tag:")
        lbl.setStyleSheet("color: #888;")
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("e.g. BZS")
        self.tag_input.setFixedWidth(180)
        self.tag_input.textChanged.connect(self._update_all_previews)
        tag_box.addWidget(lbl)
        tag_box.addWidget(self.tag_input)
        header.addLayout(tag_box)
        layout.addLayout(header)

        # ── Drop zone ───────────────────────────────────────────────────
        self.drop_zone = DropZone()
        self.drop_zone.setFixedHeight(78)
        self.drop_zone.files_dropped.connect(self._load_files)
        layout.addWidget(self.drop_zone)

        # ── Table ───────────────────────────────────────────────────────
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Original File", "Key", "BPM", "Tag", "New Name Preview"])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Stretch)
        hh.setSectionResizeMode(1, QHeaderView.Fixed)
        hh.setSectionResizeMode(2, QHeaderView.Fixed)
        hh.setSectionResizeMode(3, QHeaderView.Fixed)
        hh.setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.setColumnWidth(1, 88)
        self.table.setColumnWidth(2, 88)
        self.table.setColumnWidth(3, 140)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            "QTableWidget { alternate-background-color: #1f1f1f; }"
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.itemChanged.connect(self._on_cell_changed)
        layout.addWidget(self.table)

        # ── Status bar ──────────────────────────────────────────────────
        self.status = StatusBar()
        layout.addWidget(self.status)

        # ── Buttons ─────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.btn_folder = QPushButton("Browse Folder")
        self.btn_folder.clicked.connect(self._browse_folder)

        self.btn_analyze = QPushButton("Analyze All  (Key + BPM)")
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.clicked.connect(self._analyze_all)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self._clear)
        self.btn_clear.setEnabled(False)

        self.btn_rename = QPushButton("Rename All Files")
        self.btn_rename.setObjectName("primary")
        self.btn_rename.setEnabled(False)
        self.btn_rename.clicked.connect(self._rename_all)

        btn_row.addWidget(self.btn_folder)
        btn_row.addWidget(self.btn_analyze)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_clear)
        btn_row.addWidget(self.btn_rename)
        layout.addLayout(btn_row)

    # ── File loading ────────────────────────────────────────────────────
    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Stem Folder")
        if folder:
            files = [
                os.path.join(folder, f) for f in sorted(os.listdir(folder))
                if os.path.splitext(f)[1].lower() in SUPPORTED
            ]
            self._load_files(files)

    def _load_files(self, paths: list):
        if not paths:
            self.status.error("No supported audio files found.")
            return

        self.status.start(len(paths), f"Loading {len(paths)} file(s)...")
        self.table.setRowCount(0)
        self._file_paths.clear()

        self.table.blockSignals(True)
        for row, path in enumerate(paths):
            self.table.insertRow(row)
            self._file_paths[row] = path

            stem, ext = os.path.splitext(os.path.basename(path))

            orig = QTableWidgetItem(os.path.basename(path))
            orig.setFlags(orig.flags() & ~Qt.ItemIsEditable)
            orig.setToolTip(path)

            key_item  = QTableWidgetItem("—")
            key_item.setTextAlignment(Qt.AlignCenter)
            bpm_item  = QTableWidgetItem("—")
            bpm_item.setTextAlignment(Qt.AlignCenter)
            tag_item  = QTableWidgetItem(self.tag_input.text())
            tag_item.setTextAlignment(Qt.AlignCenter)

            prev_item = QTableWidgetItem("")
            prev_item.setFlags(prev_item.flags() & ~Qt.ItemIsEditable)
            prev_item.setForeground(QColor("#cc0000"))

            self.table.setItem(row, COL_ORIG,    orig)
            self.table.setItem(row, COL_KEY,     key_item)
            self.table.setItem(row, COL_BPM,     bpm_item)
            self.table.setItem(row, COL_TAG,     tag_item)
            self.table.setItem(row, COL_PREVIEW, prev_item)

            self.status.update(row + 1, f"Loading {row + 1} / {len(paths)}")

        self.table.blockSignals(False)
        self._update_all_previews()

        n = self.table.rowCount()
        self.status.done(f"{n} file(s) loaded.  Click 'Analyze All' to detect Key + BPM.", "#aaa")
        self.btn_analyze.setEnabled(True)
        self.btn_rename.setEnabled(True)
        self.btn_clear.setEnabled(True)

    # ── Preview logic ───────────────────────────────────────────────────
    def _update_preview(self, row: int):
        path = self._file_paths.get(row)
        if path is None:
            return
        _, ext = os.path.splitext(path)
        stem_name = os.path.splitext(os.path.basename(path))[0]

        key    = self.table.item(row, COL_KEY).text()
        bpm_t  = self.table.item(row, COL_BPM).text()
        tag    = self.table.item(row, COL_TAG).text()

        key = "" if key == "—" else key
        try:
            bpm = float(bpm_t)
        except ValueError:
            bpm = 0

        new_name = build_filename(stem_name, key, bpm, tag, ext)
        self.table.item(row, COL_PREVIEW).setText(new_name)

    def _update_all_previews(self):
        self.table.blockSignals(True)
        global_tag = self.tag_input.text()
        for row in range(self.table.rowCount()):
            tag_cell = self.table.item(row, COL_TAG)
            if tag_cell is not None:
                tag_cell.setText(global_tag)
            self._update_preview(row)
        self.table.blockSignals(False)

    def _on_cell_changed(self, item: QTableWidgetItem):
        if item.column() in (COL_KEY, COL_BPM, COL_TAG):
            self._update_preview(item.row())

    # ── Analysis ────────────────────────────────────────────────────────
    def _analyze_all(self):
        rows = [(r, self._file_paths[r]) for r in range(self.table.rowCount())]
        if not rows:
            return

        self._analyzed = 0
        self._set_busy(True)
        self.status.start(len(rows), f"Analyzing 0 / {len(rows)} ...")

        self._worker = AnalyzeWorker(rows)
        self._worker.progress.connect(self._on_result)
        self._worker.error.connect(self._on_error)
        self._worker.finished.connect(self._on_done)
        self._worker.start()

    def _on_result(self, row: int, key: str, bpm: float, fname: str):
        self.table.blockSignals(True)
        bpm_str = str(int(bpm)) if bpm == int(bpm) else str(bpm)
        self.table.item(row, COL_KEY).setText(key)
        self.table.item(row, COL_BPM).setText(bpm_str)
        self.table.blockSignals(False)
        self._update_preview(row)

        self._analyzed += 1
        total = self.table.rowCount()
        short = fname if len(fname) <= 40 else fname[:37] + "..."
        self.status.update(self._analyzed, f"Analyzed: {short}  ({self._analyzed}/{total})")

    def _on_error(self, row: int, msg: str):
        item = self.table.item(row, COL_KEY)
        if item:
            item.setText("ERR")
            item.setForeground(QColor("#ff4444"))
            item.setToolTip(msg)
        self._analyzed += 1
        self.status.update(self._analyzed)

    def _on_done(self):
        self._set_busy(False)
        n = self.table.rowCount()
        self.status.done(f"Analysis complete — {n} file(s) ready to rename.")

    # ── Rename ──────────────────────────────────────────────────────────
    def _rename_all(self):
        n = self.table.rowCount()
        if n == 0:
            return

        reply = QMessageBox.question(
            self, "Rename Files",
            f"Rename {n} file(s) on disk?\nThis cannot be easily undone.",
            QMessageBox.Yes | QMessageBox.Cancel
        )
        if reply != QMessageBox.Yes:
            return

        self.status.start(n, "Renaming...")
        errors = []
        renamed = 0

        for row in range(n):
            old_path = self._file_paths.get(row)
            new_name = self.table.item(row, COL_PREVIEW).text()
            if not old_path or not new_name:
                continue
            try:
                new_path = rename_file(old_path, new_name)
                self._file_paths[row] = new_path
                self.table.item(row, COL_ORIG).setText(os.path.basename(new_path))
                renamed += 1
            except Exception as e:
                errors.append(f"{os.path.basename(old_path)}: {e}")
            self.status.update(row + 1, f"Renaming {row + 1} / {n} ...")

        if errors:
            self.status.error(f"{renamed} renamed, {len(errors)} failed.")
            QMessageBox.warning(self, "Some files failed", "\n".join(errors))
        else:
            self.status.done(f"Done — {renamed} file(s) renamed.")

    # ── Helpers ─────────────────────────────────────────────────────────
    def _clear(self):
        self.table.setRowCount(0)
        self._file_paths.clear()
        self.btn_analyze.setEnabled(False)
        self.btn_rename.setEnabled(False)
        self.btn_clear.setEnabled(False)
        self.status.set_text("Ready.", "#555")

    def _set_busy(self, busy: bool):
        self.btn_analyze.setEnabled(not busy)
        self.btn_rename.setEnabled(not busy)
        self.btn_folder.setEnabled(not busy)
        self.drop_zone.setEnabled(not busy)
        if busy:
            self.btn_analyze.setText("Analyzing...")
        else:
            self.btn_analyze.setText("Analyze All  (Key + BPM)")
