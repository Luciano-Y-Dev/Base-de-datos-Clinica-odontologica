from fpdf import FPDF
from services.patient_service import (
    get_patient, get_patient_antecedentes, get_patient_examen,
    get_patient_odontogram, get_odontogram_details, get_patient_remaining,
    get_patient_tratamiento
)
from services.abono_service import get_patient_abonos


ANTECEDENT_LABELS = [
    ("Oido, nariz, garganta", "earNoseThroat"),
    ("Respiratorio", "respiratory"),
    ("Alergias", "allergy"),
    ("Cardiovascular", "cardiovascular"),
    ("Gastrointestinal", "gastrointestinal"),
    ("Endocrino", "endocrine"),
    ("Renal", "renal"),
    ("Hepatico", "hepatic"),
    ("Neurologico", "neurologic"),
    ("Neoplastico", "neoplastic"),
    ("Sanguineo", "blood"),
    ("Viral", "viral"),
    ("Ginecologico", "gynecologic"),
    ("Covid", "covid"),
    ("VIH", "hiv"),
    ("Cirugias", "surgeries"),
    ("Medicamentos", "medications"),
    ("Vacuna hepatitis", "hepatitisVaccine"),
    ("Vacuna covid", "covidVaccine"),
    ("Historial familiar", "familyHistory"),
]


def _safe(val):
    if val is None:
        return ""
    return str(val)


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "Clinica Odontologica", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 5, "Dra. Raquel Virguez", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(201, 146, 155)
        self.set_text_color(255, 255, 255)
        self.cell(0, 7, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def field_row(self, label, value):
        v = _safe(value)
        if not v:
            return
        self.set_font("Helvetica", "B", 9)
        self.cell(50, 5, f"{label}:", new_x="END")
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, v, new_x="LMARGIN", new_y="NEXT")

    def antecedentes_row(self, label, value):
        v = _safe(value)
        if not v:
            return
        display = v[5:] if v.startswith("Si - ") else v
        self.set_font("Helvetica", "B", 9)
        self.cell(50, 5, f"{label}:", new_x="END")
        self.set_font("Helvetica", "", 9)
        self.cell(0, 5, display, new_x="LMARGIN", new_y="NEXT")


def generate_patients_pdf(patient_ids: list[int], output_path: str) -> str:
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    for idx, pid in enumerate(patient_ids):
        paciente = get_patient(pid)
        if not paciente:
            continue

        antecedentes = get_patient_antecedentes(pid)
        examen = get_patient_examen(pid)
        odontograma = get_patient_odontogram(pid)
        remaining = get_patient_remaining(pid)
        abonos = get_patient_abonos(pid)
        tratamientos = get_patient_tratamiento(pid)

        odonto_details = []
        if odontograma:
            odonto_details = get_odontogram_details(odontograma.id)

        pdf.add_page()

        pdf.set_font("Helvetica", "B", 13)
        full_name = f"{paciente.name} {paciente.lastName}"
        pdf.cell(0, 8, full_name, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        pdf.section_title("Datos Personales")
        pdf.field_row("Nombre", paciente.name)
        pdf.field_row("Apellido", paciente.lastName)
        pdf.field_row("Edad", f"{paciente.age} anios")
        pdf.field_row("CI", paciente.CI)
        pdf.field_row("Fecha de ingreso", paciente.entryDate)
        pdf.field_row("Telefono", paciente.phoneNumber)
        pdf.field_row("Direccion", paciente.home)
        pdf.field_row("Representante", paciente.representName)
        pdf.field_row("CI Representante", paciente.representCI)
        pdf.field_row("Motivo de consulta", paciente.consultReason)
        pdf.field_row("Sintomatologia", paciente.presentIssues)
        pdf.ln(2)

        if antecedentes:
            pdf.section_title("Antecedentes Personales")
            for label, fname in ANTECEDENT_LABELS:
                pdf.antecedentes_row(label, getattr(antecedentes, fname))
            pdf.ln(2)

        if examen:
            pdf.section_title("Examen Fisico")
            pdf.field_row("Extraoral", examen.extraoral)
            pdf.field_row("Intraoral TB", examen.intraoralTB)
            pdf.field_row("Intraoral TD", examen.intraoralTD)
            pdf.field_row("Periodontal", examen.periodontal)
            pdf.field_row("PA", examen.PA)
            pdf.ln(2)

        if odontograma:
            pdf.section_title("Odontograma")
            if odontograma.notes:
                pdf.field_row("Notas", odontograma.notes)
            if odonto_details:
                pdf.set_font("Helvetica", "B", 9)
                col_w = [20, 25, 35, 90]
                headers = ["Diente", "Cara", "Afectacion", "Descripcion"]
                for i, h in enumerate(headers):
                    pdf.cell(col_w[i], 5, h, border=1, new_x="END")
                pdf.ln()
                pdf.set_font("Helvetica", "", 9)
                for d in odonto_details:
                    vals = [_safe(d[2]), _safe(d[3]), _safe(d[4]), _safe(d[5])]
                    for i, v in enumerate(vals):
                        pdf.cell(col_w[i], 5, v, border=1, new_x="END")
                    pdf.ln()
            pdf.ln(2)

        if tratamientos:
            pdf.section_title("Tratamientos")
            for t in tratamientos:
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(30, 5, _safe(t.date) or "Sin fecha", new_x="END")
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 5, _safe(t.diagnosis), new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            pdf.ln(2)

        if abonos:
            pdf.section_title("Abonos")
            pdf.set_font("Helvetica", "B", 9)
            col_w = [30, 50, 30, 30, 30]
            headers = ["Fecha", "Descripcion", "Costo", "Abono", "Resta"]
            for i, h in enumerate(headers):
                pdf.cell(col_w[i], 5, h, border=1, new_x="END")
            pdf.ln()
            pdf.set_font("Helvetica", "", 9)
            for a in abonos:
                vals = [
                    _safe(a.date),
                    _safe(a.description),
                    f"${_safe(a.treatmentCost)}",
                    f"${_safe(a.amount)}",
                    f"${_safe(a.remaining)}",
                ]
                for i, v in enumerate(vals):
                    pdf.cell(col_w[i], 5, v, border=1, new_x="END")
                pdf.ln()
            pdf.ln(2)

            pdf.set_font("Helvetica", "B", 10)
            pdf.cell(0, 6, f"Saldo pendiente: ${remaining:.2f}", new_x="LMARGIN", new_y="NEXT")

    pdf.output(output_path)
    return output_path
