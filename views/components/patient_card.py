from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from database.utils import readREMAINING

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
    edit_clicked = Signal(int)
    delete_clicked = Signal(int)

    def __init__(self, patient, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.patient = patient
        self.navigate_callback = navigate_callback
        self.patient_id = patient[0]
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: 1px solid {Divider};
                border-left: 4px solid {Primary};
                border-radius: 16px;
            }}
            QFrame:hover {{
                background-color: #FFF5F7;
                border-color: {Second};
                border-left-color: {Second};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 18, 16, 18)
        layout.setSpacing(0)

        info = QVBoxLayout()
        info.setSpacing(5)

        name = QLabel(f"{patient[1]} {patient[2]}")
        name.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        name.setStyleSheet(f"color: {Txt1}; background: transparent; border: none;")
        info.addWidget(name)

        meta = QLabel(f"{patient[3]} años  ·  {patient[5]}")
        meta.setFont(QFont("Segoe UI", 10))
        meta.setStyleSheet(f"color: {Txt2}; background: transparent; border: none;")
        info.addWidget(meta)

        motive = patient[10] if patient[10] else ""
        if motive:
            motive_lbl = QLabel(motive)
            motive_lbl.setFont(QFont("Segoe UI", 10))
            motive_lbl.setStyleSheet(f"color: {Txt2}; background: transparent; border: none;")
            motive_lbl.setWordWrap(True)
            info.addWidget(motive_lbl)

        layout.addLayout(info, 1)

        remaining = readREMAINING(self.patient_id)
        remaining = remaining if remaining is not None else 0.0

        right_layout = QVBoxLayout()
        right_layout.setSpacing(6)
        right_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        amt = QLabel(f"${remaining:.2f}")
        amt.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        amt.setStyleSheet(f"color: {Txt1}; background: transparent; border: none;")
        amt.setAlignment(Qt.AlignRight)
        right_layout.addWidget(amt)

        amt_desc = QLabel("Falta por abonar")
        amt_desc.setFont(QFont("Segoe UI", 9))
        amt_desc.setStyleSheet(f"color: {Txt2}; background: transparent; border: none;")
        amt_desc.setAlignment(Qt.AlignRight)
        right_layout.addWidget(amt_desc)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        btn_row.setAlignment(Qt.AlignRight)

        edit_btn = QPushButton("Editar")
        edit_btn.setFixedSize(60, 26)
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.setFont(QFont("Segoe UI", 9))
        edit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Second};
                border: none;
                padding: 0 8px;
            }}
            QPushButton:hover {{
                background-color: #FFF5F7;
            }}
        """)
        edit_btn.clicked.connect(lambda: self.edit_clicked.emit(self.patient_id))
        btn_row.addWidget(edit_btn)

        delete_btn = QPushButton("Borrar")
        delete_btn.setFixedSize(60, 26)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setFont(QFont("Segoe UI", 9))
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Danger};
                border: none;
                padding: 0 8px;
            }}
            QPushButton:hover {{
                background-color: {DangerBg};
            }}
        """)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.patient_id))
        btn_row.addWidget(delete_btn)

        right_layout.addLayout(btn_row)
        layout.addLayout(right_layout)

    def mousePressEvent(self, event):
        if self.navigate_callback:
            self.navigate_callback("detail", self.patient_id)
        self.clicked.emit(self.patient_id)
        super().mousePressEvent(event)
