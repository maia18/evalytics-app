import flet as ft
from typing import Callable

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_CARD,
)

from components.landing.helpers import criar_indicador


def criar_hero(
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
) -> ft.Container:

    # =========================================================
    # TEXTO
    # =========================================================

    hero_texto = ft.Column(
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
                                    radius=8
                                ),
                                padding=ft.Padding.symmetric(
                                    horizontal=25
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
                                    radius=8
                                ),
                                padding=ft.Padding.symmetric(
                                    horizontal=25
                                ),
                            ),
                        ),
                    ),
                ],
            ),
        ],
    )

    # =========================================================
    # PAINEL
    # =========================================================

    painel = ft.Container(
        width=430,
        padding=32,
        bgcolor=COR_CARD,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.BLACK12,
        ),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Visão geral",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=COR_TEXTO_TITULO,
                        ),

                        ft.Container(
                            padding=ft.Padding.symmetric(
                                horizontal=10,
                                vertical=5,
                            ),
                            bgcolor=ft.Colors.with_opacity(
                                0.10,
                                COR_PRIMARIA,
                            ),
                            border_radius=20,
                            content=ft.Text(
                                "Ativo",
                                size=11,
                                color=COR_PRIMARIA,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ],
                ),

                ft.Row(
                    spacing=15,
                    controls=[
                        criar_indicador(
                            "Avaliações",
                            "128",
                        ),

                        criar_indicador(
                            "Indicadores",
                            "24",
                        ),
                    ],
                ),

                ft.Container(
                    height=1,
                    bgcolor=ft.Colors.BLACK12,
                ),

                ft.Text(
                    "Acompanhamento institucional",
                    size=14,
                    color=COR_TEXTO_SECUNDARIO,
                ),

                ft.ProgressBar(
                    value=0.78,
                    color=COR_PRIMARIA,
                    bgcolor=ft.Colors.BLACK12,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "Progresso das avaliações",
                            size=12,
                            color=COR_TEXTO_SECUNDARIO,
                        ),

                        ft.Text(
                            "78%",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=COR_PRIMARIA,
                        ),
                    ],
                ),
            ],
        ),
    )

    # =========================================================
    # HERO RESPONSIVO
    # =========================================================

    return ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=60,
            vertical=90,
        ),
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 7,
                        "xl": 7,
                    },
                    padding=ft.Padding.only(
                        right=30,
                    ),
                    content=hero_texto,
                ),

                ft.Container(
                    col={
                        "xs": 12,
                        "sm": 12,
                        "md": 12,
                        "lg": 5,
                        "xl": 5,
                    },
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.only(
                        top=20,
                    ),
                    content=painel,
                ),
            ],
        ),
    )