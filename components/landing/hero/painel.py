import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_CARD,
)

from components.landing.helpers import criar_indicador


def criar_painel_hero() -> ft.Container:

    return ft.Container(
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