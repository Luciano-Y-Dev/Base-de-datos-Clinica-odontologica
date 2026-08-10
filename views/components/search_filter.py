from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QDateEdit
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont

Primary = "#C9929B"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"


class SearchFilter(QWidget):
    filter_changed = Signal(str, object, object)

    def __init__(self, show_dates=True, parent=None):
        super().__init__(parent)
        self._show_dates = show_dates
        self._build_ui()

    def _build_ui(self):
        self._frame = QFrame()
        self._frame.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border-radius: 12px;
                padding: 8px;
            }}
        """)
        layout = QVBoxLayout(self._frame)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(6)

        row1 = QHBoxLayout()
        row1.setSpacing(8)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Buscar por nombre, apellido o CI...")
        self._search_input.setFixedHeight(34)
        self._search_input.setFont(QFont("Segoe UI", 10))
        self._search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {pale_pink};
                border: 1px solid #E8E2DC;
                border-radius: 8px;
                padding: 0 12px;
                color: {Txt1};
            }}
            QLineEdit:focus {{
                border: 1px solid {Primary};
            }}
            QLineEdit::placeholder {{
                color: {Txt2};
            }}
        """)
        self._search_input.textChanged.connect(self._emit_filter)
        row1.addWidget(self._search_input)

        if self._show_dates:
            self._dates_btn = QPushButton("Fechas")
            self._dates_btn.setFixedHeight(34)
            self._dates_btn.setCursor(Qt.PointingHandCursor)
            self._dates_btn.setFont(QFont("Segoe UI", 9))
            self._dates_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {Txt2};
                    border: 1px solid #E8E2DC;
                    border-radius: 8px;
                    padding: 0 10px;
                }}
                QPushButton:hover {{
                    color: {Primary};
                    border-color: {Primary};
                }}
            """)
            self._dates_btn.clicked.connect(self._toggle_dates)
            row1.addWidget(self._dates_btn)

        layout.addLayout(row1)

        if self._show_dates:
            self._dates_row = QWidget()
            dates_layout = QHBoxLayout(self._dates_row)
            dates_layout.setContentsMargins(0, 0, 0, 0)
            dates_layout.setSpacing(8)

            date_from_label = QLabel("Desde:")
            date_from_label.setFont(QFont("Segoe UI", 9))
            date_from_label.setStyleSheet(f"color: {Txt2}; background: transparent;")
            dates_layout.addWidget(date_from_label)

            self._date_from = QDateEdit()
            self._date_from.setFixedHeight(30)
            self._date_from.setFont(QFont("Segoe UI", 9))
            self._date_from.setCalendarPopup(True)
            self._date_from.setDate(QDate(2020, 1, 1))
            self._date_from.setStyleSheet(f"""
                QDateEdit {{
                    background-color: {pale_pink};
                    border: 1px solid #E8E2DC;
                    border-radius: 6px;
                    min-width: 120px;
                    padding: 0 8px;
                    color: {Txt1};
                }}
                QDateEdit:focus {{
                    border: 1px solid {Primary};
                }}
                QDateEdit::drop-down {{
                    border: none;
                    width: 20px;
                }}
            """)
            self._date_from.dateChanged.connect(self._emit_filter)
            dates_layout.addWidget(self._date_from)

            date_to_label = QLabel("Hasta:")
            date_to_label.setFont(QFont("Segoe UI", 9))
            date_to_label.setStyleSheet(f"color: {Txt2}; background: transparent;")
            dates_layout.addWidget(date_to_label)

            self._date_to = QDateEdit()
            self._date_to.setFixedHeight(30)
            self._date_to.setFont(QFont("Segoe UI", 9))
            self._date_to.setCalendarPopup(True)
            self._date_to.setDate(QDate.currentDate())
            self._date_to.setStyleSheet(f"""
                QDateEdit {{
                    background-color: {pale_pink};
                    border: 1px solid #E8E2DC;
                    border-radius: 6px;
                    min-width: 120px;
                    padding: 0 8px;
                    color: {Txt1};
                }}
                QDateEdit:focus {{
                    border: 1px solid {Primary};
                }}
                QDateEdit::drop-down {{
                    border: none;
                    width: 20px;
                }}
            """)
            self._date_to.dateChanged.connect(self._emit_filter)
            dates_layout.addWidget(self._date_to)

            dates_layout.addStretch()
            layout.addWidget(self._dates_row)
            self._dates_row.hide()

        self._results_label = QLabel()
        self._results_label.setFont(QFont("Segoe UI", 9))
        self._results_label.setStyleSheet(f"color: {Txt2}; background: transparent;")
        layout.addWidget(self._results_label)
        self._results_label.hide()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._frame)

    def _emit_filter(self):
        if self._show_dates:
            self.filter_changed.emit(
                self._search_input.text().strip(),
                self._date_from.date().toPython(),
                self._date_to.date().toPython(),
            )
        else:
            self.filter_changed.emit(
                self._search_input.text().strip(),
                None,
                None,
            )

    def _toggle_dates(self):
        visible = not self._dates_row.isVisible()
        self._dates_row.setVisible(visible)
        self._dates_btn.setText("Ocultar fechas" if visible else "Fechas")
        if not visible:
            self._date_from.setDate(QDate(2020, 1, 1))
            self._date_to.setDate(QDate.currentDate())
            self._emit_filter()

    def update_results_label(self, count, total):
        if count == total:
            self._results_label.hide()
        else:
            self._results_label.setText(f"Mostrando {count} de {total} pacientes")
            self._results_label.show()

    def reset(self):
        self._search_input.clear()
        if self._show_dates:
            self._dates_row.hide()
            self._dates_btn.setText("Fechas")
            self._date_from.setDate(QDate(2020, 1, 1))
            self._date_to.setDate(QDate.currentDate())

    def show_frame(self):
        self._frame.show()

    def hide_frame(self):
        self._frame.hide()
        self.reset()

    def is_frame_visible(self):
        return self._frame.isVisible()
