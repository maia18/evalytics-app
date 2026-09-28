import flet as ft

from components.core.constants.constants import (
    COR_TEXTO_TITULO,
    COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA,
    COR_CARD,
)

from components.landing.helpers import criar_etapa


def criar_secao_sobre() -> ft.Container:

    sobre_conteudo = ft.Column(
        spacing=16,
        controls=[
            ft.Text(
                "Sobre o Evalytics",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=COR_TEXTO_TITULO,
            ),

            ft.Text(
                "O Evalytics foi pensado para centralizar o processo "
                "de avaliação institucional em uma única plataforma.",
                size=16,
                color=COR_TEXTO_SECUNDARIO,
            ),

            ft.Text(
                "A proposta é facilitar a coleta, organização e "
                "análise das informações produzidas pelas avaliações, "
                "permitindo que esses dados sejam acompanhados de "
                "forma mais estruturada.",
                size=15,
                color=COR_TEXTO_SECUNDARIO,
            ),

            ft.Text(
                "Da avaliação à melhoria contínua.",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=COR_PRIMARIA,
            ),
        ],
    )

    sobre_visual = ft.Container(
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

    return ft.Container(
        key=ft.ScrollKey("sobre"),
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=75,
        ),
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            run_spacing=35,
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
                        right=20,
                    ),
                    content=sobre_conteudo,
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
                    content=sobre_visual,
                ),
            ],
        ),
    )