import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QFont, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from services.patient_service import delete_patient
from views.components.patient_card import PatientCard
from views.components.search_filter import SearchFilter

Primary = "#C9929B"
Second = "#D4758C"
Txt1 = "#2D2D2D"
Txt2 = "#7A7A7A"
pale_pink = "#FDF2F4"
White = "#FFFFFF"


def load_svg(path, height, dpr=1.0):
    renderer = QSvgRenderer(path)
    size = renderer.defaultSize()
    width = int(size.width() * height / size.height())
    pixmap = QPixmap(int(width * dpr), int(height * dpr))
    pixmap.setDevicePixelRatio(dpr)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter, QRectF(0, 0, width, height))
    painter.end()
    return pixmap


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

        backup_btn = SidebarButton("Respaldar datos", navigate_callback=navigate_callback, nav_target="backup")
        layout.addWidget(backup_btn)

        restore_btn = SidebarButton("Restaurar respaldo", navigate_callback=navigate_callback, nav_target="restore")
        layout.addWidget(restore_btn)



    def set_active(self, target):
        for t, btn in self._buttons:
            btn.set_active(t == target)


class PrincipalView(QWidget):
    navigate = Signal(str, object)

    def __init__(self, patients=None, filter_fn=None, navigate_callback=None, parent=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self._all_patients = patients or []
        self._filter_fn = filter_fn
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

        logo_label = QLabel()
        logo_label.setStyleSheet("background: transparent;")
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "Logo.svg")
        logo_label.setPixmap(load_svg(logo_path, 140, self.devicePixelRatioF()))
        logo_label.setAlignment(Qt.AlignCenter)
        content.addWidget(logo_label)

        content.addSpacing(35)

        self._add_widget = QWidget()
        self._add_widget.setStyleSheet("background: transparent;")
        add_row = QHBoxLayout(self._add_widget)
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
        add_row.addStretch()
        add_row.addWidget(add_btn)
        add_row.addStretch()
        content.addWidget(self._add_widget)

        content.addSpacing(20)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QFrame.NoFrame)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: #D1D5DB; border-radius: 3px; min-height: 24px; }
            QScrollBar::handle:vertical:hover { background: #9CA3AF; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
        """)

        cards = QWidget()
        cards.setStyleSheet("background: transparent;")
        self._cards_layout = QVBoxLayout(cards)
        self._cards_layout.setContentsMargins(0, 0, 8, 0)
        self._cards_layout.setSpacing(12)

        for p in self._all_patients:
            card = PatientCard(p, navigate_callback=self.navigate_callback)
            card.delete_clicked.connect(self._on_delete)
            card.edit_clicked.connect(self._on_edit)
            card.add_tratamiento_clicked.connect(self._on_add_tratamiento)
            self._cards_layout.addWidget(card)

        self._cards_layout.addStretch()
        self._scroll_area.setWidget(cards)
        content.addWidget(self._scroll_area, 1)

        self._empty_widget = QWidget()
        self._empty_widget.setStyleSheet("background: transparent;")
        empty_layout = QVBoxLayout(self._empty_widget)
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
            empty_btn.clicked.connect(lambda: self.navigate_callback("form", None))
        empty_layout.addWidget(empty_btn, alignment=Qt.AlignCenter)

        content.addWidget(self._empty_widget, 1)

        self._toggle_btn = QPushButton("Buscar")
        self._toggle_btn.setFixedHeight(36)
        self._toggle_btn.setCursor(Qt.PointingHandCursor)
        self._toggle_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self._toggle_btn.setStyleSheet(f"""
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
        self._toggle_btn.clicked.connect(self._toggle_search)
        content.addSpacing(12)
        content.addWidget(self._toggle_btn, alignment=Qt.AlignLeft)

        self._search_filter = SearchFilter()
        self._search_filter.filter_changed.connect(self._on_filter_changed)
        content.addWidget(self._search_filter)
        self._search_filter.hide_frame()

        if self._all_patients:
            self._search_filter.update_results_label(len(self._all_patients), len(self._all_patients))

        if not self._all_patients:
            self._scroll_area.hide()
            self._add_widget.hide()
        else:
            self._empty_widget.hide()

        root.addLayout(content, 1)

    def _toggle_search(self):
        visible = not self._search_filter.is_frame_visible()
        if visible:
            self._search_filter.show_frame()
            self._toggle_btn.setText("Cerrar")
        else:
            self._search_filter.hide_frame()
            self._toggle_btn.setText("Buscar")
            self._refresh_patient_list(self._all_patients)

    def _on_filter_changed(self, search_text, date_from, date_to):
        filtered = self._filter_fn(self._all_patients, search_text, date_from, date_to)
        self._refresh_patient_list(filtered)
        self._search_filter.update_results_label(len(filtered), len(self._all_patients))

    def _refresh_patient_list(self, patients):
        if not hasattr(self, '_cards_layout') or not hasattr(self, '_scroll_area'):
            return

        while self._cards_layout.count():
            item = self._cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if patients:
            for p in patients:
                card = PatientCard(p, navigate_callback=self.navigate_callback)
                card.delete_clicked.connect(self._on_delete)
                card.edit_clicked.connect(self._on_edit)
                card.add_tratamiento_clicked.connect(self._on_add_tratamiento)
                self._cards_layout.addWidget(card)

            self._cards_layout.addStretch()
            self._scroll_area.show()
            self._add_widget.show()
            self._empty_widget.hide()
        else:
            self._scroll_area.hide()
            self._add_widget.hide()
            self._empty_widget.show()

    def _on_delete(self, patient_id):
        answer = QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este paciente?\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if answer == QMessageBox.Yes:
            try:
                delete_patient(patient_id)
                if self.navigate_callback:
                    self.navigate_callback("principal")
            except Exception as ex:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar: {ex}")

    def _on_edit(self, patient_id):
        if self.navigate_callback:
            self.navigate_callback("form", patient_id)

    def _on_add_tratamiento(self, patient_id):
        if self.navigate_callback:
            self.navigate_callback("add_tratamiento", patient_id)
