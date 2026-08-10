import os
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QIcon

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")

Primary = "#C9929B"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
White = "#FFFFFF"
Divider = "#E8E2DC"
Danger = "#DC2626"
DangerBg = "#FEF2F2"


class PatientCard(QFrame):
    clicked = Signal(int)
    delete_clicked = Signal(int)
    edit_clicked = Signal(int)

    def __init__(self, patient, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.patient = patient
        self.navigate_callback = navigate_callback
        self.patient_id = patient.id
        self._hovered_btn = None
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
                border-left: 4px solid {Primary};
                border-radius: 16px;
            }}
            QFrame:hover {{
                background-color: #FFF5F7;
                border: 1px solid {Second};
                border-left: 4px solid {Second};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 18, 16, 18)
        layout.setSpacing(0)

        info = QVBoxLayout()
        info.setSpacing(5)

        name = QLabel(f"{patient.name} {patient.lastName}")
        name.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        name.setStyleSheet(f"color: {Txt1}; background: transparent; border: none;")
        info.addWidget(name)

        meta = QLabel(f"{patient.age} años  ·  {patient.entryDate}")
        meta.setFont(QFont("Segoe UI", 10))
        meta.setStyleSheet(f"color: {Txt2}; background: transparent; border: none;")
        info.addWidget(meta)

        motive = patient.consultReason if patient.consultReason else ""
        if motive:
            motive_lbl = QLabel(motive)
            motive_lbl.setFont(QFont("Segoe UI", 10))
            motive_lbl.setStyleSheet(f"color: {Txt2}; background: transparent; border: none;")
            motive_lbl.setWordWrap(True)
            info.addWidget(motive_lbl)

        layout.addLayout(info, 1)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(6)
        right_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.setAlignment(Qt.AlignRight)

        self._edit_btn = QPushButton()
        self._edit_btn.setFixedSize(32, 32)
        self._edit_btn.setCursor(Qt.PointingHandCursor)
        self._edit_btn.setToolTip("Editar")
        self._edit_btn.setIcon(QIcon(os.path.join(ASSETS_DIR, "edit.svg")))
        self._edit_btn.setIconSize(QSize(16, 16))
        self._edit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1.5px solid #B8C5D6;
                border-radius: 16px;
            }}
        """)
        btn_row.addWidget(self._edit_btn)

        self._edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.patient_id))

        self._delete_btn = QPushButton()
        self._delete_btn.setFixedSize(32, 32)
        self._delete_btn.setCursor(Qt.PointingHandCursor)
        self._delete_btn.setToolTip("Eliminar")
        self._delete_btn.setIcon(QIcon(os.path.join(ASSETS_DIR, "delete.svg")))
        self._delete_btn.setIconSize(QSize(16, 16))
        self._delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: 1.5px solid #E89A9A;
                border-radius: 16px;
            }}
        """)
        btn_row.addWidget(self._delete_btn)

        self._delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.patient_id))

        right_layout.addLayout(btn_row)
        layout.addLayout(right_layout)

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self._delete_btn or obj == self._edit_btn:
            return False

        if obj == self and event.type() == event.Type.MouseMove:
            child = self.childAt(event.pos())
            hovered = None
            while child:
                if child == self._delete_btn:
                    hovered = self._delete_btn
                    break
                if child == self._edit_btn:
                    hovered = self._edit_btn
                    break
                child = child.parentWidget()
            if hovered != self._hovered_btn:
                self._hovered_btn = hovered
                self._update_btn_styles()

        if obj == self and event.type() == event.Type.MouseButtonRelease:
            if self.navigate_callback:
                self.navigate_callback("detail", self.patient_id)
            self.clicked.emit(self.patient_id)
            return True

        return super().eventFilter(obj, event)

    def _update_btn_styles(self):
        if self._hovered_btn == self._delete_btn:
            self._delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #FEE2E2;
                    border: 1.5px solid #E89A9A;
                    border-radius: 16px;
                }}
            """)
        else:
            self._delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: 1.5px solid #E89A9A;
                    border-radius: 16px;
                }}
            """)

        if self._hovered_btn == self._edit_btn:
            self._edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #E8F0FE;
                    border: 1.5px solid #93B4E8;
                    border-radius: 16px;
                }}
            """)
        else:
            self._edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: 1.5px solid #B8C5D6;
                    border-radius: 16px;
                }}
            """)
