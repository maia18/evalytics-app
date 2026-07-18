import flet as ft
from components.core.constants.constants import *

def criar_card_controle_ciclo(layout, mudar_tela, page):
    status_ciclo = ft.Container(
        content=ft.Text("EM ANDAMENTO", color="white", size=12, weight="bold"),
        bgcolor="green600",
        padding=8,
        border_radius=15
    )

    return ft.Container(
        bgcolor=layout.cores[CARD],
        padding=25,
        border_radius=10,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=5, color="black12"),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text("Ciclo de Avaliação Ativo", size=14, color="grey600"),
                                ft.Row([ft.Text("Semestre 2026.1", size=22, weight="bold", color=COR_PRIMARIA), status_ciclo])
                            ]
                        ),
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.ElevatedButton(
                                    "Visão do Usuário",
                                    icon=ft.Icons.OPEN_IN_NEW,
                                    bgcolor="blue700",
                                    color="white",
                                    on_click=lambda _: mudar_tela("/formulario")
                                ),
                                ft.ElevatedButton(
                                    "Copiar Link",
                                    icon=ft.Icons.CONTENT_COPY,
                                    bgcolor="blue50",
                                    color="blue700",
                                    on_click=lambda _: setattr(page.snack_bar, 'open', True) or setattr(page.snack_bar, 'content', ft.Text("Link copiado para a área de transferência!")) or page.update()
                                )
                            ]
                        )
                    ]
                ),
                ft.Divider(color="grey200"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("342 respostas coletadas até o momento.", size=14, color="black87"),
                        ft.TextButton("Encerrar Ciclo", icon=ft.Icons.STOP_CIRCLE, style=ft.ButtonStyle(color="red700"))
                    ]
                )
            ]
        )
    )
