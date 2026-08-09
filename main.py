import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from views.principal_view import PrincipalView
from views.form_patient import FormPatient
from views.patient_detail_view import PatientDetailView
from views.abonos_view import AbonosView
from database.createDB import (
    createTable_PACIENTES, createTable_ANTECEDENTES,
    createTable_EXAMEN, createTable_ODONTOGRAMA,
    createTable_ODONTOGRAMA_DETAILS, createTable_TRATAMIENTO,
    createTable_ABONO
)


class MainW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clínica Odontológica")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FDF2F4;
            }
            QWidget {
                background-color: #FDF2F4;
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
        self._build_ui()

    def _build_ui(self):
        self.principal = PrincipalView(navigate_callback=self.navigate)
        self.setCentralWidget(self.principal)

    def navigate(self, action, patient_id=None):
        if action == "principal":
            self.principal = PrincipalView(navigate_callback=self.navigate)
            self.setCentralWidget(self.principal)
        elif action == "form":
            self.form = FormPatient(patient_id=patient_id, navigate_callback=self.navigate)
            self.form.saved.connect(self._on_saved)
            self.setCentralWidget(self.form)
        elif action == "detail":
            self.detail = PatientDetailView(patient_id=patient_id, navigate_callback=self.navigate)
            self.setCentralWidget(self.detail)
        elif action == "abonos":
            self.abonos = AbonosView(navigate_callback=self.navigate)
            self.setCentralWidget(self.abonos)
        elif action == "export":
            print("Exportar datos")

    def _on_saved(self):
        self.principal = PrincipalView(navigate_callback=self.navigate)
        self.setCentralWidget(self.principal)


def main():
    createTable_PACIENTES()
    createTable_ANTECEDENTES()
    createTable_EXAMEN()
    createTable_ODONTOGRAMA()
    createTable_ODONTOGRAMA_DETAILS()
    createTable_TRATAMIENTO()
    createTable_ABONO()

    app = QApplication(sys.argv)
    window = MainW()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
