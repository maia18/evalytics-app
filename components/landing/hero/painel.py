import flet as ft
from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_CARD,
)
from components.landing.helpers import criar_indicador

def criar_painel_hero() -> ft.Container:
    """Cria um card ilustrativo simulando o painel de controledo sistema."""

    return ft.Container(
        width=410,
        padding=28,
        bgcolor=COR_CARD,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=24,
            spread_radius=0,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 8),
        ),
        content=ft.Column(
            spacing=18,
            controls=[

                # =========================================================
                # CABEÇALHO
                # =========================================================

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
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

                # =========================================================
                # INDICADORES
                # =========================================================

                ft.Row(
                    spacing=14,
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

                # =========================================================
                # DIVISOR
                # =========================================================

                ft.Container(
                    height=1,
                    bgcolor=ft.Colors.BLACK12,
                ),

                # =========================================================
                # ACOMPANHAMENTO
                # =========================================================

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