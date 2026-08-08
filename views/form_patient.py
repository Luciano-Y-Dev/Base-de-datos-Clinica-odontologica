from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QLineEdit, QTextEdit, QCheckBox,
    QGridLayout, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from database.utils import (
    readPACIENTE, readANTECEDENTES, readEXAMEN,
    existANTECEDENTES, existEXAMEN,
    readODONTOGRAMA_by_patient, existODONTOGRAMA
)
from database.createDB import (
    createRow_PACIENTES, updateRow_PACIENTES,
    createRow_ANTECEDENTES, updateRow_ANTECEDENTES,
    createRow_EXAMEN, updateRow_EXAMEN,
    createRow_ODONTOGRAMA, updateRow_ODONTOGRAMA,
    createRow_ODONTOGRAMA_DETAILS, deleteRow_ODONTOGRAMA_DETAILS,
    readODONTOGRAMA_DETAILS,
    createRow_ABONO, readABONO, updateRow_ABONO
)
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

    def __init__(self, patient_id=None, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.navigate_callback = navigate_callback
        self.is_edit = patient_id is not None
        self.setStyleSheet(f"background-color: {pale_pink};")
        self._load_data()
        self._build_ui()

    def _load_data(self):
        if self.is_edit:
            self.paciente = readPACIENTE(self.patient_id)
            self.antecedentes = readANTECEDENTES(self.patient_id)
            self.examen = readEXAMEN(self.patient_id)
            self.odontograma = readODONTOGRAMA_by_patient(self.patient_id)
            self.odontograma_details = []
            if self.odontograma:
                self.odontograma_details = readODONTOGRAMA_DETAILS(self.odontograma[0])
        else:
            self.paciente = None
            self.antecedentes = None
            self.examen = None
            self.odontograma = None
            self.odontograma_details = []

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

        self.nameF = _make_field("Nombre(es)", self.paciente[1] if self.paciente else "")
        self.lastF = _make_field("Apellido(s)", self.paciente[2] if self.paciente else "")
        self.ageF = _make_field("Edad", str(self.paciente[3]) if self.paciente else "")
        self.ciF = _make_field("CI", str(self.paciente[4]) if self.paciente else "")
        self.dateF = _make_field("Fecha de Ingreso", self.paciente[5] if self.paciente else "")
        self.phoneF = _make_field("Teléfono", self.paciente[6] if self.paciente else "")
        self.homeF = _make_field("Dirección", self.paciente[7] if self.paciente else "")
        self.repNameF = _make_field("Representante (Si aplica)", self.paciente[8] if self.paciente else "")
        self.repCiF = _make_field("CI Representante (Si aplica)", str(self.paciente[9]) if self.paciente and self.paciente[9] else "")
        self.motivF = _make_field("Motivo de Consulta", self.paciente[10] if self.paciente else "")
        self.symptF = _make_field("Sintomatología Actual", self.paciente[11] if self.paciente else "", multiline=True)

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
            val = self.antecedentes[i + 2] if self.antecedentes else None
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

        self.extF = _make_field("Extraoral", self.examen[2] if self.examen else "")
        self.itbF = _make_field("Intraoral TB", self.examen[3] if self.examen else "")
        self.itdF = _make_field("Intraoral TD", self.examen[4] if self.examen else "")
        self.periF = _make_field("Periodontal", self.examen[5] if self.examen else "")
        self.paF = _make_field("PA", self.examen[6] if self.examen else "")

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

        if self.is_edit and self.patient_id:
            abonos = readABONO(self.patient_id)
            if abonos:
                last = abonos[-1]
                self.costF.setText(str(last[4]) if last[4] else "")
                self.abonoF.setText(str(last[5]) if last[5] else "")
                self.descAbonoF.setText(last[3] if last[3] else "")

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
            name = self.nameF.text().strip()
            last = self.lastF.text().strip()

            if not name:
                QMessageBox.warning(self, "Campo requerido", "El nombre es obligatorio.")
                return

            age_text = self.ageF.text().strip()
            if not age_text:
                QMessageBox.warning(self, "Campo requerido", "La edad es obligatoria.")
                return
            try:
                age = int(age_text)
            except ValueError:
                QMessageBox.warning(self, "Dato inválido", "La edad debe ser un número entero.")
                return

            ci_text = self.ciF.text().strip()
            if not ci_text:
                QMessageBox.warning(self, "Campo requerido", "La CI es obligatoria.")
                return
            try:
                ci = int(ci_text)
            except ValueError:
                QMessageBox.warning(self, "Dato inválido", "La CI debe ser un número entero.")
                return

            date = self.dateF.text().strip()
            phone = self.phoneF.text().strip()
            home = self.homeF.text().strip()
            rep_name = self.repNameF.text().strip()
            rep_ci_text = self.repCiF.text().strip()
            rep_ci = int(rep_ci_text) if rep_ci_text else 0
            motiv = self.motivF.text().strip()
            sympt = self.symptF.toPlainText().strip()

            if self.is_edit:
                updateRow_PACIENTES(self.patient_id, name, last, age, ci,
                    date, phone, home, rep_name, rep_ci, motiv, sympt)
                cid = self.patient_id
            else:
                cid = createRow_PACIENTES(name, last, age, ci,
                    date, phone, home, rep_name, rep_ci, motiv, sympt)

            ad = [None] * 20
            for idx, (fname, cb, tf) in enumerate(self.ant_checks):
                if cb.isChecked():
                    ad[idx] = f"Si - {tf.toPlainText()}" if tf.toPlainText() else "Si"
            if existANTECEDENTES(cid):
                updateRow_ANTECEDENTES(cid, *ad)
            else:
                createRow_ANTECEDENTES(cid, *ad)

            ed = [
                self.extF.text(), self.itbF.text(), self.itdF.text(),
                self.periF.text(), self.paF.text()
            ]
            if existEXAMEN(cid):
                updateRow_EXAMEN(cid, *ed)
            else:
                createRow_EXAMEN(cid, *ed)

            od_data = self.odontogram_widget.get_data()
            if od_data["affections"]:
                notes = ""
                if existODONTOGRAMA(cid):
                    od_header = readODONTOGRAMA_by_patient(cid)
                    odontogram_id = od_header[0]
                    updateRow_ODONTOGRAMA(odontogram_id, notes)
                else:
                    odontogram_id = createRow_ODONTOGRAMA(cid, notes)

                existing_details = readODONTOGRAMA_DETAILS(odontogram_id)
                for detail in existing_details:
                    deleteRow_ODONTOGRAMA_DETAILS(detail[0])

                for aff in od_data["affections"]:
                    createRow_ODONTOGRAMA_DETAILS(
                        odontogram_id,
                        aff["tooth"],
                        aff["face"],
                        aff["affected"],
                        aff["description"],
                    )

            cost_text = self.costF.text().strip()
            abono_text = self.abonoF.text().strip()
            desc_abono = self.descAbonoF.text().strip()
            if cost_text:
                try:
                    cost = float(cost_text)
                    amount = float(abono_text) if abono_text else 0.0
                    remaining = cost - amount
                    from datetime import date
                    today = date.today().isoformat()
                    abonos_existentes = readABONO(cid)
                    if abonos_existentes:
                        last_id = abonos_existentes[-1][0]
                        updateRow_ABONO(last_id, today, desc_abono, cost, amount, remaining)
                    else:
                        createRow_ABONO(cid, today, desc_abono, cost, amount, remaining)
                except ValueError:
                    pass

            self.saved.emit()
            if self.navigate_callback:
                self.navigate_callback("principal")

        except Exception as ex:
            QMessageBox.critical(self, "Error al guardar", f"No se pudo guardar el registro:\n{ex}")
