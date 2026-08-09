from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from services.patient_service import get_patients_ordered, delete_patient
from views.components.patient_card import PatientCard

Primary = "#C9929B"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"


class SidebarButton(QPushButton):
    def __init__(self, text, active=False, navigate_callback=None, nav_target=None, parent=None):
        super().__init__(text, parent)
        self.navigate_callback = navigate_callback
        self.nav_target = nav_target
        self._active = active
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(44)
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        self._update_style()

        if self.navigate_callback and self.nav_target:
            self.clicked.connect(lambda: self.navigate_callback(self.nav_target))

    def set_active(self, active):
        self._active = active
        self._update_style()

    def _update_style(self):
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {White};
                    color: {Primary};
                    border: none;
                    border-radius: 12px;
                    padding: 0 16px;
                    text-align: left;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: rgba(255, 255, 255, 0.75);
                    border: none;
                    border-radius: 12px;
                    padding: 0 16px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.15);
                    color: white;
                }}
            """)


class Sidebar(QFrame):
    def __init__(self, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.setFixedWidth(220)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Primary};
                border-radius: 20px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 28, 16, 20)
        layout.setSpacing(8)

        brand = QLabel("Clínica")
        brand.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        brand.setStyleSheet("color: white; background: transparent;")
        layout.addWidget(brand)

        brand_sub = QLabel("Odontológica")
        brand_sub.setFont(QFont("Segoe UI", 11))
        brand_sub.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        layout.addWidget(brand_sub)

        layout.addSpacing(36)

        nav_items = [
            ("Pacientes", "principal", True),
            ("Abonos", "abonos", False),
            ("Exportar datos", "export", False),
        ]

        self._buttons = []
        for label, target, is_active in nav_items:
            btn = SidebarButton(label, active=is_active, navigate_callback=navigate_callback, nav_target=target)
            self._buttons.append((target, btn))
            layout.addWidget(btn)

        layout.addStretch()

        doctor = QLabel("Dra. Raquel Virguez")
        doctor.setFont(QFont("Segoe UI", 9))
        doctor.setStyleSheet("color: rgba(255, 255, 255, 0.7); background: transparent;")
        layout.addWidget(doctor)

    def set_active(self, target):
        for t, btn in self._buttons:
            btn.set_active(t == target)


class PrincipalView(QWidget):
    navigate = Signal(str, object)

    def __init__(self, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.setStyleSheet(f"background-color: {pale_pink};")
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        sidebar = Sidebar(self.navigate_callback)
        root.addWidget(sidebar)

        content = QVBoxLayout()
        content.setContentsMargins(28, 28, 28, 28)
        content.setSpacing(0)

        title = QLabel("Clínica Odontológica")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Txt1}; background: transparent;")
        content.addWidget(title)

        content.addSpacing(4)

        subtitle = QLabel("Dra. Raquel Virguez")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet(f"color: {Txt2}; background: transparent;")
        content.addWidget(subtitle)

        content.addSpacing(20)

        patients = get_patients_ordered()

        if patients:
            add_row = QHBoxLayout()
            add_row.setContentsMargins(0, 0, 0, 0)

            add_btn = QPushButton("Añadir Paciente")
            add_btn.setFixedHeight(42)
            add_btn.setCursor(Qt.PointingHandCursor)
            add_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
            add_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Second};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 0 24px;
                }}
                QPushButton:hover {{
                    background-color: #C0607A;
                }}
                QPushButton:pressed {{
                    background-color: #A84860;
                }}
            """)
            if self.navigate_callback:
                add_btn.clicked.connect(lambda: self.navigate_callback("form", None))
            add_row.addWidget(add_btn)
            add_row.addStretch()
            content.addLayout(add_row)

            content.addSpacing(20)

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
            cards_layout.setSpacing(12)

            for p in patients:
                card = PatientCard(p, self.navigate_callback)
                card.edit_clicked.connect(self._on_edit)
                card.delete_clicked.connect(self._on_delete)
                cards_layout.addWidget(card)

            cards_layout.addStretch()
            scroll.setWidget(cards)
            content.addWidget(scroll, 1)
        else:
            empty = QWidget()
            empty.setStyleSheet("background: transparent;")
            empty_layout = QVBoxLayout(empty)
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_layout.setSpacing(12)

            empty_text = QLabel("No hay registros aún :)")
            empty_text.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))
            empty_text.setAlignment(Qt.AlignCenter)
            empty_text.setStyleSheet(f"color: {Txt1}; background: transparent;")
            empty_layout.addWidget(empty_text)

            empty_desc = QLabel("Añade tu primer paciente para comenzar")
            empty_desc.setFont(QFont("Segoe UI", 11))
            empty_desc.setAlignment(Qt.AlignCenter)
            empty_desc.setStyleSheet(f"color: {Txt2}; background: transparent;")
            empty_layout.addWidget(empty_desc)

            empty_layout.addSpacing(8)

            empty_btn = QPushButton("Añadir Paciente")
            empty_btn.setFixedHeight(42)
            empty_btn.setCursor(Qt.PointingHandCursor)
            empty_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
            empty_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Second};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 0 28px;
                }}
                QPushButton:hover {{
                    background-color: #C0607A;
                }}
                QPushButton:pressed {{
                    background-color: #A84860;
                }}
            """)
            if self.navigate_callback:
                empty_btn.clicked.connect(lambda: self.navigate_callback("form", None))
            empty_layout.addWidget(empty_btn, alignment=Qt.AlignCenter)

            content.addWidget(empty, 1)

        root.addLayout(content, 1)

    def _on_edit(self, patient_id):
        if self.navigate_callback:
            self.navigate_callback("form", patient_id)

    def _on_delete(self, patient_id):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar eliminación")
        msg.setText("¿Estás seguro de que quieres eliminar este paciente?")
        msg.setInformativeText("Esta acción no se puede deshacer.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        if msg.exec() == QMessageBox.Yes:
            try:
                delete_patient(patient_id)
                if self.navigate_callback:
                    self.navigate_callback("principal")
            except Exception as ex:
                err = QMessageBox()
                err.setIcon(QMessageBox.Critical)
                err.setWindowTitle("Error")
                err.setText(f"Error al eliminar: {ex}")
                err.exec()
