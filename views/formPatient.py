import flet as ft
from createDB import (
    createRow_PACIENTES, updateRow_PACIENTES,
    createRow_ANTECEDENTES, updateRow_ANTECEDENTES,
    createRow_EXAMEN, updateRow_EXAMEN
)
from utils import readPACIENTE, readANTECEDENTES, readEXAMEN, existANTECEDENTES, existEXAMEN

Primary = "#C9929B"
PrimaryBorder = "#E8D5D8"
Second = "#D4758C"
Txt1 = "#1A1A2E"
Txt2 = "#6C757D"

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

def formPatientView(page, patientID=None, refresh_callback=None):
    isEdit = patientID is not None

    if isEdit:
        paciente = readPACIENTE(patientID)
        antecedentes = readANTECEDENTES(patientID)
        examen = readEXAMEN(patientID)
    else:
        paciente = None
        antecedentes = None
        examen = None

    def field(label, value="", keyboard=None, multiline=False, max_lines=1):
        return ft.TextField(
            label=label, value=value, text_size=13,
            keyboard_type=keyboard, multiline=multiline, max_lines=max_lines,
            border_color=PrimaryBorder, focused_border_color=Second,
            cursor_color=Txt1, label_style=ft.TextStyle(color=Txt2, size=12),
            text_style=ft.TextStyle(color=Txt1), expand=True, bgcolor=ft.Colors.WHITE,
        )

    nameF = field("Nombre(es)", paciente[1] if paciente else "")
    lastF = field("Apellido(s)", paciente[2] if paciente else "")
    ageF = field("Edad", str(paciente[3]) if paciente else "", keyboard=ft.KeyboardType.NUMBER)
    ciF = field("CI", str(paciente[4]) if paciente else "", keyboard=ft.KeyboardType.NUMBER)
    dateF = field("Fecha de Ingreso", paciente[5] if paciente else "")
    phoneF = field("Teléfono", paciente[6] if paciente else "")
    homeF = field("Dirección", paciente[7] if paciente else "")
    repNameF = field("Representante", paciente[8] if paciente else "")
    repCiF = field("CI Representante", str(paciente[9]) if paciente and paciente[9] else "", keyboard=ft.KeyboardType.NUMBER)
    motivF = field("Motivo de Consulta", paciente[10] if paciente else "")
    symptF = field("Sintomatología Actual", paciente[11] if paciente else "", multiline=True, max_lines=3)

    antChecks = []
    for i, (label, fname) in enumerate(ANTECEDENT_FIELDS):
        val = antecedentes[i + 2] if antecedentes else None
        checked = val is not None and val != ""
        ctxt = val[5:] if checked and val and val.startswith("Si - ") else ""

        cb = ft.Checkbox(label=label, value=checked, fill_color=Second, check_color=ft.Colors.WHITE,
                        label_style=ft.TextStyle(color=Txt1, size=12))
        tf = ft.TextField(value=ctxt, hint_text="Contexto...", visible=checked,
                         multiline=True, min_lines=1, max_lines=2, text_size=11,
                         border_color=PrimaryBorder, focused_border_color=Second,
                         cursor_color=Txt1, expand=True)
        antChecks.append((fname, cb, tf))

    def make_toggle(cb, tf):
        def on_change(e):
            tf.visible = cb.value
            page.update()
        return on_change

    for _, cb, tf in antChecks:
        cb.on_change = make_toggle(cb, tf)

    extF = field("Extraoral", examen[2] if examen else "")
    itbF = field("Intraoral TB", examen[3] if examen else "")
    itdF = field("Intraoral TD", examen[4] if examen else "")
    periF = field("Periodontal", examen[5] if examen else "")
    paF = field("PA", examen[6] if examen else "")

    def save(e):
        try:
            if isEdit:
                updateRow_PACIENTES(patientID, nameF.value, lastF.value,
                    int(ageF.value) if ageF.value else 0, int(ciF.value) if ciF.value else 0,
                    dateF.value, phoneF.value, homeF.value, repNameF.value,
                    int(repCiF.value) if repCiF.value else 0, motivF.value, symptF.value)
                cid = patientID
            else:
                cid = createRow_PACIENTES(nameF.value, lastF.value,
                    int(ageF.value) if ageF.value else 0, int(ciF.value) if ciF.value else 0,
                    dateF.value, phoneF.value, homeF.value, repNameF.value,
                    int(repCiF.value) if repCiF.value else 0, motivF.value, symptF.value)

            ad = [None]*20
            for idx, (_, cb, tf) in enumerate(antChecks):
                ad[idx] = f"Si - {tf.value}" if cb.value and tf.value else ("Si" if cb.value else None)
            if existANTECEDENTES(cid): updateRow_ANTECEDENTES(cid, *ad)
            else: createRow_ANTECEDENTES(cid, *ad)

            ed = [extF.value, itbF.value, itdF.value, periF.value, paF.value]
            if existEXAMEN(cid): updateRow_EXAMEN(cid, *ed)
            else: createRow_EXAMEN(cid, *ed)

            if refresh_callback: refresh_callback()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al guardar: {ex}", color=ft.Colors.WHITE),
                bgcolor="#E53935",
            )
            page.snack_bar.open = True
            page.update()

    def go_back(e):
        if refresh_callback: refresh_callback()

    def antItem(cb, tf):
        return ft.Container(
            content=ft.Column([cb, tf], spacing=4),
            border=ft.Border.all(1, PrimaryBorder),
            border_radius=6,
            padding=8,
            bgcolor=ft.Colors.WHITE,
            expand=True,
        )

    def buildAntGrid():
        left_items = [antItem(cb, tf) for _, cb, tf in antChecks[:10]]
        right_items = [antItem(cb, tf) for _, cb, tf in antChecks[10:]]
        return ft.Row([
            ft.Column(left_items, spacing=8, expand=True),
            ft.Column(right_items, spacing=8, expand=True),
        ], spacing=16, expand=True)

    title = f"Editar Ficha: {paciente[1]} {paciente[2]}" if isEdit and paciente else "Nuevo Registro de Paciente"

    return ft.Column([
        ft.Container(
            content=ft.Row([
                ft.Button("Volver", icon=ft.Icons.ARROW_BACK_ROUNDED, on_click=go_back,
                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), bgcolor=ft.Colors.WHITE, color=Txt1, side=ft.BorderSide(1, PrimaryBorder))),
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=Txt1),
                ft.Button("Guardar", icon=ft.Icons.SAVE_ROUNDED, bgcolor=Second, color=ft.Colors.WHITE, on_click=save,
                         style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE, border=ft.Border(bottom=ft.BorderSide(2, PrimaryBorder)), padding=16,
        ),

        ft.Container(
            content=ft.Column([
                ft.Text("Información Personal", size=14, weight=ft.FontWeight.W_600, color=Txt1),
                ft.Divider(height=1, color=PrimaryBorder),
                ft.Row([nameF, lastF], spacing=12, expand=True),
                ft.Row([ageF, ciF, dateF], spacing=12, expand=True),
                ft.Row([phoneF, homeF], spacing=12, expand=True),
                ft.Row([repNameF, repCiF], spacing=12, expand=True),
                motivF, symptF,
            ], spacing=10),
            bgcolor=ft.Colors.WHITE, border=ft.Border.all(1, PrimaryBorder), border_radius=10, padding=20,
        ),

        ft.Container(
            content=ft.Column([
                ft.Text("Antecedentes Personales", size=14, weight=ft.FontWeight.W_600, color=Txt1),
                ft.Divider(height=1, color=PrimaryBorder),
                buildAntGrid(),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE, border=ft.Border.all(1, PrimaryBorder), border_radius=10, padding=20,
        ),

        ft.Container(
            content=ft.Column([
                ft.Text("Examen Físico", size=14, weight=ft.FontWeight.W_600, color=Txt1),
                ft.Divider(height=1, color=PrimaryBorder),
                ft.Row([extF, itbF, itdF, periF, paF], spacing=12, expand=True),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE, border=ft.Border.all(1, PrimaryBorder), border_radius=10, padding=20,
        ),

        ft.Container(
            content=ft.Column([
                ft.Text("Odontograma / Tratamiento / Costo-Abono", size=14, weight=ft.FontWeight.W_600, color=Txt2),
                ft.Text("Sección reservada", size=12, color=Txt2),
            ], spacing=4),
            bgcolor=ft.Colors.GREY_100, border_radius=10, padding=20,
        ),
    ], spacing=16, expand=True, scroll=ft.ScrollMode.AUTO)
