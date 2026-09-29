import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_CARD,
    COR_PRIMARIA,
)

from components.landing.helpers import criar_etapa

def criar_sobre_visual() -> ft.Container:

    return ft.Container(
        width=420,
        height=270,
        padding=28,
        bgcolor=COR_CARD,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color=ft.Colors.BLACK12,
        ),
        content=ft.Column(
            spacing=18,
            controls=[
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Container(
                            width=10,
                            height=10,
                            bgcolor=COR_PRIMARIA,
                            border_radius=10,
                        ),

                        ft.Text(
                            "Fluxo de avaliação",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=COR_TEXTO_TITULO,
                        ),
                    ],
                ),

                criar_etapa(
                    "01",
                    "Avaliar",
                    "Coleta das percepções institucionais.",
                ),

                criar_etapa(
                    "02",
                    "Analisar",
                    "Organização dos resultados e indicadores.",
                ),

                criar_etapa(
                    "03",
                    "Melhorar",
                    "Informações para apoiar ações de melhoria.",
                ),
            ],
        ),
    )