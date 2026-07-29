import flet as ft
from views.principalView import sideBar, principalContainer
from views.formPatient import formPatientView

Bg = "#FDF6F6"

def main(page: ft.Page):
    page.title = "Clínica Odontológica - Dra. Raquel Virguez"
    page.bgcolor = Bg
    page.padding = 0
    page.window.width = 1200
    page.window.height = 700

    content_area = ft.Column(expand=True)

    def navigate(view, patientID=None):
        content_area.controls.clear()

        if view == "principal":
            content_area.controls.append(principalContainer(page, navigate))
        elif view == "form":
            def go_back():
                navigate("principal")
            content_area.controls.append(formPatientView(page, patientID, go_back))

        page.update()

    navigate("principal")

    page.add(ft.Row([
        sideBar(navigate),
        content_area
    ], expand=True))

ft.run(main)
