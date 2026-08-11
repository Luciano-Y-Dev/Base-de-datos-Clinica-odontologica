import sys
import os
import logging
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFileDialog, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
import platformdirs
from views.principal_view import PrincipalView
from views.form_patient import FormPatient
from views.patient_detail_view import PatientDetailView
from views.abonos_view import AbonosView
from views.export_view import ExportView
from database.migrations import initialize_database
from services import backup_service
from services.patient_service import (
    get_patients_ordered, get_patients_with_remaining,
    get_patient_full_data, get_odontogram_details,
    filter_patients
)
from services.abono_service import get_patients_paid, get_patient_abonos, get_patients_with_remaining as get_patients_pending

_APP_NAME = "clinica_odontologica"


def _setup_logging():
    log_dir = os.path.join(platformdirs.user_data_dir(_APP_NAME, appauthor=False), "logs")
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


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

    def _make_principal_view(self):
        return PrincipalView(
            patients=get_patients_with_remaining(),
            filter_fn=filter_patients,
            navigate_callback=self.navigate
        )

    def _make_form_view(self, patient_id):
        data = None
        if patient_id:
            data = get_patient_full_data(patient_id)
            if data:
                data["has_abonos"] = len(get_patient_abonos(patient_id)) > 0
                if data["odontograma"]:
                    data["odontograma_details"] = get_odontogram_details(data["odontograma"].id)
                else:
                    data["odontograma_details"] = []
        view = FormPatient(data=data, navigate_callback=self.navigate)
        view.saved.connect(self._on_saved)
        return view

    def navigate(self, action, patient_id=None):
        if action == "principal":
            self._switch_view(self._make_principal_view())
        elif action == "form":
            self._switch_view(self._make_form_view(patient_id))
        elif action == "add_tratamiento":
            view = self._make_form_view(patient_id)
            self._switch_view(view)
            QTimer.singleShot(0, view.prompt_new_tratamiento)
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
        elif action == "backup":
            self._run_backup()
        elif action == "restore":
            self._run_restore()

    def _run_backup(self):
        dest = QFileDialog.getExistingDirectory(
            self, "Elegir carpeta donde guardar el respaldo (ej. USB)"
        )
        if not dest:
            return
        try:
            path = backup_service.create_backup(dest)
            QMessageBox.information(self, "Respaldo creado", f"Respaldo guardado en:\n{path}")
        except Exception as ex:
            logging.getLogger(__name__).exception("Error al crear respaldo")
            QMessageBox.critical(self, "Error", f"No se pudo crear el respaldo:\n{ex}")

    def _run_restore(self):
        answer = QMessageBox.question(
            self, "Restaurar respaldo",
            "Se reemplazarán TODOS los datos actuales por los del respaldo.\n"
            "Se creará primero un respaldo de seguridad del estado actual.\n\n"
            "¿Deseas continuar?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if answer != QMessageBox.Yes:
            return
        src = QFileDialog.getExistingDirectory(
            self, "Selecciona la carpeta del respaldo (debe contener Clinica.db)"
        )
        if not src:
            return
        try:
            backup_service.restore_backup(src)
            QMessageBox.information(self, "Restaurado", "El respaldo se restauró correctamente.")
            self.navigate("principal")
        except Exception as ex:
            logging.getLogger(__name__).exception("Error al restaurar respaldo")
            QMessageBox.critical(self, "Error", f"No se pudo restaurar el respaldo:\n{ex}")

    def _on_saved(self):
        self._switch_view(self._make_principal_view())


def main():
    _setup_logging()
    initialize_database()

    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "clinica-icon.ico")
    app.setWindowIcon(QIcon(icon_path))
    app.aboutToQuit.connect(backup_service.auto_backup)
    window = MainW()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("clinica.odontologica.app")
    main()
