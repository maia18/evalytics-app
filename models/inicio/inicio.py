import flet as ft
from components.layout.responsive.responsive import ResponsiveLayout
from components.core.theme.theme import AppColors
from models.inicio.widgets.card_inicio import criar_card

def ViewInicio(page: ft.Page, mudar_tela):
    layout = ResponsiveLayout(page, "Início", "Bem-vindo ao Evalytics", mudar_tela=mudar_tela)

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
                        "Sistema de Avaliação Institucional",
                        weight="bold",
                        size=20,
                        color=layout.cores["TEXTO_PRINCIPAL"]
                    ),
                    ft.ElevatedButton(
                        "Iniciar nova avaliação",
                        bgcolor=AppColors.PRIMARIA,
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
                    criar_card(layout, "Nova Avaliação", "Criar um novo instrumento.", ft.Icons.ADD, "/formulario", mudar_tela),
                    criar_card(layout, "Dashboard", "Visão geral dos indicadores.", ft.Icons.GRID_VIEW, "/dashboard", mudar_tela),
                    criar_card(layout, "Cursos", "Consultar e organizar cursos.", ft.Icons.MENU_BOOK, "/cursos", mudar_tela),
                    criar_card(layout, "Relatórios", "Gerar relatórios.", ft.Icons.PIE_CHART, "/relatorios", mudar_tela),
                ]
            )
        ]
    )

    layout.add_content(conteudo)
    return layout.criar_view("/inicio")
