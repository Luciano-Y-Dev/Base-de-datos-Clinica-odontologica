import os
import platformdirs
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QFont, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

_APP_NAME = "clinica_odontologica"
_FLAG_FILE = "first_run_done"

Primary = "#C9929B"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"


def _load_svg(path, height, dpr=1.0):
    renderer = QSvgRenderer(path)
    size = renderer.defaultSize()
    width = int(size.width() * height / size.height())
    pixmap = QPixmap(int(width * dpr), int(height * dpr))
    pixmap.setDevicePixelRatio(dpr)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter, QRectF(0, 0, width, height))
    painter.end()
    return pixmap


def is_first_run() -> bool:
    data_dir = platformdirs.user_data_dir(_APP_NAME, appauthor=False)
    flag_path = os.path.join(data_dir, _FLAG_FILE)
    return not os.path.exists(flag_path)


def mark_first_run_done():
    data_dir = platformdirs.user_data_dir(_APP_NAME, appauthor=False)
    os.makedirs(data_dir, exist_ok=True)
    flag_path = os.path.join(data_dir, _FLAG_FILE)
    with open(flag_path, "w") as f:
        f.write("done")


class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bienvenido")
        self.setFixedSize(520, 500)
        self.setStyleSheet(f"background-color: {pale_pink};")
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 30)
        layout.setSpacing(0)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border-radius: 20px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 36, 32, 28)
        card_layout.setSpacing(0)

        logo_label = QLabel()
        logo_label.setStyleSheet("background: transparent;")
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "Logo.svg")
        logo_label.setPixmap(_load_svg(logo_path, 120, self.devicePixelRatioF()))
        logo_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(logo_label)

        card_layout.addSpacing(28)

        title = QLabel("Bienvenida Dra. Raquel")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        card_layout.addWidget(title)

        card_layout.addSpacing(12)

        desc = QLabel("Es un gusto tenerla aquí.")
        desc.setFont(QFont("Segoe UI", 11))
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet(f"color: {Txt2}; background: transparent;")
        desc.setWordWrap(True)
        card_layout.addWidget(desc)

        card_layout.addSpacing(32)

        btn = QPushButton("Comenzar")
        btn.setFixedHeight(44)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Second};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0 32px;
            }}
            QPushButton:hover {{
                background-color: #C0607A;
            }}
            QPushButton:pressed {{
                background-color: #A84860;
            }}
        """)
        btn.clicked.connect(self._on_start)
        card_layout.addWidget(btn, alignment=Qt.AlignCenter)

        layout.addWidget(card)

    def _on_start(self):
        mark_first_run_done()
        self.accept()
