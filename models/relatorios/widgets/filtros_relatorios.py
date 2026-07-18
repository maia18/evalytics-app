import flet as ft
from components.core.constants.constants import *

def criar_secao_filtros(layout, borda_container):
    dropdown_semestre = ft.Dropdown(
        label="Semestre",
        options=[ft.dropdown.Option("2026.1"), ft.dropdown.Option("2025.2")],
        width=200,
        dense=True
    )

    dropdown_eixo = ft.Dropdown(
        label="Eixo Avaliativo",
        options=[
            ft.dropdown.Option("Infraestrutura"),
            ft.dropdown.Option("Didática"),
            ft.dropdown.Option("Atendimento")
        ],
        width=200,
        dense=True
    )

    return ft.Container(
        bgcolor=layout.cores[CARD],
        padding=20,
        border_radius=8,
        border=borda_container,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row([dropdown_semestre, dropdown_eixo], spacing=10),
                ft.Row([
                    ft.ElevatedButton("Exportar CSV", icon=ft.Icons.TABLE_VIEW, bgcolor="green700", color="white"),
                    ft.ElevatedButton("Gerar Documento (PDF)", icon=ft.Icons.PICTURE_AS_PDF, bgcolor="red700", color="white")
                ], spacing=10)
            ]
        )
    )
