from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QLineEdit, QDateEdit, QMessageBox,
    QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont
from services.abono_service import add_abono, update_abono, delete_abono
from services.patient_service import filter_patients
from views.components.search_filter import SearchFilter

Primary = "#C9929B"
PrimaryBorder = "#E8D5D8"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"


class AbonosView(QWidget):
    def __init__(self, patients_pending=None, patients_paid=None, load_abonos_fn=None, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.selected_patient_id = None
        self._patients_pending = patients_pending or []
        self._patients_paid = patients_paid or []
        self._load_abonos_fn = load_abonos_fn
        self.setStyleSheet(f"background-color: {pale_pink};")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_header())

        body = QHBoxLayout()
        body.setContentsMargins(16, 16, 16, 16)
        body.setSpacing(16)

        self.patients_panel = self._build_patients_panel()
        body.addWidget(self.patients_panel, 1)

        self.detail_panel = self._build_detail_panel()
        body.addWidget(self.detail_panel, 2)

        root.addLayout(body, 1)

    def _build_header(self):
        hdr = QFrame()
        hdr.setFixedHeight(64)
        hdr.setStyleSheet(f"QFrame {{ background-color: {White}; border-bottom: 2px solid {PrimaryBorder}; }}")
        lo = QHBoxLayout(hdr)
        lo.setContentsMargins(24, 0, 24, 0)

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

        title = QLabel("Abonos")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        lo.addWidget(title)
        lo.addStretch()
        return hdr

    def _build_patients_panel(self):
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {White};
                border-radius: 14px;
            }}
        """)
        lo = QVBoxLayout(panel)
        lo.setContentsMargins(12, 12, 12, 12)
        lo.setSpacing(8)

        # Pestañas
        tabs_frame = QFrame()
        tabs_frame.setStyleSheet("background: transparent;")
        tabs_lo = QHBoxLayout(tabs_frame)
        tabs_lo.setContentsMargins(0, 0, 0, 0)
        tabs_lo.setSpacing(4)

        self.tab_pendientes = QPushButton("Pendientes")
        self.tab_pendientes.setFixedHeight(32)
        self.tab_pendientes.setCursor(Qt.PointingHandCursor)
        self.tab_pendientes.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.tab_pendientes.clicked.connect(lambda: self._switch_tab("pending"))
        self._style_tab(self.tab_pendientes, active=True)
        tabs_lo.addWidget(self.tab_pendientes)

        self.tab_saldadas = QPushButton("Saldadas")
        self.tab_saldadas.setFixedHeight(32)
        self.tab_saldadas.setCursor(Qt.PointingHandCursor)
        self.tab_saldadas.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.tab_saldadas.clicked.connect(lambda: self._switch_tab("paid"))
        self._style_tab(self.tab_saldadas, active=False)
        tabs_lo.addWidget(self.tab_saldadas)

        lo.addWidget(tabs_frame)

        self._search_filter = SearchFilter(show_dates=False)
        self._search_filter.filter_changed.connect(self._on_search_changed)
        lo.addWidget(self._search_filter)

        self.current_tab = "pending"

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: #D1D5DB; border-radius: 3px; min-height: 24px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        self.patients_list = QWidget()
        self.patients_list.setStyleSheet("background: transparent;")
        self.patients_layout = QVBoxLayout(self.patients_list)
        self.patients_layout.setContentsMargins(0, 0, 0, 0)
        self.patients_layout.setSpacing(4)
        self.patients_layout.addStretch()
        scroll.setWidget(self.patients_list)
        lo.addWidget(scroll, 1)

        self._load_patients()
        return panel

    def _style_tab(self, btn, active):
        if active:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Second};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 0 16px;
                }}
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {pale_pink};
                    color: {Txt2};
                    border: none;
                    border-radius: 8px;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: #F0E0E5;
                }}
            """)

    def _switch_tab(self, tab):
        self.current_tab = tab
        self._style_tab(self.tab_pendientes, active=(tab == "pending"))
        self._style_tab(self.tab_saldadas, active=(tab == "paid"))

        self.detail_placeholder.setVisible(True)
        self.detail_content.setVisible(False)
        self.selected_patient_id = None

        self._search_filter.reset()
        self._load_patients()

    def _on_search_changed(self, search_text, date_from, date_to):
        if self.current_tab == "pending":
            patients = self._patients_pending
        else:
            patients = self._patients_paid

        if search_text:
            patients = filter_patients(patients, search_text)

        self._load_patients(patients)

    def _load_patients(self, patients=None):
        while self.patients_layout.count():
            item = self.patients_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if patients is None:
            if self.current_tab == "pending":
                patients = self._patients_pending
            else:
                patients = self._patients_paid

        if not patients:
            empty_lbl = QLabel("No hay cuentas pendientes" if self.current_tab == "pending" else "No hay cuentas saldadas")
            empty_lbl.setAlignment(Qt.AlignCenter)
            empty_lbl.setFont(QFont("Segoe UI", 11))
            empty_lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")
            self.patients_layout.addWidget(empty_lbl)
            self.patients_layout.addStretch()
            return

        for p in patients:
            pid = p.id
            remaining = p.remaining if p.remaining is not None else 0.0

            card = QFrame()
            card.setCursor(Qt.PointingHandCursor)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {pale_pink};
                    border-radius: 10px;
                    padding: 4px;
                }}
                QFrame:hover {{
                    background-color: #FFF5F7;
                }}
            """)
            card_lo = QVBoxLayout(card)
            card_lo.setContentsMargins(12, 10, 12, 10)
            card_lo.setSpacing(2)

            name = QLabel(f"{p.name} {p.lastName}")
            name.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
            name.setStyleSheet(f"color: {Txt1}; background: transparent;")
            card_lo.addWidget(name)

            if self.current_tab == "paid":
                amt = QLabel("Saldado")
                amt.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
                amt.setStyleSheet(f"color: #4CAF50; background: transparent;")
            else:
                amt = QLabel(f"${remaining:.2f}")
                amt.setFont(QFont("Segoe UI", 10))
                amt.setStyleSheet(f"color: {Second}; background: transparent;")
            card_lo.addWidget(amt)

            card.mousePressEvent = lambda _, i=pid: self._select_patient(i)
            self.patients_layout.addWidget(card)

        self.patients_layout.addStretch()

    def _build_detail_panel(self):
        panel = QFrame()
        panel.setObjectName("detailPanel")
        panel.setStyleSheet(f"""
            QFrame#detailPanel {{
                background-color: {White};
                border-radius: 14px;
            }}
        """)
        lo = QVBoxLayout(panel)
        lo.setContentsMargins(28, 50, 28, 28)
        lo.setSpacing(16)

        self.detail_title = QLabel("Selecciona un paciente")
        self.detail_title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.detail_title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        lo.addWidget(self.detail_title)

        self.detail_placeholder = QLabel("Haz clic en un paciente\npara ver sus abonos")
        self.detail_placeholder.setAlignment(Qt.AlignCenter)
        self.detail_placeholder.setFont(QFont("Segoe UI", 13))
        self.detail_placeholder.setStyleSheet(f"color: {Txt2}; background: transparent;")
        lo.addWidget(self.detail_placeholder, 1)

        self.detail_content = QFrame()
        self.detail_content.setObjectName("detailContent")
        self.detail_content.setVisible(False)
        self.detail_content.setStyleSheet(f"""
            QFrame#detailContent {{
                background-color: {pale_pink};
                border-radius: 14px;
                border: none;
            }}
        """)
        dc_lo = QVBoxLayout(self.detail_content)
        dc_lo.setContentsMargins(12, 12, 12, 12)
        dc_lo.setSpacing(12)

        balance_card = QFrame()
        balance_card.setObjectName("balanceCard")
        balance_card.setStyleSheet(f"""
            QFrame#balanceCard {{
                background-color: {pale_pink};
                border-radius: 14px;
            }}
        """)
        bc_lo = QVBoxLayout(balance_card)
        bc_lo.setContentsMargins(24, 24, 24, 24)

        self.balance_label = QLabel()
        self.balance_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.balance_label.setStyleSheet(f"color: {Second}; background: transparent;")
        bc_lo.addWidget(self.balance_label)

        dc_lo.addWidget(balance_card)

        self.abonos_scroll = QScrollArea()
        self.abonos_scroll.setWidgetResizable(True)
        self.abonos_scroll.setFrameShape(QFrame.NoFrame)
        self.abonos_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.abonos_scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: #D1D5DB; border-radius: 3px; min-height: 24px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        self.abonos_list = QWidget()
        self.abonos_list.setStyleSheet("background: transparent;")
        self.abonos_list_lo = QVBoxLayout(self.abonos_list)
        self.abonos_list_lo.setContentsMargins(0, 0, 0, 0)
        self.abonos_list_lo.setSpacing(6)
        self.abonos_list_lo.addStretch()
        self.abonos_scroll.setWidget(self.abonos_list)
        dc_lo.addWidget(self.abonos_scroll, 1)

        self.new_frame = QFrame()
        self.new_frame.setObjectName("newFrame")
        self.new_frame.setStyleSheet(f"""
            QFrame#newFrame {{
                background-color: {pale_pink};
                border-radius: 10px;
            }}
        """)
        nf_lo = QHBoxLayout(self.new_frame)
        nf_lo.setContentsMargins(12, 8, 12, 8)
        nf_lo.setSpacing(8)

        self.date_field = QDateEdit()
        self.date_field.setDate(QDate.currentDate())
        self.date_field.setCalendarPopup(True)
        self.date_field.setFont(QFont("Segoe UI", 10))
        self.date_field.setFixedHeight(32)
        self.date_field.setMinimumWidth(130)
        self.date_field.setStyleSheet(f"""
            QDateEdit {{
                background-color: {White};
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                color: {Txt1};
            }}
            QDateEdit:focus {{ border: none; }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border: none;
            }}
        """)
        nf_lo.addWidget(self.date_field)

        self.amount_field = QLineEdit()
        self.amount_field.setPlaceholderText("Monto ($)")
        self.amount_field.setFont(QFont("Segoe UI", 10))
        self.amount_field.setFixedHeight(32)
        self.amount_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {White};
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                color: {Txt1};
            }}
            QLineEdit:focus {{ border: none; }}
        """)
        nf_lo.addWidget(self.amount_field, 1)

        self.desc_field = QLineEdit()
        self.desc_field.setPlaceholderText("Descripción")
        self.desc_field.setFont(QFont("Segoe UI", 10))
        self.desc_field.setFixedHeight(32)
        self.desc_field.setStyleSheet(f"""
            QLineEdit {{
                background-color: {White};
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                color: {Txt1};
            }}
            QLineEdit:focus {{ border: none; }}
        """)
        nf_lo.addWidget(self.desc_field, 1)

        add_btn = QPushButton("Agregar")
        add_btn.setFixedSize(80, 32)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Second};
                color: white;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{ background-color: #C0607A; }}
        """)
        add_btn.clicked.connect(self._add_abono)
        nf_lo.addWidget(add_btn)

        dc_lo.addWidget(self.new_frame)

        lo.addWidget(self.detail_content, 1)
        return panel

    def _select_patient(self, patient_id):
        self.selected_patient_id = patient_id
        self.detail_placeholder.setVisible(False)
        self.detail_content.setVisible(True)

        patients = self._patients_pending if self.current_tab == "pending" else self._patients_paid
        for p in patients:
            if p.id == patient_id:
                self.detail_title.setText(f"{p.name} {p.lastName}")
                remaining = p.remaining if p.remaining is not None else 0.0
                if self.current_tab == "paid":
                    self.balance_label.setText("Cuenta saldada")
                    self.balance_label.setStyleSheet("color: #4CAF50; background: transparent;")
                else:
                    self.balance_label.setText(f"Saldo pendiente: ${remaining:.2f}")
                    self.balance_label.setStyleSheet(f"color: {Second}; background: transparent;")
                break

        # Ocultar formulario de nuevo abono si la cuenta está saldada
        if self.current_tab == "paid":
            self.new_frame.setVisible(False)
        else:
            self.new_frame.setVisible(True)

        self._load_abonos()

    def _load_abonos(self):
        while self.abonos_list_lo.count():
            item = self.abonos_list_lo.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.selected_patient_id:
            return

        abonos = self._load_abonos_fn(self.selected_patient_id) if self._load_abonos_fn else []
        abonos = list(reversed(abonos))  # Ordena del abono inicial al abono final
        for i, a in enumerate(abonos):
            row = QFrame()
            row.setStyleSheet(f"""
                QFrame {{
                    background-color: {pale_pink};
                    border-radius: 8px;
                    padding: 2px;
                }}
            """)
            row_lo = QHBoxLayout(row)
            row_lo.setContentsMargins(12, 8, 12, 8)
            row_lo.setSpacing(12)

            date_lbl = QLabel(a.date if a.date else "—")
            date_lbl.setFont(QFont("Segoe UI", 10))
            date_lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")
            row_lo.addWidget(date_lbl, 1)

            desc_lbl = QLabel(a.description if a.description else "—")
            desc_lbl.setFont(QFont("Segoe UI", 10))
            desc_lbl.setStyleSheet(f"color: {Txt1}; background: transparent;")
            row_lo.addWidget(desc_lbl, 2)

            prev_balance = abonos[i-1].remaining if i > 0 else a.treatmentCost
            if i == 0:
                math_text = f"Costo inicial: ${prev_balance:.2f} - Abono: ${a.amount:.2f} = Saldo: ${a.remaining:.2f}"
            else:
                math_text = f"Saldo: ${prev_balance:.2f} - Abono: ${a.amount:.2f} = Saldo: ${a.remaining:.2f}"

            math_lbl = QLabel(math_text)
            math_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
            math_lbl.setStyleSheet(f"color: {Second}; background: transparent;")
            math_lbl.setAlignment(Qt.AlignRight)
            row_lo.addWidget(math_lbl, 2)

            edit_btn = QPushButton("Editar")
            edit_btn.setFixedSize(56, 24)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setFont(QFont("Segoe UI", 8))
            edit_btn.setStyleSheet(f"""
                QPushButton {{ background-color: {Second}; color: white; border: none; border-radius: 6px; }}
                QPushButton:hover {{ background-color: #C0607A; }}
            """)
            edit_btn.clicked.connect(lambda _, ab=a: self._edit_abono(ab))
            row_lo.addWidget(edit_btn)

            del_btn = QPushButton("✕")
            del_btn.setFixedSize(24, 24)
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            del_btn.setStyleSheet(f"""
                QPushButton {{ background-color: transparent; color: #C0607A; border: 1px solid #E8B4C0; border-radius: 6px; }}
                QPushButton:hover {{ background-color: #FDECEF; }}
            """)
            del_btn.clicked.connect(lambda _, ab=a: self._delete_abono(ab))
            row_lo.addWidget(del_btn)

            self.abonos_list_lo.addWidget(row)

        self.abonos_list_lo.addStretch()

    def _add_abono(self):
        if not self.selected_patient_id:
            return

        try:
            date = self.date_field.date().toString("yyyy-MM-dd")
            desc = self.desc_field.text().strip()
            add_abono(self.selected_patient_id, self.amount_field.text().strip(), date, desc)
            self.amount_field.clear()
            self.desc_field.clear()
            self.date_field.setDate(QDate.currentDate())
            if self.navigate_callback:
                self.navigate_callback("abonos")
        except ValueError as ex:
            QMessageBox.warning(self, "Error", str(ex))

    def _edit_abono(self, abono):
        dialog = _AbonoEditDialog(abono, parent=self)
        if dialog.exec() != QDialog.Accepted:
            return
        date, amount_text, desc = dialog.get_data()
        try:
            update_abono(self.selected_patient_id, abono.id, amount_text, date, desc)
            if self.navigate_callback:
                self.navigate_callback("abonos")
        except ValueError as ex:
            QMessageBox.warning(self, "Error", str(ex))

    def _delete_abono(self, abono):
        answer = QMessageBox.question(
            self, "Eliminar abono",
            f"¿Eliminar el abono de ${abono.amount:.2f} del {abono.date or '—'}?\n"
            "Los saldos posteriores se recalcularán.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if answer != QMessageBox.Yes:
            return
        try:
            delete_abono(self.selected_patient_id, abono.id)
            if self.navigate_callback:
                self.navigate_callback("abonos")
        except ValueError as ex:
            QMessageBox.warning(self, "Error", str(ex))


class _AbonoEditDialog(QDialog):
    def __init__(self, abono, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar abono")
        self.setMinimumWidth(380)
        self.setStyleSheet(f"background-color: {White};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Editar abono")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        layout.addWidget(title)

        date_lbl = QLabel("Fecha")
        date_lbl.setFont(QFont("Segoe UI", 10))
        date_lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")
        layout.addWidget(date_lbl)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setFont(QFont("Segoe UI", 10))
        self.date_edit.setFixedHeight(34)
        self.date_edit.setStyleSheet(f"""
            QDateEdit {{
                background-color: {pale_pink};
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                color: {Txt1};
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 24px;
                border: none;
            }}
        """)
        parsed = QDate.fromString(abono.date, "yyyy-MM-dd") if abono.date else QDate()
        self.date_edit.setDate(parsed if parsed.isValid() else QDate.currentDate())
        layout.addWidget(self.date_edit)

        amount_lbl = QLabel("Monto ($)")
        amount_lbl.setFont(QFont("Segoe UI", 10))
        amount_lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")
        layout.addWidget(amount_lbl)

        self.amount_edit = QLineEdit()
        self.amount_edit.setText(f"{abono.amount:.2f}" if abono.amount is not None else "")
        self.amount_edit.setFont(QFont("Segoe UI", 10))
        self.amount_edit.setFixedHeight(34)
        self.amount_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {pale_pink};
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                color: {Txt1};
            }}
        """)
        layout.addWidget(self.amount_edit)

        desc_lbl = QLabel("Descripción")
        desc_lbl.setFont(QFont("Segoe UI", 10))
        desc_lbl.setStyleSheet(f"color: {Txt2}; background: transparent;")
        layout.addWidget(desc_lbl)

        self.desc_edit = QLineEdit()
        self.desc_edit.setText(abono.description or "")
        self.desc_edit.setFont(QFont("Segoe UI", 10))
        self.desc_edit.setFixedHeight(34)
        self.desc_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {pale_pink};
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                color: {Txt1};
            }}
        """)
        layout.addWidget(self.desc_edit)

        note = QLabel("Los saldos posteriores se recalcularán automáticamente.")
        note.setFont(QFont("Segoe UI", 9))
        note.setStyleSheet(f"color: {Txt2}; background: transparent;")
        note.setWordWrap(True)
        layout.addWidget(note)

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
        return (
            self.date_edit.date().toString("yyyy-MM-dd"),
            self.amount_edit.text().strip(),
            self.desc_edit.text().strip(),
        )
