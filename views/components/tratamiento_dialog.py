from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QTextEdit, QDateEdit, QDialog, QDialogButtonBox
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QFont

Primary = "#C9929B"
PrimaryBorder = "#E8D5D8"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"


class TratamientoDialog(QDialog):
    """Dialogo para agregar o editar un tratamiento (fecha + descripcion)."""

    def __init__(self, text="", date="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tratamiento")
        self.setMinimumWidth(450)
        self.setMinimumHeight(250)
        self.setStyleSheet(f"background-color: {White};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Agregar Tratamiento" if not text else "Editar Tratamiento")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        date_label = QLabel("Fecha")
        date_label.setFont(QFont("Segoe UI", 11))
        date_label.setStyleSheet(f"color: {Txt2}; background: transparent;")
        layout.addWidget(date_label)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFont(QFont("Segoe UI", 11))
        self.date_edit.setStyleSheet(f"""
            QDateEdit {{
                background-color: {pale_pink};
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                color: {Txt1};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border: none;
            }}
        """)
        if date:
            self.date_edit.setDate(QDate.fromString(date, "yyyy-MM-dd"))
        else:
            self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        text_label = QLabel("Tratamiento (diagnóstico y procedimiento)")
        text_label.setFont(QFont("Segoe UI", 11))
        text_label.setStyleSheet(f"color: {Txt2}; background: transparent;")
        layout.addWidget(text_label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Describa el diagnóstico y tratamiento realizado...")
        self.text_edit.setPlainText(text)
        self.text_edit.setFont(QFont("Segoe UI", 11))
        self.text_edit.setMinimumHeight(100)
        self.text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {pale_pink};
                border: none;
                border-radius: 8px;
                padding: 10px 12px;
                color: {Txt1};
            }}
        """)
        layout.addWidget(self.text_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        for btn in buttons.buttons():
            btn.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
            btn.setFixedHeight(32)
            if btn == buttons.button(QDialogButtonBox.Save):
                btn.setStyleSheet(f"""
                    QPushButton {{ background-color: {Second}; color: white; border: none; border-radius: 8px; padding: 0 20px; }}
                    QPushButton:hover {{ background-color: #C0607A; }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{ background-color: transparent; color: {Txt2}; border: 1px solid {PrimaryBorder}; border-radius: 8px; padding: 0 20px; }}
                    QPushButton:hover {{ background-color: {pale_pink}; }}
                """)
        layout.addWidget(buttons)

    def get_data(self):
        return self.text_edit.toPlainText().strip(), self.date_edit.date().toString("yyyy-MM-dd")
