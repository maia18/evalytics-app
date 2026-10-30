import flet as ft
from typing import Callable
from components.landing.palette import ROXO, ROSA

def criar_cta(mudar_tela: Callable[[str], None]) -> ft.Container:
    """
    Cria o banner final centralizado de conversão (Call to Action).
        Layout verticalizado com título, subtítulo e botão de ação.
    """

    return ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=24,
            vertical=48,
        ),
        bgcolor="#271B33",
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=["#141119", "#48208A", ROXO, "#8248F8", ROSA, "#792F78", "#271B33", "#141119"],
            stops=[0, 0.16, 0.30, 0.48, 0.62, 0.78, 0.90, 1],
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[

                ft.Text(
                    "Toda melhoria começa com uma boa escuta.",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Text(
                    "Acesse o Evalytics e acompanhe as avaliações "
                    "da sua instituição.",
                    size=13,
                    color="#E9E3FF",
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Container(height=8),

                ft.ElevatedButton(
                    "Entrar na plataforma",
                    bgcolor=ft.Colors.WHITE,
                    color=ROXO,
                    height=48,
                    on_click=lambda e: mudar_tela("/login"),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=12,
                        ),
                        padding=ft.Padding.symmetric(
                            horizontal=28,
                        ),
                    ),
                ),
            ],
        ),
    )
