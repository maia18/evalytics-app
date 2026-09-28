import flet as ft
from typing import Callable

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
)


def criar_hero_texto(
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
) -> ft.Column:

    return ft.Column(
        spacing=18,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Text(
                "AVALIAÇÃO INSTITUCIONAL",
                size=13,
                weight=ft.FontWeight.BOLD,
                color=COR_PRIMARIA,
            ),

            ft.Text(
                "Transforme avaliações\nem melhorias.",
                size=42,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
            ),

            ft.Container(
                content=ft.Text(
                    "Uma plataforma para coletar, organizar e "
                    "analisar avaliações institucionais, "
                    "apoiando a tomada de decisões e a "
                    "melhoria contínua.",
                    size=17,
                    color=COR_TEXTO_SECUNDARIO,
                ),
            ),

            ft.Container(height=5),

            ft.ResponsiveRow(
                columns=12,
                run_spacing=10,
                controls=[
                    ft.Container(
                        col={
                            "xs": 12,
                            "sm": 12,
                            "md": 6,
                            "lg": 6,
                            "xl": 6,
                        },
                        content=ft.ElevatedButton(
                            "Começar agora",
                            bgcolor=COR_PRIMARIA,
                            color=ft.Colors.WHITE,
                            height=48,
                            width=190,
                            on_click=lambda e: mudar_tela("/login"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=8,
                                ),
                                padding=ft.Padding.symmetric(
                                    horizontal=25,
                                ),
                            ),
                        ),
                    ),

                    ft.Container(
                        col={
                            "xs": 12,
                            "sm": 12,
                            "md": 6,
                            "lg": 6,
                            "xl": 6,
                        },
                        content=ft.OutlinedButton(
                            "Conhecer a plataforma",
                            height=48,
                            width=210,
                            on_click=ir_para_recursos,
                            style=ft.ButtonStyle(
                                color=COR_PRIMARIA,
                                side=ft.BorderSide(
                                    1,
                                    COR_PRIMARIA,
                                ),
                                shape=ft.RoundedRectangleBorder(
                                    radius=8,
                                ),
                                padding=ft.Padding.symmetric(
                                    horizontal=25,
                                ),
                            ),
                        ),
                    ),
                ],
            ),
        ],
    )