import flet as ft
from typing import Callable

from components.landing.palette import FUNDO
from components.landing.hero.painel import criar_painel_hero
from components.landing.hero.texto import criar_hero_texto


def criar_hero(
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
) -> ft.Container:
    """Abertura institucional com uma prévia amigável da plataforma."""
    return ft.Container(
        bgcolor=FUNDO,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=[FUNDO, "#20152E", FUNDO],
        ),
        padding=ft.Padding.symmetric(horizontal=32, vertical=48),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=30,
            controls=[
                ft.ResponsiveRow(
                    columns=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    run_spacing=28,
                    controls=[
                        ft.Container(
                            col={"xs": 12, "sm": 12, "md": 6, "lg": 6, "xl": 6, "xxl": 6},
                            padding=ft.Padding.only(right=24),
                            content=criar_hero_texto(mudar_tela, ir_para_recursos),
                        ),
                        ft.Container(
                            col={"xs": 12, "sm": 12, "md": 6, "lg": 6, "xl": 6, "xxl": 6},
                            content=criar_painel_hero(),
                        ),
                    ],
                ),
            ],
        ),
    )
