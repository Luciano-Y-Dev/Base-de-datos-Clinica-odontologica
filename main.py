import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QIcon
from views.principal_view import PrincipalView
from views.form_patient import FormPatient
from views.patient_detail_view import PatientDetailView
from views.abonos_view import AbonosView
from views.export_view import ExportView
from database.createDB import (
    createTable_PACIENTES, createTable_ANTECEDENTES,
    createTable_EXAMEN, createTable_ODONTOGRAMA,
    createTable_ODONTOGRAMA_DETAILS, createTable_TRATAMIENTO,
    migrateTRATAMIENTO_add_date, createTable_ABONO
)
from services.patient_service import (
    get_patients_ordered, get_patients_with_remaining,
    get_patient_full_data, get_odontogram_details,
    filter_patients
)
from services.abono_service import get_patients_paid, get_patient_abonos, get_patients_with_remaining as get_patients_pending


class MainW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clínica Odontológica")
        self.setFixedSize(1200, 800)
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "clinica-icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FDF2F4;
            }
            QWidget {
                background-color: #FDF2F4;
            }
            QCalendarWidget {
                background-color: white;
            }
            QCalendarWidget QWidget {
                background-color: white;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
            }
            QScrollBar::handle:vertical {
                background: #D1D5DB;
                border-radius: 3px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9CA3AF;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self._build_ui()

    def _build_ui(self):
        patients = get_patients_with_remaining()
        view = PrincipalView(
            patients=patients,
            filter_fn=filter_patients,
            navigate_callback=self.navigate
        )
        self.stack.addWidget(view)

    def _switch_view(self, view):
        old = self.stack.currentWidget()
        self.stack.addWidget(view)
        self.stack.setCurrentWidget(view)
        if old:
            self.stack.removeWidget(old)
            old.deleteLater()

    def navigate(self, action, patient_id=None):
        if action == "principal":
            patients = get_patients_with_remaining()
            view = PrincipalView(
                patients=patients,
                filter_fn=filter_patients,
                navigate_callback=self.navigate
            )
            self._switch_view(view)
        elif action == "form":
            data = None
            if patient_id:
                data = get_patient_full_data(patient_id)
                if data:
                    abonos = get_patient_abonos(patient_id)
                    data["last_abono"] = abonos[-1] if abonos else None
                    if data["odontograma"]:
                        data["odontograma_details"] = get_odontogram_details(data["odontograma"].id)
                    else:
                        data["odontograma_details"] = []
            view = FormPatient(data=data, navigate_callback=self.navigate)
            view.saved.connect(self._on_saved)
            self._switch_view(view)
        elif action == "detail":
            data = get_patient_full_data(patient_id) if patient_id else None
            if data:
                data["abonos"] = get_patient_abonos(patient_id)
                if data["odontograma"]:
                    data["odontograma_details"] = get_odontogram_details(data["odontograma"].id)
                else:
                    data["odontograma_details"] = []
            view = PatientDetailView(data=data, navigate_callback=self.navigate)
            self._switch_view(view)
        elif action == "abonos":
            view = AbonosView(
                patients_pending=get_patients_pending(),
                patients_paid=get_patients_paid(),
                load_abonos_fn=get_patient_abonos,
                navigate_callback=self.navigate
            )
            self._switch_view(view)
        elif action == "export":
            view = ExportView(
                patients=get_patients_ordered(),
                navigate_callback=self.navigate
            )
            self._switch_view(view)

    def _on_saved(self):
        patients = get_patients_with_remaining()
        view = PrincipalView(
            patients=patients,
            filter_fn=filter_patients,
            navigate_callback=self.navigate
        )
        self._switch_view(view)


def main():
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("clinica.odontologica.app")

    createTable_PACIENTES()
    createTable_ANTECEDENTES()
    createTable_EXAMEN()
    createTable_ODONTOGRAMA()
    createTable_ODONTOGRAMA_DETAILS()
    createTable_TRATAMIENTO()
    migrateTRATAMIENTO_add_date()
    createTable_ABONO()

    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "clinica-icon.ico")
    app.setWindowIcon(QIcon(icon_path))
    window = MainW()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
