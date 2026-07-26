import flet as ft
from numpy import spacing

def sideBar():

    def hover(e):
        e.control.content.color = ft.Colors.BLUE_300 if e.data else ft.Colors.BLACK
        e.control.update()

    return ft.Column(
       [ft.Container(content= ft.Text("Pacientes"), on_hover= hover),
        ft.Container(content= ft.Text("Abonos"), on_hover= hover),
        ft.Container(content= ft.Text("Exportar Datos"), on_hover= hover)]
    )

def customeButtom(textbuttom: str):
    return ft.Button(f"{textbuttom}")


# Tiene que recibir un objeto paciente (Recordar crear la claseee)
def cardPatient():
    return ft.Button(
        content= ft.Row([
            ft.Text("Nombre"),
            ft.Text("Edad"),
            ft.Text("Motivo de consulta"),
            ft.Text("Falta por abonar")
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment = ft.CrossAxisAlignment.CENTER,
            spacing=20),
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
            )

def content():
    return ft.Column(
        [

         ft.Text("Clínica Odontológica - Dra. Raquel Virguez", size=32, weight=ft.FontWeight.BOLD),

         ft.Row([
             customeButtom("Añadir Paciente"),
             customeButtom("Actualizar balances"),
         ],
         alignment=ft.MainAxisAlignment.CENTER),

         ft.Container(
             content=ft.Column([
                 cardPatient(),
                 cardPatient(),
                 cardPatient(),
                 ], 
                 alignment=ft.MainAxisAlignment.CENTER,
                 horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                 width=840,
                 alignment=ft.Alignment.CENTER,
                 )

         ],

         expand=True,
         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

def principalContainer():
    return ft.Row(
        [sideBar(),
        content()],
        expand=True
    )

def main(page: ft.Page):
    page.title = "Clínica Odontológica - Dra. Raquel Virguez"
    page.padding = 20
    page.window.width = 1200
    page.window.height = 700

    
    page.add(
        principalContainer()
    )

ft.run(main)
