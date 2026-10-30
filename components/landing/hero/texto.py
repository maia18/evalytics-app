import flet as ft
from typing import Callable

from components.landing.palette import ROXO, ROXO_CLARO, TEXTO_CLARO, TEXTO_CLARO_SECUNDARIO


def criar_hero_texto(
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
) -> ft.Column:
    """Mensagem principal da apresentação institucional Qualtrics-inspired."""
    return ft.Column(
        spacing=18,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=12, vertical=7),
                border_radius=24,
                bgcolor="#2A2238",
                content=ft.Row(
                    tight=True,
                    spacing=7,
                    controls=[
                        ft.Icon(ft.Icons.AUTO_AWESOME, size=14, color=ROXO_CLARO),
                        ft.Text(
                            "AVALIAÇÃO INSTITUCIONAL, COM MAIS CLAREZA",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            color=ROXO_CLARO,
                        ),
                    ],
                ),
            ),
            ft.Column(
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text(
                        "Ouça sua comunidade.",
                        size=42,
                        weight=ft.FontWeight.BOLD,
                        color=TEXTO_CLARO,
                        text_align=ft.TextAlign.LEFT,
                    ),
                    ft.Text(
                        "Melhore com dados.",
                        size=42,
                        weight=ft.FontWeight.BOLD,
                        color=ROXO_CLARO,
                        text_align=ft.TextAlign.LEFT,
                    ),
                ],
            ),
            ft.Text(
                "Crie avaliações, acompanhe cada eixo e transforme as respostas "
                "da comunidade acadêmica em próximos passos concretos.",
                size=16,
                color=TEXTO_CLARO_SECUNDARIO,
                text_align=ft.TextAlign.LEFT,
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                spacing=12,
                run_spacing=8,
                wrap=True,
                controls=[
                    ft.ElevatedButton(
                        "Começar agora",
                        bgcolor=ROXO,
                        color=ft.Colors.WHITE,
                        height=48,
                        on_click=lambda e: mudar_tela("/login"),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=ft.Padding.symmetric(horizontal=22),
                        ),
                    ),
                    ft.TextButton(
                        "Conhecer recursos  ↓",
                        height=48,
                        style=ft.ButtonStyle(
                            color=TEXTO_CLARO,
                            padding=ft.Padding.symmetric(horizontal=12, vertical=12),
                        ),
                        on_click=ir_para_recursos,
                    ),
                ],
            ),
            ft.Text(
                "Feito para instituições que querem evoluir a partir da escuta.",
                size=12,
                color=TEXTO_CLARO_SECUNDARIO,
                text_align=ft.TextAlign.LEFT,
            ),
        ],
    )
