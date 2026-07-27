import flet as ft

Primary = "#C9929B"
Bg = "#FDF6F6"
Second = "#D4758C"
Txt1 = "#1A1A2E"
Txt2 = "#6C757D"

def sideBar():
    def hover(e):
        e.control.bgcolor = Second if e.data else Primary
        e.control.update()

    return ft.Container(
        content=ft.Column(
            [ft.Container(
                content=ft.Text("Pacientes", 
                                color=ft.Colors.WHITE, 
                                weight=ft.FontWeight.W_500),
                on_hover=hover, 
                bgcolor=Primary, 
                padding=10),

             ft.Container(
                content=ft.Text("Abonos", 
                                color=ft.Colors.WHITE, 
                                weight=ft.FontWeight.W_500),
                on_hover=hover, 
                bgcolor=Primary, 
                padding=10),

             ft.Container(
                content=ft.Text("Exportar Datos", 
                                color=ft.Colors.WHITE, 
                                weight=ft.FontWeight.W_500),
                on_hover=hover, 
                bgcolor=Primary, 
                padding=10)]
        ),
        bgcolor=Primary,
        width=200,
        padding=20,
        border_radius= 27
    )

def customeButtom(textbuttom):
    return ft.Button(
        textbuttom,
        bgcolor=Second,
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

def cardPatient():
    return ft.Container(
        content=ft.Row([
            ft.Text("Nombre", 
                    weight=ft.FontWeight.BOLD, color=Txt1),

            ft.Text("Edad", color=Txt2),

            ft.Text("Motivo de consulta", color=Txt2),

            ft.Text("Falta por abonar", color=Txt2)

        ], 
        spacing=20, 
        vertical_alignment=ft.CrossAxisAlignment.CENTER),

        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, Primary),
        border_radius=12,
        padding=16,
        width=840,
    )

def content():
    return ft.Column([
        ft.Text("Clínica Odontológica",
                size=28, 
                weight=ft.FontWeight.BOLD, 
                color=Txt1),

        ft.Text("Dra. Raquel Virguez", 
                size=18, 
                color=Txt2),

        ft.Divider(color=Primary),

        ft.Row([
            customeButtom("Añadir Paciente"),
            customeButtom("Actualizar balances"),
        ],
        alignment=ft.MainAxisAlignment.CENTER),

        ft.Column([cardPatient(), 
                   cardPatient(), 
                   cardPatient()],
                  alignment=ft.MainAxisAlignment.CENTER,
                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                  spacing=12)
    ], 
    expand=True, 
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def principalContainer():
    return ft.Row([sideBar(), 
                   content()], 
                   expand=True
                   )

def main(page: ft.Page):
    page.title = "Clínica Odontológica - Dra. Raquel Virguez"
    page.bgcolor = Bg
    page.padding = 24
    page.window.width = 1200
    page.window.height = 700
    page.add(principalContainer())

ft.run(main)
