import flet as ft

from components.router import obter_view

class Navigator:

    def __init__(self, page: ft.Page):
        self.page = page

    def go(self, rota: str):

        self.page.views.clear()

        view = obter_view(rota)

        self.page.views.append(view(self.page, self.go))

        self.page.update()