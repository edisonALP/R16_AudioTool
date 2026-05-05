from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame,
)
from PyQt5.QtCore import pyqtSignal

from src import settings as sett

PRESET_TAGS = [
    "analog", "don", "wavy", "ambient", "melodic", "drill", "trap",
    "afro", "synth", "dark", "cinematic", "bounce", "grimey", "plugg",
    "emo", "rage", "jersey", "uk drill", "phonk",
]

MAX_PRODUCERS = 3


class NamingSection(QWidget):
    naming_changed = pyqtSignal(list, list)  # style_tags, producers

    def __init__(self, parent=None):
        super().__init__(parent)
        self._expanded = False
        self._active_tags: list[str] = []
        self._custom_tags: list[str] = []
        self._producer_inputs: list[QLineEdit] = []
        self._build_ui()
        self._load()

    # ── Public accessors ────────────────────────────────────────────────

    def style_tags(self) -> list[str]:
        return list(self._active_tags)

    def producers(self) -> list[str]:
        return [inp.text().strip() for inp in self._producer_inputs
                if inp.text().strip()]

    # ── Build UI ────────────────────────────────────────────────────────

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._toggle_btn = QPushButton("▶  Naming")
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
            "QFrame { background: #1a1a1a; border: 1px solid #333;"
            " border-radius: 6px; }"
        )
        body_layout = QVBoxLayout(self._body)
        body_layout.setContentsMargins(10, 8, 10, 10)
        body_layout.setSpacing(8)

        # ── Style Tags ───────────────────────────────────────────────
        tags_lbl = QLabel("Style / Vibe Tags:")
        tags_lbl.setStyleSheet("color: #888; font-size: 12px;")
        body_layout.addWidget(tags_lbl)

        self._chips_widget = QWidget()
        self._chips_layout = QHBoxLayout(self._chips_widget)
        self._chips_layout.setContentsMargins(0, 0, 0, 0)
        self._chips_layout.setSpacing(4)
        self._chips_layout.addStretch()
        body_layout.addWidget(self._chips_widget)

        add_row = QHBoxLayout()
        add_row.setSpacing(6)
        self._tag_input = QLineEdit()
        self._tag_input.setPlaceholderText("+ eigener Tag  (Enter)")
        self._tag_input.setFixedWidth(200)
        self._tag_input.setStyleSheet(
            "QLineEdit { background: #2a2a2a; color: #ccc; border: 1px solid #444;"
            " border-radius: 4px; padding: 2px 8px; font-size: 12px; }"
        )
        self._tag_input.returnPressed.connect(self._add_custom_tag)
        add_row.addWidget(self._tag_input)
        add_row.addStretch()
        body_layout.addLayout(add_row)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("QFrame { border-color: #2a2a2a; }")
        body_layout.addWidget(div)

        # ── Producer Tags ────────────────────────────────────────────
        prod_lbl = QLabel("Producer Tags:")
        prod_lbl.setStyleSheet("color: #888; font-size: 12px;")
        body_layout.addWidget(prod_lbl)

        self._prod_widget = QWidget()
        self._prod_inner = QHBoxLayout(self._prod_widget)
        self._prod_inner.setContentsMargins(0, 0, 0, 0)
        self._prod_inner.setSpacing(6)

        self._add_prod_btn = QPushButton("+")
        self._add_prod_btn.setFixedSize(26, 26)
        self._add_prod_btn.setStyleSheet(
            "QPushButton { background: #2a2a2a; color: #888; border: 1px solid #444;"
            " border-radius: 4px; font-size: 14px; }"
            "QPushButton:hover { background: #3a3a3a; color: #fff; }"
        )
        self._add_prod_btn.clicked.connect(self._add_producer_field)

        self._add_producer_input()  # first input always present
        self._rebuild_producers()
        body_layout.addWidget(self._prod_widget)

        outer.addWidget(self._body)
        self._rebuild_chips()

    # ── Style tag logic ─────────────────────────────────────────────────

    def _rebuild_chips(self):
        while self._chips_layout.count() > 1:
            item = self._chips_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        all_tags = list(PRESET_TAGS)
        for ct in self._custom_tags:
            if ct not in all_tags:
                all_tags.append(ct)

        for tag in all_tags:
            chip = self._make_chip(tag, active=tag in self._active_tags,
                                   is_custom=tag in self._custom_tags)
            self._chips_layout.insertWidget(self._chips_layout.count() - 1, chip)

    def _make_chip(self, tag: str, active: bool, is_custom: bool) -> QPushButton:
        label = f"● {tag}  ×" if is_custom else tag
        btn = QPushButton(label)
        btn.setFixedHeight(24)
        btn.setStyleSheet(
            "QPushButton { background: #2a2a2a; color: #666; border: 1px solid #383838;"
            " border-radius: 4px; padding: 0 8px; font-size: 11px; }"
            "QPushButton:checked { background: #3a0808; color: #cc0000;"
            " border-color: #cc0000; }"
            "QPushButton:hover { color: #aaa; }"
        )
        if is_custom:
            btn.setCheckable(False)
            btn.clicked.connect(lambda _, t=tag: self._remove_custom_tag(t))
        else:
            btn.setCheckable(True)
            btn.setChecked(active)
            btn.toggled.connect(lambda checked, t=tag: self._on_chip_toggled(t, checked))
        return btn

    def _on_chip_toggled(self, tag: str, checked: bool):
        if checked and tag not in self._active_tags:
            self._active_tags.append(tag)
        elif not checked and tag in self._active_tags:
            self._active_tags.remove(tag)
        self._emit()

    def _remove_custom_tag(self, tag: str):
        if tag in self._custom_tags:
            self._custom_tags.remove(tag)
        if tag in self._active_tags:
            self._active_tags.remove(tag)
        self._rebuild_chips()
        self._emit()

    def _add_custom_tag(self):
        tag = self._tag_input.text().strip().lower()
        if not tag or tag in PRESET_TAGS or tag in self._custom_tags:
            self._tag_input.clear()
            return
        self._custom_tags.append(tag)
        self._active_tags.append(tag)
        self._tag_input.clear()
        self._rebuild_chips()
        self._emit()

    # ── Producer logic ───────────────────────────────────────────────────

    def _add_producer_input(self):
        placeholders = ["beatsexuell", "R16Studios", "producer3"]
        idx = len(self._producer_inputs)
        ph = placeholders[idx] if idx < len(placeholders) else "producer"
        inp = QLineEdit()
        inp.setPlaceholderText(ph)
        inp.setFixedWidth(140)
        inp.setStyleSheet(
            "QLineEdit { background: #2a2a2a; color: #ccc; border: 1px solid #444;"
            " border-radius: 4px; padding: 2px 8px; font-size: 12px; }"
        )
        inp.textChanged.connect(self._emit)
        self._producer_inputs.append(inp)

    def _add_producer_field(self):
        if len(self._producer_inputs) >= MAX_PRODUCERS:
            return
        self._add_producer_input()
        self._rebuild_producers()
        self._emit()

    def _rebuild_producers(self):
        while self._prod_inner.count():
            item = self._prod_inner.takeAt(0)
            w = item.widget()
            if w is not None and w not in self._producer_inputs \
                    and w is not self._add_prod_btn:
                w.deleteLater()

        for inp in self._producer_inputs:
            at = QLabel("@")
            at.setStyleSheet("color: #888; font-size: 12px;")
            at.setFixedWidth(14)
            self._prod_inner.addWidget(at)
            self._prod_inner.addWidget(inp)

        self._prod_inner.addWidget(self._add_prod_btn)
        self._prod_inner.addStretch()
        self._add_prod_btn.setVisible(len(self._producer_inputs) < MAX_PRODUCERS)

    # ── Toggle ───────────────────────────────────────────────────────────

    def _toggle(self):
        self._expanded = not self._expanded
        self._body.setVisible(self._expanded)
        self._update_toggle_label()

    def _update_toggle_label(self):
        arrow = "▼" if self._expanded else "▶"
        parts = []
        if self._active_tags:
            parts.append("[" + ", ".join(self._active_tags) + "]")
        prods = self.producers()
        if prods:
            parts.append("_".join(f"@{p}" for p in prods))
        suffix = "  ·  " + "  ·  ".join(parts) if parts else ""
        self._toggle_btn.setText(f"{arrow}  Naming{suffix}")

    # ── Persistence ──────────────────────────────────────────────────────

    def _load(self):
        data = sett.load()
        self._custom_tags = data.get("custom_tags", [])
        self._active_tags = data.get("style_tags", [])
        saved_producers = data.get("producers", ["beatsexuell"])

        if saved_producers and self._producer_inputs:
            self._producer_inputs[0].setText(saved_producers[0])
        for p in saved_producers[1:]:
            self._add_producer_input()
            self._producer_inputs[-1].setText(p)

        self._rebuild_chips()
        self._rebuild_producers()
        self._update_toggle_label()

    def _autosave(self):
        data = sett.load()
        data["style_tags"] = self._active_tags
        data["custom_tags"] = self._custom_tags
        data["producers"] = self.producers()
        sett.save(data)

    def _emit(self):
        self._update_toggle_label()
        self._autosave()
        self.naming_changed.emit(self.style_tags(), self.producers())
