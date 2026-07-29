import flet as ft
from utils import readTable_PACIENTES_ordered, readREMAINING
from createDB import deleteRow_PACIENTES

Primary = "#C9929B"
Second = "#D4758C"
Txt1 = "#1A1A2E"
Txt2 = "#6C757D"


def sideBar(navigate_callback=None):
    def hover(e):
        e.control.bgcolor = Second if e.data else Primary
        e.control.update()

    items = ["Pacientes", "Abonos", "Exportar Datos"]
    buttons = []
    for item in items:
        on_click_action = None
        if navigate_callback:
            if item == "Pacientes":
                on_click_action = lambda e: navigate_callback("principal")
        buttons.append(ft.Container(
            content=ft.Text(item, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
            on_hover=hover,
            on_click=on_click_action,
            bgcolor=Primary,
            padding=12,
            border_radius=8,
        ))

    return ft.Container(
        content=ft.Column(buttons, spacing=8),
        bgcolor=Primary,
        width=200,
        padding=16,
        margin=8,
        border_radius=20,
    )


def cardPatient(patient, navigate_callback, page):
    remaining = readREMAINING(patient[0])

    def on_edit(e):
        navigate_callback("form", patient[0])

    def on_delete(e):
        def confirm_delete(e):
            deleteRow_PACIENTES(patient[0])
            dialog.open = False
            page.update()
            navigate_callback("principal")

        def cancel_delete(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Eliminar a {patient[1]} {patient[2]}? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancel_delete),
                ft.TextButton("Eliminar", on_click=confirm_delete, style=ft.ButtonStyle(color="#E53935")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    return ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(f"{patient[1]} {patient[2]}",
                        weight=ft.FontWeight.BOLD, color=Txt1),
                ft.Text(f"Edad: {patient[3]} años - Fecha: {patient[5]}", color=Txt2),
                ft.Text(f"Motivo: {patient[10]}", color=Txt2),
            ], spacing=4, expand=True),

            ft.Column([
                ft.Text(f"Falta por abonar: ${remaining:.2f}", color=Txt2, size=14),
                ft.Row([
                    ft.Button("Editar", on_click=on_edit, bgcolor=Second, color=ft.Colors.WHITE,
                             style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                    ft.Button("Eliminar", on_click=on_delete, bgcolor="#E53935", color=ft.Colors.WHITE,
                             style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                ], spacing=8),
            ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.END),

        ],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.CENTER),

        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, Primary),
        border_radius=12,
        padding=16,
        expand=True,
    )


def principalContainer(page, navigate_callback):
    patients = readTable_PACIENTES_ordered()

    def on_add(e):
        navigate_callback("form", None)

    if not patients:
        content = ft.Column([
            ft.Text("Clínica Odontológica", size=28,
                    weight=ft.FontWeight.BOLD, color=Txt1),
            ft.Text("Dra. Raquel Virguez", size=18, color=Txt2),
            ft.Divider(color=Primary),
            ft.Text("Añada un registro :)", size=16, color=Txt2),
            ft.Button("Añadir Paciente", bgcolor=Second, color=ft.Colors.WHITE,
                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                      on_click=on_add),
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        )
    else:
        header = ft.Column([
            ft.Text("Clínica Odontológica", size=28,
                    weight=ft.FontWeight.BOLD, color=Txt1),
            ft.Text("Dra. Raquel Virguez", size=18, color=Txt2),
            ft.Divider(color=Primary),
            ft.Row([
                ft.Button("Añadir Paciente", bgcolor=Second, color=ft.Colors.WHITE,
                          style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                          on_click=on_add),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        body = ft.ListView(
            controls=[cardPatient(p, navigate_callback, page) for p in patients],
            spacing=12,
            expand=True,
        )

        content = ft.Column([header, body], expand=True, spacing=12)

    return ft.Container(
        content=content,
        padding=24,
        expand=True,
    )
