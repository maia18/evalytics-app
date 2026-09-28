import flet as ft
from typing import Callable

from components.core.constants.constants import COR_PRIMARIA

def criar_cta(
    mudar_tela: Callable[[str], None],
) -> ft.Container:

    return ft.Container(
        margin=ft.Margin.symmetric(
            horizontal=20,
            vertical=30,
        ),
        padding=35,
        bgcolor=COR_PRIMARIA,
        border_radius=16,
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=20,
            controls=[
                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 8,
                        "lg": 8,
                        "xl": 8,
                    },
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(
                                "Pronto para começar?",
                                size=25,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),

                            ft.Text(
                                "Acesse o Evalytics e acompanhe "
                                "as avaliações da sua instituição.",
                                size=14,
                                color=ft.Colors.WHITE70,
                            ),
                        ],
                    ),
                ),

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 4,
                        "lg": 4,
                        "xl": 4,
                    },
                    alignment=ft.Alignment.CENTER,
                    content=ft.ElevatedButton(
                        "Entrar na plataforma",
                        bgcolor=ft.Colors.WHITE,
                        color=COR_PRIMARIA,
                        height=45,
                        on_click=lambda e: mudar_tela("/login"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(
                                radius=8,
                            ),
                            padding=ft.Padding.symmetric(
                                horizontal=24,
                            ),
                        ),
                    ),
                ),
            ],
        ),
    )