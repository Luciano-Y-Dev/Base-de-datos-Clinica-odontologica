from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QCheckBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from services.patient_service import get_patients_ordered
from services.export_service import generate_patients_pdf

Primary = "#C9929B"
PrimaryBorder = "#E8D5D8"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"


class ExportView(QWidget):
    def __init__(self, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.setStyleSheet(f"background-color: {pale_pink};")
        self._checkboxes: list[QCheckBox] = []
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet(f"QFrame {{ background-color: {White}; border-bottom: 2px solid {PrimaryBorder}; }}")
        header_lo = QHBoxLayout(header)
        header_lo.setContentsMargins(24, 0, 24, 0)

        back_btn = QPushButton("\u2190 Volver")
        back_btn.setFixedHeight(38)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setFont(QFont("Segoe UI", 11))
        back_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {Txt2}; border: none; }}
            QPushButton:hover {{ color: {Txt1}; }}
        """)
        if self.navigate_callback:
            back_btn.clicked.connect(lambda: self.navigate_callback("principal"))
        header_lo.addWidget(back_btn)

        header_lo.addSpacing(24)

        title = QLabel("Exportar Datos")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        header_lo.addWidget(title)
        header_lo.addStretch()

        root.addWidget(header)
        root.addSpacing(16)

        patients = get_patients_ordered()

        if patients:
            actions = QHBoxLayout()
            actions.setSpacing(8)

            select_all_btn = QPushButton("Seleccionar todos")
            select_all_btn.setCursor(Qt.PointingHandCursor)
            select_all_btn.setFixedHeight(36)
            select_all_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
            select_all_btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {Second};
                    border: 1px solid {Second};
                    border-radius: 8px;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: #FFF5F7;
                }}
            """)
            select_all_btn.clicked.connect(self._toggle_all)
            actions.addWidget(select_all_btn)

            actions.addStretch()

            self.export_btn = QPushButton("Exportar PDF (0)")
            self.export_btn.setCursor(Qt.PointingHandCursor)
            self.export_btn.setFixedHeight(36)
            self.export_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
            self.export_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Second};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0 20px;
                }}
                QPushButton:hover {{ background-color: #C0607A; }}
                QPushButton:pressed {{ background-color: #A84860; }}
            """)
            self.export_btn.clicked.connect(self._export)
            actions.addWidget(self.export_btn)

            root.addLayout(actions)
            root.addSpacing(12)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.NoFrame)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setStyleSheet("""
                QScrollArea { border: none; background: transparent; }
                QScrollBar:vertical { background: transparent; width: 6px; }
                QScrollBar::handle:vertical { background: #D1D5DB; border-radius: 3px; min-height: 24px; }
                QScrollBar::handle:vertical:hover { background: #9CA3AF; }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
            """)

            cards = QWidget()
            cards.setStyleSheet("background: transparent;")
            cards_layout = QVBoxLayout(cards)
            cards_layout.setContentsMargins(0, 0, 8, 0)
            cards_layout.setSpacing(8)

            for p in patients:
                card = QFrame()
                card.setStyleSheet(f"""
                    QFrame {{
                        background-color: {White};
                        border: none;
                        border-left: 4px solid {Primary};
                        border-radius: 14px;
                    }}
                """)
                card_lo = QHBoxLayout(card)
                card_lo.setContentsMargins(16, 14, 16, 14)
                card_lo.setSpacing(12)

                cb = QCheckBox()
                cb.setStyleSheet(f"""
                    QCheckBox::indicator {{
                        width: 18px; height: 18px;
                        border: 2px solid {PrimaryBorder};
                        border-radius: 4px;
                        background: {White};
                    }}
                    QCheckBox::indicator:checked {{
                        background-color: {Second};
                        border-color: {Second};
                    }}
                """)
                cb.stateChanged.connect(self._update_count)
                self._checkboxes.append((cb, p.id))
                card_lo.addWidget(cb)

                info = QVBoxLayout()
                info.setSpacing(2)

                name_lbl = QLabel(f"{p.name} {p.lastName}")
                name_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
                name_lbl.setStyleSheet(f"color: {Txt1}; background: transparent;")
                info.addWidget(name_lbl)

                meta_lbl = QLabel(f"{p.age} anos  ·  CI: {p.CI}  ·  {p.entryDate}")
                meta_lbl.setFont(QFont("Segoe UI", 9))
                meta_lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")
                info.addWidget(meta_lbl)

                card_lo.addLayout(info, 1)
                cards_layout.addWidget(card)

            cards_layout.addStretch()
            scroll.setWidget(cards)
            root.addWidget(scroll, 1)
        else:
            empty = QWidget()
            empty.setStyleSheet("background: transparent;")
            empty_lo = QVBoxLayout(empty)
            empty_lo.setAlignment(Qt.AlignCenter)
            empty_lo.setSpacing(8)

            empty_text = QLabel("No hay pacientes registrados")
            empty_text.setFont(QFont("Segoe UI", 14, QFont.Weight.DemiBold))
            empty_text.setAlignment(Qt.AlignCenter)
            empty_text.setStyleSheet(f"color: {Txt1}; background: transparent;")
            empty_lo.addWidget(empty_text)

            root.addWidget(empty, 1)

    def _toggle_all(self):
        all_checked = all(cb.isChecked() for cb, _ in self._checkboxes)
        for cb, _ in self._checkboxes:
            cb.setChecked(not all_checked)

    def _update_count(self):
        count = sum(1 for cb, _ in self._checkboxes if cb.isChecked())
        self.export_btn.setText(f"Exportar PDF ({count})")

    def _export(self):
        selected = [pid for cb, pid in self._checkboxes if cb.isChecked()]
        if not selected:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Sin seleccion")
            msg.setText("Selecciona al menos un paciente para exportar.")
            msg.exec()
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar PDF", "reporte_pacientes.pdf", "PDF (*.pdf)"
        )
        if not path:
            return

        try:
            generate_patients_pdf(selected, path)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Exportado")
            msg.setText(f"PDF exportado correctamente.\n{path}")
            msg.exec()
        except Exception as ex:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
            msg.setText(f"Error al exportar: {ex}")
            msg.exec()
