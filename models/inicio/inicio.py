import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from models.inicio.widgets.card_inicio import criar_card
from components.core.constants import *

def ViewInicio(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(page, TEXTOS_INICIO[0], TEXTOS_INICIO[1], mudar_tela=mudar_tela)

    conteudo = ft.Column(
        expand=True,
        controls=[
            ft.Container(
                bgcolor=layout.cores["CARD"],
                padding=25,
                border_radius=12,
                border=ft.Border(
                    left=ft.BorderSide(1, layout.cores["BORDA"]),
                    top=ft.BorderSide(1, layout.cores["BORDA"]),
                    right=ft.BorderSide(1, layout.cores["BORDA"]),
                    bottom=ft.BorderSide(1, layout.cores["BORDA"])
                ),
                content=ft.Column([
                    ft.Text(
                        TEXTOS_INICIO[2],
                        weight="bold",
                        size=20,
                        color=layout.cores["TEXTO_PRINCIPAL"]
                    ),
                    ft.ElevatedButton(
                        TEXTOS_INICIO[3],
                        bgcolor=COR_PRIMARIA,
                        color="white",
                        on_click=lambda e: mudar_tela("/formulario")
                    )
                ])
            ),
            ft.Container(height=20),
            ft.Row(
                wrap=True,
                spacing=20,
                run_spacing=20,
                controls=[
                    criar_card(layout, TEXTOS_AVALIACAO[0], TEXTOS_AVALIACAO[1], ft.Icons.ADD, "/formulario", mudar_tela),
                    criar_card(layout, TEXTOS_DASHBOARD[0], TEXTOS_DASHBOARD[1], ft.Icons.GRID_VIEW, "/dashboard", mudar_tela),
                    criar_card(layout, TEXTOS_CURSOS[0], TEXTOS_CURSOS[1], ft.Icons.MENU_BOOK, "/cursos", mudar_tela),
                    criar_card(layout, TEXTOS_RELATORIOS[0], TEXTOS_RELATORIOS[1], ft.Icons.PIE_CHART, "/relatorios", mudar_tela),
                ]
            )
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/inicio")