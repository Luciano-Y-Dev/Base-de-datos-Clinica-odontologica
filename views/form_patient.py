from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QLineEdit, QTextEdit, QCheckBox,
    QGridLayout, QGroupBox, QMessageBox, QDialog, QDateEdit
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont
from services.patient_service import save_patient, ci_exists
from services.tratamiento_service import (
    add_tratamiento, update_tratamiento, delete_tratamiento,
    get_patient_tratamientos
)
from views.components.odontogram import OdontogramWidget
from views.components.tratamiento_dialog import TratamientoDialog

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
        self.tratamientos = data.get("tratamientos", []) if data else []
        self.pending_tratamientos = []
        self.odontograma = data.get("odontograma") if data else None
        self.odontograma_details = data.get("odontograma_details", []) if data else []
        self.has_abonos = data.get("has_abonos", False) if data else False
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
        content_layout.addLayout(self._build_tratamiento_section())
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

        self.dateF = QDateEdit()
        self.dateF.setCalendarPopup(True)
        self.dateF.setFont(QFont("Segoe UI", 11))
        self.dateF.setFixedHeight(42)
        self.dateF.setStyleSheet(f"""
            QDateEdit {{
                background-color: {almost_rose};
                border: none;
                border-radius: 10px;
                padding: 10px 12px;
                color: {Txt1};
            }}
            QDateEdit:focus {{
                border: none;
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border: none;
            }}
        """)
        if self.paciente and self.paciente.entryDate:
            self.dateF.setDate(QDate.fromString(self.paciente.entryDate, "yyyy-MM-dd"))
        else:
            self.dateF.setDate(QDate.currentDate())

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

        notes_label = QLabel("Notas del odontograma")
        notes_label.setFont(QFont("Segoe UI", 10))
        notes_label.setStyleSheet(f"color: {Txt2}; background: transparent;")
        card_layout.addWidget(notes_label)

        notes_text = self.odontograma.notes if self.odontograma and self.odontograma.notes else ""
        self.odontoNotesF = _make_field("Observaciones generales del odontograma...", notes_text, multiline=True)
        card_layout.addWidget(self.odontoNotesF)

        layout.addWidget(card)
        return layout

    def _build_tratamiento_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Tratamiento")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        self._tratamiento_card = self._make_card()
        self._tratamiento_card_lo = QVBoxLayout(self._tratamiento_card)
        layout.addWidget(self._tratamiento_card)

        self._refresh_tratamiento_list()
        return layout

    def _refresh_tratamiento_list(self):
        while self._tratamiento_card_lo.count():
            item = self._tratamiento_card_lo.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        all_tratamientos = list(self.tratamientos) + list(self.pending_tratamientos)

        if not all_tratamientos:
            empty = QLabel("Sin tratamientos registrados")
            empty.setFont(QFont("Segoe UI", 12))
            empty.setStyleSheet(f"color: {Txt2}; background: transparent;")
            self._tratamiento_card_lo.addWidget(empty)
        else:
            for t in all_tratamientos:
                self._tratamiento_card_lo.addWidget(self._make_tratamiento_item(t))

        add_btn = QPushButton("+ Añadir nuevo tratamiento")
        add_btn.setFixedHeight(36)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setFont(QFont("Segoe UI", 10))
        add_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {Second}; color: white; border: none; border-radius: 8px; padding: 0 20px; }}
            QPushButton:hover {{ background-color: #C0607A; }}
            QPushButton:pressed {{ background-color: #A84860; }}
        """)
        add_btn.clicked.connect(self._on_add_tratamiento)
        self._tratamiento_card_lo.addWidget(add_btn)

    def _make_tratamiento_item(self, t):
        is_pending = isinstance(t, dict)

        item_frame = QFrame()
        item_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {pale_pink};
                border: none;
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        item_lo = QVBoxLayout(item_frame)
        item_lo.setContentsMargins(12, 10, 12, 10)
        item_lo.setSpacing(4)

        header_lo = QHBoxLayout()
        date_lbl = QLabel(t.get("date", "") if is_pending else (t.date or "Sin fecha"))
        date_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        date_lbl.setStyleSheet(f"color: {Second}; background: transparent;")
        header_lo.addWidget(date_lbl)
        header_lo.addStretch()

        edit_btn = QPushButton("Editar")
        edit_btn.setFixedHeight(28)
        edit_btn.setCursor(Qt.PointingHandCursor)
        edit_btn.setFont(QFont("Segoe UI", 9))
        edit_btn.setStyleSheet(f"""
            QPushButton {{ background-color: {Second}; color: white; border: none; border-radius: 6px; padding: 0 12px; }}
            QPushButton:hover {{ background-color: #C0607A; }}
        """)
        header_lo.addWidget(edit_btn)

        del_btn = QPushButton("Eliminar")
        del_btn.setFixedHeight(28)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.setFont(QFont("Segoe UI", 9))
        del_btn.setStyleSheet(f"""
            QPushButton {{ background-color: transparent; color: #C0607A; border: 1px solid #E8B4C0; border-radius: 6px; padding: 0 12px; }}
            QPushButton:hover {{ background-color: #FDECEF; }}
        """)
        header_lo.addWidget(del_btn)

        if is_pending:
            idx = self.pending_tratamientos.index(t)
            edit_btn.clicked.connect(lambda _, i=idx: self._on_edit_pending(i))
            del_btn.clicked.connect(lambda _, i=idx: self._on_delete_pending(i))
        else:
            edit_btn.clicked.connect(lambda _, tid=t.id, txt=t.diagnosis, dt=t.date: self._on_edit_tratamiento(tid, txt, dt))
            del_btn.clicked.connect(lambda _, tid=t.id: self._on_delete_tratamiento(tid))

        item_lo.addLayout(header_lo)

        text_lbl = QLabel(t.get("text", "") if is_pending else (t.diagnosis or ""))
        text_lbl.setFont(QFont("Segoe UI", 11))
        text_lbl.setStyleSheet(f"color: {Txt1}; background: transparent;")
        text_lbl.setWordWrap(True)
        item_lo.addWidget(text_lbl)

        return item_frame

    def prompt_new_tratamiento(self):
        self._on_add_tratamiento()

    def _on_add_tratamiento(self):
        dialog = TratamientoDialog(parent=self)
        if dialog.exec() == QDialog.Accepted:
            text, date = dialog.get_data()
            try:
                if self.patient_id:
                    add_tratamiento(self.patient_id, text, date)
                    self.tratamientos = get_patient_tratamientos(self.patient_id)
                else:
                    self.pending_tratamientos.append({"text": text, "date": date})
                self._refresh_tratamiento_list()
            except Exception as ex:
                QMessageBox.critical(self, "Error", f"No se pudo guardar: {ex}")

    def _on_edit_tratamiento(self, tratamiento_id, current_text, current_date):
        dialog = TratamientoDialog(text=current_text, date=current_date, parent=self)
        if dialog.exec() == QDialog.Accepted:
            text, date = dialog.get_data()
            try:
                update_tratamiento(tratamiento_id, text, date)
                self.tratamientos = get_patient_tratamientos(self.patient_id)
                self._refresh_tratamiento_list()
            except Exception as ex:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar: {ex}")

    def _on_delete_tratamiento(self, tratamiento_id):
        answer = QMessageBox.question(
            self, "Eliminar tratamiento",
            "¿Eliminar este tratamiento? Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if answer != QMessageBox.Yes:
            return
        try:
            delete_tratamiento(tratamiento_id)
            self.tratamientos = get_patient_tratamientos(self.patient_id)
            self._refresh_tratamiento_list()
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar: {ex}")

    def _on_edit_pending(self, index):
        t = self.pending_tratamientos[index]
        dialog = TratamientoDialog(text=t["text"], date=t["date"], parent=self)
        if dialog.exec() == QDialog.Accepted:
            text, date = dialog.get_data()
            self.pending_tratamientos[index] = {"text": text, "date": date}
            self._refresh_tratamiento_list()

    def _on_delete_pending(self, index):
        del self.pending_tratamientos[index]
        self._refresh_tratamiento_list()

    def _build_pricing_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("Costo del Tratamiento")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        # Si el paciente ya tiene abonos, el historial de pagos solo se
        # gestiona desde la vista de Abonos (para no alterar saldos).
        if self.is_edit and self.has_abonos:
            card = self._make_card()
            card_layout = QVBoxLayout(card)
            note = QLabel("Este paciente ya tiene pagos registrados.\nGestiona sus abonos desde la sección Abonos.")
            note.setFont(QFont("Segoe UI", 11))
            note.setStyleSheet(f"color: {Txt2}; background: transparent;")
            note.setWordWrap(True)
            card_layout.addWidget(note)
            layout.addWidget(card)
            self.costF = None
            self.abonoF = None
            self.descAbonoF = None
            return layout

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
                "entryDate": self.dateF.date().toString("yyyy-MM-dd"),
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
                "odontogramNotes": self.odontoNotesF.toPlainText().strip(),
                "cost": self.costF.text().strip() if self.costF else "",
                "abono": self.abonoF.text().strip() if self.abonoF else "",
                "descAbono": self.descAbonoF.text().strip() if self.descAbonoF else "",
            }

            ci_text = form_data["CI"]
            if ci_text.isdigit() and ci_exists(ci_text, exclude_patient_id=self.patient_id):
                answer = QMessageBox.question(
                    self, "CI duplicada",
                    f"Ya existe otro paciente registrado con la CI {ci_text}.\n¿Guardar de todas formas?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if answer != QMessageBox.Yes:
                    return

            new_patient_id = save_patient(self.patient_id, form_data, self.ant_checks, self.odontogram_widget)
            if not self.patient_id and self.pending_tratamientos:
                for t in self.pending_tratamientos:
                    add_tratamiento(new_patient_id, t["text"], t["date"])
                self.pending_tratamientos.clear()
            self.saved.emit()
        except ValueError as ex:
            QMessageBox.warning(self, "Error de validación", str(ex))
        except Exception as ex:
            QMessageBox.critical(self, "Error al guardar", f"No se pudo guardar el registro:\n{ex}")
