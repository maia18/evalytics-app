import flet as ft
from typing import Callable

from components.landing.palette import FUNDO, FUNDO_CABECALHO
from components.landing.hero.painel import criar_painel_hero
from components.landing.hero.texto import criar_hero_texto
from components.landing.transicao import criar_fluxo_animado, preparar_entrada


def criar_hero(
    page: ft.Page,
    mudar_tela: Callable[[str], None],
    ir_para_recursos: Callable,
) -> ft.Container:
    """Abertura institucional com uma prévia amigável da plataforma."""
    return ft.Container(
        bgcolor=FUNDO_CABECALHO,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=[FUNDO_CABECALHO, "#20152E", FUNDO],
        ),
        clip_behavior=ft.ClipBehavior.NONE,
        content=ft.Stack(
            clip_behavior=ft.ClipBehavior.NONE,
            controls=[
                *criar_fluxo_animado(page, 560),
                preparar_entrada(
                    page,
                    ft.Container(
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
                    ),
                    0.15,
                ),
            ],
        ),
    )
