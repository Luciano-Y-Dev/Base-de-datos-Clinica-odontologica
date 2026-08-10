from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QLineEdit, QTextEdit, QCheckBox,
    QGridLayout, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from services.patient_service import save_patient
from views.components.odontogram import OdontogramWidget

Primary = "#C9929B"
PrimaryBorder = "#E8D5D8"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
almost_rose = "#FFFBFB"
White = "#FFFFFF"
Fieldalmost_rose = "#FFFBFB"

ANTECEDENT_FIELDS = [
    ("Oídos / Nariz / Garganta", "earNoseThroat"),
    ("Respiratorio", "respiratory"),
    ("Alergias", "allergy"),
    ("Cardiovascular", "cardiovascular"),
    ("Gastrointestinal", "gastrointestinal"),
    ("Endocrino", "endocrine"),
    ("Renal", "renal"),
    ("Hepático", "hepatic"),
    ("Neurológico", "neurologic"),
    ("Neoplásico", "neoplastic"),
    ("Enfermedades de sangre", "blood"),
    ("Viral", "viral"),
    ("Ginecológico", "gynecologic"),
    ("Covid", "covid"),
    ("VIH", "hiv"),
    ("Cirugías", "surgeries"),
    ("Medicamentos", "medications"),
    ("Vacuna Hepatitis", "hepatitisVaccine"),
    ("Vacuna Covid", "covidVaccine"),
    ("Historial Familiar", "familyHistory"),
]


def _make_field(placeholder="", text="", multiline=False):
    if multiline:
        field = QTextEdit()
        field.setPlaceholderText(placeholder)
        field.setPlainText(text)
        field.setFixedHeight(70)
        field.setFont(QFont("Segoe UI", 11))
        field.setStyleSheet(f"""
            QTextEdit {{
                background-color: {almost_rose};
                border: none;
                border-radius: 10px;
                padding: 10px 12px;
                color: {Txt1};
            }}
            QTextEdit:focus {{
                border: none;
            }}
        """)
        return field
    else:
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setText(text)
        field.setFont(QFont("Segoe UI", 11))
        field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {almost_rose};
                border: none;
                border-radius: 10px;
                padding: 10px 12px;
                color: {Txt1};
            }}
            QLineEdit:focus {{
                border: none;
            }}
            QLineEdit::placeholder {{
                color: #B0B0B0;
            }}
        """)
        return field


class FormPatient(QWidget):
    saved = Signal()

    def __init__(self, data=None, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.is_edit = data is not None and data.get("paciente") is not None
        self.patient_id = data["paciente"].id if self.is_edit else None
        self.paciente = data["paciente"] if data else None
        self.antecedentes = data["antecedentes"] if data else None
        self.examen = data["examen"] if data else None
        self.odontograma_details = data.get("odontograma_details", []) if data else []
        self.last_abono = data.get("last_abono") if data else None
        self.setStyleSheet(f"background-color: {pale_pink};")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = self._build_header()
        root.addWidget(header)

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

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 32)
        content_layout.setSpacing(20)

        content_layout.addLayout(self._build_personal_section())
        content_layout.addLayout(self._build_antecedentes_section())
        content_layout.addLayout(self._build_examen_section())
        content_layout.addLayout(self._build_odontogram_section())
        content_layout.addLayout(self._build_pricing_section())

        content_layout.addStretch()
        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def _build_header(self):
        header = QFrame()
        header.setFixedHeight(64)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
            }}
        """)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 0, 24, 0)

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
        layout.addWidget(back_btn)

        layout.addSpacing(24)

        title = QLabel("Editar Ficha" if self.is_edit else "Nuevo Registro de Paciente")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        layout.addStretch()

        save_btn = QPushButton("Guardar")
        save_btn.setFixedHeight(38)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Second};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: #C0607A;
            }}
            QPushButton:pressed {{
                background-color: #A84860;
            }}
        """)
        save_btn.clicked.connect(self._save)
        layout.addWidget(save_btn)

        return header

    def _build_personal_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Información Personal")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        card = self._make_card()

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.nameF = _make_field("Nombre(es)", self.paciente.name if self.paciente else "")
        self.lastF = _make_field("Apellido(s)", self.paciente.lastName if self.paciente else "")
        self.ageF = _make_field("Edad", str(self.paciente.age) if self.paciente else "")
        self.ciF = _make_field("CI", str(self.paciente.CI) if self.paciente else "")
        self.dateF = _make_field("Fecha de Ingreso", self.paciente.entryDate if self.paciente else "")
        self.phoneF = _make_field("Teléfono", self.paciente.phoneNumber if self.paciente else "")
        self.homeF = _make_field("Dirección", self.paciente.home if self.paciente else "")
        self.repNameF = _make_field("Representante (Si aplica)", self.paciente.representName if self.paciente else "")
        self.repCiF = _make_field("CI Representante (Si aplica)", str(self.paciente.representCI) if self.paciente and self.paciente.representCI else "")
        self.motivF = _make_field("Motivo de Consulta", self.paciente.consultReason if self.paciente else "")
        self.symptF = _make_field("Sintomatología Actual", self.paciente.presentIssues if self.paciente else "", multiline=True)

        grid.addWidget(self.nameF, 0, 0)
        grid.addWidget(self.lastF, 0, 1)
        grid.addWidget(self.ageF, 1, 0)
        grid.addWidget(self.ciF, 1, 1)
        grid.addWidget(self.dateF, 2, 0)
        grid.addWidget(self.phoneF, 2, 1)
        grid.addWidget(self.homeF, 3, 0, 1, 2)
        grid.addWidget(self.repNameF, 4, 0)
        grid.addWidget(self.repCiF, 4, 1)
        grid.addWidget(self.motivF, 5, 0, 1, 2)
        grid.addWidget(self.symptF, 6, 0, 1, 2)

        card_layout = QVBoxLayout(card)
        card_layout.addLayout(grid)

        layout.addWidget(card)
        return layout

    def _build_antecedentes_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Antecedentes Personales")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        card = self._make_card()
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)

        self.ant_checks = []
        for i, (label, fname) in enumerate(ANTECEDENT_FIELDS):
            val = getattr(self.antecedentes, fname) if self.antecedentes else None
            checked = val is not None and val != ""
            ctxt = val[5:] if checked and val and val.startswith("Si - ") else ""

            cb = QCheckBox(label)
            cb.setChecked(checked)
            cb.setFont(QFont("Segoe UI", 10))
            cb.setStyleSheet(f"""
                QCheckBox {{
                    color: {Txt2};
                    spacing: 8px;
                }}
                QCheckBox::indicator {{
                    width: 18px;
                    height: 18px;
                    border: 2px solid {PrimaryBorder};
                    border-radius: 4px;
                    background-color: {White};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {Second};
                    border-color: {Second};
                }}
            """)

            tf = _make_field("Contexto...", ctxt, multiline=True)
            tf.setVisible(checked)
            tf.setFixedHeight(65)

            cb.toggled.connect(lambda checked, t=tf: t.setVisible(checked))

            self.ant_checks.append((fname, cb, tf))

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        for i, (fname, cb, tf) in enumerate(self.ant_checks):
            row = i // 2
            col = i % 2

            container = QFrame()
            container.setStyleSheet(f"""
                QFrame {{
                    background-color: {White};
                    border: none;
                    border-radius: 8px;
                }}
            """)
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(12, 10, 12, 10)
            container_layout.setSpacing(6)
            container_layout.addWidget(cb)
            container_layout.addWidget(tf)

            grid.addWidget(container, row, col)

        card_layout.addLayout(grid)
        layout.addWidget(card)
        return layout

    def _build_examen_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Examen Físico")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        card = self._make_card()
        card_layout = QVBoxLayout(card)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.extF = _make_field("Extraoral", self.examen.extraoral if self.examen else "")
        self.itbF = _make_field("Intraoral TB", self.examen.intraoralTB if self.examen else "")
        self.itdF = _make_field("Intraoral TD", self.examen.intraoralTD if self.examen else "")
        self.periF = _make_field("Periodontal", self.examen.periodontal if self.examen else "")
        self.paF = _make_field("PA", self.examen.PA if self.examen else "")

        grid.addWidget(self.extF, 0, 0, 1, 2)
        grid.addWidget(self.itbF, 1, 0)
        grid.addWidget(self.itdF, 1, 1)
        grid.addWidget(self.periF, 2, 0)
        grid.addWidget(self.paF, 2, 1)

        card_layout.addLayout(grid)
        layout.addWidget(card)
        return layout

    def _build_odontogram_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Odontograma")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        self.odontogram_widget = OdontogramWidget()
        if self.odontograma_details:
            self.odontogram_widget.load_data(self.odontograma_details)

        card = self._make_card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.addWidget(self.odontogram_widget)

        layout.addWidget(card)
        return layout

    def _build_pricing_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Costo del Tratamiento")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        card = self._make_card()
        card_layout = QVBoxLayout(card)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.costF = _make_field("Costo total ($)", "")
        self.abonoF = _make_field("Abono inicial ($)", "")
        self.descAbonoF = _make_field("Descripción del abono", "")

        grid.addWidget(self.costF, 0, 0)
        grid.addWidget(self.abonoF, 0, 1)
        grid.addWidget(self.descAbonoF, 1, 0, 1, 2)

        if self.is_edit and self.last_abono:
            self.costF.setText(str(self.last_abono.treatmentCost) if self.last_abono.treatmentCost else "")
            self.abonoF.setText(str(self.last_abono.amount) if self.last_abono.amount else "")
            self.descAbonoF.setText(self.last_abono.description if self.last_abono.description else "")

        card_layout.addLayout(grid)
        layout.addWidget(card)
        return layout

    def _make_card(self):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border: none;
                border-radius: 14px;
                padding: 4px;
            }}
        """)
        return card

    def _save(self):
        try:
            form_data = {
                "name": self.nameF.text().strip(),
                "lastName": self.lastF.text().strip(),
                "age": self.ageF.text().strip(),
                "CI": self.ciF.text().strip(),
                "entryDate": self.dateF.text().strip(),
                "phoneNumber": self.phoneF.text().strip(),
                "home": self.homeF.text().strip(),
                "representName": self.repNameF.text().strip(),
                "representCI": self.repCiF.text().strip(),
                "consultReason": self.motivF.text().strip(),
                "presentIssues": self.symptF.toPlainText().strip(),
                "extraoral": self.extF.text(),
                "intraoralTB": self.itbF.text(),
                "intraoralTD": self.itdF.text(),
                "periodontal": self.periF.text(),
                "PA": self.paF.text(),
                "cost": self.costF.text().strip(),
                "abono": self.abonoF.text().strip(),
                "descAbono": self.descAbonoF.text().strip(),
            }
            save_patient(self.patient_id, form_data, self.ant_checks, self.odontogram_widget)
            self.saved.emit()
        except ValueError as ex:
            QMessageBox.warning(self, "Error de validación", str(ex))
        except Exception as ex:
            QMessageBox.critical(self, "Error al guardar", f"No se pudo guardar el registro:\n{ex}")
