from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from database.utils import readPACIENTE, readANTECEDENTES, readEXAMEN, readREMAINING, readODONTOGRAMA_by_patient
from database.createDB import deleteRow_PACIENTES, readODONTOGRAMA_DETAILS

Primary = "#C9929B"
PrimaryBorder = "#E8D5D8"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
Bg = "#FDF2F4"
White = "#FFFFFF"
Danger = "#DC2626"

ANTECEDENT_LABELS = [
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


def _field(label, value):
    w = QWidget()
    w.setStyleSheet("background: transparent;")
    lo = QVBoxLayout(w)
    lo.setContentsMargins(0, 0, 0, 0)
    lo.setSpacing(2)

    l = QLabel(label)
    l.setFont(QFont("Segoe UI", 11))
    l.setStyleSheet(f"color: {Txt2}; background: transparent;")
    lo.addWidget(l)

    v = QLabel(str(value) if value else "—")
    v.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
    v.setStyleSheet(f"color: {Txt1}; background: transparent;")
    v.setWordWrap(True)
    lo.addWidget(v)

    return w


def _card(title):
    frame = QFrame()
    frame.setStyleSheet(f"""
        QFrame {{
            background-color: {White};
            border: none;
            border-radius: 14px;
        }}
    """)
    lo = QVBoxLayout(frame)
    lo.setContentsMargins(24, 20, 24, 24)
    lo.setSpacing(16)
    t = QLabel(title)
    t.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
    t.setStyleSheet(f"color: {Txt1}; background: transparent;")
    lo.addWidget(t)
    return frame, lo


class PatientDetailView(QWidget):
    navigate = Signal(str, object)

    def __init__(self, patient_id=None, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.navigate_callback = navigate_callback
        self.paciente = readPACIENTE(patient_id) if patient_id else None
        self.antecedentes = readANTECEDENTES(patient_id) if patient_id else None
        self.examen = readEXAMEN(patient_id) if patient_id else None
        self.remaining = readREMAINING(patient_id) if patient_id else 0.0
        self.remaining = self.remaining if self.remaining is not None else 0.0
        self.odontograma = readODONTOGRAMA_by_patient(patient_id) if patient_id else None
        self.odontograma_details = []
        if self.odontograma:
            self.odontograma_details = readODONTOGRAMA_DETAILS(self.odontograma[0])
        self.setStyleSheet(f"background-color: {Bg};")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_header())

        if not self.paciente:
            lbl = QLabel("Paciente no encontrado")
            lbl.setFont(QFont("Segoe UI", 16))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")
            root.addWidget(lbl, 1)
            return

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: transparent; width: 8px; }
            QScrollBar::handle:vertical { background: #D1D5DB; border-radius: 4px; min-height: 32px; }
            QScrollBar::handle:vertical:hover { background: #9CA3AF; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
        """)

        body = QWidget()
        body.setStyleSheet("background: transparent;")
        body_lo = QVBoxLayout(body)
        body_lo.setContentsMargins(40, 32, 40, 40)
        body_lo.setSpacing(24)

        body_lo.addWidget(self._section_personal())
        body_lo.addWidget(self._section_antecedentes())
        body_lo.addWidget(self._section_examen())
        body_lo.addWidget(self._section_odontogram())
        body_lo.addWidget(self._section_saldo())

        body_lo.addStretch()
        scroll.setWidget(body)
        root.addWidget(scroll, 1)

    def _build_header(self):
        hdr = QFrame()
        hdr.setFixedHeight(72)
        hdr.setStyleSheet(f"QFrame {{ background-color: {White}; border: none; }}")
        lo = QHBoxLayout(hdr)
        lo.setContentsMargins(32, 0, 32, 0)

        back = QPushButton("\u2190 Volver")
        back.setFixedHeight(38)
        back.setCursor(Qt.PointingHandCursor)
        back.setFont(QFont("Segoe UI", 11))
        back.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {Txt2}; border: none; }}
            QPushButton:hover {{ color: {Txt1}; }}
        """)
        if self.navigate_callback:
            back.clicked.connect(lambda: self.navigate_callback("principal"))
        lo.addWidget(back)

        lo.addSpacing(24)

        name = f"{self.paciente[1]} {self.paciente[2]}" if self.paciente else ""
        title = QLabel(name)
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        lo.addWidget(title)

        lo.addStretch()

        age = QLabel(f"{self.paciente[3]} años")
        age.setFont(QFont("Segoe UI", 13))
        age.setStyleSheet(f"color: {Txt2}; background: transparent;")
        lo.addWidget(age)

        sep = QLabel("·")
        sep.setFont(QFont("Segoe UI", 16))
        sep.setStyleSheet(f"color: {PrimaryBorder}; background: transparent;")
        lo.addWidget(sep)

        ci = QLabel(f"CI: {self.paciente[4]}")
        ci.setFont(QFont("Segoe UI", 13))
        ci.setStyleSheet(f"color: {Txt2}; background: transparent;")
        lo.addWidget(ci)

        lo.addSpacing(20)

        edit_btn = QPushButton("Editar")
        edit_btn.setFixedHeight(38)
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        edit_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {Second}; color: white; border: 1px solid #C07088; border-radius: 8px; padding: 0 20px; }}
            QPushButton:hover {{ background-color: #C07088; border-color: {Second}; }}
        """)
        if self.navigate_callback:
            edit_btn.clicked.connect(lambda: self.navigate_callback("form", self.patient_id))
        lo.addWidget(edit_btn)

        del_btn = QPushButton("Eliminar")
        del_btn.setFixedHeight(38)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        del_btn.setStyleSheet(f"""
            QPushButton {{ background-color: #E8807A; color: white; border: 1px solid #D66E68; border-radius: 8px; padding: 0 20px; }}
            QPushButton:hover {{ background-color: #D66E68; border-color: #C55C56; }}
        """)
        del_btn.clicked.connect(self._on_delete)
        lo.addWidget(del_btn)

        return hdr

    def _section_personal(self):
        frame, lo = _card("Datos Personales")

        g = QGridLayout()
        g.setSpacing(16)
        g.setColumnStretch(0, 1)
        g.setColumnStretch(1, 1)
        g.setColumnStretch(2, 1)

        g.addWidget(_field("Nombre", self.paciente[1]), 0, 0)
        g.addWidget(_field("Apellido", self.paciente[2]), 0, 1)
        g.addWidget(_field("Edad", f"{self.paciente[3]} años"), 0, 2)
        g.addWidget(_field("CI", self.paciente[4]), 1, 0)
        g.addWidget(_field("Teléfono", self.paciente[6]), 1, 1)
        g.addWidget(_field("Fecha de ingreso", self.paciente[5]), 1, 2)
        g.addWidget(_field("Dirección", self.paciente[7]), 2, 0, 1, 3)
        g.addWidget(_field("Representante", self.paciente[8]), 3, 0)
        g.addWidget(_field("CI Rep.", self.paciente[9] if self.paciente[9] else None), 3, 1)

        lo.addLayout(g)

        lo.addWidget(_field("Motivo de consulta", self.paciente[10]))

        if self.paciente[11]:
            st = QLabel("Sintomatología")
            st.setFont(QFont("Segoe UI", 11))
            st.setStyleSheet(f"color: {Txt2}; background: transparent;")
            lo.addWidget(st)
            stxt = QLabel(self.paciente[11])
            stxt.setFont(QFont("Segoe UI", 12))
            stxt.setStyleSheet(f"color: {Txt1}; background: transparent;")
            stxt.setWordWrap(True)
            lo.addWidget(stxt)

        return frame

    def _section_antecedentes(self):
        frame, lo = _card("Antecedentes Personales")

        items = []
        for label, fname in ANTECEDENT_LABELS:
            idx = ANTECEDENT_LABELS.index((label, fname))
            val = self.antecedentes[idx + 2] if self.antecedentes else None
            if val and val != "":
                display = val[5:] if val.startswith("Si - ") else "Sí"
                items.append((label, display))

        if items:
            grid = QGridLayout()
            grid.setSpacing(12)
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)

            for i, (label, display) in enumerate(items):
                row = i // 2
                col = i % 2

                badge = QLabel(label)
                badge.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
                badge.setStyleSheet(f"""
                    background-color: {Primary};
                    color: white;
                    border-radius: 6px;
                    padding: 5px 12px;
                """)
                badge.setFixedHeight(30)
                badge.setAlignment(Qt.AlignCenter)

                val_lbl = QLabel(display)
                val_lbl.setFont(QFont("Segoe UI", 11))
                val_lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")

                item = QHBoxLayout()
                item.setSpacing(10)
                item.addWidget(badge)
                item.addWidget(val_lbl, 1)
                grid.addLayout(item, row, col)

            lo.addLayout(grid)
        else:
            empty = QLabel("Sin antecedentes registrados")
            empty.setFont(QFont("Segoe UI", 12))
            empty.setStyleSheet(f"color: {Txt2}; background: transparent;")
            lo.addWidget(empty)

        return frame

    def _section_examen(self):
        frame, lo = _card("Examen Físico")

        g = QGridLayout()
        g.setSpacing(16)
        g.setColumnStretch(0, 1)
        g.setColumnStretch(1, 1)
        g.setColumnStretch(2, 1)

        g.addWidget(_field("Extraoral", self.examen[2] if self.examen else None), 0, 0)
        g.addWidget(_field("Intraoral TB", self.examen[3] if self.examen else None), 0, 1)
        g.addWidget(_field("Intraoral TD", self.examen[4] if self.examen else None), 0, 2)
        g.addWidget(_field("Periodontal", self.examen[5] if self.examen else None), 1, 0)
        g.addWidget(_field("PA", self.examen[6] if self.examen else None), 1, 1)

        lo.addLayout(g)
        return frame

    def _section_odontogram(self):
        frame, lo = _card("Odontograma")

        if not self.odontograma_details:
            empty = QLabel("Sin odontograma registrado")
            empty.setFont(QFont("Segoe UI", 12))
            empty.setStyleSheet(f"color: {Txt2}; background: transparent;")
            lo.addWidget(empty)
            return frame

        from views.components.odontogram import OdontogramWidget, TOOL_COLORS, FACE_LABELS
        odontogram = OdontogramWidget()
        odontogram.load_data(self.odontograma_details)

        for tw in odontogram._tooth_widgets.values():
            tw.setEnabled(False)
            tw.setCursor(Qt.ArrowCursor)

        lo.addWidget(odontogram)

        if self.odontograma and self.odontograma[2]:
            notes_label = QLabel(f"Notas: {self.odontograma[2]}")
            notes_label.setFont(QFont("Segoe UI", 11))
            notes_label.setStyleSheet(f"color: {Txt1}; background: transparent;")
            notes_label.setWordWrap(True)
            lo.addWidget(notes_label)

        return frame

    def _section_saldo(self):
        frame, lo = _card("Saldo Pendiente")

        lbl = QLabel(f"${self.remaining:.2f}")
        lbl.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        lbl.setStyleSheet(f"color: {Second}; background: transparent;")
        lbl.setAlignment(Qt.AlignCenter)
        lo.addWidget(lbl)

        return frame

    def _on_delete(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar eliminación")
        msg.setText(f"¿Eliminar a {self.paciente[1]} {self.paciente[2]}?")
        msg.setInformativeText("Esta acción no se puede deshacer.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        if msg.exec() == QMessageBox.Yes:
            try:
                deleteRow_PACIENTES(self.patient_id)
                if self.navigate_callback:
                    self.navigate_callback("principal")
            except Exception as ex:
                err = QMessageBox()
                err.setIcon(QMessageBox.Critical)
                err.setWindowTitle("Error")
                err.setText(f"Error al eliminar: {ex}")
                err.exec()
