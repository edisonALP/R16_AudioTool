from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QFrame,
)
from PyQt5.QtCore import pyqtSignal

from src.presets import PRESETS, AVAILABLE_TOKENS


class _TokenChip(QPushButton):
    removed = pyqtSignal(int)

    def __init__(self, label: str, index: int, removable: bool = False):
        super().__init__(label if not removable else f"{label}  ×")
        self._index = index
        self.setCheckable(False)
        self.setFixedHeight(26)
        self.setStyleSheet(
            "QPushButton {"
            "  background: #2a2a2a; color: #ccc; border: 1px solid #444;"
            "  border-radius: 4px; padding: 0 10px; font-size: 12px;"
            "}"
            "QPushButton:hover { background: #3a3a3a; color: #fff; }"
        )
        if removable:
            self.clicked.connect(lambda: self.removed.emit(self._index))


class NamingPatternBar(QWidget):
    pattern_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._expanded = False
        self._active: list[tuple[str, str, str]] = []  # (token_id, suffix, label)
        self._building = False
        self._build_ui()
        self._load_preset("Classic")

    def current_pattern(self) -> list[tuple[str, str]]:
        return [(tid, sfx) for tid, sfx, _ in self._active]

    def update_preview(self, sample: str):
        self._preview_lbl.setText(sample)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._toggle_btn = QPushButton("▶  Naming Pattern: Classic")
        self._toggle_btn.setFlat(True)
        self._toggle_btn.setStyleSheet(
            "QPushButton { text-align: left; color: #888; font-size: 12px;"
            " background: transparent; border: none; padding: 4px 0; }"
            "QPushButton:hover { color: #ccc; }"
        )
        self._toggle_btn.clicked.connect(self._toggle)
        outer.addWidget(self._toggle_btn)

        self._body = QFrame()
        self._body.setVisible(False)
        self._body.setStyleSheet(
            "QFrame { background: #1a1a1a; border: 1px solid #333; border-radius: 6px; }"
        )
        body_layout = QVBoxLayout(self._body)
        body_layout.setContentsMargins(10, 8, 10, 8)
        body_layout.setSpacing(6)

        # Row 1: preset dropdown + available tokens
        row1 = QHBoxLayout()
        self._preset_combo = QComboBox()
        self._preset_combo.addItems(list(PRESETS.keys()))
        self._preset_combo.setCurrentText("Classic")
        self._preset_combo.setFixedWidth(120)
        self._preset_combo.setStyleSheet(
            "QComboBox { background: #2a2a2a; color: #ccc; border: 1px solid #444;"
            " border-radius: 4px; padding: 2px 6px; }"
            "QComboBox::drop-down { border: none; }"
            "QComboBox QAbstractItemView { background: #2a2a2a; color: #ccc; }"
        )
        self._preset_combo.currentTextChanged.connect(self._on_preset_changed)
        row1.addWidget(self._preset_combo)
        row1.addSpacing(12)
        avail_lbl = QLabel("Available:")
        avail_lbl.setStyleSheet("color: #888; font-size: 12px;")
        row1.addWidget(avail_lbl)
        for tid, sfx, label in AVAILABLE_TOKENS:
            btn = _TokenChip(label, -1, removable=False)
            btn.clicked.connect(lambda _, t=tid, s=sfx, l=label: self._add_token(t, s, l))
            row1.addWidget(btn)
        row1.addStretch()
        body_layout.addLayout(row1)

        # Row 2: active sequence
        row2 = QHBoxLayout()
        active_lbl = QLabel("Active:")
        active_lbl.setFixedWidth(56)
        active_lbl.setStyleSheet("color: #888; font-size: 12px;")
        row2.addWidget(active_lbl)
        self._active_container = QWidget()
        self._active_inner = QHBoxLayout(self._active_container)
        self._active_inner.setContentsMargins(0, 0, 0, 0)
        self._active_inner.setSpacing(4)
        row2.addWidget(self._active_container)
        row2.addStretch()
        body_layout.addLayout(row2)

        # Row 3: preview
        row3 = QHBoxLayout()
        prev_lbl = QLabel("Preview:")
        prev_lbl.setFixedWidth(56)
        prev_lbl.setStyleSheet("color: #888; font-size: 12px;")
        self._preview_lbl = QLabel("—")
        self._preview_lbl.setStyleSheet("color: #cc0000; font-size: 12px;")
        row3.addWidget(prev_lbl)
        row3.addWidget(self._preview_lbl)
        row3.addStretch()
        body_layout.addLayout(row3)

        outer.addWidget(self._body)

    def _toggle(self):
        self._expanded = not self._expanded
        self._body.setVisible(self._expanded)
        self._update_toggle_label()

    def _on_preset_changed(self, name: str):
        if self._building:
            return
        if name != "Custom":
            self._load_preset(name)

    def _load_preset(self, name: str):
        self._active = [
            (tid, sfx, self._label_for(tid, sfx))
            for tid, sfx in PRESETS[name]
        ]
        self._refresh_active_chips()
        self._update_toggle_label()
        if not self._building:
            self.pattern_changed.emit()

    def _add_token(self, tid: str, sfx: str, label: str):
        self._active.append((tid, sfx, label))
        self._building = True
        self._preset_combo.setCurrentText("Custom")
        self._building = False
        self._refresh_active_chips()
        self._update_toggle_label()
        self.pattern_changed.emit()

    def _remove_token(self, index: int):
        if 0 <= index < len(self._active):
            self._active.pop(index)
        self._building = True
        self._preset_combo.setCurrentText("Custom")
        self._building = False
        self._refresh_active_chips()
        self._update_toggle_label()
        self.pattern_changed.emit()

    def _refresh_active_chips(self):
        while self._active_inner.count():
            item = self._active_inner.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for i, (tid, sfx, label) in enumerate(self._active):
            chip = _TokenChip(label, i, removable=True)
            chip.removed.connect(self._remove_token)
            self._active_inner.addWidget(chip)

    def _update_toggle_label(self):
        arrow = "▼" if self._expanded else "▶"
        preset = self._preset_combo.currentText()
        self._toggle_btn.setText(f"{arrow}  Naming Pattern: {preset}")

    @staticmethod
    def _label_for(tid: str, sfx: str) -> str:
        for t, s, label in AVAILABLE_TOKENS:
            if t == tid and s == sfx:
                return label
        return tid
