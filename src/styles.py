DARK = """
QMainWindow, QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QLabel#title {
    font-size: 22px;
    font-weight: 700;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    color: #cc0000;
    letter-spacing: 1px;
}

QLabel#subtitle {
    font-size: 11px;
    color: #666;
}

QGroupBox {
    border: 1px solid #333;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 10px;
    color: #888;
    font-size: 11px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    color: #888;
}

QTableWidget {
    background-color: #242424;
    border: 1px solid #333;
    border-radius: 4px;
    gridline-color: #2e2e2e;
    selection-background-color: #cc000044;
    selection-color: #fff;
}

QTableWidget::item {
    padding: 4px 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #cc000033;
    color: #fff;
}

QHeaderView::section {
    background-color: #1e1e1e;
    color: #888;
    padding: 6px 8px;
    border: none;
    border-right: 1px solid #333;
    border-bottom: 1px solid #333;
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QPushButton {
    background-color: #2a2a2a;
    color: #e0e0e0;
    border: 1px solid #444;
    border-radius: 5px;
    padding: 8px 18px;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #333;
    border-color: #cc0000;
    color: #fff;
}

QPushButton:pressed {
    background-color: #cc0000;
    color: #fff;
    border-color: #cc0000;
}

QPushButton#primary {
    background-color: #cc0000;
    color: #fff;
    border: none;
    font-weight: bold;
}

QPushButton#primary:hover {
    background-color: #e60000;
}

QPushButton#primary:pressed {
    background-color: #aa0000;
}

QPushButton#primary:disabled {
    background-color: #3a0a0a;
    color: #666;
}

QPushButton:disabled {
    background-color: #222;
    color: #444;
    border-color: #333;
}

QLineEdit {
    background-color: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 6px 10px;
    color: #e0e0e0;
}

QLineEdit:focus {
    border-color: #cc0000;
}

QProgressBar {
    background-color: #2a2a2a;
    border: 1px solid #333;
    border-radius: 4px;
    height: 6px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: #cc0000;
    border-radius: 3px;
}

QScrollBar:vertical {
    background: #1a1a1a;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #444;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #666;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QToolTip {
    background-color: #333;
    color: #e0e0e0;
    border: 1px solid #555;
    border-radius: 3px;
    padding: 4px 8px;
}
"""
